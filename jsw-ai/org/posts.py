"""Post scheduling backend on content_items: each row is a planned post
(photo + platform + caption + hashtags + slot_time + status). The Approvals queue
and the Ayrshare posting service read this same table. Statuses:
draft -> pending_review -> approved -> posted (or rejected)."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(__file__))
import requests
import db
import model_data
import zen_client

PLATFORMS = ("instagram", "tiktok", "x", "youtube", "facebook", "reddit", "fanvue")


def _ensure():
    con = db.connect()
    try:
        con.execute("ALTER TABLE content_items ADD COLUMN hashtags TEXT")
        con.commit()
    except Exception:
        pass
    try:
        con.execute("ALTER TABLE content_items ADD COLUMN extra_paths TEXT")
        con.commit()
    except Exception:
        pass
    con.close()


def _pid(slug):
    con = db.connect()
    r = con.execute("SELECT id FROM personas WHERE slug=?", (slug,)).fetchone()
    con.close()
    return r["id"] if r else None


def create_post(slug, category, idx, platform, caption, hashtags, slot_time, extra_idxs=None):
    """idx = cover photo; extra_idxs = additional slides (same slug+category) -> carousel."""
    _ensure()
    pid = _pid(slug)
    if not pid:
        raise RuntimeError("unknown persona")
    if platform not in PLATFORMS:
        raise RuntimeError("unknown platform")
    imgs = model_data.persona_media(slug, category=category)
    if not (0 <= int(idx) < len(imgs)):
        raise RuntimeError("bad image index")
    path = imgs[int(idx)]
    extras = []
    for e in (extra_idxs or []):
        e = int(e)
        if not (0 <= e < len(imgs)):
            raise RuntimeError("bad extra image index")
        p = imgs[e]
        if p != path and p not in extras:
            extras.append(p)
    kind = "carousel" if extras else "photo"
    con = db.connect()
    cur = con.execute("INSERT INTO content_items(persona_id, platform, kind, path, caption, hashtags, "
                      "status, slot_time, extra_paths) VALUES(?,?,?,?,?,?,?,?,?)",
                      (pid, platform, kind, path, caption or "", hashtags or "",
                       "pending_review", slot_time or "", json.dumps(extras)))
    con.commit(); pid_row = cur.lastrowid; con.close()
    db.log_event("posts", "create", {"msg": "Post drafted: %s -> %s (%s)" % (slug, platform, slot_time or "unscheduled")})
    return pid_row


def list_posts(slug):
    _ensure()
    pid = _pid(slug)
    if not pid:
        return []
    con = db.connect()
    rows = con.execute("SELECT * FROM content_items WHERE persona_id=? ORDER BY "
                       "CASE WHEN slot_time IS NULL OR slot_time='' THEN 1 ELSE 0 END, slot_time",
                       (pid,)).fetchall()
    con.close()
    imgs = model_data._all_images()
    pos = {p: i for i, p in enumerate(imgs)}
    out = []
    for r in rows:
        try:
            extras = json.loads((r["extra_paths"] if "extra_paths" in r.keys() else "") or "[]")
        except Exception:
            extras = []
        idxs = [pos.get(r["path"])] + [pos.get(p) for p in extras]
        out.append({"id": r["id"], "platform": r["platform"], "caption": r["caption"] or "",
                    "hashtags": (r["hashtags"] if "hashtags" in r.keys() else "") or "",
                    "status": r["status"] or "draft", "slot_time": r["slot_time"] or "",
                    "review_notes": r["review_notes"] or "", "img_idx": pos.get(r["path"]),
                    "img_idxs": [i for i in idxs if i is not None],
                    "created_at": r["created_at"]})
    return out


def update_post(post_id, fields):
    _ensure()
    allowed = {"caption", "hashtags", "platform", "slot_time", "status", "review_notes"}
    sets, vals = [], []
    for k, v in fields.items():
        if k in allowed:
            sets.append("%s=?" % k); vals.append(v)
    if not sets:
        return False
    sets.append("updated_at=datetime('now')")
    vals.append(post_id)
    con = db.connect()
    con.execute("UPDATE content_items SET %s WHERE id=?" % ", ".join(sets), vals)
    con.commit(); con.close()
    return True


def set_slides(post_id, idxs):
    """Replace a post's photo set. idxs = GLOBAL image indices (first = cover).
    Turns the post into a carousel (2+) or single photo (1)."""
    _ensure()
    imgs = model_data._all_images()
    paths = []
    for i in (idxs or []):
        i = int(i)
        if not (0 <= i < len(imgs)):
            raise RuntimeError("bad image index")
        if imgs[i] not in paths:
            paths.append(imgs[i])
    if not paths:
        raise RuntimeError("a post needs at least one photo")
    con = db.connect()
    con.execute("UPDATE content_items SET path=?, extra_paths=?, kind=?, updated_at=datetime('now') "
                "WHERE id=?",
                (paths[0], json.dumps(paths[1:]), "carousel" if len(paths) > 1 else "photo", post_id))
    con.commit(); con.close()
    db.log_event("posts", "slides", {"msg": "Post %s slides set: %d photo(s)" % (post_id, len(paths))})
    return True


def create_post_global(slug, platform, caption, hashtags, slot_time, idxs):
    """Create a post from GLOBAL image indices (first = cover). Used by the calendar composer."""
    _ensure()
    pid = _pid(slug)
    if not pid:
        raise RuntimeError("unknown persona")
    if platform not in PLATFORMS:
        raise RuntimeError("unknown platform")
    imgs = model_data._all_images()
    paths = []
    for i in (idxs or []):
        i = int(i)
        if not (0 <= i < len(imgs)):
            raise RuntimeError("bad image index")
        if imgs[i] not in paths:
            paths.append(imgs[i])
    if not paths:
        raise RuntimeError("pick at least one photo")
    kind = "carousel" if len(paths) > 1 else "photo"
    con = db.connect()
    cur = con.execute("INSERT INTO content_items(persona_id, platform, kind, path, caption, hashtags, "
                      "status, slot_time, extra_paths) VALUES(?,?,?,?,?,?,?,?,?)",
                      (pid, platform, kind, paths[0], caption or "", hashtags or "",
                       "pending_review", slot_time or "", json.dumps(paths[1:])))
    con.commit(); rid = cur.lastrowid; con.close()
    db.log_event("posts", "create", {"msg": "Post drafted: %s -> %s (%s)" % (slug, platform, slot_time or "unscheduled")})
    return rid


def lib_global_idxs(slug, category):
    """Global image indices for a model's folder (for slide pickers)."""
    imgs = model_data._all_images()
    pos = {p: i for i, p in enumerate(imgs)}
    return [pos.get(p) for p in model_data.persona_media(slug, category=category)]


