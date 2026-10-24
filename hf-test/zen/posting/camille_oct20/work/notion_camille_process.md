
Reusable daily template for Camille. Replace `<week>` (e.g. `camille_oct20`), `<day>` and `<clip>`.
Base dir: `/workspace/hf-test/zen/posting/`. Read first: `MODEL_CONTENT_PROCESS.md`, `CONTENT_RECIPE.md`,
`HIGGSFIELD_EXPERT_GUIDE.md`, `SHARED_LEARNINGS.md`, `<week>/LOCKED_BODY.txt`, `<week>/WEEK_PLAN.md`,
`/home/box/agent-data/workflows/jsw-daily-content-process/SKILL.md`, and Camille's weekly Notion page.

Hard limits: max 3 posts/day, about 70% video and at most 30% stills (carousels). Camille never posts; the Scheduler does.
Never touch AdsPower unless Samuel has said it is free (see step 7).

## 1. Weekly story
- Open `<week>/WEEK_PLAN.md` and Camille's weekly Notion page. Find today's day number and its story beat (concept, format, hook, outfit, sound, caption).
- Today's post must move that story forward. If the file and Notion disagree, follow WEEK_PLAN and flag the difference.
- Check overlaps with other models this week (e.g. no boats = Valentina, gym/squats = Madison).

## 2. Ideas
- Take ideas from the JSW Content Researcher (agent `7c0fb063-1296-4cd7-9ecb-f63c00c59265`) and its Notion page (Weekly Content Research, Camille section).
- Keep only ideas that fit today's story beat.
- Trends, sounds and events: live-verify each one today (web/X search; sounds in TikTok's commercial library). Never invent one. Drop any trend you can't verify.

## 3. Generation (Higgsfield)
1. Check the shared Higgsfield credit balance first, then quote the cost (`get_cost:true`) before generating.
2. Stills: Seedream 5.0 Pro reference edit, refs led by `camille_oct16/REFERENCE_CONTACT_SHEET_v4.jpg` (Body 1 + Face 1). Even front light on the face. Re-anchor from the original refs every time; to fix a scene, edit a passing still.
3. Paste this LOCKED_BODY line word for word into every prompt (source `<week>/LOCKED_BODY.txt`):
   > woman in her mid-20s, medium height, slim-curvy natural build; full natural C-D cup bust with visible soft cleavage (exactly as Body 1), narrow defined waist, softly rounded hips, toned slim arms; voluminous jet-black tight natural ringlet curls, shoulder-length chin-to-shoulder bob with big volume and side part; warm light-olive / light-tan skin with faint freckles across nose and cheeks, matte natural skin texture.
4. Motion: Kling 3.0 with Element `e3a57e1a-19fd-4d3c-8e92-c1b306a46ace`, from a gated, finished start still (soft closed-mouth smile, waist-up). Prompt lines: "keep the same expression, smile with eyes open, natural blinks only", "keep freckles and skin texture", "matte skin, no sheen". Sound off unless talking.
5. Lip-sync: Seedance 2.0 i2v from an approved start still with Camille's voice reference; transcribe and check the line word for word.
6. Creative rules: 2+ takes per shot; one idea with a payoff; 3-4 cuts in 8-9 s; on-screen text from frame 1; she's actually doing something; no frozen background people (or none at all).
7. Finish: matte skin via `finish_v4C.py` (copy from `camille_test/finish_v4C.py`), no blur ever.
8. Check: `identity_gate.py` (face) plus a visual check of body, hair and outfit against REFERENCE_CONTACT_SHEET_v4. Extract and check frames every 0.5 s across the whole clip (drift shows at 3-5 s). Redo any take that drifts.
9. Log credits spent, including redos, per item and day total.

## 4. Export
- `ffmpeg -i in.mp4 -c:v libx264 -profile:v main -pix_fmt yuv420p -movflags +faststart -map_metadata -1 ... out.mp4`
- Full 9:16 1080x1920 (Kling 720x1276: scale to 1084 wide, crop 1080x1920), no blur bands, under 15 MB. Verify with ffprobe.
- Thumbnail `<clip>_thumb.jpg`, 1080x1920, from the best frame, using the OpenCV venv `/workspace/thumbs/venv` (create it if missing: `python3 -m venv /workspace/thumbs/venv && /workspace/thumbs/venv/bin/pip install opencv-python-headless`).

## 5. Platform rules
- TikTok, Instagram, YouTube, Facebook: clean. No Fanvue mentions, no spice, no swearing; AI label/toggle ON where the platform requires it (settings only).
- X: tease content is X-only, labeled "X-only", sensitive media on, no nudity; tease posts are at least half of each day's X posts.
- No Fanvue link anywhere until Camille's Fanvue exists (a linked account from Charlotte's, later). Use "coming soon" wording.
- Never mention or deny AI in captions, hashtags, hooks, spoken lines or on-screen text.

## 6. Review and hand-off
- Send to the JSW Content Reviewer (`99a98fb5-f7d1-48c7-aee8-44145d400592`): file paths, captions per platform, credits spent, a same-scale side-by-side vs REFERENCE_CONTACT_SHEET_v4 (frames across the clip), and the thumbnail.
- PASS = approval of that exact file and captions. Hand off to the JSW Content Scheduler (`d3859293-ae63-4af6-a544-0dfcb66b2c13`).
- FAIL: fix what was flagged and resubmit. Don't send clips to Samuel or his Drive.

## 7. Learnings and engagement
- Append dated learnings (what worked, failed, credits) to `SHARED_LEARNINGS.md`.
- Engagement sessions (Researcher's TikTok engagement bank and cross-platform follow plan on Camille's page; pacing page for limits) only when AdsPower is free and Samuel OKs engagement, headless profile 6 only. Nice local time, staggered in the ET morning.

## Conflicts to resolve (flagged 2026-10-21)
- Approval: Camille's weekly page says "nothing is posted without Samuel's approval"; the SOP (owner rule 2026-10-20) says a Reviewer PASS counts as approval. This process follows the SOP.
- Reviewer: the SOP's peer-review step says Madison reviews Camille; this process uses the JSW Content Reviewer bot.
- Day 7: Camille's page still says golf above Cannes; WEEK_PLAN.md now says Vespa ride (changed 2026-10-21). The Notion page was not edited.
- Gym: Day 2 (hotel gym squats) clashes with Madison owning gym/squats this week (the page flags this itself).
- Fanvue: the cross-platform section says "Fanvue only in the X bio" and the X rules say "until verified"; this process says no Fanvue link anywhere until Camille's Fanvue exists. The SOP says no Fanvue links except Sienna.
- Swearing: some X lifestyle captions use putain/merde/bordel; those are fine on X but can't be reused on TikTok/IG/YT/FB.
- Engagement: Camille's page and the pacing page don't mention "headless profile 6 only".
- The older JSW AI Models > Process page says "Sam approves once per week-batch" (out of date).
