> Notion is the source of truth: https://app.notion.com/p/400f29949b29810fbe39cbcde5d3d9f4. If this file conflicts, Notion wins.

# ZenCreator expert guide for NSFW / Fanvue (Sienna only)
Compiled 2026-10-14 (America/Detroit). Research only: no generations, no credits spent, nothing posted.
Reads first: `~/agent-data/workflows/zencreator/SKILL.md`, `zen/NSFW_VIDEO_RESEARCH.md` (note: the file is NOT under `posting/`), `zen/ZENCREATOR_EXPERT.md`, `zen/AUTOMATION_PLAN.md`, `zen/posting/MODEL_CONTENT_PROCESS.md`, `REALISM_RESEARCH.md`, `CONTENT_RECIPE.md`.
Prices below are from Zen's help page dated "21 days ago" and the MCP docs. Both say the UI/estimate price wins, so check before running.

## 0. Context that governs everything
- **Sienna is the only model approved on Fanvue.** No other persona goes to Fanvue. Couple Collabs need a second approved model, so Collabs are on hold for Fanvue until Sam approves another pack.
- **Identity** is face-locked from approved refs and checked with `identity_gate.py --model sienna` (centroid >=0.60, best ref >=0.62, one face, headroom). A Zen output that fails the gate is rejected whatever it looks like.
- **Sienna refs caveat:** `sienna_face_keeper` scores 0.58 against her other refs. Sam has not confirmed which refs are the real her. Use only the Sam-approved face plate (`keepers/sienna_face_close.png`).
- **NSFW video is parked** because it looked waxy and fake. Stills come first. Video is a test lane only (section 6).
- **Fanvue requires AI disclosure.** Policy (as of Oct 3): media must be disclosed "clearly and prominently" in the bio, caption or watermark. AI creator accounts carry an AI tag, and Fanvue lists a 15 AI-account limit. No real-person likeness, and nothing that could look under 18. Content passes a three-moderator "Reasonable Person's Test".
  - This is the opposite of `CONTENT_RECIPE.md`'s "no AI mention" rule, which is for SFW platforms only. Keep the two rules separate per platform.
- A JSW Content Reviewer PASS on the exact file (path + md5) and exact captions is the approval; only the JSW Content Scheduler posts (Ayrshare). (Updated 10/21 to match Hard Rules.) Bots never buy credits.

## 1. Surfaces and what an agent can do
| Surface | Use | Limits |
|---|---|---|
| App `app.zencreator.pro` | Photoshoot theme grid, 18+ toggle, Personas, LoRA templates, Undress Woman V3, Video Generator | Needs a human or computer-use. The Undress click is refused by the agent safety layer, so Sam or an approved handoff runs it. |
| Public API / Org Studio | Scripted `photoshoot`, `image_editor`, `videogen`, `upscaler`, `faceswap` | `GET /photoshoot-categories` and `/templates` show **SFW only**. NSFW category ids must be copied from the app. Org Studio has no `flux_klein_lora`, so Undress is not listed (see `CLAUDE_ORG_STUDIO_PATCH.md`). |
| MCP `mcp.zencreator.pro` | Same tools through OAuth. Use `get_me`, `get_tool_schema`, `estimate_price`, `compare_prices`, `create_task`, `get_call_result` | Not wired in this environment. Face Swap is unavailable here. Videos take 60 s to 55 min, so use create_task and poll. Never `run_and_wait` a video. |
| Account flags | `is_trusted` (set after first paid pack, permanent) gates NSFW models, Face Swap, `flux_klein_lora`, `text_to_video`. | MCP docs say `nsfw_allowed` only controls listing 18+ templates and LoRAs, not generation. This corrects `ZENCREATOR_EXPERT.md` §0/§5. |

