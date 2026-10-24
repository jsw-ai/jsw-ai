#!/usr/bin/env python3
import json, ssl, urllib.request, urllib.error
from pathlib import Path
p = Path("/home/box/agent-data/connector-secrets/b03764fa-1acf-4eb6-b1e0-b6890366beb7/Higgsfield.json")
d = json.loads(p.read_text())
key, secret = d["HF_API_KEY"], d["HF_SECRET"]
ctx = ssl.create_default_context()
H = {"Authorization": f"Key {key}:{secret}", "Accept": "application/json", "Content-Type": "application/json", "User-Agent": "higgsfield-client-py/1.0"}
base = "https://platform.higgsfield.ai"

def call(method, url, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method, headers=H)
    try:
        with urllib.request.urlopen(req, timeout=25, context=ctx) as resp:
            return resp.status, resp.read(2000).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(2000).decode("utf-8", "replace")
    except Exception as e:
        return 0, type(e).__name__

print("=== ACCOUNT ===")
for path in ["/account", "/v1/account", "/me", "/v1/me", "/credits", "/v1/credits", "/billing", "/user", "/v1/user", "/organizations", "/v1/organizations"]:
    code, raw = call("GET", base+path)
    print(f"GET {path} HTTP {code} {raw[:250]}")

print("=== RETRY GEN cheaper ===")
SIENNA = "f9700355-bf71-4d6f-bec5-e87142075794"
PROMPT = "Candid iPhone photo, natural daylight, pore-level skin texture, natural tan, relaxed natural body. Gold Coast woman, tank and shorts. NOT airbrushed, NOT glossy, NOT plastic, NOT cinematic."
for label, body in [
    ("min", {"prompt": PROMPT, "soul_id": SIENNA, "aspect_ratio": "3:4"}),
    ("q15", {"prompt": PROMPT, "soul_id": SIENNA, "aspect_ratio": "3:4", "quality": "1.5k"}),
    ("no_soul", {"prompt": "plain landscape test unused", "aspect_ratio": "1:1"}),
]:
    code, raw = call("POST", base+"/estimate/higgsfield-ai/soul/v2/standard", body)
    print(f"EST {label} HTTP {code} {raw[:200]}")
    # do NOT submit no_soul generation; only cheaper sienna if estimate is tiny
    if label != "no_soul":
        code, raw = call("POST", base+"/higgsfield-ai/soul/v2/standard", body)
        print(f"GEN {label} HTTP {code} {raw[:300]}")
