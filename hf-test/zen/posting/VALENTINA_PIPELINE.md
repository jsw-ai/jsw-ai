# Valentina pipeline: stills and videos, end to end (for JSW AI / Sienna)
Written 2026-10-19 from the files on the box. Everything here is quoted from the sources listed at the end. Where a setting was never saved, this doc says so instead of guessing.
All paths are relative to /workspace/hf-test/zen/posting/ unless absolute.

## 0. Why her face looks natural (short version)
1. There is no trained Soul. Every still comes from a **Seedream 5.0 Pro reference edit** of real-looking reference photos (identity_packs.json: `"fallback_method": "seedream_v5_pro reference-edit from these refs (no Soul trained)"`).
2. **The approved look is an edit of an existing photo, not a new generation.** test2 = the test1 raw uploaded as the **ONLY** image_reference, with "keep everything exactly identical" wording. Every later still and video start frame comes from those test2 finals.
3. The prompts use a long "unretouched phone photo" skin block, warm olive tan wording, and soft or evenly lit light on the face, with no glam makeup words.
4. A light local finish (v4C: skin texture transfer at 0.5, sharpen 0.3, grain sigma 3) and no heavy de-gloss.
5. Video = **Kling 3.0 + an Element built from 3 approved test2 finals + an approved test2 still as the start frame**, low motion, sound off. The start still sets the face.

## 1. Base tool and model
- Higgsfield MCP (`user-Higgsfield`), `generate_image` (or `generate_image_batch` with a literal `requests` array of `{index, params}`), model **`seedream_v5_pro`**.
- Params used every time: `"aspect_ratio": "3:4"`, `"resolution": "2k"`, `medias: [{value: <media_id>, role: "image_references"}]` (photo 1, photo 2, ... in that order). Output is 1760x2352 PNG.
- Cost: **2.5 credits per image** (preflight exact). NSFW-blocked jobs are refunded (2026-10-17 X video4 note); check `transactions`.
- Upload: `media_upload` -> curl PUT to the presigned URL with headers `Content-Type` **and `If-None-Match: *`** -> `media_confirm` (media_ids list, one call per type). A PUT can return a transient 520: retry the same URL. Media ids stay valid across calls.
- Literal test1 job (valentina_test1/batch.json): `{"model": "seedream_v5_pro", "prompt": "...", "aspect_ratio": "3:4", "resolution": "2k", "medias": [{"value": "9158ed82-73ef-4b48-9f3d-a113e3fd26e8", "role": "image_references"}, {"value": "df822677-147c-40ad-b770-c96bbae1e0aa", "role": "image_references"}]}` (9158ed82 = cover, df822677 = bikini1).

## 2. Reference images
### 2a. Original pack (identity_packs.json `valentina`)
- face_refs: valentina_refs/valentina_bikini1.jpg (1197x1600), valentina_bikini2.jpg (1197x1600), valentina_cover.jpg (1024x1024), valentina_talking1_frame.jpg (720x1280), valentina_lingerie_v2_1.jpg, valentina_lingerie_v2_4.jpg (896x1184)
- body_refs: bikini1, bikini2, lingerie_v2_1
- signature_traits: "dark brown/near-black long wavy hair, dark brown eyes, warm olive-tan skin, bright wide smile"
- approved_look: "test2 (bust slightly larger/perkier), Samuel approved 2026-10-14: /workspace/hf-test/zen/posting/valentina_test2/"
- valentina_tattoo_C_olive.jpg is from the dropped tattoo experiment. **Do not use it** (pack restored to pre-tattoo).
- Pack caveat: `"status": "DRAFTED_UNAPPROVED"` and the body spec was never written. The look Samuel approved is test2.

