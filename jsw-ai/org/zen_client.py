"""Server-side ZenCreator client for the org panel Studio.

Talks to the public API (Bearer key from config/.env). Full tool parity comes from
the API itself: we proxy the live tool list + each tool's input_schema, so every
Zen option renders in the UI without hand-coding. Outputs are downloaded into
/opt/jsw-ai/content/generated/<slug>/ and tagged to the persona + folder
(photo_tags), so they appear in that model's library immediately.
"""
import sys, os, json, time, mimetypes
sys.path.insert(0, os.path.dirname(__file__))
import requests
import db
import model_data

API = "https://api.zencreator.pro/api/public/v1"
ENV = "/opt/jsw-ai/config/.env"
GEN_DIR = "/opt/jsw-ai/content/generated"

_key_cache = None
_tools_cache = {"t": 0, "data": None}


def _api_key():
    global _key_cache
    if _key_cache:
        return _key_cache
    try:
        for line in open(ENV, encoding="utf-8", errors="ignore"):
            if line.strip().startswith("ZENCREATOR_API_KEY"):
                _key_cache = line.split("=", 1)[1].strip().strip('"').strip("'")
                return _key_cache
    except Exception:
        pass
    return None


def _h():
    return {"Authorization": "Bearer " + (_api_key() or "")}


def _ensure_tables():
    con = db.connect()
    con.execute("CREATE TABLE IF NOT EXISTS zen_assets(path TEXT PRIMARY KEY, asset_id TEXT, "
                "uploaded_at TEXT DEFAULT (datetime('now')))")
    con.execute("CREATE TABLE IF NOT EXISTS zen_jobs(gid TEXT PRIMARY KEY, slug TEXT, category TEXT, "
                "tool TEXT, status TEXT, text TEXT, files_json TEXT, raw_json TEXT, "
                "created_at TEXT DEFAULT (datetime('now')), updated_at TEXT DEFAULT (datetime('now')))")
    try:
        con.execute("ALTER TABLE zen_jobs ADD COLUMN input_json TEXT")
    except Exception:
        pass
    con.commit(); con.close()


def list_tools(force=False):
    now = time.time()
    if not force and _tools_cache["data"] and now - _tools_cache["t"] < 300:
        return _tools_cache["data"]
    r = requests.get(API + "/tools", headers=_h(), timeout=30)
    r.raise_for_status()
    data = r.json()
    _tools_cache["data"] = data; _tools_cache["t"] = now
    return data


def tool_detail(name):
    r = requests.get(API + "/tools/" + name, headers=_h(), timeout=30)
    r.raise_for_status()
    return r.json()


def upload_asset(path):
    """Upload a local file to Zen, caching asset ids per path."""
    _ensure_tables()
    con = db.connect()
    row = con.execute("SELECT asset_id FROM zen_assets WHERE path=?", (path,)).fetchone()
    con.close()
    if row:
        return row["asset_id"]
    mt = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as fh:
        r = requests.post(API + "/assets", headers=_h(),
                          files={"file": (os.path.basename(path), fh, mt)},
                          data={"media_type": mt}, timeout=180)
    if r.status_code in (200, 201):
        j = r.json()
        aid = j.get("id") or j.get("asset_id") or (j.get("asset") or {}).get("id")
        if aid:
            con = db.connect()
            con.execute("INSERT OR REPLACE INTO zen_assets(path, asset_id) VALUES(?,?)", (path, aid))
            con.commit(); con.close()
            return aid
    raise RuntimeError("asset upload failed: %s %s" % (r.status_code, r.text[:200]))


def resolve_token(tok, slug):
    """Turn a UI token into a Zen asset id. Tokens: @face, @body, @lib:<idx>, asset:<id>."""
    if not isinstance(tok, str):
        return tok
    if tok == "@face" or tok.startswith("@face:"):
        i = int(tok[6:]) if tok.startswith("@face:") else 0
        p = model_data.reference_image(slug, "face", i)
        if not p: raise RuntimeError("no face reference %d for %s" % (i, slug))
        return upload_asset(p)
    if tok == "@body" or tok.startswith("@body:"):
        i = int(tok[6:]) if tok.startswith("@body:") else 0
        p = model_data.reference_image(slug, "body", i)
        if not p: raise RuntimeError("no body reference %d for %s" % (i, slug))
        return upload_asset(p)
    if tok == "@back" or tok.startswith("@back:"):
        i = int(tok[6:]) if tok.startswith("@back:") else 0
        p = model_data.reference_image(slug, "back", i)
        if not p: raise RuntimeError("no back reference %d for %s" % (i, slug))
        return upload_asset(p)
    if tok == "@waist" or tok.startswith("@waist:"):
        i = int(tok[7:]) if tok.startswith("@waist:") else 0
        p = model_data.reference_image(slug, "waist", i)
        if not p: raise RuntimeError("no waist reference %d for %s" % (i, slug))
        return upload_asset(p)
    if tok == "@xfanvue" or tok.startswith("@xfanvue:"):
        i = int(tok[9:]) if tok.startswith("@xfanvue:") else 0
        p = model_data.reference_image(slug, "xfanvue", i)
        if not p: raise RuntimeError("no X/Fanvue reference %d for %s" % (i, slug))
        return upload_asset(p)
    if tok.startswith("@lib:"):
        p = model_data.image_by_index(int(tok[5:]))
        if not p: raise RuntimeError("bad library index")
        return upload_asset(p)
    if tok.startswith("asset:"):
        return tok[6:]
    return tok


