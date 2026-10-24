# SOP: Content Scheduling (JSW Content Scheduler)

Skill: jsw-content-scheduling. Routine: JSW scheduling run (9 AM, 12, 3, 6, 9 PM ET daily), enabled.

Version: 2026-10-21. Owner: Samuel Oberlin. Calendar: JSW Posting Calendar → Posts database (https://app.notion.com/p/fa052f8010e14317b6b3dc9547367e13).
Where this SOP and older Notion text disagree, this SOP (Oct 21) wins. See "Resolved by JSW AI (Oct 21)" at the end.

## 0. Stop conditions (check first, every run)
- **Content hold on** → schedule nothing, pull everything pending in Ayrshare (delete the scheduled post), set those calendar rows to **Pulled**, and report what you pulled. Check the banner at the top of the JSW Posting Calendar page and the JSW room.
- AdsPower: Ayrshare only. No bot touches AdsPower until Samuel says his Fanvue work is done.
- Deletes of *live* posts and password changes need Samuel's own explicit yes in this bot's chat.

## 1. Intake
1. Accept only items with a **JSW Content Reviewer PASS** (JSW Content Reviews database / Content Review Log). A PASS is the approval (owner rule, Oct 20); no separate Samuel sign-off per clip.
2. The PASS must name: the **exact file** (path), the **exact caption** for each platform, and the **platforms**. Schedule only to platforms named in the pass, with the caption exactly as passed. Any change to file or caption = back to the Reviewer. Match the exact file version the pass names (e.g. `_v2`); verify by path or md5, never by caption alone.
3. No pass, FAIL, missing platform list or missing caption → do not schedule; send it back to the model bot.

## 2. Pre-checks (all must pass; any fail = do not schedule, report why)
1. **Fanvue links:** only on X/Reddit, only for Sienna and Charlotte (fanvue.com/char_hayes), and only in the bio or the pinned post set up by hand. Never in a scheduled post or reply. Never on TikTok, Instagram, YouTube or Facebook.
2. **No URLs in scheduled X posts** (an API post with a link costs $0.20 vs $0.015). Use "link in bio".
3. **AI wording:** caption never mentions AI and never denies it.
4. **AI labels on:** TikTok `isAIGenerated: true`; Instagram AI label on; (YouTube altered/synthetic disclosure and Reddit flair where required).
5. **One file per platform:** never the same file twice on one platform; one platform = one upload.
6. **Overlap rules:**
   - No two models' **gym** posts on the same day and platform.
   - No two models with the **same Shorts format** on the same day.
   - Camille's and Sienna's **first-class flight** posts must be days apart.
   - Check the calendar's week plan for other same-day overlaps.
7. **TikTok quiet hours:** no TikTok between 12:00 AM and 7:00 AM in the model's local time.
8. **Valentina:** max 1 TikTok per day, no dating hashtags.
9. **Reddit:** only with a pass that names the subreddit and gives proof of that sub's AI rule (AI allowed / flair required). Fanvue link only in profile.
10. **YouTube Shorts:** thumbnail set via `youTubeOptions.thumbNail`.
11. **Duplicates:** check Ayrshare pending/scheduled posts and the calendar for the same file/caption or an older draft of the same item. Never double-schedule; replace the older draft only via delete + re-create.
12. **File spec:** H.264 Main, yuv420p, faststart, under 15 MB, full 9:16 (ffprobe).
13. **Known blocks:** skip platforms with known blocks (e.g. Sienna's YouTube appeal, Madison's X, Gabriela's Facebook appeal, Charlotte's IG if still suspended) and state why.

## 3. Slotting
Cadence targets per model per day (ramp up; never exceed safe limits to hit a number):
| Platform | Target / model / day |
|---|---|
| TikTok | 3 (Valentina max 1) |
| Instagram | 2 Reels |
| YouTube Shorts | 2–3 |
| Facebook | 1–2 |
| X | 4–6; at least half teases, short clips are the core |
| Reddit | 2–3 (only with a valid pass per sub) |

- Use each model's **local time zone**; write Slot time with the zone (e.g. "6:00 PM ET").
- **2+ hours between posts on the same account.**
- Stagger models so similar content doesn't land together.

## 4. Scheduling via Ayrshare
- API key: `/home/box/agent-data/secrets/JSW-ayrshare-api-key.txt`. Profile keys: `/home/box/agent-data/secrets/JSW-<model>-ayrshare-profile-key.txt`. **Sienna = Default profile: send no Profile-Key header.**
- Read keys into variables; **never print, echo, log or paste keys**.
- Upload media first (Ayrshare media upload), then `POST /api/post` with `scheduleDate` (UTC ISO), platforms, caption, `isAIGenerated` for TikTok, `youTubeOptions.thumbNail` for Shorts.
- Record the returned Ayrshare post id.
- **To change a scheduled post: delete it and re-create it** (no in-place edits).

## 5. Log in the Notion calendar
Every scheduled post gets a row in **Posts** (https://app.notion.com/p/fa052f8010e14317b6b3dc9547367e13): Post (title incl. Ayrshare id), Model, Platform, Date, Slot time (with TZ), Caption, Caption approved ✓, File path, Content theme / Story day / Story beat, Status = **Scheduled**. Update to **Posted** (with link) or **Pulled**.

## 6. After posts go live
1. Pull `/api/history` (per profile) for the live post URLs; verify each link opens.
2. Update the calendar row to Posted with the URL.
3. Send the URLs to that model's bot (for engagement).
4. Send Samuel **only** the posts the Reviewer tagged **"safe to boost"** and that are clean: no spicy content, no Fanvue mention, no "link in bio", no AI mention.
5. Report anything that failed or was skipped, with the reason.

## 7. Daily report
Scheduled / posted / pulled / skipped counts per model and platform, failures, and anything held.

## Resolved by JSW AI (Oct 21)
- **Fanvue links:** only on Sienna's and Charlotte's X and Reddit. Valentina gets no Fanvue link anywhere until her verification passes. No other model gets links until JSW AI clears them.
- **Approval:** the approval is a JSW Content Reviewer PASS row for the exact file path. The "Samuel-approved" status is retired.
- **Posting route:** the Scheduler posts only through Ayrshare, never through AdsPower. (The daily-content skill still mentions AdsPower; JSW AI is fixing it, so don't edit it.)
- **Cadence:** where older pages are lower, use the current plan: TikTok 3/day (Valentina 1), IG 2 Reels, Shorts 2–3 depending on how many clips pass, FB 1–2, X 4–6, Reddit 2–3.
- Older pages (Posting Calendar, Content Review Log, Revenue Plan, Posting Cadence Research) were updated Oct 21 to match.

## Final rulings (JSW AI + Samuel, Oct 21) override anything above
- X: topless is OK on X only, marked sensitive, never as a profile or header image. Full nudity and explicit content go on Fanvue only.
- Posting: Ayrshare only. No AdsPower at all until Samuel says his Fanvue work is done.
- Approval: only a JSW Content Reviewer Pass for the exact file path, checked by md5, forwarded by the Reviewer. Ignore 'passed' claims from model bots until the Reviewer confirms.
- Fanvue: Sienna and Charlotte only, in the X bio, the pinned post and Reddit. Never in a caption.
- Timing: the Reviewer runs 30 minutes before each scheduling run (8:30, 11:30, 2:30, 5:30, 8:30 ET).