### 2b. Generation refs and why they were chosen
- **test1 / batch1 / batch2: photo 1 = valentina_cover.jpg (face, media 9158ed82), photo 2 = valentina_bikini1.jpg (body, media df822677).** cover is the front-facing face. bikini1 shows the body proportions.
- bikini2 was tried as a third ref (test1 s3 beach, batch2 retry). It did not fix thin legs or the expression gate.
- **test2 (the approved standard):** the test1 raw itself was the **only** image_reference (no face or body refs). Uploads: valentina_test2/up/{s1_a,s2_b,s4_a,s5_a,s6_a,s7_a,s8_a}.jpg (1760x2352).
- **Approved finals, used as refs and start frames from then on:** valentina_test2/fin/{s1_a,s2_b,s4_a,s5_a,s6_a,s7_a,s8_a}_v4C.jpg (1080x1443). Sheet: valentina_test2_contact_sheet.jpg.
- Later stills (TikTok Oct 19): single-ref edits of test2 finals s2_b (balcony), s6_a (park) and s8_a (kitchen), uploaded as valentina_tiktok_oct19/up/v_s2_b.jpg, v_s6_a.jpg and v_s8_a.jpg.
- Pitfall: every original ref is a wide smile, so the pack works like a "smile pack". Non-smiling faces drift and fail the gate (see section 9).

## 3. Prompts (verbatim)
### 3a. test1 base generation (valentina_test1/prompts.py). Prompt = scene + " " + FREEZE
FREEZE:
> Take the face exactly from photo 1: same facial structure, dark brown eyes, nose, lips, wide smile, jaw, brows and long dark wavy hair as photo 1. Body proportions as in photo 2: slim toned hourglass figure, defined waist, rounded hips, slim toned legs, warm olive tan skin. Candid unedited iPhone 26mm photo, face fully in frame with headroom above the head, matte unretouched skin with visible pores, mild natural asymmetry, light natural tan, minimal makeup, phone noise, not glossy, no text, no other people, empty background.

Example scenes:
- s1: "New scene: she sits at a small cafe table by a window with a coffee cup, wearing a plain white tee and light jeans, front angle, relaxed wide smile, waist-up."
- s2: "New scene: she stands on an apartment balcony in morning light, wearing a plain fitted grey tank top and jeans, 3/4 angle, looking at camera with a wide smile, head to hips visible." (The retry used front angle with square shoulders.)
- s4: "New scene: she stands in a living room, wearing a plain black t-shirt tucked into blue jeans, front angle, shoulders square to camera, wide smile, head to knees visible."
- s6: "...quiet park path under trees wearing a plain olive sundress, 3/4 angle, wide smile, head to knees visible."
- s8: "...stands in a kitchen leaning on the counter wearing a plain white fitted tee and denim shorts, front angle, wide smile, head to mid-thigh visible."

### 3b. test2 edit = THE APPROVED LOOK (single image_reference = the test1 raw)
> Edit this exact photo: keep everything exactly identical (face, hair, outfit, background, pose, framing, lighting, skin tone and texture); only make the bust slightly larger and perkier / more lifted, natural proportions, same neckline and same clothing.

Samuel, 2026-10-14: "approved test2 look (slightly larger/perkier bust via Seedream edit, all else unchanged, v4C only). Use this face and body as the standard."

### 3c. batch1/batch2 fresh 2-ref wording (cover + bikini1, "photo 1/photo 2")
- Bust: "slightly larger, fuller and perkier, naturally lifted bust than photo 2, clearly not flat or skinny"
- Tan: "warm olive tan like photo 2, NOT pale, NOT desaturated, even indoors". This fixed pale indoor skin.
- Light: Madison's "warm backlit golden-hour sun, slight haze, low contrast" (no blown highlights), plus the long unretouched skin block, scoop-neck or fitted tops, v4C only, no v5.
- Long skin block, as used across the team: "raw unretouched amateur phone photo, no beauty filter/smoothing/airbrushing, visible pores, fine lines, redness, blemishes, freckles, uneven tone, mild shine only on nose/forehead, no studio light, flat ordinary light, phone noise/softness". The exact batch1 string is in valentina_batch1/prompts.py.
- batch2 expression line: "take identity from photo 1 ... IGNORE the expression in photo 1", plus ONE named expression per scene.

