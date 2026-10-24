# ZenCreator expert briefing — JSW AI

**Audience:** JSW AI pipeline (6 adult female personas). Higgsfield for SFW. ZenCreator for NSFW / Fanvue stills. Fanvue monetization.  
**Date:** 2026-08-30 (America/Detroit).  
**Constraint:** Do not generate images. Do not spend credits. Do not post.  
**Sources:** help.zencreator.pro, zencreator.pro/ai-university, mcp.zencreator.pro, api.zencreator.pro OpenAPI + SKILL.md, zencreator.pro/pricing. Marketing pages that contradict help/API are flagged.

---

## 0. JSW standing rules (source of truth)

These override generic Zen marketing copy when they conflict.

1. **Face + body slots:** If a Zen tool has separate face and body reference slots, **use both**. Photoshoot has both (`face_ref` + `body_ref`).
2. **Single-ref tools:** If a tool only takes one reference image, use a **front-facing full-body shot** or the body will be inaccurate.
3. **Photoshoot is category-driven.** Pick a theme. Do not write a custom prompt. `category_id` beats `prompt` if both are sent.
4. **Face ref** = sharp front-facing portrait, shoulders/chest-up, **not** a full-body crop.
5. **Body ref** = full/half body. For 18+, use a **headless body** so the model does not confuse faces. A clothed or headed body is the likely cause of JSW skull-shape drift.
6. **3 credits per photoshoot image.** One credit wallet across app + API + MCP.
7. **Public API `GET /photoshoot-categories` returns SFW-only presets regardless of trusted status.** NSFW categories live in the **app UI** (`app.zencreator.pro` Photoshoot, 18+ toggle).
8. **`image_editor` + `SEEDREAM_5_PRO` keeps composition** (better skull). Photoshoot **redraws poses organically** via theme templates.
9. **Trusted status** after first paid credit pack; unlocks uncensored models (`FLUX_KLEIN_NSFW`, `SDXL_NSFW`, `wan@2.7-nsfw`, etc.).
10. **Org Studio at the droplet is a raw schema form** (`category_id` is a text field, no theme grid). The real theme picker is **app.zencreator.pro → Photoshoot**.
11. **Higgsfield keepers → Zen photoshoot themes** for Fanvue stills. Editor only when a theme is not enough. Never post from Zen.

---

## 1. Mental model (app vs API vs MCP vs Org Studio)

Four surfaces, **one account, one credit wallet**. Same generation tools underneath. Different UX and different catalog visibility.

| Surface | URL | Auth | What it is | When JSW uses it |
|---|---|---|---|---|
| **App** | https://app.zencreator.pro | session login | Real product. Theme grid, Personas, 18+ toggle, Publishing, Companion. | **Default for Photoshoot NSFW.** Pick themes visually. Save persona face/body. |
| **Public API** | https://api.zencreator.pro | Bearer `zc_live_…` from app.zencreator.pro/api-keys | REST: upload asset → `POST /generations` → poll → fetch result. | Automation at scale. **Cannot list NSFW photoshoot categories.** |
| **MCP** | https://mcp.zencreator.pro/mcp | OAuth 2.1 (no API key) | Hosted MCP. ~28 `zencreator_*` tools. Agent calls `zencreator_create_task` with a generation `tool_name`. | Cursor / Claude / ChatGPT driving the same tools. Estimate price first. |
| **Org Studio (droplet)** | internal schema form | whatever the droplet wired | Raw JSON schema of a generation tool. `category_id` is a **text field**. No theme cards. | Debugging / API-shaped submits. **Do not pick themes here.** Copy IDs from the app. |

### Two layers of "tools" (MCP especially)

This is the most common confusion.

- **MCP tools** (what the client lists): `zencreator_create_task`, `zencreator_list_tools`, `zencreator_get_me`, `zencreator_estimate_price`, `zencreator_upload_asset`, …
- **Generation tools** (values you pass as `tool_name`): `photoshoot`, `image_editor`, `by_prompt`, `videogen`, `faceswap`, `upscaler`, `collaber`, `lipsync`, …

Example: `zencreator_create_task` is an MCP tool. `photoshoot` is a generation tool. `SEEDREAM_5_PRO` is a **model** on `image_editor`.

Public API equivalent: `POST /api/public/v1/generations` with `{"tool": "photoshoot", "input": {…}}`.

### Async everywhere

App hides it. API/MCP do not.

1. Upload refs → `asset_id`.
2. Start generation → task / generation id.
3. Poll until `succeeded` | `partial` | `failed`.
4. Fetch outputs (MCP: `zencreator_get_call_result` — polled `output` is lazy/`null`).
5. Failed generations **auto-refund credits**. Bad creative results do **not**.

