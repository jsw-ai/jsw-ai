#!/usr/bin/env python3
import json, ssl, urllib.request, urllib.error, urllib.parse
from pathlib import Path
p = Path("/home/box/agent-data/connector-secrets/b03764fa-1acf-4eb6-b1e0-b6890366beb7/Higgsfield.json")
d = json.loads(p.read_text())
key, secret = d["HF_API_KEY"], d["HF_SECRET"]
ctx = ssl.create_default_context()
UA = "higgsfield-client-py/1.0"
SIENNA = "f9700355-bf71-4d6f-bec5-e87142075794"
PROMPT = "Editorial portrait in soft daylight"

def call(method, url, headers, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            raw = resp.read(8000).decode("utf-8", "replace")
            return resp.status, raw
    except urllib.error.HTTPError as e:
        raw = e.read(8000).decode("utf-8", "replace")
        return e.code, raw
    except Exception as e:
        return 0, type(e).__name__

def hdr(style, base_extra=None):
    h = {"Accept": "application/json", "Content-Type": "application/json", "User-Agent": UA}
    if style == "key":
        h["Authorization"] = f"Key {key}:{secret}"
    else:
        h["hf-api-key"] = key
        h["hf-secret"] = secret
    if base_extra:
        h.update(base_extra)
    return h

bases = ["https://platform.higgsfield.ai", "https://api.higgsfield.ai"]
list_paths = [
    "/v1/custom-references/list?page=1&page_size=50",
    "/v1/custom-references?page=1&page_size=50",
    "/custom-references/list?page=1&page_size=50",
    "/v1/soul-ids",
    "/soul-ids",
    "/reference-elements",
    "/v1/reference-elements",
]
print("=== LIST ===")
for base in bases:
    for style in ("key", "legacy"):
        for path in list_paths:
            code, raw = call("GET", base + path, hdr(style))
            if code in (401, 404, 405):
                print(f"{style} {base}{path.split('?')[0]} HTTP {code}")
                continue
            print(f"{style} {base}{path.split('?')[0]} HTTP {code} {raw[:500]}")

print("=== ESTIMATE SOUL2 ===")
soul_bodies = [
    ("prompt", {"prompt": PROMPT}),
    ("soul_id_45", {"prompt": PROMPT, "soul_id": SIENNA, "aspect_ratio": "4:5"}),
    ("cref_45", {"prompt": PROMPT, "custom_reference_id": SIENNA, "aspect_ratio": "4:5"}),
    ("soul_id_34_q", {"prompt": PROMPT, "soul_id": SIENNA, "aspect_ratio": "3:4", "quality": "2k"}),
    ("cref_34_q", {"prompt": PROMPT, "custom_reference_id": SIENNA, "aspect_ratio": "3:4", "quality": "2k"}),
]
for base in bases:
    for path in ("/higgsfield-ai/soul/v2/standard", "/higgsfield-ai/soul/character"):
        for label, body in soul_bodies:
            code, raw = call("POST", base + "/estimate" + path, hdr("key"), body)
            print(f"EST {base}{path} {label} HTTP {code} {raw[:400]}")
        code, raw = call("POST", base + path, hdr("key"), {})
        print(f"SCHEMA {base}{path} HTTP {code} {raw[:600]}")

print("=== ESTIMATE SEEDANCE2 ===")
sd_body = {
    "prompt": "drone shot over a mountain valley at sunrise",
    "duration": 5,
    "aspect_ratio": "16:9",
    "generate_audio": True,
    "resolution": "720p",
    "bitrate_mode": "standard",
    "mode": "std",
    "genre": "auto",
    "audio_references": [],
    "image_references": [],
    "video_references": [],
}
sd_paths = [
    "/bytedance/seedance-2.0/text-to-video",
    "/bytedance/seedance-2.0/image-to-video",
    "/bytedance/seedance-2.0/reference-to-video",
    "/bytedance/seedance-2.0/fast/text-to-video",
    "/bytedance/seedance-2.0/mini/text-to-video",
]
base = "https://platform.higgsfield.ai"
for path in sd_paths:
    code, raw = call("POST", base + "/estimate" + path, hdr("key"), sd_body)
    print(f"EST {path} HTTP {code} {raw[:500]}")
    code, raw = call("POST", base + path, hdr("key"), {})
    print(f"SCHEMA {path} HTTP {code} {raw[:700]}")