**Cannot (this environment):**
- Face Swap (so there is no Zen face re-lock step).
- Undresser, via computer-use.
- NSFW photoshoot theme discovery by API.
- Post from Zen.
- A video face swap (Zen's `faceswap` is image-only).
- Skin Enhancer (this is Higgsfield and web-UI only).

## 2. Tool-by-tool recipes for Sienna stills
**Photoshoot (3 cr/img)**
- Slots: Face = tight chest-up (Persona or `sienna_face_close.png`). Body = front-facing full body per Sam's rule. Zen's own help says use a *faceless/headless* body for 18+ to stop face confusion. Sam's rule overrides this because back and headless plates drifted the skull. Test headless only as a deliberate A/B.
- Pick the theme from the app grid (18+ toggle). No custom prompt. `category_id` beats `prompt`. `rewrite_prompt` off.
- 3:4, one aspect ratio per run, 6 images per theme. Use Retry Failed for gaps (no extra charge).
- The shoot redraws poses from scratch, so expect drift. Run the gate on every frame.
- Help says outputs are already upscaled and "ready to publish". Still do the finishing in section 5.

**Image Editor (keeps composition, best skull)**
- Default: `SEEDREAM_5_PRO` 2K (3 cr). It takes up to 10 refs and **order matters**, so put scene first and face after. Prompt as a change: "keep her face and pose unchanged".
- Explicit anatomy not in the ref: `FLUX_KLEIN_NSFW` (1-2 cr, 3 refs, accepts a face ref, slightly lower quality).
- `FLUX_KLEIN_LORA` (3 cr) is only for a picked LoRA template. Without one it equals Klein Spicy. This is where Undress Woman V3 lives. App only, run by Sam.
- Nano Banana 2 is SFW only and has weaker likeness. Never use it for Fanvue.
- Do complex edits step by step (pose first, then clothing). Do not chain more than 2 edits. Re-anchor from the pack refs each time (matches `MODEL_CONTENT_PROCESS.md` §2).

**Variations (2K = 3 cr per generation, per Zen help)**
- One input, up to 10 angles, no prompt, uniform ratio. Use it on a keeper that already passed the gate. 5-7 images makes a tidy carousel.
- Help recommends the Image Upscaler before export. Re-gate after.
- Notes say "per generation"; Miami ×5 used about 15 cr. Check the UI.

**Collabs (couples only; on hold for Sienna-only Fanvue)**
- Seedream 5 Pro 2K = 3 cr. The legacy "General" model is 1 cr and 4K, and is "best for character series".
- One person per ref, matched light and angle, a location image to fix the background, and a short scene prompt. Make 2-4 and pick one. Max 2 people.

**Face Swap (unavailable here)**
- Zen order of use: scenes, curate, Safe Face upscale, then swap.
- Models: Seedream 5 Pro `face`/`head`/`person` (2-3 cr, slow, up to ~5 min), Full Head & Face Beta (1 cr, ~1K), MuleRouter fast (1 cr, 2K, no persona support), `GENERAL_ADVANCED` (best identity among the legacy models).
- Zen's own course says "Full Face" for 90% of cases.
- **Fallback for Sienna:** re-edit from the pack refs with Seedream 5 Pro (Higgsfield 3/3 gate pass) instead of swapping. Do not use a Zen stock face-swap as a workaround.

**Upscaler**
- Always `*_safe_face` (basic 1 cr, premium 2 cr). Non-safe-face upscaling changes the face.
- Alternative: `natural_clarity` (1 cr) or SeedVR2 3B/7B (1-3 cr), which are more natural than the sharpeners.
- Re-run the gate after upscaling.

**Personas**
- A Persona links a **face only** (plus name, group, bio, and linked socials). It does not hold a body.
- Photoshoot and Face Swap read the face from it. Make one Sienna Persona from `sienna_face_close.png` and nothing else.
- Don't save the other five models until Sam approves their packs.

## 3. Face and body consistency rules (Zen-specific)
1. Face slot: sharp, front-facing, chest-up, at least 512 px (use >=1000 px), no sunglasses or occlusion. Never a full-body crop.
2. Body slot or one-slot tools: front-facing full body with the face, otherwise the body is guessed. Paste the body spec line (`sienna_body_spec.md`) where a prompt is allowed.
3. Keep hair, makeup level and ratio stable across a shoot. Zen's own consistency guidance says treat the persona like a brand.
4. Every image is a fresh edit from the pack refs. No edit chains.
5. Face Swap needs similar lighting between source and target. Mismatched skin tone means a better source or matched light.
6. Gate then check body by eye: bust, waist, hips, tan. The gate scores the face only. Check hair and eye colour (blonde braids, blue eyes) on the sheet, because the gate does not score them.
7. Zen's Persona and Face Swap route is a reference-based lock. Independent reviews rate it 4/5 for consistency and say a trained LoRA is more robust. Sienna Body v1 on Higgsfield is the only trained identity we have, and it passes only 3/36 on the gate.

## 4. Realism settings
- Choose the realism lane by model: Seedream 5 Pro or WAN 2.7 Pro for edits (uncensored, realistic). `FLUX_KLEIN_*` is lower quality with artifacts. `Z_IMAGE_SPICY` and `KREA_2` (1-3 cr) are photoreal text-to-image options, but text-to-image does not lock identity. Skip them for Sienna.
- Prompt rules from Zen and our realism notes: "realistic skin texture, natural pores, no over-retouch". Don't use "beauty skin", "flawless" or "perfect". Add mild asymmetry, flat or soft off-centre light, and phone noise.
- Zen has no Skin Enhancer. Use Premium safe-face upscale or SeedVR2 for texture, then the `make_v4.py` option C finish (skin-masked 50% luminance texture, no blur, mild sharpen, grain, q90, strip metadata). Re-gate after each step.
- For video, add "film grain, natural imperfections, no 3D/cartoon/VFX" (Zen Seedance guide) and "realistic skin texture" for plastic skin.

## 5. Finishing pipeline (still)
Generate N candidates, then the **gate**. Then Safe Face upscale, then the gate again. Then the option C finish, then the gate again, then the reviewer-bot visual check (body, hands, props, hair and eye colour). Then the contact sheet for Sam. Fanvue disclosure goes in the caption or bio, never as hidden text.

## 6. Image-to-Video (still a test lane; Sam parked it)
What changed since the Sept notes (new models in the Zen help page):
| Model | 5 s credits (480/720/1080) | Notes |
|---|---|---|
| **Seedance 2.5 Spicy** | 13 / 29 / 100 | Zen claims "more natural, less AI-looking": skin, eyes, light. First frame, first+last frame, or Reference Mode (30 images, 10 audio, `[img1]`). 5-30 s. No negative prompt. Audio may be missing. Test at 480p/720p first. |
| Wan 3.0 Spicy / Prime | 15 / 30 / 50 (Prime 14/27/45) | Reference Mode up to 9 images and 3 audio clips. 5-30 s, native audio. MCP says 12/24/40. Runs 15-55 min. No negative prompt. |
| Seedance 2.0 Spicy / Fast / Mini | Spicy 7 / 16; Fast 6 / 13; Mini 4 / 8 (480p/720p) | Literal first frame. Mini was used for the Miami near-kiss. |
| Seedance Pro Fast | 2 / 4 / 7 | Cheapest draft. "~$0.20" in older notes is the 480p price. Zen calls it "less control, lower quality". |
| Wan 2.7 Spicy | 720p 13 (5 s), 26, 39 | Waxy on the lingerie test. |
| Kling 2.1/2.5/2.6 | 7 / 13 (10 s) | Most realistic skin, but Filters ON (SFW only). Zen's "AI Kissing" page is now a Kling-based template, not a Seedance Pro Fast guide. The Sept note's claim is outdated. |

Recipe (no spending until Sam OKs a test; the whole test is about 60 cr):
1. Start frame = a gated, finished, Sienna still. Wardrobe and pose already as wanted. Pose-match matters (single-person pose, camera not extreme).
2. **Seedance 2.5 Spicy, 720p, 5 s, one action** (about 29 cr), Start Frame mode. If testing identity drift, also try Reference Mode with `[img1]` set to the face plate. Compare with Mini (8 cr) as a cheap control.
3. Prompt = motion, then camera, then physics, then light and sound. 25-35 words, no re-description of the photo, no "beautiful". Example: `she breathes softly, blinks, tilts head 5° toward camera; static locked-off shot, slight handheld drift; soft window light, natural skin texture, visible pores, no over-retouch; faint room tone`.
4. Enhance prompt OFF. Fixed camera. No zoom (zoom melted the Miami faces). For Wan models use the negative prompt: `flicker, ghosting, plastic skin, warped hands, clothing coming off, watermark, text`. Seedance 2.5 and Wan 3.0 take no negatives, so state "keep the same outfit, no 3D, no cartoon" in the prompt.
5. Start/End Frame models: set both to the same still for loops.
6. Gate the clip frames (video mode of `identity_gate.py`, >=85% of frames pass) and review by eye on a phone screen. Add grain and mild sharpening only, no blur.
7. Zen help says to finish all stills (upscale, identity fix) before animating. Do not animate a draft.
- Kisses and couples need two people in the start frame, so they are out of scope for Sienna-only Fanvue.
- Keep spicy prompts to action descriptions. A vague prompt on a Spicy model undresses.
- Cheaper control: Wan 2.7 + LoRA "Blink" presets need no prompt but need a start frame similar to the preset example.

## 7. Credit cheat-sheet (help page, check live UI)
Photoshoot 3/img. Collabs: General 1, S5P 1K 2, 2K 3. Editor: General 1, Klein Spicy 1, S5P 2/3, WAN 2.7 Pro 2, Klein LoRA 3, NB2 4 (SFW). Face Swap: most 1, S5P 2/3. Variations 2/3. Upscale 1-4. Face Gen 2/3. Text-to-image: S5P 2/3, Klein Spicy 2, Z-Image 1-2, Krea 1-2. Lipsync 3/s. Merger 1. Packs: 200 cr = $19.99, 550 = $49.99, 1,200 = $99, 6,300 = $499. Credits never expire. Failed generations auto-refund, bad results do not. No free trial. Auto top-up exists (card only), so never enable it.
Estimated Sienna-only still batch: 1 theme × 6 = 18 cr. Safe Face upscale ×3 keepers = about 3-6 cr. Variations ×5 on one keeper = about 15 cr.

## 8. Content limits (Zen policy)
- 18+ platform. Auto pre-moderation of prompts and uploads, with face age estimation. Never minors or anyone who looks under 18, even labelled "18+" (permanent ban, NCMEC report). No non-consensual content, no real-person intimate or deepfake content, no recognised public figures.
- Zen says outputs have a full commercial licence. Fanvue requires AI disclosure and bans content taken from other sites or creators.
- Applies to bots: keep Sienna clearly adult in refs and prompt. Reject any output where she could read under 18. Delete it and do not retry.

## 9. Gaps vs Higgsfield
| Need | Higgsfield | ZenCreator |
|---|---|---|
| Trained identity | Soul ID (Body v1, passes 3/36) | None for us. Persona is face-only. Reference-lock only. LoRA training is claimed by reviewers, unverified. |
| Face-locked reference edit | Seedream 5 Pro 3/3 on the gate | Same Seedream 5 Pro is in Zen editor (cheaper, 3 cr at 2K). Face Swap here is unavailable. |
| Skin Enhancer | Web app, ~4 cr | None. Use safe-face or SeedVR2 upscale. |
| Video with voice ref | Seedance 2.0, voice ref, 8 s, 9:16 | Seedance 2.0/2.5 Spicy with audio refs (`[audio1]`), Wan 3.0 audio. Untested. |
| NSFW | Blocked (GPT Image "nsfw", filters) | Uncensored: Flux Klein, Spicy video models, LoRAs |
| Agent control | MCP tools | Browser or app mostly. API cannot list NSFW categories. Undress blocked for the agent. |
| Posting | Via Ayrshare | Do not post from Zen |
Net: Zen is the only NSFW-capable lane. For identity, Seedream 5 Pro reference edits on Higgsfield or Zen both work. Zen's own advantage is uncensored output and Spicy video.

## 10. Recommended workflow for a Sienna Fanvue batch
1. Preflight: the pack is Sam-approved. The gate venv works. The Zen balance is known (do not buy).
2. Photoshoot (app, human or approved handoff): Sienna Persona face + full-body ref, 18+ theme, 3:4, 6 images. Or Image Editor Seedream 5 Pro with face-then-scene refs for a specific pose.
3. Gate all outputs. Keep only passes.
4. Safe Face upscale on survivors. Gate again.
5. Finish (option C). Gate again. Reviewer-bot check. Build one contact sheet with captions that include the AI disclosure.
6. A JSW Content Reviewer PASS on the exact file (path + md5) and exact captions is the approval; only the JSW Content Scheduler posts (Ayrshare). (Updated 10/21 to match Hard Rules.) No `approved/` folder gate.
7. Undress variants: Sam runs Undress Woman V3 in the app from an approved still. The bot gates the result, because Undress can break pose and face.
8. Video (optional): the one Seedance 2.5 Spicy test in section 6, on one gated still. Sam judges.

## 11. Rules for bots
1. Sienna only. No other persona goes to Fanvue until Sam approves its pack.
2. Never post, buy credits, enable auto top-up, or change `go_live`.
3. Never run Undresser through computer-use or retry after a refusal. Hand off to Sam. If the agent is blocked, report it and stop.
4. Never invent a Face Swap substitute. If swap is needed, say it is unavailable here.
5. Photoshoot: pick the theme from the app, no custom prompt, `rewrite_prompt` off, both slots filled, 3:4.
6. Never chain edits. Every image is a fresh generation from pack refs.
7. Gate every file (`identity_gate.py`) before and after upscale and finish. Log rejects to `reject_log.jsonl`. If a batch passes <30%, stop and change the recipe.
8. Check body, hair colour and eye colour by eye. The gate does not.
9. Upscale only with `*_safe_face` or SeedVR2. Never apply a "beauty" or retouch step.
10. Animate only finished, gated stills. One action per clip, motion-only prompt, Enhance off, fixed camera, no zoom, 5 s at 480p/720p first.
11. Estimate cost before any run and get Sam's OK. Report credits used in the log.
12. Fanvue content carries a clear AI disclosure. No real-person likeness. Nothing under 18 or that could read as under 18. Delete and report such an output.
13. Trust the live UI over this guide for prices and model names. Both Zen help and MCP docs say they drift.
14. Failed or blocked tool calls are reported, not routed around.

## 12. Open items for Sam
- Confirm which Sienna refs are canonical (face_keeper is an outlier).
- Approve one Seedance 2.5 Spicy test (about 29 cr) and say whether a Mini control (8 cr) is OK.
- Decide if headless-body A/B for Photoshoot is worth 18 cr.
- Confirm the Fanvue AI tag and disclosure caption wording.
- Decide whether to enable the Zen MCP for the agent (Face Swap, estimates) and fix Org Studio for LoRAs.

## Sources
- Zen Help: Image to Video https://help.zencreator.pro/en/articles/12020612 · Photoshoot /12012768 · Collabs /4510901 · Head & Face Swap /11953232 · Variations /11953361 · Image Editor /12629094 · Pricing & Credits /12068902 · Content Policy /1373215 · Prompting for video https://help.zencreator.pro/articles/12023011 · Seedance 2.0 https://help.zencreator.pro/articles/9643424-mastering-seedance-20
- Zen MCP docs: https://mcp.zencreator.pro/docs/models · https://mcp.zencreator.pro/docs/workflows
- Zen site: https://zencreator.pro/pricing · https://zencreator.pro/help/getting-started/getting-started-with-zencreator · AI University persona course lessons 1-4 and 1-5 (https://zencreator.pro/ai-university/courses/en-ai-persona-course/lessons/en-lesson-1-4, …/en-lesson-1-5) · https://zencreator.pro/ai-university/guides/ai-kissing-video-seedance · https://zencreator.pro/ai-university/courses/wan-2-7-spicy-course/lessons/describe-motion-not-frame
- Fanvue: https://help.fanvue.com/en/articles/9538738-is-ai-content-allowed-on-fanvue · https://help.fanvue.com/en/articles/14290142-how-do-i-know-if-a-creator-is-ai · https://help.fanvue.com/en/articles/9539091-passing-kyc-and-creating-multiple-accounts-as-an-ai-creator · https://landing.fanvue.com/blog/ai-content-guidelines
- Community / reviews: https://www.outseeker.net/blog/ai-onlyfans-model-generator-tools-2026 · https://lustfind.com/site/zencreator · https://contentmavericks.com/best-ai-influencer-generator/ · https://picsart.com/blog/how-to-make-realistic-ai-videos/ · https://www.seedance.tv/blog/seedance-2-5-image-to-video-guide-2026 · https://wavespeed.ai/docs/docs-api/bytedance/bytedance-seedance-2.5-image-to-video-spicy
- Not retrievable: `zencreator.pro/ai-university/guides/photoshoot-tool-deep-dive` now 404s. AI University courses (including the NSFW photoshoot lesson 4-2) are "being rebuilt", so the old NSFW course claims in `ZENCREATOR_EXPERT.md` can't be re-verified.
- Review sites (LustFind, Outseeker, Contentmavericks) are affiliate-style and disagree on pricing. Treat them as low-confidence.
