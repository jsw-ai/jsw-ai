# Sienna Blake — Week 1 Content Plan (DRY WEEK, for Sam approval)
Prepared Mon Oct 12 2026 ~11:30 PM ET. Replaces `sienna_batch1.md` (superseded).
Status: **PLAN ONLY — nothing generated, no credits spent, nothing queued or posted. `go_live` stays OFF** until Sam approves this week (AUTOMATION_PLAN rule).

## Rules applied (sources: `/workspace/jsw-ai/org/sops.py`, `AUTOMATION_PLAN.md`)
- **TikTok:** 1-2 trend-aligned short videos/day, trending sounds, hook in first 1-2s, AI-generated label ON.
- **Instagram:** 1 feed post/day (Reels prioritized) + daily Stories. AI label ("Made with AI") ON.
- **Reddit:** 2-4 value-first posts/week in relevant subs, follow each sub's rules, never overtly promotional, no NSFW.
- **X:** 3-5 posts/day + replies (drafted below; X not linked yet → hold). X may be cheekier (bikini/lingerie stills OK, **no nudity**).
- **YouTube Shorts 3-5/wk, Facebook ~1/day:** in SOP but no accounts connected → noted only; reuse TikTok cuts when linked.
- **Global:** AI disclosed on every profile; consistent voice + ongoing story; post at audience peak times; human-like engagement (no mass follow/like); compete only via better content, never coordinated boosting between personas.
- **SFW lane = stills + Higgsfield talking/lip-sync clips.** No Fanvue links/teasers/nudes on TikTok/IG/Reddit/YT/FB. No lingerie on SFW lanes (beach swimwear is fine, keep it classy).
- **Store (Gold Coast Babe): NOT promoted this week.** Later affiliate ratio ~1 in 4 posts, with "#ad I earn from links. Sienna is an AI character."
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
| C1 | keepers/sienna_cover.png | windy beach, hair moving | "Right, so apparently I'm an AI. Still a Gold Coast girl though. Stick around, I'll show you the best bits of the Goldie." |
| C2 | sienna_cafe_face.png | café table, iced matcha | "Café ranking, day one. Matcha: eight out of ten. The barista called me 'mate' twice. Ten out of ten. We're off to a cracker start." |
| C3 | keepers/sienna_bikini1.png | sunrise surf beach, wet hair | "Five-thirty a.m., dawn patrol. Water's glassy, I'm freezing, and I would not trade this for anything. Who's actually up this early?" |
| C4 | sienna_candid.png | car / street, sunnies on head | "Things I've lost today: my keys, my sunnies, which are on my head, and my dignity at the servo. Things I've found: a sausage roll." |
| C5 | sienna_full.png | boardwalk | "Gold Coast or Bondi. I'll go first. Bondi has the coffee, Goldie has the waves and the parking. Comment your pick, and be honest." |
| C6 | sienna_volleyball.png | beach volleyball net | "Beach volleyball rules: I'm on the team, I'm not catching anything, and I'm definitely the one yelling 'mine' and then ducking." |
| C7 | keepers/sienna_face_keeper.png | sunset, golden light | "Aussie slang test. If you know what 'arvo', 'togs' and 'servo' mean, you're basically one of us. Wrong answers only in the comments." |
| C8 | keepers/sienna_bikini2.png | pool, sunnies | "Too hot for the beach crowds, so pool day it is. Tell me where you're watching from, I want to see how far this goes." |
| C9 | sienna_2.png | sunset beach walk | "One week back home on the Goldie. Best café, best swim, best sunset. Tell me what I should do next week." |

Lip-sync clips needed: **9 new** (C1-C9). Plus 2 existing clips reused, 1 stills slideshow (Sun) and 1 no-credit re-edit of C2 (Mon) = 13 TikTok slots.
**Credits:** no per-clip cost recorded on the box for Higgsfield talking-head. Before generating: run Higgsfield `balance` and the model cost/quote tool for the chosen talking-head engine, multiply × 9 (plus ~30% buffer for 2-3 rerolls on face/lip realism). Do not auto-buy packs (AUTOMATION_PLAN). Sam to approve spend.

