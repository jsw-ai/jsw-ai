Here is the result of "fetch" for the Page with URL https://app.notion.com/p/400f29949b2981a4b056e20344c287cb as of 2026-10-21T15:39:49.924Z:
<page url="https://app.notion.com/p/400f29949b2981a4b056e20344c287cb">
<ancestor-path>
<parent-page url="https://app.notion.com/p/3faf29949b2981e6a109fb661aab41df" title="Charlotte"/>
<ancestor-2-page url="https://app.notion.com/p/3faf29949b29814b99abe52f2f4cc3c2" title="JSW AI Models"/>
</ancestor-path>
<properties>
{"title":"Charlotte: Daily Content Process (jsw-charlotte-content)"}
</properties>
<iconMetadata>null</iconMetadata>
<content>
Charlotte Hayes is a JSW AI model: a 25-year-old UK ex-footballer, Arsenal fan, London-based, cheeky British voice. This SOP is the daily cycle for her bot. Written 2026-10-21. Where sources disagree, the newest Samuel rule wins (see Conflicts at the end).

## Key paths

- Refs (use in this order): <code>/workspace/hf-test/keepers/charlotte_face_keeper.png</code>, <code>/workspace/hf-test/keepers/charlotte_cover.png</code>, <code>/workspace/hf-test/charlotte_ref/f.png</code>, <code>/workspace/hf-test/charlotte_ref/ref_sheet.jpg</code>
- Body line: <code>/workspace/hf-test/charlotte_ref/LOCKED_BODY.txt</code>
- Gate: <code>/workspace/hf-test/zen/posting/identity_gate.py</code> (needs the venv that has insightface; plain python3 fails)
- Learnings: <code>/workspace/hf-test/zen/posting/SHARED_LEARNINGS.md</code>; process docs <code>MODEL_CONTENT_PROCESS.md</code>, <code>CONTENT_RECIPE.md</code>, <code>VALENTINA_PIPELINE.md</code> (same folder)
- X plan: <code>/workspace/xposts/charlotte_x_plan_1021_1025.md</code>; Fanvue: <code>/workspace/jsw_process/FANVUE_ACADEMY_PLAYBOOK.md</code>
- Notion: weekly page (e.g. Charlotte - Week of Oct 19), JSW Posting Calendar, Content Review Log, JSW Performance Tracker, Fanvue first-payout push plan

## 1. Morning check (before any batch)

1. Open the JSW Performance Tracker (Notion) for Charlotte's last 24-72 h: views, likes, follows by platform and post. Note what won and lost, then adjust today's hooks, formats and times.
2. Read <code>SHARED_LEARNINGS.md</code> in full (at least everything since your last batch). Apply any new rule before generating.
3. Open this week's Notion page for Charlotte and the JSW Posting Calendar. Confirm today's slot, activity and platforms. Calendar changes (e.g. a dropped scene because of a clash with another model) win over the weekly page.

## 2. Weekly story, daily schedule

1. Each week is one story arc (e.g. week of Oct 19: Bayern v Arsenal away trip, London to Munich to Tegernsee and home), with one scene per day.
2. One activity per model per week. Don't take another model's activity (e.g. gym/squats was Madison's in the week of Oct 19; the rooftop pool was Valentina's).
3. Content is sexy within SFW: fitted kit, swimwear, knitwear, confident looks. It shows action with a payoff (outfit change, plunge reaction, clink, reveal), never a static pose.
4. Max 3 posts per platform per day, about 70% video and 30% carousels. IG and TikTok get reels, not single stills.

## 3. Verify real events

