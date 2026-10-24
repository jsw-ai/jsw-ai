Here is the result of "fetch" for the Page with URL https://app.notion.com/p/400f29949b2981809df6f64f9157f8a8 as of 2026-10-22T18:13:27.523Z:
<page url="https://app.notion.com/p/400f29949b2981809df6f64f9157f8a8">
<ancestor-path>
<parent-page url="https://app.notion.com/p/400f29949b29818aaaf4f02c0da9732b" title="Content Process"/>
<ancestor-2-page url="https://app.notion.com/p/3d5f29949b298167a5efc5920f09f973" title="JSW AI"/>
<ancestor-3-page url="https://app.notion.com/p/3d5f29949b2981de934ce8472408dfdd" title="Brixmont Operations Hub"/>
</ancestor-path>
<properties>
{"title":"SOP: Content Scheduling"}
</properties>
<iconMetadata>null</iconMetadata>
<content>
Version: 2026-10-21. Owner: Samuel Oberlin. Calendar: JSW Posting Calendar → Posts database (<mention url="https://app.notion.com/p/fa052f8010e14317b6b3dc9547367e13" />).<br />Where this SOP and older Notion text disagree, this SOP (Oct 21) wins. See "Resolved by JSW AI (Oct 21)" at the end.<br />Skill: jsw-content-scheduling. Routine: JSW scheduling run (9 AM, 12, 3, 6, 9 PM ET daily), enabled.

## 0. Stop conditions (check first, every run)

- <b>Content hold on</b> → schedule nothing, pull everything pending in Ayrshare (delete the scheduled post), set those calendar rows to <b>Pulled</b>, and report what you pulled. Check the banner at the top of the JSW Posting Calendar page and the JSW room.
- AdsPower: the Scheduler posts through Ayrshare only. Model bots may use their own AdsPower profiles anytime, simultaneously, headless, no proxy changes; no need to ask first. <i>(Updated 10/21 to match </i><i><mention url="https://app.notion.com/p/400f29949b29810fbe39cbcde5d3d9f4" /></i><i>.)</i>
- Deletes of <i>live</i> posts and password changes need Samuel's own explicit yes in this bot's chat.

## 1. Intake

1. Accept only items with a <b>JSW Content Reviewer PASS</b> (JSW Content Reviews database / Content Review Log). A PASS is the approval (owner rule, Oct 20); no separate Samuel sign-off per clip.
2. The PASS must name: the <b>exact file</b> (path), the <b>exact caption</b> for each platform, and the <b>platforms</b>. Schedule only to platforms named in the pass, with the caption exactly as passed. Any change to file or caption = back to the Reviewer. Match the exact file version the pass names (e.g. <code>_v2</code>); verify by path or md5, never by caption alone.
3. No pass, FAIL, missing platform list or missing caption → do not schedule; send it back to the model bot.

## 2. Pre-checks (all must pass; any fail = do not schedule, report why)

