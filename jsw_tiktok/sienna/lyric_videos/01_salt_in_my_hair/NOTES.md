# Sienna Blake – "Salt in My Hair" (Track 1) lyric video + hook Short
Built 2026-10-22 (ET). REVIEW ONLY: nothing was posted, scheduled or uploaded.

## Finals (use these)
- Full YouTube lyric video: `sienna_salt_in_my_hair_lyric_video_1920x1080_v4.mp4`
- Hook Short: `sienna_salt_in_my_hair_hook_short_1080x1920_v2.mp4`
- Superseded (kept, not overwritten): `sienna_salt_in_my_hair_lyric_video_1920x1080_v3.mp4` (its AAC track stopped at 203.7 s; v4 is the same video stream copied, with the full WAV re-muxed), `sienna_salt_in_my_hair_lyric_video_1920x1080_v2.mp4` (the tight portrait crops let lyrics touch her chin), `sienna_salt_in_my_hair_hook_short_1080x1920.mp4` (yuvj420p full-range, not yuv420p), `work/failed/FAILED_oom_partial_lyric_video.mp4` (ffmpeg was OOM-killed; broken file)

## Method (changed to a slideshow per the parent's instruction: no Kling or video generation)
Ken Burns pans and zooms on stills, 1 s crossfades (xfade fade), the full track audio, synced lyrics burned in with libass (DejaVu Sans Bold, white, soft blurred shadow, bottom-centre lower third). Built entirely with ffmpeg. See ../HOWTO.md and work/build.py.
- Full: 47 shots of about 5.93 s each, alternating scene and Sienna. Sienna's portrait stills are centred at full height over a blurred, darkened copy of the same still, so the lyrics sit below her chest and never cover her face (checked in work/full_check3.jpg).
- Short: 24.0 s of the first chorus (track 38.2 to 62.2 s), 6 shots. The last 4 s are an end card: "full lyric video on YouTube / search Sienna Blake / Salt in My Hair". The audio fades in and out. No AI mention anywhere.

## Lyric timing
faster-whisper medium (int8, CPU, the official lyrics as initial_prompt) gave word timestamps in work/words_med.json. They were aligned to the official lines in release.md (work/lyrics.txt) with difflib sequence matching in work/align.py. The result is work/timings.json, with 43 lines and none interpolated. Each line shows 0.15 s before its first word and ends at the next line, at most 7 s later. A small-model pass (words.json) only caught 132 words, so it was dropped.

## Sources
Sienna stills. These passed the identity gate (0.78) per the box gate logs and NOTES. **I found no explicit JSW Content Reviewer PASS record for any of them on the box. Get them confirmed before publishing.**
- 2026-10-22_album/fin/sA2_b_v4C.jpg, sC2_b_v4C.jpg (0.780, borderline), eC2_a_v4C.jpg (0.788), eB4_b_v4C.jpg (0.824), eB4_c_v4C.jpg (0.817). Gate files: 2026-10-22_album/gate*.txt
- 2026-10-20/stills/surf_c_v4C.jpg, 2026-10-20/gc/gc_surf_i_v4C.jpg (used in the 10-20 surf TikTok), 2026-10-20/gc2/fin/b1a_v4C.jpg (centroid 0.800 PASS, 2026-10-20/gc/NOTES.md)
- Drive "02 Ready SFW" / "05 Posted": the folders exist, but the only Sienna images in Drive are the X/spicy Bali set, refs and the cover. None of them were used.
People-free scene stills (generated, all checked for no people): scenes/scene_0..7.png (golden-hour beach, sunrise wave, surfboard and fence, Bali rice terrace, lifeguard tower at dusk, rock pools, aerial shoreline, beyond-the-break horizon).

## Credits
Higgsfield seedream_v5_pro, 8 images at 16:9, at about 2.5 cr each = **about 20 cr** (the per-image rate comes from earlier Sienna NOTES; the shared balance was 8717.88 before). Job ids: 3342e6b9, 9a0b8e93, 1df920d3, 2e84b358, 87a7d121, 3b05bca6, 36e53260, 030f046c. No Kling, video or face generation.

## ffprobe
```
== sienna_salt_in_my_hair_lyric_video_1920x1080_v4.mp4
codec_name=h264
profile=Main
width=1920
height=1080
pix_fmt=yuv420p
r_frame_rate=30/1
duration=232.900000
codec_name=aac
profile=LC
sample_rate=48000
channels=2
r_frame_rate=0/0
duration=232.900000
duration=232.900000
size=122717274
bit_rate=4215277
73b9c9c3e07d85a1ca06df7570aa220e  sienna_salt_in_my_hair_lyric_video_1920x1080_v4.mp4
moov@ 36
== sienna_salt_in_my_hair_hook_short_1080x1920_v2.mp4
codec_name=h264
profile=Main
width=1080
height=1920
pix_fmt=yuv420p
r_frame_rate=30/1
duration=24.000000
codec_name=aac
profile=LC
sample_rate=48000
channels=2
r_frame_rate=0/0
duration=24.000000
duration=24.000000
size=9560729
bit_rate=3186909
fbae5ba9e4972574970bb3850a9770fd  sienna_salt_in_my_hair_hook_short_1080x1920_v2.mp4
moov@ 36
```

## Known issues
- The full video is 232.9 s vs. 233.48 s for the track (frame rounding in the chunked xfade). The last 0.58 s of the outro tail is trimmed.
- The scene stills are 2720x1536 upscales. The portrait stills sit in a centred panel over a blurred backdrop (fine for 16:9, and different from the 9:16 no-blur-bands rule).

## v5 full / v3 Short (2026-10-22, Reviewer fixes)
- Removed sA2_b, eB4_b and eB4_c. Stills: surf_c, sC2_b, eC2_a, gc_surf_i, gc2 b1a + scene_0..7. They alternate, so the same still never appears twice in a row. The pan direction rotates on each reuse. The full video opens on surf_c. The Short order is surf_c, scene_1, sC2_b, scene_0, b1a, scene_7.
- Short end card: "full song: search Sienna Blake / 'Salt in My Hair'" on 2 lines, centred at 66 px, about y 920-1030 of 1920 (above the bottom 20%).
- Full: tpad clones the last frame so the video is 233.5 s. The audio cut at 203 s again (work/failed/v5_premux_audio_cut_203s.mp4), so the full WAV was re-muxed with -t 233.48. The last audio packet is at 233.47 s.
- Previous segs/chunks are in work/prev_v4/. The previous build script is work/build_v4.py. QC sheets are in work/qc_v5/.
- full v5 md5 140b89409e226fb327fa4bf42eb19b41, 122862342 B. Short v3 md5 3ddf5b3c3b3ec55098b6c09da457c51b, 9608672 B.

## v4 Short (2026-10-22, end card only)
- `sienna_salt_in_my_hair_hook_short_1080x1920_v4.mp4`: same as v3 (reused seg_short + chunk_short_000), only the end card changed to 3 lines: "full song: search" / "Sienna Blake" / "'Salt in My Hair'" (66 px, centred). Script: work/build_short_v4.py. v3 ASS backed up as work/short_v3.ass.
- End-card text bbox (incl. shadow): x 266-809, y 870-1057 of 1080x1920. Frame: work/qc_short_v4/v4_end.png (t=23 s), text-only render work/qc_short_v4/textonly.png.
- md5 09581c64a0dede1d172e61d4e34de4f2, 9644810 B, H.264 Main, yuv420p, AAC LC 48k, 24.0 s, moov at front. v3 is unchanged (md5 3ddf5b3c3b3ec55098b6c09da457c51b).
