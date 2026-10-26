#!/usr/bin/env python3
"""Read-only Higgsfield auth check + Soul 2 cost quote. Generates nothing.

The platform API has no credit-balance endpoint (probed 2026-10-26: /credits, /balance, /wallet,
/account, /me ... all 404/405 on platform.* and api.*, GET and POST; the official SDK has none
either). The API balance is visible only in the console (cloud.higgsfield.ai / open.higgsfield.ai
Billing); an empty balance surfaces as 403 not_enough_credits on submit.
"""
import json, sys, time, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hf_auth import BASE, headers

SIENNA = "ba97f512-0ed0-4c56-9480-5abe167b06d1"  # approved baseline soul (HIGGSFIELD_EXPERT_GUIDE)


def call(method, path, body=None, h=None):
    req = urllib.request.Request(BASE + path, method=method, headers=h,
                                 data=None if body is None else json.dumps(body).encode())
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(500).decode("utf-8", "replace")


def authed_headers():
    """hf-api-key/hf-secret; on 401 wait 60s once (Sam may be saving a regenerated key) and retry."""
    for attempt in range(2):
        h = headers()
        s, _ = call("GET", "/models?page=1&page_size=1", h=h)
        if s != 401:
            return h, s
        if attempt == 0:
            print("AUTH 401 - waiting 60s for a possibly just-saved key, then retrying", flush=True)
            time.sleep(60)
    return h, s


if __name__ == "__main__":
    h, s = authed_headers()
    print("AUTH", "OK" if s == 200 else f"FAILED HTTP {s}")
    if s != 200:
        sys.exit(1)
    print("BALANCE n/a via API (no endpoint) - check the Higgsfield console Billing page")
    s, t = call("POST", "/estimate/higgsfield-ai/soul/v2/standard",
                {"prompt": "portrait", "soul_id": SIENNA, "aspect_ratio": "3:4", "quality": "2k"}, h)
    print("ESTIMATE soul/v2/standard 2k:", s, t)