MCP: use `zencreator_run_and_wait` for stills this turn. **Do not** block on video — submit and poll.

API rate limits (per key, 60s window): read 60/min, generate 10/min, upload 30/min. Idempotency-Key on POST /generations (24h).

### Catalog mismatch (critical for JSW)

Official API/SKILL.md:

> Templates & photoshoot categories — `GET /api/public/v1/templates` and `GET /api/public/v1/photoshoot-categories` return **only SFW, public presets through the public API, regardless of account status.**

So: trusted + NSFW-allowed still does **not** expose Lingerie / BDSM / Essential Touch via the public listing. Those live in the **app Photoshoot grid** behind **"Show 18+ templates"**. If Org Studio or an agent only sees SFW category IDs, that is expected — not a broken account.

### Publishing (do not use)

App can send results to Instagram / TikTok / YouTube / Facebook / Threads. Getting Started also says native publishing/scheduling "arrive in Version 2; until then export and post manually." Either way: **JSW does not post from Zen.** Export stills → Fanvue. Higgsfield owns SFW social.

---

## 2. Photoshoot recipe (refs, themes, counts, ratios, credits, 18+)

Photoshoot is **not** text-to-image. It is a **template batcher with Identity Lock**. You pick a category; the tool owns wardrobe, lighting, lens, mood, composition. Each category holds 100–500 internal prompt templates for variation.

Official API description (keep this distinction):

> Each shot is generated from scratch, so **poses come out organically different** between frames — unlike `image_editor`, which **keeps the source composition**.

### Inputs (always both slots)

| Slot | API field | What to put | Why |
|---|---|---|---|
| **Face** | `face_ref` | Sharp, well-lit, **front-facing**, **shoulders/chest-up**, ≥512×512, neutral expression. Or a saved Persona face. | Identity Lock. Full-body crops in this slot mix identity with physique and cause skull/face drift. |
| **Body** | `body_ref` | Full or half body. **No face.** For 18+: **headless** (and for explicit Fanvue: unclothed so anatomy is not invented). | Physique, framing, outfit/stance. A headed body lets the model pick the wrong face. |

**JSW rule:** Photoshoot has both slots → **always fill both.** Do not run face-only.

Help article + university NSFW lesson agree: face = chest-up at most; body = full, ideally without a face; 18+ prefers headless. University NSFW lesson adds: if the body is covered with clothing/lingerie/straps, the network **invents** anatomy and consistency dies.

### Categories / themes — pick, do not prompt

App flow:

1. Open Photoshoot.
2. Choose Female / Male.
3. Toggle **"Show 18+ templates"** for Lingerie and other 18+ cards.
4. Enter **how many images per category** (app examples: 5 / 10 / 15; help example Lingerie 6, Bikini 4). Button shows total.
5. Set aspect ratio + resize.
6. Generate. Cost shown on the button (**3 credits / image**).

API/MCP:

- `category_id` — curated preset. **Takes precedence over `prompt` if both are sent.**
- `prompt` — free-text fallback. Official docs allow it, but **JSW does not use it for Photoshoot.** Templates are the point. Need a custom shot → `image_editor` or `by_prompt`, not Photoshoot.
- `image_count` — total images (min 1). Drives how many shots from that category.
- `number_of_images` — parallel images **per shot**. Leave at 1. Control volume with `image_count`.
- `ratio` takes precedence over width/height when they disagree. Width/height clamped 512–4096, default 1024².
- `rewrite_prompt` default `false`. **Leave off.** Especially NSFW — the rewriter corrupts the prompt.

### Ratios (Fanvue stills)

Help: 3:4, 21:9, 1:1, 9:16, etc. API enum includes 1:1, 1:2, 2:1, 1:3, 3:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 9:21, 21:9.

JSW default for Fanvue vertical stills: **3:4** (or 9:16 if the destination is Stories-like). Keep ratio **consistent across a persona** — help lists identity inconsistency as a ratio/face-quality problem.

Outputs are already upscaled/resized to the chosen canvas. Optional polish: Upscaler (Safe Face) then Head & Face Swap last.

### Counts and credits

- **3 credits per photoshoot image**, × `image_count`.
- App mixes multiple categories in one run (Lingerie 6 + Bikini 4 = 10 images = 30 credits).
- University influencer guide: pick 3–5 niche categories × 10 photos = 30–50 stills per run.
- Lingerie guide: 5 / 10 / 15 per category, ~30 seconds.
- Retry Failed re-renders **only missing frames**.

