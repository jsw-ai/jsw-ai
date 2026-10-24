# JSW content process: DRAFT for Samuel to review (2026-10-19)
Status: DRAFT ONLY. Nothing in routines, skills, Notion or posting has been changed. **All six model bots stay ON HOLD (no creating, no posting) until you lock this.**
Sources: jsw-daily-content-process/SKILL.md, MODEL_CONTENT_PROCESS.md, CONTENT_RECIPE.md, LIPSYNC_METHOD.md, CONSISTENCY_RESEARCH*.md, SHARED_LEARNINGS.md (Oct 14-19), low_tide_lover/NOTES.md, identity_packs.json, posted logs.

## Summary (10 lines)
1. One pipeline for all six: Plan → Create → Self-check → Review gate (another bot) → Samuel approval → Schedule → Post/verify → Track → Learn.
2. Every shot starts from that model's APPROVED face/body photos. Only scene, pose and outfit change. No hoping a random generation looks like her.
3. Photos: Seedream 5.0 Pro ref-edit (2.5 cr) for everyone except Sienna, who uses only her Soul "Sienna Blake" (0.12 cr).
4. Video: Kling 3.0 Element plus an approved, pre-checked start still (7.5 cr per 5 s, sound off). Wan 2.7 only for singing/lip-sync to real audio.
5. The real gate is a by-eye side-by-side of face AND body against the approved refs (start/middle/end frames for video). The face script (0.78 cutoff) only confirms.
6. Bots never approve their own work. A different bot (or a dedicated review bot) passes or fails it. Then you see the exact file and caption per platform.
7. Nothing gets scheduled without your explicit yes on that exact file. Before any batch, check the posted log and Ayrshare history (no reposts).
8. Every Higgsfield job is quoted with get_cost first and logged from transactions, not from the shared balance.
9. Tracking is broken today: the daily pull was never built, the tracking CSVs are empty, and Ayrshare analytics worked for only 1 of 6 profiles. A tracking bot would own this.
10. Before we unpause, you need to decide on the open items in section 6 (pack approvals for Valentina/Camille, review-bot setup, budget caps, cadence).

---
## 1. One-page overview
| # | Stage | Who | Output | Gate to next stage |
|---|---|---|---|---|
| 1 | Plan | Model bot (+ proposed Research bot weekly brief) | Day plan: 3 items max, ~70% video, captions, verified events only | Plan has no unverified events and no reposts |
| 2 | Create | Model bot | Start still(s), then clip(s), from approved refs only | Cost quoted first; locked recipe used |
| 3 | Self-check | Model bot | Side-by-side sheet + gate JSON | Bot's own sheet passes (it **cannot approve**, only reject) |
| 4 | Review gate | Peer bot (or proposed Review bot) | PASS/FAIL + reasons | PASS by someone who is not the creator |
| 5 | Samuel approval | Samuel | "Yes" on the exact file + caption per platform | Explicit yes. "Post now" with no file named does not count |
| 6 | Schedule | Model bot | Ayrshare post id + time | Posted log + Ayrshare history re-checked |
| 7 | Post / verify | Model bot | Live links | Each link opened live; failures reported as failures |
| 8 | Track | Proposed Tracking bot | Daily row per post in one sheet | Numbers pulled live, not estimated |
| 9 | Learn | Model bot + Research bot | SHARED_LEARNINGS entry; weekly summary to Samuel | |

---
## 2. Each stage in detail

### Stage 1: Plan (daily, model bot)
Inputs: weekly brief (proposed Research bot), PLATFORM_FORMAT_PLAN.md, the model's posted log, Ayrshare history.
1. Max 3 posts per model per day, ~70% video, ≤30% stills, stills as carousels only (no single photos; Instagram and TikTok get reels).
2. Any real-world event (sports, news, weather, holiday, trend) is live-searched and its source cited **before** generating, because spoken lines get baked into the video. Never invent one. If it can't be verified, use a neutral line.
3. No-repeat check: list candidate files and compare them against `<model>_posted_log` (filename + frame hash) **and** Ayrshare `/api/history` with that model's Profile-Key (Valentina etc. need both keys or you get error 221). Drop matches.
4. Captions: no AI mention (caption, hashtags, on-screen text, spoken line, bio). No Fanvue links except Sienna. No NSFW on SFW platforms.
5. Write a cost estimate for the day (section 4 prices) and stay under the cap.
Log: `posting/<model>_<date>/PLAN.md`.

