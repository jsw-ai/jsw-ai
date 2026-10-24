
Reusable daily template for Camille. Replace `<week>` (e.g. `camille_oct20`), `<day>` and `<clip>`.
Base dir: `/workspace/hf-test/zen/posting/`. Read first: `MODEL_CONTENT_PROCESS.md`, `CONTENT_RECIPE.md`,
`HIGGSFIELD_EXPERT_GUIDE.md`, `SHARED_LEARNINGS.md`, `<week>/LOCKED_BODY.txt`, `<week>/WEEK_PLAN.md`,
`/home/box/agent-data/workflows/jsw-daily-content-process/SKILL.md`, and Camille's weekly Notion page.

Routine: runs daily at 8:00 AM ET.
Precedence: this skill (Camille's own) beats the shared jsw-daily-content-process skill. Flag any remaining gap to JSW AI.
Hard limits: max 3 posts/day, about 70% video and at most 30% stills (carousels). Camille never posts. Posting goes only through Ayrshare, via the JSW Content Scheduler.
No AdsPower at all (posting, uploads or engagement) until Samuel says his Fanvue work is done.

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
4. Silent clips: Kling 3.0 with Element `e3a57e1a-19fd-4d3c-8e92-c1b306a46ace`, from a gated, finished start still (soft closed-mouth smile, waist-up). Prompt lines: "keep the same expression, smile with eyes open, natural blinks only", "keep freckles and skin texture", "matte skin, no sheen". Sound off unless talking.
5. Lip-sync and talking clips: Seedance 2.0 i2v from an approved start still with Camille's voice reference; transcribe and check the line word for word.
6. Creative rules: 2+ takes per shot; one idea with a payoff; 3-4 cuts in 8-9 s; on-screen text from frame 1; she's actually doing something; no frozen background people (or none at all).
7. Finish: matte skin via `finish_v4C.py` (copy from `camille_test/finish_v4C.py`), no blur ever.
8. Check: `identity_gate.py img --model camille --source seedream --body` on stills (face gate 0.78) and `identity_gate.py video --model camille` on clips, plus a visual check of body, hair and outfit against REFERENCE_CONTACT_SHEET_v4. Extract and check frames every 0.5 s across the whole clip (drift shows at 3-5 s). Redo any take that drifts.
9. Log credits spent, including redos, per item and day total.

## 4. Export
- `ffmpeg -i in.mp4 -c:v libx264 -profile:v main -pix_fmt yuv420p -movflags +faststart -map_metadata -1 ... out.mp4`
- Full 9:16 1080x1920 (Kling 720x1276: scale to 1084 wide, crop 1080x1920), no blur bands, under 15 MB. Verify with ffprobe.
- Thumbnail `<clip>_thumb.jpg`, 1080x1920, from the best frame, using the OpenCV venv `/workspace/thumbs/venv` (create it if missing: `python3 -m venv /workspace/thumbs/venv && /workspace/thumbs/venv/bin/pip install opencv-python-headless`).

## 5. Platform rules
- TikTok, Instagram, YouTube, Facebook: clean. No Fanvue mentions, no spice, no swearing; AI label/toggle ON where the platform requires it (settings only).
- X: tease content is X-only, labeled "X-only", sensitive media on; tease posts are at least half of each day's X posts. Topless is allowed on X only, marked sensitive, and never as a profile or header image. Full nudity and explicit content are Fanvue only, so never for Camille.
- No Fanvue for Camille anywhere: no link, no mention, never in a caption (Fanvue is Sienna and Charlotte only). Use "coming soon" wording at most.
- Never mention or deny AI in captions, hashtags, hooks, spoken lines or on-screen text.

## 6. Review and hand-off
- Send to the JSW Content Reviewer (`99a98fb5-f7d1-48c7-aee8-44145d400592`): file paths, captions per platform, credits spent, a same-scale side-by-side vs REFERENCE_CONTACT_SHEET_v4 (frames across the clip), and the thumbnail.
- Only the JSW Content Reviewer issues a PASS, and a PASS is the approval of that exact file and its captions. The Reviewer (not Camille) forwards each PASS to the JSW Content Scheduler (`d3859293-ae63-4af6-a544-0dfcb66b2c13`), which posts via Ayrshare. Models don't review each other.
- FAIL: fix what was flagged and resubmit. Don't send clips to Samuel or his Drive.

## 7. Learnings and engagement
- Append dated learnings (what worked, failed, credits) to `SHARED_LEARNINGS.md`.
- Engagement sessions: none while AdsPower is frozen, i.e. until Samuel says his Fanvue work is done. After that, use the Researcher's TikTok engagement bank and cross-platform follow plan on Camille's page, with the pacing page for limits: headless profile 6 only, staggered in the ET morning.

## Conflicts (all resolved per JSW AI, 2026-10-21; see /workspace/jsw_process/CONFLICT_REVIEW_2026-10-21.md)
- RESOLVED: Approval. Only a JSW Content Reviewer PASS is approval; the Samuel-approval line on Camille's week page and the old Process page are superseded.
- RESOLVED: Reviewer. Models don't review each other (the peer pairings are dropped). The Reviewer forwards each PASS to the Scheduler.
- RESOLVED: Day 7 is the Vespa ride in WEEK\_PLAN and Notion.
- RESOLVED: Gym. Day 2 is a Cours Saleya market to Castel beach morning; no gym, pool or boats.
- RESOLVED: Fanvue. It's Sienna and Charlotte only and never in a caption; Camille has no Fanvue anywhere, including the X bio.
- RESOLVED: X content. Topless is OK on X only, marked sensitive, never as a profile or header image; full nudity and explicit content are Fanvue only. Swearing stays on X, never on TikTok, IG, YT or FB.
- RESOLVED: Posting and engagement. Posting goes through Ayrshare via the Scheduler only; no AdsPower at all, engagement included, until Samuel says his Fanvue work is done (then headless profile 6 only).
- RESOLVED: Models. Lip-sync is Seedance 2.0, silent clips are Kling 3.0, and the face gate is 0.78.
- RESOLVED: Routine runs at 8:00 AM ET, and this skill beats the shared skill.
