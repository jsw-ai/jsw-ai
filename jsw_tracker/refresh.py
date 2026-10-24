#!/usr/bin/env python3
"""JSW tracker refresh. READ-ONLY on social platforms (GET requests only).

Pulls:
  * Ayrshare: GET /api/user, /api/history/{platform}, /api/analytics/social?platforms=X
    (Sienna = Default profile: main key, no Profile-Key header)
  * X public API (optional): needs env X_BEARER_TOKEN; otherwise use the agent's
    'x' MCP tools and pass their JSON via --x-json.
Outputs (always): out/posts.json, out/snapshots.json, out/glance.md (at-a-glance table).
Notion upsert (optional): with env NOTION_TOKEN (an integration shared with the
JSW Performance Tracker), it upserts Post Performance rows by Post URL, adds
follower snapshots (one per model/platform/date) and regenerates the
at-a-glance table at the top of the JSW Stats Dashboard.
Without NOTION_TOKEN, an agent applies out/*.json with the Notion MCP tools.
Never prints keys. Never invents numbers: missing metrics stay null.
"""
import argparse, datetime as dt, json, os, pathlib, sys, urllib.request, urllib.error
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/Detroit")
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
SECRET_DIRS = [pathlib.Path("/home/box/agent-data/secrets"), pathlib.Path("/home/box/sand-data/secrets")]
MODELS = ["Sienna", "Camille", "Charlotte", "Madison", "Gabriela", "Valentina"]
X_HANDLES = {"Sienna": "BlakeSienn39605", "Camille": "CamilleDubav", "Charlotte": "char_hayes_26", "Gabriela": "GabrielaSailq1", "Madison": "MadisonCole69", "Valentina": "v_reyes_wc2026"}
TIKTOK_HANDLES = {"Sienna": "thesienna_blake", "Camille": "camilledubois089", "Charlotte": "charlottehayes240",
                  "Madison": "madisoncolewc26", "Gabriela": "gabriela_santos343", "Valentina": "valentinareyes33240"}
POST_DS = "c99829b1-e51e-4a44-82ef-1c43f6b6e2a0"
SNAP_DS = "e9656a2f-20af-4f92-9c9b-5b064872eba6"
DASHBOARD_PAGE = "3fff29949b29817fbfcaef9eb6f34ab6"
GLANCE_PLATFORMS = ["Instagram", "TikTok", "X", "Facebook", "YouTube", "Reddit"]
PLAT_NAME = {"instagram": "Instagram", "tiktok": "TikTok", "twitter": "X", "facebook": "Facebook",
             "youtube": "YouTube", "reddit": "Reddit"}
DB_PLATFORM = {"Instagram": "Instagram", "TikTok": "TikTok", "X": "X"}  # others -> "Other"


def secret(name):
    for d in SECRET_DIRS:
        p = d / name
        if p.exists():
            v = p.read_text().strip()
            return v.split(":", 1)[1].strip() if ":" in v.splitlines()[0] and not v.startswith("{") else v
    return None


def get(url, headers):
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode())
        except Exception:
            return {"status": "error", "message": f"HTTP {e.code}"}


def ayrshare(model, api_key):
    h = {"Authorization": f"Bearer {api_key}"}
    if model != "Sienna":
        pk = secret(f"JSW-{model.lower()}-ayrshare-profile-key.txt")
        if not pk:
            return [], [], [f"{model}: no Ayrshare profile key file"]
        h["Profile-Key"] = pk
    base = "https://api.ayrshare.com/api"
    user = get(f"{base}/user", h)
    posts, snaps, errs = [], [], []
    for pl in user.get("activeSocialAccounts") or []:
        P = PLAT_NAME.get(pl, pl)
        hist = get(f"{base}/history/{pl}", h)
        if hist.get("status") == "error":
            errs.append(f"{model} {P} history: {str(hist.get('message'))[:120]}")
        for p in hist.get("posts") or []:
            posts.append(norm_ayr(model, P, p))
        soc = (get(f"{base}/analytics/social?platforms={pl}", h).get(pl) or {}).get("analytics") or {}
        f = next((soc.get(k) for k in ("followersCount", "subscriberCount", "followerCount") if soc.get(k) is not None), None)
        if f is not None:
            snaps.append({"model": model, "platform": P, "followers": f, "source": "Ayrshare /api/analytics/social"})
    if not user.get("activeSocialAccounts"):
        errs.append(f"{model}: no linked accounts in Ayrshare")
    return posts, snaps, errs


