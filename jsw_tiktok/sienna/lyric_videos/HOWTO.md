# HOWTO: Sienna lyric-video slideshow (repeat per track)
Slideshow only: stills with Ken Burns pans, crossfades, the full track and burned-in synced lyrics. Built with ffmpeg. No video generation, lip-sync or new face images.

1. Folder: `lyric_videos/NN_<slug>/` with `work/` and `scenes/`. Never overwrite: bump `_v2`, `_v3`.
2. Lyrics: copy that track's section from `/workspace/music/distrokid/sienna/release.md` into `work/lyrics.txt`. Blank lines are ignored, and one display line = one lyric line.
3. Timing: copy `01_salt_in_my_hair/work/asr2.py` and `align.py`. Change the WAV path, then run `python3 asr2.py` (faster-whisper **medium**, lyrics as initial_prompt, about 3 min CPU), then `python3 align.py`, which writes `timings.json`. Check any `INTERP` lines and spot-check 3 or 4 timings by ear.
4. Stills: use only gate-passed or Reviewer-passed Sienna v4C finals (check the gate*.txt / NOTES.md logs; confirm the Reviewer PASS). Add 6-8 people-free scenes that fit the song. Reuse `01_*/scenes/` where they fit. Otherwise generate with Higgsfield `seedream_v5_pro` 16:9 (about 2.5 cr each, prompts end with "no people, no text, photographic"), check them by eye, and log job ids and credits.
5. Build: copy `build.py` and edit the P (stills + face height fraction), SC (scenes), and the Short's T0/T1 (the chorus window; 24 s total, with the last 4 s as the end card) and shot order. Then run:
   `python3 build.py short ../<name>_hook_short_1080x1920.mp4` and `python3 build.py full ../<name>_lyric_video_1920x1080.mp4`
   - Shots are rendered one by one, then crossfaded in chunks of 6 (a single 47-input xfade gets OOM-killed). Next, libass subtitles + audio are added in one encode with libx264 Main, yuv420p (`scale=out_range=tv` to avoid yuvj), AAC 192k 48 kHz, `+faststart`, `-map_metadata -1`.
   - In 16:9, portrait stills are centred over a blurred copy of the same still, so the lyrics never cover her face.
   - Delete `seg_*`/`chunk_*` before rebuilding if you change the stills.
6. Audio check: the single-pass encode once cut the AAC at 203.7 s. Verify with `ffprobe -select_streams a -show_entries packet=pts_time` (last packet ≈ video length). If it is short, re-mux: `ffmpeg -i vid.mp4 -i track.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -t <video_dur> -movflags +faststart -map_metadata -1 out_vN.mp4`.
7. QC: grab frames (`ffmpeg -ss T -frames:v 1`) across the video and check the text stays off the face and is readable. Run ffprobe (h264 Main, yuv420p, 1920x1080 / 1080x1920, Short under 15 MB and 15-30 s) and check that moov comes before mdat.
8. NOTES.md: sources + pass status, process, credits, ffprobe. Never mention AI in the video text. Don't post; hand it to the Reviewer.
