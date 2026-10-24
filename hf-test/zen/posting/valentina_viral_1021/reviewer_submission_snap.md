# STATUS: NOT READY / NOT SUBMITTED (2026-10-21 22:50 EDT). The face gate fails on every shot-2 render; no cut was built. Not posted.
v3 round 2 (folder v3/), Samuel-approved spend:
- Closed-mouth sundress still, job a7e9df9b, 2.5 cr: v3/S2b_raw.png, gate .794.
- 2 still variants (keep s2_b smirk), jobs f473bd6c and f203cdb1, 5 cr: v3/S2c1.png .817, S2c2.png .767.
- Sundress clip from S2c1, Kling, job 71896d81, 7.5 cr: v3/kS2b.mp4. FAIL: .69-.80, only 0.05-0.45 s >= .78.
- Pool clip from approved test2 s5_a (.885), Kling, job cf563027, 7.5 cr: v3/kS2pool.mp4. PARTIAL: 0.05-1.45 s .80-.92, 1.55-2.65 s .73-.77, 2.75-3.75 s .79-.81, 3.85-4.05 s .77-.78, 4.15-4.95 s .79-.83.
- The snap clip v3/kS1.mp4 (job c5e3a0a0) still passes: .885-.915 over 0.05-2.25 s.
Credits: v3 round 1 17.5 + round 2 22.5 = 40 for the re-render (Higgsfield transactions confirm 2.5+2.5+2.5+7.5+7.5 this round). Batch total = 57.5 + 40 = 97.5.
Blocker: shot 2 has no passing span longer than ~1.4 s, so the cut comes to < 7.5 s without jump cuts or slow-mo.
---- earlier notes below ----
# STATUS: NOT READY. v2 FAILED reviewer realism (Notion 400f2994-9b29-81df-81c6-c80e6ddb9024); v3 re-render in progress, blocked on credit cap (2026-10-21 18:45 EDT). Not posted, not scheduled.
v3 (folder v3/): spent 17.5 of the 20 cr cap.
- New snap clip, Kling 3.0 + Element, job c5e3a0a0 (7.5 cr): v3/kS1.mp4, 828x1108. The snap is crisp: thumb and middle finger press together at 0.9-1.8 s and release at ~2.0 s. Usable span 0.05-2.25 s; after 2.4 s it turns into an open-palm wave with motion blur, so cut before that. Face gate at 10 fps: min .885, all pass.
- Sundress still on a plain whitewashed wall with the sea, Seedream, job 24ea7bc2 (2.5 cr): v3/S2_raw.png. Gate .81. Toothy smile.
- Sundress clip, Kling 3.0 + Element, job 7ccd8cf8 (7.5 cr): v3/kS2.mp4. Face gate FAIL: only 0.05-0.85 s is >= .78, and the rest is .65-.77, with the smile widening and the head tilting. Unusable.
- Needed: one more sundress clip at 7.5 cr, plus 2.5 cr for a closed-mouth start still, which takes the batch over the 20 cr cap. Waiting on Samuel.
---- previous (v2) submission below ----
# STATUS: READY for JSW Content Reviewer, resubmission (2026-10-21 18:25 EDT). The first submission failed review for blur bands on shot 1; shot 1 is now a full-frame cover crop. Not posted, not scheduled.
To: JSW Content Reviewer. This is Valentina's first viral attempt: a "finger snap" getting-ready swipe (Cartagena trip with mom and the tías, Wed Oct 21 beat).

Transition: FINGER SNAP. Her hand is raised beside her shoulder, away from her face, with a synthetic snap click on the cut. It's not a hand-over-lens or match cut.
Format: this-to-that swipe. Shot 1 is the grey tank on her tía's Bocagrande balcony (approved test2 s2_b as the start frame). Snap. Shot 2 is a yellow linen sundress on a colonial balcony in the walled city. Calm, soft smiles throughout, no laughs.
Framing: shot 1 now uses a full-frame cover crop. kB1 (828x1108, 3:4) is scaled to 1435x1920 with its aspect kept, then cropped to 1080x1920 with the horizontal center at 45%, so the face is near center and the snap hand stays fully in frame. No stretching and no blur bands. Shot 2 (kB2, 720x1276) is scaled to 1080 wide with its aspect kept and fills the frame. Text sits in the top band only (y=70).
Trims: kB1 to the snap, then kB2 0.05-1.60, then kB2 2.25-4.95 with a gate dip removed (3.25-3.45 on TikTok and Reels, 3.25-3.55 on YT). Build config: work/s3_cover.json.