def norm_ayr(model, P, p):
    txt = (p.get("post") or p.get("title") or "").replace("\n", " ")
    if P == "Facebook":
        likes = (p.get("reactions") or {}).get("total", p.get("likeCount"))
    elif P == "Reddit":
        likes = p.get("ups")
    else:
        likes = p.get("likeCount")
    views = p.get("videoViews") if P in ("TikTok", "Facebook") else None
    if P == "YouTube" and likes is None and views is None:
        views = None  # Ayrshare returns no YouTube stats; row kept with blank metrics
    url = (p.get("postUrl") or "").split("?utm")[0]
    return {"model": model, "platform": P, "url": url, "created": p.get("created"), "text": txt,
            "format": {"TikTok": "TikTok video", "Reddit": "Reddit post", "YouTube": "YouTube video"}.get(P)
                      or (p.get("mediaProductType") if P == "Instagram" else ("FB reel" if "/reel/" in url else "FB post")),
            "views": views, "likes": likes, "comments": p.get("commentsCount", p.get("numComments")),
            "shares": p.get("shareCount", p.get("sharesCount")), "source": f"Ayrshare /api/history/{P.lower()}"}


def x_pull(bearer):
    posts, snaps, errs = [], [], []
    h = {"Authorization": f"Bearer {bearer}"}
    for model, u in X_HANDLES.items():
        usr = get(f"https://api.x.com/2/users/by/username/{u}?user.fields=public_metrics", h).get("data")
        if not usr:
            errs.append(f"{model} X @{u}: lookup failed"); continue
        snaps.append({"model": model, "platform": "X", "followers": usr["public_metrics"]["followers_count"],
                      "source": f"X public API @{u}"})
        tl = get(f"https://api.x.com/2/users/{usr['id']}/tweets?max_results=20&tweet.fields=created_at,public_metrics", h)
        posts += [norm_x(model, u, t) for t in tl.get("data") or []]
    return posts, snaps, errs


def norm_x(model, u, t):
    m = t["public_metrics"]
    return {"model": model, "platform": "X", "url": f"https://x.com/{u}/status/{t['id']}", "created": t["created_at"],
            "text": t["text"].replace("\n", " "), "format": "Image post" if "https://t.co/" in t["text"] else "Text post",
            "views": m.get("impression_count"), "likes": m.get("like_count"), "comments": m.get("reply_count"),
            "shares": (m.get("retweet_count") or 0) + (m.get("quote_count") or 0), "source": "X public API"}


