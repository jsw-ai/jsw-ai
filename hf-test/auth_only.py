#!/usr/bin/env python3
import json, ssl, urllib.request, urllib.error
from pathlib import Path
p = Path("/home/box/agent-data/connector-secrets/b03764fa-1acf-4eb6-b1e0-b6890366beb7/Higgsfield.json")
d = json.loads(p.read_text())
key, secret = d["HF_API_KEY"], d["HF_SECRET"]
ctx = ssl.create_default_context()
headers_a = {"Authorization": f"Key {key}:{secret}", "Accept": "application/json"}
headers_b = {"hf-api-key": key, "hf-secret": secret, "Accept": "application/json"}
dummy = "00000000-0000-4000-8000-000000000000"
for base in ("https://platform.higgsfield.ai", "https://api.higgsfield.ai"):
    for name, hdrs in (("keyhdr", headers_a), ("legacy", headers_b)):
        url = f"{base}/requests/{dummy}/status"
        req = urllib.request.Request(url, headers=hdrs, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=25, context=ctx) as resp:
                body = resp.read(500).decode("utf-8", "replace")
                print(f"OK {name} {base} HTTP {resp.status} {body[:200]!r}")
        except urllib.error.HTTPError as e:
            body = e.read(500).decode("utf-8", "replace")
            print(f"ERR {name} {base} HTTP {e.code} {body[:200]!r}")
        except Exception as e:
            print(f"EXC {name} {base} {type(e).__name__}")