Worked JSW numbers (do not spend yet):

| Job | Images | Credits | $ at Influencer pack (~$0.083/cr) |
|---|---|---|---|
| 1 theme × 6 | 6 | 18 | ~$1.50 |
| 1 theme × 10 | 10 | 30 | ~$2.50 |
| 3 themes × 10 | 30 | 90 | ~$7.50 |
| 6 personas × 3 themes × 10 | 180 | 540 | ~$45 (one Creator pack) |

### 18+ tips

- Toggle **Show 18+ templates** in the **app** grid. Not in Org Studio. Not in public API listing.
- Body ref: **headless**, full, anatomy visible. Face ref: chest-up, not full body.
- Lingerie is "formally not 18+" in the university NSFW lesson but sits behind the 18+ toggle in the lingerie product guide. Treat it as an app-grid 18+ card.
- Mix Lingerie + Cozy Home + Night Out in one app run if you want a Fanvue set that is not all one vibe.
- Do **not** use `rewrite_prompt`. Do **not** send a custom `prompt` hoping to "spice" a category — `category_id` wins and the custom text is discarded.

### Theme names found in public docs (not a complete catalog)

Public sources never publish the full grid. OpenAPI example pagination: **total 57** categories (gender-split; SFW public listing only). Marketing says **40+**. University NSFW lesson says **~18** in an older course recording. Treat 40+/57 as current SFW-visible size; 18+ cards are extra and app-only.

**Named in official pages (compile, not exhaustive):**

SFW / lifestyle (product, university, unfiltered guide, influencer guide):

- Cozy / Cozy Home
- Studio / studio editorial
- Beach / Beach Lifestyle (OpenAPI example)
- Work / Professional
- Glamour
- Holiday
- Fitness / gym
- Travel
- Street Style
- Portrait
- Night Out
- Café / café shoot
- Casual
- Winter / winter knit
- Summer pool
- Autumn park
- Rooftop
- Cosplay, anime, cyberpunk, fairy (themed/fantasy cluster)

18+ / near-18+ (help Photoshoot + university NSFW lesson + lingerie guide):

- Lingerie (toggle 18+; good poses; boudoir / fashion lingerie / close-ups / lifestyle-in-lingerie)
- Bikini (help example counts)
- BDSM (leather, straps, attributes)
- Essential Touch (softer boudoir)
- Holiday-themed 18+ variants: New Year, Christmas (course)

**To get the real current list without spending credits:** open app.zencreator.pro → Photoshoot → Female → enable 18+ → screenshot/note the cards. Do not query `GET /photoshoot-categories` expecting NSFW. Do not type guesses into Org Studio `category_id`.

---

## 3. Full tool map — when to use each (SFW vs Fanvue)

Higgsfield owns **SFW social**. Zen owns **Fanvue / NSFW stills** (and optional NSFW video later). Do not duplicate SFW volume on Zen.

### Image generation

| Generation tool | App name | Face+body slots? | Use for JSW Fanvue | Skip / SFW-elsewhere |
|---|---|---|---|---|
| **`photoshoot`** | Photoshoot | **Yes — always use both** | **Primary Fanvue still factory.** Theme batches, organic poses, Identity Lock. 3 cr/img. | Not for one-off custom compositions. |
| **`image_editor`** | Image Editor | Single `image_assets[]` (put scene first, face after). No dedicated body slot. | **Surgical edits** when a theme is not enough: outfit/location tweak, garment removal, keep pose. `SEEDREAM_5_PRO` keeps composition / skull. `FLUX_KLEIN_NSFW` for explicit anatomy on a ref. | Not for "give me 10 new poses." That is Photoshoot. Single-ref → **front-facing full-body** (JSW rule). |
| **`by_prompt`** | Text to Image | None | Rare. Mint a **body bible** from scratch (`SDXL_NSFW` / `FLUX_KLEIN_NSFW`). Not identity-stable for a series. | Higgsfield Soul 2 is the SFW face/body source of truth. |
| **`by_ref`** | Reference-To-Image | face + optional body (legacy) / `character_assets` 1–4 | Recreate a **reference scene** for the persona (`SEEDREAM_5_PRO`). `keep_pose: true` = person swap, ignore prompt. | MCP: explicit-request-only; prefer `image_editor` unless you need scene recreation. |
| **`facegen`** | Face Generation | None (parametric) | Only if minting a **new** Zen-native face. 1K=2 / 2K=3 cr. | JSW personas already exist in Higgsfield. Prefer Higgs keeper face crop. |
| **`faceswap`** | Head & Face Swap | face + target (not a body slot) | **Last identity lock** on keepers. Trusted-only. Run **after** upscale. Only Face = keep target hair; Full Head = persona hair/skull. `SEEDREAM_5_PRO` highest quality / person swap. 1–3 cr. | Not a content generator. |
| **`carousel`** | Variations / Carousel | One `asset_ref` | Extra **angles of one finished still**. No prompt. 1K=2 / 2K=3 cr per image. Single-ref → **front-facing full-body** if body must hold. | University: NSFW carousel is strong **if** the source is already a good nude. |
| **`collaber`** | Collabs | Two character images + optional location | Couple / duet Fanvue stills. 1–3 cr. One person per ref. | Not first-line. |
| **`upscaler`** | Image Upscaler | One image | Polish keepers. Use `*_safe_face` or identity drifts. | Don't upscale before you're sure it's a keeper. |
| **`flux_klein_lora`** | LoRAs AI Effects / Editor Flux Klein LoRA | 1–3 image refs | Trusted. Style templates + clothing-removal presets. 3 cr. Prefer `image_editor` + `FLUX_KLEIN_LORA`. Single-ish ref → full-body. | Don't use as a pose factory. |

