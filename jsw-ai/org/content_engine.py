"""Concept-first content engine (the 'brains').

bio + goal -> concept -> media prompt + persona-voice caption -> approvals queue.

Higgsfield media is generated in-session by Claude and downloaded here by URL;
this module owns the concept, the caption, and the queue insert. LLM = Grok-3
(XAI) since it's the only working key on the box.
"""
import sys, os, json, re, time, urllib.request
sys.path.insert(0, "/opt/jsw-ai/org")
import db  # noqa: E402

ENV = "/opt/jsw-ai/config/.env"
BIOS = "/opt/jsw-ai/org/data/bios.json"
GEN = "/opt/jsw-ai/content/generated"


def _env(k):
    for l in open(ENV):
        if l.startswith(k + "="):
            return l.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def _grok(system, user, max_tokens=800, temp=0.9):
    body = json.dumps({"model": "grok-3", "max_tokens": max_tokens, "temperature": temp,
                       "messages": [{"role": "system", "content": system},
                                    {"role": "user", "content": user}]}).encode()
    req = urllib.request.Request("https://api.x.ai/v1/chat/completions", data=body,
                                 headers={"Authorization": "Bearer " + _env("XAI_API_KEY"),
                                          "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=90))
    return r["choices"][0]["message"]["content"]


def _json(text, fallback):
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    return fallback


def persona(slug):
    b = json.load(open(BIOS)).get(slug, {})
    con = db.connect()
    r = con.execute("SELECT name, geo, meta_json FROM personas WHERE slug=?", (slug,)).fetchone()
    con.close()
    meta = json.loads(r["meta_json"]) if r and r["meta_json"] else {}
    return {"slug": slug, "name": r["name"], "geo": r["geo"],
            "partner": meta.get("partner_name", ""),
            "bio": b.get("bio", ""), "themes": b.get("content_themes", ""),
            "voice": b.get("voice_sfw", "")}


def concept(slug, goal="lifestyle"):
    """One fresh post concept grounded in the persona's bio + geo + relationship."""
    p = persona(slug)
    sysp = ("You are the content director for an OPENLY-AI virtual influencer whose goal right now is "
            "to GROW REAL FOLLOWERS with authentic, relatable, scroll-stopping lifestyle content. "
            "Output ONE post concept as STRICT JSON with keys: "
            "format ('reel'|'carousel'|'single'), "
            "scene (a specific true-to-her real-life moment, concrete and visual), "
            "video_prompt (1-2 vivid sentences describing the shot for an image-to-video model; candid "
            "iPhone realism; describe ONLY what is seen, no camera/style jargon), "
            "hook (the scroll-stopping first beat/on-screen text), "
            "caption_idea (what the caption should say and feel). "
            "Make it true to her bio, location, and relationship. No explicit content.")
    u = ("PERSONA: %s (%s), partner: %s\nBIO: %s\nCONTENT THEMES: %s\nGOAL: %s\n"
         "Give ONE fresh concept for today. JSON only."
         % (p["name"], p["geo"], p["partner"], p["bio"][:1200], p["themes"][:600], goal))
    out = _grok(sysp, u)
    return _json(out, {"format": "reel", "scene": out[:200], "video_prompt": out[:200],
                       "hook": "", "caption_idea": ""})


def caption(slug, con_obj, platform="instagram"):
    """Persona-voice caption + hashtags that MATCH the concept's scene."""
    p = persona(slug)
    sysp = ("Write in the persona's authentic first-person voice. She is an openly-AI creator; stay in "
            "character but never claim to be a literal human. Output STRICT JSON {caption, hashtags}. "
            "caption: 1-3 short natural lines, a little playful, MATCHES the scene; a soft 'follow' CTA "
            "is fine, never a hard sell. hashtags: 5-8 relevant, space-separated, each starts with #.")
    u = ("PERSONA VOICE: %s\nSCENE: %s\nHOOK: %s\nCAPTION IDEA: %s\nPLATFORM: %s\nJSON only."
         % (p["voice"][:600], con_obj.get("scene", ""), con_obj.get("hook", ""),
            con_obj.get("caption_idea", ""), platform))
    out = _grok(sysp, u, max_tokens=400, temp=0.85)
    d = _json(out, {"caption": out[:280], "hashtags": ""})
    return d.get("caption", ""), d.get("hashtags", "")


def save_media(slug, url, ext="mp4"):
    d = os.path.join(GEN, slug)
    os.makedirs(d, exist_ok=True)
    fn = os.path.join(d, "reel_%d.%s" % (int(time.time() * 1000), ext))
    urllib.request.urlretrieve(url, fn)
    return fn


def queue_reel(slug, platform, media_path, cap, hashtags, slot_time="", viral_score=None, kind="reel"):
    con = db.connect()
    pid = con.execute("SELECT id FROM personas WHERE slug=?", (slug,)).fetchone()["id"]
    note = ("viral score: %s" % viral_score) if viral_score is not None else ""
    cur = con.execute("INSERT INTO content_items(persona_id, platform, kind, path, caption, hashtags, "
                      "status, slot_time, review_notes) VALUES(?,?,?,?,?,?,?,?,?)",
                      (pid, platform, kind, media_path, cap or "", hashtags or "",
                       "pending_review", slot_time or "", note))
    con.commit()
    rid = cur.lastrowid
    con.close()
    db.log_event("engine", "reel", {"msg": "concept-first %s queued: %s -> %s" % (kind, slug, platform)})
    return rid
