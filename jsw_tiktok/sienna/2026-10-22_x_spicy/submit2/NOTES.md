# Sienna X spicy v2 redo (single-ref), 2026-10-22 ~12:25-12:50 AM ET. NOT DELIVERED: no still passed the 0.78 gate.
seedream_v5_pro 3:4 2k, ONE image_reference per job, locked body line word for word, even front light, finish_v4C.py (P repointed), identity_gate --source seedream --body.
R1 (p_*.txt, ref story2_a 2969a422, head-to-waist): 6 imgs, 0.636-0.709. Jobs dd9fa93c 34ed05e7 ec1e3d8f b7ab5ce8 6455cbab 82f46193
R2 (p2_*.txt "Edit this exact photo", ref story2_a, head-to-chest, round-face wording): 6 imgs, 0.656-0.746. Jobs da414b48 bcf2e200 759171ac 45e2e32b 6803d70d ca958b3b
R3 (p3_*.txt wider-face wording, ref story2_a): 12 imgs, 0.646-0.748. Jobs 14515295 dab9e07e d5df0be8 25a1bc2c de1b4312 cae92382 61b49eb5 353eb000 4351d290 3ae13545 c5065807 6bc9062e
R4 (p3_*.txt; bed ref reddit_x1_b_v4C fa09357e, shower/pool ref story1_a 5abc094e): 9 imgs, 0.672-0.759. Jobs 833a73ef 4d5a405b 6ca91052 78661e54 64c75c6e b4a8b605 7fccf846 dd306d85 63819952
Credits: 33 x 2.5 = 82.5 cr. No blocks/refunds.
Best per scene: bed2_a 0.746, bed4_b 0.737; shower4_b 0.721; pool4_c 0.759 (body flag sh_w 0.88), pool3_b 0.748, pool4_a 0.745.
Learning: single-ref + non-grin expressions (closed smile / over-shoulder / lip bite) drift long-narrow and cap ~0.75; matches the "smile pack" pitfall in VALENTINA_PIPELINE.md s2b/s9.

## R5 (2026-10-22 ~12:45 AM ET, p5_*.txt = p3 base + softened expressions; single ref per scene, 2.5 cr each, 12 x 2.5 = 30 cr)
- bed (ref story2_a_v4C 2969a422, light teeth smile): bed5_a..d = 4136ebe6 5a71285f 1b92f8be 5ea42712
- shower (ref story1_a_v4C 5abc094e, face mostly to camera): shower5_a..d = 09e40d92 98455f08 e9effd30 73696bdb
- pool (ref story1_a_v4C 5abc094e, half-smile lip bite): pool5_a..d = 97f3b084 56386e10 ca264e23 d19b647a
- R5 gate (qc/gate5.json): ALL FAIL. bed 0.665-0.726 (best bed5_d 0.726), shower 0.706-0.758 (shower5_d 0.758, shower5_c 0.755/best 0.771), pool 0.662-0.757 (pool5_d 0.757). No body flags. Softened expressions did not lift scores.
## R6 fallback (wide teeth smile, p6_*.txt, 10 cr cap = 4 imgs: bed 1, shower 1, pool 2; same refs as R5)
- bed6_a 136d21b4, shower6_a a9d50a1e, pool6_a 31a683d8, pool6_b eed10672 (4 x 2.5 = 10 cr)
- R6 gate (qc/gate6.json): ALL FAIL. bed6_a 0.733 (body unmeasurable: shoulders not visible), shower6_a 0.755, pool6_a 0.759, pool6_b 0.766 (closest yet). No body flags otherwise.
## Outcome R5+R6: 16 imgs, 40 cr (R5 30 + R6 10). Running total 49 imgs / 122.5 cr. Nothing >= 0.78 -> no _v2 files, no Drive upload, v1 files NOT moved to 99 Rejected.
Best ever: bed 0.746 (bed2_a), shower 0.758 (shower5_d), pool 0.766 (pool6_b). Learning: expression changes alone cap ~0.73-0.77 with these single refs; next lever is likely a different ref (an approved Sienna final with a softer expression) or a mid framing (head-to-waist) rather than face-large.
