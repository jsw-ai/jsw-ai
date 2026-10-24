# REVIEW SUBMISSION: firstclass_whippan clip 1 (Sienna, 2026-10-22)

## Files
- `/workspace/jsw_tiktok/sienna/2026-10-22_daily/clip1/sienna_20261022_firstclass_whippan_v1_cutA_tiktok.mp4` md5 `b01847e1e81506d086d3bb921654c539` 2774984 bytes
- `/workspace/jsw_tiktok/sienna/2026-10-22_daily/clip1/sienna_20261022_firstclass_whippan_v1_cutB_instagram.mp4` md5 `b01847e1e81506d086d3bb921654c539` 2774984 bytes
- `/workspace/jsw_tiktok/sienna/2026-10-22_daily/clip1/sienna_20261022_firstclass_whippan_v1_cutC_shorts.mp4` md5 `b01847e1e81506d086d3bb921654c539` 2774984 bytes
- `/workspace/jsw_tiktok/sienna/2026-10-22_daily/clip1/sienna_20261022_firstclass_whippan_v1_cutD_facebook.mp4` md5 `b01847e1e81506d086d3bb921654c539` 2774984 bytes
- `/workspace/jsw_tiktok/sienna/2026-10-22_daily/clip1/sienna_20261022_firstclass_whippan_v1_cutE_x.mp4` md5 `b01847e1e81506d086d3bb921654c539` 2774984 bytes
- `/workspace/jsw_tiktok/sienna/2026-10-22_daily/clip1/sienna_20261022_firstclass_whippan_v1_thumb.jpg` md5 `d1e9930d912d332cc275a78c0d2d6afb` 189056 bytes
- `/workspace/jsw_tiktok/sienna/2026-10-22_daily/clip1/sienna_20261022_firstclass_whippan_v1_sidebyside.jpg` md5 `e8a80653c3d24eb501c513e39acc82da` 315495 bytes
(All five platform cuts are the same encode; byte-identical.)

## Spec (ffprobe)
H.264 Main, yuv420p, 1080x1920 (full 9:16, cover-crop from native 9:16 Kling 720x1276, no bars, no blur bands), 24 fps, 70 frames, 2.92 s, silent (no audio track), +faststart (moov before mdat), metadata stripped, 2.77 MB (<15 MB).

## Content / story
First-class suite day of her travel week: A = cream knit, sunglasses on head, smiling selfie at the window (Kling k2 0.45-1.80 s); whip-pan transition; B = same suite with the flat bed made up, white tank and champagne flute (Kling k5 0.00-0.92 s, slowed 1.5x by frame doubling). Transition used: **whip pan** (synthetic whip blur built from the edge frames). Check it against her last 3 transitions and the other models' transitions today in the Content Review Log before you pass it; I could not confirm that from here.

## Process statement
Valentina's process: stills = Seedream 5.0 Pro single-ref edits of approved v4C finals, finish_v4C.py, identity gate; start frames A_a_v4C.jpg (centroid 0.801 PASS) and B3_b_v4C.jpg (0.796 PASS), both checked by eye for her fuller bust and golden tan. Video = kling3_0 + Element Sienna-v2-1020 <<<2603afeb-5f21-4acc-a3de-8904d5a32cb9>>>, start_image = gated still, 5 s, 720p std, sound off, low motion, eyes on camera. No Seedance or lip-sync. Kling drift took the full clips below 0.78 after about 1-2 s (k2 median 0.77, k3 0.74, k4 0.77, k5 0.74), so only the windows where every frame scored at least 0.78 were kept. Gates were run one at a time, each only with 3 GB or more free.
Start-still paths: `/workspace/jsw_tiktok/sienna/2026-10-22_daily/fin/A_a_v4C.jpg`, `/workspace/jsw_tiktok/sienna/2026-10-22_daily/fin/B3_b_v4C.jpg`. Source clips: `/workspace/jsw_tiktok/sienna/2026-10-22_daily/kl/k2.mp4`, `/workspace/jsw_tiktok/sienna/2026-10-22_daily/kl/k5.mp4`.