### Video (optional later; not the Fanvue still path)

| Tool | When | NSFW model | Notes |
|---|---|---|---|
| **`videogen`** | Animate a **finished** still (`ref_asset` required) | `wan@2.7-nsfw` (trusted) or `wan@2.2-lora` (nsfw_allowed; Blink LoRAs, no prompt) | Finish upscale + faceswap **before** video. Do not animate a draft. |
| **`text_to_video`** | No starting frame | trusted-only | Don't use if you already have a keeper still. |
| **`video2video`** | Motion transfer / character replace | `replace_nsfw`, `animate_nsfw`, `dreamactor_m2` (trusted) | Uncensored modes trade quality. |
| **`lipsync`** | Talking head, audio + portrait | `GENERAL_NSFW` (different model than image GENERAL_NSFW) | 3 cr / second of audio, max 35s. |
| **`couplegen`** | Two characters → combined still + wan-2.2 i2v | 10 cr flat | Paired LoRA. |
| **`video_upscaler` / `video_merger`** | Polish / stitch | — | Merger 1 cr. |

**Videogen cheat sheet:** general cheap → Seedance; NSFW still→clip → `wan@2.7-nsfw`; beginner explicit action from a still → `wan@2.2-lora` Blink (match the example first frame); SFW complex motion → Kling (censored — wrong stack for Fanvue).

### Other

- **Companion** — chat that writes prompts and generates. $19.99/mo unlimited **text**; media still burns the same credits. Optional. Not required for JSW.
- **`run_any_llm`** — 1 cr. Uncensored text (`grok` vision, `hermes-3-405b`, `euryale-70b`). Prompt-rewriting node. MCP also has **free** `zencreator_craft_prompt` (no Zen credits) when the sidecar is on.
- **Personas** — saved face (and related refs) in the app. Photoshoot and Face Swap can pick a Persona instead of re-uploading. Save the Higgs face crop here once per girl.
- **Templates** — public API/MCP list is **SFW-only**. 18+ LoRA templates appear in-app / `GET /loras` for trusted keys.
- **Publishing** — do not use.

### Model groups (by_prompt / image_editor)

Remember three buckets:

1. **Censored cloud, highest polish:** `NANO_BANANA` (also the only reliable in-image text). `GENERAL_NSFW` is uncensored-ish but **covers explicit anatomy from text**. Wrong for Fanvue nudes-from-scratch.
2. **Uncensored, transform refs, won't invent porn from text:** `SEEDREAM_5` / `SEEDREAM_5_PRO`, `WAN_2_7_IMAGE(_PRO)`, `QWEN_IMAGE(_PRO)`. This is why editor+Seedream keeps skull: it **edits the pixels you gave it**.
3. **Local, built for explicit:** `SDXL_NSFW` (text-only, ignores ratio, ~2:3), `FLUX_KLEIN_NSFW` (explicit **and** accepts a face ref). Slightly more artifacts.

