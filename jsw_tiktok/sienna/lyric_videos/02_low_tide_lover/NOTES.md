# Sienna Blake — "Low Tide Lover" (album "Salt in My Hair", track 2) — lyric video + hook Short

Status: BUILT, NOT REVIEWED, NOT POSTED. Nothing was uploaded or scheduled anywhere.

## Process statement
ffmpeg slideshow of approved v4C stills + people-free scenes, Ken Burns, crossfades, burned-in synced lyrics; no video generation.
(No Kling, no Seedance, no lip-sync, no new face images. Scenes = Higgsfield seedream_v5_pro still images of empty places only.)

## Final deliverables
| file | md5 | size | duration |
|---|---|---|---|
| sienna_low_tide_lover_lyric_video_1920x1080_v2.mp4 | 976e1de181985690057b853aa87c981e | 82,643,880 B | 167.200 s (full track) |
| sienna_low_tide_lover_hook_short_1080x1920_v2.mp4 | f899440f397c158708fe9d6c3bc95275 | 9,248,254 B | 24.000 s |

Superseded (kept, do not post):
- sienna_low_tide_lover_hook_short_1080x1920.mp4 (v1, md5 5db0c1577ecbebd702b77ef518cde3e5): end card sat on busy pandanus scene, less readable.
- work/failed/premux_audio_cut_136s_lyric_video.mp4: single-pass AAC stopped at 136.8 s; fixed by re-muxing the WAV with -t 167.2 (HOWTO fix).

## ffprobe
```
== sienna_low_tide_lover_lyric_video_1920x1080_v2.mp4
stream|codec_name=h264|profile=Main|width=1920|height=1080|pix_fmt=yuv420p|bit_rate=3750352
stream|codec_name=aac|profile=LC|sample_rate=48000|channels=2|bit_rate=195085
format|duration=167.200000|size=82643880|bit_rate=3954252
976e1de181985690057b853aa87c981e  sienna_low_tide_lover_lyric_video_1920x1080_v2.mp4
== sienna_low_tide_lover_hook_short_1080x1920_v2.mp4
stream|codec_name=h264|profile=Main|width=1080|height=1920|pix_fmt=yuv420p|bit_rate=2879245
stream|codec_name=aac|profile=LC|sample_rate=48000|channels=2|bit_rate=194152
format|duration=24.000000|size=9248254|bit_rate=3082751
f899440f397c158708fe9d6c3bc95275  sienna_low_tide_lover_hook_short_1080x1920_v2.mp4
```
- Full: last audio packet 167.189 s vs video 167.200 s; moov at byte 36, mdat at 183707 (+faststart OK). 34 shots x 5.9 s, 1 s xfade.
- Short: last audio packet 23.979 s vs 24.000 s; moov 36, mdat 27538. 6 shots x 4.833 s; audio 32.8–56.8 s of the track (verse 2 into chorus). End card last ~4.8 s on blue-hour scene: "full song: search / Sienna Blake / 'Low Tide Lover'".
- Both: -map_metadata -1, scale=out_range=tv, H.264 Main yuv420p, AAC LC 48 kHz ~195 kbps.

## Face stills (all v4C, gate-passed; re-gated today with identity_gate.py img --model sienna, log work/gate_stills.txt)
| still | source | centroid | best | expression |
|---|---|---|---|---|
| sC2_b | 2026-10-22_album/fin/sC2_b_v4C.jpg | 0.780 | 0.761 | soft closed-mouth smile (BORDERLINE, at threshold) |
| eC2_a | 2026-10-22_album/fin/eC2_a_v4C.jpg | 0.788 | 0.820 | soft smile |
| surf_c | track-1 composite strip (original archived off-box 10-22 03:25, disk cleanup, not revoked) | 0.801 | 0.782 | wide grin |
| gc_surf_i | track-1 composite strip (archived, same) | 0.822 | 0.778 | wide grin |
| b1a | track-1 composite strip (archived, same) | 0.812 | 0.806 | wide grin |
Not used: sA2_b, eB4_b, eB4_c, anything in REVOKED/, eA4_c (body-proxy fail).
Note: whole-Short video gate reports FAIL (frame_pass_frac 0.5, no_face_detected) because 3 of 6 shots are people-free scenes plus crossfade frames; every face still passes individually.

