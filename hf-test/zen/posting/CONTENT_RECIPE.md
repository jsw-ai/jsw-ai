> Notion is the source of truth: https://app.notion.com/p/400f29949b29810fbe39cbcde5d3d9f4. If this file conflicts, Notion wins.

# Sienna Blake — Standard content recipe (SFW social: TikTok / IG / X / Reddit)
Every still and clip is made this way. If you deviate, note it in her Notion SOP.

## 1. Identity (face AND body)
- **Soul (Higgsfield `soul_2`):** `Sienna Blake Body v1` = `50583a87-b62e-4933-b601-5dad8072f30f` (trained Oct 14 on 15 approved face+body keepers) — **not approved yet**: body matches keepers but all 3 test stills cropped her head off, so face is untested. Until a face-in-frame test passes, use the fallback. Fallback: `Sienna Blake` `ba97f512-0ed0-4c56-9480-5abe167b06d1`. Old `f9700355…` is gone — never use it.
- Training set for Body v1: keepers/sienna_bikini1, bikini2, cover, face_keeper, face_close; zen/sienna_lingerie_v4_2/3/4; posting_oct14/v3/x2_dawn_v3 + _alt; sienna_candid, sienna_cafe_face; posting_oct14/v4/story1_a/story2_a/story3_b_v4C.
- Paste the body spec line (zen/posting/sienna_body_spec.md) into every body-visible prompt:
  > Same figure as reference: full natural rounded C-cup bust (clearly fills the top, visible cleavage), slim toned waist, flat stomach with light ab definition, curvy hips, slim athletic hourglass build, long toned legs, even golden tan.
- Pass `keepers/sienna_bikini1.png` as the single Soul 2 image reference when the body is in frame.
- Angles: front or 3/4 only. No rear / over-the-shoulder angles in swimwear (flattens the bust).

## 2. Still prompts (start frames and photo posts)
- Candid iPhone / phone-photo look: "Candid unedited iPhone photo, slightly off-centre and tilted framing, flat natural daylight, visible skin texture and pores, flyaway hairs, minimal makeup, ordinary clothes, natural asymmetry, not posed, not retouched, not glossy, not cinematic."
- Ordinary clothes (tee, linen shirt, tank, plain swimsuit). Off-centre framing. Flat natural light.
- **No background people** — plain/empty backgrounds (balcony, empty beach path, plain wall). Frozen extras look fake in video.
- Props: plain, no logos or text.

## 3. Clips (talking / TikTok / Reels) (updated 10/21 to match Hard Rules)
- Always image-to-video from a still that passed the identity gate (0.78) and the body check. Never text-to-video. Quote the cost first (`get_cost`) and log exact credits.
- **Silent clips:** Higgsfield `kling3_0` + her Kling Element (Sienna-v2-1020 `2603afeb-5f21-4acc-a3de-8904d5a32cb9`), gated still as `start_image`, sound off, low motion ("keep the same expression, natural blinks only, matte skin, no sheen, camera locked").
- **Lip-sync / talking:** Higgsfield `seedance_2_0` i2v, 9:16, gated still as `start_image`, `audio_references` = `/workspace/hf-test/voicerefs-from-sam/sienna.mp3`; check the line word for word with whisper.
- Run `identity_gate.py video --model sienna` across the whole clip (drift shows at 3-5 s) plus a same-scale side-by-side.
- Export: H.264 Main, yuv420p, faststart, under 15 MB, full 9:16; one cut per platform.

## 4. Reroll checks (every still and clip)
- **Face** vs `keepers/sienna_face_close.png` (side-by-side sheet).
- **Body check** vs `keepers/sienna_bikini1.png` / `bikini2.png`: bust size, waist, hips, tan, build must match. Check the start frame AND first/middle/last frames of the clip (body must not shrink or morph during motion). Fail → reroll or fix with a gpt_image_2 edit ("change only body proportions to match image 2") before animating.
- Garbled text / logos / signage; extra fingers; warped props; continuity (latte vs matcha etc. must match the caption/line).
- Speech: transcribe with faster-whisper (`/workspace/.whisper-venv`), must match the line word for word; voice must sound like the reference.
- No background people, no frozen extras.

## 5. Finishing (= option C from posting_oct14/v4/make_v4.py)
- Stills: 50% luminance-only skin texture, skin-masked (eyes/lips/hair edges protected), **NO blur**, mild sharpening (0.3), light grain, JPEG q90, metadata stripped.
- Clips: light luminance grain + mild sharpening, no blur, re-encode H.264/AAC, `-map_metadata -1`.
- **No blur ever** — Sam rejected the soft v3 look.

## 6. Rules (updated 10/21 to match Hard Rules)
- Retired: old glossy clips (e.g. `videos/sienna_talking1_web.mp4`) — never post.
- Never mention AI in post content (caption, hashtags, hook, spoken line, on-screen text). Platform AI labels/toggles are settings: leave them on where required.
- No Fanvue links/mentions or spicy content on TikTok, Instagram, YouTube, Facebook. Fanvue funnelling only from X (link in bio + hand-pinned post, never in scheduled/API posts) and Reddit profile.
- A **JSW Content Reviewer PASS** for the exact file (path + md5) and exact captions is the approval to post; Samuel does not review each file. Only the JSW Content Scheduler posts (Ayrshare).

## 7. Log
- Oct 14: Body v1 Soul trained (25 credits, queued ~45 min). Test stills (front swim, 3/4 swim, tee): body (bust, waist, hips, legs) matches bikini1/2 closely, tan a shade darker; ALL THREE cropped above the chin (no face). Next test: add "face fully in frame, head and shoulders visible with headroom, camera at eye level". Sheet: posting_oct14/v4/compare/bodysoul_test.jpg.
- Oct 14: Passing keepers/sienna_bikini1.png as the Soul 2 image ref with the old Soul overrode the scene (made bikini-beach shots instead of balcony/tank). Text body-spec line alone gave the right scene and a good body (T1src_f). Use the image ref only when the shot is swimwear anyway.
- Oct 14: TikTok 1 v4 = Seedance 2.0 i2v from body-checked start frame v4/raw/T1src_f.png → T1_lastaweek.mp4 / _b.mp4; body held through the clip.
- Oct 14 face test (bodysoul_facetest.jpg): with "face fully in frame, headroom, eye-level" all 3 kept the face. Same person (braids, blue eyes, nose and smile), but the face reads slightly broader and more weathered than face_close, with a deeper tan; the café shot is closest. Body matches bikini1/2; bust slightly fuller in tee/café. Body v1 OK for body-visible shots once Sam approves the face; always add the face-in-frame line.
