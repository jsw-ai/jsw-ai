# STATUS: NOT READY — v2 FAILS the 0.78 face gate. Do NOT forward as a PASS candidate without Samuel's call.
To: JSW Content Reviewer (99a98fb5-f7d1-48c7-aee8-44145d400592) — Valentina Rosario reel v2 (realism redo)
Clip: final/valentina_rosario_coconut_v2_CANDIDATE.mp4  md5 ea794cebcc2531cda4889b4100ca9a01 (5.04 s, 1080x1920, H.264 Main, yuv420p, faststart, 4.6 MB; bottom hook "Cartagena said one more day / and I listened"; music "Bossa Antigua" Kevin MacLeod, CC BY 4.0, credit in captions.md)
Silent: final/valentina_rosario_coconut_v2_CANDIDATE_silent.mp4  md5 9063675e3ed510b2a8f9587f8e31f169
Thumb: final/valentina_rosario_coconut_v2_CANDIDATE_thumb.jpg  md5 edda266c7c9669bc4fd276abe46a3bad (bow pose with coconut, start still, gate .810)
Side-by-side: qc/valentina_rosario_coconut_v2_sidebyside.jpg ; match note: qc/match_note_v2.md ; captions unchanged: captions.md
Gate (bar .78): export frames .830 .812 .597 .620 .675 .698 .704 .656 .657 .726 -> min .597, median .687 = FAIL. (Video-mode default thresholds say PASS, min .569, but house rule is .78.) Start still .816.
Per fix:
1) Frozen smile -> real action: holds coconut, eye-glance to the island, soft laugh, brow lift, tucks hair behind ear, ends on half-smile. Expression changes throughout. (This is also why the face score drops: laugh/squint/hand near face.)
2) Waxy skin / locked highlights -> start still re-finished with v4C; whole clip run through a per-frame v4C-style pass (skin-mask specular compression + pore texture + grain, work/tex/vtex.py); handheld wobble makes highlights shift. Improvement is modest, not dramatic.
3) Hands -> hands hold the coconut or touch hair, never on hips; start-still fingers checked at full res (5 distinct each). In-clip the hair-tuck hand is softer but not fused in sampled frames.
4) Sarong melt -> sarong knot is clear of the hip in the still and flutters separately; sampled frames show no melting (check 2-4 s at full speed).
5) Hair loop -> strong side wind, irregular gusts, Kling pro + handheld/boat sway prompt; hair now blows one direction with the wind.
Credits this redo: 45 exact by job price (4 Seedream 5.0 Pro @2.5 = 10; 4 Kling 3.0 PRO 5 s sound-off @8.75 = 35).
