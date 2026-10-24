"""Model detail data — reuses on-disk assets and a manual photo-tag store.

Each photo belongs to a persona and one CONTENT CATEGORY:
  - sfw     : IG / TikTok / general safe content
  - x       : X (Twitter) subscriber content
  - fanvue  : adult content for Fanvue
Category comes from the manual tag store (photo_tags) if set; otherwise, for
legacy images whose PATH contains a persona slug, we infer sfw (or fanvue if the
path is under an /NSFW/ folder). Everything else is 'untagged' and shows up in the
Tag page. We only READ / ORGANIZE assets already on disk — nothing here generates
or publishes content.
"""
import sys, os, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import db
import metrics as M

CONTENT = "/opt/jsw-ai/content"
REFS = "/opt/jsw-ai/memory/refs"
EXTS = (".jpg", ".jpeg", ".png", ".webp")
CATS = ("sfw", "x", "fanvue")
CAT_LABEL = {"sfw": "SFW", "x": "X", "fanvue": "Fanvue"}


def reference_images(slug, which):
    """ALL face/body reference images for a persona, sorted (primary first, then _2, _3...)."""
    out = []
    for p in sorted(glob.glob(os.path.join(REFS, slug + "_" + which + "*"))):
        if os.path.isfile(p) and p.lower().endswith(EXTS):
            out.append(p)
    return out


def reference_image(slug, which, i=0):
    """i-th face/body reference image (identity refs used by ZenCreator), or None."""
    refs = reference_images(slug, which)
    return refs[i] if 0 <= int(i) < len(refs) else None


def add_reference(slug, which, src_path=None, data=None, ext="png"):
    """Save a new reference image for a persona (copy of src_path, or raw bytes)."""
    import shutil
    n = len(reference_images(slug, which))
    if src_path:
        ext = src_path.rsplit(".", 1)[-1].lower()
    name = slug + "_" + which + ("" if n == 0 else "_%d" % (n + 1)) + "." + ext
    dest = os.path.join(REFS, name)
    if src_path:
        shutil.copyfile(src_path, dest)
    else:
        open(dest, "wb").write(data)
    return dest

# Confirmed handles (from project memory). Anything not listed simply shows no pill.
KNOWN_HANDLES = {
    "sienna": {"x": "BlakeSienn39605", "tiktok": "siennablake0320"},
}


def _ensure_tags_table():
    con = db.connect()
    con.execute("CREATE TABLE IF NOT EXISTS photo_tags("
                "path TEXT PRIMARY KEY, slug TEXT, category TEXT, updated_at TEXT DEFAULT (datetime('now')))")
    con.commit(); con.close()


def _load_tags():
    _ensure_tags_table()
    con = db.connect()
    rows = con.execute("SELECT path, slug, category FROM photo_tags").fetchall()
    con.close()
    return {r["path"]: (r["slug"], r["category"]) for r in rows}


def _all_images():
    return sorted(f for f in glob.glob(CONTENT + "/**/*", recursive=True)
                  if os.path.isfile(f) and f.lower().endswith(EXTS))


def _persona_slugs():
    return [p["slug"] for p in db.get_personas()]


def _resolve(path, tags, slugs):
    """Return (slug, category) for an image, or (None, None) if untagged."""
    if path in tags:
        return tags[path]
    pl = path.replace("\\", "/").lower()
    for s in slugs:
        if s.lower() in pl:
            return (s, "fanvue" if "/nsfw/" in pl else "sfw")
    return (None, None)


def persona_media(slug, category="sfw", limit=200):
    tags = _load_tags(); slugs = _persona_slugs()
    out = []
    for f in _all_images():
        rs, rc = _resolve(f, tags, slugs)
        if rs == slug and rc == category:
            out.append(f)
            if len(out) >= limit:
                break
    return out


def untagged_images(limit=400):
    """Images with no persona/category resolution yet — the Tag page pool."""
    tags = _load_tags(); slugs = _persona_slugs()
    imgs = _all_images()
    out = []
    for idx, f in enumerate(imgs):
        rs, rc = _resolve(f, tags, slugs)
        if rs is None:
            out.append({"idx": idx, "name": os.path.basename(f),
                        "under_nsfw": "/nsfw/" in f.replace("\\", "/").lower()})
        if len(out) >= limit:
            break
    return out


def image_by_index(idx):
    imgs = _all_images()
    if 0 <= idx < len(imgs):
        return imgs[idx]
    return None


def set_photo_tag(idx, slug, category):
    imgs = _all_images()
    if not (0 <= idx < len(imgs)):
        return False
    if category not in CATS:
        return False
    path = imgs[idx]
    _ensure_tags_table()
    con = db.connect()
    con.execute("INSERT INTO photo_tags(path, slug, category) VALUES(?,?,?) "
                "ON CONFLICT(path) DO UPDATE SET slug=excluded.slug, category=excluded.category, "
                "updated_at=datetime('now')", (path, slug, category))
    con.commit(); con.close()
    return True


def counts_for(slug):
    tags = _load_tags(); slugs = _persona_slugs()
    c = {k: 0 for k in CATS}
    for f in _all_images():
        rs, rc = _resolve(f, tags, slugs)
        if rs == slug and rc in c:
            c[rc] += 1
    return c


def model_json(slug):
    con = db.connect()
    p = con.execute("SELECT * FROM personas WHERE slug=?", (slug,)).fetchone()
    if not p:
        con.close(); return None
    meta = json.loads(p["meta_json"] or "{}")
    a = con.execute("SELECT id, status FROM agents WHERE name=?", ("model:" + slug,)).fetchone()
    con.close()
    board = M.board_data()
    mp = next((x for x in board["personas"] if x["slug"] == slug), None)
    handles = dict(KNOWN_HANDLES.get(slug, {}))
    handles.update(meta.get("handles", {}) or {})
    return {
        "slug": slug, "name": p["name"], "geo": p["geo"],
        "team": meta.get("team"), "partner_name": meta.get("partner_name"), "partner_slug": meta.get("partner_slug"),
        "agent_id": a["id"] if a else None, "agent_status": a["status"] if a else None,
        "handles": handles,
        "metrics": mp["metrics"] if mp else {}, "score": mp["score"] if mp else 0, "rank": mp["rank"] if mp else None,
        "sample": board.get("sample", True),
        "counts": counts_for(slug),
        "refs": {"face": len(reference_images(slug, "face")), "body": len(reference_images(slug, "body")),
                 "back": len(reference_images(slug, "back")), "waist": len(reference_images(slug, "waist")),
                 "xfanvue": len(reference_images(slug, "xfanvue"))},
    }
