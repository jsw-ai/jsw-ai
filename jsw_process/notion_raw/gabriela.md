Here is the result of "fetch" for the Page with URL https://app.notion.com/p/400f29949b2981af9c3dcfb5d7b53287 as of 2026-10-21T15:39:28.996Z:
<page url="https://app.notion.com/p/400f29949b2981af9c3dcfb5d7b53287">
<ancestor-path>
<parent-page url="https://app.notion.com/p/3faf29949b2981f1a41ce3862e0de35a" title="Gabriela"/>
<ancestor-2-page url="https://app.notion.com/p/3faf29949b29814b99abe52f2f4cc3c2" title="JSW AI Models"/>
</ancestor-path>
<properties>
{"title":"Gabriela daily content process (jsw-gabriela-content)"}
</properties>
<iconMetadata>null</iconMetadata>
<content>
Source: box skill <code>jsw-gabriela-content</code>, copied 10/21/2026. It builds on the shared JSW daily content process skill. Where the two conflict, the shared skill wins.

## 0. Read first, every batch

- /workspace/hf-test/zen/posting/SHARED\_[LEARNINGS.md](http://LEARNINGS.md)
- VALENTINA\_[PIPELINE.md](http://PIPELINE.md) (face and body consistency method)
- Gabriela's locked body line at /workspace/hf-test/zen/posting/gabriela\_locked\_body\_[line.md](http://line.md). Paste it word for word into every image or video prompt.
- The approved reference board and keepers.
- Gabriela's Notion week page and the JSW Notion SOP.

## 1. Weekly story

Each week has a planned story with one beat per day (e.g. Brazil trip home: airport outfit change, flight, churrasco with her mom, leg day, Ipanema, samba night, boat day, flight back). Every post belongs to that day's beat, never a random idea. Sexy within SFW, aspirational life (beach, gym in tight shorts, golf, parties, first-class travel). No generic walking-around clips.

## 2. Ideas (2 to 3 posts a day)

- One simple idea with a payoff or transition, such as a hand-over-lens outfit change.
- Each clip has 3 to 4 cuts in 8 to 9 seconds.
- One line of on-screen text at the very top from the first frame, kept off her face.
- Captioned identity hook (Brazilian, São Paulo, Miami).
- Vary her poses across shots.
- Check the Researcher's notes and verify any trending event live before using it.
- Log the setting and outfit for every clip.

## 3. Generation

- <b>Stills:</b> Seedream 5.0 Pro reference edit from an approved photo, even front light on her face.
- <b>Video:</b> Kling 3.0 Element, starting from a still with a soft closed-mouth smile. Prompt lines: "keep the same expression, eyes open", "matte skin, no sheen", "camera locked, no zoom".
- <b>Lip sync:</b> she talks within the first second.
- <b>Takes:</b> 2 or more per shot.
- <b>Look:</b> light natural skin texture only. No tattoos or marks, no frozen people in the background.
- <b>Credits:</b> quote the cost before generating and report exact credits after.

## 4. Self check

- Same-scale side-by-side of frames from across the whole clip next to the reference sheet (face, body, hair). The identity gate checks the face only.
- Redo any drift. Body or hair drift is an automatic fail.

## 5. Export

- <code>ffmpeg -c:v libx264 -profile:v main -pix_fmt yuv420p -movflags +faststart</code>; under 15 MB, full 9:16, no padding bands; check with ffprobe.
- Clips without lip sync get royalty-free Brazilian music (funk, samba, bossa) cut to the beat, plus a silent copy. CC BY credit in the caption when needed.
- One distinct cut per platform (cutTT, cutIG, cutRD, cutX, plus the YouTube file), each with its own opening, hook and track.
- YouTube Shorts need <code><clip>_thumb.jpg</code> at 1080x1920 from the best frame.

## 6. Platform rules

- No AI mentions, but never deny it. Apply any AI label a platform or subreddit requires.
- No swimwear on YouTube.
- TikTok, Instagram, YouTube and Facebook stay clean with no Fanvue links.
- X allows tease content, swearing and provocative captions, with media marked sensitive. Until her Fanvue exists, use "coming soon" teases.
- No nudity off Fanvue.
- Reddit needs proof of the subreddit's rules and AI flair.

## 7. Reviewer handoff

Send the JSW Content Reviewer: file paths, side-by-sides, thumbnail, captions per platform, setting and outfit, credits spent.

## 8. Scheduler handoff

Send passed files to the JSW Content Scheduler with captions and credits. Note what was scheduled, then log learnings in SHARED\_[LEARNINGS.md](http://LEARNINGS.md).

## Hard rules

- AdsPower runs headless only. Never edit the proxy. Respect any AdsPower hold.
- Never post in Slack as the owner.
- Keep secrets in the secrets folder and never print them.
- Don't retry failed logins. Leave locked accounts alone.

## Conflicts with SOP

Compared 10/21/2026 against SOP: Content Scheduling, SOP: JSW review gate (Reviewer), JSW AI Models › Process, Gabriela's model page, and Gabriela — Week of Oct 19, 2026.

1. <b>Approval.</b> Skill: "Send passed files to the JSW Content Scheduler". Week page: "Ideas only: nothing is posted without Samuel's approval." Process page: "Rule zero: no bot posts anything. Sam approves once per week-batch, never per photo." Scheduling SOP (Oct 21, newest): "A PASS is the approval (owner rule, Oct 20); no separate Samuel sign-off per clip."
2. <b>Nudity on X.</b> Skill: "No nudity off Fanvue." Week page rules: "No full nudity or explicit content on X", but the Sun 10/25 plan has "Topless still from behind at the shoreline" (Outfit: "thong bikini bottoms only"). Review gate SOP: "X: spicy or topless content must be marked sensitive". Process page: "X 3-5/day (no nudity)".
3. <b>Posts per day.</b> Skill: "Ideas (2 to 3 posts a day)". Process page: "Cap 3 posts per day per model." Scheduling SOP: "TikTok \| 3", "Instagram \| 2 Reels", "YouTube Shorts \| 2–3", "X \| 4–6". Week page plans 4 X posts a day.
4. <b>AdsPower.</b> Skill: "AdsPower runs headless only. Never edit the proxy. Respect any AdsPower hold." Scheduling SOP: "never open or use it without asking in the JSW room first and getting a yes." Week page: "all sessions start only after Samuel confirms AdsPower is free".
5. <b>Music.</b> Skill: "royalty-free Brazilian music (funk, samba, bossa)". Week page: "All sounds must be checked in TikTok's commercial library before use." Its ideas also use "trending Brazilian funk sound (to check)" and "Sound: Training Season".
6. <b>Reference pack status.</b> Skill: "The approved reference board and keepers." Gabriela model page: "the pack is a draft and unapproved." Process page: "Only Sienna and Camille packs are approved."
7. <b>Skin finish.</b> Skill: "light natural skin texture only". Process page: "Skin Enhancer "Realistic Skin" (about 4 cr), then re-gate." Gabriela page: "Use a light v4C finish only."
8. <b>Body line file.</b> Skill: "gabriela\_locked\_body\_[line.md](http://line.md)". Gabriela page lists "zen/posting/gabriela\_body\_[spec.md](http://spec.md)" (no locked-body-line file).
9. <b>Gym/leg day.</b> Skill story example includes "leg day" and "gym in tight shorts". Week page: "gym and squats belong to Madison this week, so Thu X posts skip the gym". Review gate SOP: "Gym content: different setups, and never two models on the same day."
10. <b>Boat day.</b> Skill story example: "boat day". Week page: "Sun uses the suggested Lopes Mendes beach day, not the boat (Valentina has the boat day)."
</content>
</page>