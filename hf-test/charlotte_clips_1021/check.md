# Frame checks (identity_gate --model charlotte --source seedream, 6 frames at evenly spaced times on the FINAL file) + visual check vs ref_sheet
Montages (top: ref_sheet.jpg; bottom: the 6 frames at the same 480 px tile height): *_montage.jpg

| Clip | 6-frame face scores (centroid) | ≥.70 | Visual face | Visual body/hair |
|---|---|---|---|---|
| pilates_vs_icebath | .50 / .05 / .48 / .09 / .00 (no face: back turned in the plunge) / .48 | 0/6 | Reads as her in the front-facing frames (start .85 on a 2x head crop); drifts on spins, turned-away and screaming frames | Full bust, waist and hips hold; hair dark, thick waves; matches the refs |
| matchday_swipe_awayend | .75 / .28 / .00 (scarf over the lens) / .75 / .66 / .69 | 2/6 | Lounge and away end both read as her; big open-mouth cheers score lower | Bust/hair consistent; plain red top has no badge; flares and crowd move the whole clip (the background diff never drops to zero) |
| X_ONLY_sauna_tease | .19 / .00 / -.04 / .41 / .55 / .60 | 0/6 | Head is small and often turned; recognisable but softer | Towel stays on, fully covered; bust/hair/build consistent |
Start stills (v4C finals): P1 .871, I4 .843, L2 .794, N1 .831, S5 .863, all PASS on face. P1/I4 trip only the body proxy's thigh_thin flag (leggings or a swimsuit crop; the legs look right by eye).
Thumbnails (gate): pilates .87, matchday .79, sauna .862, all PASS, eyes open, sharp.
Export: all three are H.264 Main, yuv420p, 1080x1920, faststart, no blur band, AAC audio; sizes 8.4 / 9.6 / 4.5 MB.
VERDICT: start stills and thumbnails pass. Clip frames FAIL the numeric face gate in big-action and full-body moments. This is the known trade-off: the head is small, turned or mid-expression. They need Samuel's visual call before use.
