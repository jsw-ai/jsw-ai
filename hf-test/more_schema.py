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
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            return resp.status, resp.read(8000).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(8000).decode("utf-8", "replace")
    except Exception as e:
        return 0, type(e).__name__

print("=== MORE LIST ===")
for path in [
    "/v1/soul-id", "/v1/souls/list", "/v1/references", "/v1/characters",
    "/higgsfield-ai/soul/ids", "/v2/custom-references/list",
    "/v1/custom-references/list?page=1&page_size=100",
    "/files/generate-upload-url",
]:
    method = "GET"
    body = None
    if path.endswith("generate-upload-url"):
        method = "POST"
        body = {"content_type": "image/jpeg"}
    code, raw = call(method, base+path, body)
    print(f"{method} {path} HTTP {code} {raw[:250]}")

print("=== SOUL V2 extra field probe ===")
SIENNA = "f9700355-bf71-4d6f-bec5-e87142075794"
est = base + "/estimate/higgsfield-ai/soul/v2/standard"
probes = [
    {"prompt": "x", "soul_id": SIENNA, "aspect_ratio": "3:4", "quality": "2k", "resolution": "1080p"},
    {"prompt": "x", "soul_id": SIENNA, "aspect_ratio": "3:4", "quality": "4k"},
    {"prompt": "x", "soul_id": SIENNA, "aspect_ratio": "3:4", "batch_size": 1},
    {"prompt": "x", "soul_id": SIENNA, "aspect_ratio": "3:4", "num_images": 1},
    {"prompt": "x", "soul_id": SIENNA, "aspect_ratio": "3:4", "custom_reference_strength": 1},
    {"prompt": "x", "soul_id": "not-a-uuid", "aspect_ratio": "3:4"},
]
for body in probes:
    code, raw = call("POST", est, body)
    print(f"HTTP {code} fields={sorted(body.keys())} {raw[:300]}")

print("=== SEEDANCE extra ===")
for path in [
    "/bytedance/seedance-2.0/text-to-video",
    "/bytedance/seedance/v1/pro/text-to-video",
    "/bytedance/seedance/v1/pro/fast/text-to-video",
]:
    code, raw = call("POST", base+"/estimate"+path, {"prompt": "x"})
    print(f"EST {path} HTTP {code} {raw[:300]}")
    code, raw = call("POST", base+path, {"bogus_field_xyz": True})
    print(f"SCHEMA {path} HTTP {code} {raw[:400]}")
