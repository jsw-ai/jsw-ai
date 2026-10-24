# JSW process docs: conflict review and draft rulings (2026-10-21)

Prepared Wed Oct 21, 2026, about 11:45 AM EDT. Read-only review: nothing in Notion or the skills was edited, and no messages were sent.

**Sources read:** 9 Notion pages (Scheduler SOP, Researcher, Tracker, Sienna, Gabriela, Valentina, Camille, Charlotte, Madison; fetched 11:37-11:42 AM EDT), all 13 `jsw-*` skills (review-gate, scheduling, weekly-content-research, stats-refresh, whats-working-notes, weekly-report, daily-content-process, gabriela, valentina, camille, charlotte, madison, sienna-creation), and `CONTENT_RECIPE.md`, `MODEL_CONTENT_PROCESS.md`, `SHARED_LEARNINGS.md` (searched, not read in full) and `identity_gate.py`. I also spot-checked `/workspace/xposts/{sienna,gabriela}.md`.

**Precedence I applied:** Samuel's settled rules (from the brief) come first. Next is the Scheduler SOP on Notion (v2026-10-21, newest). Older text loses. The Reviewer is the **JSW Content Reviewer bot** (agent 99a98fb5), not a peer model.

---

## (1) Conflicts, sources and proposed rulings

### C1. Who approves a post
- **Old rule:** `MODEL_CONTENT_PROCESS.md` line 3 ("Rule zero: no bot posts anything. Sam approves once per week-batch") and §5 ("Sam approves one week at a time… `approved/<model>/<week>/`… Nothing outside that folder is ever posted"). `CONTENT_RECIPE.md` §6 ("Sam reviews every final file and the exact caption before anything posts"). The week pages for Gabriela, Camille, Valentina, Madison and Charlotte ("nothing is posted without Samuel's approval"). The Notion "JSW AI Models › Process" page.
- **Current rule:** the Scheduler SOP, review-gate skill, daily-content skill step 5, and every model doc.
- **Ruling:** a JSW Content Reviewer PASS for the exact file path and version, plus the exact captions, is the approval. Retire the "approved/ folder" and the per-week Sam sign-off. The two box docs still carry the old rule and must be marked superseded.

### C2. Who reviews: peer pairings vs the Reviewer bot
- **Peer pairing:** `jsw-daily-content-process` step 4: "Camille reviews Gabriela, Gabriela reviews Madison, Madison reviews Camille and Sienna, Valentina and Charlotte review each other."
- **What actually happens:** SHARED_LEARNINGS shows Madison and Valentina reviewing each other. Valentina's skill already flags this ("Open conflicts" #2). Camille, Charlotte and Madison all name the JSW Content Reviewer bot.
- **Ruling:** drop peer pairings entirely. One reviewer, the JSW Content Reviewer bot, uses the `jsw-content-review-gate` checklist. A model may self-check, but its opinion is never a PASS.

### C3. X nudity and topless content
- **Allows topless:** `jsw-content-review-gate` step 6 ("X: spicy **or topless** content must be marked sensitive"), which reads as permission. `/workspace/review_sop.md` has the same line. Gabriela's week page and `xposts/gabriela.md` (Sun 10/25: "Topless still from behind… thong bikini bottoms only"). `xposts/sienna.md` (morning: "topless still with hair covering… bikini bottoms only", and the caption contains "[Fanvue link").
- **Forbids it:** Samuel's rule (tease only, no nudity on X). Madison's skill and Notion page, which explicitly override "the older note that allowed topless posts on X". The Gabriela skill ("No nudity off Fanvue"). Valentina ("Never nudity"). Researcher ("no nudity"). The Charlotte Notion page ("no full nudity").
- **Charlotte's claim:** Charlotte says that at 3:46 PM ET on 10/20, Samuel allowed topless photos on X if marked sensitive. **UNVERIFIED.** No ReadTranscript tool was available. I searched this bot's transcripts and memory, the workspace and the stores for "topless" and "3:46" and found no such Samuel message. The only hits were older "X subscriber lane" bible text, the review-gate line and the plans above. Charlotte's own Notion page records "no full nudity" as resolved, which does not match her claim.
- **Ruling:** no nudity, including topless, on X until Samuel confirms the 10/20 message directly. Change the Reviewer line to "spicy or tease content must be marked sensitive; any nudity, including topless, is a FAIL on X." Pull the Gabriela Sun 10/25 and Sienna villa topless ideas, or reframe them as implied, with a covered bikini top or towel. Ask Samuel one question: "Did you allow topless on X if marked sensitive (10/20 ~3:46 PM ET)?"