def delete_post(post_id):
    con = db.connect()
    con.execute("DELETE FROM content_items WHERE id=?", (post_id,))
    con.commit(); con.close()
    return True


def gen_caption(slug, platform, hint):
    """Persona-voiced caption + hashtags via Zen run_any_llm (grok). Blocking, ~5-15s."""
    con = db.connect()
    p = con.execute("SELECT * FROM personas WHERE slug=?", (slug,)).fetchone()
    con.close()
    name = p["name"] if p else slug
    geo = (p["geo"] if p else "") or ""
    prompt = ("You write social captions for %s, a playful %s-based influencer (openly AI persona). "
              "Write ONE %s caption for a photo%s. Sound natural and human, 1-2 short sentences, "
              "max 2 emojis, no quotes. Then 10 relevant hashtags. Reply in EXACTLY this format:\n"
              "CAPTION: <text>\nHASHTAGS: <#tag1 #tag2 ...>"
              % (name, geo, platform, (" of: " + hint) if hint else ""))
    body = {"tool": "run_any_llm", "input": {"model": "grok", "prompt": prompt}}
    r = requests.post(zen_client.API + "/generations", headers=zen_client._h(), json=body, timeout=30)
    if r.status_code not in (200, 201):
        raise RuntimeError("caption gen failed: %s" % r.status_code)
    gid = r.json().get("id")
    text = ""
    for _ in range(15):
        time.sleep(2)
        g = requests.get(zen_client.API + "/generations/" + gid, headers=zen_client._h(), timeout=20).json()
        if g.get("status") in ("succeeded", "failed"):
            if g.get("status") == "succeeded":
                res = requests.get(zen_client.API + "/generations/" + gid + "/result",
                                   headers=zen_client._h(), timeout=20).json()
                text = res.get("text") or ""
            break
    caption, hashtags = "", ""
    for line in text.splitlines():
        ls = line.strip()
        if ls.upper().startswith("CAPTION:"):
            caption = ls[8:].strip().strip(chr(60)+chr(62))
        elif ls.upper().startswith("HASHTAGS:"):
            hashtags = ls[9:].strip().strip(chr(60)+chr(62))
    if not caption and text:
        caption = text.strip()[:200]
    if not hashtags:
        hashtags = " ".join(w for w in text.split() if w.startswith("#"))[:300]
    return {"caption": caption, "hashtags": hashtags}


def gen_captions3(slug, platform, hint):
    """Three caption styles in ONE grok call: Playful / Story / Punchy. Returns {options:[...]}"""
    con = db.connect()
    p = con.execute("SELECT * FROM personas WHERE slug=?", (slug,)).fetchone()
    con.close()
    name = p["name"] if p else slug
    geo = (p["geo"] if p else "") or ""
    prompt = ("You write social captions for %s, a playful %s-based influencer (openly AI persona). "
              "Write THREE different %s captions for a photo%s, one per style:\n"
              "1 PLAYFUL: flirty, fun, teasing energy\n"
              "2 STORY: personal, storytelling, warm and a little candid\n"
              "3 PUNCHY: very short, bold, high-impact (a fragment is fine)\n"
              "Each caption 1-2 short sentences, max 2 emojis, no quotes. "
              "After each caption give 10 relevant hashtags. Reply in EXACTLY this format:\n"
              "CAPTION1: <text>\nHASHTAGS1: <#a #b ...>\nCAPTION2: <text>\nHASHTAGS2: <#a ...>\n"
              "CAPTION3: <text>\nHASHTAGS3: <#a ...>"
              % (name, geo, platform, (" of: " + hint) if hint else ""))
    text = zen_client.quick_llm(prompt)
    styles = ["Playful", "Story", "Punchy"]
    out = []
    for n in (1, 2, 3):
        cap, tags = "", ""
        for line in text.splitlines():
            ls = line.strip()
            if ls.upper().startswith("CAPTION%d:" % n):
                cap = ls[9:].strip().strip(chr(60) + chr(62))
            elif ls.upper().startswith("HASHTAGS%d:" % n):
                tags = ls[10:].strip().strip(chr(60) + chr(62))
        if cap:
            out.append({"style": styles[n - 1], "caption": cap, "hashtags": tags})
    if not out:
        one = gen_caption(slug, platform, hint)
        out = [{"style": "Caption", "caption": one["caption"], "hashtags": one["hashtags"]}]
    return {"options": out}