| Platform | File | md5 | Len | Size | Snap at |
|---|---|---|---|---|---|
| YouTube Short | final/valentina_snap_ytshort.mp4 | bd3d7711451327834ba2a983f12784a0 | 8.20 s | 3.7 MB | 4.20 s |
| YT thumb (1080x1920) | final/valentina_snap_ytshort_thumb.jpg | c8a1f242ebda9c813dfcb73d052b65ea | frame 5.0 s, face .853 (text overlay only flag) | | |
| TikTok | final/valentina_snap_tiktok.mp4 | a8b729b5e3624733609738d5ce0ea19a | 7.55 s | 3.5 MB | 3.45 s |
| Reels/FB | final/valentina_snap_reels.mp4 | a38eaa3844c0779a81e58fc7b96f4af5 | 7.97 s | 3.7 MB | 3.85 s |
All files: H.264 Main, yuv420p, faststart, 1080x1920, 30 fps, AAC 48 kHz (checked with ffprobe).

On-screen text
- YT: 'my tía: "we leave in 5, mija"' (0-4.25), then "me, one snap later:", then "Cartagena ready. who's waiting on who?" (to 8.2 s)
- TikTok: "Cartagena family trip be like:", then "hora colombiana, but make it fast"
- Reels: "send this to the friend who's never ready", then "Bocagrande morning to old city afternoon"

Captions
- YT Short: "my tía said 5 minutes. I said one snap 🫰🇨🇴 who's always late in your family? #cartagena #colombia #shorts #latina #travel"
- TikTok: "Cartagena family trip: getting ready in one snap 🫰 who's the late one in your family? #cartagena #colombia #grwm #colombiana #travelcolombia"
- Reels/FB: "Cartagena, from balcony coffee to old city in one snap 🫰 send this to the friend who's never ready #cartagena #colombia #latina #travelreels"
- Music credit, in every description: Music: "Samba Isobel" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0
- No AI wording, no Fanvue, no dating tags.

Gate (identity_gate.py unchanged, Valentina pack, bar .78 on every scored frame, final exports at 10 fps)
| Cut | Frames | Min (at) | Median | Below .78 | Result | Log |
|---|---|---|---|---|---|---|
| YT Short | 81 | .785 (6.35 s) | .834 | 0 | PASS | qc/gate_snap_ytshort_cover.txt |
| TikTok | 75 | .781 (5.55 s) | .835 | 0 | PASS | qc/gate_snap_tiktok_cover.txt |
| Reels | 79 | .784 (4.95 s) | .833 | 0 | PASS | qc/gate_snap_reels_cover.txt |
Start stills: s2_b (approved) .888. B2c sundress (Seedream job ba09ba9e) .851.

Side-by-side: qc/snap_cover_sidebyside_vs_test2.jpg (valentina_test2_contact_sheet.jpg on the left, then 6 YT frames at 1.0, 2.5, 3.9, 4.6, 5.5 and 7.5 s at the same height).
Body and hair note: proportions are now natural; the old stretch is gone. The build matches the refs: slim-athletic, narrow waist, softly curved hips, full natural bust in both outfits. The sundress reads a touch fuller in the bust than s2_b, which is within range. Hair matches: dark brown, long, loose high-volume waves past the shoulders. No tattoos. Skin is matte, with a slight Kling smoothness in the sundress shot.
Visual check: hands are 5-fingered. The snap hand is raised beside her shoulder and is a little soft at the snap, but not fused. Nobody is in the background and there's no scene text. Hair moves in the breeze. Watch for a slightly fixed smile in the sundress span. The trims weren't changed for this: the sundress frames sit at .78-.80, and any re-trim risks the gate and the 7.5 s minimum.
Thumb: unchanged. It's taken from the sundress shot at 5.0 s, which shot 1's crop doesn't affect.

Credits: 57.5 total for the batch (Valentina viral 1021). This Short used Kling 2 x 7.5 = 15 (kB1 134103a9, kB2 1b72baa5), plus Seedream for B2c and the failed B2a/B2b first pass. The re-export and gate fixes used 0 credits.
Platforms: YT Short, TikTok, Reels/FB (one file each).
