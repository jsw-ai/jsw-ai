"""JSW AI org — metrics model, sample data, and overall-score algorithm."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(__file__))
import db

# key, label, format, weight (weights sum to 1.0)
METRICS = [
    {"key": "avg_post_views",  "label": "Avg Views / Post",   "fmt": "int",   "weight": 0.10},
    {"key": "profile_views",   "label": "Profile Views",      "fmt": "int",   "weight": 0.08},
    {"key": "avg_post_likes",  "label": "Avg Likes / Post",   "fmt": "int",   "weight": 0.09},
    {"key": "total_likes",     "label": "Profile Likes",      "fmt": "int",   "weight": 0.05},
    {"key": "avg_comments",    "label": "Avg Comments / Post","fmt": "int",   "weight": 0.08},
    {"key": "followers",       "label": "Followers",          "fmt": "int",   "weight": 0.10},
    {"key": "x_subs",          "label": "X Subs",             "fmt": "int",   "weight": 0.10},
    {"key": "fanvue_subs",     "label": "Fanvue Subs",        "fmt": "int",   "weight": 0.15},
    {"key": "revenue",         "label": "Revenue (30d)",      "fmt": "money", "weight": 0.20},
    {"key": "engagement_rate", "label": "Engagement %",       "fmt": "pct",   "weight": 0.05},
]

# Realistic sample data so the board is interactive before live collectors run.
SAMPLE = {
    "sienna":    {"avg_post_views": 48000, "profile_views": 132000, "avg_post_likes": 5400, "total_likes": 910000, "avg_comments": 230, "followers": 86000, "x_subs": 340, "fanvue_subs": 640, "revenue": 8600, "engagement_rate": 6.3},
    "camille":   {"avg_post_views": 31000, "profile_views": 74000,  "avg_post_likes": 3100, "total_likes": 410000, "avg_comments": 140, "followers": 47000, "x_subs": 190, "fanvue_subs": 410, "revenue": 5200, "engagement_rate": 5.4},
    "charlotte": {"avg_post_views": 52000, "profile_views": 141000, "avg_post_likes": 6100, "total_likes": 980000, "avg_comments": 260, "followers": 93000, "x_subs": 380, "fanvue_subs": 720, "revenue": 9800, "engagement_rate": 6.7},
    "madison":   {"avg_post_views": 39000, "profile_views": 98000,  "avg_post_likes": 4200, "total_likes": 560000, "avg_comments": 180, "followers": 61000, "x_subs": 250, "fanvue_subs": 520, "revenue": 6400, "engagement_rate": 5.9},
    "valentina": {"avg_post_views": 27000, "profile_views": 63000,  "avg_post_likes": 2600, "total_likes": 330000, "avg_comments": 120, "followers": 38000, "x_subs": 150, "fanvue_subs": 300, "revenue": 3900, "engagement_rate": 5.1},
    "gabriela":  {"avg_post_views": 34000, "profile_views": 81000,  "avg_post_likes": 3600, "total_likes": 470000, "avg_comments": 160, "followers": 52000, "x_subs": 210, "fanvue_subs": 450, "revenue": 5800, "engagement_rate": 5.6},
}

def record(slug, key, value, platform=None):
    con = db.connect()
    r = con.execute("SELECT id FROM personas WHERE slug=?", (slug,)).fetchone()
    if r:
        con.execute("INSERT INTO metrics(persona_id,platform,metric,value,ts) VALUES(?,?,?,?,?)",
                    (r["id"], platform, key, value, time.time()))
        con.commit()
    con.close()

def seed_sample(force=False):
    con = db.connect()
    n = con.execute("SELECT COUNT(*) c FROM metrics").fetchone()["c"]
    con.close()
    if n > 0 and not force:
        return False
    for slug, vals in SAMPLE.items():
        for k, v in vals.items():
            record(slug, k, v)
    db.log_event("metrics", "seed_sample", {"personas": len(SAMPLE)})
    return True

def _latest():
    con = db.connect()
    rows = con.execute("""SELECT persona_id, metric, value FROM metrics m
        WHERE ts = (SELECT MAX(ts) FROM metrics m2
                    WHERE m2.persona_id=m.persona_id AND m2.metric=m.metric)""").fetchall()
    con.close()
    d = {}
    for r in rows:
        d.setdefault(r["persona_id"], {})[r["metric"]] = r["value"]
    return d

def board_data():
    personas = db.get_personas()
    latest = _latest()
    ranges = {}
    for m in METRICS:
        vals = [latest.get(p["id"], {}).get(m["key"], 0) or 0 for p in personas]
        ranges[m["key"]] = (min(vals) if vals else 0, max(vals) if vals else 0)
    con = db.connect()
    teams = con.execute("SELECT * FROM teams").fetchall()
    tmap = {t["id"]: t["name"] for t in teams}
    amap = con.execute("SELECT persona_id, team_id FROM agents WHERE kind='model'").fetchall()
    con.close()
    p2t = {a["persona_id"]: a["team_id"] for a in amap}
    out_p = []
    for p in personas:
        met = latest.get(p["id"], {})
        score = 0.0
        for m in METRICS:
            lo, hi = ranges[m["key"]]
            v = met.get(m["key"], 0) or 0
            norm = 0.5 if hi == lo else (v - lo) / (hi - lo)
            score += m["weight"] * norm
        meta = json.loads(p["meta_json"] or "{}")
        out_p.append({
            "slug": p["slug"], "name": p["name"], "geo": p["geo"],
            "team": tmap.get(p2t.get(p["id"]), ""),
            "partner_slug": meta.get("partner_slug"), "partner_name": meta.get("partner_name"),
            "metrics": {m["key"]: met.get(m["key"], 0) or 0 for m in METRICS},
            "score": round(score * 100, 1),
        })
    out_p.sort(key=lambda x: -x["score"])
    for i, o in enumerate(out_p, 1):
        o["rank"] = i
    teams_out = {}
    for o in out_p:
        t = teams_out.setdefault(o["team"], {"team": o["team"], "members": [], "revenue": 0, "fanvue_subs": 0})
        t["members"].append({"slug": o["slug"], "name": o["name"], "score": o["score"],
                             "partner_slug": o["partner_slug"], "geo": o["geo"]})
        t["revenue"] += o["metrics"]["revenue"]
        t["fanvue_subs"] += o["metrics"]["fanvue_subs"]
    tlist = []
    for t in teams_out.values():
        t["score"] = round(sum(m["score"] for m in t["members"]) / max(1, len(t["members"])), 1)
        tlist.append(t)
    tlist.sort(key=lambda x: -x["score"])
    for i, t in enumerate(tlist, 1):
        t["rank"] = i
    con = db.connect()
    try:
        row = con.execute("SELECT value FROM settings WHERE key='live_metrics'").fetchone()
    except Exception:
        row = None
    con.close()
    return {"metrics": METRICS, "personas": out_p, "teams": tlist,
            "sample": not (row and row["value"] == "1")}
