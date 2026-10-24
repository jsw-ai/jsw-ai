Here is the result of "fetch" for the Page with URL https://app.notion.com/p/400f29949b298103bd92fe2f6ea6c6f8 as of 2026-10-21T15:39:03.999Z:
<page url="https://app.notion.com/p/400f29949b298103bd92fe2f6ea6c6f8">
<ancestor-path>
<parent-page url="https://app.notion.com/p/3fff29949b2981e48162c64478722402" title="Valentina — Week of Oct 19, 2026"/>
<ancestor-2-page url="https://app.notion.com/p/3fff29949b2981198039cbba4486ae38" title="Weekly Content Research - Week of Oct 19, 2026"/>
<ancestor-3-page url="https://app.notion.com/p/3d5f29949b298167a5efc5920f09f973" title="JSW AI"/>
<ancestor-4-page url="https://app.notion.com/p/3d5f29949b2981de934ce8472408dfdd" title="Brixmont Operations Hub"/>
</ancestor-path>
<properties>
{"title":"Valentina daily content process (jsw-valentina-content)"}
</properties>
<iconMetadata>null</iconMetadata>
<content>
Daily step-by-step content cycle for JSW model Valentina. Written 2026-10-21 from MODEL\_CONTENT\_[PROCESS.md](http://PROCESS.md), CONTENT\_[RECIPE.md](http://RECIPE.md), SHARED\_[LEARNINGS.md](http://LEARNINGS.md), HIGGSFIELD\_EXPERT\_[GUIDE.md](http://GUIDE.md), LOCKED\_BODY\_LINE.txt, the shared jsw-daily-content-process skill, FANVUE\_ACADEMY\_[PLAYBOOK.md](http://PLAYBOOK.md), and the JSW Notion pages (Week of Oct 19, TikTok pacing, cross-platform warm-up plan). Where sources disagree, see "Conflicts" at the end. When rules conflict, the stricter one wins until Samuel decides.

## 0. Before you start (every day)

- Read the JSW room. If anyone has posted an AdsPower hold, don't touch AdsPower until Samuel confirms it is free. AdsPower runs headless only (local API + Playwright CDP), never as a visible browser.
- Check valentina\_posted\_log.json and Ayrshare /api/history (it needs the Authorization key and Valentina's Profile-Key). Never repost a file that has already gone out.
- Before planning an action clip, check what the other models are doing this week. Don't copy another model's outfit, set or activity. Gym/squats belong to Madison this week.
- Daily cap: max 3 posts per platform per model (TikTok max 1/day while throttled). Aim for about 70% video and at most 30% carousels. No single stills, only carousels, reels or video.

## 1. Weekly story

- Current arc (Week of Oct 19): Valentina goes home to Colombia, to Cartagena, where mom and the tías comment on everything. Days: Mon salsa class, Tue first class to Cartagena, Wed rooftop pool ("¿y el novio?"), Thu old city to salsa (red dress, mom's curfew), Fri Rosario Islands boat day (mama's sunscreen texts), Sat family lunch (patacones, single questions), Sun heading back (suitcase full of food).
- Read that day's entry and the X post list on the Week of Oct 19 page (Notion 3fff29949b2981e48162c64478722402) before making anything. Each week's new story page replaces this one.

## 2. Ideas

- Start from the Content Researcher's picks for the day (weekly page, IG Reels trending picks, X post list).
- Apply the Tracker's feedback: short flirty hooks, funny to-camera lip-sync Shorts, and dance clips come first.
- Real events, trends, sounds, weather and holidays are allowed, but live-verify each one (source plus date) before you generate, because spoken lines are baked into the video. Never invent one. Check each sound in TikTok's commercial library.
- Plan per platform: one clean lifestyle cut for TikTok, IG, FB and YouTube, and X lifestyle plus tease posts (at least half of the day's X posts are tease).

## 3. Generation

- Look: the approved test2 look only. Refs are valentina\_test2/up/ (see also valentina\_test2\_contact\_sheet.jpg, NEW columns).
- Stills: use Seedream 5.0 Pro reference-edit from valentina\_test2/up refs ("Edit this exact photo…", 3:4, 2k, even front daylight on the face). Never chain edits; re-anchor from the original refs every time. Finish with v4C: light, natural, matte skin, no sheen, no blur.
- Video: use Kling 3.0 Element built from 3 approved, matte, clothed stills. The start frame is an approved still with a soft closed-mouth smile, waist-up, hands resting on something if possible. Always include these lines in the prompt: "keep the same expression, smile with eyes open, natural blinks only", "matte skin, no sheen", "camera locked, no zoom". Sound off unless the clip is lip-sync.
- Paste the locked body line word for word into every image and video prompt:
  > Valentina: Latina woman in her late 20s, about 5'6", slim-athletic build with a narrow waist and softly curved hips, full perky medium-large natural bust (C/D cup) with visible natural cleavage in low necklines, toned slim arms and legs; long dark-brown almost black hair, wavy to loose curls, high volume, falling past her shoulders to mid-chest, middle-ish part; warm light-olive tan skin with light natural texture, matte, no sheen; no tattoos.
- Never: frozen background people (use empty backgrounds), tattoos, glossy or smoothed skin, logos or text in the scene. Seedance flagged a one-piece pool still as NSFW, so use a sundress or cover-up for pool lip-syncs.
- Credits: quote the cost (get\_cost) before generating. Afterwards, report the exact credits spent from transactions, including redos, refunds and wasted attempts.

## 4. Checks

- Build a same-scale side-by-side of 4–6 frames sampled across the whole clip (drift shows at 3–5 s) next to valentina\_test2\_contact\_sheet.jpg. Write a match note covering body (bust, waist, hips, build) and hair (colour, length, curl, volume).
- Look at body and outfit yourself, not just the face gate (identity\_[gate.py](http://gate.py) checks the face only). Also check eyes open and not mid-blink, expression, hands and fingers, tattoos or odd arms, glossy skin, frozen background people, garbled text, and that props match the caption.
- For lip-sync, transcribe the audio with faster-whisper; it must match the line word for word. If any check fails, reroll or fix the still before spending more on video.

## 5. Export

- ffmpeg: -c:v libx264 -profile:v main -pix\_fmt yuv420p -movflags +faststart, 1080x1920, under 15 MB, full 9:16 with no blurred padding. Check with ffprobe.
- On-screen text goes in the top or bottom band only, never over the face.
- Clips without lip-sync need licensing-safe music (commercial library or royalty-free).
- Make a separate cut and caption for each platform.
- YouTube Shorts thumbnail: \<clipname>\_thumb.jpg, 1080x1920, from a sharp frame with a clear face, not mid-blink.

## 6. Reviewer handoff, then Scheduler

- Send the JSW Content Reviewer: the final file(s), captions per platform, the side-by-side sheet with the body/hair note, the thumbnail, credits spent, and an "X-only, mark sensitive" label on any tease content.
- After a Reviewer PASS on the exact file and captions, hand off to the JSW Content Scheduler (Ayrshare, or headless AdsPower when no hold is active). Log the post in valentina\_posted\_log.json, verify the live links, and add what you learned to SHARED\_[LEARNINGS.md](http://LEARNINGS.md).

## Platform rules

- TikTok, IG, FB and YouTube: clean only. No Fanvue links, no spicy content, no swearing. On TikTok, no dating or red-flag hashtags, and max 1 post a day while throttled.
- X: tease, sensitive and provocative captions are allowed, with sensitive media marked. At least half of the day's X posts are tease. Never nudity, and nothing suggesting underage, non-consent, or real people.
- Fanvue: Valentina's account is NOT verified. No Fanvue link anywhere, including the X bio. "More coming soon" is the most a caption can say.
- AI: never mention AI in captions, hashtags, hooks or spoken lines, and never deny it. Platform AI toggles stay ON as settings only.

## Engagement sessions

- Follow the Researcher's TikTok engagement bank (Cartagena, salsa, champeta, Colombian food niches; 25 comments) and the week-1 cross-platform follow plan (Notion 400f29949b2981dcb05dc727f29edb80).
- Sessions only start after Samuel confirms AdsPower is free, run headless, and use one platform per session. Stagger with the other models (Valentina runs ET late morning to afternoon). Follow first, watch fully, never repeat a comment.
- Week 1 caps: TikTok 2 follows, 3–15 likes, 1 comment. IG 3–5 follows. X 5–10 follows and 3–5 replies. YouTube 2–3 subs. FB 2–3 pages. Reddit: join and upvote only, no comments. If an action gets blocked, stop it for 48 h and go back to week-1 numbers.

## Conflicts found

1. Approval: the shared skill (owner rule 2026-10-20) says a Reviewer PASS counts as approval. MODEL\_CONTENT\_[PROCESS.md](http://PROCESS.md), CONTENT\_[RECIPE.md](http://RECIPE.md), the Notion Process page ("no bot posts; Sam approves per week-batch") and the Week of Oct 19 page ("nothing posted without Samuel's approval") still require Samuel.
2. Reviewer pairing: the skill pairs Valentina with Charlotte, but SHARED\_LEARNINGS records Madison and Valentina as reviewers for each other, and Madison did review her.
3. Video model: the task specifies Kling 3.0 Element, but CONTENT\_RECIPE and recent Valentina lip-syncs (Oct 19–20) used Seedance 2.0, since Kling Element sound-on talking isn't the documented lip-sync path. The skill also says Seedance multi-reference failed for identity.
4. Cadence: the Notion Process page says TikTok 1–2/day and the skill allows 3/day, but while throttled TikTok is max 1/day.
5. AI labels: the Fanvue Academy playbook says Reddit and subreddits may require AI labels or flair. That is compatible with "never deny AI" but clashes with "never mention AI" if a label goes in the post.
6. The week page's X tease ideas ("top untied", "dress slips down", "striptease-dance", lingerie stills) are close to the no-nudity line and to Seedance NSFW filters, so they need careful framing. The week page also puts the flight home on Wed 10/21 in the IG picks but on Sun 10/25 in the story.
</content>
</page>