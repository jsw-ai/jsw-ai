#!/usr/bin/env python3
import json, ssl, time, urllib.request, urllib.error
from pathlib import Path
p = Path("/home/box/agent-data/connector-secrets/b03764fa-1acf-4eb6-b1e0-b6890366beb7/Higgsfield.json")
d = json.loads(p.read_text())
key, secret = d["HF_API_KEY"], d["HF_SECRET"]
ctx = ssl.create_default_context()
H = {"Authorization": f"Key {key}:{secret}", "Accept": "application/json", "Content-Type": "application/json", "User-Agent": "higgsfield-client-py/1.0"}
base = "https://platform.higgsfield.ai"
path = "/higgsfield-ai/soul/v2/standard"
SIENNA = "f9700355-bf71-4d6f-bec5-e87142075794"
PROMPT = (
    "Candid iPhone photo, natural daylight, pore-level skin texture, natural tan, "
    "relaxed natural body. Gold Coast woman, tank and shorts. NOT airbrushed, "
    "NOT glossy, NOT plastic, NOT cinematic."
)
body = {
    "prompt": PROMPT,
    "soul_id": SIENNA,
    "aspect_ratio": "3:4",
    "quality": "2k",
}

def call(method, url, body=None, timeout=45):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method, headers=H)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            raw = resp.read().decode("utf-8", "replace")
            try:
                return resp.status, json.loads(raw), raw
            except Exception:
                return resp.status, None, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw), raw
        except Exception:
            return e.code, None, raw
    except Exception as e:
        return 0, None, type(e).__name__ + ":" + str(e)

print("SUBMIT", path, "fields", sorted(body.keys()))
code, obj, raw = call("POST", base + path, body, timeout=60)
print("SUBMIT_HTTP", code)
print("SUBMIT_BODY", raw[:1500])
Path("/workspace/hf-test/sienna_submit.json").write_text(raw if raw else "")
if not obj or not obj.get("request_id"):
    raise SystemExit("submit failed")
rid = obj["request_id"]
status_url = obj.get("status_url") or f"{base}/requests/{rid}/status"
print("JOB", rid)
deadline = time.time() + 180
last_obj = obj
last_raw = raw
while time.time() < deadline:
    code, obj, raw = call("GET", status_url, timeout=30)
    last_obj, last_raw = obj, raw
    st = (obj or {}).get("status") if isinstance(obj, dict) else None
    print("POLL", code, st)
    if st in ("completed", "failed", "nsfw", "canceled", "cancelled"):
        break
    time.sleep(5)
print("FINAL", last_raw[:2500])
Path("/workspace/hf-test/sienna_status.json").write_text(last_raw if last_raw else "")
url = None
if isinstance(last_obj, dict):
    images = last_obj.get("images") or []
    if images and isinstance(images, list):
        first = images[0]
        if isinstance(first, dict):
            url = first.get("url")
            rawr = first.get("raw")
            if not url and isinstance(rawr, dict):
                url = rawr.get("url")
        elif isinstance(first, str):
            url = first
    if not url:
        jobs = last_obj.get("jobs") or []
        if jobs and isinstance(jobs[0], dict):
            res = jobs[0].get("results") or {}
            if isinstance(res, dict):
                rawr = res.get("raw") or res.get("min") or {}
                if isinstance(rawr, dict):
                    url = rawr.get("url")
if url:
    low = url.lower().split("?")[0]
    ext = ".jpg"
    if low.endswith(".png"):
        ext = ".png"
    elif low.endswith(".webp"):
        ext = ".webp"
    dest = Path("/workspace/hf-test") / f"sienna_soul2_test{ext}"
    req = urllib.request.Request(url, headers={"User-Agent": "higgsfield-client-py/1.0"})
    with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
        data = resp.read()
    dest.write_bytes(data)
    print("SAVED", dest, "bytes", len(data))
else:
    print("NO_IMAGE_URL")
