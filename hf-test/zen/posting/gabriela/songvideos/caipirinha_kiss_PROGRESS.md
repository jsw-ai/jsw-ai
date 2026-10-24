# Caipirinha Kiss progress (update after each step)
Dir: caipirinha_kiss/. Job ids: work/jobs.txt. Media ids: work/media_ids.json.
1. DONE 28 Seedream stills (raw/) -> finish_v4C (fin/), still gates qc + work/sg.log, work/sg3.log. FAIL: h07, h10, v04 (not used).
2. DONE 25 Kling 3.0 clips (Element bd5edf6e, std 5s, sound off) in kl/: 13 h (h01-06,08,09,11-15), 12 v (v01-03,v05-13). Spend: Seedream 70 cr + Kling 187.5 cr (25x7.5).
3. RUNNING clip gates: work/clipq.sh -> kl/*_pf.json (log work/clipq.log). Gate waits on >=3GB & no Gabriela gate.
4. ASR dropped (whisper fails on this mix); lyrics shown as title cards. Hook in-point chosen by energy: a0=46.5.
5. TODO: work/cuts.json -> work/build.py hook|x|yt (one at a time, waitok.sh), gate finals, thumb, side-by-sides, captions, REVIEWER_PACKET.
- mkcuts.py written (auto-picks windows from pf scores); run after all clips gated
- 17:43 resume: Y1 (quota v3) uses 2026-10-22 k2_* clips (beachbar, miamisway); none of my kl/ clips overlap. Priority: hook + X; YT if time. 16/25 gated.
- 18:10 all 25 clips gated (v05 .815/.673, v09 .794/.112 fail full-clip; windows chosen >=.70 only). cuts.json made.
- 18:19 started work/finq.sh (build+gate hook, x, yt sequentially; log work/finq.log)
- 18:25 captions written final/captions.md
- 18:26 built final/gabriela_caipirinha_kiss_hook_21s_1080x1920.mp4
- 18:33 gate step failed (wrong python); fixed as work/finq2.sh, queued after finq.sh; log work/finq2.log
- 18:33 built final/gabriela_caipirinha_kiss_x_24s_1080x1920.mp4
- 18:34 hook probe OK (h264 Main, yuv420p, 1080x1920, 21.000s); sheet caipirinha_kiss/qc/hook_sheet.jpg: 12 unique scenes, consistent look
- 18:40 built final/gabriela_caipirinha_kiss_youtube_21s_1920x1080.mp4
- 19:00 YT thumb + 3 manifests (final/*_manifest.json) written
- 19:00 added 'ig' cut (IG Reel own first shot v12 sunsetpier; TikTok hook opens v01); queued work/finq3.sh after finq2
- 19:01 waiters self-matched; killed; running work/finq4.sh (gates hook,x,ig,yt + build ig) log work/finq4.log
- 19:25 gated gabriela_caipirinha_kiss_hook_21s_1080x1920: 0.8274999999999999 0.714 True
- 19:46 gated gabriela_caipirinha_kiss_x_24s_1080x1920: 0.8225 0.723 True
- 19:50 built final/gabriela_caipirinha_kiss_igreel_21s_1080x1920.mp4
- 20:08 gated gabriela_caipirinha_kiss_igreel_21s_1080x1920: 0.8274999999999999 0.719 True
- 20:15 side-by-sides qc/*_sbs.jpg (final frame | finished still, same height)
- 20:15 REVIEWER_PACKET + SHARED_LEARNINGS written (YT gate pending)
- 20:15 igreel manifest written
- 20:16 REVIEWER_PACKET + SHARED_LEARNINGS written; rerun work/packet.py after YT gate
- 20:22 gated gabriela_caipirinha_kiss_youtube_21s_1920x1080: 0.828 0.791 True
- 20:23 ALL CUTS DONE + gated; packet refreshed. Remaining: Reviewer/JSW AI/Scheduler handoff (parent).
- 20:26 v2 fix round started (Reviewer failed all 4)
- 20:27 v2: 8 covered Seedream stills v14-v21 submitted (b5, jobs.txt); YT v2 re-encode at 4.8M queued (work/finq5.sh)
- 20:30 8 covered stills downloaded raw/v14-v21 (all covered by eye, qc/b5_sheet.jpg); pipe6 queued finish+still gate
- 20:30 CORRECTION: X keeps original edit + sensitive; only re-encode x2 at 4.4M (<15MB) via finq6 after pipe6. Covered stills now only used for hook/IG v11 replacement.
- 20:33 built final/gabriela_caipirinha_kiss_youtube_21s_1920x1080_v2.mp4
- 20:43 YT v2 size 13031524 bytes
- 20:47 gated gabriela_caipirinha_kiss_youtube_21s_1920x1080_v2: 0.8285 0.785 True
- 20:54 v14-v21 finish_v4C done
- 20:55 uploaded v14-v21 fins (media_ids.json); Kling b6 submitted v14,v15,v16,v20 (jobs.txt)
- 20:57 v14-v21 still gate -> qc/stills_gate5.json
- 21:02 built final/gabriela_caipirinha_kiss_x_24s_1080x1920_v2.mp4
- 21:02 4 new Kling clips in kl/ (v14,v15,v16,v20); pipe7 queued to gate them after x2
- 21:17 X v2 size 13445129 bytes; still gate5 checked
- 21:20 YT v2 thumb regrabbed from v2 file (1.2s title card)
- 21:26 gated gabriela_caipirinha_kiss_x_24s_1080x1920_v2: 0.822 0.725 True
- 21:31 clip gate v14_linenset: 0.823 0.785
- 21:34 clip gate v15_mididress: 0.812 0.743
- 21:35 v14 -> TikTok hook2, v15 -> IG ig2 (replacing v11); stopped remaining clip gates; finq7 builds+gates hook2, ig2
- 21:42 built final/gabriela_caipirinha_kiss_hook_21s_1080x1920_v2.mp4
- 21:59 gated gabriela_caipirinha_kiss_hook_21s_1080x1920_v2: 0.831 0.705 True
- 22:00 per-shot check hook2/x2/yt2: all shots median>=.78 min>=.70
- 22:05 built final/gabriela_caipirinha_kiss_igreel_21s_1080x1920_v2.mp4
- 22:10 per-shot check hook2/x2/yt2: all shots median>=.78 min>=.70
- 22:11 wrote work/packet_v2.py (run after IG v2 gate + sbs)
- 22:21 gated gabriela_caipirinha_kiss_igreel_21s_1080x1920_v2: 0.83 0.731 True
- 22:46 v2 side-by-sides qc/*_v2_sbs.jpg
- 22:46 REVIEWER_PACKET_caipirinha_kiss_v2.md + v2 manifests written
