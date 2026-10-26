#!/opt/jsw/.venv/bin/python
"""ONE Sienna Soul 2 test image (smoke test, not content: never post it or send it to the Reviewer).
Quotes the cost first, submits once (no auto-resubmit), polls to completion, saves as PNG.

usage: gen_sienna.py [OUT.png]     default /var/www/html/_sienna_test.png
"""
import json, sys, time, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from balance import SIENNA, authed_headers, call

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/var/www/html/_sienna_test.png")
PATH = "/higgsfield-ai/soul/v2/standard"
BODY = {"prompt": "Candid iPhone portrait, soft daylight evenly lit from the front, closed-mouth soft "
                  "smile, woman in a plain white t-shirt on a sunny cafe terrace, head and shoulders, "
                  "natural unretouched skin texture.",
        "soul_id": SIENNA, "aspect_ratio": "3:4", "quality": "2k"}
LOG = Path(f"/opt/jsw-data/hf_smoke{OUT.stem.removeprefix('_sienna_test')}_sienna.json")

h, s = authed_headers()
if s != 200:
    sys.exit(f"AUTH FAILED HTTP {s}")
s, t = call("POST", "/estimate" + PATH, BODY, h)
print("QUOTE", s, t, flush=True)
s, t = call("POST", PATH, BODY, h)
print("SUBMIT", s, t[:400], flush=True)
if s != 200:
    sys.exit(f"not submitted (HTTP {s}) - nothing generated")
job = json.loads(t)
rid = job["request_id"]
st = {}
for _ in range(60):
    time.sleep(5)
    s, t = call("GET", f"/requests/{rid}/status", h=h)
    st = json.loads(t) if s == 200 else {}
    print("POLL", s, st.get("status"), flush=True)
    if st.get("status") in ("completed", "failed", "nsfw", "canceled", "cancelled"):
        break
LOG.write_text(json.dumps({"request_id": rid, "submit": job, "final": st}, indent=1))
if st.get("status") != "completed":
    sys.exit(f"job {rid} ended {st.get('status')!r} - see {LOG}")
imgs = st.get("images") or []
url = (imgs[0].get("url") if imgs and isinstance(imgs[0], dict) else (imgs[0] if imgs else None))
if not url:
    sys.exit(f"completed but no image url - see {LOG}")
data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "higgsfield-client-py/1.0"}),
                              timeout=60).read()
if data[:8] != b"\x89PNG\r\n\x1a\n":  # job returned jpg/webp: convert so the .png is really PNG
    import cv2, numpy as np
    data = cv2.imencode(".png", cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR))[1].tobytes()
OUT.write_bytes(data)
print("SAVED", OUT, len(data), "bytes | request", rid)
