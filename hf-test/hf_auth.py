#!/usr/bin/env python3
"""Higgsfield API credentials from 1Password (vault JSW, item "JSW - Higgsfield API").

KEY_ID = item username, KEY_SECRET = item password; if the password is empty, the username holds
"KEY_ID:KEY_SECRET" and is split on the first ':'. Auth headers: hf-api-key / hf-secret.
Never print or log the returned values.
"""
import os, subprocess
from pathlib import Path

OP_ENV = Path("/etc/jsw/op.env")
ITEM = "op://JSW/JSW - Higgsfield API"
BASE = "https://platform.higgsfield.ai"


def _op(field):
    env = dict(os.environ)
    for line in OP_ENV.read_text().splitlines():
        k, _, v = line.partition("=")
        if k.strip():
            env[k.strip()] = v.strip()
    r = subprocess.run(["op", "read", f"{ITEM}/{field}"], env=env, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def creds():
    user, pw = _op("username"), _op("password")
    if not pw:
        user, _, pw = user.partition(":")
    if not user or not pw:
        raise SystemExit("Higgsfield creds missing/unparseable in 1Password item 'JSW - Higgsfield API'")
    return user, pw


def headers():
    kid, sec = creds()
    return {"hf-api-key": kid, "hf-secret": sec, "Accept": "application/json",
            "Content-Type": "application/json", "User-Agent": "higgsfield-client-py/1.0"}