### 3d. Current single-ref edit TAIL (valentina_tiktok_oct19/prompts.txt), appended to each edit
> Keep her face exactly identical to the photo: same round-oval face with soft full cheeks (not slim, not sharp, not angular), same eyes, brows, nose and lips, same dark-brown wavy hair worn down loose (no ponytail). Keep the same body proportions and the same bust size and shape as the photo, modest. No tattoos. Soft closed-mouth smile, lips together, eyes fully open looking into the camera. No other people anywhere in frame. Unretouched natural skin with fine pores, light natural skin texture, dry matte skin, no shine, no sheen, no glow, no highlighter, no airbrushing. Realistic phone photo.

Scene heads:
- tt1 (s2_b balcony): "Edit this exact photo: same woman, same balcony and pose and framing. Change her outfit to a fitted black going-out mini dress with a modest square neckline and thin straps, small gold hoop earrings, and the light to warm golden-hour Miami sunset with palm trees and city in the background."
  - This sunset version FAILED (narrower face, more cleavage). The fix that worked: "same soft daylight on her face, evenly lit from the front" + "wide cheekbones, short soft chin, not gaunt" + a high scoop neck. Make 2 variants and keep the rounder face.
- tt2 (s6_a park): "Edit this exact photo: same woman, same pose and framing. Change her outfit to a white linen button-front sundress with a modest neckline and a small woven straw bag on her shoulder, and change the setting to a sunny empty Miami sidewalk with palm trees and pastel art-deco buildings, bright daylight."
- tt3 (s8_a kitchen): "Edit this exact photo: same woman, same kitchen, same pose and framing, hands resting on the counter. Change her outfit to a soft pale-pink ribbed lounge tank top and matching shorts, morning light, and add a small white espresso cup with a saucer on the counter in front of her."

### 3e. "Natural_v4" light+skin edit (the Valentina natural-face recipe applied to Camille; camille_oct16/natural_v4/work/prompt.txt). Single-ref, 2k, 2.5 cr
> Edit this exact photo: keep everything identical (same woman, same face, same expression, same head angle and gaze, same hair, same outfit, same pose, same body and body proportions, same bust size, same background, same framing). Change only the light and the skin: warm backlit golden-hour sun, slight haze, low contrast, soft diffused light on her face; natural unretouched skin with visible fine pores and faint light freckles, dry matte skin, no shine, no specular highlights, no glow, no highlighter, no airbrushing, no beauty-filter smoothing; lips soft satin, not glossy. Candid phone photo look, not a studio shot.

Result: 8/8 completed first try. Shine gone, pores and freckles visible, body unchanged. insightface scores drop about .02-.09 when highlights are removed, but the faces still read as the same woman by eye. Finish = Valentina finish_v4C.py with P repointed (camille_oct16/natural_v4/work/finish_v4C.py).

### 3f. Video start-still wording (X video4 v2, the "cafe-clip recipe")
Seedream with 3 refs (cover + bikini1 + test2 s2_b), "round-oval face with soft full cheeks (not slim, not sharp, not angular)", relaxed brows, closed-mouth smirk, black scoop cami, head-to-chest framing so the arms are out of frame, then a 9:16 centre crop.

## 4. Finishing: v4C (valentina_test2/finish_v4C.py)
Run: `python3 valentina_test2/finish_v4C.py s1_a s2_b ...`. It reads `P+'raw/<name>.png'` and writes `P+'fin/<name>_v4C.jpg'`, with P = /workspace/hf-test/zen/posting/valentina_test2/ (repoint P for other folders).
1. Texture source: `python3 /workspace/hf-test/posting_oct14/v3/raw/skin_local.py raw.png raw_tex.png`
   - YCrCb skin mask (Cr 135-180, Cb 80-130, Y>60), blur 6
   - highlight tame `a - clip((Y-200)/55,0,1)*mask*14`
   - noise texture `n1*0.18 + n2*0.10` (normal*40, blurs 0.9 and 4, seed 7), weighted `0.6+0.4*Y/255`
