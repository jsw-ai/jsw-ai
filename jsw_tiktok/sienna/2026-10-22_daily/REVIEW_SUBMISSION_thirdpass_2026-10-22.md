# Sienna third pass, 2026-10-22: submission

## Submitted: beach tease v4 (X), body-drift fix (v3 1ce83ebf was failed by the Reviewer)
- File: thirdpass/sienna_x_20261022_x_tease_sunrise_bikini_v4.jpg
- md5: 02361f4c7a4ae1c772b85df4db701a08
- Unique: matches only its own source, fin/BT10_5_v4C.jpg, from a fresh generation. Matches no other file in 2026-10-22_daily/ or the v4C sheets.
- Gate: PASS, centroid 0.817, best ref 0.829; body/shoulder checks clean.
- Side-by-side at the same height: thirdpass/sidebyside_tease_v4_vs_v2sheet.jpg (vs sienna_v4C_reference_sheet_v2: b1a, gc_surf_i, surf_c).
  - Fuller, rounder, lifted natural bust and cleavage, matching gc_surf_i and surf_c.
  - Shoulders at full width.
  - Same golden tan.
- Content:
  - Terracotta ribbed triangle bikini, same cut as the refs' sage top but not the sage bikini.
  - Shoulders turned about 15 degrees, closed-mouth smile, waist-deep in the sunrise sea.
- No link. **Mark as sensitive media on X.**
- Process:
  - Seedream v5 pro, single ref reddit_x1_b. Prompt v3/p_BT10.txt has the locked body line word for word plus the fuller-bust wording.
  - Then finish_v4C, then identity_gate (seedream, --body).
  - Path to BT10: BT7 (3 refs) dropped face scores (0.72–0.77); BT8 best 0.782; BT9 best PASS 0.788 (under 0.79); BT10_5 at 0.817 is the only one at or above 0.79.

## Not submitted: clip1 v3 (7–9 s)
- Side A is ready: kA4_a frames 38–105 (68 frames).
- No side-B clip had the roughly 100 consecutive frames at 0.78 or higher needed to reach 7 s:
  - Best runs: kB4_a 48, kB7_3 42, kB8_1 41 (near-static), kB8_2 31, kB6 at most about 26, kB7_1/2/4 21–26, kB8_3 30, kB8_4 about 30.
  - Identity drifts below 0.78 within about 1–2 s even with almost no motion.
- No cut was built, so no splices were used.

## Not submitted: album still
- Nothing at 0.79 or higher yet. Best is AL5_6 at 0.783.
- AL5_14–21 are still in the gate queue, which is slow because the shared box has only about 2 GB of RAM free.
