> Notion is the source of truth: https://app.notion.com/p/400f29949b29810fbe39cbcde5d3d9f4. If this file conflicts, Notion wins.

# MODEL_CONTENT_PROCESS.md — standard process for all six models
Models: Sienna, Camille, Charlotte, Madison, Gabriela, Valentina. Any bot follows this. Written 2026-10-14.
Rule zero (updated 10/21 to match Hard Rules): a **JSW Content Reviewer PASS** for the exact file (path + md5) and exact captions is the approval to schedule and post. Samuel does not approve posts or weeks. Only the JSW Content Scheduler posts, via Ayrshare.

## 0a. Sienna: current method (updated 2026-10-14, supersedes §0/§2 where they conflict)
- **Primary:** the approved **'Sienna Blake' Soul (`ba97f512-0ed0-4c56-9480-5abe167b06d1`)** + body spec (`sienna_body_spec.md`) + identity gate (`identity_gate.py`, recalibrated) + **v4C finishing** (the pipeline that produced `posting_oct14/v4/*_v4C.jpg`).
- **Fallback if the face drifts:** **Seedream 5.0 Pro reference-edit** (§2 recipe), anchored on the pack refs.
- **No retraining** on `retrain/` images (they are rejects; never use them as training or reference data). Any future training follows §6 only.
- **Reference set (only these):** `v4/{story1_a,story2_a,story3_b,reddit_x1_b,x2_dawn}_v4C.jpg`, `v3/x2_dawn_v3.jpg`, 3 frames from approved noon TikTok `v6/T1_wan_b.mp4`; copies in `zen/posting/sienna_refs/`, sheet `zen/posting/reference_set_sienna.jpg`. `sienna_face_keeper.png` and other older refs are dropped (listed under `dropped_refs` in the pack).

### 0b. Sienna lock test, measured (2026-10-14 ~22:50 ET; **CORRECTED by §0c: the "8/8" below was a face-only gate; photos 6-8 were rejected by Sam on review and replaced in v2**; sheet `zen/posting/higgsfield_lock_test.jpg`, files `zen/posting/lock_test/`)
8 candid phone-style stills (kitchen, balcony, cafe, beach path, one-piece, beach, park, sofa; front/3-4; body spec in prompt; 3:4, 2k), all through `identity_gate.py`, failures retried with Seedream 5.0 Pro (face ref `story1_a_v4C` + body ref `x2_dawn_v4C`), passers finished with v4C (`lock_test/finish_v4C.py` = make_v4 option C) and re-gated.
| Method | n | Gate pass (first try) | Notes |
|---|---|---|---|
| Soul 2.0 + face Soul `ba97f512` | 6 | **5/6 (83%)**, centroid 0.79-0.84, best 0.76-0.81 | only miss: `no_headroom_top_cropped` (cafe), identity itself fine |
| Soul 2.0 + body Soul `50583a87` | 2 | **0/2 (0%)** | centroid 0.75-0.78 but best-ref 0.69-0.70 (`identity_best_ref_low`); body Soul still not approved for face |
| Seedream 5.0 Pro ref-edit fallback (retry) | 3 | **3/3 (100%)** on attempt 1, centroid 0.79-0.81, best 0.83-0.85 | no 2nd retry needed; cafe scene fixed headroom too |
| Soul overall, no fallback | 8 | 5/8 (62%) | |
| Pipeline after fallback | 8 | **8/8 (100%)** | |
| v4C finishing re-gate | 8 | **8/8 (100%)** | centroid drop 0.00-0.03 (min 0.769), no flips |
Credits: balance 2507.26 -> 2498.80 = **8.46 spent** (8 Soul ~0.96 + 3 Seedream 7.5); cap was ~40. Skin Enhancer not used (not exposed via MCP); the v4C texture source was the local `skin_local.py` pass used for story2_a/x2_dawn (free).
Caveats for the reviewer pass (not gated): (1) Soul 2.0 ignores some clothing instructions and defaults to bikini/crop tops (the "sundress" prompt returned a pink bikini; the cardigan scene shows a sports top) and the bust reads larger than the pack refs, so swimwear/crop output needs Sam's body check; (2) no Soul style-preset parameter is exposed in the MCP (`soul_2` takes only quality, soul_id, one image), so the "Old Smartphone" look was prompt-text only; (3) n is tiny (6/2/3), directional only; (4) body Soul `50583a87` should be dropped from the primary path until it clears 12 gated images.
Recipe takeaway: use face Soul `ba97f512` first with "headroom above the head" worded explicitly; send gate failures (headroom or identity) straight to Seedream 5.0 Pro, 1 attempt was enough here.

