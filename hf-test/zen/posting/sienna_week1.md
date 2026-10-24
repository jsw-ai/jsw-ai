# Sienna Blake — Week 1 Content Plan (DRY WEEK, for Sam approval)
Prepared Mon Oct 12 2026 ~11:30 PM ET. Replaces `sienna_batch1.md` (superseded).
> **HARD RULE (Sam, Oct 13): never mention AI anywhere in post content** — no AI words in captions, hashtags (#aigenerated #aiinfluencer #aigirl etc.), on-screen hook text, spoken lines, Reddit titles/bodies, X posts or Stories. **Platform AI-content toggles (TikTok AI-generated label, IG "AI info" label) stay ON as account/post SETTINGS only** — that is the only disclosure; it is never written into the post itself.

Status: **PLAN ONLY — nothing generated, no credits spent, nothing queued or posted. `go_live` stays OFF** until Sam approves this week (AUTOMATION_PLAN rule).

## Rules applied (sources: `/workspace/jsw-ai/org/sops.py`, `AUTOMATION_PLAN.md`)
- **TikTok:** 1-2 trend-aligned short videos/day, trending sounds, hook in first 1-2s, AI-generated toggle ON (setting only).
- **Instagram:** 1 feed post/day (Reels prioritized) + daily Stories. "AI info" label ON (setting only).
- **Reddit:** 2-4 value-first posts/week in relevant subs, follow each sub's rules, never overtly promotional, no NSFW.
- **X:** 3-5 posts/day + replies (drafted below; X not linked yet → hold). X may be cheekier (bikini/lingerie stills OK, **no nudity**).
- **YouTube Shorts 3-5/wk, Facebook ~1/day:** in SOP but no accounts connected → noted only; reuse TikTok cuts when linked.
- **Global:** platform AI toggles/labels ON as settings (no AI text in posts); consistent voice + ongoing story; post at audience peak times; human-like engagement (no mass follow/like); compete only via better content, never coordinated boosting between personas.
- **SFW lane = stills + Higgsfield talking/lip-sync clips.** No Fanvue links/teasers/nudes on TikTok/IG/Reddit/YT/FB. No lingerie on SFW lanes (beach swimwear is fine, keep it classy).
- **Store (Gold Coast Babe): NOT promoted this week.** Later affiliate ratio ~1 in 4 posts, with "#ad I earn from links." (disclosure via platform label setting; no AI wording in post).
- Monetize CTA this week: none hard. Soft "follow for more Goldie mornings" only.

## Persona voice
Aussie (Gold Coast born, Sydney/Bondi based), sunny, chaotic-funny, self-deprecating, slang ("arvo", "brekkie", "heaps", "reckon", "Goldie", "no worries", "sunnies", "togs"). Running story arc for week 1: **"Goldie vs Bondi" week** — she's back on the Gold Coast for a week visiting home, comparing it to Bondi life, with a recurring café-ranking bit and "things I lost today" bit.
Open issue: dog name is **Bruce** (bios.json) vs **Remi** (content_themes) — don't name the dog until Sam picks.

## Timing (ET → AEDT is +15h)
Primary windows: **7:00-8:30 PM ET** (= 10-11:30 AM AEDT next day, AU morning scroll + US evening) and **12:00 PM ET** (US lunch). Stories spread through the day.

## Existing asset inventory
### Video
| File | Len | Content | SFW use? |
|---|---|---|---|
| `/workspace/hf-test/videos/sienna_talking1_web.mp4` (also `sienna_talking1.mp4`) | 8.1s, audio | Sienna solo, braids, grey bikini top, palm beach, talking to camera | **YES** — TikTok/IG/X. Audio line unknown (no transcriber on box) → Sam/agent must listen + confirm the line before captioning. |
| `/workspace/hf-test/videos/collab_sienna_camille_v2.mp4` (+ `_web`, v1 `collab_sienna_camille.mp4`) | 8.1s, audio | Sienna + Camille, swimwear, pool/palms, talking | **YES (collab)** — use v2. Needs Camille account tag/consent of that persona's agent; don't use as coordinated boosting (one organic collab is fine). |
| `/workspace/hf-test/zen/sienna_camille_collab_v1.mp4`, `sienna_camille_collab_seedance_v1.mp4` | 5s | Sienna + Camille on bed, sheer robe/lingerie | **NO SFW.** X-only at most (no nudity) or Fanvue lane. |
| Other *.mp4 in `/workspace` + `~/Downloads` (hf_2026082x…, miami_*, camille/gabriela/etc.) | — | other personas / Miami / unrelated | Not Sienna → not used. |

### Stills (SFW-usable)
`keepers/sienna_bikini1.png`, `keepers/sienna_bikini2.png`, `keepers/sienna_cover.png`, `keepers/sienna_face_keeper.png`, `sienna_cafe_face.png`, `sienna_candid.png`, `sienna_volleyball.png`, `sienna_full.png`, `sienna_cowboy.png`, `sienna_1.png`, `sienna_2.png`, `sienna_cover.png` (all under `/workspace/hf-test/`). Excluded: `sienna_face_close.png` (UI chrome), all `zen/sienna_lingerie_*` (X/Fanvue only), Fanvue/editor screenshots.
Voice ref: `/workspace/hf-test/voicerefs-from-sam/sienna.mp3` (use for lip-sync voice).

## Clips to generate (Higgsfield talking-head / lip-sync) — NOT generated yet
Engine: Higgsfield talking head (`generate_talking_head` / lip-sync app), source still listed, voice = Sienna voice from `sienna.mp3`, Aussie accent, 9:16, 6-12s. Visual prompt base for all: *"Vertical 9:16 selfie-style talking video, natural iPhone front camera, slight handheld sway, real skin texture, natural daylight, relaxed Australian beach-girl energy, speaks directly to camera with expressive eyebrows and a laugh at the end, no text overlays."*

| ID | Source still | Scene add-on | Exact line (voice) |
|---|---|---|---|
| C1 | keepers/sienna_cover.png | windy beach, hair moving | "G'day, I'm Sienna. Gold Coast girl, back home for a week. Stick around, I'll show you the best bits of the Goldie." |
| C2 | sienna_cafe_face.png | café table, iced matcha | "Café ranking, day one. Matcha: eight out of ten. The barista called me 'mate' twice. Ten out of ten. We're off to a cracker start." |
| C3 | keepers/sienna_bikini1.png | sunrise surf beach, wet hair | "Five-thirty a.m., dawn patrol. Water's glassy, I'm freezing, and I would not trade this for anything. Who's actually up this early?" |
| C4 | sienna_candid.png | car / street, sunnies on head | "Things I've lost today: my keys, my sunnies, which are on my head, and my dignity at the servo. Things I've found: a sausage roll." |
| C5 | sienna_full.png | boardwalk | "Gold Coast or Bondi. I'll go first. Bondi has the coffee, Goldie has the waves and the parking. Comment your pick, and be honest." |
| C6 | sienna_volleyball.png | beach volleyball net | "Beach volleyball rules: I'm on the team, I'm not catching anything, and I'm definitely the one yelling 'mine' and then ducking." |
| C7 | keepers/sienna_face_keeper.png | sunset, golden light | "Aussie slang test. If you know what 'arvo', 'togs' and 'servo' mean, you're basically one of us. Wrong answers only in the comments." |
| C8 | keepers/sienna_bikini2.png | pool, sunnies | "Too hot for the beach crowds, so pool day it is. Tell me where you're watching from, I want to see how far this goes." |
| C9 | sienna_2.png | sunset beach walk | "One week back home on the Goldie. Best café, best swim, best sunset. Tell me what I should do next week." |

Lip-sync clips needed: **9 new** (C1-C9). Plus 2 existing clips reused, 1 stills slideshow (Sun) and 1 no-credit re-edit of C2 (Mon) = 13 TikTok slots.
**Credits (checked Oct 13, preflight only, nothing spent):** balance 3,000 cr (Ultra). Engine used for earlier Sienna talking clips = `seedance_2_0` (video_recipe.json; voice via audio_references). 9:16 720p with audio: **8s = 36 cr, 10s = 45 cr** (4.5 cr/s). 9 clips × 8s = 324 cr; with ~30% reroll buffer ≈ 420 cr. Older note follows: Before generating: run Higgsfield `balance` and the model cost/quote tool for the chosen talking-head engine, multiply × 9 (plus ~30% buffer for 2-3 rerolls on face/lip realism). Do not auto-buy packs (AUTOMATION_PLAN). Sam to approve spend.

## 7-day calendar (Tue Oct 13 – Mon Oct 19 ET)
All TikToks: AI-generated content toggle ON (setting only, no AI hashtag/text); trending sound picked same-day from TikTok Creative Center (style given; voice track kept at full, sound underneath at ~15%). Every IG Reel = same clip re-exported (no TikTok watermark), AI label ON as a setting only.

### Tue Oct 13
- **TikTok 1 — 12:00 PM** · Intro. Clip: **existing `sienna_talking1_web.mp4`** (confirm audio line first). Hook (on-screen text, 0-1s): "POV: you meet the Gold Coast girl 🌊". Sound: upbeat summer/beach trending audio. Caption: "g'day, i'm Sienna 👋 Goldie girl, back home for a week. Goldie week starts now 🌴" · #goldcoast #aussie #beachgirl #australia #fyp
- **TikTok 2 — 7:30 PM** · **C1** "G'day, I'm Sienna…". Hook text: "back on the Goldie for a week. no I won't stop saying 'arvo'". Sound: trending "storytime/intro" voiceover-friendly beat. Caption: "Gold Coast tour starts tomorrow, who's coming 🌊" · #goldcoast #australia #goldcoastlife #fyp
- **IG feed 7:00 PM — Reel:** C1. Caption: "G'day 👋 I'm Sienna — Goldie girl, professional sunnies-loser. Come along this week while I'm back home on the Gold Coast 🌴" · #goldcoast #aussiegirl #beachlife #queensland #goldcoastlife
- **Stories:** (1) sienna_cover still + poll "Gold Coast 🌊 or Bondi 🏙️?" (2) "Back home for a week ✈️" text over sienna_2.png (3) question box "What should I do on the Goldie?"
- **Reddit 1 — 1:00 PM · u/TheSiennaBlake (own profile post)** · Image: keepers/sienna_cover.png (classy beach). Title: "Gold Coast morning, back home for a week 🌊". Body: "G'day! Back on the Goldie for a week visiting home. Tell me your fave beach up here, I'm making a list." No links. Risk: low (own profile; Reddit's own rules apply only). Grow karma by genuine comments, not subreddit posting.
- **X (hold):** 3 posts — "g'day from the Goldie 🌴 back home for a week" + cover still · "hot take: sunnies are a personality" · reply-bait "what's your go-to beach snack?"

### Wed Oct 14
- **TikTok 1 — 7:00 AM** · **C3** dawn patrol. Hook text: "5:30am on the Gold Coast hits different". Sound: chill lo-fi/sunrise trend. Caption: "dawn patrol > sleep in. fight me 🌅" · #dawnpatrol #goldcoast #surfergirl #fyp
- **TikTok 2 — 7:30 PM** · **C2** café ranking ep.1. Hook text: "rating Gold Coast cafés until someone stops me ☕". Sound: trending "rating/review" sound. Caption: "café ranking ep. 1 — drop the next one 👇" · #goldcoastcafe #matcha #aussie #fyp
- **IG feed 7:00 PM — Reel:** C3. Caption: "Dawn patrol done, salt still in me hair. Glassy and freezing — perfect 🌊" · #goldcoast #surfergirl #sunrise #aussiegirl
- **Stories:** C2 café clip 15s cut + emoji slider "how good is matcha?"; "lost my sunnies again" text story; repost TikTok link sticker.
- **X (hold):** "café ranking ep.1: matcha 8/10, barista 10/10" · bikini1 still "dawn patrol 🌅" · reply to 2-3 Aussie/beach threads.

### Thu Oct 15
- **TikTok 1 — 12:00 PM** · **C4** "things I lost today". Hook text: "things i've lost today (it's 11am)". Sound: trending comedic/chaotic sound. Caption: "the sunnies were on my head the whole time 🫠" · #chaoticgirl #aussie #relatable #fyp
- **TikTok 2 — 7:30 PM** · **C5** Goldie vs Bondi debate. Hook text: "Gold Coast vs Bondi — settle it". Sound: trending "debate/this or that" beat. Caption: "comment your side, I'm keeping score 🌊🏙️" · #goldcoast #bondi #sydney #australia #fyp
- **IG feed 7:00 PM — Reel:** C5. Caption: "Gold Coast or Bondi? I'm keeping a tally in the comments 👇" · #goldcoast #bondibeach #australia #aussiegirl
- **Stories:** quiz sticker "What's a 'servo'?"; tally update screenshot; candid still sienna_candid.png.
- **Reddit 2 — 2:00 PM · u/TheSiennaBlake (own profile post)** · Image: sienna_volleyball.png. Title: "Beach volleyball rules: yell 'mine', then duck 🏐". Body: "Arvo hit on the sand. I'm still the team liability. Anyone else play?" Risk: low.
- **X (hold):** "Goldie vs Bondi, go" poll · C4 clip · "things i've lost today: keys, sunnies, dignity".

### Fri Oct 16
- **TikTok 1 — 12:00 PM** · **C6** volleyball rules. Hook text: "beach volleyball rules if you're me 🏐". Sound: trending sports/funny-fail sound. Caption: "I yelled 'mine' and ducked. team player 🤝" · #beachvolleyball #goldcoast #funny #fyp
- **TikTok 2 — 7:30 PM** · **existing `collab_sienna_camille_v2.mp4`** — collab. Hook text: "when your bestie visits the Goldie". Sound: trending "bestie/duo" sound. Caption: "pool day with @[Camille handle] ☀️ " · #besties #poolday #goldcoast #fyp. Note: tag only if Camille account live; one organic collab, no engagement-swapping.
- **IG feed 7:00 PM — Reel:** collab_sienna_camille_v2 (Collab post with Camille if her IG exists). Caption: "Pool day with my girl 💛 " · #poolday #besties #goldcoast
- **Stories:** volleyball clip cut; "this or that" stickers (sunrise/sunset, beach/pool); behind-the-scenes text "Friday arvo plans?"
- **Reddit 3 — 1:00 PM · u/TheSiennaBlake (own profile post)** · Image: sienna_full.png. Title: "Boardwalk walk before the arvo heat ☀️". Body: "Gold Coast or Bondi, which one's got the better boardwalk? Be honest." Risk: low.
- **X (hold):** collab clip · bikini2 "pool > ocean today" · reply to mentions.

### Sat Oct 17
- **TikTok 1 — 11:00 AM** · **C7** Aussie slang test. Hook text: "only Aussies will pass this test 🇦🇺". Sound: trending quiz/"wrong answers only" sound. Caption: "wrong answers only 👇" · #aussieslang #australia #learnenglish #fyp
- **TikTok 2 — 8:00 PM** · **C8** where are you watching from. Hook text: "how far does this video go? 🌍". Sound: trending travel/map sound. Caption: "drop your city, I'm reading all of them ☀️" · #poolday #goldcoast #whereareyoufrom #fyp
- **IG feed 7:30 PM — Reel:** C7. Caption: "Aussie slang test 🇦🇺 arvo, togs, servo — how'd you go?" · #aussieslang #australia #aussiegirl
- **Stories:** slang quiz stickers (one word per frame); reply-to-comments Story; sunset still.
- **X (hold):** slang quiz post · "drop your city" · cheeky bikini still (keepers/sienna_bikini2) — X lane OK.

### Sun Oct 18
- **TikTok 1 — 12:00 PM** · **Photo-mode slideshow** (stills: sienna_cover, bikini1, cafe_face, volleyball, full, sienna_2) "my Goldie week in 6 pics". Sound: trending photo-dump sound. Caption: "goldie week recap 🌴 which one's your fav?" · #photodump #goldcoast #aussie #fyp
- **TikTok 2 — 7:30 PM** · **C9** "one week back home" recap/next week ask. Hook text: "my week on the Goldie in 10 seconds". Sound: trending emotional/"week recap" sound. Caption: "tell me where I go next 👇" · #goldcoast #australia #weekrecap #fyp
- **IG feed 7:00 PM — Carousel** (feed variety): same 6 stills. Caption: "Goldie week recap 🌴 Swipe and pick a fav. Back to Bondi soon" · #goldcoast #photodump #aussiegirl
- **Stories:** C9 clip; "Bondi next week?" poll; thank-you Story to commenters (non-spammy).
- **X (hold):** recap thread (3 tweets, one still each) · C9 clip.

### Mon Oct 19
- **TikTok 1 — 7:30 PM** · Re-edit of C2 café ranking with new on-screen overlay "café ranking ep.2 — your picks" (no new credits; reuse) OR skip if performance says 1/day. Sound: same trending review sound. Caption: "you voted, I went ☕" · #goldcoastcafe #aussie #fyp (1 TikTok today)
- **IG feed 7:00 PM — Reel:** C9. Caption: "One week back home. Best café, best swim, best sunset 🌅 Where next?" · #goldcoast #australia #aussiegirl
- **Stories:** Q&A box "ask me anything"; next week teaser "Bondi arc 🏙️"; café still.
- **Reddit:** none (3 this week = within 2-4).
- **X (hold):** "monday mood" · AMA prompt · reply to mentions.

## Counts
| Platform | Week 1 |
|---|---|
| TikTok | 13 videos/posts (Tue-Sun 2/day, Mon 1): 9 new lip-sync, 2 existing clips, 1 photo slideshow, 1 re-edit |
| Instagram | 7 feed (6 Reels + 1 carousel) + 7 days Stories (~3 frames/day) |
| Reddit | 3 posts, all on own profile u/TheSiennaBlake (no subreddit posts) |
| X | ~21 drafted (3/day, below 3-5 SOP until linked; add replies) — HOLD, not linked |
| YouTube Shorts / Facebook | 0 — no accounts; reuse Reels 3-5/wk when linked |

## Subreddits (re-checked via web Oct 13, after no-AI-mention rule)
- **Dropped r/StunningAIGirls and r/aiArt** — both are AI-only communities (StunningAIGirls requires AI-generated women; aiArt is an AI-art sub with tool flair). Posting there signals AI by itself, which breaks the no-AI rule.
- **Real-people SFW subs (model/beach/outfit/selfie, e.g. r/beach, r/OUTFITS, r/selfie, r/GoldCoast, r/sydney): NOT recommended.** Many explicitly ban AI images (a 2026 rules index found 813 of 3,765 subs with an AI-content removal rule, e.g. r/BeAmazed, r/backpacking, r/AsianBeauty). Even where no rule is written, posting a generated person in a "real people" sub without saying so breaks the sub's intent. Reddit users and mods actively call these posts out (see r/Instagramreality thread, Sep 2026, on generated "outfit" posters), which leads to removals, bans, and account-level suspicion. Reddit's content policy also bans impersonation and misleading content. **Risk: HIGH** for the account and the brand. I couldn't find a sub that welcomes original photo posts of a generated model without an AI label.
- **Chosen: profile posts on u/TheSiennaBlake only** (posts to u/ profile, no sub rules apply, AI never mentioned). Reach is low at first, so build karma with genuine comments in Aussie/beach subs (no image posts, no links). Re-evaluate if Sam picks a sub after reading its sidebar himself.

## Blockers before go_live (carried from batch1 audit)
- Hub `/org` needs login; `go_live` is GLOBAL (flips all personas' approved items) — clear others' approved queue first.
- `ayr_poster.py` sends no `redditOptions` (title/subreddit) and no `tikTokOptions.isAIGenerated` → patch or post by hand.
- Sienna Ayrshare profile key was missing in the Sep 5 inventory — verify.
- Confirm audio line in `sienna_talking1_web.mp4`; confirm Camille has a live account before the collab tag.
- Dog name (Bruce vs Remi) unresolved.
