"""JSW AI org — core data layer (SQLite)."""
import sqlite3, os, json, time

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "org.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS personas(
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  geo TEXT,
  status TEXT DEFAULT 'active',
  meta_json TEXT DEFAULT '{}',
  created_at REAL
);
CREATE TABLE IF NOT EXISTS teams(
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  created_at REAL
);
CREATE TABLE IF NOT EXISTS agents(
  id INTEGER PRIMARY KEY,
  persona_id INTEGER,
  team_id INTEGER,
  kind TEXT NOT NULL,
  name TEXT,
  status TEXT DEFAULT 'idle',
  config_json TEXT DEFAULT '{}',
  created_at REAL
);
CREATE TABLE IF NOT EXISTS platform_accounts(
  id INTEGER PRIMARY KEY,
  persona_id INTEGER,
  platform TEXT NOT NULL,
  handle TEXT,
  status TEXT DEFAULT 'unconfigured',
  meta_json TEXT DEFAULT '{}',
  UNIQUE(persona_id, platform)
);
CREATE TABLE IF NOT EXISTS metrics(
  id INTEGER PRIMARY KEY,
  persona_id INTEGER,
  platform TEXT,
  metric TEXT NOT NULL,
  value REAL,
  ts REAL
);
CREATE TABLE IF NOT EXISTS tasks(
  id INTEGER PRIMARY KEY,
  agent_id INTEGER,
  persona_id INTEGER,
  title TEXT NOT NULL,
  detail TEXT,
  status TEXT DEFAULT 'pending',
  priority INTEGER DEFAULT 3,
  scheduled_for REAL,
  created_at REAL,
  updated_at REAL
);
CREATE TABLE IF NOT EXISTS content_items(
  id INTEGER PRIMARY KEY,
  persona_id INTEGER,
  platform TEXT,
  kind TEXT,
  path TEXT,
  caption TEXT,
  status TEXT DEFAULT 'draft',
  slot_time REAL,
  review_notes TEXT,
  created_at REAL,
  updated_at REAL
);
CREATE TABLE IF NOT EXISTS events(
  id INTEGER PRIMARY KEY,
  ts REAL,
  actor TEXT,
  kind TEXT,
  detail_json TEXT
);
"""

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL;")
    return con

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = connect()
    con.executescript(SCHEMA)
    con.commit(); con.close()

def log_event(actor, kind, detail=None):
    con = connect()
    con.execute("INSERT INTO events(ts,actor,kind,detail_json) VALUES(?,?,?,?)",
                (time.time(), actor, kind, json.dumps(detail or {})))
    con.commit(); con.close()

def upsert_persona(name, slug, geo=None, meta=None):
    con = connect()
    con.execute(
        "INSERT INTO personas(name,slug,geo,meta_json,created_at) VALUES(?,?,?,?,?) "
        "ON CONFLICT(slug) DO UPDATE SET name=excluded.name, geo=excluded.geo, meta_json=excluded.meta_json",
        (name, slug, geo, json.dumps(meta or {}), time.time()))
    con.commit(); con.close()

def get_personas():
    con = connect()
    rows = con.execute("SELECT * FROM personas ORDER BY name").fetchall()
    con.close()
    return [dict(r) for r in rows]

def add_metric(persona_id, platform, metric, value):
    con = connect()
    con.execute("INSERT INTO metrics(persona_id,platform,metric,value,ts) VALUES(?,?,?,?,?)",
                (persona_id, platform, metric, value, time.time()))
    con.commit(); con.close()

def scoreboard():
    """Latest value per persona+metric, summed into a simple ranking."""
    con = connect()
    rows = con.execute("""
      SELECT p.name AS persona, m.platform, m.metric, m.value, m.ts
      FROM metrics m JOIN personas p ON p.id=m.persona_id
      WHERE m.ts = (SELECT MAX(ts) FROM metrics m2
                    WHERE m2.persona_id=m.persona_id AND m2.platform IS m.platform AND m2.metric=m.metric)
      ORDER BY p.name
    """).fetchall()
    con.close()
    return [dict(r) for r in rows]
