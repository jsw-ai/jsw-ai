# Camille: Friday Oct 16 batch (built Thu Oct 15 ~01:00-01:35 ET). NOTHING POSTED OR SENT; Samuel reviews first.
Captions, hashtags, platforms, order, X texts and the ZenCreator request spec: **CAPTIONS_AND_PLAN.md**.

## Files
| File | What |
|---|---|
| stills/camille_s1..s10.jpg, raw/s1..s10.png | 10 new stills (Seedream 5.0 Pro ref-edit, 3:4 2k). contact_sheet_stills.jpg has an expression/angle/eye label per photo |
| lip1_pier_flirting_with_sunsets.mp4 | Seedance 2.0 lip-sync, 1080x1920 H.264/AAC, 8s. Start = s10 (pier, cardigan) |
| lip2_window_not_staring.mp4 | Seedance 2.0 lip-sync, 8s. Start = s7 (window, white tank + cardigan) |
| dance_beach_nobody_is_watching.mp4 | Seedance 2.0 image-to-video, no audio ref, 8s, start = s8 (full-body twirl); synth music added |
| montage1_tell_me_im_not_the_only_one.mp4 | 6 distinct stills (s2,s1,s3,s6,s5,s4), 14.4s, 100 bpm synth track, burned-in captions, hook at 0s |
| montage2_getting_ready_last_light.mp4 | 6 distinct stills (s7,s9,fb2,s10,fb3,s8), 12.9s, 112 bpm synth track. fb2/fb3 = camille_fullbody shots Samuel already saw |
| contact_sheet_videos.jpg | 3 frames per video (0.8s, 3.2s, 6.0s) |
| video/raw/*.mp4, video/start/, video/camille_voice*.mp3 | untouched Seedance outputs, 9:16 start frames, voice copies |
| music/*.wav | two original synthesized tracks (numpy; golden_hour_pop 100bpm, evening_drive 112bpm) |
| refs/ | the 3 refs fed to Seedream (face_front, face_three_quarter_matte, body_waistup) |
| work/ | prompts.py (all still prompts), cos.py, asr.py, voice.py, finish.py, build_montages.py, check strips |

## Method
Stills: Seedream 5.0 Pro, 3 refs (photo 1 = face_front, photo 2 = face_three_quarter_matte, photo 3 = body_waistup), "take identity from photos 1 and 2, IGNORE their expression", body wording from the r3_4 line (slim toned hourglass, moderate-to-full proportionate bust, not skinny/heavy), round-3 beauty wording (striking, symmetrical, cheekbones, full lips, large bright eyes, long lashes, soft makeup), "matte natural skin finish, even healthy tone, light freckles, no oily shine/glow/highlighter", NO imperfection words (no pores/blemish/redness), warm soft low-contrast golden hour, empty backgrounds, one named expression + head angle + eye direction (gaze off-camera) each, scoop-neck fitted tops, no bikinis.
Videos: Seedance 2.0, 9:16, 720p, 8s, audio on, start_image = still cropped to 9:16, camille.mp3 re-imported per clip as audio_references, prompt names "light French accent", line <=9 words, "begins speaking immediately in the first second ... finishes by about 4.5 seconds". Finish: upscale 1080x1920, mild unsharp + light grain, burned-in captions, synth music at 14% under speech, crf 22, metadata stripped.

## Voice (camille.mp3, checked without listening)
ffprobe: mp3, 44.1 kHz stereo, 8.10 s. Whisper: auto-detects English (0.90), transcript "Everyone tells you Paris is so romantic. Let me be the one to ruin it for you." Forcing French makes whisper output a fluent French rendering, so I can't tell accent from ASR alone. Median f0 205 Hz. The persona config + MANIFEST label her "French-coded"; the prompt asks for English with a light French accent. **UNCERTAIN: I cannot hear the audio, so whether her accent is light Parisian French or something else is inferred, not verified. Samuel/JSW AI should listen to lip1/lip2 against camille.mp3.**

## Checks (what was machine-checked vs eye-only)
| Item | Result |
|---|---|
| lip1 transcript | whisper small, exact: "Tell me I'm not the only one flirting with sunsets." speech 0.7-4.0 s, no dropped words (also on the finished mix) |
| lip1 voice | median f0 190 Hz vs ref 205 Hz (same ballpark; crude); mouth vs speech by eye on 8 frames |
| lip1 identity gate (camille_v3_draft pack, video) | PASS 8/8 frames, min centroid 0.69 |
| lip2 transcript | exact: "Tell me you're not staring. I won't tell anyone." speech 0.8-4.0 s |
| lip2 voice | f0 195 Hz vs 205 Hz |
| lip2 identity gate | PASS 8/8, min centroid 0.73 |
| dance | **EYE-ONLY**. Gate FAILED (0.125 frames pass: face tiny + back to camera during twirl, no_face_detected). Visually same woman, same dress/body (slim hourglass), no frozen background people, no artifacts seen in 8 frames; face is small in frame |
| montage1/2 | **EYE-ONLY** (stills are the checked units). Captions read, no AI wording, no repeated photo (no loop-back tail either), no people |
| stills s1..s10 | Gate not calibrated for the v3 pack (angled/off-camera faces): insightface cosine vs r3_4 / face_front / tq_matte: s1 .65/.66/.74, s2 .66/.66/.65, s3 .63/.63/.70, s4 .77/.77/.79, s5 .63/.62/.58, s6 .68/.68/.74, s7 .79/.80/.74, s8 .43 (face 9% of frame, tiny), s9 .76/.76/.81, s10 .70/.72/.83. Same pattern as the camille_fullbody batch (0.58-0.67) so **all stills are eye-checked for identity**: 9/10 clearly read as the same curly-haired woman; s8 is a distant full-body shot (identity by hair/skin/body only). Body: slim toned hourglass in all, bust moderate-to-full; s3 (cream tee) bust looks a bit smaller than s2/s7. No text in any still. No background people |
| No AI wording | on-screen text and spoken lines read through: clean |

## What looked off / honest quality notes
- Matte skin worked in the stills (much less glow than r3_4), but in the **videos the skin picks up more sheen**, especially lip2 (highlights on forehead/cheeks). lip1 is cleaner (open shade).
- lip2's white tank is cleavage-forward in motion (still passed Seedance with no nsfw flag). Keep to IG/TikTok/X; not Shorts/Reddit/Facebook.
- s9 shows her seated on a bed with bare thighs (black short top-dress): used in montage2 only; keep off FB/Shorts/Reddit.
- s9 uses her phone instead of the requested compact mirror (Seedream swapped it). Fine for "getting ready".
- lip1 camera reframes (zooms) a bit from the start frame; hair/face consistent. Both clips hold a smile/smirk after the line ends (~4 s).
- dance: spin passes through a back-to-camera moment; face small; caption sits over the dress.
- Montage crops: 3:4 -> 9:16 crop cuts side edges (s2 loses part of the railing, s6 is face-large). Caption on slide 6 of montage1 sits on a dark street (readable, slightly low contrast).
- Closest duplicate-ish expressions: s9 and s10 (both head-down), both only in montage2.
- No failed generations, no NSFW blocks, no retries needed on stills or video. fb2 (cafe wall) shows a car and empty tables in the window reflection: harmless.
- Nothing is marked "failed". The only gate failure is the dance video's face gate (small/back-turned face), judged by eye.

## Credits (actual, from Higgsfield transactions list + balance)
- 10 x Seedream 5.0 Pro @ 2.5 = **25**
- 3 x Seedance 2.0 720p 8s @ 36 (preflight said 36 exact) = **108**
- Montages/finishing/music: 0
- **Total 133 credits** (balance 1265.3 -> 1132.3, no other agent spending in the window). Staggered: stills in two batches of 5, lip1 + dance, then lip2 only after lip1 passed transcript/gate checks. Under the ~200 budget (67 left).
- Retrying a lip clip would be +36.

## Best 5 picks
1. lip1_pier_flirting_with_sunsets.mp4 (clean skin, exact transcript, gate 8/8, tells the bit)
2. dance_beach_nobody_is_watching.mp4 (best motion/likeness-in-motion, hair + skirt natural)
3. montage1_tell_me_im_not_the_only_one.mp4 (six clearly different expressions, hook at 0s)
4. stills/camille_s4.jpg (over-shoulder smirk, best face match .77-.79, blue-hour city)
5. stills/camille_s2.jpg (big laugh at the sea, strongest golden-hour shot)
Runners-up: s7 (cheeky smirk window), lip2.