def resolve_input(inp, slug):
    out = {}
    for k, v in (inp or {}).items():
        if isinstance(v, str):
            out[k] = resolve_token(v, slug)
        elif isinstance(v, list):
            out[k] = [resolve_token(x, slug) for x in v]
        else:
            out[k] = v
    return out


def create_generation(slug, category, tool, inp):
    _ensure_tables()
    body = {"tool": tool, "input": resolve_input(inp, slug)}
    r = requests.post(API + "/generations", headers=_h(), json=body, timeout=60)
    if r.status_code not in (200, 201):
        raise RuntimeError("create failed: %s %s" % (r.status_code, r.text[:300]))
    gid = r.json().get("id")
    con = db.connect()
    con.execute("INSERT OR REPLACE INTO zen_jobs(gid, slug, category, tool, status, input_json) "
                "VALUES(?,?,?,?,?,?)",
                (gid, slug, category, tool, "queued", json.dumps(inp, default=str)[:8000]))
    con.commit(); con.close()
    db.log_event("studio", "generate", {"msg": "Zen %s started for %s -> %s" % (tool, slug, category)})
    return gid


def _asset_url(aid):
    try:
        r = requests.get(API + "/assets/" + str(aid), headers=_h(), timeout=30)
        if r.status_code == 200:
            j = r.json()
            return j.get("url") or j.get("download_url") or (j.get("asset") or {}).get("url")
    except Exception:
        pass
    return None


def _download(url, dest):
    r = requests.get(url, timeout=300, stream=True)
    r.raise_for_status()
    ext = os.path.splitext(url.split("?")[0])[1]
    if not ext or len(ext) > 5:
        ct = r.headers.get("content-type", "")
        ext = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp",
               "video/mp4": ".mp4"}.get(ct.split(";")[0], ".bin")
    path = dest + ext
    with open(path, "wb") as f:
        for chunk in r.iter_content(1 << 16):
            f.write(chunk)
    return path


def poll(gid):
    """Poll a generation; on success, download outputs into the library. Idempotent."""
    _ensure_tables()
    con = db.connect()
    job = con.execute("SELECT * FROM zen_jobs WHERE gid=?", (gid,)).fetchone()
    con.close()
    if not job:
        return {"error": "unknown job"}
    if job["status"] in ("succeeded", "failed") and job["files_json"] is not None:
        return _job_json(job)
    r = requests.get(API + "/generations/" + gid, headers=_h(), timeout=30)
    st = r.json().get("status") if r.status_code == 200 else "unknown"
    prog = r.json().get("progress") if r.status_code == 200 else None
    if st in ("succeeded", "success", "completed"):
        res = requests.get(API + "/generations/" + gid + "/result", headers=_h(), timeout=60).json()
        files = []
        os.makedirs(os.path.join(GEN_DIR, job["slug"]), exist_ok=True)
        for n, o in enumerate(res.get("outputs") or []):
            url = None
            if isinstance(o, str):
                url = o if o.startswith("http") else _asset_url(o)
            elif isinstance(o, dict):
                url = o.get("url") or o.get("download_url")
                if not url:
                    aid = o.get("id") or o.get("asset_id")
                    if aid: url = _asset_url(aid)
            if not url:
                continue
            dest = os.path.join(GEN_DIR, job["slug"], "%s_%d" % (gid[:8], n))
            try:
                p = _download(url, dest)
                files.append(p)
                if p.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    con = db.connect()
                    con.execute("INSERT OR REPLACE INTO photo_tags(path, slug, category) VALUES(?,?,?)",
                                (p, job["slug"], job["category"]))
                    con.commit(); con.close()
            except Exception:
                continue
        con = db.connect()
        con.execute("UPDATE zen_jobs SET status='succeeded', text=?, files_json=?, raw_json=?, "
                    "updated_at=datetime('now') WHERE gid=?",
                    (res.get("text"), json.dumps(files), json.dumps(res, default=str)[:4000], gid))
        con.commit()
        job = con.execute("SELECT * FROM zen_jobs WHERE gid=?", (gid,)).fetchone()
        con.close()
        db.log_event("studio", "done", {"msg": "Zen %s finished for %s (%d files)" % (job["tool"], job["slug"], len(files))})
        return _job_json(job)
    if st in ("failed", "error"):
        err = (r.json().get("error") or "failed") if r.status_code == 200 else "failed"
        con = db.connect()
        con.execute("UPDATE zen_jobs SET status='failed', text=?, files_json='[]', updated_at=datetime('now') "
                    "WHERE gid=?", (json.dumps(err, default=str)[:500], gid))
        con.commit(); con.close()
        return {"gid": gid, "status": "failed", "error": err}
    con = db.connect()
    con.execute("UPDATE zen_jobs SET status=?, updated_at=datetime('now') WHERE gid=?", (st, gid))
    con.commit(); con.close()
    return {"gid": gid, "status": st, "progress": prog}