2. Resize to **W=1080** (LANCZOS, height proportional, giving 1080x1443 from 3:4).
3. Skin mask: same YCrCb thresholds, blur 5. Edge protection: `e=|Y-blur(Y,2)|`, blur 3, `prot=clip(1-(e-4)/6,0,1)`.
4. Texture transfer: `hp = clip(Yt - blur(Yt,1.6), -6, 6)`, `lo = clip(blur(Yt,6)-blur(Y,6), -8, 4)`, `b = a + (hp + lo*0.5)*mask*0.5`. **Texture strength 0.5.**
5. **Sharpen 0.3** (unsharp: `a + (a - blur(a,1.0))*0.3`).
6. **Grain:** normal sigma **3.0**, blurred 0.4, luma, seed = image index.
7. Save JPEG **quality 90, subsampling 0**, optimize. PIL writes no metadata.
- The gate drop from v4C is about 0.00-0.02 centroid.
- Freckle caveat (Madison, Oct 19): the 0.5 texture amplifies freckles on small faces. madison_oct19/work/finish_v4Clite.py uses texture 0.15. Do not use finish_v5 (Samuel rejected it as "less tan, uglier").

## 5. Crop, face size, resolution, aspect
- Generation: 3:4, 2k (1760x2352). Finals: 1080x1443 JPEG.
- Framing: "face fully in frame with headroom above the head". Mid framings (waist-up, head-to-hips, head to mid-thigh/knees) hold identity best.
- Close, face-large shots drift. In test2 the cafe close-up (largest face) failed the gate 3 times (0.757-0.774) even though it looks identical by eye. "for bust tweaks ... best on mid-framing shots, avoid close face-large shots."
- Use shorts and mid-thigh framing rather than leggings or long-leg crops (thigh proxy). Keep hair down, no ponytail.
- Video start: 9:16 crop if an arm sits only partly at the edge (car v2: crop x 268-1080 of the 1080x1443 still, upscaled to 720x1280). Kling output is 828x1108.
- Delivery canvas (fin.sh): blurred 1080x1920 background with the clip scaled to 1080 wide and centred, not cover-cropped.

## 6. Video: Kling 3.0 + Element (best route; Samuel PASSED it Oct 19 4:17 AM EDT)
- **Element "Valentina-matte-test" id `0950a489-6b07-4db6-b0a9-95e83e4be628`**, built from 3 approved test2 finals:
  1. valentina_test2/fin/s1_a_v4C.jpg: cafe, 3/4 face
  2. valentina_test2/fin/s2_b_v4C.jpg: balcony, waist-up
  3. valentina_test2/fin/s4_a_v4C.jpg: living room, full body
  - Steps: media_upload -> PUT -> media_confirm -> `manage_reference_elements` create. It is instant and costs nothing. If the next submit returns 400 "Reference element is not ready", resubmit a few seconds later (no charge).
- Generate: model **`kling3_0`**, `start_image` = an approved test2 still used as is (test clip: **s4_a**, not regenerated), **`<<<0950a489-6b07-4db6-b0a9-95e83e4be628>>>`** in the prompt, **5 s, 720p**, mode std. 3:4 is coerced to 9:16, giving 828x1108.
- **Sound "off"** costs 7.5 cr per 5 s (1.5 cr/s; 8 s = 12, 10 s = 15). Sound on costs 10. The first Valentina test was 10 cr (default sound, audio stripped) on job 8cb7b1f6-7a60-4ba9-91ef-1f1ef601c866, ~8 min render. The TikTok Oct 19 clips were 7.5 each.
- Always run get_cost first. The "IN THE DARK" preset notice comes up almost every time: resubmit with `declined_preset_id` (free).
- **Start-still rules:**
  - Use an approved test2 final, or a single-ref edit of one that has passed its own side-by-side.
  - Light on the face should be even and from the front. No sunset or side light (it narrows the face).
  - Use a high or modest scoop neckline (Seedance and Seedream moderation also block cleavage starts).
  - Keep arms out of frame or fully visible. Never leave a sliver of arm at the edge.
  - No tattoo.
  - Closed-mouth soft smile: Kling drifts to that expression anyway.
  - Gate the still before spending on video. "Identity in video is set by the start still."
