# Review request (priority): Sienna Blake – 'Low Tide Lover' lyric video v3c
Album 'Salt in My Hair', track 2, live on Apple Music. Built 2026-10-22 14:55 EDT. NOT posted. Addresses the v3b fail.

## Files (H.264 Main, yuv420p, AAC LC 48 kHz, +faststart with moov at byte 36)
| file | md5 | bytes | spec |
|---|---|---|---|
| /workspace/jsw_tiktok/sienna/lyric_videos/02_low_tide_lover/sienna_low_tide_lover_hook_short_1080x1920_v3c.mp4 | 9fb32ce8064e3db8cafc0a291cfc995b | 9,338,743 (<15 MB) | 1080x1920, 24.0 s, 30 fps |
| /workspace/jsw_tiktok/sienna/lyric_videos/02_low_tide_lover/sienna_low_tide_lover_lyric_video_1920x1080_v3c.mp4 | 4650ac89e29be0abc9d44fb4f7256c43 | 92,815,711 | 1920x1080, 167.2 s, 30 fps |
| /workspace/jsw_tiktok/sienna/lyric_videos/02_low_tide_lover/sienna_low_tide_lover_v3c_thumb.jpg | 57cf4aef86ae419cd9b0b05a781bddf0 | | 1280x720, from bal_p (0.812) |
End card (both cuts, checked by eye): "Sienna Blake / 'Low Tide Lover' – out now on Apple Music".
Images: contact sheets /workspace/jsw_tiktok/sienna/lyric_videos/02_low_tide_lover/sienna_low_tide_lover_v3c_contact_sheet_full.jpg and /workspace/jsw_tiktok/sienna/lyric_videos/02_low_tide_lover/sienna_low_tide_lover_v3c_contact_sheet_short.jpg; gate image /workspace/jsw_tiktok/sienna/lyric_videos/02_low_tide_lover/sienna_low_tide_lover_v3c_face_gate16.jpg; first and last frames /workspace/jsw_tiktok/sienna/lyric_videos/02_low_tide_lover/sienna_low_tide_lover_{hook_short,lyric_video}_v3c_{first,last}.png. Manifest: /workspace/jsw_tiktok/sienna/lyric_videos/02_low_tide_lover/sienna_low_tide_lover_v3_manifest.json (key "v3c").

## Fixes
1. 16:9: eC2_a is removed. It is replaced by bal_p_v4C (/workspace/jsw_tiktok/sienna/x_clips_2026-10-21/remake/fin/bal_p_v4C.jpg). That is a Seedream single-ref edit of b1a with the b1a face pasted back, finished with v4C, face centroid 0.812. The body flag thigh_thin comes from the seated pose. Golden tan and fuller bust checked by eye. Outpainted to 16:9 (job 355dc47d-a79c-482c-8059-cd6effd018b2) and framed to fill (no bars). Banned sC2_b, sA2_b, eB4_b and eB4_c are not used.
2. Short: face shots are now gc_surf_i (0.818) and bal_p (0.812, native 9:16). b1a and eC2_a are out of the Short. All 16 re-gated frames score 0.79 or higher (table below).
3. YouTube thumbnail, title and description, and the FB caption are added (below).
4. TikTok and IG captions now say "link in bio".
5. Reddit is left out of this submission.
6. The manifest is updated with the v3c md5s and the end card.

Face stills in the 16:9 cut: v2sA2_c 0.808, surf_c 0.793, bal_p 0.812, gc_surf_i 0.818, b1a 0.813. In the Short: gc_surf_i and bal_p. v2sA2_c appears only in the 16:9 cut.

## Process
Valentina process. Approved v4C single-ref Seedream-edit stills, finished with finish_v4C, identity gate (cut 0.78, this job 0.79), checked by eye against the refs. ffmpeg slideshow with Ken Burns and 1 s crossfades, burned-in synced lyrics. Crisp text, inside the safe zone. No Kling, Seedance, lip-sync or new face generation.
16:9 outpaint jobs: f5982472-ba07-4f58-b9ab-524ccaa6f611 (v2sA2_c), aebc53b4-378b-4181-acad-23254e36da72 (surf_c), 8ecc5483-f2dd-42c3-b6f6-6f4cc05bfd4b (gc_surf_i), 9c044beb-b1de-46c8-b07e-3c81050ba537 (b1a), 355dc47d-a79c-482c-8059-cd6effd018b2 (bal_p, new in v3c).

## 16-frame face gate (Short v3c, identity_gate.py --model sienna --source seedream, frames in work/v3/gate16c/)
| # | t (s) | still | centroid | best | result |
|---|---|---|---|---|---|
| 1 | 0.2 | gc_surf_i | 0.816 | 0.777 | PASS |
| 2 | 0.7 | gc_surf_i | 0.811 | 0.778 | PASS |
| 3 | 1.2 | gc_surf_i | 0.799 | 0.778 | PASS |
| 4 | 1.7 | gc_surf_i | 0.811 | 0.779 | PASS |
| 5 | 2.2 | gc_surf_i | 0.801 | 0.775 | PASS |
| 6 | 2.7 | gc_surf_i | 0.793 | 0.774 | PASS |
| 7 | 3.2 | gc_surf_i | 0.806 | 0.763 | PASS |
| 8 | 3.7 | gc_surf_i | 0.808 | 0.769 | PASS |
| 9 | 8.8 | bal_p | 0.827 | 0.805 | PASS |
| 10 | 9.2 | bal_p | 0.823 | 0.813 | PASS |
| 11 | 9.6 | bal_p | 0.822 | 0.812 | PASS |
| 12 | 10.0 | bal_p | 0.800 | 0.783 | PASS |
| 13 | 10.4 | bal_p | 0.814 | 0.805 | PASS |
| 14 | 10.8 | bal_p | 0.805 | 0.785 | PASS |
| 15 | 11.1 | bal_p | 0.830 | 0.798 | PASS |
| 16 | 11.4 | bal_p | 0.836 | 0.797 | PASS |
Lowest centroid: 0.793. 16/16 frames score 0.79 or higher. The frames cover every clean face frame range; the other shots are people-free scenes.

## Credits
v3c: 2 Higgsfield credits (1 outpaint). v3 series total: 10 credits (5 outpaints at 2 each).

## Captions (no AI, no Spotify)
- YouTube title: Sienna Blake – Low Tide Lover (Lyric Video)
- YouTube description: 'Low Tide Lover' – a summer song about the one who only turns up when the tide's out. From the album 'Salt in My Hair', out now on Apple Music: https://music.apple.com/us/album/salt-in-my-hair/6825685962 #lowtidelover #siennablake #newmusic #indiepop
- Facebook: he only ever turns up when the tide's out… so I wrote him a song 🌊 'Low Tide Lover' is out now on Apple Music: https://music.apple.com/us/album/salt-in-my-hair/6825685962
- X: he only shows up when the water's gone 🌊 low tide lover https://music.apple.com/us/album/salt-in-my-hair/6825685962
- TikTok: wrote this one on the bonnet with a bag of hot chips after he left his towel at mine again 🌊 'Low Tide Lover' out now on Apple Music, link in bio #lowtidelover #newmusic #goldcoast #surfergirl
- IG Reel: he only ever turns up when the tide's out… so I wrote him a song 🌊 'Low Tide Lover' out now on Apple Music, link in bio #lowtidelover #newmusic #indiepop #goldcoast
- IG Story: new lyric video 🌊 'Low Tide Lover' – out now on Apple Music, link in bio
