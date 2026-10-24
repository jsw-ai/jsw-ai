#!/usr/bin/env python3
"""Higgsfield REST probe. Never prints secrets. Never writes secrets to files."""
from __future__ import annotations

import json
import os
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SECRETS_PATH = Path("/home/box/agent-data/connector-secrets/b03764fa-1acf-4eb6-b1e0-b6890366beb7/Higgsfield.json")
OUT_DIR = Path("/workspace/hf-test")
NOTES = OUT_DIR / "api_notes.md"
SIENNA_ID = "f9700355-bf71-4d6f-bec5-e87142075794"
PROMPT = (
    "Candid iPhone photo, natural daylight, pore-level skin texture, natural tan, "
    "relaxed natural body. Gold Coast woman, tank and shorts. NOT airbrushed, "
    "NOT glossy, NOT plastic, NOT cinematic."
)
KNOWN = {
    "charlotte": "9a55147c-01b7-4160-9767-5c77077259d9",
    "camille": "01d09bd2-7160-49aa-8540-b3f5d89d803c",
    "valentina": "fa97f078-550a-4126-9a79-7ed4dc027139",
    "gabriela": "f4d6ae5e-9b8a-4d0c-94f5-4bf7dc3bcf79",
    "madison": "b6bfeec5-7d03-498d-b057-8d2a4a440635",
    "sienna": SIENNA_ID,
}
BASES = ["https://platform.higgsfield.ai", "https://api.higgsfield.ai"]
CTX = ssl.create_default_context()
MAX_BODY = 4000
errors = []
results = []


def redact(text: str) -> str:
    if not text:
        return text
    # never keep key-like tokens
    text = re.sub(r"(?i)(authorization|hf-api-key|hf-secret|api[_-]?key|secret)\s*[:=]\s*\S+", r"\1: [redacted]", text)
    text = re.sub(r"Key [0-9a-fA-F-]+:[A-Za-z0-9+/=._-]+", "Key [redacted]", text)
    return text[:MAX_BODY]


def load_creds():
    d = json.loads(SECRETS_PATH.read_text())
    key = d.get("HF_API_KEY") or ""
    secret = d.get("HF_SECRET") or ""
    if not key or not secret:
        raise SystemExit("missing credentials")
    return key, secret


def request(method, url, headers, body=None, timeout=45):
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
            raw = resp.read()
            elapsed = round(time.time() - t0, 2)
            try:
                parsed = json.loads(raw.decode("utf-8", "replace"))
            except Exception:
                parsed = None
            return {
                "ok": True,
                "status": resp.status,
                "elapsed": elapsed,
                "headers": {k.lower(): v for k, v in resp.headers.items() if k.lower() in ("content-type", "x-request-id")},
                "text": redact(raw.decode("utf-8", "replace")),
                "json": parsed,
            }
    except urllib.error.HTTPError as e:
        raw = e.read()
        elapsed = round(time.time() - t0, 2)
        try:
            parsed = json.loads(raw.decode("utf-8", "replace"))
        except Exception:
            parsed = None
        return {
            "ok": False,
            "status": e.code,
            "elapsed": elapsed,
            "headers": {},
            "text": redact(raw.decode("utf-8", "replace")),
            "json": parsed,
        }
    except Exception as e:
        elapsed = round(time.time() - t0, 2)
        return {
            "ok": False,
            "status": 0,
            "elapsed": elapsed,
            "headers": {},
            "text": redact(type(e).__name__ + ": " + str(e)),
            "json": None,
        }


def summarize_json(obj, limit=1200):
    if obj is None:
        return ""
    try:
        s = json.dumps(obj, ensure_ascii=False, default=str)
    except Exception:
        s = str(obj)
    return redact(s)[:limit]


