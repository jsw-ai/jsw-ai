"""JSW AI org — scoreboard: rank personas and teams from latest metrics."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import db

WEIGHTS = {"followers": 1.0, "likes": 0.1, "comments": 0.5,
           "subs": 5.0, "revenue": 10.0, "posts": 0.2}

def _latest_metrics():
    con = db.connect()
    rows = con.execute("""
      SELECT persona_id, platform, metric, value FROM metrics m
      WHERE ts = (SELECT MAX(ts) FROM metrics m2
                  WHERE m2.persona_id=m.persona_id AND m2.metric=m.metric
                  AND (m2.platform IS m.platform))
    """).fetchall()
    con.close()
    return rows

def persona_scores():
    rows = _latest_metrics()
    agg = {}
    for r in rows:
        d = agg.setdefault(r["persona_id"], {"score": 0.0, "metrics": {}})
        d["metrics"][r["metric"]] = r["value"]
        d["score"] += WEIGHTS.get(r["metric"], 0) * (r["value"] or 0)
    personas = {p["id"]: p for p in db.get_personas()}
    out = []
    for pid, p in personas.items():
        d = agg.get(pid, {"score": 0.0, "metrics": {}})
        out.append({"persona": p["name"], "slug": p["slug"],
                    "score": round(d["score"], 1), "metrics": d["metrics"]})
    out.sort(key=lambda x: -x["score"])
    for i, o in enumerate(out, 1):
        o["rank"] = i
    return out

def team_scores():
    con = db.connect()
    teams = con.execute("SELECT * FROM teams").fetchall()
    # map persona_id -> team via model agents
    m = con.execute("SELECT persona_id, team_id FROM agents WHERE kind='model' AND team_id IS NOT NULL").fetchall()
    con.close()
    p2t = {r["persona_id"]: r["team_id"] for r in m}
    pscores = {}
    for ps in persona_scores():
        con = db.connect()
        r = con.execute("SELECT id FROM personas WHERE slug=?", (ps["slug"],)).fetchone()
        con.close()
        if r:
            pscores[r["id"]] = ps["score"]
    out = []
    for t in teams:
        members = [pid for pid, tid in p2t.items() if tid == t["id"]]
        score = round(sum(pscores.get(pid, 0) for pid in members), 1)
        out.append({"team": t["name"], "team_id": t["id"], "members": len(members), "score": score})
    out.sort(key=lambda x: -x["score"])
    for i, o in enumerate(out, 1):
        o["rank"] = i
    return out

if __name__ == "__main__":
    import json
    print("PERSONAS:", json.dumps(persona_scores(), indent=1))
    print("TEAMS:", json.dumps(team_scores(), indent=1))