def _file_indexes(files):
    imgs = model_data._all_images()
    pos = {p: i for i, p in enumerate(imgs)}
    return [{"n": n, "idx": pos.get(p), "name": os.path.basename(p),
             "video": p.lower().endswith((".mp4", ".webm", ".mov"))}
            for n, p in enumerate(files)]


def _job_json(job):
    files = json.loads(job["files_json"] or "[]")
    return {"gid": job["gid"], "status": job["status"], "tool": job["tool"], "slug": job["slug"],
            "category": job["category"], "text": job["text"], "files": _file_indexes(files),
            "created_at": job["created_at"]}


def jobs_for(slug, limit=12):
    _ensure_tables()
    con = db.connect()
    rows = con.execute("SELECT * FROM zen_jobs WHERE slug=? ORDER BY created_at DESC LIMIT ?",
                       (slug, limit)).fetchall()
    con.close()
    return [_job_json(r) for r in rows]


_tpl_cache = {"t": 0, "data": None}


def templates_all(force=False):
    """Every public Zen template (name, tool_name, tags, input preset), cached 10 min."""
    now = time.time()
    if not force and _tpl_cache["data"] and now - _tpl_cache["t"] < 600:
        return _tpl_cache["data"]
    out, page = [], 1
    while page <= 20:
        r = requests.get(API + "/templates", headers=_h(),
                         params={"limit": 100, "page": page}, timeout=45)
        r.raise_for_status()
        j = r.json()
        batch = j.get("templates") or []
        out.extend(batch)
        pg = j.get("pagination") or {}
        if not batch or page >= int(pg.get("total_pages") or 1):
            break
        page += 1
    _tpl_cache["data"] = out; _tpl_cache["t"] = now
    return out


def templates(q=None, tool=None, page=1, per=24):
    """Filtered/paged view over the cached template list."""
    items = templates_all()
    if tool:
        items = [t for t in items if t.get("tool_name") == tool]
    if q:
        ql = q.lower()
        items = [t for t in items if ql in json.dumps(
            [t.get("name"), t.get("tags"), t.get("tool_name")], default=str).lower()]
    total = len(items)
    page = max(1, int(page))
    return {"total": total, "page": page, "per": per,
            "templates": items[(page - 1) * per: page * per]}


def quick_llm(prompt, system=None):
    """One-shot text generation via run_any_llm/grok (no job row, synchronous)."""
    body = {"tool": "run_any_llm", "input": {"model": "grok", "prompt": prompt}}
    if system:
        body["input"]["system_prompt"] = system
    r = requests.post(API + "/generations", headers=_h(), json=body, timeout=60)
    if r.status_code not in (200, 201):
        raise RuntimeError("llm create failed: %s" % r.status_code)
    gid = r.json().get("id")
    for _ in range(40):
        time.sleep(2)
        s = requests.get(API + "/generations/" + gid, headers=_h(), timeout=30).json()
        if s.get("status") in ("succeeded", "success", "completed"):
            res = requests.get(API + "/generations/" + gid + "/result", headers=_h(), timeout=30).json()
            return (res.get("text") or "").strip()
        if s.get("status") in ("failed", "error"):
            raise RuntimeError("llm failed")
    raise RuntimeError("llm timeout")


def enhance_prompt(text, persona_name=None):
    sys_p = ("You are an expert prompt engineer for photorealistic AI image generation. "
             "Rewrite the user's rough idea into one vivid, detailed image prompt: subject, outfit, "
             "pose, setting, lighting, camera angle, mood. Keep it under 120 words, photorealistic, "
             "Instagram-quality. Return ONLY the improved prompt text, nothing else.")
    if persona_name:
        sys_p += (" The subject is %s (her face and body come from reference photos, so describe "
                  "the scene and styling, not her identity)." % persona_name)
    return quick_llm(text or "a lifestyle photo", sys_p)


def retry(gid):
    """Re-submit a stored job with the same tool + input tokens (refs re-resolve fresh)."""
    _ensure_tables()
    con = db.connect()
    row = con.execute("SELECT * FROM zen_jobs WHERE gid=?", (gid,)).fetchone()
    con.close()
    if not row:
        raise RuntimeError("unknown job")
    try:
        inp = json.loads(row["input_json"] or "")
    except Exception:
        raise RuntimeError("no stored input for this older job — set options and generate again")
    return create_generation(row["slug"], row["category"], row["tool"], inp)


def file_path(gid, n):
    """Absolute path of the nth output file of a job (serving videos and non-library files)."""
    _ensure_tables()
    con = db.connect()
    row = con.execute("SELECT files_json FROM zen_jobs WHERE gid=?", (gid,)).fetchone()
    con.close()
    files = json.loads((row["files_json"] if row else None) or "[]")
    if 0 <= n < len(files) and isinstance(files[n], str) and os.path.isfile(files[n]):
        return files[n]
    return None
