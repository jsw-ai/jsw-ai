# Identity consistency across photos + videos (research only, 0 credits) — 2026-10-18

## Already tried (from SHARED_LEARNINGS.md / HIGGSFIELD_EXPERT_GUIDE.md)
- Seedream 5.0 Pro 2-4 ref edits (face ref + body ref + body-spec wording): stills hold identity (Sam still rejected some Sienna ones).
- Soul 2 + face Soul ba97f512 (Sienna): face ~83% gate, body drifted; a retrain failed on unchecked images.
- Seedance 2.0 i2v from ONE start still (+ audio_references), 720p 8s: drift in face (narrower, hollow cheeks), bust larger, gloss, face detail loss (Valentina audit, Camille deglossing). Mitigations used: tight start crops, matte prompt, deglossed start frames, face-large framing.
- Guide notes Elements / motion_control / Kling Elements exist, but I found NO log of an actual test of them.

## NOT tried (per notes)
1. Elements (`manage_reference_elements` create) used as @character in Seedance 2.0 / Kling 3.0.
2. `motion_control` (Kling 3.0) with a real driving video.
3. Seedance multi-reference (face + body images as references, not just start_image).
4. Face-swap/Recast post-pass on video; first+last-frame; clip trimming; external LoRA.

## Tool facts (schemas)
- `show_characters` train: 5-20 images, ~10 min, Soul is usable ONLY with soul_2 / soul_cinematic; one soul_id per generation. Official help page: trained Souls auto-appear as Elements and carry into Seedance; "clearly the same person," not pixel-identical; extreme angles drift. Training is face-driven; no body control.
- `manage_reference_elements`: create from images, instant; use `<<<UUID>>>` in generate_image/generate_video prompts. Supported video: seedance_2_0, kling3_0 (needs start_image), cinematic_studio_video_v2/3_0. Not a body-proportion guarantee.
- `motion_control`: Kling 3.0, image_id + motion_video_id, resolution 720p/1080p, scene_control; no prompt. Kling's guide: element binding uses FACIAL info only (not body/clothes), needs matching orientation.
- `build_ai_influencer` / `ai_influencer_*`: character-sheet designer for NEW characters (1 identity ref); no video/ID lock. Not useful here.
- user-higgsfield-api: `create_character` (1-5 faces, 40 cr) works only with legacy Soul `generate_image`; video tools there are old (Kling 2.1, Seedance v1, DoP), single image, no references. `generate_talking_head` = Speak v2, image+WAV. Skip all.

## Web evidence
- Seedance 2.0 refs: 1-3 aligned images with roles (face / body / angle), explicit "inherit list incl. body proportion, build" + "do not inherit pose/background" clause; reference VIDEO is for motion not identity (seedance2video.ai, awesome-seedance character-reference-lock.md). Vendor-ish blogs; unverified by us.
- Kling (r/KlingAI_Videos 2,500-character test): less motion = more identity; head turns >15° and torso motion drift; trim clip before the end. 3-5 s clips beat 8-10 s. Face-swap (FaceFusion/LivePortrait) on drifted frames was suggested by a bot comment in r/generativeAI (low reliability).
- Wan 2.2 LoRA on fal: i2v trainer $0.005/step (400 steps ≈ $2) but REQUIRES video clips; image-only LoRA needs t2v/image trainer; 15-40 images recommended (fal.ai, wan27.org). Outside Higgsfield; body fidelity unproven.

## Ranked tests (cost = single cheap test; credit figures from guide/3P pricing, not preflighted)
1. Seedance 2.0 with face-ref + body-ref as @references plus the start still, inherit/do-not-inherit prompt, 5 s 720p: ~22 cr (observed 8 s = 36). Cheapest direct attack on bust/body drift.
2. Element of the approved still(s) → Kling 3.0 720p, 3-5 s, low-motion: ~7-15 cr (Kling 720p 7 cr 3P).
3. Motion Control: approved still + short real driving clip (needs Samuel's clip), 720p: ~6-12 cr. Best for body motion; face may need element binding (not exposed in the MCP tool).
4. Trim all clips to ≤5 s, hold-mode motion, waist-up framing: 0 cr extra.
5. Face-swap post-pass on one clip: ~2 cr/image 3P; fixes face only, can look pasted.
6. Wan 2.2 i2v LoRA on fal: ~$2-5 + needs video dataset + non-Higgsfield setup; last resort.
Low value: retraining Soul (video can't use it except via Element; body not controlled).

## Uncertainty
- No source proves any option holds BODY proportions in video; all identity claims are face-centric.
- Element/Seedance behavior with Higgsfield's MCP wasn't tested; Elements creation cost unknown (run get_cost preflight).
- Credit costs are from third-party trackers; preflight first.