def _tt_stats(u, ua):
    import re
    req = urllib.request.Request(f"https://www.tiktok.com/@{u}", headers={"User-Agent": ua, "Accept-Language": "en-US"})
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode("utf-8", "replace")
    m = re.search(r'__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>', html, re.S)
    return json.loads(m.group(1))["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["stats"]


def tiktok_pull():
    """Public TikTok profile pages (no login, GET only): __UNIVERSAL_DATA_FOR_REHYDRATION__ userInfo.stats."""
    import re
    snaps, errs = [], []
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
    for model, u in TIKTOK_HANDLES.items():
        st, err = None, None
        for attempt in range(3):
            try:
                st = _tt_stats(u, ua); break
            except Exception as e:
                err = e; import time; time.sleep(3)
        if st is None and err is not None:
            errs.append(f"{model} TikTok @{u}: fetch failed after 3 tries ({type(err).__name__})"); continue
        if not st or st.get("followerCount") is None:
            errs.append(f"{model} TikTok @{u}: no stats in public page"); continue
        snaps.append({"model": model, "platform": "TikTok", "followers": st["followerCount"],
                      "following": st.get("followingCount"), "likes_total": st.get("heartCount", st.get("heart")),
                      "videos": st.get("videoCount"), "source": f"TikTok public profile @{u}",
                      "fetched_at": dt.datetime.now(ET).isoformat(timespec="seconds")})
    return snaps, errs


YT_CHANNELS = {"Camille": "@CamilleDubois-r6m", "Charlotte": "@CharlotteHayesUK", "Madison": "@MadisonColeUSA", "Valentina": "@ValentinaReyes-WC2026"}
YTDLP = str(HERE / ".venv/bin/yt-dlp")


def youtube_pull():
    """Public YouTube pages via yt-dlp (no login). Real view/like/comment and subscriber counts."""
    import subprocess
    posts, snaps, errs = [], [], []
    for model, ch in YT_CHANNELS.items():
        try:
            ids = subprocess.run([YTDLP, "--flat-playlist", "--print", "id", f"https://www.youtube.com/{ch}/shorts"],
                                 capture_output=True, text=True, timeout=300).stdout.split()
        except Exception as e:
            errs.append(f"{model} YouTube list: {e}"); continue
        subs = None
        for vid in ids:
            r = subprocess.run([YTDLP, "--skip-download", "-j", f"https://www.youtube.com/watch?v={vid}"],
                               capture_output=True, text=True, timeout=120)
            try: j = json.loads(r.stdout)
            except Exception:
                # box IP often gets YouTube's bot check; the web_safari client usually still returns metadata
                r = subprocess.run([YTDLP, "--skip-download", "--ignore-no-formats-error", "--extractor-args",
                                    "youtube:player_client=web_safari", "-j", f"https://www.youtube.com/watch?v={vid}"],
                                   capture_output=True, text=True, timeout=120)
                try: j = json.loads(r.stdout.strip().splitlines()[-1])
                except Exception: errs.append(f"{model} YouTube {vid}: no data"); continue
            subs = j.get("channel_follower_count", subs)
            posts.append({"model": model, "platform": "YouTube", "url": f"https://www.youtube.com/shorts/{vid}",
                          "created": dt.datetime.fromtimestamp(j["timestamp"], dt.timezone.utc).isoformat().replace("+00:00", "Z") if j.get("timestamp") else None,
                          "text": (j.get("description") or j.get("title") or "").replace("\n", " "), "format": "YouTube Short",
                          "views": j.get("view_count"), "likes": j.get("like_count"), "comments": j.get("comment_count"),
                          "shares": None, "source": "YouTube public page (yt-dlp)"})
        if subs is not None:
            snaps.append({"model": model, "platform": "YouTube", "followers": subs, "source": f"YouTube public {ch}"})
    return posts, snaps, errs


def merge_ig(posts, snaps, ig):
    """Merge IG reel play counts read headless from AdsPower (mac: ~/jsw_tracker/ig_read.py)."""
    errs = []
    for model, d in ig.items():
        if d.get("error"):
            errs.append(f"{model} Instagram: {d['error']}"); continue
        for p in posts:
            if p["model"] == model and p["platform"] == "Instagram":
                code = p["url"].rstrip("/").split("/")[-1]
                it = d.get("items", {}).get(code, {})
                v = it.get("play_count", it.get("ig_play_count", it.get("view_count")))
                if v is not None:
                    p["views"] = v; p["source"] += " + IG play_count (AdsPower, read-only)"
    return errs


def glance(posts, snaps, today):
    latest = {}
    for s in snaps:
        latest[(s["model"], s["platform"])] = s["followers"]
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=7)
    views7 = {}
    for p in posts:
        try:
            c = dt.datetime.fromisoformat(p["created"].replace("Z", "+00:00"))
        except Exception:
            continue
        if c >= cutoff and p["views"] is not None:
            k = (p["model"], p["platform"]); views7[k] = views7.get(k, 0) + p["views"]
    hdr = ["Model"] + [f"{P} followers" for P in GLANCE_PLATFORMS] + [f"{P} views 7d" for P in GLANCE_PLATFORMS] + ["Total followers", "Total views 7d"]
    rows, tot = [], [0] * (len(hdr) - 1)
    for m in MODELS:
        vals = [latest.get((m, P)) for P in GLANCE_PLATFORMS] + [views7.get((m, P)) for P in GLANCE_PLATFORMS]
        tf = sum(v for v in vals[:6] if v is not None); tv = sum(v for v in vals[6:] if v is not None)
        vals += [tf, tv]
        for i, v in enumerate(vals):
            if v is not None: tot[i] += v
        rows.append([m] + ["—" if v is None else str(v) for v in vals])
    rows.append(["**Total**"] + [str(v) for v in tot])
    cell = lambda r: "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    now = dt.datetime.now(ET).strftime("%b %d, %Y %I:%M %p ET")
    return (f"## At a glance\nLast refreshed {now}. Followers = latest snapshot; views = sum over posts from the last 7 days "
            f"(Instagram views = reel play counts read from the signed-in AdsPower profiles; IG photo posts and Reddit have no view counts). — = no data.\n"
            f"<table header-row=\"true\">\n{cell(hdr)}\n" + "\n".join(cell(r) for r in rows) + "\n</table>\n")


