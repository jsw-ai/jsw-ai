Here is the result of "fetch" for the Page with URL https://app.notion.com/p/400f29949b2981f9a6e7d57b16b368b8 as of 2026-10-21T15:40:37.155Z:
<page url="https://app.notion.com/p/400f29949b2981f9a6e7d57b16b368b8" icon="⚙️">
<ancestor-path>
<parent-page url="https://app.notion.com/p/3faf29949b29812fa9abcc6d7492947a" title="Madison"/>
<ancestor-2-page url="https://app.notion.com/p/3faf29949b29814b99abe52f2f4cc3c2" title="JSW AI Models"/>
</ancestor-path>
<properties>
{"title":"JSW Madison: Daily Content Process"}
</properties>
<iconMetadata>{"type":"emoji","emoji":"⚙️"}</iconMetadata>
<content>
Persona: Madison Cole, 23, grew up in Austin, lives in NYC. Funny, sporty, iced coffee, Pilates. Her best friend Charlotte appears in captions only, never on camera. Canon is Look A (approved 2026-10-14): long, thick, wavy golden-brown hair with honey-caramel highlights (never ash-blonde), brown eyes, golden tan.<br />Daily cap: per the Scheduler's SOP until the 3 PM review (see step 0); about 70% video.

## 0. Settled rules (JSW AI, 2026-10-21, all models; these override the steps below)

- <b>Routine paused:</b> this daily routine stays paused until JSW AI signs off. Until then, prepare drafts only; nothing goes to the Scheduler.
- <b>Approval:</b> a JSW Content Reviewer PASS for the exact file is the approval.
- <b>X:</b> tease content only (lingerie, bikinis, implied shots), with sensitive media on. No nudity or explicit content on X; that goes on Fanvue only. This overrides the older note that allowed topless posts on X.
- <b>AdsPower:</b> headless only, and untouched until Samuel says his Fanvue work is done.
- <b>Post caps:</b> to be settled at the 3 PM review. Until then, use the Scheduler's SOP (replaces the "max 3 per platform per day" line below).

## 1. Weekly story