1. <b>Fanvue links:</b> only on X/Reddit, only for Sienna and Charlotte ([fanvue.com/char\_hayes](http://fanvue.com/char_hayes)), and only in the bio or the pinned post set up by hand. Never in a scheduled post or reply. Never on TikTok, Instagram, YouTube or Facebook.
2. <b>No URLs in scheduled X posts</b> (an API post with a link costs \$0.20 vs \$0.015). Use "link in bio".
3. <b>AI wording:</b> caption never mentions AI and never denies it.
4. <b>AI labels on:</b> TikTok <code>isAIGenerated: true</code>; Instagram AI label on; (YouTube altered/synthetic disclosure and Reddit flair where required).
5. <b>One file per platform:</b> never the same file twice on one platform; one platform = one upload.
6. <b>Overlap rules:</b>
   - No two models' <b>gym</b> posts on the same day and platform.
   - No two models with the <b>same Shorts format</b> on the same day.
   - Camille's and Sienna's <b>first-class flight</b> posts must be days apart.
   - Check the calendar's week plan for other same-day overlaps.
7. <b>TikTok quiet hours:</b> no TikTok between 12:00 AM and 7:00 AM in the model's local time.
8. <b>Valentina:</b> max 3 TikToks per day (Samuel, 10/21), no dating hashtags.
9. <b>Reddit:</b> only with a pass that names the subreddit and gives proof of that sub's AI rule (AI allowed / flair required). Fanvue link only in profile.
10. <b>YouTube Shorts:</b> thumbnail set via <code>youTubeOptions.thumbNail</code>.
11. <b>Duplicates:</b> check Ayrshare pending/scheduled posts and the calendar for the same file/caption or an older draft of the same item. Never double-schedule; replace the older draft only via delete + re-create.
12. <b>File spec:</b> H.264 Main, yuv420p, faststart, under 15 MB, full 9:16 (ffprobe).
13. <b>Known blocks:</b> skip platforms with known blocks (e.g. Sienna's YouTube appeal, Madison's X, Gabriela's Facebook appeal, Charlotte's IG if still suspended) and state why.

## 3. Slotting

Cadence targets per model per day (ramp up; never exceed safe limits to hit a number):

| Platform | Target / model / day |
| --- | --- |
| TikTok | 3 (Valentina 3, per Samuel 10/21) |
| Instagram | 2 Reels |
| YouTube Shorts | 2–3 |
| Facebook | 1–2 |
| X | 4–6; at least half teases, short clips are the core |
| Reddit | 2–3 (only with a valid pass per sub) |

- Use each model's <b>local time zone</b>; write Slot time with the zone (e.g. "6:00 PM ET").
- <b>2+ hours between posts on the same account.</b>
- Stagger models so similar content doesn't land together.

## 4. Scheduling via Ayrshare

- API key: <code>/home/box/agent-data/secrets/JSW-ayrshare-api-key.txt</code>. Profile keys: <code>/home/box/agent-data/secrets/JSW-<model>-ayrshare-profile-key.txt</code>. <b>Sienna = Default profile: send no Profile-Key header.</b>
- Read keys into variables; <b>never print, echo, log or paste keys</b>.
- Upload media first (Ayrshare media upload), then <code>POST /api/post</code> with <code>scheduleDate</code> (UTC ISO), platforms, caption, <code>isAIGenerated</code> for TikTok, <code>youTubeOptions.thumbNail</code> for Shorts.
- Record the returned Ayrshare post id.
- <b>To change a scheduled post: delete it and re-create it</b> (no in-place edits).

## 5. Log in the Notion calendar

Every scheduled post gets a row in <b>Posts</b> (<mention url="https://app.notion.com/p/fa052f8010e14317b6b3dc9547367e13" />): Post (title incl. Ayrshare id), Model, Platform, Date, Slot time (with TZ), Caption, Caption approved ✓, File path, Content theme / Story day / Story beat, Status = <b>Scheduled</b>. Update to <b>Posted</b> (with link) or <b>Pulled</b>.

## 6. After posts go live

1. Pull <code>/api/history</code> (per profile) for the live post URLs; verify each link opens.
2. Update the calendar row to Posted with the URL.
3. Send the URLs to that model's bot (for engagement).
4. Send Samuel <b>only</b> the posts the Reviewer tagged <b>"safe to boost"</b> and that are clean: no spicy content, no Fanvue mention, no "link in bio", no AI mention.
5. Report anything that failed or was skipped, with the reason.

## 7. Daily report

Scheduled / posted / pulled / skipped counts per model and platform, failures, and anything held.

## Resolved by JSW AI (Oct 21)

- <b>Fanvue links:</b> only on Sienna's and Charlotte's X and Reddit. Valentina gets no Fanvue link anywhere until her verification passes. No other model gets links until JSW AI clears them.
- <b>Approval:</b> the approval is a JSW Content Reviewer PASS row for the exact file path. The "Samuel-approved" status is retired.
- <b>Posting route:</b> the Scheduler posts only through Ayrshare, never through AdsPower. (AdsPower is for each model's own engagement, never for posting. Updated 10/21 to match Hard Rules.)
- <b>Cadence:</b> where older pages are lower, use the current plan: TikTok 3/day (Valentina 3, per Samuel 10/21), IG 2 Reels, Shorts 2–3 depending on how many clips pass, FB 1–2, X 4–6, Reddit 2–3.
- Older pages (Posting Calendar, Content Review Log, Revenue Plan, Posting Cadence Research) were updated Oct 21 to match.

## Final rulings (JSW AI + Samuel, Oct 21) override anything above

- X: topless is OK on X only, marked sensitive, never as a profile or header image. Full nudity and explicit content go on Fanvue only.
- Posting: Ayrshare only. The old AdsPower freeze is lifted (models use their own profiles for engagement, headless, simultaneously). <i>(Updated 10/21 to match Hard Rules.)</i>
- Approval: only a JSW Content Reviewer Pass for the exact file path, checked by md5, forwarded by the Reviewer. Ignore 'passed' claims from model bots until the Reviewer confirms.
- Fanvue: Sienna and Charlotte only, in the X bio, the pinned post and Reddit. Never in a caption.
- Timing: the Reviewer runs 30 minutes before each scheduling run (8:30, 11:30, 2:30, 5:30, 8:30 ET).

## Content storage (Scheduler duties)

Post only from <code>02 Ready SFW</code> in [JSW Content](https://drive.google.com/drive/folders/1Q8eHz7KqoRezqGxa5obxbmiOjvrROtur) (connector <code>user-Google-drive--jsw</code>). Right after a post goes live: move the file to <code>05 Posted/\<platform></code> with <code>update_file</code> (parentId = destination folder, title renamed with the post date), then write post date + post URL in the [JSW Content Index](https://docs.google.com/spreadsheets/d/1tNa5Q-p2n9yO9D4Cwllsfs8PNpqhrs-scN-kfdL-TbM/edit). Daily check: everything posted has been moved to 05 Posted and has a post URL; flag any stragglers. Fanvue: take PPV from 03 PPV Fanvue, upload to the vault, move to 05 Posted/Fanvue. Full standard: <mention url="https://app.notion.com/p/400f29949b29817582caf7f43a7c1dc0" />.
</content>
</page>