### Stage 2: Create (model bot)
Rule: each still is a **fresh** edit from the original approved refs. Never chain edits, never generate from scratch.
**Stills (all except Sienna):** Seedream 5.0 Pro ref-edit, 2.5 cr each, 9:16 (3:4 only for carousels if you agree).
1. Refs: photo 1 = approved face ref, photo 2 = approved body ref (both ≥1000 px, re-uploaded each time because media IDs are temporary; the PUT needs `If-None-Match: *`).
2. Prompt = "New scene: <scene, outfit, angle, expression>" + "Take the face exactly from photo 1 … body proportions as in photo 2 (<body spec line>)" + realism block (candid phone photo, matte skin, pores, light makeup, no text, no other people, no signs/logos).
3. Use 2 refs only. A third face ref made Madison older/gaunt.
4. Expression: half-smiles and soft smiles hold identity. Fully neutral or looking-away faces fail. Put the expression first in the prompt.
5. Single-ref "keep everything, change only X" edits (light/skin, mouth, outfit kept the same) are the natural-face recipe (Valentina/Camille natural_v4).
**Stills (Sienna only):** Soul 2 + Soul "Sienna Blake" `ba97f512`, 9:16, 2k, 0.12 cr. Expression sentence FIRST ("MOUTH CLOSED … no teeth"), then the realism block ("bare natural face, almost no makeup … not airbrushed"), with the light restated. No Seedream for her.
**Finish (stills):** v4C finish (light skin texture, no blur, mild sharpen). Use the lighter texture (0.15, `finish_v4Clite.py`) when freckles get amplified on small faces. Heavy grain looked worse. Check raw vs finished face crops.
**Video (default): Kling 3.0 Element**, std, 5 s, 9:16, 720p, sound OFF = 7.5 cr (10 with sound).
1. Element = 3 approved, matte, clothed stills (front face, 3/4 face, waist-up body). Creation is free and instant. Reuse it, don't duplicate it.
2. Start still = an approved still with a soft closed-mouth smile, waist-up, face large, hands resting on an object if visible. **Pre-check the start still at ≥0.80** (a 0.749 start gave 0.68-0.72 frames, while a 0.839 start gave 0.79-0.86).
3. Prompt: low motion only. Always include: "looking straight into the camera from the very first frame to the last", "does not look down, does not turn her head, does not close her eyes", "quick natural blinks only", "keep the face identical to the first frame", "matte skin, no sheen, skin stays dry and matte", "camera locked, no zoom", no speech. Don't add glance or head-turn motions.
4. Expect an opening blink and eyes closing near the end. Trim the head/tail (3.6-3.8 s clips are fine) instead of paying for a retry.
5. Finish: scale to 1080x1920, luma unsharp 0.3-0.45, light grain (3), natural grade (no orange, no vignette), strip audio/metadata.
**Talking / lip-sync:** Seedance 2.0 i2v + the model's locked voice mp3, ~36 cr per 8 s 720p (22.5 per 5 s). It drifts face/bust over the clip, so it needs the strictest audit. **Singing to a real track:** Wan 2.7 (16.5 cr per 11 s 720p; 1080p is 2.5 cr/s). Seedance re-sings the song instead of following it.
Don't use: Seedance multi-reference for identity (failed), Nano Banana / GPT Image (wrong face / blocked), outpaint on faces (softens them; paste the original back), Soul retraining.
Log: job ids, preflight cost and actual charge (from transactions) in `<model>_<date>/JOBS.md`.

### Stage 3: Self-check (model bot; can reject only, never approve)
1. Sheet: approved face ref + body ref next to the still, or next to video frames at **start, middle and end** (4-6 frames, including 3-5 s where drift shows).
2. Face script: `identity_gate.py img --source seedream` on the still and on ~10 evenly spaced video frames. **0.78 cutoff for everything.** Within ±0.01 counts as borderline. Use the right pack (e.g. `camille_v3_draft`, not `camille`).
3. Eyes: landmark eye-aspect check (camille_oct19/work/eyes.py) or a 4 fps strip. 4 or more low samples in a row = closed-eye moment = trim or fail.
4. By-eye list: face (jaw/cheek width, eyes, nose, lips), body (bust, waist, hips, shoulders), hair colour, hands/fingers, no text/signs/logos, no background people, no gloss/airbrushing, no odd arms or tattoos, props match the caption. For talking clips: the whisper transcript matches word for word and the accent matches.
Log: failures go to `reject_log.jsonl`; the sheet goes in the batch folder.