## 7-day calendar (Tue Oct 13 – Mon Oct 19 ET)
All TikToks: AI-generated content toggle ON + `#aigenerated`; trending sound picked same-day from TikTok Creative Center (style given; voice track kept at full, sound underneath at ~15%). Every IG Reel = same clip re-exported (no TikTok watermark), "Made with AI" label ON.

### Tue Oct 13
- **TikTok 1 — 12:00 PM** · Intro. Clip: **existing `sienna_talking1_web.mp4`** (confirm audio line first). Hook (on-screen text, 0-1s): "POV: the Gold Coast girl is AI 🤖🌊". Sound: upbeat summer/beach trending audio. Caption: "g'day, i'm Sienna 👋 AI creator, real Aussie energy. Goldie week starts now 🌴" · #goldcoast #aussie #beachgirl #aiinfluencer #fyp #aigenerated
- **TikTok 2 — 7:30 PM** · **C1** "Right, so apparently I'm an AI…". Hook text: "yes I'm AI. no I won't stop saying 'arvo'". Sound: trending "storytime/intro" voiceover-friendly beat. Caption: "Gold Coast tour starts tomorrow, who's coming 🌊" · #goldcoast #australia #aigirl #fyp #aigenerated
- **IG feed 7:00 PM — Reel:** C1. Caption: "G'day 👋 I'm Sienna — AI creator, Goldie girl, professional sunnies-loser. Following me this week while I'm back home on the Gold Coast 🌴 (AI-generated)" · #goldcoast #aussiegirl #beachlife #aiinfluencer #madewithai
- **Stories:** (1) sienna_cover still + poll "Gold Coast 🌊 or Bondi 🏙️?" (2) "Back home for a week ✈️" text over sienna_2.png (3) question box "What should I do on the Goldie?"
- **Reddit 1 — 1:00 PM · r/StunningAIGirls** · Image: keepers/sienna_cover.png (classy beach). Title: "[Realistic] Sienna — Gold Coast beach morning". Body: "Original AI character I've been building — Australian beach girl. Made with Higgsfield. Feedback on realism welcome, especially skin/light." No links. Flair per sub. Risk: low-med (sub is SFW, swimwear OK; ban for reposts/real-person likeness — she's original).
- **X (hold):** 3 posts — "g'day from the Goldie 🌴 (AI, obviously)" + cover still · "hot take: sunnies are a personality" · reply-bait "what's your go-to beach snack?"

### Wed Oct 14
- **TikTok 1 — 7:00 AM** · **C3** dawn patrol. Hook text: "5:30am on the Gold Coast hits different". Sound: chill lo-fi/sunrise trend. Caption: "dawn patrol > sleep in. fight me 🌅" · #dawnpatrol #goldcoast #surfergirl #fyp #aigenerated
- **TikTok 2 — 7:30 PM** · **C2** café ranking ep.1. Hook text: "rating Gold Coast cafés until someone stops me ☕". Sound: trending "rating/review" sound. Caption: "café ranking ep. 1 — drop the next one 👇" · #goldcoastcafe #matcha #aussie #fyp #aigenerated
- **IG feed 7:00 PM — Reel:** C3. Caption: "Dawn patrol done, salt still in me hair. Glassy and freezing — perfect 🌊 (AI-generated)" · #goldcoast #surfergirl #sunrise #aussiegirl #madewithai
- **Stories:** C2 café clip 15s cut + emoji slider "how good is matcha?"; "lost my sunnies again" text story; repost TikTok link sticker.
- **X (hold):** "café ranking ep.1: matcha 8/10, barista 10/10" · bikini1 still "dawn patrol 🌅" · reply to 2-3 Aussie/beach threads.

### Thu Oct 15
- **TikTok 1 — 12:00 PM** · **C4** "things I lost today". Hook text: "things i've lost today (it's 11am)". Sound: trending comedic/chaotic sound. Caption: "the sunnies were on my head the whole time 🫠" · #chaoticgirl #aussie #relatable #fyp #aigenerated
- **TikTok 2 — 7:30 PM** · **C5** Goldie vs Bondi debate. Hook text: "Gold Coast vs Bondi — settle it". Sound: trending "debate/this or that" beat. Caption: "comment your side, I'm keeping score 🌊🏙️" · #goldcoast #bondi #sydney #australia #fyp #aigenerated
- **IG feed 7:00 PM — Reel:** C5. Caption: "Gold Coast or Bondi? I'm keeping a tally in the comments 👇 (AI-generated)" · #goldcoast #bondibeach #australia #aussiegirl #madewithai
- **Stories:** quiz sticker "What's a 'servo'?"; tally update screenshot; candid still sienna_candid.png.
- **Reddit 2 — 2:00 PM · r/aiArt** (ONE post only this week — sub bans repeated same-model posts since Aug 26 2026). Image: sienna_volleyball.png (varied scene). Flair: "Image-Other" naming Higgsfield. Title: "Beach volleyball on the Gold Coast — photoreal character test". Body: 2-3 lines of genuine process (consistent character across scenes, lighting approach). No links, no self-promo (promo only in their pinned thread). Risk: **medium** — mods remove "fake influencer" spam/sexualized posts; keep fully clothed-sporty, never repost Sienna there more than ~1×/2 weeks.
- **X (hold):** "Goldie vs Bondi, go" poll · C4 clip · "things i've lost today: keys, sunnies, dignity".

### Fri Oct 16
- **TikTok 1 — 12:00 PM** · **C6** volleyball rules. Hook text: "beach volleyball rules if you're me 🏐". Sound: trending sports/funny-fail sound. Caption: "I yelled 'mine' and ducked. team player 🤝" · #beachvolleyball #goldcoast #funny #fyp #aigenerated
- **TikTok 2 — 7:30 PM** · **existing `collab_sienna_camille_v2.mp4`** — collab. Hook text: "when your bestie visits the Goldie". Sound: trending "bestie/duo" sound. Caption: "pool day with @[Camille handle] ☀️ (both AI)" · #besties #poolday #goldcoast #fyp #aigenerated. Note: tag only if Camille account live; one organic collab, no engagement-swapping.
- **IG feed 7:00 PM — Reel:** collab_sienna_camille_v2 (Collab post with Camille if her IG exists). Caption: "Pool day with my girl 💛 (both AI-generated)" · #poolday #besties #goldcoast #madewithai
- **Stories:** volleyball clip cut; "this or that" stickers (sunrise/sunset, beach/pool); behind-the-scenes text "Friday arvo plans?"
- **Reddit 3 — 1:00 PM · r/StunningAIGirls** · Image: sienna_full.png (boardwalk, different outfit). Title: "[Realistic] Sienna on the Gold Coast boardwalk". Body: "Same character as earlier this week, testing consistency in a new location + outfit. Thoughts?" Risk: low-med (don't exceed 2/week here).
- **X (hold):** collab clip · bikini2 "pool > ocean today" · reply to mentions.

### Sat Oct 17
- **TikTok 1 — 11:00 AM** · **C7** Aussie slang test. Hook text: "only Aussies will pass this test 🇦🇺". Sound: trending quiz/"wrong answers only" sound. Caption: "wrong answers only 👇" · #aussieslang #australia #learnenglish #fyp #aigenerated
- **TikTok 2 — 8:00 PM** · **C8** where are you watching from. Hook text: "how far does this video go? 🌍". Sound: trending travel/map sound. Caption: "drop your city, I'm reading all of them ☀️" · #poolday #goldcoast #whereareyoufrom #fyp #aigenerated
- **IG feed 7:30 PM — Reel:** C7. Caption: "Aussie slang test 🇦🇺 arvo, togs, servo — how'd you go? (AI-generated)" · #aussieslang #australia #aussiegirl #madewithai
- **Stories:** slang quiz stickers (one word per frame); reply-to-comments Story; sunset still.
- **X (hold):** slang quiz post · "drop your city" · cheeky bikini still (keepers/sienna_bikini2) — X lane OK.

### Sun Oct 18
- **TikTok 1 — 12:00 PM** · **Photo-mode slideshow** (stills: sienna_cover, bikini1, cafe_face, volleyball, full, sienna_2) "my Goldie week in 6 pics". Sound: trending photo-dump sound. Caption: "goldie week recap 🌴 which one's your fav?" · #photodump #goldcoast #aussie #fyp #aigenerated
- **TikTok 2 — 7:30 PM** · **C9** "one week back home" recap/next week ask. Hook text: "my week on the Goldie in 10 seconds". Sound: trending emotional/"week recap" sound. Caption: "tell me where I go next 👇" · #goldcoast #australia #weekrecap #fyp #aigenerated
- **IG feed 7:00 PM — Carousel** (feed variety): same 6 stills. Caption: "Goldie week recap 🌴 Swipe and pick a fav. Back to Bondi soon (AI-generated)" · #goldcoast #photodump #aussiegirl #madewithai
- **Stories:** C9 clip; "Bondi next week?" poll; thank-you Story to commenters (non-spammy).
- **X (hold):** recap thread (3 tweets, one still each) · C9 clip.

### Mon Oct 19
- **TikTok 1 — 7:30 PM** · Re-edit of C2 café ranking with new on-screen overlay "café ranking ep.2 — your picks" (no new credits; reuse) OR skip if performance says 1/day. Sound: same trending review sound. Caption: "you voted, I went ☕" · #goldcoastcafe #aussie #fyp #aigenerated (1 TikTok today)
- **IG feed 7:00 PM — Reel:** C9. Caption: "One week back home. Best café, best swim, best sunset 🌅 Where next? (AI-generated)" · #goldcoast #australia #aussiegirl #madewithai
- **Stories:** Q&A box "ask me anything"; next week teaser "Bondi arc 🏙️"; café still.
- **Reddit:** none (3 this week = within 2-4).
- **X (hold):** "monday mood" · AMA prompt · reply to mentions.

## Counts
| Platform | Week 1 |
|---|---|
| TikTok | 13 videos/posts (Tue-Sun 2/day, Mon 1): 9 new lip-sync, 2 existing clips, 1 photo slideshow, 1 re-edit |
| Instagram | 7 feed (6 Reels + 1 carousel) + 7 days Stories (~3 frames/day) |
| Reddit | 3 posts: r/StunningAIGirls ×2, r/aiArt ×1 |
| X | ~21 drafted (3/day, below 3-5 SOP until linked; add replies) — HOLD, not linked |
| YouTube Shorts / Facebook | 0 — no accounts; reuse Reels 3-5/wk when linked |

## Subreddits (checked via web Oct 12)
- **r/StunningAIGirls** — rules: AI-generated women only, freshly generated, **SFW only, swimwear OK "keep it classy"**, no real people/deepfakes. Good fit. Risk low-med.
- **r/aiArt** — SFW, family-friendly; flair = tool; self-promo only in pinned thread; **since Aug 26 2026 repeated posts of the same AI model/"fake influencer" are removed** → max 1 varied post every ~2 weeks. Risk medium.
- Rejected: r/aiinfluencers (must use non-persona account, no growth posting), r/AI_Influencers / r/Ai_ContentCreators / r/Pro_Ai_Art (NSFW-allowed/mixed — off-brand for SFW lane), r/GoldCoast / r/sydney (real-locals subs; AI persona posts would read as spam — engage via comments only, don't post).
- Re-check each sub's sidebar on the day of posting (mods change rules); account u/TheSiennaBlake should have some comment karma first (comment genuinely 2-3×/day in those subs).

## Blockers before go_live (carried from batch1 audit)
- Hub `/org` needs login; `go_live` is GLOBAL (flips all personas' approved items) — clear others' approved queue first.
- `ayr_poster.py` sends no `redditOptions` (title/subreddit) and no `tikTokOptions.isAIGenerated` → patch or post by hand.
- Sienna Ayrshare profile key was missing in the Sep 5 inventory — verify.
- Confirm audio line in `sienna_talking1_web.mp4`; confirm Camille has a live account before the collab tag.
- Dog name (Bruce vs Remi) unresolved.