## Scenes (scenes/, all eyeballed at full res: no people, no text, no logos)
| scene | content | source |
|---|---|---|
| scene_0 | low-tide sand ripples at dusk | seedream_v5_pro 16:9, job db91ec35-bdb5-454d-9adb-930f96d81243 |
| scene_1 | blue-hour wet shoreline, crescent moon | job c23618b5-661e-4330-b8e2-d2d0597a6e92 |
| scene_2 | striped towel + thongs at sunset | job 00456bda-3b44-4ccf-8c74-e6d36328141a |
| scene_3 | white ute bonnet, hot chips, seagulls | job fbf54e87-1a12-45c6-95aa-3d4f2856f722 |
| scene_4 | pandanus headland at sunset | job 952a5b3b-2939-479c-aee6-69d2e8f982ae |
| scene_5 | rock pools | reused track-1 scene_5 |
| scene_6 | lifeguard tower at dusk | reused track-1 scene_4 |
| scene_7 | horizon beyond the break | reused track-1 scene_7 |
Prompts all end "no people, no text, photographic".

## Credits
Higgsfield: 12.50 credits total (5 images x 2.5). Balance 8030.13 -> 8017.63.

## Lyric timing
Lyrics = release.md section 2 (34 lines; release.md says it is an ASR transcript, not an official sheet). faster-whisper medium int8 word timestamps (work/asr2.py) + difflib alignment (align.py); verse 1 was missed so work/asr_intro.py re-ran 8–32 s; cross-checked with older /workspace/music/sienna/low_tide_lover/lyrics_timed.json (agree within ~0.8 s; earlier start used where mine lagged >0.3 s). Sung "And I wore it" vs written "Then I wore it" — kept the written lyric.

## QC
Frame sheets: work/qc_full/sheet.jpg, work/qc_short/v2_sheet.jpg, endcrop.png. Lyrics never over her face (sit over torso/lower third). Minor: b1a strip in the Short is ~1.5x upscaled, slightly soft; chips scene lands ~0.6 s before the "hot chips" line; sC2_b is at the 0.78 gate threshold (Reviewer may prefer swapping it).

## Draft captions (no links, no AI, no Spotify/Apple)
- TikTok: wrote this one on the bonnet with a bag of hot chips after he left his towel at mine again 🌊 search Sienna Blake 'Low Tide Lover' for the full song #lowtidelover #newmusic #goldcoast #surfergirl
- IG Reel: he only ever turns up when the tide's out… so I wrote him a song 🌊 search Sienna Blake 'Low Tide Lover' #lowtidelover #newmusic #indiepop #goldcoast
- X: he only shows up when the water's gone 🌊 low tide lover
- Reddit title (r/indieheads-style "[FRESH]" or a small new-music sub): [FRESH] Sienna Blake – Low Tide Lover (lyric video) — a summer song about the one who only shows up at low tide
- IG story text: new lyric video 🌊 'Low Tide Lover' — search Sienna Blake
Caption flag: track-1 album captions were switched to "coming soon" by the Reviewer (REV-155) while JSW AI says the album went live Oct 22 — these drafts avoid both "out now" and "coming soon"; Reviewer/JSW AI to decide.

## v3 (2026-10-22 14:30 EDT) — BUILT, NOT SUBMITTED/POSTED
Manifest: sienna_low_tide_lover_v3_manifest.json (process, stills and provenance, gate, credits).
- sC2_b replaced by v2sA2_c_v4C (gate 0.808, golden tan, fuller bust, eye-checked). Banned sA2_b, eB4_b and eB4_c are not used.
- 16:9 face shots are outpainted to fill the frame (4 Higgsfield outpaints, 8 credits). No letterbox or pillarbox.
- Lyric at 0:21.97 changed to "And I wore it…". End cards read "'Low Tide Lover' – coming soon". Text is sharp (no \blur) and sits inside the safe zone (Short MarginV 560, sides 110).
- Short faces: b1a and gc_surf_i. A first Short try that used v2sA2_c/eC2_a gated at a minimum of 0.772 and was moved to work/v3/rejected/.
- 16-frame face gate (Short): 16/16 PASS, minimum centroid 0.786.

## v3b (14:35 EDT): end card "out now on Apple Music"
Short md5 179dcb4d440b28bf60e57adf322d6556 (9,478,956 B). Full md5 5f48fca7c1232192b62f932705221bfa (92,389,033 B). Review message: REVIEW_SUBMISSION_v3b.md. NOT yet sent (SendToAgent unavailable to subagent).

## v3c (14:55 EDT): bal_p replaces eC2_a; Short = gc_surf_i + bal_p; 16-frame gate min 0.793
Short md5 9fb32ce8064e3db8cafc0a291cfc995b (9,338,743 B); full md5 4650ac89e29be0abc9d44fb4f7256c43 (92,815,711 B); thumb 57cf4aef86ae419cd9b0b05a781bddf0. Credits +2 (outpaint 355dc47d). See REVIEW_SUBMISSION_v3c.md.
