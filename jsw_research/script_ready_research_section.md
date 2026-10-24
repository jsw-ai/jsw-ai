## Research pull (JSW Content Researcher)
Sources: box skills jsw-daily-idea-slate, jsw-business-research-rotation, jsw-weekly-content-research, jsw-midday-trend-pulse, jsw-evening-performance-dig, and /workspace/jsw_research outputs. **(to confirm)** means the files did not back it up.

**Schedules:** daily slate at 6 AM ET. Rotation every 2 h, 8-22 ET; the hour-to-focus map is (to confirm), and the last run sends the top 1-3 business ideas to JSW AI. Weekly research Sunday 7:30 PM ET, after the Tracker's 6 PM report. Midday and evening run times are (to confirm).

1. **Tracker pull.** Read the Tracker rankings, Post Performance DB, Stats Dashboard (refreshed by /workspace/jsw_tracker/refresh.py) and posts.json (box path to confirm) with user-Notion notion-search / notion-fetch. Output: per-model winners and flops by hook, format, platform and slot, with medians. Pass: real numbers only, cited with the refresh time. The evening dig covers the last 48-72 h and writes keep / kill / test / timing.
2. **Competitor and trend pulls.**
   - X connector: search_posts_all (query; since:YYYY-MM-DD in UTC), get_posts_counts_recent (7 days), get_trends_by_woeid, search_news, get_users_by_username → get_users_posts, get_posts_by_ids. Use these for live bio and URL checks too.
   - TikTok, IG and YT: WebSearch / WebFetch on public trend sources (for example Virlo, newengen, Modash).
   - Reddit: `cd /workspace/jsw_research/sienna_subreddits && python3 fetch.py SUB1 SUB2` (Playwright plus Chrome) writes raw_SUB_rules.json and raw_SUB_about.json. Known failure: Reddit returns an HTML wall to the box.
   - Output: about 10 niche accounts per model, each with hook, format, sound, time, comment bait and a link.
3. **Idea slate.**
   - Files: /workspace/jsw_research/daily_ideas_YYYY-MM-DD[_vN].md and slates_YYYY-MM-DD/MODEL.md.
   - Each idea lists: platform, format, hook line, sound, reference link, caption/CTA, slot and transition.
   - Count: fill each model's full daily quota. The "5 per model" minimum is (to confirm).
   - Verified pass rules: at least 1 music video and 1 comedy idea each; no format more than twice a day; same-platform videos at least 3 h apart; one cut per platform; TikTok sound from the commercial library or marked unverified with her own track as fallback; no lip-sync, singing or talking without a passed face test; face-gate-friendly framing (front light, closed mouth, 0.78 gate); never mention AI; no Fanvue in captions; real events only; cross-model clash check.
   - (to confirm), not in the files: album song videos as the main push; no lifestyle or no-caption posts (this conflicts with the weekly skill's lifestyle themes); no swear words; the "Out now on Apple Music" and Gabriela "coming soon" rules, with no Spotify or "everywhere"; Apple link on X/YT/FB/Reddit and "link in bio" on TikTok/IG.
   - Lyric timestamps: `python3 /workspace/jsw_research/lyric_ts/ts.py TRACK.wav` (faster-whisper). Confirm by ear.
4. **Engagement lists.** Accounts plus rule-checked subreddits only: small subs that allow new accounts and selfies, AI rule noted, rules screenshotted. Mark anything unverified. If no sub is verified, post to her own profile. The weekly run also refreshes reply banks.
5. **Notion saves.** Use notion-create-pages under Research (https://app.notion.com/p/400f29949b2981d298aadec6e2e7b235): "Daily Ideas — Day Mon DD, YYYY (revision)", with the format-mix table at the top. Append the midday and evening sections with notion-update-page insert_content. Weekly: "Weekly Content Research - Week of [date]".
6. **Sends.** Each model bot gets only her own slate. JSW AI gets the summary (example: summary_2026-10-22_for_JSW_AI.md). The weekly run also posts a summary in the JSW Operations room. The messaging tool name is (to confirm). Never post, and never message Samuel. Escalate only after 3 failed fixes.
7. **Rotation log.** Append a timestamped entry (focus, findings, sources, actions sent to whom) to the JSW Research Log (https://app.notion.com/p/401f29949b298126bdb8e9f792cd88b3) with insert_content at the end. Keep each run to 20-40 min of tool work.

**Failures and fixes:**
- Reddit blocks the box (verified). Models pull sub rules in their own signed-in AdsPower sessions (to confirm).
- Rotation runs can't message bots, so they hand send lines to the parent (to confirm).
- A billing failure stops a run; run a catch-up afterwards (to confirm).
- Never use Samuel's Mac for research (to confirm).
- Re-check live account state before writing a CTA (verified).