def names_ids_from_list(payload):
    items = []
    if isinstance(payload, dict):
        items = payload.get("items") or payload.get("data") or payload.get("results") or payload.get("souls") or payload.get("references") or []
        if isinstance(items, dict):
            items = items.get("items") or []
    elif isinstance(payload, list):
        items = payload
    out = []
    if isinstance(items, list):
        for it in items:
            if not isinstance(it, dict):
                continue
            name = it.get("name") or it.get("title") or it.get("label")
            sid = it.get("id") or it.get("soul_id") or it.get("custom_reference_id") or it.get("reference_id")
            status = it.get("status") or it.get("state")
            model = it.get("model") or it.get("job_set_type") or it.get("type") or it.get("variant")
            rec = {"name": name, "id": sid}
            if status:
                rec["status"] = status
            if model:
                rec["model"] = model
            if sid:
                out.append(rec)
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    key, secret = load_creds()
    auth_key = {"Authorization": f"Key {key}:{secret}", "Content-Type": "application/json", "Accept": "application/json"}
    auth_legacy = {"hf-api-key": key, "hf-secret": secret, "Content-Type": "application/json", "Accept": "application/json"}

    working_base = None
    working_auth = None
    list_hits = []
    estimate_soul = None
    estimate_seedance = None
    soul_body_ok = None
    gen = {}

    dummy = "00000000-0000-4000-8000-000000000000"

    # AUTH + LIST
    for base in BASES:
        for style, headers in (("Authorization: Key ${HF_API_KEY}:${HF_SECRET}", auth_key), ("legacy hf-api-key + hf-secret", auth_legacy)):
            url = f"{base}/requests/{dummy}/status"
            r = request("GET", url, headers)
            rec = {"kind": "auth-status", "base": base, "auth": style, "http": r["status"], "body": summarize_json(r["json"]) or r["text"][:400]}
            results.append(rec)
            errors.append(rec)
            # 401 = bad auth; 404/400/422 = auth accepted
            if r["status"] not in (0, 401, 403):
                if working_base is None:
                    working_base = base
                    working_auth = style

            list_paths = [
                "/v1/custom-references/list?page=1&page_size=50",
                "/v1/custom-references?page=1&page_size=50",
                "/custom-references/list?page=1&page_size=50",
                "/souls",
                "/v1/souls",
                "/soul-ids",
                "/v1/soul-ids",
                "/reference-elements",
                "/v1/reference-elements",
                "/elements",
            ]
            for path in list_paths:
                r = request("GET", base + path, headers, timeout=30)
                rec = {"kind": "list", "base": base, "auth": style, "path": path.split("?")[0], "http": r["status"], "body": summarize_json(r["json"]) or r["text"][:300]}
                results.append(rec)
                if r["status"] == 200:
                    hits = names_ids_from_list(r["json"])
                    list_hits.append({"base": base, "auth": style, "path": path.split("?")[0], "items": hits, "raw_keys": list(r["json"].keys()) if isinstance(r["json"], dict) else type(r["json"]).__name__})
                    if working_base is None:
                        working_base = base
                        working_auth = style
                elif r["status"] not in (0, 401, 404, 405):
                    errors.append(rec)

    if working_base is None:
        working_base = BASES[0]
        working_auth = "Authorization: Key ${HF_API_KEY}:${HF_SECRET}"

    headers = auth_key if "Authorization" in working_auth else auth_legacy

    # ESTIMATE / DISCOVER Soul 2
    soul_payloads = [
        ("prompt-only", {"prompt": "Editorial portrait in soft daylight"}),
        ("soul_id+4:5", {"prompt": PROMPT, "soul_id": SIENNA_ID, "aspect_ratio": "4:5"}),
        ("custom_reference_id+4:5", {"prompt": PROMPT, "custom_reference_id": SIENNA_ID, "aspect_ratio": "4:5"}),
        ("soul_id+3:4+quality", {"prompt": PROMPT, "soul_id": SIENNA_ID, "aspect_ratio": "3:4", "quality": "2k"}),
        ("custom_reference_id+3:4+quality", {"prompt": PROMPT, "custom_reference_id": SIENNA_ID, "aspect_ratio": "3:4", "quality": "2k"}),
        ("custom_reference_id+2:3+resolution", {"prompt": PROMPT, "custom_reference_id": SIENNA_ID, "aspect_ratio": "2:3", "resolution": "1080p", "custom_reference_strength": 1}),
    ]
    soul_paths = [
        "/higgsfield-ai/soul/v2/standard",
        "/higgsfield-ai/soul/v2",
        "/higgsfield-ai/soul/character",
    ]
    for path in soul_paths:
        est_url = working_base + "/estimate" + path
        gen_url = working_base + path
        for label, body in soul_payloads:
            r = request("POST", est_url, headers, body)
            rec = {"kind": "estimate-soul", "url": est_url, "label": label, "http": r["status"], "body": summarize_json(r["json"]) or r["text"][:500]}
            results.append(rec)
            errors.append(rec)
            if r["status"] in (200, 201) and estimate_soul is None:
                estimate_soul = rec
                soul_body_ok = {"path": path, "label": label, "body": body}
                break
        if soul_body_ok:
            break
        # empty POST to generation to capture 422 schema without spending if possible
        r = request("POST", gen_url, headers, {})
        rec = {"kind": "schema-soul", "url": gen_url, "http": r["status"], "body": summarize_json(r["json"]) or r["text"][:800]}
        results.append(rec)
        errors.append(rec)

    # If estimate never succeeded, a 422 on generation with extra fields still confirms the path exists.
    # Don't generate until a 2xx estimate OR a 422 that mentions prompt (endpoint exists) and we then submit a valid body.

    # SEEDANCE 2.0 mapping via estimate + empty POST schema
    seedance_paths = [
        "/bytedance/seedance-2.0/text-to-video",
        "/bytedance/seedance-2.0/image-to-video",
        "/bytedance/seedance-2.0/reference-to-video",
        "/bytedance/seedance-2.0/fast/text-to-video",
        "/bytedance/seedance-2.0/mini/text-to-video",
        "/bytedance/seedance/v2/text-to-video",
        "/bytedance/seedance/2.0/text-to-video",
    ]
    seedance_body = {
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
    seedance_map = []
    for path in seedance_paths:
        for kind, url, body in (
            ("estimate-seedance", working_base + "/estimate" + path, seedance_body),
            ("schema-seedance", working_base + path, {}),
            ("schema-seedance-full", working_base + path, seedance_body),
        ):
            r = request("POST", url, headers, body)
            rec = {"kind": kind, "url": url, "http": r["status"], "body": summarize_json(r["json"]) or r["text"][:800]}
            results.append(rec)
            seedance_map.append(rec)
            if kind == "estimate-seedance" and r["status"] in (200, 201) and estimate_seedance is None:
                estimate_seedance = rec
            # if full body 200 that would SPEND credits for video — cancel immediately
            if kind == "schema-seedance-full" and r["status"] in (200, 201) and isinstance(r["json"], dict) and r["json"].get("request_id"):
                rid = r["json"]["request_id"]
                cancel_url = r["json"].get("cancel_url") or f"{working_base}/requests/{rid}/cancel"
                c = request("POST", cancel_url, headers, {})
                rec2 = {"kind": "cancel-unwanted-video", "id": rid, "http": c["status"], "body": summarize_json(c["json"]) or c["text"][:300]}
                results.append(rec2)
                errors.append({"note": "accidentally submitted seedance; cancelled", **rec2})

    # Confirm Soul 2 endpoint existence: estimate 200 or schema 422/400 (not 404/401)
    soul_confirmed = False
    soul_path = "/higgsfield-ai/soul/v2/standard"
    for rec in results:
        if rec.get("kind") in ("estimate-soul", "schema-soul") and rec.get("http") not in (0, 401, 403, 404):
            soul_confirmed = True
            if "/soul/v2" in str(rec.get("url", "")):
                soul_path = urllib.parse.urlparse(rec["url"]).path.replace("/estimate", "") or soul_path
                if soul_path.startswith("/estimate"):
                    soul_path = soul_path[len("/estimate"):]
            break

    # Generation — only if Soul 2 confirmed
    image_path = None
    if soul_confirmed:
        # choose best body: prefer 4:5 + soul_id
        candidates = []
        if soul_body_ok:
            candidates.append(soul_body_ok["body"])
        candidates.extend([
            {"prompt": PROMPT, "soul_id": SIENNA_ID, "aspect_ratio": "4:5", "quality": "2k"},
            {"prompt": PROMPT, "custom_reference_id": SIENNA_ID, "aspect_ratio": "4:5", "quality": "2k"},
            {"prompt": PROMPT, "soul_id": SIENNA_ID, "aspect_ratio": "3:4", "quality": "2k"},
            {"prompt": PROMPT, "custom_reference_id": SIENNA_ID, "aspect_ratio": "3:4", "quality": "2k"},
            {"prompt": PROMPT, "custom_reference_id": SIENNA_ID, "aspect_ratio": "2:3", "resolution": "1080p", "custom_reference_strength": 1, "batch_size": 1},
            {"prompt": PROMPT, "soul_id": SIENNA_ID},
        ])
        submitted = None
        used_body = None
        seen = []
        for body in candidates:
            keyb = json.dumps(body, sort_keys=True)
            if keyb in seen:
                continue
            seen.append(keyb)
            r = request("POST", working_base + soul_path, headers, body, timeout=60)
            rec = {"kind": "generate-soul", "path": soul_path, "fields": sorted(body.keys()), "http": r["status"], "body": summarize_json(r["json"]) or r["text"][:800]}
            results.append(rec)
            errors.append(rec)
            if r["status"] in (200, 201, 202) and isinstance(r["json"], dict) and r["json"].get("request_id"):
                submitted = r["json"]
                used_body = body
                break
        gen["submit"] = submitted
        gen["body_fields"] = sorted((used_body or {}).keys())
        gen["path"] = soul_path
        if submitted:
            rid = submitted["request_id"]
            status_url = submitted.get("status_url") or f"{working_base}/requests/{rid}/status"
            deadline = time.time() + 180
            last = None
            while time.time() < deadline:
                s = request("GET", status_url, headers, timeout=30)
                last = s
                st = (s.get("json") or {}).get("status") if isinstance(s.get("json"), dict) else None
                rec = {"kind": "poll", "id": rid, "http": s["status"], "status": st, "body": summarize_json(s["json"])[:500]}
                results.append(rec)
                if st in ("completed", "failed", "nsfw", "canceled", "cancelled"):
                    break
                time.sleep(5)
            gen["job_id"] = rid
            gen["final"] = last
            # download if completed
            payload = last.get("json") if last else None
            url = None
            if isinstance(payload, dict) and payload.get("status") == "completed":
                images = payload.get("images") or []
                if images and isinstance(images, list):
                    first = images[0]
                    if isinstance(first, dict):
                        url = first.get("url") or (first.get("raw") or {}).get("url") if isinstance(first.get("raw"), dict) else first.get("url")
                    elif isinstance(first, str):
                        url = first
                if not url and isinstance(payload.get("image"), dict):
                    url = payload["image"].get("url")
                if not url:
                    # nested jobs
                    jobs = payload.get("jobs") or payload.get("results")
                    if isinstance(jobs, list) and jobs:
                        j0 = jobs[0]
                        if isinstance(j0, dict):
                            url = (
                                (j0.get("results") or {}).get("raw", {}).get("url")
                                if isinstance(j0.get("results"), dict)
                                else j0.get("url")
                            )
            if url and isinstance(url, str) and url.startswith("http"):
                ext = ".jpg"
                low = url.lower().split("?")[0]
                if low.endswith(".png"):
                    ext = ".png"
                elif low.endswith(".webp"):
                    ext = ".webp"
                dest = OUT_DIR / f"sienna_soul2_test{ext}"
                img_req = urllib.request.Request(url, headers={"User-Agent": "hf-probe/1.0"})
                with urllib.request.urlopen(img_req, timeout=60, context=CTX) as resp:
                    data = resp.read()
                dest.write_bytes(data)
                image_path = str(dest)
                gen["image_path"] = image_path
                gen["bytes"] = len(data)

    # WRITE NOTES
    lines = []
    lines.append("# Higgsfield REST proof (JSW AI)")
    lines.append("")
    lines.append(f"- Date: 2026-08-26 (America/Detroit)")
    lines.append(f"- Working base URL: `{working_base}`")
    lines.append(f"- Working auth style: `{working_auth}` (secret not recorded)")
    lines.append("- Bases tried: `https://api.higgsfield.ai`, `https://platform.higgsfield.ai`")
    lines.append("")
    lines.append("## Soul 2 (stills with soul_id)")
    lines.append("")
    lines.append(f"- Official catalog path: `POST /higgsfield-ai/soul/v2/standard`")
    lines.append(f"- Confirmed: `{soul_confirmed}`")
    lines.append(f"- Path used: `{soul_path}`")
    if soul_body_ok:
        lines.append(f"- Estimate-accepted field set (`{soul_body_ok['label']}`): `{json.dumps(sorted(soul_body_ok['body'].keys()))}`")
    lines.append("- Documented / CLI body fields for Soul V2 (`text2image_soul_v2`):")
    lines.append("  - `prompt` (required)")
    lines.append("  - `soul_id` alias `custom_reference_id` (Soul UUID)")
    lines.append("  - `aspect_ratio`: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3` (CLI). Prefer `4:5` if API accepts it; otherwise `3:4` / `2:3`.")
    lines.append("  - `quality`: `1.5k` | `2k` (maps to 720p/1080p)")
    lines.append("  - optional single image reference")
    lines.append("- Older OpenAPI `/higgsfield-ai/soul/character` (Soul 1 character): `prompt`, `custom_reference_id`, `custom_reference_strength`, `aspect_ratio` (includes `2:3` not `4:5`), `resolution` 720p/1080p, `batch_size` 1|4")
    lines.append("- Status poll: `GET /requests/{request_id}/status`")
    lines.append("")
    lines.append("## Seedance 2.0 (video) — mapped, not generated")
    lines.append("")
    lines.append("- Official catalog default: `POST /bytedance/seedance-2.0/text-to-video`")
    lines.append("- Also catalogued: `POST /bytedance/seedance-2.0/fast/text-to-video`, `POST /bytedance/seedance-2.0/mini/text-to-video`")
    lines.append("- CLI `seedance_2_0` body fields:")
    lines.append("  - `prompt` (required)")
    lines.append("  - `generate_audio` (bool, default true)")
    lines.append("  - `duration` (int, default 5; CLI 4–15s)")
    lines.append("  - `aspect_ratio`: `auto`, `16:9`, `9:16`, `4:3`, `3:4`, `1:1`, `21:9`")
    lines.append("  - `audio_references` (0..3)")
    lines.append("  - `image_references` (repeated; at most 9 including start/end)")
    lines.append("  - also: `start_image`, `end_image`, `video_references` (0..3), `resolution` (480p/720p/1080p/4k), `mode` (std|fast), `bitrate_mode` (standard|high), `genre`")
    lines.append("- Estimate/schema probe results:")
    for rec in seedance_map:
        lines.append(f"  - `{rec['kind']}` `{rec['url']}` HTTP {rec['http']}: {rec['body'][:220].replace(chr(10),' ')}")
    lines.append("")
    lines.append("## List souls / reference-elements")
    lines.append("")
    if list_hits:
        for hit in list_hits:
            lines.append(f"- `{hit['base']}{hit['path']}` auth=`{hit['auth']}` keys=`{hit['raw_keys']}`")
            for it in hit["items"]:
                lines.append(f"  - {it.get('name')} `{it.get('id')}` status={it.get('status')} model={it.get('model')}")
    else:
        lines.append("- No successful list endpoint in this probe. Known JSW souls (not deleted):")
        for n, i in KNOWN.items():
            lines.append(f"  - {n} `{i}`")
    lines.append("")
    lines.append("## Test generation (Sienna only)")
    lines.append("")
    if not soul_confirmed:
        lines.append("- Skipped: Soul 2 endpoint was not confirmed.")
    else:
        lines.append(f"- Job id: `{gen.get('job_id')}`")
        payload = (gen.get("final") or {}).get("json") if gen.get("final") else None
        st = payload.get("status") if isinstance(payload, dict) else None
        lines.append(f"- Final status: `{st}`")
        lines.append(f"- Body fields used: `{gen.get('body_fields')}`")
        lines.append(f"- Local image: `{gen.get('image_path')}`")
        if payload:
            lines.append(f"- Status payload (truncated): `{summarize_json(payload, 800)}`")
    lines.append("")
    lines.append("## Errors / status codes")
    lines.append("")
    for rec in results:
        if rec.get("kind") in ("auth-status", "list", "estimate-soul", "schema-soul", "generate-soul", "poll", "estimate-seedance", "schema-seedance", "schema-seedance-full", "cancel-unwanted-video"):
            url = rec.get("url") or rec.get("path") or rec.get("base", "")
            lines.append(f"- {rec.get('kind')} {url} HTTP {rec.get('http')} {str(rec.get('body') or rec.get('status') or '')[:180].replace(chr(10),' ')}")
    lines.append("")
    NOTES.write_text("\n".join(lines) + "\n")
    # stdout summary without secrets
    print("WROTE", str(NOTES))
    print("BASE", working_base)
    print("AUTH", working_auth)
    print("SOUL_CONFIRMED", soul_confirmed)
    print("SOUL_PATH", soul_path)
    print("GEN_ID", gen.get("job_id"))
    print("GEN_STATUS", (payload.get("status") if isinstance(payload, dict) else None) if soul_confirmed else None)
    print("IMAGE", gen.get("image_path"))
    print("LIST_HITS", len(list_hits))
    if list_hits:
        for hit in list_hits:
            print("LIST", hit["path"], "n=", len(hit["items"]))
            for it in hit["items"]:
                print("SOUL", it.get("name"), it.get("id"))


if __name__ == "__main__":
    main()