- One story per week, written in <code>[week folder]/WEEK_PLAN.md</code> (example: <code>/workspace/madison_oct20/WEEK_PLAN.md</code>, Scottsdale girls' trip). It must not overlap another model's story or look.
- Each day gets a scene, a format (transition, talking, action, montage) and a hook. Vary the camera and the format.
- Don't invent or claim real events, weather or trends. A real event may be used only after a live check confirms it is current.

## 2. Researcher ideas

- Read the Researcher's weekly page for Madison (Notion: Weekly Content Research > "Madison — Week of \[date\]") and any DM or ideas file.
- Keep only ideas that fit the story, the platform rules (step 11) and the current account status. If an idea is held (for example "HOLD UNTIL X IS RESTORED"), stay held until it is verified live.
- If the Researcher's idea conflicts with WEEK\_PLAN (for example squats were replaced by pickleball on Oct 20), WEEK\_PLAN wins. Note the conflict.

## 3. Stills: Seedream 5.0 Pro reference-edit

- References: her approved keepers only (<code>madison_face_keeper.png</code>, <code>mad20_face.jpg</code>, <code>madison_body_keeper.png</code>, about 1600 px). Never use a generated frame as a reference, and never chain edits.
- Number the photos in the prompt ("photo 1/2 = face, photo 3 = body, use only face and body, never clothing, pose or background").
- Paste <code>/workspace/madison_oct20/LOCKED_BODY_LINE.txt</code> word for word into every image and video prompt. Don't add hair-colour pushes that contradict it.
- Add the scene, a fitted scoop or open-placket top (baggy tees, sundresses and high necks shrink the bust), a warm golden tan ("NOT pale"), a candid phone shot, warm light, light natural skin texture, no gloss, no other people, no text, and head-to-mid-thigh framing with headroom.
- Size: 9:16 (or 4:5), 2k. Use 3-4 candidates per scene. Preflight with <code>get_cost</code> (2.5 cr each).
- Moderation: no bikini or two-piece wording (it gets NSFW-blocked and blocked jobs are still charged). Use a high neckline on any video start frame.

## 4. Identity gate + honest eye check

- Run <code>/workspace/.face-venv/bin/python /workspace/hf-test/zen/posting/identity_gate.py img --model madison --source seedream --body [files]</code>. The bar is centroid ≥ 0.78. Re-gate after finishing.
- The gate checks the face only. Every candidate must also be checked by eye at the same scale against <code>madison_body_keeper</code>: bust (the usual miss), waist, hips, tan, hair depth and volume, face fullness, hands, text, and background people.
- Pick the best one honestly. If none matches, regenerate; don't send a near-miss. A high gate score does not mean approved.

## 5. Video: Kling 3.0 + Element 04d4157b

- Image-to-video from a gated, eye-checked still with a soft closed-mouth smile, waist-up or wider.
- Use Madison Element <code>04d4157b</code>. Prompt lines: "keep the same face and body", "matte skin, no sheen", "natural blinks". Use "camera locked" only for propped-phone shots.
- Requirements: real action (pickleball, a hike, a pool cannonball), varied expressions across the week, no frozen background people (use empty locations), and the payoff early (in the first 2-3 s for transitions).
- Talking or lip-sync clips: Seedance 2.0 with <code>madison.mp3</code>, a line of 8 words or fewer, "begins speaking immediately". Check with whisper.
- Turn sound off unless she talks. Quote the cost first and report the credits.

## 6. Finish: light v4C skin

- Apply the v4C-lite finish (<code>/workspace/madison_oct20/lipsync/work/finish_v4Clite.py</code>): skin-masked luma texture, mild sharpen 0.3, light grain, no blur, JPEG q90, metadata stripped. Don't use v5 or a heavy finish.

## 7. Export

<code>ffmpeg -i in.mp4 -c:v libx264 -profile:v main -pix_fmt yuv420p -movflags +faststart -c:a aac -ar 48000 -b:a 128k -map_metadata -1 out.mp4</code><br />Full 9:16 (1080x1920 or 720x1280), no blurred padding bands, under 15 MB. Verify with ffprobe (profile=Main, yuv420p, aac 48000) before review. Keep the hook text in the top band from frame 1.

## 8. YouTube thumbnail

For each Short, take a JPG from a strong frame of the final clip (face clear, eyes open, the payoff visible), for example <code>ffmpeg -ss [t] -i out.mp4 -frames:v 1 -q:v 2 thumb.jpg</code>. Use 1080x1920 or a 1280x720 crop. No new generation.

## 9. Same-scale side-by-side

For every still or clip that shows Madison, build a sheet with the face keeper, the body keeper and the candidate (or 6 frames sampled across the clip) at the same height and scale, with <code>reference_set_madison.png</code> below. Write a body and hair match note.

## 10. Reviewer handoff (JSW Content Reviewer)

Send one message per batch with:

- file paths and captions
- platform labels (X-only for tease or suggestive content)
- credits spent, including redos and blocked jobs
- a story-fit note
- the side-by-side path with the match note
- gate scores

Use that bot's own messaging tool. Don't message the owner per clip. Resubmit only after fixing a FAIL.

## 11. Platform rules

- <b>X:</b> flirty, spicy and swearing are allowed. Tease content only (lingerie, bikinis, implied shots) with sensitive media on. No nudity or explicit content anywhere on X, including the profile picture, header and pinned post; nudity and explicit content go on Fanvue only.
- <b>TikTok, IG, YT, FB:</b> clean, SFW lifestyle, no swearing.
- <b>Fanvue:</b> no Fanvue link anywhere until Madison is verified. Use "more coming soon" teases only.
- <b>AI:</b> never advertise or deny AI in captions, lines, hooks or replies. Platform AI toggles are a separate setting.

## 12. Scheduler (after PASS only)

- After a Reviewer PASS on the exact file and caption, hand the item to the JSW Content Scheduler.
- Posting runs through AdsPower in headless mode only, profile <code>k1cwwjw5</code>. Never touch or change the proxy. Obey every AdsPower hold: don't touch AdsPower until Samuel says his Fanvue work is done.
- New X account @MadisonCole69: go slow. Start with 1-3 lifestyle-first posts a day plus a few genuine replies. Don't mass-follow, mass-like or post links. Ramp up only if there are no blocks; after any block, halve the pace for 48 h.
- Verify every post link live afterwards. State a platform's block instead of guessing.

## 13. Music

Never reuse a music track across clips or models. Use a new original track per clip (synth on the box) or a cleared library sound picked at posting time (TikTok Commercial Music Library). Log the track used.

## 14. Tracker feedback loop

- Read the JSW Performance Tracker and the Tracker's daily what's-working notes before planning the next day.
- Current notes: show the payoff sooner in transitions; always caption Facebook posts; Shorts with coffee-talk hooks perform best (1,215 views).

## 15. Learnings

Append a dated line to <code>/workspace/hf-test/zen/posting/SHARED_LEARNINGS.md</code> after each batch: what worked, what failed, credits, and file paths.

## SOP conflicts found (Oct 21, 2026), need Samuel's call

1. <b>Approval (resolved 2026-10-21 by JSW AI: a Reviewer PASS for the exact file is the approval):</b> the Notion Process page and MODEL\_CONTENT\_[PROCESS.md](http://PROCESS.md) say "no bot posts; Sam approves once per week-batch", and the Week of Oct 19 page says "nothing posted without Samuel's approval". The jsw-daily-content-process skill says the owner rule of 2026-10-20 makes a Reviewer PASS count as approval. This page follows the newer owner rule.
2. <b>Reviewer:</b> the skill pairs Gabriela to review Madison. In practice Madison goes to the JSW Content Reviewer bot.
3. <b>Gate threshold:</b> the Notion Process page lists 0.72 centroid / 0.74 best-ref. For Seedream stills the gate code uses a 0.78 centroid (<code>seedream_centroid</code>), which this page uses.
4. <b>Finishing:</b> the Notion Process page and MODEL\_CONTENT\_PROCESS §4 say Skin Enhancer "Realistic Skin" (\~4 cr). Current Madison practice and SHARED\_LEARNINGS say light v4C only.
5. <b>Aspect ratio:</b> the Notion Process page says 3:4 stills. This process uses 9:16 or 4:5, with full 9:16 for video.
6. <b>Video model:</b> CONTENT\_[RECIPE.md](http://RECIPE.md) (Sienna) says Seedance 2.0 for clips. The skill and WEEK\_PLAN say Kling 3.0 Element for action and Seedance only for talking.
7. <b>X account:</b> the Week of Oct 19 page says Madison's X is suspended (hold), and the Tracker lists @madisoncole26 (suspended). The new account is @MadisonCole69, and its status has not been verified live here.
8. <b>Fanvue link:</b> the Posting Calendar and the cross-platform plan say the Fanvue link goes in the X bio. Samuel's current rule is no Fanvue link until Madison is verified.
9. <b>Week page content:</b> the Week of Oct 19 X ideas include a string bikini, a striptease and implied-nude shower, bath and bed teases. These risk the NSFW block (two-piece wording gets blocked) and the "slow start, lifestyle first" rule for the new account. The Wed squat/leg-day idea was replaced by pickleball in WEEK\_PLAN (squats were overused across models).
10. <b>Music:</b> the Week page suggests a trending sound ("Windows in Brazil, sped up") for the recap. That conflicts with the no-reuse rule unless it is picked from the commercial library at posting time.
11. <b>Posting route:</b> the skill says the Scheduler posts via Ayrshare or AdsPower. For Madison this page says AdsPower headless only, profile k1cwwjw5, never touch the proxy.
12. <b>Batch size:</b> MODEL\_CONTENT\_PROCESS says 6 candidates per scene. Madison practice is 3-4 candidates per scene to save credits.

Sources: JSW AI Models > Process, Madison model page, Madison — Week of Oct 19, 2026; box files jsw-daily-content-process/[SKILL.md](http://SKILL.md), MODEL\_CONTENT\_[PROCESS.md](http://PROCESS.md), CONTENT\_[RECIPE.md](http://RECIPE.md), SHARED\_[LEARNINGS.md](http://LEARNINGS.md), madison\_oct20/WEEK\_[PLAN.md](http://PLAN.md). Skill copy: /workspace/xposts/jsw-madison-content\_[SKILL.md](http://SKILL.md)
</content>
</page>