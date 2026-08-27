"""Instantiate the JSW AI org: 3 couple-teams + support agents, with reporting lines."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(__file__))
import db

COUPLES = [
    {"team": "The Roses",      "members": [("Charlotte", "charlotte", "England"), ("Madison", "madison", "England")]},
    {"team": "Sunset & Seine", "members": [("Sienna Blake", "sienna", "Australia"), ("Camille", "camille", "Paris")]},
    {"team": "Miami Nights",   "members": [("Valentina", "valentina", "Miami"), ("Gabriela", "gabriela", "Miami")]},
]
PLATFORMS = ["tiktok", "instagram", "x", "youtube", "reddit", "facebook", "fanvue"]
FUNCTIONS = ["content_creator", "comment_dm", "affiliate", "shop", "subscription"]
DEPT_HEADS = ["content", "growth", "operations"]
SUPPORT_PARENT = {"onboarding": "dept_head:operations", "compliance": "ceo",
                  "accounting": "ceo", "reporting": "ceo"}

def reset():
    con = db.connect()
    con.execute("DELETE FROM agents"); con.execute("DELETE FROM teams")
    con.commit(); con.close()

def get_team(name):
    con = db.connect()
    con.execute("INSERT OR IGNORE INTO teams(name, created_at) VALUES(?,?)", (name, time.time()))
    con.commit()
    tid = con.execute("SELECT id FROM teams WHERE name=?", (name,)).fetchone()["id"]
    con.close()
    return tid

def persona_id(slug):
    con = db.connect()
    r = con.execute("SELECT id FROM personas WHERE slug=?", (slug,)).fetchone()
    con.close()
    return r["id"] if r else None

def make_agent(kind, name, pid=None, team_id=None, config=None):
    con = db.connect()
    con.execute("INSERT INTO agents(persona_id,team_id,kind,name,status,config_json,created_at) VALUES(?,?,?,?,?,?,?)",
                (pid, team_id, kind, name, "idle", json.dumps(config or {}), time.time()))
    con.commit(); con.close()

def build():
    reset()
    make_agent("leadership", "ceo", config={"reports_to": None, "interval": 300})
    for d in DEPT_HEADS:
        make_agent("leadership", "dept_head:" + d, config={"reports_to": "ceo", "interval": 300})
    for c in COUPLES:
        tid = get_team(c["team"]); mem = c["members"]; mgr = "manager:" + c["team"]
        for i, (name, slug, geo) in enumerate(mem):
            partner = mem[1 - i]
            db.upsert_persona(name, slug, geo, {"team": c["team"], "partner_slug": partner[1], "partner_name": partner[0]})
            make_agent("model", "model:" + slug, persona_id(slug), tid, {"reports_to": mgr, "interval": 120})
        make_agent("manager", mgr, None, tid, {"reports_to": "dept_head:operations", "interval": 180})
        make_agent("reviewer", "reviewer:" + c["team"], None, tid, {"reports_to": mgr, "interval": 180})
    make_agent("manager", "manager:platforms", config={"reports_to": "dept_head:growth", "interval": 300})
    for p in PLATFORMS:
        make_agent("platform", "platform:" + p, config={"reports_to": "manager:platforms", "interval": 600})
    for f in FUNCTIONS:
        parent = "dept_head:content" if f == "content_creator" else "dept_head:growth"
        make_agent("function", "function:" + f, config={"reports_to": parent, "interval": 600})
    for s, parent in SUPPORT_PARENT.items():
        make_agent("leadership", "support:" + s, config={"reports_to": parent, "interval": 600})
    db.log_event("build_org", "couples_structure", {"teams": len(COUPLES)})

# ---- sample "what each agent is doing" + activity log --------------------
SAMPLE_TASK = {
    "model": "Publish + engage across today's content slots",
    "manager": "Move the team up the scoreboard this week",
    "reviewer": "Review & approve today's content queue",
    "platform": "Refresh this platform's trend playbook",
    "function": "Teach the model agents this week's best practices",
    "leadership": "Track performance and unblock the teams",
}
SAMPLE_LOG = {
    "model": ["Reviewed today's content queue", "Replied to 4 comments in-voice", "Drafted tomorrow's hook"],
    "manager": ["Checked the team scoreboard", "Nudged the lowest performer", "Reviewed weekly targets"],
    "reviewer": ["Approved 3 posts, flagged 1", "Updated the review rubric", "Ran brand-safety on drafts"],
    "platform": ["Pulled trending audio", "Logged best posting times", "Updated the platform playbook"],
    "function": ["Researched top-performing hooks", "Updated the shared playbook", "Summarized what's working"],
    "leadership": ["Reviewed the org scoreboard", "Checked agent health", "Set weekly priorities"],
}

def seed_activity(force=False):
    con = db.connect()
    n = con.execute("SELECT COUNT(*) c FROM events WHERE actor LIKE 'agent:%'").fetchone()["c"]
    if n > 0 and not force:
        con.close(); return False
    agents = con.execute("SELECT id, kind FROM agents").fetchall()
    now = time.time()
    for a in agents:
        task = SAMPLE_TASK.get(a["kind"], "Working")
        con.execute("INSERT INTO tasks(agent_id,title,status,priority,created_at,updated_at) VALUES(?,?,?,?,?,?)",
                    (a["id"], task, "in_progress", 2, now, now))
        for i, line in enumerate(SAMPLE_LOG.get(a["kind"], ["Working"])):
            con.execute("INSERT INTO events(ts,actor,kind,detail_json) VALUES(?,?,?,?)",
                        (now - (i + 1) * 1800, "agent:%d" % a["id"], "log", json.dumps({"msg": line})))
    con.commit(); con.close()
    return True

def summary():
    con = db.connect()
    rows = con.execute("SELECT kind, COUNT(*) c FROM agents GROUP BY kind ORDER BY kind").fetchall()
    teams = con.execute("SELECT name FROM teams ORDER BY name").fetchall()
    total = con.execute("SELECT COUNT(*) c FROM agents").fetchone()["c"]
    con.close()
    return {"teams": [t["name"] for t in teams], "agents_total": total,
            "by_kind": {r["kind"]: r["c"] for r in rows}}

if __name__ == "__main__":
    build(); seed_activity(force=True)
    print("SUMMARY", json.dumps(summary()))
