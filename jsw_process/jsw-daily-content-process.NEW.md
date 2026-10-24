---
name: JSW daily content process
description: >-
  Use when running or auditing the daily content cycle for the six JSW AI
  models: research, create, face-and-body check, JSW Content Reviewer PASS
  (= approval), Ayrshare scheduling, tracking.
---
# JSW daily content process (shared rulebook)

Goal: every model gets fresh content every day that fits her weekly story, passes the JSW Content Reviewer and is scheduled through Ayrshare.

**Precedence:** Samuel's settled rules come first. Next is the model's own skill, which wins over this shared file. Then SOP: Content Scheduling (Notion). Flag any remaining gap to JSW AI. Verify every account or status fact live, and label anything unchecked as unverified.

## Settled rules (Samuel)
- **Approval:** a JSW Content Reviewer PASS for the exact file (path and version) and its exact captions is approval to post. Samuel doesn't approve each post. Don't send clips to Samuel or his Drive.
- **Review:** only the JSW Content Reviewer bot issues a PASS or FAIL, and only it forwards a PASS to the Scheduler. Models never review each other and never forward a PASS.
- **Posting:** the JSW Content Scheduler posts only through Ayrshare. Model bots never post.
- **AdsPower:** frozen for every bot until Samuel says his Fanvue work is done. The freeze covers posting, engagement, Fanvue uploads and stats reads. After the freeze lifts, run it headless only and never touch the proxy.
- **AI:** disclose AI wherever a platform requires it (TikTok AI toggle, IG label, YouTube synthetic disclosure, Reddit flair, Fanvue AI flag). Never deny it. Don't make it the point of the caption.
- **Platforms:**
  - TikTok, Instagram, YouTube and Facebook stay clean: no Fanvue, no spice, no swearing. IG and TikTok get reels, not single stills.
  - X takes spicier tease: lingerie, bikinis, implied shots and **topless**, always marked sensitive. That media is X-only and is never used as a profile or header image. No full nudity or explicit content on X.
  - Full nudity and explicit content go on Fanvue only.
  - X content is short clips first, with photos mixed in.
- **Fanvue links:** only for Sienna and Charlotte, and only in the X bio, an X pinned post set by hand, and Reddit. Never put the link in a caption or scheduled post; write "link in bio". Every other model (Valentina's verification failed) uses "coming soon" at most.
- **Banned everywhere:** anything suggesting someone is underage, non-consent, content aimed at real people, and invented events.

## Daily cycle
1. **Story:** each model has one weekly story with one beat per day. Every post moves that day's beat forward. No two models share a theme or activity (gym, pool, boat, flight and so on) on the same day. The Posting Calendar wins for the day's slot.
2. **Ideas:** start from the Researcher's weekly page and the Tracker's what's-working notes (7 AM). Live-verify any real event, trend or sound before generating, since spoken lines get baked in. TikTok sounds come from the commercial library or are royalty-free.
3. **Stills:** Seedream 5.0 Pro reference-edit from the model's approved references only, with the locked body line pasted word for word, even front light, and a local v4C finish (no blur). Never chain edits.
4. **Video:**
   - **Silent clips:** Kling 3.0 with the model's Element, from a gated still.
   - **Lip-sync and talking:** Seedance 2.0 i2v from a gated still with the model's voice reference. Check it with whisper, word for word.
   - **Cost:** quote it before generating, and report the exact credits afterwards, including redos.
5. **Face and body check:**
   - **Stills:** `identity_gate.py img --model <m> --source seedream --body`, which must reach **0.78**.
   - **Clips:** `identity_gate.py video --model <m>`.
   - **Always:** a same-scale side-by-side of frames from across the whole clip next to the reference sheet, plus a by-eye body and hair note. A passing score alone isn't approval.
6. **Export:** H.264 Main, yuv420p, faststart, under 15 MB, full 9:16 1080x1920 with no blur bands. Verify with ffprobe. **Every YouTube Short** gets a `<clip>_thumb.jpg` at 1080x1920 from the clip itself. Each platform gets its own cut, and one file goes to one platform only.
7. **Submit to the Reviewer:** send the files, the caption per platform, the platforms, the X-only and sensitive tags, credits, the side-by-side and the thumbnail. After a FAIL, fix exactly what was flagged and resubmit. After a PASS, the Reviewer logs it and forwards it to the Scheduler.
8. **Schedule:** the Scheduler takes Reviewer PASSes only, runs its pre-checks, schedules through Ayrshare, logs the Posting Calendar, verifies live links and sends Samuel only the clean "safe to boost" posts.
9. **Track and learn:** the Tracker logs the results. Models append dated learnings to `SHARED_LEARNINGS.md`.
10. **Engage:** only after the AdsPower freeze lifts. Run 3-4 TikTok sessions a day per model, 10-20 minutes each, staggered so models don't overlap, headless, one platform per session, within the warm-up caps.
11. **Deletes and passwords:** deleting live posts or changing a password needs Samuel's own explicit yes.

## Cadence
- **Platform caps:** per the Scheduler SOP cadence table. Valentina gets 1 TikTok a day. Madison's YouTube runs 2-3 Shorts a day. X leads with clips, and at least half of X posts are teases.

## Routine times (ET)
- **Tracker notes:** 7:00 AM.
- **Models:**

  | Time | Model |
  |---|---|
  | 8:00 AM | Camille |
  | 8:15 AM | Charlotte |
  | 8:30 AM | Gabriela |
  | 8:45 AM | Valentina |
  | 9:00 AM | Madison |
  | 2:30 PM | Sienna |

- **Reviewer:** 8:30 AM, 11:30 AM, 2:30 PM, 5:30 PM and 8:30 PM.
- **Scheduler:** 9 AM, 12 PM, 3 PM, 6 PM and 9 PM.
- **Researcher:** Sunday 7:30 PM, after the Tracker's 6 PM weekly report.
- **Submission timing:** submit before the next Reviewer run so a PASS reaches the Scheduler run 30 minutes later.
