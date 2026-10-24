# Higgsfield REST proof (JSW AI)

- Date: 2026-08-26 (America/Detroit)
- Working base URL: `https://platform.higgsfield.ai` (official SDK default). `https://api.higgsfield.ai` accepts the same auth and the same Soul 2 path.
- Working auth style: `Authorization: Key ${HF_API_KEY}:${HF_SECRET}`
- Legacy auth also works: headers `hf-api-key` + `hf-secret`
- User-Agent required: requests without a UA get Cloudflare 1010. Official SDK UA `higgsfield-client-py/1.0` works.
- Secrets were not written to this file.

## Soul 2 (stills with soul_id) — CONFIRMED

- Path: `POST /higgsfield-ai/soul/v2/standard`
- Full URL: `https://platform.higgsfield.ai/higgsfield-ai/soul/v2/standard`
- Empty body → HTTP 422, `prompt` required
- Estimate: `POST /estimate/higgsfield-ai/soul/v2/standard` → HTTP 200 `{credits: "0.150", usd: "0.010"}` for quality `2k` / default
- Status poll: `GET /requests/{request_id}/status`
- Cancel: `POST /requests/{request_id}/cancel`

### Body fields (live-validated)

| field | required | notes |
|---|---|---|
| `prompt` | yes | 422 if missing |
| `soul_id` | no (needed for identity) | accepted; alias `custom_reference_id` also accepted |
| `custom_reference_id` | no | alias of soul id |
| `custom_reference_strength` | no | estimate 200 when sent |
| `aspect_ratio` | no | **not 4:5**. Allowed: `9:16`, `16:9`, `4:3`, `3:4`, `1:1`, `2:3`, `3:2`. Closest to 4:5 is `3:4`. Sending `4:5` → HTTP 400 |
| `quality` | no | CLI/REST: `1.5k` or `2k` (estimate 0.150) |
| `resolution` | no | sending `1080p` raised estimate to 0.750 credits |
| `batch_size` / `num_images` | no | estimate 200; keep 1 to avoid extra credits |

Related older path (do not use for Soul 2): `POST /higgsfield-ai/soul/character` requires `custom_reference_id`, estimate 1.500 credits.

## Seedance 2.0 (video) — mapped, not generated

Official catalog (`docs.higgsfield.ai/docs/llms-full.txt` / models catalog):

- `POST /bytedance/seedance-2.0/text-to-video` (default)
- `POST /bytedance/seedance-2.0/fast/text-to-video`
- `POST /bytedance/seedance-2.0/mini/text-to-video`

Also probed (same family, not in the short catalog table):

- `POST /bytedance/seedance-2.0/image-to-video`
- `POST /bytedance/seedance-2.0/reference-to-video`

### Live status on this API key (no video was generated)

| path | estimate/schema HTTP | detail |
|---|---|---|
| `/bytedance/seedance-2.0/text-to-video` | 503 | `model_disabled` |
| `/bytedance/seedance-2.0/image-to-video` | 503 | `model_disabled` |
| `/bytedance/seedance-2.0/reference-to-video` | 503 | `model_disabled` |
| `/bytedance/seedance-2.0/fast/text-to-video` | 423 | `model_blocked` |
| `/bytedance/seedance-2.0/mini/text-to-video` | 423 | `model_blocked` |

Paths exist (not 404). This account cannot run Seedance 2.0 right now. Seedance v1 OpenAPI paths like `/bytedance/seedance/v1/pro/text-to-video` returned 404 `model_not_found`.

### Body fields (from official CLI `seedance_2_0` + REST catalog; not fully schema-echoed because the model is disabled)

| field | required | notes |
|---|---|---|
| `prompt` | yes | |
| `generate_audio` | no | bool, CLI default `true` |
| `duration` | no | int, CLI default `5` (range ~4–15s) |
| `aspect_ratio` | no | `auto`, `16:9`, `9:16`, `4:3`, `3:4`, `1:1`, `21:9` |
| `audio_references` | no | 0..3; CLI requires at least one image/video/start/end if audio refs are set |
| `image_references` | no | repeated; at most 9 including start/end |
| `start_image` / `end_image` | no | single |
| `video_references` | no | 0..3 |
| `resolution` | no | `480p`, `720p`, `1080p`, `4k`; fast mode only 480p/720p |
| `mode` | no | `std` \| `fast` |
| `bitrate_mode` | no | `standard` \| `high` |
| `genre` | no | `auto`, `action`, `horror`, `comedy`, `noir`, `drama`, `epic` |

Total refs cap: 12 across images + videos + audios.

## List souls / reference-elements

- Working list endpoint: `GET /v1/custom-references/list?page=1&page_size=50`
- Response on this API key: HTTP 200 `{"total":0,"page":1,"page_size":50,"total_pages":0,"items":[]}`
- Other guessed paths (`/soul-ids`, `/reference-elements`, `/v1/characters`, …) returned HTTP 405
- Soul 2 IDs for this project were **not** returned by REST list (likely trained in the Higgsfield app/CLI account, not as legacy custom-references). Known IDs (not deleted):

  - charlotte `9a55147c-01b7-4160-9767-5c77077259d9`
  - camille `01d09bd2-7160-49aa-8540-b3f5d89d803c`
  - valentina `fa97f078-550a-4126-9a79-7ed4dc027139`
  - gabriela `f4d6ae5e-9b8a-4d0c-94f5-4bf7dc3bcf79`
  - madison `b6bfeec5-7d03-498d-b057-8d2a4a440635`
  - sienna `f9700355-bf71-4d6f-bec5-e87142075794`

## Test generation (Sienna only)

- Endpoint confirmed, so one still was attempted.
- `POST /higgsfield-ai/soul/v2/standard` body: `prompt`, `soul_id` (sienna), `aspect_ratio: 3:4` (4:5 rejected), `quality: 2k`
- Job id: none (request never queued)
- Final status: HTTP **403** `{"detail":"not_enough_credits"}` on both `platform.higgsfield.ai` and `api.higgsfield.ai`
- Retries without quality and with `quality: 1.5k` also 403 `not_enough_credits` (estimate still 0.150 credits)
- Local image: none — no file written to `/workspace/hf-test/sienna_soul2_test.jpg`
- No video was generated. No Camille / Valentina / Gabriela jobs.

## Errors / status codes

- Missing User-Agent → Cloudflare HTTP 403 error 1010
- Dummy `GET /requests/00000000-0000-4000-8000-000000000000/status` + valid Key auth → HTTP 404 `{"detail":"Not found"}` (auth OK)
- Invalid credentials would be HTTP 401 (not observed)
- Soul 2 `aspect_ratio: "4:5"` → HTTP 400, allowed enum listed above
- Soul 2 empty POST → HTTP 422 missing `prompt`
- Soul 2 generate → HTTP 403 `not_enough_credits`
- Seedance 2.0 std/image/reference → HTTP 503 `model_disabled`
- Seedance 2.0 fast/mini → HTTP 423 `model_blocked`
- Upload URL works: `POST /files/generate-upload-url` HTTP 200 (not used for the still)