# ---------------- optional Notion REST upsert ----------------
def notion(method, path, token, body=None):
    req = urllib.request.Request(f"https://api.notion.com/v1/{path}", method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {token}", "Notion-Version": "2022-06-28",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def num(v):
    return {"number": v}


def notion_upsert(posts, snaps, today, token, glance_md):
    db = notion("GET", f"databases/{POST_DS}", token)["id"]
    for p in posts:
        q = notion("POST", f"databases/{db}/query", token, {"filter": {"property": "Post URL", "url": {"equals": p["url"]}}})
        props = {"Views": num(p["views"]), "Likes": num(p["likes"]), "Comments": num(p["comments"]),
                 "Shares": num(p["shares"]), "Last checked": {"date": {"start": today}}}
        if q["results"]:
            notion("PATCH", f"pages/{q['results'][0]['id']}", token, {"properties": props})
        else:
            props.update({"Post": {"title": [{"text": {"content": f"{p['model']} {p['platform']} - {p['text'][:50] or '(no caption)'}"}}]},
                          "Model": {"select": {"name": p["model"]}},
                          "Platform": {"select": {"name": DB_PLATFORM.get(p["platform"], "Other")}},
                          "Post URL": {"url": p["url"]}, "Posted date": {"date": {"start": p["created"]}},
                          "Hook": {"rich_text": [{"text": {"content": p["text"][:100]}}]},
                          "Format": {"rich_text": [{"text": {"content": p["format"] or ""}}]},
                          "Notes": {"rich_text": [{"text": {"content": f"{p['source']}. Platform: {p['platform']}."}}]}})
            notion("POST", "pages", token, {"parent": {"database_id": db}, "properties": props})
    sdb = notion("GET", f"databases/{SNAP_DS}", token)["id"]
    for s in snaps:
        title = f"{s['model']} {s['platform']} {today}"
        q = notion("POST", f"databases/{sdb}/query", token, {"filter": {"property": "Snapshot", "title": {"equals": title}}})
        props = {"Snapshot": {"title": [{"text": {"content": title}}]}, "Model": {"select": {"name": s["model"]}},
                 "Platform": {"select": {"name": s["platform"]}}, "Date": {"date": {"start": today}},
                 "Followers": num(s["followers"]), "Source": {"rich_text": [{"text": {"content": s["source"]}}]}}
        if q["results"]:
            notion("PATCH", f"pages/{q['results'][0]['id']}", token, {"properties": props})
        else:
            notion("POST", "pages", token, {"parent": {"database_id": sdb}, "properties": props})
    print("Notion upsert done. At-a-glance table: replace the '## At a glance' section with out/glance.md "
          "(REST API cannot edit table blocks in place; the agent does this via Notion MCP update_content).")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ig-json", help="output of mac ~/jsw_tracker/ig_read.py (AdsPower headless, read-only)")
    ap.add_argument("--no-youtube", action="store_true")
    ap.add_argument("--no-tiktok", action="store_true")
    ap.add_argument("--x-json", help="JSON file {model: {followers, posts:[raw X post objects]}} from the x MCP tools")
    a = ap.parse_args()
    today = dt.datetime.now(ET).date().isoformat()
    key = secret("JSW-ayrshare-api-key.txt")
    posts, snaps, errs = [], [], []
    if not key:
        errs.append("Ayrshare main key file missing")
    else:
        for m in MODELS:
            p, s, e = ayrshare(m, key); posts += p; snaps += s; errs += e
    posts = [p for p in posts if p["platform"] not in ("X", "YouTube")]
    # 2026-10-21: Sienna's Default Ayrshare profile has Valentina's Facebook/YouTube linked; those belong to Valentina (already pulled via her profile)
    posts = [p for p in posts if not (p["model"] == "Sienna" and p["platform"] in ("Facebook", "YouTube"))]
    snaps = [x for x in snaps if not (x["model"] == "Sienna" and x["platform"] in ("Facebook", "YouTube"))]
    snaps = [s for s in snaps if s["platform"] != "YouTube"]
    if not a.no_youtube:
        p, s_, e = youtube_pull(); posts += p; snaps += s_; errs += e
    if not a.no_tiktok:
        s_, e = tiktok_pull(); errs += e
        got = {x["model"] for x in s_}
        snaps = [x for x in snaps if not (x["platform"] == "TikTok" and x["model"] in got)] + s_
    if a.ig_json:
        errs += merge_ig(posts, snaps, json.load(open(a.ig_json)))
    else:
        errs.append("Instagram views skipped: pass --ig-json from AdsPower ig_read.py")
    snaps = [s for s in snaps if s["platform"] != "X"]
    if os.environ.get("X_BEARER_TOKEN"):
        p, s, e = x_pull(os.environ["X_BEARER_TOKEN"]); posts += p; snaps += s; errs += e
    elif a.x_json:
        for model, d in json.load(open(a.x_json)).items():
            u = X_HANDLES[model]
            if d.get("followers") is not None:
                snaps.append({"model": model, "platform": "X", "followers": d["followers"], "source": f"X public API @{u}"})
            posts += [norm_x(model, u, t) for t in d.get("posts", [])]
    else:
        errs.append("X skipped: set X_BEARER_TOKEN or pass --x-json from the x MCP tools")
    OUT.mkdir(exist_ok=True)
    g = glance(posts, snaps, today)
    (OUT / "posts.json").write_text(json.dumps(posts, indent=1, ensure_ascii=False))
    (OUT / "snapshots.json").write_text(json.dumps([dict(s, date=today) for s in snaps], indent=1, ensure_ascii=False))
    (OUT / "glance.md").write_text(g)
    (OUT / "errors.txt").write_text("\n".join(errs))
    print(f"{len(posts)} posts, {len(snaps)} follower snapshots, {len(errs)} warnings -> {OUT}")
    for e in errs: print("  warn:", e)
    if os.environ.get("NOTION_TOKEN"):
        notion_upsert(posts, snaps, today, os.environ["NOTION_TOKEN"], g)
    else:
        print("NOTION_TOKEN not set: apply out/posts.json, out/snapshots.json, out/glance.md via Notion MCP.")


if __name__ == "__main__":
    main()
