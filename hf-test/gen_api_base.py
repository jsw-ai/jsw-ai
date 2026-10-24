#!/usr/bin/env python3
import json, ssl, urllib.request, urllib.error
from pathlib import Path
p = Path("/home/box/agent-data/connector-secrets/b03764fa-1acf-4eb6-b1e0-b6890366beb7/Higgsfield.json")
d = json.loads(p.read_text())
key, secret = d["HF_API_KEY"], d["HF_SECRET"]
ctx = ssl.create_default_context()
H = {"Authorization": f"Key {key}:{secret}", "Accept": "application/json", "Content-Type": "application/json", "User-Agent": "higgsfield-client-py/1.0"}
SIENNA = "f9700355-bf71-4d6f-bec5-e87142075794"
PROMPT = "Candid iPhone photo, natural daylight, pore-level skin texture, natural tan, relaxed natural body. Gold Coast woman, tank and shorts. NOT airbrushed, NOT glossy, NOT plastic, NOT cinematic."
body = {"prompt": PROMPT, "soul_id": SIENNA, "aspect_ratio": "3:4", "quality": "2k"}
url = "https://api.higgsfield.ai/higgsfield-ai/soul/v2/standard"
req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST", headers=H)
try:
    with urllib.request.urlopen(req, timeout=45, context=ctx) as resp:
        print("HTTP", resp.status, resp.read(800).decode())
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read(800).decode())