### 0c. Lock-test review fix: face tightening + body check + v2 results (2026-10-14 ~23:25 ET)
**What Sam found on the v1 sheet** (`higgsfield_lock_test.jpg`; sheet position, not scene id: 1 kitchen, 2 balcony, 3 beach path, 4 park, 5 sofa, **6 = cafe `lock_test/fin/sd_3_a1_v4C.jpg`**, **7 = one-piece `sd_5_a1_v4C.jpg`**, **8 = beach `sd_6_a1_v4C.jpg`**; the 3 Seedream fallbacks): photo 6 face looked off; 7 and 8 had a too-skinny body / small bust. §0b "8/8 pass" was therefore wrong: **the gate only checked the face, and only loosely.** Passing the gate is not approval.

**(1) Why photo 6 passed the face gate.** buffalo_l centroid 0.771 / best-ref 0.819, inside the pass range of Sam's good photos (Soul 1-5 centroid 0.769-0.813, best 0.747-0.805). Per-ref sims show why: 0.82 vs `story1_a` (the face ref we fed Seedream) but only 0.64-0.73 vs the other 4 approved finals, i.e. Seedream partly copies one ref's face, which looks fine to the "best-ref" criterion. A second embedding (antelopev2 `glintr100`) and 106-point landmark geometry (eye/face-width, eye-mouth, nose, mouth ratios, Procrustes shape distance) were tried: **neither separates photo 6** (glint centroid 0.37 vs 0.30-0.46 for good photos and 0.34-0.53 for approved finals; landmark distance 0.043 vs 0.050-0.063 for good ones). They are not wired in. Only separator found: a per-source cut.
- **New rule: `--source seedream` requires centroid >= 0.78** (`THRESH.seedream_centroid`; reason `identity_centroid_low_seedream`). Result on the 8 v1 finals: photo 6 FAIL (0.771), Soul 1-5 unaffected (the cut is not applied to Soul), Seedream 7/8 pass the face part (0.796/0.811).
- **Honest limits:** margin is 0.009 on n=1 failing example. Leave-one-out on the approved finals with the cut applied: story1/story2/story3/reddit pass (0.79-0.84), **x2_dawn_v4C fails (0.76, its v3 twin excluded)**, so the cut would also reject 1 of 5 approved finals; it is only meant for Seedream output, which is not in the approved set. The numeric face score cannot see "looks off"; the visual check below is the real control.

