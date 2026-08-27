"""JSW AI org — encrypted credential vault.

Secrets are encrypted at rest with a Fernet master key stored 0600 on the server.
Agents call get_secret(...) at runtime; values never transit chat and are never logged.
"""
import sqlite3, os, time
from cryptography.fernet import Fernet

BASE = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE, "data", "org.db")
KEY_PATH = os.path.join(BASE, "secrets", "master.key")

def _load_key():
    if not os.path.exists(KEY_PATH):
        os.makedirs(os.path.dirname(KEY_PATH), exist_ok=True)
        k = Fernet.generate_key()
        fd = os.open(KEY_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        os.write(fd, k); os.close(fd)
    return open(KEY_PATH, "rb").read()

def _fernet():
    return Fernet(_load_key())

def _con():
    con = sqlite3.connect(DB_PATH); con.row_factory = sqlite3.Row; return con

def init_vault():
    con = _con()
    con.execute("""CREATE TABLE IF NOT EXISTS secrets(
      id INTEGER PRIMARY KEY,
      persona TEXT NOT NULL DEFAULT '*',
      service TEXT NOT NULL,
      name TEXT NOT NULL,
      value_enc BLOB NOT NULL,
      updated_at REAL,
      UNIQUE(persona, service, name))""")
    con.commit(); con.close()

def set_secret(persona, service, name, value):
    init_vault()
    enc = _fernet().encrypt(value.encode())
    con = _con()
    con.execute(
        "INSERT INTO secrets(persona,service,name,value_enc,updated_at) VALUES(?,?,?,?,?) "
        "ON CONFLICT(persona,service,name) DO UPDATE SET value_enc=excluded.value_enc, updated_at=excluded.updated_at",
        (persona, service, name, enc, time.time()))
    con.commit(); con.close()

def get_secret(persona, service, name):
    con = _con()
    row = con.execute("SELECT value_enc FROM secrets WHERE persona=? AND service=? AND name=?",
                      (persona, service, name)).fetchone()
    con.close()
    if not row:
        return None
    return _fernet().decrypt(row["value_enc"]).decode()

def list_secrets():
    """Metadata only — never returns values."""
    con = _con()
    rows = con.execute("SELECT persona,service,name,updated_at FROM secrets ORDER BY persona,service,name").fetchall()
    con.close()
    return [dict(r) for r in rows]

def delete_secret(persona, service, name):
    con = _con()
    con.execute("DELETE FROM secrets WHERE persona=? AND service=? AND name=?", (persona, service, name))
    con.commit(); con.close()

if __name__ == "__main__":
    import sys, json
    a = sys.argv[1:]
    if a and a[0] == "selftest":
        set_secret("__test__", "selftest", "k", "ok123")
        ok = get_secret("__test__", "selftest", "k") == "ok123"
        delete_secret("__test__", "selftest", "k")
        print("VAULT_SELFTEST", "PASS" if ok else "FAIL")
    elif a and a[0] == "list":
        print(json.dumps(list_secrets(), indent=1))
    elif a and a[0] == "set" and len(a) == 5:
        set_secret(a[1], a[2], a[3], a[4]); print("SET", a[1], a[2], a[3])
    else:
        print("usage: vault.py [selftest|list|set persona service name value]")
