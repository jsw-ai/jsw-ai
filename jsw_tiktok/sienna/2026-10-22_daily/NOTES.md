2026-10-22 16:07 clip1 firstclass_whippan v1 + X set (3 tease, 2 album) submissions written; Kling drift <0.78 after ~1-2s on all 5 clips, used passing windows only
2026-10-22 18:20 v3 pass progress:
- stills gated (fin/*_v4C.jpg, gate/*.txt): PASS>=0.79 only S3B_c 0.793 (green slip rooftop dusk), S3A4_b 0.825 (porch cream tank guitar). All AL3/AL3r/AL4 and BT3/BT3r/BT4 fail (best BT3r_a 0.781, AL4_a 0.759).
- kling kB3v3_a/b (S3B_c hair-down): drift <0.78 after ~0.35s, unusable.
- pending kling: kA4_a,b (S3A4_b, media a99ea965) kB4_a,b (S3B_c gentle, media 304c73bf) — jobs in jobs.txt
18:2x gated kA4_a kB4_a (see gate/v_*.json)
kA4_a clean run f38-105 (2.83s); kB4_a clean f0-47 (2.0s)
18:42 kA4_b clean runs f28-83 (2.33s); kB4_b best f0-10. Max single-window total = kA4_a 68f + kB4_a 48f = 4.83s < 6s -> clip1 v3 NOT buildable to spec. No v3 submissions written. Album/beach: no still >=0.79.
18:43 3rd-pass decision: keep side A kA4_a f38-105; side B low-motion from S3B_c; one reroll round AL5/BT5 x9 each
18:44 submitted kB5_a-c, AL5_1-9, BT5_1-9 (jobs.txt)
18:46 fetched all 3rd-pass outputs; gating -> qc/thirdpass_gate.log
18:52 parent: credits unlimited, keep rerolling until pass
18:52 kB5_a FAIL (med .769); submitted SB6_1-6 fresh side-B stills
19:18 kB5 a/b/c all FAIL (S3B_c source too weak). AL5_1-3,BT5_1-2 FAIL so far
19:18 submitted AL5_10-15 BT5_10-15
19:32 BT5_4 centroid .807 but gate FAIL (see reason); AL5_6 PASS .783 (<.79)
BT5_7 FAIL centroid': 0.74 reasons': ['identity_centroid_low_seedream']
AL5_8 FAIL centroid': 0.737 reasons': ['identity_centroid_low_seedream', 'identity_best_ref_low']
BT5_8 FAIL centroid': 0.792 reasons': ['body_slim_or_turned:shoulder_width_0.85']
AL5_9 FAIL centroid': 0.727 reasons': ['identity_centroid_low_seedream']
--: line 2: 3582064 Killed                  /workspace/.face-venv/bin/python /workspace/hf-test/zen/posting/identity_gate.py img --model sienna --source seedream --body fin/${n}_v4C.jpg > gate/$n.txt 2> /dev/null  
BT5_9   
19:39 gate queue script gateq.sh -> qc/gateq.log (resumable)
19:43 fetched BT6_1-6; gateq running (SB6_1 FAIL .748)
19:53 SB6_5 PASS .815 (smirk) uploaded c1f24b6e; SB6_6 .801 toothy unused
19:54 submitted kB6_1-4
19:54 submitted AL5_16-21
20:02 BT5_11 PASS .797, BT5_13 PASS .794 (beach candidates). fetched kB6_1-4, AL5_16-21. pausing still queue for video gates
20:02 beach pick = BT5_11 (closed mouth, angled, terracotta one-piece)
20:13 kB6_1 FAIL (max ~21f clean). submitted kB7_1-4 head-turn
20:23 kB6_1-4 all FAIL (max 26f). fetched kB7
20:25 beach deliverable thirdpass/sienna_x_20261022_x_tease_sunrise_wade_v3.jpg (from BT5_11)
20:32 new rule: clip 7-9s -> side B needs >=100 clean frames (A=68f)
20:33 kB7_1 FAIL (21f). submitted kB8_1-4 near-static
20:41 kB7_2 FAIL(26f) kB7_3 FAIL(42f). kB8 fetched; chain2 queued: vq kB8 then gateq stills
21:10 kB8 all FAIL (max 41f). Wrote REVIEW_SUBMISSION_thirdpass (beach only). chain2 still gating stills
21:12 Reviewer FAILED BT5_11 tease v3 body drift. BT7_1-6 submitted (locked line, fuller bust, refs uploaded 01556abd/6521b294/ecc0d0cd)
21:14 BT7 fetched; chain3 gating BT7 first then BT6/AL5
21:24 BT7_1/4/6 FAIL (.717/.751/.773). BT8_1-8 submitted single-ref
21:28 BT8 fetched (fuller bust visible). chain4 gating BT8 first
21:40 BT8_5 PASS .782 (<.79); BT8_2/6/8 FAIL; BT8_4 OOM requeue. BT9 from reddit_x1_b direct
21:46 BT8_1/3 FAIL. BT9 fetched; chain5 gating BT9 first
21:58 BT9_3 PASS .788; BT9_4 .794 but shoulder_width FAIL. BT10 = squarer shoulders
22:01 BT9_6 FAIL. BT10 fetched; chain6 gating BT10 first
22:15 BT10_5 PASS .817 -> tease v4 02361f4c, side-by-side done, REVIEW_SUBMISSION updated. album queue continuing in chain6
