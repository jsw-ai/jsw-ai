"""JSW AI org — base agent framework.

Every agent (model, manager, reviewer, platform, function, ceo, ...) subclasses Agent
and implements tick(). The base handles config, secret access via the vault, task
queue, status/heartbeat, and structured event logging.
"""
import time, json, sys, os, traceback
sys.path.insert(0, os.path.dirname(__file__))
import db, vault

class Agent:
    kind = "base"

    def __init__(self, agent_id):
        self.agent_id = int(agent_id)
        row = self._load()
        self.persona_id = row["persona_id"]
        self.team_id = row["team_id"]
        self.name = row["name"]
        self.config = json.loads(row["config_json"] or "{}")
        self.interval = self.config.get("interval", 60)

    def _load(self):
        con = db.connect()
        r = con.execute("SELECT * FROM agents WHERE id=?", (self.agent_id,)).fetchone()
        con.close()
        if not r:
            raise ValueError("no agent " + str(self.agent_id))
        return r

    def persona_slug(self):
        if not self.persona_id:
            return "*"
        con = db.connect()
        r = con.execute("SELECT slug FROM personas WHERE id=?", (self.persona_id,)).fetchone()
        con.close()
        return r["slug"] if r else "*"

    def secret(self, service, name):
        """Persona-scoped secret, falling back to a shared '*' secret."""
        slug = self.persona_slug()
        return vault.get_secret(slug, service, name) or vault.get_secret("*", service, name)

    def set_status(self, status):
        con = db.connect()
        con.execute("UPDATE agents SET status=? WHERE id=?", (status, self.agent_id))
        con.commit(); con.close()

    def heartbeat(self):
        self.config["last_beat"] = time.time()
        con = db.connect()
        con.execute("UPDATE agents SET config_json=? WHERE id=?",
                    (json.dumps(self.config), self.agent_id))
        con.commit(); con.close()

    def log(self, kind, detail=None):
        db.log_event("agent:%s" % self.agent_id, kind, detail)

    def next_task(self):
        con = db.connect()
        r = con.execute(
            "SELECT * FROM tasks WHERE agent_id=? AND status='pending' ORDER BY priority, created_at LIMIT 1",
            (self.agent_id,)).fetchone()
        con.close()
        return dict(r) if r else None

    def complete_task(self, task_id, status="done"):
        con = db.connect()
        con.execute("UPDATE tasks SET status=?, updated_at=? WHERE id=?",
                    (status, time.time(), task_id))
        con.commit(); con.close()

    def tick(self):
        """Override: one unit of work. Base no-ops."""
        return

    def run(self, once=False):
        self.set_status("running"); self.log("start")
        try:
            while True:
                self.heartbeat()
                try:
                    self.tick()
                except Exception as e:
                    self.log("error", {"err": str(e), "tb": traceback.format_exc()[-1500:]})
                    self.set_status("error")
                if once:
                    break
                time.sleep(self.interval)
        finally:
            self.set_status("idle"); self.log("stop")


# ---- registry: kind -> class -----------------------------------------------
REGISTRY = {}

def register(cls):
    REGISTRY[cls.kind] = cls
    return cls

# Lightweight built-in kinds. Real platform/content logic is added incrementally.
@register
class ModelAgent(Agent):
    kind = "model"
    def tick(self):
        t = self.next_task()
        if t:
            self.log("task_seen", {"title": t["title"]})

@register
class ManagerAgent(Agent):
    kind = "manager"

@register
class ReviewerAgent(Agent):
    kind = "reviewer"

@register
class PlatformAgent(Agent):
    kind = "platform"

@register
class FunctionAgent(Agent):
    kind = "function"

@register
class LeadershipAgent(Agent):
    kind = "leadership"

def make(agent_id):
    con = db.connect()
    r = con.execute("SELECT kind FROM agents WHERE id=?", (int(agent_id),)).fetchone()
    con.close()
    cls = REGISTRY.get(r["kind"], Agent) if r else Agent
    return cls(agent_id)