**(2) Body check (`body_check.py`, wired into `identity_gate.py img --body`; reason codes `body_*`).** RTMPose-m keypoints (rtmlib) + u2net_human_seg silhouette, all widths in **face-heights** (buffalo face bbox height) so framing does not matter. Features: shoulder keypoint width `sh_w`; upper-torso silhouette width `bust_w` (widest row 15-45% shoulder->hip); thigh silhouette width `thigh_w` (hips+knees visible). Fail if `sh_w` < 0.90 (turned/narrow), `bust_w` < 1.40, `thigh_w` < 0.90; "unmeasurable" (not a fail) if pose/mask unreliable (`sh_w`<0.6 or mask width at shoulders < 1.05x shoulder width). Calibrated on: approved body refs (`x2_dawn_v4C/v3`, `reddit_x1`, `story1/2/3`, `T1` frames, keepers `sienna_bikini1/2`) and Sam's good photos 1-5, against skinny photos 7-8.
| Image | sh_w | bust_w | thigh_w | Body check |
|---|---|---|---|---|
| approved x2_dawn_v4C / bikini1 / bikini2 / reddit_x1 / story1 | 1.31 / 1.50 / 1.41 / 1.30 / 1.11 | 1.69 / 1.96 / 1.87 / 2.12 / 1.52 | 1.48 / 1.00 / 2.09 / - / - | all PASS |
| approved story2_a, story3_b | pose/mask unreliable | | | unmeasurable (selfie crops; story3 mask 1.00) |
| Sam-good photos 1-5 (kitchen, balcony, beach path, park, sofa) | 1.35-1.63 | 1.77-2.01 | 1.57 (beach path), others n/a | 5/5 PASS |
| **v1 photo 7 one-piece** | 1.35 | 1.75 | **0.83** | **FAIL** (thin thighs) |
| **v1 photo 8 beach** | **0.75** | 1.45 | 1.44 | **FAIL** (shoulders narrow/turned; bust 1.45 only just under-the-approved range) |
| v1 photo 6 cafe | 1.40 | 1.82 | n/a | PASS (its problem was the face) |
**Reliability, honestly:** this is a coarse silhouette proxy tuned on ~12 positives and 2 negatives, so it is overfit by construction. It measures width, not breast size: "small bust in a one-piece" is **not** directly measurable; photo 7 is caught only through thin thighs and photo 8 only through the narrow shoulder line from the 3/4 turn (its bust width 1.45 is above the 1.40 cut, so the bust cut did no work). It will flag legitimate 3/4 shots (sh_w <0.90) and arms-at-sides frames inflate widths. A zero-shot CLIP bust/skinny prompt was also tried and rejected (noisy: sd_6 scored like approved refs). **The body check can only reject, never approve.**
**MANDATORY visual body check (new, every still, every model):** the reviewer (model bot self-check, then the JSW Content Reviewer) must put the image beside `x2_dawn_v4C` and the body spec and confirm bust fullness, waist/hip curve, thigh and arm thickness, and face. `identity_gate.py --body` prints `visual_check_required` for every result; Reviewer submissions must carry a `VISUAL: checked` line. No numeric result substitutes for it.

**(3) Regenerated scenes (Seedream 5.0 Pro ref-edit, 1 attempt each, 3:4 2k).** Refs: photo 1 = `story1_a_v4C` (face), photo 2 = `x2_dawn_v4C` (body); front/shoulders-square angles; prompt adds the fuller-figure wording from `sienna_body_spec.md` plus "clearly fuller than a slim model, full toned thighs, wide curvy hips, not skinny" and for the swimwear scenes "head to mid-thigh visible" so thighs are measurable. Raw `lock_test/v2/raw/sd_{3,5,6}_b1.png`, finished with `v4C` (`v2/finish_v4C.py`) -> `v2/fin/sd_{3,5,6}_b1_v4C.jpg`. Gate results `v2/gate_fin_b1.json` (`--source seedream --body`):
| Photo | Scene | centroid / best-ref | sh_w / bust_w / thigh_w | Face gate | Body gate |
|---|---|---|---|---|---|
| 6 | cafe | 0.818 / 0.831 | 1.30 / 1.67 / - | PASS | PASS |
| 7 | one-piece | 0.799 / 0.842 | 1.38 / 1.81 / 1.41 | PASS | PASS |
| 8 | beach | 0.818 / 0.873 | 1.32 / 1.71 / 0.91 | PASS | PASS (thigh 0.91 is only just over the 0.90 cut: still a leaner figure than x2_dawn) |
Raw (pre-finish) all three also passed (0.81 / 0.796 / 0.81). v4C finishing moved centroid by +0.00 to +0.01. The visual check is pending Sam; my own look: bust fuller than v1 in all three, face reads as her, beach legs are still on the lean side.
Cost: balance 2498.80 -> 2491.30 = **7.5 credits** (3 x 2.5), cap 25. No training, nothing posted. Sheet: `zen/posting/higgsfield_lock_test_v2.jpg` (labels per check; bottom row = v1 6-8 re-scored with the new checks: all three FAIL). Scripts: `body_check.py`, `lock_test/v2/make_sheet_v2.py`. Tooling installed on the box: rtmlib RTMPose, `/workspace/models/u2net_human_seg.onnx` (+ unused pose_landmarker, antelopev2, CLIP onnx in `/workspace/models/`).
Generation rule going forward: Seedream prompts must carry the body-spec wording AND the body ref `x2_dawn_v4C`; never let a Seedream still through on face gate alone.


