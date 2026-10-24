# CONSISTENCY_PROTOCOL.md (2026-10-21, ET)

## 1. What the logs say (measured)
Sources: 393 `*gate*.json` files under /workspace, SHARED_LEARNINGS.md, and today's tests. These are rough counts: files overlap (reruns, re-scored frames).

**Scored stills by model** (median gate centroid; % that clear the Seedream bar of .78; % that clear the general bar of .72):

| model | stills scored | median | >= .78 | >= .72 |
|---|---|---|---|---|
| Sienna | 139 | .810 | 73% | 90% |
| Camille | 73 | .817 | 58% | 64% |
| **Charlotte** | 362 | **.770** | **42%** | 78% |
| Madison | 195 | .815 | 67% | 84% |
| Gabriela | 90 | .809 | 60% | 76% |
| Valentina | 47 | .856 | 68% | 85% |

- About 394 of 906 scored stills missed .78. At 2.5 cr a still, that is **about 1,000 cr of still waste**. Charlotte alone accounts for about 520 cr of it.
- **Fail reasons across all gate files:** identity_centroid_low 1,863; best_ref_low 1,018; no_face 57; headroom 13; body_thigh_thin 14; text_in_image 13+.
- **Video re-renders logged in SHARED_LEARNINGS:** Madison golf failed review 4x (184 cr). Charlotte lip-sync took 211 cr for 4 submissions, one flagged nsfw. Valentina v3 to v3_v2 cost 106 cr. Camille Oct 16 used 133 cr with 2 re-rolls. Wan lip-sync failed the gate (.505). The 477.5 cr and 212 cr batches each included multiple rerolls. Rough video waste: **at least 700 cr**.
- **Today's Charlotte tests (Oct 21):** night or TV-glow light with an anxious, teeth-showing face scored .659-.739. Stage light with a 2-ref generation scored .69-.727. A single-ref edit of a previously passing daylight still scored .749-.784, and one passed.

## 2. Root causes (ranked)
1. **Lighting and expression drift.** Dim, coloured or night light and extreme expressions (anxious, open mouth) cost .05-.12 of gate score. Daylight with a closed-mouth smile scores highest.
2. **Wrong or weak face ref.** Uploading `keepers/charlotte_face_keeper.png` fresh scored worse than the older media fd8e810e (.686 vs .739, same prompt family). Some ref uploads may be degraded (resizing or format). The gate's ref set (4 face_refs) is also broader than the generation ref (1 face), so generations drift toward one ref while the gate averages all four.
3. **Fresh 2-ref generation instead of editing a passing still.** Single-ref edits of a gated still keep identity best.
4. **Tool choice.** Seedream 5 Lite and Elements score about .75. Wan fails. Kling warps hands and props. Outpaint repaints the face (-.07). Upscaling lowers the score (scale artifact).
5. **Start frames for video.** Mid-speech or teeth frames, cleavage (nsfw refusal, credits lost), small faces, background people.
6. **Video run before the still is proven.** Video costs 36-96 cr, so a bad still multiplies the loss.

## 3. Protocol (do this every time)
1. **Locked refs per model:** use one generation face ref plus one body ref. These are the media in identity_packs `gen_refs`; add that field, Charlotte = the fd8e810e source plus b8d45ca6. Keep the full face_refs set for the gate. Re-upload only from the original file, never a resized copy.
2. **Draft stills first, cheap:** draft every scene as 1 Seedream Pro still, or an edit of a passing still. Gate immediately (`identity_gate.py img --source seedream --body`), at the threshold for the source (.78 Seedream, .80 Soul).
3. **Edit, don't regenerate:** when a scene changes, edit a passing still (single ref) rather than starting fresh from the refs.
4. **Prompt template:** "closed-mouth smile, lips together, faithful recognisable likeness of photo 1, [face descriptors], soft even daylight on her face from the front". No night, TV-glow or coloured stage light on the face. Expressions come from the video, not the still.
5. **Video only from a still that passed the gate**, with a closed-mouth expression, the face at least 6% of the frame, higher neckline, no background people. Gate each clip on 8 frames before finishing. Never gate upscaled frames.
6. **Max retries:** 2 rerolls per still (3 attempts total). If all fail, escalate to the Reviewer or Samuel with the scores. For video: 1 reroll, then escalate. Stop any job at 1.5x its estimate.
7. **Log every fail** with `--log zen/posting/gate_fail_log.jsonl` so it can be counted next audit.

## 4. Approved tools
- **Stills:** seedream_v5_pro 2-ref or edit (default); soul_2 + soul_id (Sienna only; others need training first).
- **Talking:** seedance_2_0 i2v + audio_references, 720p, 8 s (15 s untested until today's stand-up test). Lines of 8 words or fewer per 8 s.
- **Motion:** kling3_0 + Element only without props in hands.
- **Finish:** local ffmpeg (grain, sharpen, text). Topaz upscale only after the gate.

## 5. Banned combinations
- Wan lip-sync.
- Seedream Lite or Elements for finals.
- Outpaint across the face.
- Kling with a golf club, racket or bottle in hand.
- Gating upscaled frames.
- Cleavage or bikini start frames for Seedance.
- Night or TV-glow faces as start frames.
- Mid-speech or teeth start frames.
- Background people.

## 6. Soul ID for the other five?
- **Seedream Pro:** 2.5 cr per still at a 42-73% pass rate, so about 3.4-6 cr per passing still.
- **Soul 2:** 0.12 cr per still. Sienna's pass rate with Soul looks similar (.831 today).
- **Training:** about 25-40 cr per model.
- **Break-even:** about 8-12 passing stills per model, which is one week of content.
- **Recommendation:** train Soul IDs for Charlotte first (biggest waste), then Camille and Gabriela. Training only with Samuel's approval of the exact 10-20 image set (hard rule). Body still needs a check: Soul is face-first, so run `--body`.

## 7. Savings estimate
| fix | basis | saving |
|---|---|---|
| Daylight and closed-mouth template + editing passing stills | Charlotte from 42% to ~65% pass | ~150-250 cr/month |
| Gate stills before video + 1-reroll cap | | ~300-500 cr/month |
| Soul for Charlotte | | ~80% cheaper per passing still |
| Banned combos | Golf/Kling and Wan repeats alone were 280+ cr | |