### Stage 4: Review gate (another bot)
Current pairs disagree between docs (see Contradictions). Proposed lock: Camille↔Charlotte, Madison↔Valentina, Gabriela→Madison, Madison→Sienna, OR a single Review bot for all six.
1. The reviewer opens the sheet and the original approved refs itself (it doesn't trust the creator's sheet labels).
2. It applies the 6-point PEER REVIEW CHECKLIST (SHARED_LEARNINGS, Oct 17): face+body vs refs; hands/text/tattoos/gloss/background people; events verified; no AI/Fanvue/NSFW; persona fit; not a repeat and format fits the platform.
3. It posts PASS/FAIL with reasons. FAIL goes back to Stage 2. It never fixes the file itself.
Log: `<model>_<date>/REVIEW.md` + a one-line entry in SHARED_LEARNINGS.

### Stage 5: Samuel approval
1. One message per model: the exact final file(s), the side-by-side sheet, captions **per platform**, the planned time, the credits spent, review PASS by whom, and posted/unposted flags.
2. Only a yes that names those files counts. Status facts in the message (account linked, post live, etc.) are checked live or labelled "unverified".
Log: approval time + wording in `<model>_<date>/APPROVAL.md`.

### Stage 6: Schedule
1. Re-check the posted log + Ayrshare history (and native schedules, e.g. FB Meta Business Suite, because deleting in Ayrshare does not clear native schedules).
2. Schedule via Ayrshare with the correct Profile-Key (Sienna = primary profile). Skip known-blocked platforms and say why (e.g. Madison X suspended, Sienna YouTube appeal, Reddit SFW subs ban AI).
3. Only the approved file and the approved caption, byte for byte.
Log: Ayrshare id, platforms and time (ET) in the posted log.