`SDXL_NSFW` is **not** on `image_editor` (can't take refs). Explicit-on-a-reference → `FLUX_KLEIN_NSFW`.

---

## 4. Identity lock / persona refs

"Identity Lock" is Zen's name for Photoshoot tying every frame to the face (and body) refs. It is **not** a separate toggle. It is the Photoshoot pipeline.

### Persona kit per JSW girl (build once, reuse)

From Higgsfield keepers, cut **two Zen refs** (do not generate new identities on Zen unless a persona has no usable keeper):

| Asset | Crop | Used in |
|---|---|---|
| **Face bible** | Sharp front-facing, shoulders/chest-up, no heavy tilt, well-lit, ≥512×512 | Photoshoot `face_ref`, Face Swap source, Persona save |
| **Body bible (SFW)** | Front-facing **full body**, clothed, head optional but Photoshoot prefers **no face** | Photoshoot body for lingerie/bikini-adjacent SFW-leaning themes; single-ref tools |
| **Body bible (18+)** | **Headless** full body, anatomy visible, proportions correct | Photoshoot 18+ themes. University: clothing/straps on this ref → invented anatomy |
| **Full-body front (single-ref)** | Face **and** body in one frame, front-facing | `image_editor`, `carousel`, Flux Klein LoRA, videogen first frame when the tool has **one** image slot |

**JSW rule restated:**

- Two slots (Photoshoot, and by_ref when you pass face+body) → send **both**, never face-only.
- One slot → **front-facing full-body**, or body goes wrong.
- Never put a full-body crop in the **face** slot.

### Canonical Zen-native build (only if a persona has no Higgs face)

University / help "create a model from scratch":

1. `facegen` → pick the face, save to Personas.
2. `by_prompt` + `SDXL_NSFW` (or SDXL + body LoRAs) → nude body bible. General is weak at nudes-from-scratch.
3. Upscale body.
4. Head & Face Swap face onto body → combined bible.
5. `image_editor` to dress her for SFW refs ("dress her in a red dress", keep proportions).
6. Photoshoot / editor / carousel from those two refs forever.

JSW should skip 1–4 when Higgs keepers already lock identity. Crop keepers into the table above.

### Lock order (help Getting Started + Face Swap article)

1. Generate scenes (Photoshoot / editor).
2. Curate.
3. Upscale with **Safe Face**.
4. **Head & Face Swap last** onto the Persona face.
5. Then (only then) videogen.

Upscale without Safe Face changes the face. Face Swap before upscale gets softened/altered. Video from an unfinished still bakes the wrong identity.

Face Swap model pick:

- Safest / keep target hair → Only Face (`SDXL` / `GENERAL` / Only Face).
- Persona hair + skull → Full Head (or Full Head unusual poses).
- Highest quality / whole person into a scene → `SEEDREAM_5_PRO` (`swap_type`: face | head | person).

---

## 5. NSFW / trusted / LoRA notes

### Two gates (check both)

From MCP `zencreator_get_me` and help Trusted Status:

| Flag | Meaning | How to get it |
|---|---|---|
| **`nsfw_allowed`** | Adult content enabled in account settings | Toggle in app settings. If false, enable and retry — **do not silently fall back to SFW**. |
| **`is_trusted`** | Trusted Status | **Automatically after first successful payment of any credit pack.** Permanent. No specific plan required. Not available without payment. |

Trusted unlocks: uncensored NSFW generation, 18+ templates and LoRAs, Head & Face Swap, Text to Video, `flux_klein_lora`, trusted models (`SDXL_NSFW`, `FLUX_KLEIN_NSFW`, `wan@2.7-nsfw`, `wan@3.0-nsfw`, `dreamactor_m2`, …).

Until trusted: 18+ templates hidden, NSFW models error, **submitting a trusted-only task can fail and waste credits** (MCP docs). Face Swap is trusted-only in the help article.

Getting Started: "There's nothing to turn on manually — buy any credit pack, and Trusted Status unlocks automatically." Still verify `nsfw_allowed` if generations refuse.

### What "unfiltered" does **not** mean

Content Policy (Trust & Safety): 18+ platform. **Never** minors or anyone who appears under 18, even if labeled 18+. No NCII, sexual violence, impersonation of real people without rights, illegal content. Enforcement: block, suspend, terminate, report. abuse@zencreator.pro.

JSW personas are adult fictional/owned identities. Do not feed real-person nudes you do not have rights to.

### LoRAs (three families)

**1. SDXL body-shape LoRAs** — Text to Image + Reference-To-Image. Up to 3, strength 0.1–3.0, default 0.8, sweet spot 0.5–1.2. Keywords auto-injected. Contradictory pairs (Slim + Plus Size) at high strength = artifacts.

API keys include: `bombshell_v2`, `hourglass_body_shape`, `slimwoman_v2`, `softtummy_xl`, `uz_bbw`, `curvy_bodies`, `cameltoe_xl_000007`, breast sliders, `euromilf_mature`, `extrmusc`, `fbb_photo_sdxl_1_6_lite`, `chubby_cellulite_fat_bbw`.

App display names: Large Breast & Hourglass, Adjustable Large Breast / 2, Cameltoe, Soft Fuller Figure, Thick Thighs & Wide Hips, Plus Size Body, Soft Tummy & Curves, Elegant Mature, Athletic Tone, Strong Muscular Body, Slim Figure, Classic Hourglass Shape, Triple Breast (fantasy).

**2. Flux Klein style LoRAs** — Image Editor (`FLUX_KLEIN_LORA`) / LoRAs AI Effects. Trusted. **One template at a time.** Upload a photo; the LoRA owns pose/style (including clothing-removal presets). Optional short prompt for scene/pose only. 3 credits. Browse `GET /templates` or in-app LoRAs hub.

**3. Wan video LoRAs** — `videogen` `wan@2.2-lora` and `wan@2.7-lora`. Action presets ("Blink": any photo morphs into the NSFW action). Match the example first frame for non-Blink. `wan@2.7-lora` catalog: `zencreator_list_wan27_loras` / `GET /loras?model=wan@2.7`. Pass `loras: { "<id>": {} }` — exactly one id, empty object, no scale. NSFW/trusted presets filtered by account. 18+ LoRAs **do** appear on `GET /loras` for trusted keys (unlike photoshoot categories).

---

## 6. Pricing and credit costs JSW will actually hit

**One wallet. Credits never expire. Packs, not a required subscription** (Companion $19.99/mo is optional text). In-app Billing is source of truth; VoltPay tab can be more expensive than the table.

| Pack | Credits | Price | $/credit |
|---|---|---|---|
| Starter | 200 | $19.99 | ~$0.100 |
| Creator (popular) | 550 | $49.99 | ~$0.091 |
| Influencer | 1,200 | $99 | ~$0.083 |
| Professional | 6,300 | $499 | ~$0.079 |

Any pack → Trusted Status. First pack also: no watermarks, premium photoshoot themes, extra Wan 2.2 + Flux Klein LoRAs.

Marketing line "Starter $19.99/month" on some university pages is **wrong**. Help + pricing page: buy credits, they don't expire, no recurring charge unless you opt into auto top-up or Companion.

### Stills JSW will actually buy

| Action | Credits | Notes |
|---|---|---|
| **Photoshoot** | **3 / image** | Primary path. 10 Fanvue stills = 30 cr. |
| image_editor GENERAL / SEEDREAM_5 / WAN 2.7 / FLUX_KLEIN_NSFW | 1 / image | Cheap surgical edit. |
| image_editor SEEDREAM_5_PRO 1K / 2K | 2 / 3 | **Keep composition / skull.** Prefer 2K for hero Fanvue. |
| image_editor NANO_BANANA | 4 | Censored. Don't use for Fanvue NSFW. |
| image_editor / flux_klein_lora | 3 | Clothing-removal / style template. |
| by_prompt SDXL_NSFW fast / quality | 1 / 2 | Body-from-scratch only. |
| by_prompt FLUX_KLEIN_NSFW | 2 | Explicit + face ref. |
| by_ref SEEDREAM_5_PRO | 2 (1K) / 3 (2K) | Scene recreation. |
| faceswap most models | 1 | Last lock. |
| faceswap SEEDREAM_5_PRO | 2 / 3 | Best likeness. |
| upscaler basic / natural / seedvr2_3b | 1 | Safe Face variants same price band. |
| upscaler premium / ultra 16MP | 2 | |
| carousel / variations | 2 (1K) / 3 (2K) per image | |
| collabs GENERAL / Seedream 2K | 1 / 3 | |
| facegen | 2 / 3 | Avoid if Higgs face exists. |

### Video (only if JSW animates Fanvue later)

Ballpark, help article + OpenAPI (backend-driven — estimate before submit):

- NSFW still→clip: `wan@2.7-nsfw` 5s 720p **13 cr**, 1080p **17 cr**; 10s 26 / 34.
- `wan@2.2-lora` **10 cr** any duration (help: 720p 5s).
- Seedance Pro Fast 5s 720p **4 cr** (uncensored-ish, not the explicit flagship).
- Kling 5s **7 cr** — censored, SFW stack, skip for Fanvue.
- lipsync **3 cr / second of audio**.
- text_to_video wan@2.7 5s 720p **13 cr** (trusted).

### Refunds

Used credits: no refund. Partial packs: no refund. Failed generation: **auto refund**. Chargebacks before talking to support can lock the account. support@zencreator.com / in-app chat.

---

## 7. What NOT to do

1. **Do not write custom Photoshoot prompts.** Pick a theme. If API gets both, `category_id` wins and the prompt is ignored. Custom control → `image_editor` / `by_prompt`.
2. **Do not set `rewrite_prompt: true` on NSFW** (Photoshoot, image_editor SEEDREAM_5_PRO, by_prompt SEEDREAM_5_PRO). Default false. The provider rewriter corrupts explicit prompts into unrelated images.
3. **Do not pass `start_image` into Photoshoot.** Photoshoot is `face_ref` + `body_ref` + `category_id`. There is no start-frame / start_image field. Seeding a pose belongs on `image_editor` (keeps composition) or videogen (`ref_asset` = **finished** still). Don't confuse Higgsfield Seedance `start_image` with Zen Photoshoot.
4. **Do not post live** from Zen Publishing (Instagram/TikTok/YouTube/Facebook/Threads). JSW: export → Fanvue. Higgsfield owns SFW social.
5. **Do not put a full-body crop in the face slot.** Skull-shape drift. Face = shoulders/chest-up.
6. **Do not use a headed / clothed body as the 18+ body ref.** Headless + anatomy visible. Help's exact 18+ tip: headless body.
7. **Do not run face-only Photoshoot.** Two slots → use both (JSW rule).
8. **Do not feed a portrait-only image into a single-ref tool** (`image_editor` without a body in the set, carousel, many LoRAs). Body will be invented/wrong. Use a front-facing full-body.
9. **Do not expect `GET /photoshoot-categories` or Org Studio to show 18+ themes.** App grid only. Org Studio is a raw `category_id` text field.
10. **Do not use `image_editor` when you want a new pose series.** Editor keeps composition. Photoshoot redraws poses. Conversely: don't Photoshoot when you must preserve a Higgs keeper's exact skull/pose — editor + SEEDREAM_5_PRO.
11. **Do not Face Swap or Upscale (non-Safe-Face) in the wrong order.** Upscale Safe Face → Face Swap last → then video.
12. **Do not animate a draft** (`videogen` `ref_asset` must be a finished keeper). Help: "generate video from already fully finished materials."
13. **Do not silently fall back to SFW models** if NSFW is refused. Check `nsfw_allowed` + `is_trusted`. Fix the gate.
14. **Do not spend credits to "probe" themes in Org Studio.** Open the app Photoshoot grid.
15. **Do not use NANO_BANANA / Kling for Fanvue NSFW.** Censored. Don't use GENERAL_NSFW expecting nudes-from-text — it covers anatomy.
16. **Do not violate Content Policy** (minors, NCII, real-person impersonation). Immediate ban, no refund.

---

## 8. Recommended JSW workflow

**Goal:** 6 adult female personas. Higgsfield keepers stay the SFW identity. Zen Photoshoot themes produce Fanvue stills. Editor only when a theme cannot do the shot. No posting. No speculative generations in this briefing.

### A. One-time kit per persona (crop Higgs keepers — no new Zen identity)

1. From a Higgs keeper, export:
   - **Face bible** — front, shoulders/chest-up, sharp.
   - **18+ body bible** — headless full body (build via editor clothing-removal / Flux Klein LoRA on a full-body keeper if needed, **once**).
   - **Single-ref full-body front** — for editor/carousel/video.
2. Save the face into Zen **Personas**.
3. Confirm account: paid pack → `is_trusted`, settings → `nsfw_allowed`.

### B. Fanvue still production (default)

1. Open **app.zencreator.pro → Photoshoot** (not Org Studio, not API category list).
2. Female → **Show 18+ templates**.
3. Fill **both** slots: Persona face + headless body.
4. Ratio **3:4** (Fanvue still). Match width/height to that ratio.
5. Pick 2–4 themes for the drop (e.g. Lingerie + Essential Touch + a lifestyle 18+ mix like Night Out / Cozy if it fits the girl). Counts 6–10 per theme.
6. Generate. **3 cr × N**. Retry Failed only.
7. Curate. Reject identity/anatomy misses; do not "fix" by rewriting Photoshoot prompts.
8. Upscale keepers with **Safe Face**.
9. Head & Face Swap **last** from the face bible if skull/face still drifted.
10. Export. Upload to Fanvue. **Do not** Zen-publish.

### C. When a theme is not enough (editor branch)

Use `image_editor` when you need **this exact composition** (Higgs pose, specific couch, specific crop) or a change the category will not make.

- Single image in: **front-facing full-body** (JSW single-ref rule).
- Multiple images: scene/base **first**, face bible **after**.
- Model: `SEEDREAM_5_PRO` 2K (3 cr) to **keep skull/composition**. `rewrite_prompt: false`.
- Need explicit anatomy the ref doesn't have: `FLUX_KLEIN_NSFW` (or Flux Klein LoRA clothing-removal), still with a full-body ref.
- Then Safe Face upscale → Face Swap last, same as B.

Do **not** start on editor for a 10-pose lingerie set. That is Photoshoot.

### D. Optional extras (after stills exist)

- **Carousel / Variations** on a winning nude for extra angles (single-ref = full-body).
- **Collabs** for two-persona Fanvue, one person per ref.
- **Videogen** `wan@2.7-nsfw` or `wan@2.2-lora` Blink from a **finished** still only. Estimate price first. No `run_and_wait`.

### E. What stays on Higgsfield

SFW social, Soul 2 identity, anything that must stay on the public-facing influencer accounts. Zen is the NSFW / Fanvue lane. Don't burn Zen credits duplicating café/street/gym SFW — Photoshoot can do those themes, but Higgs already owns that look.

---

## Appendix A — Help center index (walked 2026-08-30)

**Getting Started (1):** Your First Generation — https://help.zencreator.pro/articles/12034564-getting-started-with-zencreator

**Tools (21):** LoRAs AI Effects (6278218), Companion (6757693), Image to Video (12020612), Text to Video (6350226), Video to Video (12689501), Video Upscaler (13465993), LipSync (12883213), Video Merger (3411080), Text to Image (12020609), Image Editor (12629094), Head & Face Swap (11953232), Image Upscaler (12020606), Reference-To-Image (12020610), Photoshoot (12012768), Face Generation (11939450), Variations (11953361), Collabs (4510901), General FAQ (0306652), Public API (0458410), ZenCreator MCP (2285943), Zen Audio (0308782)

**Prompting & Core Concepts (11, sampled):** Prompting People (12021250), Image LoRA Guide (12020838). Others exist in the collection (video prompting, consistency, etc.).

**Billing & Account (4):** Pricing & Credits (12068902), Payments & Billing (12068926), Top Up Credits (13217480), Affiliate Program.

**Trust & Safety (4):** Refund Policy (1189715), Content Policy (1373215), Terms (5361807), + privacy/cookies referenced from Terms.

**Trusted Status:** https://help.zencreator.pro/en/articles/2793903-trusted-status

**University (high signal):**  
- Photoshoot deep dive: /ai-university/guides/photoshoot-tool-deep-dive  
- Build AI influencer: /ai-university/guides/how-to-build-ai-influencer  
- Lingerie Photoshoot: /ai-university/guides/ai-lingerie-photos-photoshoot  
- NSFW Photoshoot lesson: /ai-university/courses/en-ai-persona-course/lessons/en-lesson-4-2  
- SFW Photoshoot + Editor: …/en-lesson-3-2  
- NSFW Carousel: …/en-lesson-4-1  

**MCP:** https://mcp.zencreator.pro/docs/concepts · /docs/models · /docs/workflows  
**API:** https://api.zencreator.pro/api/public/docs · /openapi.json · /skill.md  
**Pricing:** https://zencreator.pro/pricing

### Contradictions (resolved)

| Claim | Where | Resolution |
|---|---|---|
| Photoshoot is "SFW only" | Unfiltered-tools marketing page | **False** vs help, lingerie guide, NSFW course, API. 18+ lives in the app toggle. |
| Starter is "$19.99/month" | Same marketing FAQ | **False.** Credit pack $19.99, credits never expire. Companion is the $19.99/mo text sub. |
| "Usually four" variations | Photoshoot deep-dive FAQ | App lets you set 5/10/15 (or arbitrary counts in help). Use the count you set. |
| "~18 categories" | Older NSFW course lesson | Current marketing/API: 40+ / example total **57** SFW-listed. 18+ extra in app. |
| Native publishing live vs "Version 2" | Influencer guide vs Getting Started | Irrelevant: JSW does not post from Zen. |

---

## Appendix B — Photoshoot API fields (do not fire)

```
tool: photoshoot
face_ref: <asset>          # required
body_ref: <asset>          # required — JSW: always send
category_id: <uuid>        # from app grid; beats prompt
prompt: ""                 # JSW: leave empty
image_count: 6–10
number_of_images: 1
ratio: "3:4"
width/height: match 3:4
rewrite_prompt: false      # never true on NSFW
```

Cost: `3 × image_count` credits. Estimate on MCP before any real run.

