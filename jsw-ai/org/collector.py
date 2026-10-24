"""Real-metrics collector — pulls live Ayrshare analytics into the metrics table.

Sienna uses the main API key; other personas use their ayrshare_profile_key (refId)
from PROJECT_STATE. Personas with no linked socials record zeros (honest scoreboard).
Run via systemd timer (jsw-metrics.timer) or manually.
"""
import sys, os, json, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
import db
import metrics

ENV = "/opt/jsw-ai/config/.env"
STATE = "/opt/jsw-ai/agents/PROJECT_STATE.json"
PLATFORMS = ["instagram", "tiktok", "twitter", "youtube", "reddit", "facebook"]


def _api_key():
    for l in open(ENV):
        if l.startswith("AYRSHARE_API_KEY"):
            return l.split("=", 1)[1].strip()
    return None


def _call(path, key, profile_key=None, body=None):
    headers = {"Authorization": "Bearer " + key, "Content-Type": "application/json"}
    if profile_key:
        headers["Profile-Key"] = profile_key
    req = urllib.request.Request("https://api.ayrshare.com/api/" + path,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers=headers, method="POST" if body is not None else "GET")
    return json.load(urllib.request.urlopen(req, timeout=40))


def _num(d, *keys):
    for k in keys:
        v = d.get(k)
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            return v
    return 0


def collect():
    key = _api_key()
    personas = json.load(open(STATE)).get("personas", {})
    for p in db.get_personas():
        slug = p["slug"]
        cfg = personas.get(slug, {})
        pk = None
        if slug != "sienna":
            try:
                import vault
                pk = (vault.get_secret(slug, "ayrshare", "profile_key") or "").strip() or None
            except Exception:
                pk = None
            if not pk:
                pk = (cfg.get("ayrshare_profile_key") or "").strip() or None
        vals = {}
        if slug == "sienna" or pk:
            try:
                u = _call("user", key, pk)
                plats = [x for x in (u.get("activeSocialAccounts") or [])
                         if isinstance(x, str) and x in PLATFORMS]
                if not plats:
                    raise RuntimeError("no linked social accounts")
                d = {}
                for pl in plats:
                    try:
                        r1 = _call("analytics/social", key, pk, {"platforms": [pl]})
                        if isinstance(r1, dict):
                            d.update(r1)
                    except Exception as e2:
                        print("  skip", slug, pl, str(e2)[:60], flush=True)
                followers = likes = views = posts = 0
                for plat, pd in (d or {}).items():
                    if not isinstance(pd, dict):
                        continue
                    a = pd.get("analytics") if isinstance(pd.get("analytics"), dict) else pd
                    followers += _num(a, "followersCount", "followerCount", "fanCount",
                                      "subscriberCount", "subscribers")
                    likes += _num(a, "likesCount", "likeCount", "totalLikes")
                    views += _num(a, "viewCount", "viewsCount", "views", "totalViews")
                    posts += _num(a, "mediaCount", "videoCountTotal", "videoCount",
                                  "postsCount", "tweetCount")
                vals = {"followers": followers, "total_likes": likes, "profile_views": views,
                        "engagement_rate": round(100.0 * likes / views, 1) if views > 0 else 0,
                        "avg_post_likes": int(likes / posts) if posts > 0 else 0,
                        "avg_post_views": int(views / posts) if posts > 0 else 0}
            except Exception as e:
                print("ERR", slug, str(e)[:120], flush=True)
        for m in metrics.METRICS:
            metrics.record(slug, m["key"], vals.get(m["key"], 0))
        print(slug, json.dumps({k: v for k, v in vals.items() if v}), flush=True)
    con = db.connect()
    con.execute("INSERT OR REPLACE INTO settings(key, value) VALUES('live_metrics','1')")
    con.commit(); con.close()
    db.log_event("metrics", "collect", {"msg": "live Ayrshare metrics collected for all personas"})
    print("COLLECT-DONE", flush=True)


if __name__ == "__main__":
    collect()
