"""Bootstrap the JSW AI org: init DB + vault, seed personas, self-test."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import db, vault

PERSONAS = [
    ("Sienna Blake", "sienna", "Australia"),
    ("Charlotte", "charlotte", None),
    ("Madison", "madison", None),
    ("Camille", "camille", None),
    ("Gabriela", "gabriela", None),
    ("Valentina", "valentina", None),
]

def main():
    db.init_db()
    vault.init_vault()
    for name, slug, geo in PERSONAS:
        db.upsert_persona(name, slug, geo)
    vault.set_secret("__test__", "selftest", "k", "ok123")
    passed = vault.get_secret("__test__", "selftest", "k") == "ok123"
    vault.delete_secret("__test__", "selftest", "k")
    db.log_event("init_org", "bootstrap", {"personas": len(PERSONAS), "vault_ok": passed})
    ps = db.get_personas()
    print("PERSONAS_SEEDED", len(ps))
    for p in ps:
        print("  -", p["name"], "(" + p["slug"] + ")", p["geo"] or "")
    print("VAULT_SELFTEST", "PASS" if passed else "FAIL")
    print("DB_READY", os.path.exists(db.DB_PATH))

if __name__ == "__main__":
    main()