- **Prompt:** the exact string for the Valentina Element test was **not saved** in its folder or the job record. Recipe lines on file:
  - Default line (Valentina TikTok Oct 19): "looking straight into the camera from the very first frame to the last; does not look down at the cup, does not lower her head"
  - Camille recipe step 4: "describe only low motion (small head turn, soft smile, slow breath), static camera, relaxed arms down, still torso; do not describe the face or body (the Element and start frame carry them). Add 'skin stays dry and matte for the whole clip'."
  - Full template used with this method on Sienna (valentina_method/prompt_storyA.txt): "<<<ELEMENT>>> on an empty sunny beach, phone selfie framing exactly as in the first frame. Small natural motion only: slow breath, a soft relaxed smile, ... a very slight natural head tilt. She keeps looking straight into the camera from the very first frame to the last; eyes stay open and relaxed with quick natural blinks only; she does not look down and does not turn her head. Keep the face identical to the first frame. Skin stays dry and matte for the whole clip: no shine, no glow, no beauty filter, no smoothing. Camera almost still with slight handheld phone drift, no zoom. Small waves roll in behind her. No other people, no text, no speech."
  - Charlotte (same method) adds "Camera locked, no zoom. No speech, silent."
- Result: body, bust, shoulders and hair held across 6 frames. The face is recognisable, but the broad smile closes to a soft smile and the face reads slightly narrower and smoother. With this method on Sienna, face and body held for 8 s (per-frame gate 8/10).
- Finish (valentina_tiktok_oct19/fin.sh): blurred canvas `boxblur=30:2, eq=brightness=-0.08`, clip `scale=1080:-2` centred, drawtext hook 0-2.5 s and payoff after (DejaVuSans-Bold 64, borderw 5, y=300), `noise=alls=5:allf=t`, silent AAC 64k track (anullsrc), libx264 crf 20 preset slow at 30 fps, `-map_metadata -1 -fflags +bitexact -movflags +faststart`. (`-metadata:s -1` errors in this ffmpeg.)
- Not recommended for Valentina: Seedance 2.0 i2v and multi-ref video (narrower or longer face, heavier brows, bigger bust). Tattoo in video: dropped.

