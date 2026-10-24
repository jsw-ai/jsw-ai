#!/usr/bin/env python3
"""GeeLark posting client for JSW (replaces Ayrshare + AdsPower).

Dry-run by default. A live submit needs BOTH `--live` and the file /etc/jsw/GO_LIVE, which is created
only after Sam explicitly says "go live". Dry-run validates everything and prints the request it would
send, but uploads nothing and calls no write endpoint.

Gate (Hard Rules s1, Scheduler SOP): nothing posts without a JSW Content Reviewer PASS for the exact
file path + md5 + caption + platform. The PASS is passed in as JSON:
  {"model": "sienna", "file": "/abs/path.mp4", "md5": "...", "transition": "hair flip",
   "platforms": {"tiktok": {"caption": "..."}, "youtube": {"caption": "...", "title": "..."},
                 "reddit": {"caption": "...", "title": "...", "community": "..."}}}

Docs: github.com/GeeLark/geelark-openapi (docs/en, read 2026-10-24 at commit 4abb551).
Auth: Bearer token = op://JSW/7h4mzmkqm5dyfefguroh6tjbr4/password, plus a traceId header per request.

usage: geelark.py phones
       geelark.py post PASS.json PLATFORM [--at UNIX_TS] [--live]
       geelark.py status TASK_ID [TASK_ID ...]
"""
import hashlib, json, os, re, subprocess, sys, time, urllib.error, urllib.request, uuid
from pathlib import Path

BASE = "https://openapi.geelark.com"
OP_ENV = Path("/etc/jsw/op.env")
GO_LIVE = Path("/etc/jsw/GO_LIVE")
PHONES = Path(__file__).with_name("phones.json")
LEDGER = Path("/opt/jsw-data/geelark_ledger.jsonl")
MAX_BYTES = 15 * 1024 * 1024
MODELS = ("sienna", "charlotte", "madison", "gabriela", "camille", "valentina")

# Per-platform: endpoint, caption limit, whether a title is needed. AI label is always on where the
# API exposes one (TikTok markAI, IG aiTag, YouTube isDisclosureMandatory). X/FB/Reddit RPA tasks have
# no AI-label field - see NO_AI_FLAG.
PLATFORMS = {
    "tiktok":    {"path": "/open/v1/task/add",               "cap": 4000},
    "instagram": {"path": "/open/v1/rpa/task/instagramPubReels", "cap": 2200},
    "youtube":   {"path": "/open/v1/rpa/task/youtubePubShort",   "cap": 5000, "title": 100},
    "facebook":  {"path": "/open/v1/rpa/task/faceBookPubReels",  "cap": 500},
    "x":         {"path": "/open/v1/rpa/task/xPublish",          "cap": 280},
    "reddit":    {"path": "/open/v1/rpa/task/redditVideo",       "cap": 40000, "title": 300},
}
NO_AI_FLAG = {"facebook", "x", "reddit"}
FUNNEL_OK = {"x", "reddit"}  # Hard Rules s6: Fanvue funneling only from X and Reddit


class GateError(Exception):
    pass


def _token():
    env = dict(os.environ)
    for line in OP_ENV.read_text().splitlines():
        k, _, v = line.partition("=")
        if k.strip():
            env[k.strip()] = v.strip()
    return subprocess.check_output(["op", "read", "op://JSW/7h4mzmkqm5dyfefguroh6tjbr4/password"],
                                   env=env).decode().strip()


# Read-only endpoints may be retried on 40007 (rate limit, lifts within a minute). Writes are never
# retried here: verify state first, then resubmit by hand.
READ_ONLY = {"/open/v1/phone/list", "/open/v1/task/query", "/open/v1/pay/plan/info", "/open/v1/pay/wallet",
             "/open/v1/app/installable/list", "/open/v1/app/list", "/open/v1/app/teamApp/list",
             "/open/v1/group/list", "/open/v1/proxy/list"}


