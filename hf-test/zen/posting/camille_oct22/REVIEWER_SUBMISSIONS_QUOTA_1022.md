# Camille Dubois — Reviewer submissions, Friday quota batch (Oct 22, 2026, partial)
Written 9:27 PM EDT. Only items that are already gated and passing are listed here. No videos are ready yet: every video cut now has to be at least 7 s, and the v2 cuts (TT1/TT2/TT3) have not been gated. Nothing has been posted or scheduled.
Pipeline: Seedream v5 single-ref edits of approved camille_v3 finals, then finish_v4C, then a 1080x1920 crop. Gate: identity_gate img --model camille_v3, PASS at >=0.78. A by-eye body/outfit check was OK on all of them (qc/sheet_stills.jpg). All images are SFW, matte skin, closed-mouth smile, and she is alone in every shot. Captions don't mention AI or other platforms.
AI labels to set at scheduling: Meta AI info ON for IG; Reddit gets the profile-sub disclosure flair if available.

| # | Platform | File | md5 | Gate (centroid/best) |
|---|---|---|---|---|
| 1 | IG Story 1 | quota/platform/ig_story1_Q1_lane.jpg | 70ffdada9eede6abf31233a31c1c4b6e | 0.828 / 0.855 PASS |
| 2 | IG Story 2 | quota/platform/ig_story2_Q4_bakery.jpg | 799c7f4562e8732767cfdce3246686bf | 0.802 / 0.804 PASS |
| 3 | IG Story 3 | quota/platform/ig_story3_Q5_rooftop.jpg | 6831d2f6059a9308898137e549c70ebd | 0.853 / 0.843 PASS |
| 4 | Reddit 1 | quota/platform/reddit1_Q2r_market.jpg | 60f30e0ced28391ea9e188b507169fd0 | 0.780 / 0.799 PASS |
| 5 | Reddit 2 | quota/platform/reddit2_Q3_promenade.jpg | c08526b82765e76ba151fc9856d14da4 | 0.785 / 0.797 PASS |
| 6 | X (still) | quota/platform/x4_Q6_records.jpg | 3ecefd406e5eff2f05a41c296189a22e | 0.793 / 0.772 PASS |

## Captions
1. IG Story 1 (lane, holding the vinyl). On-image text: "new album out now · link in bio". Link sticker: Apple Music album. IG AI label: ON.
2. IG Story 2 (bakery). On-image text: "first stop: the boulangerie". IG AI label: ON.
3. IG Story 3 (rooftop, blue hour). On-image text: "bonsoir, Nice". IG AI label: ON.
4. Reddit 1. Subreddit: Camille's own profile sub, r/u_Pristine_Culture_693 (u/Pristine_Culture_693).
   - Title: "Saturday mornings at the market in Nice ☀️"
   - AI-rule check: profile subs have no AI-image ban. Don't crosspost to r/selfie or r/Munich, which ban AI (SHARED_LEARNINGS).
5. Reddit 2. Subreddit: r/u_Pristine_Culture_693.
   - Title: "Sea breeze and no plans on the Promenade 🌊"
   - Same AI-rule check as Reddit 1.
6. X: "Digging through crates on a slow afternoon. Riviera Après Minuit is out now on Apple Music 🎶 https://music.apple.com/us/album/riviera-apr%C3%A8s-minuit/6825779566"
   - Reviewer note: the record covers in the background have printed faces on them. Please confirm this is OK.

## Format mix
3 stories and 3 feed stills, with no format used more than twice per platform per day.

## Not ready yet (follow-up run)
- Videos still to make: TT x3, IG Reel, YT Shorts x2, X videos. All must be ≥7 s.
- v2 specs are built: TT1 = L4 cut (8.0 s), TT2 = K1+P5 (8.5 s), TT3 = L5 cut at 0.9 speed (8.0 s). They have not been exported or gated.
- Raw 10 s clips: L4 .783/.699, L5 .811/.682 (windows trimmed to avoid the dips), L1 .729 FAIL. L2 was rejected because a background person appears, and L2r is the redo. The L3, L6 and L2r gates are still pending.
- export_pad.py (blur-pad, no unsharp or grain) keeps scores at raw level. The old crop+unsharp chain lost about 0.02.