## 0. What we learned (why the process changed)
- **Random generation + filtering is the wrong foundation.** Soul 2.0 + a trained Soul ID (both `Sienna Blake Body v1` and the old face Soul `ba97f512`) drifts: 34 retrain-set images + 2 test images → only **3/36 pass the identity gate**. Visually they drift to a brunette with a different face, while her approved refs are a blonde with braids and blue eyes.
- **Face-locked generation** (start every image from her approved reference through a reference-edit model) held her face far better. Test of 4 approaches on Sienna (table in §3.2): **Seedream 5.0 Pro reference-edit passed 3/3**, everything else 0/3 or blocked. Details in §2.
- Higgsfield's own docs say the same thing: reference/edit tools "anchor to images you supply"; trained identity (Soul ID) is for "this same person, everywhere" but needs 20+ coherent, recent photos; single references "tend to lose [identity] over multiple generations," so re-anchor from the original every time ([HF: why faces change](https://higgsfield.ai/blog/Why-Does-Your-AI-Characters-Face-Keep-Changing), [HF Soul 2 vs NBP](https://higgsfield.ai/blog/soul-2-vs-nano-banana-pro), [HF Soul ID help](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-create-and-use-a-soul-id-character)).

## 1. Identity pack (per model)
File: `zen/posting/identity_packs.json` (read by the gate). One pack per model, frozen after Sam signs it. Contents:
1. **Face refs (4–8)**: sharp, well-lit, unobstructed, same hairstyle/eye colour, spanning front and 3/4. These are also the gate's reference set. Paths in the pack. Sam approves by looking at ONE contact sheet of the pack.
2. **Anchor pair for edits**: 1 face ref + 1 body ref, downscaled to ≤1600px JPEG (uploaded to Higgsfield as media ids; store ids in the pack).
3. **Body refs** + **body spec line** (e.g. `zen/posting/sienna_body_spec.md`).
4. **Signature traits line** pasted in every prompt (hair colour/style, eye colour, skin tone). Sienna: blonde braided hair, blue eyes. The gate scores face geometry, **not hair or eye colour**, so check this on the review sheet.
5. **Voice ref** (`voicerefs-from-sam/<model>.mp3`) and character ids (Soul ids are fallback only).
Pack status 2026-10-14: Sienna pack REBUILT from approved finals only (9 refs: 6 stills + 3 video frames); old refs dropped. Other models' packs are drafted from `keepers/` and **unapproved**.

## 2. Generation recipe (FACE-LOCKED; best measured)
Primary: **`seedream_v5_pro` reference-edit** (2.5 credits/image; 1k/1.5k/2k).
- `medias`: [face ref, body ref], role `image_references`. Aspect 3:4 (or 9:16 for video start frames).
- Prompt = `New scene: <scene, outfit, angle, expression>.` + freeze list + realism block:
  > Take the face exactly from photo 1: same facial structure, eyes, nose, lips, jaw, brows and hair colour as photo 1. Body proportions as in photo 2 (<body spec>). Candid unedited iPhone 26mm photo, face fully in frame with headroom, matte unretouched skin with visible pores, mild natural asymmetry, light natural tan, minimal makeup, phone noise, not glossy, no text, no other people.
