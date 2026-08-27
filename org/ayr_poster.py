"""jsw-poster — publishes approved + scheduled posts via Ayrshare.

SAFETY GATE: does nothing until settings key 'go_live' == '1'.
That flag is flipped ONLY on Sam's explicit go-ahead. Until then this
daemon just logs "holding" so we can verify it's wired without any risk
of accidental publishing.

Cutover: on the FIRST successful publish, ig-agent.service (the legacy
pipeline) is stopped + disabled automatically — seamless cutover as agreed.
"""
import json
import mimetypes
import os
import subprocess
import sys
import time

sys.path.insert(0, "/opt/jsw-ai/org")
import db  # noqa: E402

import requests  # noqa: E402

ENV_PATH = "/opt/jsw-ai/config/.env"
STATE_PATH = "/opt/jsw-ai/agents/PROJECT_STATE.json"
AYR = "https://app.ayrshare.com/api"
LOOP_SECONDS = 60
# Ayrshare platform names (ours -> theirs); fanvue is NOT Ayrshare (Grok lane).
PLATFORM_MAP = {"instagram": "instagram", "tiktok": "tiktok", "x": "twitter",
                "youtube": "youtube", "facebook": "facebook", "reddit": "reddit"}


def _env(key):
    try:
        for line in open(ENV_PATH):
            line = line.strip()
            if line.startswith(key + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return ""


def _profile_key(slug):
    """Per-persona Ayrshare profile key; sienna rides the main key (None).

    Vault first (canonical since Aug 2026), PROJECT_STATE as legacy fallback.
    """
    try:
        import vault
        pk = (vault.get_secret(slug, "ayrshare", "profile_key") or "").strip()
        if pk:
            return pk
    except Exception:
        pass
    try:
        state = json.load(open(STATE_PATH))
        pk = (state.get("personas", {}).get(slug, {}) or {}).get("ayrshare_profile_key")
        return pk or None
    except Exception:
        return None


_X_KEYS = None


def x_consumer_pair():
    """X BYO OAuth 1.0 consumer key/secret from the vault (cached).

    Since 31 Mar 2026 Ayrshare requires every account posting to X to send its
    own app's consumer key + secret on EVERY request touching X.
    """
    global _X_KEYS
    if _X_KEYS is None:
        k = s = ""
        try:
            sys.path.insert(0, "/opt/jsw-ai/org")
            import vault  # noqa: E402
            k = vault.get_secret("*", "x", "X_CONSUMER_KEY") or ""
            s = vault.get_secret("*", "x", "X_CONSUMER_SECRET") or ""
        except Exception as e:
            print("[poster] vault read failed for X keys: %s" % e, flush=True)
        _X_KEYS = (k.strip(), s.strip())
    return _X_KEYS


def _x_headers(ayr_platform):
    if ayr_platform != "twitter":
        return {}
    k, s = x_consumer_pair()
    if not k or not s:
        return {}
    return {"X-Twitter-OAuth1-Api-Key": k, "X-Twitter-OAuth1-Api-Secret": s}


def _setting(key):
    con = db.connect()
    try:
        con.execute("CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT)")
        r = con.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return r["value"] if r else None
    finally:
        con.close()


def _due_posts():
    con = db.connect()
    try:
        rows = con.execute(
            "SELECT ci.*, p.slug pslug, p.name pname FROM content_items ci "
            "JOIN personas p ON p.id=ci.persona_id "
            "WHERE ci.status='approved' AND ci.slot_time IS NOT NULL AND ci.slot_time!='' "
            "AND replace(ci.slot_time,'T',' ') <= datetime('now','localtime') "
            "ORDER BY ci.slot_time").fetchall()
        return [dict(r) for r in rows]
    finally:
        con.close()


def _mark(post_id, status, note=None):
    con = db.connect()
    try:
        if note is None:
            con.execute("UPDATE content_items SET status=?, updated_at=datetime('now') WHERE id=?",
                        (status, post_id))
        else:
            con.execute("UPDATE content_items SET status=?, review_notes=?, updated_at=datetime('now') WHERE id=?",
                        (status, note[:300], post_id))
        con.commit()
    finally:
        con.close()


def _upload_media(api_key, profile_key, path, ayr_platform=None):
    name = os.path.basename(path)
    ctype = mimetypes.guess_type(name)[0] or "image/jpeg"
    headers = {"Authorization": "Bearer " + api_key}
    if profile_key:
        headers["Profile-Key"] = profile_key
    headers.update(_x_headers(ayr_platform))
    r = requests.get(AYR + "/media/uploadUrl",
                     params={"fileName": name, "contentType": ctype},
                     headers=headers, timeout=30)
    r.raise_for_status()
    j = r.json()
    up_url, access_url = j.get("uploadUrl"), j.get("accessUrl")
    if not up_url or not access_url:
        raise RuntimeError("uploadUrl response missing fields: " + str(j)[:150])
    with open(path, "rb") as fh:
        pr = requests.put(up_url, data=fh, headers={"Content-Type": ctype}, timeout=120)
    pr.raise_for_status()
    return access_url


def _publish(api_key, profile_key, platform, text, media_urls):
    headers = {"Authorization": "Bearer " + api_key, "Content-Type": "application/json"}
    if profile_key:
        headers["Profile-Key"] = profile_key
    headers.update(_x_headers(platform))
    body = {"post": text, "platforms": [platform]}
    if media_urls:
        body["mediaUrls"] = list(media_urls)
    r = requests.post(AYR + "/post", json=body, headers=headers, timeout=60)
    j = {}
    try:
        j = r.json()
    except Exception:
        pass
    ok = r.status_code < 300 and j.get("status") in ("success", "scheduled")
    return ok, j


def _cutover_if_needed():
    """First successful new-pipeline post => kill legacy ig-agent (seamless cutover)."""
    if _setting("cutover_done") == "1":
        return
    try:
        active = subprocess.run(["systemctl", "is-active", "ig-agent.service"],
                                capture_output=True, text=True).stdout.strip()
        if active == "active":
            subprocess.run(["systemctl", "stop", "ig-agent.service"], check=False)
            subprocess.run(["systemctl", "disable", "ig-agent.service"], check=False)
            db.log_event("poster", "cutover", {"msg": "legacy ig-agent stopped+disabled after first successful publish"})
            print("[poster] CUTOVER: ig-agent stopped + disabled", flush=True)
    except Exception as e:
        print("[poster] cutover check failed: %s" % e, flush=True)
    con = db.connect()
    con.execute("INSERT INTO settings(key,value) VALUES('cutover_done','1') "
                "ON CONFLICT(key) DO UPDATE SET value='1'")
    con.commit()
    con.close()


def tick():
    if _setting("go_live") != "1":
        print("[poster] holding — go_live flag is off (safety gate)", flush=True)
        return
    api_key = _env("AYRSHARE_API_KEY")
    if not api_key:
        print("[poster] no AYRSHARE_API_KEY in .env — cannot post", flush=True)
        return
    for po in _due_posts():
        pid, slug, plat = po["id"], po["pslug"], (po["platform"] or "").lower()
        if plat == "fanvue":
            continue  # not an Ayrshare platform; Fanvue lane is separate
        ayr_plat = PLATFORM_MAP.get(plat)
        if not ayr_plat:
            _mark(pid, "failed", "unknown platform: " + plat)
            continue
        if ayr_plat == "twitter":
            k, s = x_consumer_pair()
            if not k or not s:
                _mark(pid, "failed", "X consumer key/secret missing from vault — "
                                     "add X_CONSUMER_KEY + X_CONSUMER_SECRET on the Vault page")
                print("[poster] SKIP #%s — no X consumer keys in vault" % pid, flush=True)
                continue
        text = (po["caption"] or "").strip()
        tags = (po.get("hashtags") or "").strip()
        if tags:
            text = (text + "\n\n" + tags).strip()
        pkey = _profile_key(slug)
        try:
            paths = [po.get("path")]
            try:
                paths += json.loads(po.get("extra_paths") or "[]")
            except Exception:
                pass
            media_urls = [_upload_media(api_key, pkey, p, ayr_plat)
                          for p in paths if p and os.path.isfile(p)]
            ok, resp = _publish(api_key, pkey, ayr_plat, text, media_urls)
            if ok:
                _mark(pid, "posted")
                db.log_event("poster", "posted",
                             {"post_id": pid, "slug": slug, "platform": plat,
                              "ayr_id": (resp.get("id") or (resp.get("postIds") or [{}])[0].get("id", ""))})
                print("[poster] POSTED #%s %s/%s" % (pid, slug, plat), flush=True)
                _cutover_if_needed()
            else:
                _mark(pid, "failed", "ayrshare: " + str(resp)[:250])
                db.log_event("poster", "post_failed", {"post_id": pid, "slug": slug, "resp": str(resp)[:250]})
                print("[poster] FAILED #%s %s" % (pid, str(resp)[:120]), flush=True)
        except Exception as e:
            _mark(pid, "failed", "error: " + str(e)[:250])
            print("[poster] ERROR #%s %s" % (pid, e), flush=True)


def main():
    print("[poster] jsw-poster started (gate: go_live)", flush=True)
    while True:
        try:
            tick()
        except Exception as e:
            print("[poster] tick error: %s" % e, flush=True)
        time.sleep(LOOP_SECONDS)


if __name__ == "__main__":
    main()