## Credits
- 55.0 confirmed: 7 Seedream x2.5 and 5 Kling std 5 s x7.5.
- Also used, cost not yet looked up: 3 Kling pro 5 s (P3, P4, P5) and 7 Kling pro 10 s (L1–L6, L2r).

## Update 10:35 PM EDT: TikTok cuts (8 s+) and a replacement X still
These were made with the blur-pad render (export_pad.py, no unsharp or grain) and gated with vgate at 0.1 s steps against camille_v3. PASS means median ≥0.78 and no frame below 0.70.
All source clips are static with feet planted: no walking, no talking, no lip-sync. By eye, nobody else is in any shot and body and outfit stay consistent (qc/sheet_P.jpg, qc/sheet_L.jpg, qc/sheet_clips_raw.jpg). On-screen text and captions don't mention AI or other platforms. When scheduling, turn TikTok's "AI-generated" label ON. Post the music version (.mp4); the _silent.mp4 is the gate copy.

| # | Platform | File | md5 | Duration | Gate med/min |
|---|---|---|---|---|---|
| 7 | TikTok 1 | quota/final/camille_oct22q_TT1_baguette.mp4 | 2f7cd89e8e1dcbba58b42492132368cf | 8.33 s | 0.796 / 0.748 PASS |
| 8 | TikTok 2 | quota/final/camille_oct22q_TT2_album_lane.mp4 | b712cdd594a0e4894ae788ea5f93555e | 8.83 s | 0.801 / 0.747 PASS |
| 9 | TikTok 3 | quota/final/camille_oct22q_TT3_bluehour.mp4 | 4b9358e84ff405d05b02e399eb73b240 | 8.33 s | 0.827 / 0.766 PASS |
| 10 | X still (replaces failed x4_Q6) | quota/platform/x4b_Q8a_balcony.jpg | 611df3d729e4fb68fa45e1c027462212 | still | centroid 0.815 / best 0.824 PASS |

### TikTok 1: bakery (clip L4 0–6 s, then 8–10 s, jump cut)
- Opening shot: a planted, smiling hold in the boulangerie.
- On-screen text: "things France got right:" / "1 baguette" / "0 regrets"
- Music: Petit Déjeuner
- Caption: "the only morning routine I need 🥖 #nice #france #boulangerie #frenchgirl #morningroutine"

### TikTok 2: album (clip K1 lane sway holding the record, then a P5 rooftop hold)
- On-screen text: "POV: your album is finally out" / "Riviera Après Minuit" / "link in bio"
- Music: Rue de Paradis
- Caption: "Riviera Après Minuit is out now on Apple Music 🎶 link in bio #newmusic #frenchpop #nice #rivierachic"

### TikTok 3: blue hour (clip L5 0–3.4 s, then 6.2–10 s, at 0.9 speed; head-tilt dip cut out)
- On-screen text: "blue hour in Nice" / "hits different"
- Music: Bonsoir Monaco
- Caption: "bonsoir from the rooftops ✨ #bluehour #nice #cotedazur #rooftop #frenchriviera"

### X still: balcony with the album (replaces x4_Q6)
- The sleeve is blank and the background is sea and sky, so there are no faces or covers anywhere.
- Process: Seedream single-ref edit of S1a, then skin_local and finish_v4C.
- Caption: "Sea view, one record on repeat. Riviera Après Minuit is out now on Apple Music 🎶 https://music.apple.com/us/album/riviera-apr%C3%A8s-minuit/6825779566"
- Note: Ideogram edit not tried. The tip came in after this regen had already passed the gate.