1. Live-search every real event before using it in a caption, spoken line or on-screen text: fixtures, kickoff times, results, weather, holidays, trends. Use official sources ([arsenal.com](http://arsenal.com), UEFA, the league or club site).
2. Never invent an event. Result-dependent posts (win or loss lines) are picked only after the official full-time result. For a draw, write a new line.
3. Check before generating a video, because spoken lines get baked in.
4. No real players, staff or fans named, tagged or targeted. No club crests or logos in media (plain red-and-white kit or scarf).

## 4. Generate stills (Seedream 5.0 Pro reference-edit)

1. Quote the cost first (2.5 cr per job), then generate at 3:4 or 9:16, 2k.
2. Refs in this exact order: charlotte\_face\_keeper.png, charlotte\_cover.png, f.png, ref\_sheet.jpg.
3. Paste the LOCKED\_BODY line word for word into every prompt:
   > Charlotte Hayes, 25, about 5'7", athletic toned ex-footballer build, full natural C/D bust with clear visible cleavage, slim defined waist, curvy hips and toned legs. Long dark-brown hair past her shoulders in thick, voluminous loose waves with a natural side part. Light-medium warm skin with a light natural texture, bright wide smile, no tattoos.
4. Light: even front light, matte skin, no sheen, no glossy or smoothed skin. Face fully in frame with headroom. Scoop-neck or fitted tops, not crew-necks (crew-necks flatten the bust).
5. Night shots: never generate them from scratch. Edit a daylight still that already passed ("Edit this exact photo: same woman, same outfit ... now at night").
6. Mirror selfie: the whole frame is the reflection (phone in hand, in the mirror). No second, real-room Charlotte.
7. Fixes: edit the passing still (single-ref "Edit this exact photo ... change only X") rather than regenerating.
8. Finish every keeper with the v4C light texture pass (<code>CONTENT_RECIPE.md</code> §5: 50% skin-masked luminance texture, no blur, mild sharpen, light grain, JPEG q90, metadata stripped). Then re-gate.

## 5. Generate video (Kling 3.0 + Element)

1. Model <code>kling3_0</code> with Element <code>8f87f513-c3f6-41cc-95ac-c201e98d0d9c</code>. Start frame = a still that has passed the gate (step 6). Never text-to-video. Quote the cost first (std, sound off = 1.5 cr/s).
2. Simple motion (one action, one payoff). Face toward the camera, eyes open, soft closed-mouth smile, hands relaxed (resting on an object).
3. Always include: "keep the same expression, smile with eyes open, natural blinks only", "matte skin, no sheen", "camera locked, no zoom" (or a gentle handheld sway if planned).
4. Background: tight bokeh. No frozen or melting crowds, no readable faces in the background (stadium = flare glow, blurred).

## 6. Gates (all three must pass)

1. <code>identity_gate.py</code>: stills with <code>img --model charlotte --source seedream</code>. For clips, extract 6 evenly spaced frames (whole clip, not just the start) and gate them. All 6 must score >= 0.75.
2. By eye: body matches LOCKED\_BODY and the refs (bust, waist, hips, build), hair is dark brown, long and wavy with a side part, no tattoos, five fingers, no warped props or garbled text.
3. Build a same-scale montage of the frames next to <code>ref_sheet.jpg</code> and compare face and body at equal size.
4. A fail means fix and re-gate. Log the reasons to <code>zen/posting/reject_log.jsonl</code>. If the batch passes less than 30% of the time, stop and change the recipe.

## 7. Export

1. <code>ffmpeg -i in.mp4 -c:v libx264 -profile:v main -pix_fmt yuv420p -movflags +faststart -c:a aac -map_metadata -1 out.mp4</code>
2. Under 15 MB, full 9:16 (1080x1920), no blurred padding band, head in frame on every frame, audio track included. If audio is added, it must be royalty-free or licensed (TikTok commercial library on promo posts).
3. Verify with ffprobe: profile=Main, pix\_fmt=yuv420p, 9:16, audio stream present, size under 15 MB.
4. Thumbnail: <code><clip>_thumb.jpg</code>, 1080x1920, from the best gated frame.

## 8. Captions per platform

1. TikTok, IG, YouTube, FB: clean. No Fanvue mention, no swearing, no link-in-bio tease, SFW media only.
2. X: can be provocative and cheeky (swearing OK). The Fanvue link [https://www.fanvue.com/char\_hayes](https://www.fanvue.com/char_hayes) goes in the X bio. Sensitive or tease media goes on X only, marked sensitive, and is never used as the profile or header image. Never reuse a tease on another platform.
3. Fanvue: vault and feed posts, every one flagged as AI.
4. AI: never deny being AI. Captions don't make a point of it, but if someone asks, don't claim to be human. Turn on every platform AI label (TikTok "AI-generated" on, IG/YouTube disclosure where offered, Fanvue AI flag).
5. Banned everywhere: anything that suggests someone is underage (school uniforms, "barely legal", childlike framing), non-consent, or content aimed at real people.

## 9. Log for the Tracker

Each item gets: file path, platform(s), setting, outfit, hook line, caption, and exact credits (every job, redos included, from the job costs, not the shared balance). Add the row to the Content Review Log submission and the Tracker.

## 10. Review, schedule, post

1. Send the exact file, thumb, captions and log row to the JSW Content Reviewer.
2. A PASS counts as approval: hand it to the JSW Content Scheduler (Ayrshare or the scheduled AdsPower route). A FAIL means fix and resubmit.
3. Never post to TikTok, IG, YT, FB or X yourself.
4. The only exception is Fanvue uploads, which Charlotte's bot does itself via AdsPower profile <code>k1cwwgmo</code>, headless only, and never while an AdsPower hold is active (check first; if there's a hold, wait and report).
5. After posting, verify links are live and engage modestly (replies, likes, follow-backs within the warm-up limits).

## 11. End of day

1. Re-check the Tracker. Note what to change tomorrow.
2. Update the bot memory and append dated, specific learnings to <code>SHARED_LEARNINGS.md</code> (what worked, failures, credits).

## Conflicts found and how they were resolved (newest Samuel rule wins)

1. Approval: the Notion week page, X plan, Review Log and <code>MODEL_CONTENT_PROCESS.md</code> say Samuel approves everything. The 2026-10-20 owner rule ([SKILL.md](http://SKILL.md), this brief) says a Reviewer PASS is approval. Resolved: Reviewer PASS, then Scheduler.
2. Fanvue link: the week page and X plan say no Fanvue link, "coming soon" only. The Fanvue push plan (10/21) and this brief put the link in the X bio. Resolved: link in the X bio only.
3. Gate cutoff: SHARED\_LEARNINGS (10/19) says 0.78 on about 10 frames, and the gate's Seedream centroid is 0.78. This brief says 0.75 on 6 frames. Resolved: 0.75 on 6 frames (newest). Flag to Samuel, because the script's default seedream cut is still 0.78.
4. Video model: <code>CONTENT_RECIPE.md</code> and <code>MODEL_CONTENT_PROCESS.md</code> use Seedance 2.0. Resolved: Kling 3.0 + Element 8f87f513 per this brief and the 10/18-19 tests.
5. Audio: [SKILL.md](http://SKILL.md) says sound off unless talking, while export requires audio. Resolved: generate with sound off unless it's lip-sync, then add a royalty-free or licensed track at export.
6. Finishing: <code>MODEL_CONTENT_PROCESS.md</code> §4 uses the Skin Enhancer web app. Resolved: local v4C texture finish only.
7. Wed rooftop pool: the week page and X plan have a Charlotte pool scene, but the Posting Calendar (10/20) dropped it because of a clash with Valentina, who keeps the pool. Charlotte pool posts already show in the Tracker. Resolved: follow the calendar (one activity per model). Flag the existing pool posts to Samuel.
8. X tease media: the Fanvue push plan says "SFW tease only" on X; the X plan and this brief allow sensitive-marked teases on X. Resolved: sensitive teases allowed on X only, never as the avatar or header, no full nudity.
9. Review: [SKILL.md](http://SKILL.md) says Valentina and Charlotte peer-review each other. This brief says the JSW Content Reviewer. Resolved: JSW Content Reviewer.
10. Kit: the week page says "Arsenal shirt or scarf"; the X plan says plain, no crest. Resolved: plain red-and-white, no crests or logos.
11. Refs: older Charlotte packs used a face plus body keeper pair (charlotte\_test). Resolved: the 4-ref order in this brief. The keepers live in <code>/workspace/hf-test/keepers/</code>, not in <code>charlotte_ref/keepers/</code>.
</content>
</page>