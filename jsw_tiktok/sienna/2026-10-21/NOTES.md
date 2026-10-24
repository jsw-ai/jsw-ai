# Sienna Wed 2026-10-21: "Low Tide Lover" drop TikTok (REVIEW ONLY. Not posted or scheduled.)
Final: /workspace/jsw_tiktok/sienna/sienna_wed_low_tide_lover_drop.mp4. It is 13.46 s, 1080x1920, 24 fps, H.264 Main, yuv420p, AAC 48 kHz stereo, +faststart (moov at byte 36), 9.79 MB. No burned-in text.

## Structure
- 0.00-6.95 s: she sings the hook, kneeling on the sand at golden hour in a terracotta triangle bikini. Audio is the full mix from 33.10 to 40.05 s ("Oh, you're a low tide lover / Only show up when the water's gone"). The cut lands before "Leave" starts at 40.08.
- 6.95-13.46 s: the bit. She holds her phone, bites her thumbnail nervously, checks the screen, then bursts out laughing at the camera (jump cut at 10.70 s). Audio is the instrumental stem (no_vocals) from 40.05 s, with a 40 ms crossfade and a 0.55 s fade-out.

## Stills (seedream_v5_pro, 9:16 2k, refs story2_a_v4C + story1_a_v4C, media 2969a422 / 5abc094e; finish_v4C.py with P repointed)
- Prompts: pA.txt/pB.txt + tail.txt (the first try was too wide), then pA2_full/pB2_full (chest-up), then pB3_full (single-ref edit of sA2_b that adds the phone).
- The face wording follows the Reviewer's note, not the old doc's "round-oval/soft full cheeks" wording: "slim oval face, defined high cheekbones, slim cheeks, defined slightly angular jaw ... light freckles". Light: low sun behind the camera, even front light on her face.
- Gate (identity_gate img --source seedream --body, 0.78 cut): sA_* 0.751-0.804, sB_* fail, sA2_b **0.793 PASS** (sing start), sA2_c 0.786, sB2_c 0.780 (FAIL flag), sB3_* 0.729-0.778 (fail).
- Bit start sB5_d = the sA2_b head (pixel-identical) with the body/phone/hand region below the chin taken from sB3_d (similarity-aligned, feathered). Gate **0.791 PASS**. (sB4_d, the reverse paste, scored 0.776, so it was rejected.)

## Video (kling3_0 pro, sound off, 9:16, Element Sienna-v2-1020 2603afeb)
- Sing: kA.txt, 8 s, kA_a (USED, short blinks only) / kA_b (rejected: eyes closed 0.1-1.2 s).
- Bit v1 kB.txt 6 s x3: no real nail bite. kB_b's laugh, 3.2-6.0 s (phone stays in hand), is USED as the last shot.
- Bit v2 kB2.txt 6 s x3: kB2_b USED for 0.5-4.25 s (clear thumbnail bite, then looks at the phone). It is cut at 4.25 because the phone melts into her hand at around 4.4-4.7 s. kB2_a: the phone flips to show a fake call UI. kB2_c: she holds a bitten-off "nail" fragment (gross).
- Lip-sync: sync_so cut_off on kA_a 0-7.25 s (ed/sing_base.mp4, media 95e96745). sync_a/sync_b used the raw stem (aud/vocal_sing.mp3); sync_c USED the compressed and loudnormed stem (up/vocal_sing_comp.mp3).

## QC (/workspace/review/sienna_oct21/)
- Identity (drift.py, every 0.5 s): sing 0.62-0.79 (mean ~0.70), bit 0.55-0.75 (lowest on the big laugh frames and while looking down at the phone).
- Sync (qa/sync.py vs the stem, sung section): lip 0.09 / jaw 0.17 at zero lag, best 0.24 / 0.29. WEAK. The mouth moves on the words but stays small and smiley, and "Oh" barely opens (mouth_words.jpg).
- Eyes: blinks only while singing. Lids drop at 9.8-10.6 s because she is looking down at the phone (scripted).
- Hands: hands_bit.jpg, kB2_b_hands*.jpg. Five fingers, no melting in the used ranges.
- Freckles: faint (zoom100_face_*.jpg). Fewer than on the refs; the video re-render smooths them.

## Credits (from Higgsfield transactions; the balance is shared with other agents running at the same time, so this counts my jobs only)
Seedream 20 x 2.5 = 50.00; Kling 8 s pro x2 = 2 x 14 = 28.00; Kling 6 s pro x6 = 6 x 10.5 = 63.00; Sync Lipsync 3 x3 = 3 x 26.1 = 78.30. **Total 219.30 cr.**
The balance ran out (6.42 cr left at ~1:12 PM EDT), so a planned re-take of the singing shot with stronger mouth shapes (kA2.txt) could NOT be submitted.