### C4. Fanvue links (who, where)
- **Too narrow:** `jsw-daily-content-process` step 2 says "no Fanvue links except Sienna" and omits Charlotte.
- **Vague:** the review-gate skill says "only for verified models" without naming them.
- **Link inside a post:** `xposts/sienna.md` puts "[Fanvue link" inside an X caption. That breaks "no URL in scheduled X posts, link in bio".
- **Only part of the allowed scope:** Charlotte's Notion page says "link in the X bio only" (Reddit is also allowed).
- **Consistent docs:** Camille, Gabriela and Madison ("coming soon" or "more coming soon"); Valentina (no link anywhere, including the X bio); the Scheduler SOP.
- **Ruling:** Fanvue goes on X and Reddit only, for Sienna and Charlotte only, and only in the bio or a pinned post set by hand. A scheduled post carries no raw URL. Every other model gets "coming soon" at most. Name the models explicitly in the daily-content skill and the review gate.

### C5. AdsPower and the posting route
- **Allow AdsPower posting:** `jsw-daily-content-process` step 6 ("Scheduler posts through Ayrshare (or the model's AdsPower profile)"). Valentina's Notion §6 ("Ayrshare, or headless AdsPower when no hold is active"). Charlotte's Notion §10.2 ("Ayrshare or the scheduled AdsPower route"). **Madison's Notion §12 ("Posting runs through AdsPower in headless mode only, profile k1cwwjw5")**, which conflicts directly.
- **Out of date:** the box Scheduler skill §0 only says "never open… without asking in the JSW room first". It lacks the Notion line "never posts through AdsPower (Ayrshare only)".
- **Bot uses AdsPower itself:** Charlotte's skill step 10 and Notion §10.4 say Charlotte uploads to Fanvue herself through AdsPower k1cwwgmo.
- **Ruling:** the Scheduler posts only through Ayrshare. AdsPower stays frozen for every bot, for posting, engagement, Fanvue uploads and Tracker reads, until Samuel says his Fanvue work is done. After that it runs headless only, and no bot ever touches the proxy. Charlotte's Fanvue uploads stop during the freeze.

### C6. Daily post caps vs the cadence table
- **Max 3 a day:** daily-content skill ("max 3 posts per model per day"). Camille skill ("Hard limits: max 3 posts/day"). `MODEL_CONTENT_PROCESS` §5 ("Cap 3 posts per day per model").
- **2-3 a day:** Gabriela ("2 to 3 posts a day") and the Researcher ("2-3 posts a day across platforms").
- **Max 3 per platform per day:** Charlotte and Valentina.
- **Cadence table:** the Scheduler SOP gives TikTok 3, IG 2, Shorts 2-3, FB 1-2, X 4-6 and Reddit 2-3.
- **Settled:** Madison's YouTube runs 2-3 Shorts a day, and X leads with short clips.
- **Ruling (draft, confirm with Samuel):** the Scheduler SOP cadence table is the platform cap. Read "2-3 a day" as **new source pieces per model per day** (1-3 clips or carousels, each recut per platform), not total posts. Valentina stays at 1 TikTok a day. Madison's new X (@MadisonCole69) stays at 1-3 a day during warm-up, a stricter account-specific rule. Madison's 3 PM caps review is still pending.

