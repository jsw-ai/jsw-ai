> Notion is the source of truth: https://app.notion.com/p/400f29949b29810fbe39cbcde5d3d9f4. If this file conflicts, Notion wins.

# Higgsfield Expert Guide — Consistent AI-Influencer Content (Sienna Blake)
Compiled 2026-10-14 (ET) from Higgsfield official help center/blog/API docs, connected MCP tool schemas, and third-party pricing trackers. Research only: no paid generations, no training were run. Read-only calls made: `models_explore get/recommend`, tool schema reads.

**Confidence legend:** [OFFICIAL] = higgsfield.ai / docs; [MCP] = connected tool schema; [3P] = third-party (credit figures marked "~", verify with `get_cost:true` before spending).

## 0. Context: Sienna Blake
- Approved setup: Soul **"Sienna Blake" (ba97f512)** + a written body spec. Use it with `soul_2` (or `soul_cinematic`) only.
- A retrain failed because training images were not identity-checked. Root cause class: Soul ID learns *whatever is in the set*; any off-identity face (AI drift, different person-look, heavy makeup/filters) gets averaged into the identity. See §1 for the gate.

---
## 1. Training Soul ID / character models
**Counts (sources conflict — know both):**
- Official help center/blog/Soul intro [OFFICIAL]: **20+ photos, up to 80**; training ~3–5 min; "smaller clean varied set beats a large inconsistent one."
- MCP `show_characters` train + `generate_image` description [MCP]: **5–20 images, ~10 min**. Higgsfield skills repo photo-guide: min 5, max 20, sweet spot 8–12.
- **Recommendation for Sienna: 20–30 verified images** (satisfies official minimum and stays within the MCP 20 cap). Never go below 12. Never pad with weak images to hit a number.

**Composition of the set (target 24):**
| Slot | Count | Notes |
|---|---|---|
| Front, neutral/relaxed | 4 | eyes visible, sharp |
| 3/4 left + 3/4 right | 6 | |
| Profile / near-profile | 2 | official blog asks for at least one |
| Slight up/down tilt | 2 | |
| Smile / talking / laughing | 4 | expression variety, so it can extrapolate |
| Head-and-shoulders / waist-up | 3 | |
| **Full-height (≥1, ideally 2–3)** | 2–3 | official: improves body proportion; check against body spec |
Vary lighting (indoor/outdoor, soft/harsh-but-not-shadowed), outfits, backgrounds, but keep **one consistent "look"** (hair colour/length, makeup level, age, skin tone). Resolution ≥1024px (blog: ≥960px "Perfect"). JPEG/PNG, **image uploads only** (not video frames pasted as video).

**Avoid:** sunglasses, hats/scarves over face, heavy shadows, cropped faces, group shots, same pose repeated, near-duplicate batch from one session, heavy filters/beauty smoothing, costume/heavy makeup, outdated looks, upscaled mushy images, **any image that is not the approved Sienna** (AI artifacts: warped teeth/eyes, wrong moles/freckles, skin-tone shift).

**Identity-check gate (mandatory before any train call — fixes the failed retrain):**
1. Anchor set = the approved canonical Sienna images (original successful training set / approved face sheet).
2. Every candidate image is compared against anchors: face-embedding similarity (e.g. insightface/ArcFace cosine) AND human/vision-model eyeball on a contact sheet. Reject outliers (flag anything below the median-of-approved minus margin; calibrate the threshold on known-good images first).
3. Check fixed features: eye colour/shape, nose, lips, freckles/moles/beauty marks, jawline, hairline, skin tone, body build vs body spec.
4. Reject duplicates (perceptual hash) and sunglasses/occlusion/group/cropped.
5. Write a manifest (file, source job id, similarity score, pass/fail, reviewer) and keep it with the Soul id.
6. Get Samuel's approval of the final set before spending training credits.

