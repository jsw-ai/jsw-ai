#!/usr/bin/env python3
"""Ayrshare posting path for JSW (X/Twitter per Sam 2026-10-24: X posts via Ayrshare + Sam's X
developer app, not a phone login). Same gate as geelark.py: Reviewer PASS (abs path + md5 + caption
+ transition), caption lint, live ledger dedupe, dry-run unless --live AND /etc/jsw/GO_LIVE.

Hard Rules s8: Sienna is the Ayrshare Default profile (no Profile-Key header); other models need their
Profile-Key, read from 1Password item "JSW - <Model> - Ayrshare profile key" (credential field).
Hard Rules s6/s7: never put a link in an API post (each costs $0.20) - write "link in bio".
X topless only when marked sensitive: PASS may set "x_sensitive": true -> twitterOptions.possiblySensitive.

usage: ayrshare.py accounts                       linked platforms per profile (read-only)
       ayrshare.py post PASS.json x [--at UNIX_TS] [--live]
       ayrshare.py status MODEL POST_ID
"""
import json, os, subprocess, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import geelark as g

API = "https://api.ayrshare.com/api"
KEY_REF = "op://JSW/2gcfiokem5fs7eytutg4b2mgf4/credential"
NAMES = {"sienna": "Sienna", "charlotte": "Charlotte Hayes", "madison": "Madison Cole",
         "gabriela": "Gabriela Santos", "camille": "Camille Dubois", "valentina": "Valentina Reyes"}
AYR_PLATFORM = {"x": "twitter"}  # only X is routed here for now


def _op(ref):
    env = dict(os.environ)
    for line in g.OP_ENV.read_text().splitlines():
        k, _, v = line.partition("=")
        if k.strip():
            env[k.strip()] = v.strip()
    return subprocess.check_output(["op", "read", ref], env=env, stderr=subprocess.DEVNULL).decode().strip()


def headers(model):
    h = {"Authorization": f"Bearer {_op(KEY_REF)}", "Content-Type": "application/json"}
    if model != "sienna":
        try:
            h["Profile-Key"] = _op(f"op://JSW/JSW - {model.capitalize()} - Ayrshare profile key/credential")
        except subprocess.CalledProcessError:
            raise g.GateError(f"no Ayrshare Profile-Key for {model} in the JSW vault "
                              f"(expected item 'JSW - {model.capitalize()} - Ayrshare profile key')")
    return h


def call(method, path, model, body=None, h=None):
    req = urllib.request.Request(API + path, method=method, headers=h or headers(model),
                                 data=None if body is None else json.dumps(body).encode())
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Ayrshare {method} {path} HTTP {e.code}: {e.read(400).decode('utf-8', 'replace')}")


def linked():
    """{model: [ayrshare platforms]} from /user (Sienna, default profile) and /profiles (others)."""
    h = {"Authorization": f"Bearer {_op(KEY_REF)}"}
    out = {"sienna": call("GET", "/user", "sienna", h=h).get("activeSocialAccounts") or []}
    titles = {v: k for k, v in NAMES.items()}
    for p in call("GET", "/profiles", "sienna", h=h).get("profiles", []):
        if p.get("title") in titles:
            out[titles[p["title"]]] = p.get("activeSocialAccounts") or []
    return out


def post(pass_path, platform, at=None, live=False):
    if platform not in AYR_PLATFORM:
        raise g.GateError(f"{platform} is not routed through Ayrshare")
    p = json.loads(Path(pass_path).read_text())
    digest, plat = g.check_pass(p, platform)
    model, ayr = p["model"], AYR_PLATFORM[platform]
    if ayr not in linked().get(model, []):
        raise g.GateError(f"{model} has no {ayr} account linked in Ayrshare - skip")
    prior = g.ledger_find(model, platform, digest)
    if prior:
        raise g.GateError(f"already submitted live: {prior.get('postId')} at {prior.get('ts')} - check "
                          "`status` before any resubmit")
    h = headers(model)  # fails here (dry-run too) if the model's Profile-Key is missing
    # Ayrshare rejects past schedule dates; never earlier than 2 min from now.
    when = datetime.fromtimestamp(max(int(at or 0), int(time.time())) + 120, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    body = {"post": plat["caption"], "platforms": [ayr], "mediaUrls": ["<ayrshare-upload-url>"],
            "isVideo": True, "scheduleDate": when, "shortenLinks": False}
    if p.get("x_sensitive"):
        body["twitterOptions"] = {"possiblySensitive": True}
    if not (live and g.GO_LIVE.exists()):
        print("DRY-RUN (nothing uploaded, nothing posted)" +
              ("" if not live else " - --live given but /etc/jsw/GO_LIVE is absent"))
        print("POST /post", "(Profile-Key: none, Sienna default)" if model == "sienna" else "(Profile-Key: from vault)")
        print(json.dumps(body, indent=1, ensure_ascii=False))
        return None
    name = Path(p["file"]).name
    u = call("GET", f"/media/uploadUrl?fileName={urllib.request.quote(name)}&contentType=mp4", model, h=h)
    with open(p["file"], "rb") as f:
        urllib.request.urlopen(urllib.request.Request(u["uploadUrl"], data=f.read(), method="PUT",
                               headers={"Content-Type": "video/mp4"}), timeout=300).read()
    body["mediaUrls"] = [u["accessUrl"]]
    r = call("POST", "/post", model, body, h=h)
    g.ledger_add({"ts": int(time.time()), "model": model, "platform": platform, "md5": digest,
                  "file": p["file"], "live": True, "backend": "ayrshare", "postId": r.get("id"),
                  "scheduleDate": when})
    print("SUBMITTED", platform, model, r.get("status"), r.get("id"), r.get("errors") or "")
    return r.get("id")


def main(a):
    if len(a) < 2 or a[1] not in ("accounts", "post", "status"):
        print(__doc__); return 2
    try:
        if a[1] == "accounts":
            for m, pl in linked().items():
                print(m.ljust(10), sorted(pl))
        elif a[1] == "status":
            print(json.dumps(call("GET", f"/post/{a[3]}", a[2]), indent=1)[:2000])
        else:
            at = int(a[a.index("--at") + 1]) if "--at" in a else None
            post(a[2], a[3], at=at, live="--live" in a)
    except g.GateError as e:
        print("BLOCKED:", e); return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