### C7. Video and lip-sync models
- **Seedance for all clips:** `CONTENT_RECIPE.md` §3 and `MODEL_CONTENT_PROCESS` (line 78).
- **Sienna:** step 11 uses "Sync Lipsync (sync_so)" on a Kling take instead of Seedance 2.0.
- **Gabriela:** no lip-sync model named.
- **Correct:** Charlotte (no lip-sync path), Valentina, Camille and Madison all use Seedance 2.0 for lip-sync.
- **Ruling:** use Kling 3.0 with the model's Element for silent clips, and Seedance 2.0 i2v from a gated still for lip-sync and talking. Sienna changes step 11 to Seedance 2.0. Sync Lipsync is out unless Samuel makes an exception. Gabriela adds "Seedance 2.0" to her lip-sync line. Mark CONTENT_RECIPE §3 superseded.

### C8. Identity-gate thresholds
- **Gate code:** stills need centroid ≥ 0.72, best-ref ≥ 0.74, and `seedream_centroid` 0.78. Video mode uses 0.55/0.52 with 80% of frames passing.
- **Docs:** Charlotte uses "6 frames ≥ 0.75" (her own number). Sienna and Madison use 0.78. `MODEL_CONTENT_PROCESS` still lists 0.72/0.74.
- **Sienna's command:** her Notion step 9 runs `identity_gate.py --source seedream --body` with no `img --model sienna`, which will fail argparse.
- **Ruling:** Seedream stills use `img --model <m> --source seedream --body` at 0.78. Clips use `video --model <m>` with the code thresholds, plus the mandatory by-eye body and hair check and the same-scale side-by-side. Charlotte drops the 0.75 rule. Sienna fixes the command.

### C9. Skin finish
- **Conflict:** `MODEL_CONTENT_PROCESS` §4 says Skin Enhancer "Realistic Skin" (web app, about 4 cr). Every model doc uses the local v4C (or v4C-lite) finish.
- **Ruling:** use local v4C or v4C-lite only, with no blur. Mark §4 superseded.

### C10. Reference-pack status
- **Old status:** `MODEL_CONTENT_PROCESS` line 67 says the other packs are "unapproved". Gabriela's model page says her pack is "a draft and unapproved", and the Process page says "Only Sienna and Camille packs are approved".
- **Ruling:** Gabriela's pack was approved on 10/19 (settled). Update Gabriela's model page and the Process page. Status for the other packs: Madison Look A was approved 10/14 per her page. Valentina's test2 is "approved" per her doc. Charlotte has a 4-ref order. Treat these as unverified until Samuel confirms.

### C11. Export and thumbnail
- **Mostly aligned.** Small gaps:
  - The daily-content skill's export line has no thumbnail requirement.
  - Madison allows a "1280x720 crop" thumbnail and a 720x1280 export.
  - Charlotte requires AAC audio, while others only say "sound off unless talking".
- **Ruling:** use H.264 Main, yuv420p, faststart, under 15 MB and full 9:16 with no bands. **Every Short gets `<clip>_thumb.jpg` (1080x1920, from the clip itself).** Add the thumbnail to the shared skill. Madison drops the 1280x720 option. Any added audio must be royalty-free or from the TikTok commercial library.

### C12. Music
- **Gabriela:** royalty-free Brazilian music, while her week page wants the TikTok commercial library and "trending sound (to check)".
- **Madison:** "never reuse a track", while her week page has a trending sound.
- **Ruling:** TikTok cuts use only the commercial library or a royalty-free cleared track. A trending sound is OK only when picked from the commercial library at posting time and logged. Madison's no-reuse rule stands, and a library pick counts as one use.

### C13. Weekly story and theme overlaps
- **Known clashes:**
  - Gym and squats belong to Madison this week, but Madison's own WEEK_PLAN swapped squats for pickleball on Oct 20, so the owner of "gym" is now unclear.
  - The Gabriela skill still gives "leg day" and "boat day" as examples, though her week page dropped both.
  - The pool belongs to Valentina, but Charlotte's Wed pool posts already appear in the Tracker.
  - Boats belong to Valentina.
  - First-class flights: Valentina Tue 10/20, Sienna Thu 10/22, and Gabriela has a flight beat. The Scheduler only checks Camille vs Sienna.
  - Valentina's week page puts her flight home on Wed 10/21 in the IG picks but on Sun 10/25 in the story.
