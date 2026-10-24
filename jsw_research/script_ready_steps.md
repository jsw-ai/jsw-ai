## Script-ready steps (added Oct 22, 2026, 2 PM ET)
Sources: box skills jsw-daily-idea-slate, jsw-business-research-rotation, jsw-weekly-content-research, jsw-midday-trend-pulse, jsw-evening-performance-dig, plus the example outputs in /workspace/jsw_research/. **(to confirm)** means the source files did not back it up.

### Schedules
- Daily slate: 6 AM ET. The example run was the "6 AM revision" v2, made about 6-7 AM ET on 10/22. The routine cron itself is **(to confirm)**.
- Rotation: every 2 h, 8, 10, 12, 14, 16, 18, 20 and 22 ET. The routine picks the focus by hour; the exact hour-to-focus map is **(to confirm)**. The day's last run sends the top 1-3 business ideas to JSW AI.
- Midday trend pulse and evening performance dig: times **(to confirm)**.
- Weekly research: Sunday 7:30 PM ET, after the Tracker's 6 PM weekly report.

### 1. Tracker data pull
- Inputs: Tracker rankings page, Post Performance DB, Stats Dashboard, and the Tracker posts.json export. The 10/22 slate cites "posts.json refresh 4:14 AM ET" and "Stats Dashboard 4:15 AM ET". The box path of posts.json is **(to confirm)**.
- Tools: user-Notion `notion-search` / `notion-fetch` on the Tracker pages. user-Google-sheets if the dashboard lives in a sheet **(to confirm)**.
- Output: per model, winners and flops by hook, format, platform and time slot, plus medians. Example: YT median 444.5 vs TikTok 83; coffee 59; family comedy 6.5.
- Pass: real numbers only, each cited with its source and refresh time. Diagnose any per-post view drop (format, timing, hooks, volume). Fail: any invented or estimated figure that isn't marked.
- Evening dig: last 48-72 h per model, risers vs droppers, compared with 3-5 top niche accounts. Writes keep / kill / test / timing for the next slate.

