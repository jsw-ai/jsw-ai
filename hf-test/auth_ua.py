#!/usr/bin/env python3
import json, ssl, urllib.request, urllib.error
from pathlib import Path
p = Path("/home/box/agent-data/connector-secrets/b03764fa-1acf-4eb6-b1e0-b6890366beb7/Higgsfield.json")
d = json.loads(p.read_text())
key, secret = d["HF_API_KEY"], d["HF_SECRET"]
ctx = ssl.create_default_context()
dummy = "00000000-0000-4000-8000-000000000000"
uas = [
    "higgsfield-client-py/1.0",
    "higgsfield-server-js/2.0",
    "Mozilla/5.0",
    "curl/8.5.0",
]
for ua in uas:
    headers = {
        "Authorization": f"Key {key}:{secret}",
        "Accept": "application/json",
        "User-Agent": ua,
    }
    url = f"https://platform.higgsfield.ai/requests/{dummy}/status"
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=25, context=ctx) as resp:
            body = resp.read(300).decode("utf-8", "replace")
            print(f"OK ua={ua!r} HTTP {resp.status} {body[:180]!r}")
    except urllib.error.HTTPError as e:
        body = e.read(300).decode("utf-8", "replace")
        print(f"ERR ua={ua!r} HTTP {e.code} {body[:180]!r}")
    except Exception as e:
        print(f"EXC ua={ua!r} {type(e).__name__}")