- **Ruling:** each model has one weekly story, and no two models share a theme or activity on the same day. The Researcher clash check plus the Scheduler pre-check enforce it. Widen the Scheduler's first-class check to all models, at least 2 days apart. Gabriela removes the leg-day and boat examples. Charlotte's existing pool posts get flagged to Samuel and are not deleted, since deleting live posts needs his yes. Valentina fixes the flight date to match the story (Sun).

### C14. AI disclosure wording
- **Apparent conflict:** "Never mention AI" (captions) vs Reddit flair, YouTube synthetic disclosure and Fanvue AI flags (Valentina's conflict #5, Charlotte §8.4).
- **Ruling:** platform-required labels, toggles, flair and the Fanvue AI flag are required. They don't count as "mentioning AI" in creative copy. Never deny AI, in replies too.

### C15. Engagement
- **Settled:** 3-4 TikTok sessions a day, 10-20 minutes each, staggered, starting only once AdsPower is unfrozen.
- **What the docs say:**
  - Valentina: week-1 caps, and "Valentina runs ET late morning to afternoon".
  - Camille: "only when AdsPower is free and Samuel OKs engagement, headless profile 6 only".
  - Charlotte §10.5: "After posting… engage modestly", with no freeze check.
  - The daily-content skill step 7 says "Engage: after posting", with no freeze check.
  - Madison: "a few genuine replies" on the new X, with no route named.
  - The Scheduler §6.3 sends URLs to model bots "for engagement".
- **Ruling:** no engagement by any bot while AdsPower is frozen. After the unfreeze, run 3-4 TikTok sessions a day of 10-20 minutes each, staggered across models (see the slot plan below), headless, one platform per session, within the week-1 caps. Add the freeze gate to the daily-content skill and Charlotte.

### C16. Precedence clauses that point at stale docs
- **Gabriela:** her skill and Notion say "Where the two conflict, the shared skill wins", but the shared skill is the most out-of-date doc (C2, C4, C5, C15).
- **Valentina:** "stricter wins until Samuel decides".
- **Charlotte:** "newest Samuel rule wins" (fine).
- **Ruling:** every doc uses one line: "Samuel's settled rules win, then the Scheduler SOP (Notion), then this doc. Flag any remaining gap to JSW AI."

### C17. Known account blocks out of sync
- **Conflict:** the Scheduler lists "Madison's X" as blocked, and the Tracker lists @madisoncole26 as suspended. Madison now uses @MadisonCole69, whose status hasn't been verified live. The Gabriela FB appeal and Charlotte IG suspension appear only in the Scheduler's Notion page, not in its skill.
- **Ruling:** the Scheduler skill copies the Notion block list. Madison's X stays blocked for scheduling until someone verifies @MadisonCole69 live and JSW AI clears it.

### C18. Duplicate handoffs and logging
- **Double handoff:** the Reviewer skill (on PASS, "send the Scheduler the exact file path, caption, platforms and boost tag") **and** every model skill (on PASS, hand off to the Scheduler) both send the item, so the Scheduler gets two intakes.
- **Overlapping log writes:**
  - Sienna and Charlotte write their own rows in the Content Review Log, which the Reviewer also writes.
  - Valentina "logs the post, verifies live links", which is the Scheduler's job.
- **Ruling:** the Reviewer is the only one that sends a PASS to the Scheduler and the only one that writes review-log rows. Models submit to the Reviewer and stop. They don't forward a PASS, and their notes stay in their own NOTES.md or posted_log. Live-link checks and calendar rows belong to the Scheduler. The Scheduler dedupes by path and md5 (it already does).

---

## (2) Cross-bot conflicts

### Routine timing collisions (all times EDT)
| Time | Who runs | Problem |
|---|---|---|
| ~8:00 AM | Reviewer, plus models' 8 AM run | Models submit while the Reviewer is already running, so their work waits about 24 h. The Reviewer runs once a day, so the 9 AM and 2:30 PM model submissions and Sienna's 6 PM and 10:30 PM drops don't get a verdict until the next morning. |
| 9:00 AM | Scheduler, models' 9 AM run, Tracker what's-working notes, Sienna's "check overnight verdicts" | Four bots at once. The 9 AM Scheduler can only take PASSes from the 8 AM review, and models read Tracker notes before they exist (Madison §14 and Charlotte's morning check use yesterday's notes). |
| 12, 3, 6, 9 PM | Scheduler | There's no Reviewer run before them, so these slots receive no new PASSes and sit idle. |
| 2:30 PM | Models (Sienna steps 1-4) | Six bots start generating at the same minute on one shared Higgsfield balance, so cost quotes and "check balance first" become unreliable. 2:30 PM is also when Madison's 3 PM caps review is expected. |
| Every 4 h | Tracker stats refresh | It collides with the Scheduler at 12 and 9 PM if it's anchored at midnight. It shares the Ayrshare key and its rate limits. It's read-only, so the risk is low. |
| Sun 6 PM | Tracker weekly report | The Researcher runs Sunday at an unspecified time. If it runs before 6 PM it misses the weekly report, and it needs every model's next-week story first. |

**Proposed timetable (draft):**
- **Tracker notes:** move to 7:00 AM. Run stats at :30 past (00:30, 4:30, 8:30…) to stay clear of Scheduler runs.
- **Reviewer:** 8:30 AM, 11:30 AM, 2:30 PM, 5:30 PM and 8:30 PM, 30 minutes before each Scheduler run, plus 11:00 PM for Sienna's 10:30 PM drop if she keeps it.
- **Scheduler:** unchanged (9, 12, 3, 6, 9).
- **Models:** stagger by 15 minutes to protect the shared balance. For example: Sienna 2:30 PM (her Australian morning), Valentina 8:00, Camille 8:15, Charlotte 8:30, Madison 8:45, Gabriela 9:15 AM, with second blocks offset the same way.
- **Sunday:** models write next week's story by 12 PM, the Tracker weekly report goes out at 6 PM, and the Researcher runs at 7:30 PM.
- **Engagement (after the unfreeze):** 3-4 TikTok sessions a day of 10-20 minutes each. Stagger them so no two models overlap, for example Camille morning, Valentina late morning, Madison and Charlotte afternoon, Gabriela evening, and Sienna in the ET evening and overnight (her Australian daytime).

### Handoffs that don't line up
1. **Double Scheduler intake:** both the Reviewer and the model send the PASS (C18).
2. **Sienna:** plans 3 AM, 6 AM and 8 AM EDT X slots, but her clip-2 PASS can't arrive before the 8:30 AM review. Overnight slots only work if the 9 PM Scheduler run gets a 5:30 or 8:30 PM PASS.
3. **Credits:** the Tracker copies credits from the "JSW Content Reviews entry". Models report credits to the Reviewer in different formats, and some (Charlotte §9) write to the Tracker directly. Ruling: the Reviewer row is the only credits source.
4. **Boost tags:** the Scheduler sends Samuel "safe to boost" posts. Nothing reaches him otherwise, which is consistent with "no per-post approval". OK.
5. **Engagement URLs:** the Scheduler sends post URLs to models for engagement, but engagement is frozen. Models should just log them.
6. **Weekly stories:** the Researcher asks models for next week's story while the Camille and Madison WEEK_PLAN files and Notion week pages drift (Camille "follow WEEK_PLAN and flag", Madison "WEEK_PLAN wins", Charlotte "calendar wins"). Ruling: the Posting Calendar wins for the day's slot and activity. WEEK_PLAN and the Notion page get synced the same day.

### Mismatched Reviewer pairings
| Model | Shared skill (peer) | SHARED_LEARNINGS / practice | Model's own doc | Ruling |
|---|---|---|---|---|
| Gabriela | Camille | – | "JSW Content Reviewer" | Reviewer bot |
| Madison | Gabriela | reviewed by Valentina | Reviewer bot | Reviewer bot |
| Camille | Madison | – | Reviewer bot (99a98fb5) | Reviewer bot |
| Sienna | Madison | – | Reviewer bot | Reviewer bot |
| Valentina | Charlotte | Madison | Reviewer bot | Reviewer bot |
| Charlotte | Valentina | – | Reviewer bot | Reviewer bot |

---

## (3) Is each bot's routine safe to enable?

| Bot | Safe now? | Blockers |
|---|---|---|
| **Tracker** (stats, notes, weekly) | **Yes**, after moving notes to 7 AM | Read-only, freeze check present. |
| **Researcher** | **Yes**, after a timing fix | It doesn't post. Set the Sunday run to 7:30 PM, and add the explicit Sienna/Charlotte-only Fanvue rule and "no topless". |
| **Reviewer** | **No, until edited** | Topless line (C3), single 8 AM run (timing), unnamed "verified models" (C4), no nudity FAIL, no Kling/Seedance check. |
| **Scheduler** | **No, until edited** (it posts publicly) | Box skill lacks "Ayrshare only" and the full block list (C5, C17). Madison's X is unverified. Double intake (C18). Widen the first-class check (C13). It must depend on the Reviewer's revised rules. |
| **Sienna** | **Conditional** | Fix lip-sync to Seedance 2.0 (C7) and the gate command (C8). Remove the topless villa still and the in-caption Fanvue link from `xposts/sienna.md` (C3, C4). |
| **Gabriela** | **Conditional** | Fix the precedence clause (C16). Remove the Sun 10/25 topless idea (C3) and the leg-day and boat examples (C13). Name Seedance for lip-sync. Mark the pack approved 10/19. |
| **Valentina** | **Yes, after small edits** | Remove the AdsPower route (C5). Set engagement to the settled plan (C15). Fix the flight date. The "stricter wins" clause becomes the standard line. |
| **Camille** | **Yes, after small edits** | Replace "max 3 posts/day" with the cadence ruling (C6). Remove the peer-review note. Engagement wording per C15. |
| **Charlotte** | **No** | Fanvue uploads through AdsPower during the freeze (C5). Engagement after posting with no freeze check (C15). Gate at 0.75 (C8). The topless claim is unverified (C3). She writes the Tracker and Review Log directly (C18). |
| **Madison** | **No** (already paused) | Notion says posting goes through AdsPower k1cwwjw5 (C5). The @MadisonCole69 status is unverified (C17). The caps review is pending. The 1280x720 thumbnail option (C11). |
| **Shared `jsw-daily-content-process` skill** | **No** | Peer pairings, AdsPower posting, "Fanvue except Sienna", engagement with no freeze check, and no thumbnail rule. Gabriela treats this skill as the winner. |

---

## (4) Exact edits per bot (drafts, not applied)

**Shared rule line (add to every doc's header):** "Samuel's settled rules win, then SOP: Content Scheduling (Notion), then this doc. Reviewer = JSW Content Reviewer bot. Flag remaining gaps to JSW AI."

**jsw-daily-content-process (owned by JSW AI)**
- Step 2: change "no Fanvue links except Sienna" to "Fanvue links only for Sienna and Charlotte, on X and Reddit only, in the bio or a pinned post set by hand; never in a scheduled post".
- Step 2/video: add "Lip-sync/talking: Seedance 2.0 i2v from a gated still".
- Step 4: replace the peer pairings with "Submit to the JSW Content Reviewer bot; it alone issues PASS/FAIL using jsw-content-review-gate."
- Step 6: change "Ayrshare (or the model's AdsPower profile)" to "Ayrshare only".
- Step 7: prepend "Only after Samuel lifts the AdsPower freeze: 3-4 staggered TikTok sessions/day, 10-20 min, headless."
- Goal line: change "max 3 posts per model per day" to "1-3 new source pieces per model per day; platform caps per the Scheduler SOP cadence table".
- Export: add "+ `<clip>_thumb.jpg` 1080x1920 for every Short".
- X: add "short clips first, photos mixed; tease only (lingerie, bikini, implied), sensitive on; no nudity on X".

**jsw-content-review-gate (Reviewer)**
- 6: change "X: spicy or topless content must be marked sensitive" to "X: tease content (lingerie, bikini, implied) must be marked sensitive; any nudity, including topless, or explicit content is a FAIL (Fanvue only)."
- 6: change "only for verified models" to "only for Sienna and Charlotte".
- Add step 4b: "Model check: silent clips are Kling 3.0 + Element; lip-sync is Seedance 2.0. Any other path is a FAIL unless JSW AI cleared it."
- Add step 5: "Story fit: matches the model's weekly story beat for that day; no theme or activity clash with another model that day (calendar)."
- 8: add "You are the only sender of a PASS to the Scheduler and the only writer of review-log rows, including credits."
- New routine times: 8:30, 11:30 AM, 2:30, 5:30, 8:30 PM (+11 PM).

**jsw-content-scheduling (Scheduler, box skill; sync to Notion)**
- §0: add "Never posts through AdsPower; Ayrshare only (JSW AI, Oct 21)."
- §2.6: change "Camille's and Sienna's first-class posts days apart" to "any two models' first-class or flight posts at least 2 days apart".
- §2.13: copy the Notion block list (Sienna YT appeal, Madison X [@MadisonCole69 unverified], Gabriela FB appeal, Charlotte IG suspension).
- §2.1 add: "Reject any X media showing nudity, including topless."
- §3: "Madison X: 1-3/day during warm-up."
- §1: "Intake from the Reviewer's PASS only; ignore duplicate model forwards (dedupe by path + md5)."
- §6.3: "Send URLs to model bots for logging; no engagement during the freeze."

**Researcher (Notion and skill)**
- Set the run time to Sunday 7:30 PM, after the Tracker report. Collect stories by Sunday noon.
- §3 X: add "no nudity (no topless)". Change "only for verified models" to "Sienna and Charlotte only".
- §4: add "no two models share a first-class/flight, pool, boat or gym day".
- §5: add "engagement banks for the post-unfreeze plan: 3-4 TikTok sessions/day, 10-20 min".

**Tracker (Notion and skills)**
- Move what's-working notes from 9 AM to 7 AM ET. Anchor stats at :30 past.
- Stats step 4: "credits only from the Reviewer's review row".
- No other changes.

**Sienna (Notion, skill, `/workspace/jsw_tiktok/sienna/jsw-sienna-creation_SKILL.md`)**
- Step 9: change the command to `/workspace/.face-venv/bin/python identity_gate.py img --model sienna --source seedream --body <files>`.
- Step 11: change "Sync Lipsync (sync_so…)" to "Seedance 2.0 i2v from the gated still with sienna.mp3; whisper word-for-word check".
- Step 18: remove "Log it in the Content Review Log" (the Reviewer owns it).
- Step 19: change "hand the passed files to the Scheduler" to "Reviewer forwards the PASS; you don't".
- `xposts/sienna.md`: remove the "topless still with hair covering" idea (reframe as covered or implied), and remove "[Fanvue link" from the caption (use "link in bio").
- Daily routine: put clip 1 by 5:15 PM so the 5:30 Reviewer run catches it. Overnight X slots only for PASSed items.

**Gabriela (Notion and skill)**
- Header: replace "Where the two conflict, the shared skill wins" with the shared rule line.
- §1: delete "leg day" and "boat day" from the example and "gym in tight shorts" from the list (Madison and Valentina own them this week).
- §3: change "Lip sync: she talks within the first second" to "Lip sync: Seedance 2.0 i2v from a gated still; she talks within the first second; whisper check".
- §0: change "The approved reference board" to "the reference pack approved by Samuel 10/19" (also update Gabriela's model page and the Process page).
- §5 music: "TikTok cut: commercial library or royalty-free cleared only; log the track".
- §8: change "Send passed files to the Scheduler" to "Reviewer forwards PASS".
- Week page Sun 10/25: replace the topless shoreline still with an implied or back-view shot in a bikini top.

**Valentina (Notion and skill)**
- §6: change "(Ayrshare, or headless AdsPower when no hold is active)" to "(Ayrshare only)". Drop "log the post, verify live links", which is the Scheduler's job.
- Engagement: replace the start condition with "only after Samuel lifts the AdsPower freeze; 3-4 TikTok sessions/day, 10-20 min, in the staggered slot JSW AI assigns".
- Replace "stricter one wins until Samuel decides" with the shared rule line.
- Close "Open conflicts" 1-3 as resolved (Reviewer PASS; Reviewer bot; cadence per SOP, 1 TikTok/day).
- Week page: set the flight home to Sun 10/25 in the IG picks.

**Camille (Notion and skill)**
- Hard limits: change "max 3 posts/day" to "1-3 new source pieces/day; platform caps per the Scheduler SOP; at least half of X posts tease".
- §6: remove "hand off to the Scheduler" (the Reviewer forwards).
- §7 engagement: change "only when AdsPower is free and Samuel OKs engagement, headless profile 6 only" to "only after Samuel lifts the freeze; 3-4 TikTok sessions/day, 10-20 min, staggered (ET morning), headless profile 6".
- Conflicts list: mark Reviewer and Fanvue resolved (Reviewer bot; no link until JSW AI clears Camille).

**Charlotte (Notion, skill, `/workspace/jsw_process/charlotte/jsw-charlotte-content.md`)**
- Skill step 10 and Notion §10.4: change "Fanvue uploads go through AdsPower k1cwwgmo, headless only, and never during an AdsPower hold" to "No Fanvue uploads or any AdsPower use until Samuel says his Fanvue work is done; then headless only."
- Notion §10.2: change "Ayrshare or the scheduled AdsPower route" to "Ayrshare".
- Notion §10.5: prepend "After the AdsPower freeze lifts only:" and use the 3-4 session plan.
- Skill step 6 and Notion §6.1: change "≥ 0.75 on 6 frames" to "stills: `img --model charlotte --source seedream` ≥ 0.78; clips: `video --model charlotte` code thresholds + by-eye check + montage"; close conflict #3.
- Notion §8.2 and conflict #8: add "No nudity, including topless, on X (the 10/20 topless claim is unverified; hold until Samuel confirms)". Change the Fanvue link scope to "X bio/pinned and Reddit".
- §9: "Log credits on the Reviewer submission only; don't write Tracker or Review Log rows directly."

**Madison (Notion and skill)**
- Notion §12: change "Posting runs through AdsPower in headless mode only, profile k1cwwjw5" to "The Scheduler posts through Ayrshare only. AdsPower is frozen until Samuel's Fanvue work is done; then headless only, never touch the proxy." Close conflict #11.
- §8: drop the "or a 1280x720 crop" option, so it reads "1080x1920 from the clip".
- §12: "@MadisonCole69 status unverified; the Scheduler skips Madison X until it's verified live."
- §0: keep "paused" until the 3 PM caps review. Record "YouTube 2-3 Shorts/day".
- Skill §12: add "Ayrshare only".

**Box docs (owned by JSW AI)**
- `MODEL_CONTENT_PROCESS.md`: add a banner saying "SUPERSEDED for approval (§0 rule zero, §5), finishing (§4 Skin Enhancer → v4C), video model (Seedance → Kling 3.0; Seedance lip-sync only), thresholds (Seedream 0.78), pack status (Gabriela approved 10/19)."
- `CONTENT_RECIPE.md`: add a banner saying "§3 Seedance for all clips → Kling 3.0 silent / Seedance 2.0 lip-sync; §6 'Sam reviews every file' → Reviewer PASS."
- `/workspace/review_sop.md`: same topless-line fix as the review gate.

---

## Open questions for Samuel
1. Did you allow topless on X when marked sensitive (Charlotte's claim, 10/20 about 3:46 PM ET)? Until you confirm, the ruling is no.
2. Caps: is "2-3 a day" new source pieces (my draft) or total posts? This is pending the 3 PM review.
3. Who owns "gym" now that Madison has switched to pickleball? What happens to Charlotte's pool posts that are already live?
4. Can the Reviewer run 5-6 times a day instead of once at 8 AM?