def call(path, body, token=None):
    token = token or _token()
    for attempt in range(4 if path in READ_ONLY else 1):
        req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(), method="POST", headers={
            "Content-Type": "application/json", "traceId": uuid.uuid4().hex, "Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                j = json.loads(r.read())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"HTTP {e.code} {path}: {e.read(300).decode('utf-8', 'replace')}")
        if j.get("code") == 40007 and path in READ_ONLY:
            time.sleep(20 * (attempt + 1))
            continue
        if j.get("code") != 0:
            raise RuntimeError(f"GeeLark {path} code={j.get('code')} msg={j.get('msg')}")
        return j.get("data")
    raise RuntimeError(f"GeeLark {path} still rate-limited (40007)")


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def phone_for(model):
    phones = json.loads(PHONES.read_text())
    pid = (phones.get(model) or {}).get("envId")
    if not pid:
        raise GateError(f"no GeeLark phone mapped for {model} in {PHONES}")
    return pid


def lint_caption(platform, text):
    """Defense in depth only; the Reviewer is the gate. Hard Rules s6/s9."""
    problems = []
    # "AI" case-sensitive: Portuguese/Spanish "ai" is an interjection (Gabriela, Valentina).
    if re.search(r"\bA\.?I\b", text) or re.search(r"artificial intelligence|\bai[- ]generated", text, re.I):
        problems.append("mentions AI (Hard Rules s9: never in captions)")
    if re.search(r"https?://|www\.", text, re.I):
        problems.append("contains a URL (links go in the bio / hand-pinned post only)")
    if platform not in FUNNEL_OK and re.search(r"fanvue|link in bio", text, re.I):
        problems.append(f"Fanvue/link-in-bio on {platform} (clean brand account)")
    lim = PLATFORMS[platform]["cap"]
    if len(text) > lim:
        problems.append(f"caption {len(text)} chars > {platform} limit {lim}")
    return problems


def check_pass(p, platform):
    """Verify the Reviewer PASS against the file on disk. Raises GateError on any mismatch."""
    if platform not in PLATFORMS:
        raise GateError(f"unknown platform {platform}")
    if p.get("model") not in MODELS:
        raise GateError(f"unknown model {p.get('model')!r}")
    f = Path(p.get("file", ""))
    if not f.is_absolute() or not f.is_file():
        raise GateError(f"PASS file missing or not absolute: {f}")
    if f.suffix.lower() != ".mp4":
        raise GateError("only .mp4 video posts are wired so far")
    if f.stat().st_size > MAX_BYTES:
        raise GateError(f"{f.name} is {f.stat().st_size} bytes > 15 MB (Hard Rules s4)")
    got = md5(f)
    if got != p.get("md5"):
        raise GateError(f"md5 mismatch: file {got} != PASS {p.get('md5')} - back to the Reviewer")
    if not p.get("transition"):
        raise GateError("PASS names no transition (Hard Rules s5)")
    plat = (p.get("platforms") or {}).get(platform)
    if not plat or not plat.get("caption"):
        raise GateError(f"PASS does not cover {platform} with a caption")
    if PLATFORMS[platform].get("title") and not plat.get("title"):
        raise GateError(f"{platform} needs a title in the PASS")
    if platform == "reddit" and not plat.get("community"):
        raise GateError("reddit needs a community in the PASS")
    problems = lint_caption(platform, plat["caption"])
    if problems:
        raise GateError("; ".join(problems))
    return got, plat


def build_body(platform, env_id, video_url, plat, at):
    cap = plat["caption"]
    if platform == "tiktok":
        # maxTryTimes 0: a timed-out task can still have posted (failCode 20003), so we verify by hand
        # before any retry instead of letting GeeLark retry blind.
        return {"taskType": 1, "list": [{"scheduleAt": at, "envId": env_id, "video": video_url,
                "videoDesc": cap, "markAI": True, "maxTryTimes": 0, "needShareLink": True}]}
    body = {"scheduleAt": at, "id": env_id, "description": cap}
    if platform == "instagram":
        body.update(video=[video_url], aiTag=True, needShareLink=True)
    elif platform == "youtube":
        body = {"scheduleAt": at, "id": env_id, "title": plat["title"], "video": video_url,
                "sameStyleVoice": 0, "originalVoice": 0, "isDisclosureMandatory": True}
    elif platform == "facebook":
        body.update(video=video_url)
    elif platform == "x":
        body.update(video=[video_url])
    elif platform == "reddit":
        body.update(title=plat["title"], video=[video_url], community=plat["community"])
    return body


def ledger_find(model, platform, digest):
    if not LEDGER.exists():
        return None
    hit = None
    for line in LEDGER.read_text().splitlines():
        r = json.loads(line)
        if (r["model"], r["platform"], r["md5"]) == (model, platform, digest) and r.get("live"):
            hit = r
    return hit


def ledger_add(rec):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(json.dumps(rec) + "\n")


def upload(path, token):
    d = call("/open/v1/upload/getUrl", {"fileType": "mp4"}, token)
    with open(path, "rb") as f:
        req = urllib.request.Request(d["uploadUrl"], data=f.read(), method="PUT")
        urllib.request.urlopen(req, timeout=300).read()
    return d["resourceUrl"]


def post(pass_path, platform, at=None, live=False):
    p = json.loads(Path(pass_path).read_text())
    digest, plat = check_pass(p, platform)
    model = p["model"]
    env_id = phone_for(model)
    at = int(at or time.time())
    prior = ledger_find(model, platform, digest)
    if prior:
        raise GateError(f"already submitted live: task {prior.get('taskId')} at {prior.get('ts')} - "
                        "check it with `status` before any resubmit")
    if platform in NO_AI_FLAG:
        print(f"NOTE: {platform} RPA has no AI-label field; the account-level AI label must be on.")
    if not (live and GO_LIVE.exists()):
        body = build_body(platform, env_id, "<geelark-upload-url>", plat, at)
        print("DRY-RUN (nothing uploaded, nothing submitted)" +
              ("" if not live else " - --live given but /etc/jsw/GO_LIVE is absent"))
        print("POST", PLATFORMS[platform]["path"]); print(json.dumps(body, indent=1, ensure_ascii=False))
        return None
    token = _token()
    url = upload(p["file"], token)
    data = call(PLATFORMS[platform]["path"], build_body(platform, env_id, url, plat, at), token)
    task_id = (data.get("taskIds") or [None])[0] if platform == "tiktok" else data.get("taskId")
    ledger_add({"ts": int(time.time()), "model": model, "platform": platform, "md5": digest,
                "file": p["file"], "live": True, "taskId": task_id, "scheduleAt": at})
    print("SUBMITTED", platform, model, "task", task_id)
    return task_id


STATUS = {1: "waiting", 2: "in progress", 3: "completed", 4: "failed", 7: "cancelled"}


def status(ids):
    for t in call("/open/v1/task/query", {"ids": list(ids)}).get("items", []):
        print(t["id"], t.get("serialName"), STATUS.get(t.get("status"), t.get("status")),
              t.get("failCode") or "", t.get("failDesc") or "", t.get("shareLink") or "")


def phones():
    d = call("/open/v1/phone/list", {"page": 1, "pageSize": 100})
    print("total", d.get("total"))
    for i in d.get("items", []):
        px = i.get("proxy") or {}
        print(i["id"], "|", i.get("serialName"), "| status", i.get("status"), "|",
              (i.get("equipmentInfo") or {}).get("countryName"), "| proxy",
              f"{px.get('type')}://{px.get('server')}:{px.get('port')}" if px.get("server") else "none")


def main(argv):
    if len(argv) < 2 or argv[1] not in ("phones", "post", "status"):
        print(__doc__); return 2
    try:
        if argv[1] == "phones":
            phones()
        elif argv[1] == "status":
            status(argv[2:])
        else:
            at = int(argv[argv.index("--at") + 1]) if "--at" in argv else None
            post(argv[2], argv[3], at=at, live="--live" in argv)
    except GateError as e:
        print("BLOCKED:", e); return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