### 2. Competitor and trend pulls (TikTok, IG, X, Reddit, YT Shorts)
- X (connector namespace `x`): `search_posts_all` (field `query`; since:YYYY-MM-DD in UTC), `get_posts_counts_recent` (last 7 days), `get_trends_by_woeid`, `search_news` (max_age_hours 1-720), `get_users_by_username` → `get_users_posts` (needs the numeric id), `get_posts_by_id(s)`. Use get_users_by_username for live bio and URL checks (example: Sienna's X url field empty).
- TikTok, IG and YT: WebSearch / WebFetch on public pages and trend sources. Example sources: Virlo trend report 10/22, newengen 10/14, Modash niche lists. Never use the TikTok web app for account status; check that in the mobile app.
- Reddit: script /workspace/jsw_research/sienna_subreddits/fetch.py (Playwright plus /usr/bin/google-chrome, headful). Run: `cd /workspace/jsw_research/sienna_subreddits && python3 fetch.py surf surfing beach ...`. It writes raw_SUB_rules.json and raw_SUB_about.json. **Known failure:** Reddit returns an HTML wall, not JSON (see raw_surf_rules.json), so no sub got rule-checked from the box.
- Output: about 10 fast-growing niche accounts per model, each with hook (first 1-2 s), format, sound, posting time, comment bait and a link.

### 3. Idea slate writing
- Output files: /workspace/jsw_research/daily_ideas_YYYY-MM-DD[_vN].md (full slate with the format-mix table and clash check) and /workspace/jsw_research/slates_YYYY-MM-DD/MODEL.md, one file each for valentina, sienna, charlotte, madison, gabriela and camille.
- Every idea lists: platform, format, hook line, sound, reference link, caption/CTA, posting slot and transition.
- Count: the skills size the slate to each model's full daily quota. The 10/22 v2 quota was X 5 · TikTok 3 · IG 1 Reel + 3 stories · YT 2 · FB 1 · Reddit 2. The weekly rules list X 3 · TikTok 2 · IG 1 · YT 1 · FB 1 · Reddit 1. The "5 ideas per model" minimum is **(to confirm)**.
- Pass rules (verified in the files):
  - At least 1 music-video and 1 comedy idea per model.
  - No format more than twice a day.
  - Same-platform videos at least 3 h apart.
  - One cut per platform; no identical file on two platforms.
  - TikTok sound from the commercial library. If it's unverified, mark it and fall back to her own track.
  - Every idea has a reference link.
  - No lip-sync, singing or talking-to-camera unless the model passed a face test (none on file). Comedy goes in on-screen text.
  - Face-gate-friendly framing: even front light, closed-mouth smile, 0.78 identity gate.
  - Never mention AI in captions.
  - No Fanvue in captions; Fanvue only for Sienna and Charlotte, and only in the X bio/pin and Reddit.
  - 3-5 niche hashtags on TikTok, no dating or red-flag tags.
  - Real events only.
  - Cross-model clash check: no shared hook, trend or transition on the same day.
- **(to confirm)**, not found in the source files:
  - Each model's own album song videos are the main push.
  - No lifestyle or no-caption posts. The weekly skill actually asks for aspirational lifestyle themes, so this conflicts and needs a ruling.
  - No swear words in captions.
  - "Out now on Apple Music" for Sienna, Charlotte, Madison, Valentina and Camille; Gabriela "coming soon"; no Spotify or "everywhere". Note: the rotation skill mentions Spotify/DistroKid promotion, and the 10/22 slate held off on "out now" for Sienna because HyperFollow showed "Available Soon".
  - Apple link in captions on X/YT/FB/Reddit; "link in bio" on TikTok/IG.

### 4. Engagement lists
- Per model: accounts to engage plus rule-checked subreddits, with anything unverified marked. Weekly runs also refresh comment and reply banks per platform and add first-hour reply lines.
- Pass: only small subs that allow new accounts and selfies, with each sub's AI rule noted and its rules screenshotted. No karma plans. If no sub is verified, Reddit goes to her own profile (as in the 10/22 slate).

### 5. Notion saves
- Tool: user-Notion `notion-create-pages` under Research (https://app.notion.com/p/400f29949b2981d298aadec6e2e7b235). Daily page title format: "Daily Ideas — Day Mon DD, YYYY (revision)". Example: https://app.notion.com/p/401f29949b29818dba41c913e621f4a1
- Daily page: format-mix table at the top, plus the reasons for any shift. The midday pulse and the evening "Performance dig" are appended to that day's page with `notion-update-page` insert_content.
- Weekly: "Weekly Content Research - Week of [date]", with one page per model and a link to this process page.

### 6. Sending lists to model bots and JSW AI
- Each model bot gets only her own slate or swaps. JSW AI gets the summary (example: /workspace/jsw_research/summary_2026-10-22_for_JSW_AI.md, covering winners, kills, fixes and blockers). Weekly runs also post a short summary in the JSW Operations room.
- The bot-to-bot messaging tool name is **(to confirm)**.
- Never post anything. Never message Samuel directly. Escalate to JSW AI only after 3 real fixes have failed.

### 7. Rotation logging (every 2 h)
- Append a dated, timestamped entry to the JSW Research Log (https://app.notion.com/p/401f29949b298126bdb8e9f792cd88b3) with `notion-update-page` command insert_content, position end. Each entry covers: focus, findings, sources, and actions sent to whom.
- Keep each run to 20-40 minutes of tool work. Skip sends that have nothing actionable. Performance-dig findings also go into the next morning's slate.

### Other scripts on the box
- /workspace/jsw_research/lyric_ts/ts.py and ts2.py use faster-whisper "small" on CPU to find lyric timestamps for music-video ideas. Run: `python3 ts.py /workspace/music/distrokid/sienna/09_flight_to_bali.wav`. It writes FILE.json. Confirm the timestamps by ear.

### Common failures and fixes
- Reddit blocks unsigned fetches from the box (verified: HTML wall). Fix: models pull sub rules in their own signed-in AdsPower sessions **(the process is to confirm)**.
- Rotation runs can't message bots, so they hand their send lines to the parent **(to confirm)**.
- A billing failure stops a run; run a catch-up afterwards **(to confirm)**.
- Never use Samuel's Mac for research **(to confirm; the box is the research machine)**.
- Account states change often (suspended, logged out, no bio URL). Re-check live before writing a CTA (verified in the 10/22 slate).