**Captioning:** Higgsfield exposes **no caption field** for Soul training in the app, official docs, or MCP (`show_characters train` takes only name + images). No manual captions; do not rely on filenames. Identity comes from the images alone. (Any caption advice from other platforms/LoRA tools doesn't apply.)

**Retrain pitfalls / facts:**
- Retraining creates a **new** Soul id; the old one remains. Keep ba97f512 untouched as the approved baseline; name new ones with version + date (`Sienna Blake v2 2026-10-14`) and A/B before replacing.
- "Failed" status causes (skills repo): too few/too uniform images, heavy occlusion, group photos, wrong upload type. Plan requirement: training needs a paid plan ("Minimum Basic plan required").
- If outputs look inconsistent: swap repeated poses/shadowed shots, add a full-height shot, keep set in one look — don't just add more images.
- Invented characters: generate portraits first, identity-check them, then train. Soul ID on AI-generated sets compounds drift: generate from the **existing** approved Soul so every training image is on-identity.
- Soul ID is **one person per generation**; not exportable; works only with `soul_2`, `soul_cinematic` (and legacy `soul`). Expect "clearly the same person," not pixel-identical; extreme style/angles drift.
- Trained Souls auto-appear in **Elements**, usable with Seedance etc. (see §3/§5).
- Timeout in a train/gen call = outcome unknown: check `show_characters status/list` before retrying (avoid double-charging).

Sources: https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-create-and-use-a-soul-id-character · https://higgsfield.ai/blog/Soul-ID-AI-Character-Consistency · https://higgsfield.ai/blog/how-to-turn-photo-into-consistent-ai-persona-creator · https://github.com/higgsfield-ai/skills/blob/main/higgsfield-soul-id/references/photo-guide.md · .../troubleshooting.md

---
## 2. Soul 2.0 settings and styles
**Params [MCP `models_explore soul_2`]:** `quality` 1.5k | 2k (default 2k); `soul_id`; one reference image max (role `image`); aspect ratios 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3; batch 1–4 (`count`). Tags: ugc, fashion, editorial, realistic. Supports unlim (free-trial) only if user asks.
**Inputs:** prompt + preset/Moodboard + Soul ID + Soul HEX palette all combinable. **With a reference image the prompt field is disabled** (reference drives; Soul ID and HEX still apply) [OFFICIAL] — so for prompt control, don't attach a reference.
**Presets (20+):** Warm Ambient, General, Retro BW, Y2K Street, Subtle Flash, Y2K Studio, Street Photography, Theatrical Light, Asian Nostalgia, Editorial Street Style, Surreal Solarization, Flash Editorial, Digital Camera, Siren, Swag Era, Mystique City, Candy Pop, 2000s Band, Frutiger Aero, Drain, Old Smartphone.
**Realistic / iPhone look — recommended:**
- Preset: **Old Smartphone** (closest to casual phone) or **Subtle Flash**, **Digital Camera**, **Street Photography**; **one preset per series** (official consistency lever).
- Quality **2k** for finals, 1.5k for iteration; aspect **9:16** for Reels/TikTok, **3:4/4:5-ish (3:4)** for feed; batch 4 to pick best identity match.
- Prompt: short and concrete. Pattern: `Sienna, candid iPhone photo, [location], natural window light, slight motion blur, mild grain, casual [outfit], unretouched skin, visible pores`. Avoid "perfect/flawless/8k/masterpiece/ultra-detailed" (produces plastic AI sheen).
- Moodboard (Soul 2.0 only): custom style from 10–20+ cohesive, sharp, **face-free** images (up to 80). Good for a locked "Sienna feed" aesthetic. Soul HEX = colour palette from reference; Color Transfer carries grade across a series.
- Identity-check every output against the anchor set before it enters a training set or gets posted.
Cost: ~0.12 credits/image (Soul 2.0) [3P/OFFICIAL blog table 0.125]; legacy Soul 0.25.
Sources: https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-soul-to-generate-images · https://higgsfield.ai/blog/ai-fashion-photo-generator · https://higgsfield.ai/blog/create-custom-ai-moodboard-soul-2 · https://higgsfield.ai/soul-intro

---
## 3. Reference-edit models and multi-reference identity
Catalog snapshot [MCP `models_explore recommend`]:
| Model id | Notes |
|---|---|
| `nano_banana_pro` | Google; 1k/2k/4k (default 2k); image_references; reasoning-first; "consistent faces", text rendering; up to 8 refs (multi-reference mode) |
| `nano_banana_2`, `nano_banana_2_1`, `nano_banana_2_lite` | faster/cheaper; 2.1 adds thinking_level (minimal/medium/high), video refs, mask inpaint, seed |
| `nano_banana` | budget, 1 credit |
| `gpt_image_2_5` / `gpt_image_2` | OpenAI; MCP default for general/photoreal/reference editing; quality low→max, res 1k/2k/4k |
| `flux_3_image` | BFL; up to **10** reference images; 768sq–4k |
| Seedream 4.5 / 5 lite | Element-compatible; (legacy API tool: Seedream v4, 720p/1080p) |
**How to hold identity across edits:**
1. Preferred for Sienna: **generate with `soul_2` + Sienna Soul**, then use reference-edit models only to change scene/outfit/props.
2. For non-Soul models, use **Elements** (`manage_reference_elements` / `@` in prompt): save Sienna as an Element (trained Soul auto-appears). Element-compatible: Nano Banana Pro/2, GPT Image 2, Seedream 4.5/5 lite, Cinema Studio Image 2.5/Video 2/3.0, Seedance 2.0, Kling 3.0 [MCP]. Elements allow **multiple subjects**; Soul ID does not.
3. Pass 2–4 refs: one clean face anchor (front/3-4), one full-body for build, then scene/outfit refs. **State each reference's role in the prompt** ("Image 1 = Sienna's face and body, keep unchanged; image 2 = outfit only").
4. Iterate: change the prompt **or** the reference, not both. Draft at 1k, finals 2k/4k.
5. Pro Inpaint / `is_inpaint` + mask for local edits to preserve everything else.
6. Always identity-check results; reference models drift on eyes/nose over multiple edit generations — **always edit from the original anchor, never from a prior edit's output** (generational drift).
- Legacy-API MCP caveat [MCP user-higgsfield-api]: `edit_image_seedream` and `generate_image_seedream` there take **no image input parameter** (only prompt/aspect/resolution) — cannot do reference identity editing via that tool. Use the newer `user-Higgsfield` `generate_image` with `medias`.
Sources: https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-nano-banana-pro · https://higgsfield.ai/blog/soul-2-vs-nano-banana-pro

---
## 4. Face swap and character reference
- **Face Swap** (photo; also video via Video Face Swap app): source face photo + target photo/video. ~2 credits/image [3P]. Fast but "face only" — can look pasted, mismatched skin tone/lighting. Use only as a rescue; Soul-native generation is better.
- **Character Swap 2.0**: swap characters in an image in one click. **Recast**: swaps whole persona (body + motion consistency) into any video; Pro-tier app.
- **Kling 3.0 Motion Control** (MCP `motion_control`): your character still (`image_id`) + driving video (`motion_video_id`); `resolution` 720p/1080p; `scene_control` image|video (background source). ~12 credits/5s @1080p [3P]. Best way to put Sienna in a specific motion/dance without face drift. Genjutsu `hf_mult_motion_control` / `hf_mult_replace_object` models via `generate_video` (images role `image`, one video role `video`).
- **Soul Reference** (Soul 2.0 `image` ref) = style/composition reference, not identity; identity comes from Soul ID.
- **Higgsfield Character (legacy API `create_character`)**: 1–5 face images, 40 credits ($2.50) — a different, lighter reference for the legacy Soul API (`generate_image` with `character_id`). Not the same as a trained Soul ID; don't mix id spaces (ba97f512 is a Soul id for `soul_2`).
- Face swap onto borderline-safe imagery can trip NSFW filters (see §8). Only swap faces of Sienna (own AI character) or consenting real people.
Sources: https://higgsfield.ai/apps · https://higgsfield.ai/apps/face-swap · https://higgsfield.ai/apps/recast

---
## 5. Video models and keeping face/body consistent
**Default routing [MCP generate_video]:** `seedance_2_5` general; `kling3_0` multi-shot/audio/motion transfer; `minimax_h3` 2K keyframes/mixed refs; `marketing_studio_video` ads. Others on platform: Seedance 2.0 / Fast / 1.5, Kling 3.0 / 2.6 / 2.5, Wan 2.6 / 2.5, Veo 3.1, Sora 2, Hailuo 2.3, DoP (Higgsfield's own).
**Consistency rules:**
- Start from an **identity-checked still** (sharp, front/3-4, good light, full-body if body must hold). Image-to-video beats text-to-video for identity.
- Seedance: use the still/Element as identity anchor; **video references for camera/motion only, not identity**; one action + one camera move; shorter durations (5s) drift less; include "preserve face, hairstyle, outfit". `@Sienna` Element holds identity within one generation; for separate shots reuse the same Element and the same anchor still.
- Kling 3.0: Element/Bind Subject with 3–4 aligned front+profile refs; **multi-shot storyboard** to keep identity across cuts.
- Avoid: fast head turns >90°, hands near face, heavy occlusion, big camera orbits, long 10–15s clips, wide shots where face is tiny (face drift is worst at small face size).
- Generate several takes, pick by face-match check; use Motion Control for hard choreography.
- Body: include the body spec text in the prompt and use a full-body anchor still.
**Lip-sync / talking [OFFICIAL Lipsync Studio]:** image→video: Veo 3.1, Kling 2.6 Lipsync (≤1080p, audio), Wan 2.5 Speak, Kling Avatars 2.0 (longer), **Higgsfield Speak 2.0**, Infinite Talk (long-form); video→video: Kling Lipsync, Sync Lipsync 3 (≤4K). Templates: General, Selfie, Podcast, Car Talking. Native audio co-generation (Kling 3.0, Seedance, Veo) gives best alignment.
- Legacy API `generate_talking_head` (Speak v2): image + **WAV audio**, duration 5/10/15 s, quality high|mid, seed; 2–3 min.
- **Dubbing / voice_change** MCP tools: translate+lip-sync a video; replace voice keeping timing.
- **Voice cloning:** Audio → Voiceover → Add Voice (record/upload MP3/WAV, consent confirm) → reusable voice for voiceover, voice change, translation; reported **~40 credits** on success [3P]. Voices are separate from Soul ID — a Soul does **not** bind a voice; pick one voice and reuse it for Sienna everywhere. MCP: `create_voice`, `list_voices`.
- Legacy API video tools (user-higgsfield-api): `generate_video` (DoP lite/turbo/standard, motion_id, 5s), `generate_video_dop_standard` (2–10 s), `generate_video_kling` (**Kling v2.1 Pro**), `generate_video_seedance` (**Seedance v1 Pro**) — all I2V, no resolution/duration params, **older models**; prefer the newer `user-Higgsfield` tools.
Sources: https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-seedance · https://higgsfield.ai/kling-3.0 · https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-lipsync-voiceover-and-aspect-ratios · https://higgsfield.ai/voice-cloning · https://higgsfield.ai/blog/two-characters-one-scene-ai-video · community: https://seedance2video.ai/blog/seedance-2-character-consistency-reference-images · https://www.atlascloud.ai/blog/tips/solving-character-inconsistency-a-guide-to-kling-3.0-image-to-video-mode

---
## 6. Skin enhancer and realism tools
- **Skin Enhancer** (Apps; Pro badge): upload portrait → denoise, reconstruct skin texture, keep pores. Modes: **Soft Skin, Realistic Skin, Imperfect Skin** — use **Realistic** (or Imperfect for UGC candid look); Soft looks over-smoothed. ~4 credits/run [3P; button shows exact cost].
- Realism stack: Soul 2.0 + Old Smartphone/Subtle Flash/Digital Camera preset → (optional) Skin Enhancer Realistic → upscaler (`upscale_image`, Topaz-based) only if needed. Don't stack Soft Skin + upscale (plastic).
- Re-check identity after enhancing/upscaling; enhancers can subtly alter freckles/moles.
- Prompt realism terms: candid, natural light, film grain, slight blur, unretouched, visible pores, asymmetry; avoid beauty-retouch vocabulary.
Sources: https://higgsfield.ai/blog/The-Skin-Enhancer-How-to-Retouch-Pictures-with-AI · https://higgsfield.ai/blog/AI-Skin-Enhancer-How-AI-Retouching-Works-in-Editing

---
## 7. Credit costs (verify with `get_cost:true`; figures "~" and mostly [3P] soku.ai/creatify/reapi snapshots, Oct 2026)
**Images:** Soul 2.0 0.12 · Soul (legacy) 0.25 · Soul Inpaint 0.25 · Wan 2.2 0.5 · Nano Banana / Seedream / GPT Image / FLUX.2 Pro 1 · **Nano Banana Pro 2 (2K), 4 (4K)** · Face Swap 2 · FLUX.2 Max 4 · Skin Enhancer ~4 · Soul ID training: not published in sources found (check cost-preflight/plan; legacy API `create_character` = 40).
**Video (per 5s unless noted):** Seedance 2.0 720p 22 / 1080p 45 / 4K 110 · Seedance 2.0 Fast 17 · Seedance 1.5 480p 1 (~3 @720p) · Kling 3.0 720p 7 / 1080p 8 / 4K 30 · Kling 3.0 Motion Control 1080p 12 · Wan 2.6 1080p 20 · Veo 3.1 29 /4s (Fast 11) · Sora 2 10 /4s (Pro 50) · Hailuo 2.3 Fast 4 /6s · DoP Lite 3 /3s. Voice clone ~40.
**Plans:** Starter $19 = 270 credits (~$0.07/credit); Plus $59 = 1,200 (~$0.049; annual ~$0.039); Ultra $129 (~$0.043; annual ~$0.033). **API (open.higgsfield.ai, $ per second, Sept–Oct 2026 discounted):** Kling 3.0 Pro $0.084/s (list), Seedance 2.0 $0.099/s, Seedance 2.5 ~$0.145/s.
**Cheapest-good workflow:** iterate stills in Soul 2.0 (pennies) → one polished still → Kling 3.0 720p for test motion (7 cr) → Seedance 2.0/2.5 only for hero clips. Flagged NSFW generations are not charged/refunded automatically.
Sources: https://soku.ai/alternatives/higgsfield/pricing · https://reapi.ai/blog/higgsfield-ai-pricing · https://creatify.ai/blog/higgsfield-ai-review-(2026)-is-it-worth-it · https://open.higgsfield.ai/pricing · https://higgsfield.ai/blog/soul-2-vs-nano-banana-pro · https://higgsfield.ai/creator-hub/help-center/credits/how-credits-work

---
## 8. Limits and gotchas
- **NSFW status:** filters at prompt stage and at image upload/reference stage, **plus** each external provider's own filter (Nano Banana, Seedream, Kling, Sora, MiniMax, Wan, Veo). Known false positives: **swimwear/bikini, athletic/fitness wear, medical imagery, borderline reference images, ambiguous wording**. Statuses: `nsfw` in `get_generation_status`/`get_request_status`. Flagged = not charged / auto-refund (check Manage Account → Usage; contact Support with time/model/prompt if missing).
  - Legit mitigations: neutral specific wording ("swimsuit at the beach, casual vacation photo, full-coverage one-piece" instead of suggestive terms), add a descriptive prompt to an image-only input, swap/remove the borderline reference (a reference showing lots of skin can block even a safe prompt), choose a different model (filters differ by model — Soul native is generally the most permissive for fashion), use less revealing cuts/coverage, wider framing, non-sexualised poses.
  - **Do NOT** attempt to circumvent: Terms of Use prohibit bypassing moderation; support only helps rephrase. Don't loop retries on a blocked prompt (risk to account).
  - Also IP block: named characters/teams/living artists blocked; describe generically.
- Platform content policies (Instagram/TikTok) are separate; check before posting.
- Soul ID = 1 person per gen; Souls usable only in Soul 2/Cinema (other models need Elements); not exportable.
- With a Soul 2.0 reference image, prompt is disabled.
- Results (legacy API) retained **7 days** — download immediately.
- Legacy API image input must be publicly accessible HTTPS (`upload_image` takes base64); newer MCP tools require `media_upload → PUT → media_confirm` or `media_import_url` (media_id, **not URLs**) in `medias[].value`.
- Unlim/free-trial: `use_unlim` must only be true if user explicitly asks; never auto-enable.
- Transport timeout on submit = unknown outcome; don't auto-resubmit; check job list first.
- Folder/project: call `get_preferences` before first generation; reuse `folder_id` per conversation.
- Free/unlimited allowances apply only on higgsfield.ai, not via plugins/integrations; paid plan required for Soul training.
- Models/costs change often — Seedance 2.5, Kling 3.0, Nano Banana 2.1, GPT Image 2.5, FLUX 3 are current; legacy API tools are older versions.

---
## 9. Rules for bots (Sienna Blake)
1. **Never train/retrain a Soul without Samuel's explicit approval of the exact image set.** Training spends credits.
2. **Identity-check every training image** against the approved anchors (embedding score + visual contact sheet), write a manifest, reject outliers/duplicates/occlusion/groups before upload.
3. Train sets of **20–30** verified, varied images (incl. 2+ full-body); never exceed 20 if using the MCP `show_characters` path unless docs/tool allow; no padding.
4. Treat **ba97f512** as the baseline; never delete or overwrite it. New trainings get a new versioned name and must beat baseline in an A/B before use.
5. Use `soul_2` + Soul id for stills; use Elements for Nano Banana Pro/Seedance/Kling; one Soul per generation.
6. Preflight every generation with `get_cost:true`; test at cheap settings (Soul 1.5k, Kling 720p) before premium (Seedance 1080p/4K, Nano Banana Pro 4K). Don't use `use_unlim`/free gens unless told.
7. Always edit from the original anchor image, not from a previous edit; run an identity check on every output before posting or reusing as a reference.
8. Video: identity-checked still → I2V, 5s, one action, one camera move; video refs for motion only; keep face large in frame.
9. On `nsfw`: do not repeat the same prompt; rephrase neutrally/cover more/swap reference/change model once or twice, then stop and report. Never attempt filter bypass.
10. Don't mix legacy API ids (`character_id`) with Soul ids; prefer `user-Higgsfield` tools over legacy `user-higgsfield-api` (older Kling 2.1/Seedance v1, no references).
11. Download outputs promptly; log job ids, model, settings, cost, identity score.
12. Don't post or publish yourself. A JSW Content Reviewer PASS on the exact file (path + md5) and exact captions is the approval; only the JSW Content Scheduler posts (Ayrshare). (Updated 10/21 to match Hard Rules.)
13. Only real-person likeness with consent; Sienna is the AI persona.

---
## 2026-10-21 Audit addendum: tool-by-tool settings, prompts, failure modes, routing
(see HIGGSFIELD_FULL_AUDIT.md for the full map)
**Routing by content type**
- Feed still / carousel: Seedream 5.0 Pro 2-ref edit (face+body) 3:4 2k, 2.5 cr -> finish_v5 -> gate >=.78. Photo-dump look: soul_2 + soul_id + style (Disposable camera, Old smartphone, Digital camera, Subtle flash; get ids from get_presets source=soul_styles), 0.12 cr, gate >=.80 soul.
- Talking clip: seed_audio TTS with locked voice -> Seedance 2.0 i2v 9:16 720p 8s audio_references (36 cr). Lines <=8 words, "begins speaking immediately", higher neckline start frames.
- Trend dance/walk: hf_mult_motion_control (image role=our still, video role=driving clip, scene from image). Driving clip: single person, full body, no cuts, <=10 s, our own or licensed.
- Hook effect: execute_preset source=viral; input = one gated full-body still, 9:16, 720p; read the widget price before Generate.
- Outfit/scene swap in an existing clip: hf_mult_replace_object.
- Multi-model collab frame: Elements, two <<<id>>> in one prompt (nano_banana_pro or seedream_v4_5), then Seedream Pro fix-up per face.
- Localization: dubbing (spa/por/ita/fra) on lip-sync finals.
- Polish: upscale_video topaz 1080p; outpaint_image + paste-back original pixels (see Charlotte banner note).
**Failure modes**: presets/Seedance refuse cleavage-heavy start frames (status nsfw, credits may be lost); Elements drift (~.75) vs Seedream Pro; outpaint repaints faces (-.07 gate); upscaled frames lower gate (score originals); Kling warps hands with props; Seedance adds idle silence before speech; gloss comes from Seedance; preset prompts with "dark/selfie" can trigger preset notices (retry with declined_preset_id, no charge).
**Prompt patterns**: identity-first ("same woman as reference, same face"), then action, wardrobe (SFW, higher neckline for video), light, camera ("candid iPhone", "disposable camera"), and "natural skin texture, matte". Avoid imperfection lists (made models plain).