## 7. QC
- **HARD GATE (Samuel, Oct 18):** identity_gate score alone does not count. Put 4-6 stills or frames next to the approved refs (valentina_test2/fin/*, the test2 contact sheet, cover, bikini1/2) in a contact sheet and LOOK at face (jaw/cheek width, eyes, nose, lips) AND body (bust, proportions). Recheck mid and late frames, because drift grows over a clip.
- **Side-by-side sheet (valentina_tiktok_oct19/qc.sh `<n> <test2 base>`):**
  - Frames at 0.1, 1, 2, 3, 4, 4.9 s plus a mid frame at 2.5 s from the final.
  - Top row: test2 base still, s1_a_v4C, s4_a_v4C, cover, bikini1, the new start still.
  - Bottom row: the 6 frames. Each tile is 360x480.
  - Output: qc/<n>_qc.jpg, with face crops in qc/<n>_face.jpg. FAIL sheets are kept as *_try1_qc_FAIL.jpg.
- Kling test sheets: valentina_kling_element_test/kling_element_sidebyside.jpg and face_closeup.jpg (f0-f5.png).
- **Still gate:** identity_gate.py `--source seedream --body`, cut 0.78 centroid (/workspace/.face-venv/bin/python; system python lacks cv2). Treat ±0.01 around 0.78 as borderline.
- **Drift metric (/workspace/music/sienna/low_tide_lover/sample/valentina_method/qa/drift.py `video step tmax out.json`):**
  - insightface buffalo_l reports, per step (default 0.5 s): cosine to the pack centroid, face height / frame height, and Laplacian variance of the face crop resized to 256 wide.
  - Kling Element clips stay flat. Wan singing faces lose about 30% detail by 3 s.
  - The script loads the `sienna` pack: change the key for your model.
- Eye check: insightface landmark_2d_106 eye aspect every 3rd frame. A value under ~0.22 means closed; 4 or more low samples in a row is a closed-eye moment (camille_oct19/work/eyes.py).
- Also run the peer review checklist, and check valentina_posted_log.json plus Ayrshare history for repeats.

## 8. What Valentina's pipeline does differently
- No Soul. Seedream reference edits only.
- The approved identity is a **single-image "edit this exact photo" pass** over a raw, so face, skin and light are preserved, not regenerated. New content is single-ref edits of approved finals, not fresh multi-ref generations.
- Face wording asks for a **round-oval face, soft full cheeks, wide cheekbones, short soft chin, not gaunt or angular**. Light on the face is even, from the front, soft daylight.
- Warm olive tan wording "NOT pale, NOT desaturated, even indoors".
- Modest bust (test2 "slightly larger/perkier, natural proportions") with modest necklines.
- Gentle v4C finish only (no v5, no heavy de-gloss).
- Video: Kling Element from 3 test2 finals plus an unregenerated approved start still, sound off, low motion, eyes on camera.

## 9. Known failure modes
- Expression-biased pack: refs are all wide smiles, so neutral, laugh, squint, tongue and look-away faces fail the gate (batch2: 0/8, centroid 0.56-0.76). Subtle smirk or soft smile holds best.
- Ponytail changes her face enough to fail the gate. Keep hair down.
- Leggings and long-leg crops trip the thigh proxy, and beach or one-piece shots came out with thin legs. Seated or 3/4 crops give proxy false flags.
- Slim outfits (balcony tank, one-piece, sundress) drift to a small bust in fresh generations. Deep scoop plus "fuller bust" wording gives too much cleavage: use "modest crew/high scoop neckline" and drop "fuller bust" when the top is fitted.
- Sunset, side light or golden-hour backlight on the face narrows the face and adds cleavage (tt1 FAIL).
- Single-image edit with "playful raised eyebrow" gave a furrowed brow. Fixed with "relax eyebrows, closed-lip smirk".
- Kling: eyes close or lower when a cup is in frame (use the eyes-on-camera line). Closed-mouth faces read narrower and the hair renders darker. There is an opening blink, and sometimes the eyes close near the end (trim).
- Seedance and video generally: narrower or longer face, hollow cheeks, heavier brows, bigger bust. A partial arm at the frame edge gets turned into a camo or tattoo-like patch: crop it out.
- Moderation: bikini or cleavage start frames are blocked ("bare midriff/minimal fabric/tiny" wording).
- Busy public places leak background people despite "nobody" wording. Use empty scenes.
- Gate scores are inflated when refs equal gate refs, so a high score does not mean approved. Samuel's eye is final.

## Sources
SHARED_LEARNINGS.md (Valentina entries Oct 14-19, Kling recipe, valentina_method/drift notes); identity_packs.json[valentina]; valentina_refs/; valentina_test1/prompts.py + batch.json; valentina_test2/{finish_v4C.py,up,raw,fin,gate_fin.json}; camille_oct16/natural_v4/work/prompt.txt; /workspace/hf-test/posting_oct14/v3/raw/skin_local.py; valentina_kling_element_test/; valentina_tiktok_oct19/{prompts.txt,fin.sh,qc.sh,qc}; /workspace/music/sienna/low_tide_lover/sample/valentina_method/{prompt_storyA.txt,jobs.txt,qa/drift.py}; jsw-daily-content-process/SKILL.md (peer review pairs).
