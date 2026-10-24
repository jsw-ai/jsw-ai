> **SUPERSEDED 2026-10-12 by `sienna_week1.md`.** Wrong vs SOP: stills only (TikTok/IG need trend-aligned video/Reels), IG 2 feed/day (SOP: 1 feed/day + daily Stories), daily Reddit profile posts (SOP: 2-4 value-first posts/week in relevant subs), lingerie on IG. Do not queue anything from this file.

# Sienna Blake — Batch 1 (READY TO POST, NOT SCHEDULED)
Prepared 2026-10-12 11:30 PM ET. Status: **not posted / not scheduled** — see Blocker.
Scope: Sienna only. IG siennablake0320 · TikTok "Sienna Blake" · Reddit u/TheSiennaBlake (own profile only). No X (not linked). No Fanvue teasers/links in captions on IG/TikTok. No video. Lingerie: 1 IG post only (non-sheer v4_2); none on TikTok/Reddit.

## How the hub actually posts (from /workspace/jsw-ai/org source)
1. Create a row in `content_items` via `POST /org/api/post/create` {slug:"sienna", category, idx (library photo index on the droplet), platform, caption, hashtags, slot_time "YYYY-MM-DDTHH:MM" droplet-local}. Needs logged-in session (`@require`).
2. Approve it on /org/approvals (status must be `approved`).
3. `ayr_poster.py` tick: only runs if settings `go_live`='1' (toggle via `POST /org/api/golive` {on:true}); then for every approved row with slot_time <= now it uploads media to Ayrshare and calls `POST /api/post` immediately (no Ayrshare scheduleDate — scheduling = slot_time in the hub DB). Sienna → no Profile-Key (Primary Profile).

## Blocker (why nothing was posted)
- Hub is behind /org/login (admin user + password). No credentials are on the box and the Ayrshare key is server-only, so the box cannot create/approve posts or flip go_live. I did not try to get around this.
- **go_live is GLOBAL, not per-model.** Turning it on publishes EVERY approved+due item for ALL personas. Before flipping, check /org/approvals and make sure no other model has approved items with past/near slot_times (or set them back to draft).
- **Reddit will fail as coded:** ayr_poster sends no `redditOptions` (Ayrshare needs `title` + `subreddit`; for her own profile use subreddit `u_TheSiennaBlake`). Needs a code patch or post Reddit by hand.
- **TikTok AI label:** ayr_poster sends no `tikTokOptions` (Ayrshare supports `isAIGenerated: true`; image posts also want `tikTokOptions.autoAddMusic`/title). Patch needed, or post by hand with the AI-generated content toggle on.
- Images must be in the hub library for Sienna (idx); upload these files via Studio/photo upload first.

## Batch (times ET; droplet slot_time = same if droplet TZ is ET — check)
| # | When (ET) | Platform | Image (box path) | Caption | Hashtags |
|---|---|---|---|---|---|
| 1 | Tue Oct 13 9:00 AM | Instagram | /workspace/hf-test/keepers/sienna_bikini1.png | Dawn patrol done, salt still in me hair. Water was glassy this morning, absolute cracker of a start 🌊 | #goldcoast #beachgirl #surfergirl #aussiegirl #saltwater #aidisclosed |
| 2 | Tue Oct 13 7:30 PM | Instagram | /workspace/hf-test/sienna_cafe_face.png | Ranked another café today. Matcha 8/10, vibes 10/10, lost me sunnies twice ☕ | #sydneycafes #matcha #aussiegirl #coffeeaddict #aidisclosed |
| 3 | Tue Oct 13 6:00 PM | TikTok (photo, AI label ON) | /workspace/hf-test/keepers/sienna_cover.png | pov: you said "quick swim" and it's now 4pm 😅🌴 | #goldcoast #aussie #beachday #fyp #aigenerated |
| 4 | Tue Oct 13 12:00 PM | Reddit u/TheSiennaBlake (profile) | /workspace/hf-test/keepers/sienna_bikini2.png | Title: "Pool day on the Goldie — how's your arvo going?" Body: "Too hot for the beach crowds so pool it is ☀️ (AI creator)" | — |
| 5 | Wed Oct 14 8:30 AM | Instagram | /workspace/hf-test/sienna_candid.png | Errand run, no makeup, no shoes if I could get away with it. Sydney you're lucky I like you 🤍 | #sydneylife #aussiegirl #nomakeup #everydaystyle #aidisclosed |
| 6 | Wed Oct 14 8:00 PM | Instagram | /workspace/hf-test/zen/sienna_lingerie_v4_2.png | Golden hour, cosy sheets, phone on do-not-disturb. Big week, little nap 💜 | #cozynight #goldenhour #aussiegirl #aidisclosed |
| 7 | Wed Oct 14 6:30 PM | TikTok (photo, AI label ON) | /workspace/hf-test/sienna_volleyball.png | beach volleyball rules: i'm on the team, i'm not catching anything 🏐🤣 | #beachvolleyball #goldcoast #aussiegirl #fyp #aigenerated |
| 8 | Wed Oct 14 12:30 PM | Reddit u/TheSiennaBlake (profile) | /workspace/hf-test/sienna_cowboy.png | Title: "Coffee run in Bondi, rate the fit 1–10" Body: "Singlet + denim shorts, the Aussie uniform 😂 (AI creator)" | — |
| 9 | Thu Oct 15 9:00 AM | Instagram | /workspace/hf-test/keepers/sienna_bikini2.png | Pool's warmer than the ocean today and I'm not complaining. Who's coming for a dip? ☀️ | #poolday #goldcoast #bikiniseason #aussiegirl #aidisclosed |
| 10 | Thu Oct 15 7:30 PM | Instagram | /workspace/hf-test/sienna_full.png | Hot take: Gold Coast > Bondi and I'll die on this hill. Fight me in the comments 🌊 | #goldcoast #bondi #aussiegirl #hottake #aidisclosed |
| 11 | Thu Oct 15 6:00 PM | TikTok (photo, AI label ON) | /workspace/hf-test/sienna_candid.png | things i've lost this week: keys, sunnies, phone (twice). things i've found: a new café 🫶 | #aussie #sydney #chaoticgirl #fyp #aigenerated |
| 12 | Thu Oct 15 12:00 PM | Reddit u/TheSiennaBlake (profile) | /workspace/hf-test/keepers/sienna_bikini1.png | Title: "Sunrise surf then brekkie — perfect Thursday?" Body: "Gold Coast mornings never get old 🌅 (AI creator)" | — |

Excluded on purpose: sienna_lingerie_v4_1/3/4 (v4_3 sheer robe, v4_4 sheer babydoll, v4_1 posed on bed — keep for Fanvue/X); sienna_face_close (has UI chrome); all Fanvue/undress assets; all video.
Note: voice docs are bios.json (Gold Coast born, Sydney based, dog **Bruce** in bio but **Remi** in content_themes — inconsistent; I avoided naming the dog). The voices/ folder holds only mp3s.
