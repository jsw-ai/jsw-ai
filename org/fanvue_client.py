"""Fanvue OAuth 2.0 client (PKCE) — credentials + tokens live in the vault.

Flow: /org/fanvue/connect -> auth.fanvue.com consent (Sienna's browser, one time)
-> /org/fanvue/callback exchanges the code server-side -> tokens stored in vault.
Daemons call access_token(); refresh is automatic (rotating refresh tokens).
"""
import base64, hashlib, json, os, secrets as pysecrets, sys, time

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db  # noqa: E402
import vault  # noqa: E402

AUTH = "https://auth.fanvue.com/oauth2/auth"
TOKEN = "https://auth.fanvue.com/oauth2/token"
API = "https://api.fanvue.com"
SCOPES = ("openid offline_access offline read:self read:creator read:post "
          "read:media read:insights read:chat write:post write:media")
REDIRECT = "https://206-81-3-238.sslip.io/org/fanvue/callback"


def _cred():
    cid = (vault.get_secret("*", "fanvue", "FANVUE_CLIENT_ID") or "").strip()
    sec = (vault.get_secret("*", "fanvue", "FANVUE_CLIENT_SECRET") or "").strip()
    if not cid or not sec:
        raise RuntimeError("fanvue client credentials missing from vault")
    return cid, sec


def _basic():
    cid, sec = _cred()
    return {"Authorization": "Basic " + base64.b64encode((cid + ":" + sec).encode()).decode()}


def _set(k, v):
    con = db.connect()
    con.execute("INSERT INTO settings(key,value) VALUES(?,?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value", (k, v))
    con.commit(); con.close()


def _get(k):
    con = db.connect()
    try:
        r = con.execute("SELECT value FROM settings WHERE key=?", (k,)).fetchone()
        return r["value"] if r else None
    finally:
        con.close()


def authorize_url():
    cid, _ = _cred()
    ver = base64.urlsafe_b64encode(pysecrets.token_bytes(48)).decode().rstrip("=")
    chal = base64.urlsafe_b64encode(hashlib.sha256(ver.encode()).digest()).decode().rstrip("=")
    state = pysecrets.token_urlsafe(24)
    _set("fanvue_pkce_verifier", ver)
    _set("fanvue_oauth_state", state)
    from urllib.parse import urlencode
    q = urlencode({"response_type": "code", "client_id": cid, "redirect_uri": REDIRECT,
                   "scope": SCOPES, "state": state,
                   "code_challenge": chal, "code_challenge_method": "S256"})
    return AUTH + "?" + q


def exchange(code, state):
    if not code:
        raise RuntimeError("no authorization code in callback")
    if state != _get("fanvue_oauth_state"):
        raise RuntimeError("state mismatch — retry Connect")
    ver = _get("fanvue_pkce_verifier")
    r = requests.post(TOKEN, headers=_basic(),
                      data={"grant_type": "authorization_code", "code": code,
                            "redirect_uri": REDIRECT, "code_verifier": ver}, timeout=30)
    if r.status_code >= 300:
        raise RuntimeError("token exchange failed: %s %s" % (r.status_code, r.text[:200]))
    _store(r.json())
    return True


def _store(j):
    j["expires_at"] = time.time() + float(j.get("expires_in") or 3600) - 60
    vault.set_secret("*", "fanvue", "oauth_tokens", json.dumps(j))
    db.log_event("fanvue", "tokens", {"msg": "fanvue oauth tokens stored/refreshed"})


def _tokens():
    raw = vault.get_secret("*", "fanvue", "oauth_tokens")
    return json.loads(raw) if raw else None


def connected():
    return _tokens() is not None


def access_token():
    t = _tokens()
    if not t:
        raise RuntimeError("fanvue not connected — use the Connect Fanvue button on /vault")
    if time.time() < t.get("expires_at", 0):
        return t["access_token"]
    r = requests.post(TOKEN, headers=_basic(),
                      data={"grant_type": "refresh_token",
                            "refresh_token": t["refresh_token"]}, timeout=30)
    if r.status_code >= 300:
        raise RuntimeError("refresh failed: %s %s" % (r.status_code, r.text[:200]))
    _store(r.json())
    return _tokens()["access_token"]


def api_get(path):
    r = requests.get(API + path, headers={"Authorization": "Bearer " + access_token()},
                     timeout=30)
    try:
        body = r.json()
    except Exception:
        body = r.text[:300]
    return r.status_code, body