### Stage 7: Post / verify
1. After the post time, open every link live, check the handle is the right one (Charlotte's TikTok went to a different handle once), and report the links.
2. Append file, hash, platform, URL and date to `<model>_posted_log`.

### Stage 8: Track (see section 5). Stage 9: Learn
Weekly: tally rejects by recipe, top/bottom posts by views, and send Samuel a one-page summary plus any proposed recipe change. **Recipe changes need Samuel's OK before they become "locked".**

---
## 3. Per-model locked recipe
| Model | Ref pack status (identity_packs.json) | Photo route | Video route | Approved refs | Known failure modes |
|---|---|---|---|---|---|
| **Sienna** | Pack rebuilt Oct 14 from approved finals; no explicit "approved" flag in the JSON | Soul 2 + Soul `ba97f512` only, expression first, realism block, v4C | Kling Element (Element `20786f58` Sienna-LTL-tee) for story shots; Wan 2.7 for singing. Kling for general reels is **UNPROVEN** for her outside the song test | `sienna_refs/` (story1_a, story2_a, story3_b, reddit_x1_b, x2_dawn v4C + T1 frames); body ref x2_dawn_v4C | Toothy smiles; glam makeup/contour by default; rings, headstock logos, signs; bust reads larger than refs; raw Soul start stills looked AI in video; Body Soul `50583a87` not approved |
| **Camille** | JSON "camille" = OLD look (approved Oct 14). Current look = `camille_v3_draft`, **UNAPPROVED in JSON**; natural_v4 sheet made Oct 19 | Seedream single-ref edit of the v4 tiles, same outfit; v4C | Kling Element `e3a57e1a` (Camille-v4-natural), passed 8/8 frames Oct 19 | natural_v4 face1/face2/body1_v4C (approval **UNPROVEN**, see open decisions) | Gloss/pinkish lips late in clips; looks down at held objects; bust smaller in plain tops |
| **Charlotte** | Approved Oct 19 04:15 ET (charlotte_ref/ref_sheet.jpg) | Seedream 2-ref (fd8e810e/b8d45ca6), fitted scoop-neck tops; v4C | Kling Element `8f87f513` + closed-mouth start: PASS 8/8 Oct 19 | charlotte_ref/ref_sheet.jpg; keepers face/body | Crew-neck/knit = smaller bust; open smile collapses to a smirk; footballs warp; c7 has pedestrians |
| **Madison** | Approved Oct 14 (Look A) | Seedream 2-ref (m_face 1600 + m_body), "slim … natural modest bust not enlarged", round-face wording, 2 variants and keep the best; v4C-lite | Kling Element `6705eac1` + start ≥0.80; trim tail | reference_set_madison.png; keepers face/body | "Very full bust" wording overshoots; 3rd ref = older face; closed/look-away faces fail; camera pull-back; freckles amplified by finish; X suspended |
| **Gabriela** | Approved Oct 14 | Seedream 2-ref + explicit BUST MATCH wording, low scoop tops; v4C | Kling Element `8b128aab`: body/hands PASS, face borderline (laugh squint). **"Smile with eyes open" fix UNPROVEN** for her | reference_set_gabriela.jpg; keepers/gabriela_refs | Bust shrinks in plain tees; laugh squint drops identity; thigh proxy unreliable |
| **Valentina** | JSON says **DRAFTED_UNAPPROVED**, but notes treat the test2 stills as approved | Seedream single-ref edits (natural-face recipe), round-oval face wording, modest bust | Kling Element `0950a489` + approved test2 start: Samuel PASS by eye Oct 19 4:17 AM ET | valentina_test2/fin/*, cover, bikini1/2 (per audit) | Video drift: narrower face, hollow cheeks, bigger bust; arm/tattoo artifacts at frame edges (crop them out); Seedance lip-sync clips failed the audit |
Talking (Seedance) and singing (Wan) are **UNPROVEN as "locked"** for every model under the new by-eye HARD GATE. Only the Kling Element route has passed by-eye checks (Valentina by Samuel; Charlotte, Camille and Madison by the bots themselves).

---
## 4. Cadence and credit guardrails
**Daily (per model):** plan by 9 AM ET → create → self-check → review → one approval message to Samuel → schedule only approved items. Max 3 posts per day.
**Weekly:** Research brief (Mon), reject tally + performance summary (Sun), pack/recipe changes only with Samuel's OK.
**Real per-job costs (preflighted, from the notes):**
| Job | Credits |
|---|---|
| Soul 2 still (Sienna) | 0.12 |
| Seedream 5.0 Pro edit (2k) | 2.5 |
| outpaint_image | 2 |
| Kling 3.0 std 5 s, sound off / on | 7.5 / 10 (4 s = 6, 3 s = 4.5) |
| Kling 3.0 pro 5 s | 8.75 |
| Seedance 2.0 720p 5 s / 8 s | 22.5 / ~36 |
| Seedance 2.0 11 s 720p | 49.5 |
| Wan 2.7 720p 11 s / 1080p per sec | 16.5 / 2.5 |
| Element creation | 0 (observed) |
| upscale_video | unknown (no preflight) |
**Proposed guardrails (for you to set):**
1. Typical day (2 Kling clips + 1 carousel of 4 stills + ~3 retries) ≈ 2×7.5 + 4×2.5 + ~15 = **~40 cr per model, ~240 cr for all six**. The observed real days were Camille 27.5, Charlotte 32.5 and Madison 57.5.
2. Hard cap per model per day (proposal: 40 cr), and a 2-retry cap per item, then stop and report.
3. If a batch's pass rate is below 30%, stop and change the recipe (existing rule).
4. get_cost before every job. Report spend from **/transactions by job id**, never from the balance difference (the balance is shared, and other bots spend at the same time).
5. No credit purchases or auto top-up.

---
## 5. Tracking plan and what's broken
**Broken now (verified from files):**
- The daily pull was never built. `gabriela_tracking.csv` has only a header; `madison_tracking.csv` has rows with empty numbers.
- Ayrshare analytics worked for 1 of 6 profiles (per your brief; I found no file on the box documenting which one).
- Posted logs are inconsistent: different formats and places (sienna/gabriela `.md`, madison/valentina `.json`, charlotte at `/workspace/hf-test/charlotte_posted.log`, none for Camille found).
- Ayrshare state doesn't always match reality: Madison montage1 still "pending"; native FB schedules not visible to Ayrshare; a Charlotte post landed on the wrong handle.
**Proposal (Tracking bot):**
1. One Google Sheet: date, model, platform, post URL, file, views, likes, comments, shares, follows gained, source (API/manual).
2. Daily 9 AM ET pull: Ayrshare analytics per post where it works; for the rest, a platform-native or manual read (AdsPower profile) labelled as such.
3. First job: figure out why analytics fails for the other 5 profiles (profile keys, platform linking) and report it. Don't guess numbers.
4. One posted-log format for all six (JSON: file, hash, platform, url, ayrshare_id, date_ET), and keep it in sync with the sheet.

**Where the 3 proposed support bots plug in (not decided):**
| Bot | Plugs in at | Does | Doesn't |
|---|---|---|---|
| Research | Stage 1 (weekly, Mon) | Niche/platform brief, trends, verified-event list with sources | Create or post |
| Review gate | Stage 4 | PASS/FAIL on every item vs approved refs + checklist | Fix files, approve its own work, post |
| Tracking | Stages 7-9 | Daily metrics sheet, posted-log hygiene, weekly top/bottom | Post, engage |
| (Later) Engagement | After Stage 7 | Human-style replies/likes via AdsPower | Separate project; not in scope now |

---
## 6. Open decisions for Samuel
1. Approve the Valentina pack formally (JSON says DRAFTED_UNAPPROVED; is test2 + cover + bikini1/2 the locked set?).
2. Approve Camille's current look/pack (natural_v4 sheet vs camille_v3_draft; JSON "approved" points to the OLD Camille).
3. Confirm Sienna's locked ref set and whether Kling Element is OK for her general reels.
4. Review gate: peer pairs (and which pairing) or one dedicated Review bot?
5. Approval cadence: per day per item (this draft) or one week-batch (MODEL_CONTENT_PROCESS.md rule zero)?
6. Daily credit cap per model (proposed 40) and retry cap (proposed 2).
7. Are talking (Seedance) and singing (Wan) clips allowed before they pass the by-eye HARD GATE route, or Kling-only until then?
8. Which support bots to start (Research / Review / Tracking) and in what order.
9. Carousel aspect: 9:16 everywhere, or 3:4/4:5 allowed for carousels?
10. What happens to already-scheduled items (e.g. Valentina's Oct 22 4:30 PM ET post, Madison montage1 "pending") during the hold?

---
## Contradictions found between existing docs
1. **Approval cadence:** MODEL_CONTENT_PROCESS.md: "Sam approves once per week-batch, never per photo." CONTENT_RECIPE/LIPSYNC/SKILL: you see every final file + exact caption.
2. **Who posts:** MODEL_CONTENT_PROCESS/CONTENT_RECIPE/LIPSYNC: "bots never post." SKILL.md step 6: bots post via Ayrshare after approval, and bots did schedule (Valentina, Madison).
3. **Peer pairs:** SKILL.md: Camille→Gabriela, Gabriela→Madison, Madison→Camille+Sienna, Valentina↔Charlotte. SHARED_LEARNINGS Oct 17: Camille↔Charlotte, Madison↔Valentina, Gabriela↔Madison, Madison→Sienna.
4. **Gate thresholds:** MODEL_CONTENT_PROCESS §3.1: video 0.55/0.52. SHARED_LEARNINGS Oct 19: 0.78 for everything. LIPSYNC: "≥85% frames".
5. **Sienna route:** MODEL_CONTENT_PROCESS §0a/§2 and CONTENT_RECIPE allow a Seedream fallback / gpt_image_2 body fix. Your rule: Soul only, no Seedream. SKILL.md says Seedream is the best still model generally.
6. **Video model:** MODEL_CONTENT_PROCESS/CONTENT_RECIPE/LIPSYNC say Seedance 2.0 i2v. SKILL.md and the Oct 18-19 notes say Kling 3.0 Element.
7. **Finishing:** MODEL_CONTENT_PROCESS §4 says Skin Enhancer "Realistic Skin" on every still (but notes say it isn't exposed via MCP and wasn't used); CONTENT_RECIPE says "light grain"; v4C amplified freckles; you said heavy grain looks worse.
8. **Sienna refs:** CONTENT_RECIPE §4 checks against `sienna_face_close`/`bikini1` and §1 uses `sienna_bikini1` as the Soul ref; MODEL_CONTENT_PROCESS §0a dropped those older refs (and NOTES.md used `sienna_cover` as a start still).
9. **Pack status:** identity_packs.json says Valentina DRAFTED_UNAPPROVED, while CONSISTENCY_RESEARCH says the "Madison/Camille/Valentina packs [were] approved with fixes." Camille "approved" = the old look.
10. **Real events:** SKILL.md "encouraged" vs the Oct 17 hard rule's stricter "only if verified, else neutral" (compatible, but the tone differs).
11. **Aspect:** MODEL_CONTENT_PROCESS defaults to 3:4 stills. Your rule and NOTES.md say 9:16.
12. **Posted-log location/format** differs per model (see section 5).
13. **"Openly AI" bios** in older persona transcripts (LIPSYNC §8) conflict with the no-AI-mention rule.