- Number the references ("photo 1/photo 2") and state what to take from each ([Seedream guide](https://ai.byteplus.com/resources/what-is-seedream-ai), [face-consistency guide](https://docs.seedance.tv/en/face-consistency-guide)).
- **Never chain edits.** Every image is a fresh edit from the pack's original refs. If you must iterate on an approved result, pass the original ref again and say "take the face exactly from photo 2" ([guide](https://docs.seedance.tv/en/face-consistency-guide)).
- Refs must be ≥1000px, sharp, face unobstructed, one person ([HF face swap guide](https://higgsfield.ai/blog/AI-Face-Character-Swap-in-Video-Photo-PRO-Guide)).
- Scene rules from `CONTENT_RECIPE.md`: ordinary clothes, off-centre, flat natural light, no background people, no logos/text, front or 3/4 angles only for swimwear.
- Video: image-to-video from a **gated** still (Seedance 2.0 per `CONTENT_RECIPE.md` §3), then gate the clip (§3).
Fallbacks, in order: (a) Zen **Face Swap** (`faceswap`, Only-Face mode, 1–3 credits, run last on a gated keeper; per `ZENCREATOR_EXPERT.md`; not available as a tool in this environment, so untested), (b) Higgsfield Soul 2.0 + Soul ID. Both are worse until proven by the gate.
Not recommended: **GPT Image 2.5** was moderation-blocked (4/4 "nsfw") with swimwear refs, so no output.
Soul ID retraining: only if Sam wants it, and only from gated images (§6).

## 3. Automated identity gate
Script: `zen/posting/identity_gate.py` (venv `/workspace/.face-venv`; InsightFace buffalo_l / ArcFace). Packs: `identity_packs.json`. Calibration: `calibrate_gate.py`.
```
/workspace/.face-venv/bin/python zen/posting/identity_gate.py img   --model sienna a.png b.png --log zen/posting/reject_log.jsonl --json out.json
/workspace/.face-venv/bin/python zen/posting/identity_gate.py video --model sienna clip.mp4 --frames 8 --log zen/posting/reject_log.jsonl
```
Exit 0 = every file passed. Checks:
- **Identity**: identity gate at **0.78** on every scored face frame (Hard Rules §4, updated 10/21; the old 0.72/0.74 thresholds are retired).
- **Framing**: exactly one face (second face > 25% of the largest's area → `multiple_people`), face not cut by frame edges (2% margin), headroom ≥3% of image height at the top, face height ≥6% of image.
- **Text/logo**: OCR (RapidOCR) rejects any text ≥4 characters.
- **Video**: samples N frames (default 8, evenly spaced); needs ≥80% of frames to pass, median centroid ≥0.58, and no frame's centroid below 0.50.
- **Partly automated (§0c `--body`, coarse proxy, reject-only)**; the visual body check stays MANDATORY: bust/waist/hip/tan match (needs Sam's one-time body ref check on the review sheet, side by side with the body ref), hair/eye colour, hands/fingers, props/continuity. Add a reviewer-bot visual check for these (same freeze list as `CONTENT_RECIPE.md` §4).

### 3.1 Calibration (Sienna, REBUILT 2026-10-14; script `calibrate_gate.py`)
Thresholds (`THRESH`): **gate at 0.78 on every scored face frame** (Hard Rules, 10/21; old stills 0.72/0.74 retired). Old (historical) video-frame values: **video frames** centroid ≥ **0.55**, best-ref ≥ **0.52**, ≥80% frames pass, median centroid ≥ 0.58, no frame < 0.50. Framing/OCR checks unchanged. (Old thresholds 0.60/0.62 were calibrated on the old, incoherent pack and are retired.)
Positives are approved finals only; leave-one-out is by group (x2_dawn_v3 + x2_dawn_v4C are near-duplicates and are left out together; the 3 video-frame refs together).
| Group | n | Result |
|---|---|---|
| LOO approved stills (stills thresholds) | 6 | **6/6** identity pass; centroid 0.760–0.835, best 0.762–0.835 |
| LOO approved video-frame refs (video thresholds) | 3 | 3/3; centroid 0.625–0.638 |
| Other frames of approved T1_wan_b (not in pack, video thresholds) | 7 | **5/7** per-frame (f05 0.51, f09 0.53 fail); whole clip vs full pack: PASS 8/8 frames, min 0.671 |
| `retrain/raw` rejects (stills thresholds) | 32 with faces (34 total; 2 undetectable) | **0/32 pass** (centroid 0.23–0.77, but best-ref max 0.72; r03/r12/r14 reach 0.77 centroid and are stopped only by the best-ref threshold) |
| Other models' faces (all keeper files, 5 models) | 42 | **0/42**; centroid max 0.52 (`madison_bikini1`) |
| Dropped old Sienna refs vs new pack | 5 | face_keeper 0.51, face_close 0.55, bikini1 0.70, bikini2 0.73, cover 0.75 (only `cover` would pass; it is not in the pack) |
Honest limits: only 6 still positives, and the best-ref cut (0.74) sits just under the lowest approved LOO best-ref (0.762); a new approved style could be falsely rejected (re-calibrate then). Several retrain rejects score 0.70–0.77 centroid, so **centroid alone cannot separate them from her approved finals**; the stricter best-ref criterion does here, with a thin margin (0.719 vs 0.762). Video thresholds are much looser (video frames of an approved clip score 0.51–0.64) and would not reject retrain-type faces (26/32 retrain stills would pass the video thresholds if they were frames), so video relies on starting from a gated still and the reviewer-bot visual check. Passing the gate is necessary, not sufficient; Sam still reviews each batch (§5).

### 3.2 Face-lock test (Sienna, 2026-10-14; same 3 scenes: park shade laugh, kitchen tee, overcast beach bikini)
Sheet: `zen/posting/faceLock_compare.jpg`. Raw: `posting_oct14/faceLock/out/`.
| Approach | Cost/img | n | Gate pass | Centroid scores | Observation |
|---|---|---|---|---|---|
| **Seedream 5.0 Pro**, ref-edit with face + body ref | 2.5 cr | 3 | **3/3 (100%)** | 0.77 / 0.73 / 0.70 | Blonde braids, blue eyes, same face and body. Skin still a bit airbrushed/glossy (see §4). |
| Nano Banana Pro, ref-edit with face + body ref | 2 cr | 3 | 0/3 | 0.49 / 0.54 / 0.55 | Blonde braids kept, but the face reads as a different woman (broader, softer). Body OK. |
| Soul 2.0 + old face Soul `ba97f512` (no ref image) | ~0.12 | 3 | 0/3 | 0.52 / 0.62 / 0.51 | Drifts to a brunette; 2 of 3 crop the top of the head. |
| GPT Image 2.5, ref-edit | 0.25 cr | 0 | blocked | n/a | All 4 jobs returned status "nsfw" (swimwear refs); no images. |
| Baseline: Soul 2.0 + `Body v1` Soul ID (earlier tests) | ~0.12 | 36 | **3/36 (8%)** | 0.28–0.67 | Brunette drift in most. Lower realism too. |
n is small (3 per approach), so the ranking is directional. The Seedream margin (all clearly above threshold, visually the same face) is large enough to adopt as the default; re-verify when the sample reaches 20+.

### 3.3 Cost of this test
Reference-edit samples: NBP 6 cr + Seedream 7.5 cr + GPT 0 (blocked) + Soul old face ~0.4 cr ≈ 14 cr, within the ~15 cap. The Higgsfield balance moved 2529.12 → 2507.26 (−21.9) since the retrain-set report, which also includes ~10 Soul images from that batch finishing and the final Seedream sample.

## 4. Realism finishing (after the gate, before review)
1. ~~Skin Enhancer~~ (retired per Hard Rules §10, 10/21; use the local §5 finish only). Never "Imperfect Skin". Avoid "Soft" unless the face is already textured. ([review](https://www.creativepadmedia.com/make-ai-skin-realistic-with-1-click-higgsfield-skin-enhancer/), [HF playbook: Topaz Generative low creativity, Texture 1, Face Enhancement 70–85%](https://higgsfield.ai/blog/The-Playbook-for-Higgsfield-Upscale)).
2. **Re-run the gate on the enhanced file.** Enhancers can shift the face (this is why the gate runs twice: pre- and post-finish).
3. `CONTENT_RECIPE.md` §5 finish: skin-masked luminance texture 50%, no blur, mild sharpen, light grain, JPEG q90, strip metadata.
4. Video: finish the **start frame** first (enhancer), then Seedance/Kling, then light grain + sharpening only, no blur ([invideo on plasticky video](https://invideo.io/faq/why-do-ai-generated-videos-look-plasticky-and-fake-and/), [Topaz grain](https://docs.topazlabs.com/topaz-video/filters/grain)). Gate the final clip.
5. Realism prompt rules ([REALISM_RESEARCH.md](REALISM_RESEARCH.md)): matte skin, pores, mild asymmetry, uneven teeth, light tan, no "flawless/perfect/beautiful".

## 5. Batch rules
1. Generate N candidates per scene (default 6) with the §2 recipe, one fresh edit each from the pack refs.
2. Run the gate on all N. Only survivors continue; non-survivors are logged (§7) and not shown to anyone.
3. Finish survivors (§4), re-gate, then run the reviewer-bot visual checks (body vs body ref, hair/eye colour, hands, props, caption continuity, no AI mention).
4. Build **one contact sheet per model per week**: pack refs on the first row, then the gated finals with scores. Cap 3 posts per day per model.
5. Submit each final file (path + md5), its transition name and exact captions to the **JSW Content Reviewer**. A Reviewer PASS is the approval; the Reviewer forwards it to the JSW Content Scheduler, which posts via Ayrshare. No `approved/` folder gate and no weekly sign-off by Samuel (updated 10/21).
6. If the gate pass rate for a batch is <30%, stop and change the recipe (don't keep rolling); note it in the model's SOP/open issues.

## 6. Retraining rule
Soul ID / any character training sets may contain **only** images that (a) passed the gate against the approved pack, (b) were finished per §4 and re-gated, (c) show the same hair/eye colour as the pack, (d) are varied (angles, expression, light, outfits) and recent. Minimum 20, up to 80 ([HF Soul ID help](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-create-and-use-a-soul-id-character)). Never train on ungated output, on the Oct-14 retrain set, or on another model's output. After training, measure the new Soul ID on 12 fresh test images with the gate; adopt only if its pass rate is ≥80%.

## 7. Logging
Every gate failure appends one JSON line to `zen/posting/reject_log.jsonl`: timestamp, model, file, reasons (`no_face_detected`, `multiple_people`, `face_cut_by_frame`, `no_headroom_top_cropped`, `face_too_small`, `identity_centroid_low`, `identity_best_ref_low`, `text_in_image:…`, `unreadable`, or video frame failures), scores. Bots add `recipe` (e.g. `seedream_v5_pro`) when they run batches. Weekly: tally reasons per recipe and note it in the model's Notion SOP. Current log has 7 lines: the 3 NBP and 3 old-face-Soul test failures, plus 1 mis-path line.

## 8. Open items (historical, Oct 14)
- Sienna pack rebuilt from approved finals: glance at `reference_set_sienna.jpg` to confirm.
- Approve or edit the packs for the other five models.
- Decide whether to retrain Soul ID later or stay with Seedream face-lock.


## Final export (required, 2026-10-20)
`-c:v libx264 -profile:v main -pix_fmt yuv420p -movflags +faststart`, under 15 MB, full 9:16, no blurred padding bands. Verify with ffprobe (profile=Main) before review.
