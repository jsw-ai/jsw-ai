# rb2 fixes progress (Oct 22)
- Collab v4: DONE. text only y1288-1395, verified frames. gate median .793 min .736 (rb2/v4/qc/collab_v4.json). manifest updated. NOT submitted.
- X2 v4: DONE. yuv420p Main faststart, pilates half = Kling vP2 (element, c_P1). gate median .834 min .782. caption de-"vs"d.
- X5: DONE. x5j2 plunge-pool still, gate .838.
- YT1: thumb DONE final/YT1_thumb_v4.jpg (ye1 .818). video v4 final encode in progress (v5/yt_final.py), then gate.
- TODO: YT1 gate, text-window 1-frame gaps, side-by-sides, expression variety check.
- encoded final/charlotte_yt_20261022_matchday-vs-recovery_v5.mp4
- YT1 v5 encoded 17:18:49
- encoded final/charlotte_x_20261022_pilates-vs-icebath_v5.mp4
- X2 v5 encoded 17:20:12
- encoded final/charlotte_collab_20261022_oktoberfest-stein-clink_v5.mp4
- gate yt1: n=47 scored=47 median=0.766 min=0.726 below70=0 below78=35
- gate x2: n=51 scored=51 median=0.829 min=0.787 below70=0 below78=0
- gate collab: n=50 scored=50 median=0.793 min=0.743 below70=0 below78=4
- encoded final/charlotte_yt_20261022_matchday-vs-recovery_v6.mp4
- YT1 v6 (recovery half = ye1 still push-in) gate median .798 min .736
- encoded final/charlotte_yt_20261022_matchday-vs-recovery_v7.mp4
- YT1 v7 (text starts at cut) done
## FINAL (17:40 EDT) - all fixes done, not submitted (no agent messaging)
Collab v5, X2 v5, YT1 v7 + YT1_thumb_v4.jpg, X5 x5j2. Manifests updated in rb2/man and rb/man.
## Round 3 (17:55): submitted Kling vU c7c62ed5 (attempt 1/2), Seedream x5k1/x5k2
- vU attempt1 FAIL median .594; x5k2 PASS .836, x5k1 fail .773
- X5 x5k2 -> final/X5_recovered_mostly_tease_x5k2.jpg, sbs final/X5_x5k2_sbs.jpg
- encoded final/charlotte_yt_20261022_matchday-vs-recovery_v8.mp4
- YT1 v8 (Kling vU2 2.6-4.7s) gate median .796 min .756; thumb YT1_thumb_v8.jpg
## Round 3 DONE 18:15 EDT: YT1 v8 + thumb_v8 (.792), X5 x5k2 (.836)
## Round 4 (v9) 18:15: Kling vW cdb092c7 submitted (attempt 1), balance before 4881.38
- vW attempt1 FAIL: full median .771, best 2.1s window .773 min .719. Submitted vW2 f4815ea9 (attempt 2/2) 18:22
- vW2 PASS raw median .792; best 2.1s window 2.6-4.7 median .793 min .783
- seg/yt1v9_cat.mp4 built 18:37
- encoded final/charlotte_yt_20261022_matchday-vs-recovery_v9.mp4
- encoded v9 18:38
- gate v9: matchday .827/.783, recovery .793/.784 PASS
- thumb_v9 = seg frame t0.4 (vW2 3.0s) .803 PASS; sbs final/yt1_v9_sbs.jpg
## Round 4 DONE 18:43 EDT: YT1 v9 (md5 58c141a5) recovery window .793/.784, thumb_v9 .803, manifests updated rb2/man + rb/man. Not submitted.
## 20:35:48 7s rule audit started
- under 7s: hotchoc v2 5.03, pretzel v2 6.27, fitcheck v3 4.57, jetty v3 3.90, collab v5 5.03, pilates v5 5.13, YT1 v9 4.73; IG reel 1023 7.43 OK; bikini tease is a jpg
## v10 YT1 20:36:49: submitted recovery Kling vX1 ba42f6af, vX2 7e799991; gating o4 full
o4.mp4 n=50 scored=50 median=0.826 min=0.775 below70=0 below78=1
0.84 0.85 0.84 0.84 0.84 0.83 0.82 0.84 0.78 0.80 0.77 0.81 0.82 0.83 0.82 0.82 0.82 0.83 0.83 0.82 0.82 0.82 0.82 0.82 0.82 0.81 0.81 0.82 0.84 0.83 0.82 0.82 0.83 0.83 0.81 0.84 0.84 0.84 0.82 0.82 0.84 0.83 0.83 0.82 0.82 0.84 0.85 0.85 0.85 0.83
vX1.mp4 n=50 scored=50 median=0.767 min=0.715 below70=0 below78=31
0.81 0.81 0.81 0.81 0.80 0.80 0.77 0.80 0.80 0.80 0.81 0.80 0.81 0.80 0.80 0.79 0.80 0.80 0.78 0.79 0.74 0.75 0.77 0.77 0.77 0.75 0.74 0.75 0.73 0.72 0.75 0.76 0.77 0.77 0.77 0.75 0.74 0.75 0.74 0.75 0.75 0.75 0.75 0.76 0.76 0.76 0.74 0.71 0.73 0.73
- vX1 med .767; usable 0-2.0 (.80)
vX2.mp4 n=50 scored=50 median=0.755 min=0.684 below70=1 below78=37
0.81 0.81 0.82 0.81 0.81 0.80 0.80 0.78 0.78 0.78 0.73 0.75 0.75 0.77 0.76 0.75 0.75 0.75 0.68 0.74 0.75 0.75 0.74 0.75 0.73 0.75 0.75 0.75 0.75 0.74 0.74 0.75 0.75 0.74 0.75 0.75 0.75 0.76 0.76 0.76 0.78 0.77 0.78 0.77 0.78 0.79 0.78 0.78 0.78 0.78
- vX2 FAIL med .755 min .684. Plan v10: matchday o4 0-4.8 + recovery vW2 1.4-5.0
- 20:45:14 cfg v10/yt1v10.json written; encoding
start avail=4G 20:45:34
built final/charlotte_yt_20261022_matchday-vs-recovery_v10.mp4 8.433
charlotte_yt_20261022_matchday-vs-recovery_v10.mp4 n=84 scored=84 median=0.815 min=0.748 below70=0 below78=8
0.86 0.85 0.84 0.84 0.85 0.83 0.82 0.84 0.79 0.80 0.79 0.82 0.82 0.81 0.83 0.82 0.82 0.83 0.82 0.82 0.83 0.82 0.82 0.83 0.82 0.81 0.82 0.82 0.83 0.83 0.83 0.83 0.83 0.83 0.82 0.83 0.84 0.83 0.81 0.82 0.84 0.84 0.83 0.83 0.83 0.84 0.85 0.85 0.77 0.77 0.76 0.76 0.77 0.77 0.79 0.79 0.79 0.75 0.78 0.79 0.79 0.79 0.79 0.79 0.80 0.80 0.80 0.79 0.79 0.79 0.79 0.80 0.79 0.80 0.79 0.80 0.79 0.79 0.79 0.80 0.80 0.79 0.80 0.79
matchday 0-4.8 48 0.828 0.786
recovery 4.8-8.43 36 0.790 0.748
- 20:57:42 v10 first encode gate matchday .828/.786 recovery .790/.748 but recovery text started 1 frame early (seg0=145f). Re-encoding with t1 4.78/t0 4.83
built final/charlotte_yt_20261022_matchday-vs-recovery_v10.mp4 8.433
- 21:04:43 visual cut actually at frame 146 (4.8667); re-encode t1 4.81 / t0 4.85
built final/charlotte_yt_20261022_matchday-vs-recovery_v10.mp4 8.433
charlotte_yt_20261022_matchday-vs-recovery_v10.mp4 n=84 scored=84 median=0.815 min=0.749 below70=0 below78=8
0.86 0.85 0.84 0.84 0.85 0.83 0.82 0.84 0.79 0.80 0.79 0.82 0.82 0.81 0.83 0.82 0.82 0.83 0.82 0.82 0.83 0.82 0.82 0.83 0.82 0.81 0.82 0.82 0.83 0.83 0.83 0.83 0.83 0.83 0.82 0.83 0.85 0.83 0.81 0.82 0.84 0.84 0.83 0.83 0.83 0.84 0.84 0.85 0.77 0.77 0.76 0.76 0.77 0.77 0.79 0.79 0.79 0.75 0.78 0.79 0.79 0.79 0.79 0.79 0.80 0.80 0.80 0.79 0.79 0.79 0.79 0.80 0.79 0.80 0.79 0.80 0.79 0.79 0.79 0.80 0.79 0.79 0.80 0.79
matchday 0-4.83 49 0.826 0.772
recovery 4.87-8.43 35 0.790 0.749
## YT1 v10 DONE 21:25:07: md5 89cf972e7c662d4bd32a30a177f751d3 8.43s, matchday .826/.772, recovery .790/.749, thumb_v10 frame12 .849, sbs final/yt1_v10_sbs.jpg, manifest man/YT1_matchday_vs_recovery.json (v9 copy man/superseded_YT1_v9.json). NEXT: jetty-reset_v3
## 21:31:44 collab ext Kling vK2a f8b99917, vK2b b68c0194 submitted
- 21:49:06 downloaded vK2a/vK2b to v10/clips
- collab ext crop for vK2a/b = crop=623:1108:100:0 (matches try_cat framing)
vK2a_c.mp4 n=50 scored=50 median=0.765 min=0.721 below70=0 below78=43
0.78 0.79 0.78 0.78 0.78 0.78 0.77 0.77 0.78 0.78 0.77 0.76 0.75 0.75 0.74 0.75 0.76 0.75 0.75 0.75 0.75 0.74 0.72 0.75 0.76 0.78 0.79 0.77 0.76 0.77 0.77 0.77 0.78 0.79 0.77 0.72 0.73 0.76 0.78 0.77 0.76 0.77 0.77 0.76 0.75 0.77 0.76 0.75 0.76 0.76
vK2b_c.mp4 n=50 scored=50 median=0.788 min=0.753 below70=0 below78=6
0.78 0.79 0.78 0.78 0.78 0.79 0.78 0.79 0.80 0.80 0.80 0.75 0.77 0.79 0.79 0.80 0.80 0.79 0.80 0.78 0.77 0.78 0.78 0.81 0.80 0.80 0.80 0.79 0.78 0.78 0.76 0.76 0.79 0.79 0.79 0.78 0.78 0.78 0.79 0.79 0.78 0.79 0.78 0.79 0.79 0.79 0.80 0.80 0.79 0.79
COLLAB_GATES_DONE
- 22:16:32 JETTY v4 DONE 9.03s md5 b095c9c3 shots .839/.771 .821/.791 thumb f66 sbs+manifest
- 22:18:18 G1b uploaded media 8eceba94-db1b-4c7b-8cb1-21a241d8b1e3; Kling jobs kFC3a 0e4819a5 kFC3b e50ec6d6 (G1b), kPZ3a 7a2fccb8 kPZ3b 30ee76c9 (P1b)
- HC v3 plan: kHC2a 0.9-5.0 + kHC2b 0-5.0
- 22:28:34 HC v3 built+gated
- 22:29:12 HC v3 DONE 9.1s md5 288261f8 .794/.736 .787/.738 thumb f123
- 22:30:17 collab v6 queued: vK2b_c 0-4.0 + try_cat, text 0-6.565 / 6.6-end
kFC3a.mp4 n=50 scored=50 median=0.749 min=0.482 below70=14 below78=34
kFC3b.mp4 n=50 scored=50 median=0.829 min=0.748 below70=0 below78=2
kPZ3a.mp4 n=50 scored=50 median=0.751 min=0.668 below70=15 below78=27
kPZ3b.mp4 n=50 scored=50 median=0.788 min=0.612 below70=11 below78=20
GATES3_DONE
ffmpeg -nostdin -loglevel error -y -i v10/collab6_cat.mp4 -vf unsharp=3:3:0.3,noise=alls=3:allf=t,drawtext=fontfile=/usr/share/fonts/truetype/sand-box
start avail=4G 22:36:57
ffmpeg -nostdin -loglevel error -y -f lavfi -t 9.000 -i anullsrc=r=48000:cl=stereo -c:a aac -b:a 128k v5/collab6_a.m4a
start avail=5G 22:38:53
ffmpeg -nostdin -loglevel error -y -i v5/collab6_v.mp4 -i v5/collab6_a.m4a -map 0:v -map 1:a -c copy -map_metadata -1 -movflags +faststart -shortest f
start avail=5G 22:38:53
- encoded final/charlotte_collab_20261022_oktoberfest-stein-clink_v6.mp4
done final/charlotte_collab_20261022_oktoberfest-stein-clink_v6.mp4
charlotte_collab_20261022_oktoberfest-stein-clink_v6.mp4 n=90 scored=90 median=0.789 min=0.742 below70=0 below78=18
COLLAB6_DONE