## Per-frame identity gate on the final export (every frame, video bar 0.78)
Median 0.805, min 0.786, 64 face frames, 6 no-face (whip pan).
| t (s) | score | verdict |
|---|---|---|
| 0.00 | 0.8 | PASS |
| 0.04 | 0.807 | PASS |
| 0.08 | 0.799 | PASS |
| 0.12 | 0.796 | PASS |
| 0.17 | 0.791 | PASS |
| 0.21 | 0.79 | PASS |
| 0.25 | 0.795 | PASS |
| 0.29 | 0.797 | PASS |
| 0.33 | 0.795 | PASS |
| 0.38 | 0.786 | PASS |
| 0.42 | 0.799 | PASS |
| 0.46 | 0.796 | PASS |
| 0.50 | 0.803 | PASS |
| 0.54 | 0.816 | PASS |
| 0.58 | 0.815 | PASS |
| 0.62 | 0.805 | PASS |
| 0.67 | 0.814 | PASS |
| 0.71 | 0.811 | PASS |
| 0.75 | 0.805 | PASS |
| 0.79 | 0.803 | PASS |
| 0.83 | 0.808 | PASS |
| 0.88 | 0.797 | PASS |
| 0.92 | 0.802 | PASS |
| 0.96 | 0.802 | PASS |
| 1.00 | 0.798 | PASS |
| 1.04 | 0.805 | PASS |
| 1.08 | 0.807 | PASS |
| 1.12 | 0.801 | PASS |
| 1.17 | 0.815 | PASS |
| 1.21 | 0.812 | PASS |
| 1.25 | 0.808 | PASS |
| 1.29 | 0.813 | PASS |
| 1.33 | 0.809 | PASS |
| 1.38 | no face (whip-pan blur, transition frame) | PASS |
| 1.42 | no face (whip-pan blur, transition frame) | PASS |
| 1.46 | no face (whip-pan blur, transition frame) | PASS |
| 1.50 | no face (whip-pan blur, transition frame) | PASS |
| 1.54 | no face (whip-pan blur, transition frame) | PASS |
| 1.58 | no face (whip-pan blur, transition frame) | PASS |
| 1.62 | 0.805 | PASS |
| 1.67 | 0.807 | PASS |
| 1.71 | 0.807 | PASS |
| 1.75 | 0.794 | PASS |
| 1.79 | 0.799 | PASS |
| 1.83 | 0.798 | PASS |
| 1.88 | 0.804 | PASS |
| 1.92 | 0.805 | PASS |
| 1.96 | 0.807 | PASS |
| 2.00 | 0.804 | PASS |
| 2.04 | 0.805 | PASS |
| 2.08 | 0.805 | PASS |
| 2.12 | 0.807 | PASS |
| 2.17 | 0.796 | PASS |
| 2.21 | 0.795 | PASS |
| 2.25 | 0.793 | PASS |
| 2.29 | 0.804 | PASS |
| 2.33 | 0.805 | PASS |
| 2.38 | 0.815 | PASS |
| 2.42 | 0.816 | PASS |
| 2.46 | 0.815 | PASS |
| 2.50 | 0.811 | PASS |
| 2.54 | 0.811 | PASS |
| 2.58 | 0.81 | PASS |
| 2.62 | 0.812 | PASS |
| 2.67 | 0.809 | PASS |
| 2.71 | 0.808 | PASS |
| 2.75 | 0.812 | PASS |
| 2.79 | 0.805 | PASS |
| 2.83 | 0.806 | PASS |
| 2.88 | 0.803 | PASS |

## Captions
- TikTok: from my window seat to my suite in one blink ✈️🥂 #firstclass #travelvlog #surfergirl #flightmode
- Instagram Reel: Outfit change at 30,000 feet ✈️ Where should I land next? #firstclass #travelgram #beachgirl
- YouTube Short (title): First Class Glow Up in 1 Second ✈️ #shorts #firstclass #travel (thumbnail = sienna_20261022_firstclass_whippan_v1_thumb.jpg)
- Facebook: Window seat → suite mode. Next stop: somewhere with waves 🌊✈️
- X: Window seat or suite? I picked both 🥂 link in bio

## Credits
Kling clips today k1-k5: 37.5 (k2 and k5 used; k1, k3 and k4 are redos). Seedream stills A, B, B2 and B3: 30. Day total so far incl. the X stills: 120.0. Balance at 15:36 ET: 5738.88.
