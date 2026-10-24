# CREATIVE_FORMATS.md (2026-10-21, ET)

## A. Clipping pipeline: voiceover / music + locked voices + lip-sync
**Why it "failed" before (from SHARED_LEARNINGS):** no single clipping-pipeline failure is logged; the failures were in the lip-sync step: (1) lines over ~8 words get cut off in 8 s Seedance clips (Madison 10-15); (2) Seedance adds idle silence before speech; (3) Wan 2.7 lip-sync gave an intense face and failed the gate (.505); (4) cleavage-heavy start frames get refused as nsfw; (5) upscaled frames score lower on the gate (score originals); (6) Seedance adds skin gloss.
**Pipeline**
1. Source: an approved, gated clip (Seedance/Kling) or a lip-sync final.
2. Voice: seed_audio TTS with the model's locked voice element (`generate_audio`, voice_type=element), <=8 words per 8 s; or VO laid over a silent b-roll clip (no lip-sync needed, cheapest).
3. Lip-sync only for to-camera lines: Seedance 2.0 i2v, audio_references = the TTS file, "begins speaking immediately", 36 cr 720p.
4. Finish in ffmpeg: trim/loop to length, 1080x1920 crop, caption via drawtext, music bed ducked under VO (`sidechaincompress`), loudnorm I=-14 LUFS, AAC 192k.
   ```
   ffmpeg -i clip.mp4 -i vo.wav -i music.wav -filter_complex "[2:a]volume=0.35[m];[m][1:a]sidechaincompress=threshold=0.05:ratio=8[d];[d][1:a]amix=2,loudnorm=I=-14[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -shortest out.mp4
   ```
5. Music: only our own synth tracks (camille_oct20/music/synth.py, camille_oct16/music) or platform-licensed sounds added in-app at posting time. Never bake commercial songs into the file.
**10 s test (0 credits):** hf_audit_1021/clip_sample_10s.mp4 = Sienna waved clip looped to 10 s, 1080x1920, "POV: first day of vacation" caption, our golden_hour_pop track, -14 LUFS. Rendered fine in 4 s. Lip-sync step not tested (36 cr, over the audit cap).

## B. Weekly trend-remix workflow
1. Monday research (30 min/platform): TikTok Creative Center (ads.tiktok.com/business/creativecenter: Trends > Songs, Hashtags, Creators, filter US/7 days); IG: Reels audio with the "trending" arrow, Professional Dashboard > Trends; X: x-namespace search tools (top posts by keyword: "pov", "photo dump", "first class", "gym") sorted by engagement; YouTube Shorts: Explore Shorts + YouTube Research tab in Studio. Use Higgsfield `video_analysis_create` on a top video URL for a scene-by-scene breakdown.
2. Pick 3 formats (structure, not the footage): hook text, beat timing, camera move, edit pattern.
3. Remake originally: our model, our setting, our audio (or the in-app trending sound attached at upload), our caption twist. Never re-upload others' clips.
4. Model twists: Sienna = surf/van/beach; Camille = Paris chic/cafe; Charlotte = British football fan/pub; Madison = gym/golf/US preppy; Gabriela = Miami/Brazil energy; Valentina = Buenos Aires/rooftop glam.
5. Gate, virality_predictor, Reviewer, schedule. Log which format won in SHARED_LEARNINGS.

## C. Comedy angles + 3 recurring bits each
- **Sienna (chaotic surfer):** 1) "Surf report" with fake-serious forecasts ("swell: emotional"); 2) "Things Aussies say vs mean"; 3) van-life fails (sand everywhere, eaten by seagull).
- **Camille (dry Parisian snob):** 1) "Rating American things as a Parisian" (/10, eyebrow); 2) "Café rules you broke"; 3) "Mon dieu" reaction to tourist outfits (stills of herself, no real people).
- **Charlotte (anxious Arsenal fan):** 1) Matchday mood meter: green-screen-style still of her over a plain scoreline card (text only, no league footage/logos); 2) Pub reenactment: she plays every fan type after a late goal; 3) "Tactical analysis" with salt shakers / bottle caps on a pub table.
- **Madison (overconfident gym girl):** 1) "Gym bro translation"; 2) Golf "confidence vs result" (stills, no club in hands); 3) Spreadsheet of her rest-day excuses.
- **Gabriela (hyper Miami):** 1) "Brazilian mom calling" POV; 2) Miami price-shock reviews; 3) "Portuguese words you need" with dramatic examples.
- **Valentina (Colombian drama queen):** 1) Telenovela-style overreaction to small problems; 2) "Tinto (Colombian coffee) etiquette" rules; 3) "Rating dances at the salsa club" (her own clones via Clones preset).
**Top 3 to test first:** (1) Charlotte matchday mood meter (still + scoreline card + VO, ~3 cr); (2) Camille "Rating American things" (lip-sync 36 cr); (3) Valentina telenovela overreaction (Frozen in motion / Superstar preset + VO).

## D. COPYRIGHT: clipping sports highlights
**Short answer: Samuel's assumption is mostly wrong.** Adding your own sound or commentary does not by itself make a clip fair use, and the platforms' automated systems don't check for fair use at all. They match the footage.

**US fair use (17 U.S.C. §107)** weighs four factors: purpose (transformative? commercial?), nature of the work, amount used, and market effect. https://www.law.cornell.edu/uscode/text/17/107 , https://www.copyright.gov/fair-use/
- Commentary/criticism *about* the clip can be transformative (Campbell v. Acuff-Rose, 1994: https://supreme.justia.com/cases/federal/us/510/569/). Hosseinzadeh v. Klein (S.D.N.Y. 2017) found a reaction video fair use because it was interspersed with real critique: https://law.justia.com/cases/federal/district-courts/new-york/nysdce/1:2016cv03081/456012/45/
- Warhol v. Goldsmith (2023) narrowed "transformative": a new meaning isn't enough when the use serves the same purpose as the original, especially commercially: https://www.supremecourt.gov/opinions/22pdf/21-869_87ad.pdf
- Highlights are the most valuable part of a match (amount factor), and the leagues license them for money (market factor). A goal clip with commentary on top still replaces the licensed highlight, so fair use is weak.
- Swapping or adding audio doesn't help with the video match. Content ID and Rights Manager match the picture. Removing the original audio only avoids the separate broadcast-audio claim.

**Platform enforcement**
- YouTube: Content ID claims can block the video, monetize it for the rights owner, or track it. A takedown request is a copyright strike; 3 strikes in 90 days terminates the channel. https://support.google.com/youtube/answer/2797370 , https://support.google.com/youtube/answer/2814000
- Meta (IG/FB) Rights Manager: matches can mute, block, or monetize the content for the rights owner. Repeat infringement removes accounts and their monetization eligibility. https://rightsmanager.fb.com/ , https://www.facebook.com/help/1020633957973118
- TikTok: removes infringing content and bans repeat infringers. Muting happens with unlicensed music. https://www.tiktok.com/legal/page/global/copyright-policy/en
- X: DMCA takedowns, with accounts suspended for repeat violations (NFL notices got Deadspin and SB Nation suspended in 2015). https://help.x.com/en/forms/ipi , https://help.x.com/en/rules-and-policies/copyright-policy

**Leagues in practice**
- Premier League: aggressive. It runs an IP enforcement programme and social-media monitoring, plus creator takedowns. https://www.premierleague.com/ip-enforcement-policy . The only safe route is its official Adobe fan tools and assets: https://www.sportspro.com/news/premier-league-adobe-ai-tools-content-july-2025/
- NBA: tolerant. Silver called highlights "marketing" and the league monetizes via Content ID. But its terms forbid reposting, and it does send takedowns. https://www.businessinsider.com/adam-silver-nba-ok-highlights-social-media-twitter-gifs-2018-5 , https://www.sportsbusinessjournal.com/Daily/Issues/2017/07/20/Technology/adam-silver-against-suing-nba-highlights-youtube
- NFL: strict, as the 2015 X suspensions show. https://www.si.com/extra-mustard/2016/02/09/nba-highlight-videos-clips-youtube-legality
- UFC: very aggressive about piracy (Zuffa has sued streamers and users). Treat as no-go.

**Risk to our accounts:** new accounts have no goodwill. Early strikes or claims cut reach, and on YouTube three strikes ends the channel. Claimed videos earn nothing for us, and repeat Rights Manager or Content ID hits can cost monetization eligibility (YPP, Meta partner tools) on monetized accounts. Our models are AI personas, which brings extra platform scrutiny. One bad sports clip can sink an account that took weeks to build.

**Rule set (practical)**
1. No league broadcast footage on any model account. That covers the Premier League, NFL, UFC, UEFA, and F1.
2. NBA only if Samuel accepts the risk: a clip of 5 s or less inside a post of 30 s or more, at least 80% of the runtime being the model's own commentary on screen, original audio removed, one clip per post, never the full play sequence, never on a brand-new account (wait until it has 30+ clean posts), and expect claims. My recommendation is still no.
3. Commentary must be about the play itself (analysis or critique), not just "OMG" reactions with a clip running.
4. Safe alternatives: text scoreline cards and stat graphics we make ourselves (no logos); reenactments with the model in a pub, at home, or with table tactics; AI stills of the model in generic kit colours; a stitch or duet in-app of the league's own official TikTok or IG post, which stays inside the platform license; and the Premier League's official fan-content tools.
5. Music: add licensed sounds in-app only. Never bake commercial tracks into the file.
6. Dispute a claim only when the post is genuinely commentary. Never fight a Premier League or NFL claim on a model account.
*(This is research, not legal advice. For anything monetized, ask a lawyer.)*

## E. Stand-up comedy for X
**What goes viral on X (from observed top clips; heuristics, not measured):** 20-60 s, with the punchline landing in the first 3-5 s (open on the strongest line, then the setup). Burned-in captions (most people watch muted). A tight waist-up shot on a mic stand with a brick wall or red curtain and one spotlight. Real-sounding laughter right after each punch, because a hard cut on the laugh reads as authentic. Post text = the best line, not "lol". One premise per clip.
**Format:** a 45 s set built from 4-5 Seedance 2.0 i2v takes of 8 s each (36 cr each, 720p, audio_references = TTS from the locked voice, at most 8 words per take). All takes use one gated start still (same stage, same outfit, higher neckline, holding the mic at chest height). Crowd cutaways are 2-3 Seedream stills of a dim generic audience (no real faces) with a slow push in ffmpeg. Laughter: our own recorded or CC0 laugh beds, 0.5-1.5 s, mixed at -12 dB after punches. Cost is about 150-190 cr per set, so try it as one test before making it a series.
**Longer talking takes, consistent face:** Seedance 2.0 is the best for identity but is reliably clean only up to 8 s, so chain the takes with a matched start frame. Legacy generate_talking_head (Speak v2) does 5/10/15 s from image + WAV but is older and identity is untested. Kling 3.0 with an Element can do multi-shot but its lip-sync is weaker. Gate every take, then cut on the laughs to hide joins.

**Charlotte, 45 s ("Arsenal anxiety")**
1. "I'm an Arsenal fan, so I've got trust issues." (laugh)
2. "We're 2-0 up in the 80th minute. Lovely."
3. "I'm already writing the apology text to myself." (laugh)
4. "My boyfriend asked if I'd ever leave him."
5. "I said I've stayed through worse defending." (big laugh)
6. "My mum prays at church. I pray at corners."
7. "Same God, different panic." (laugh, applause out)

**Madison, 45 s ("Gym girl logic")**
1. "I go to the gym six days a week." (pause)
2. "Mostly to film myself walking to the gym." (laugh)
3. "My trainer said listen to your body."
4. "My body said Chipotle. Respect the process." (laugh)
5. "I tried golf to meet rich guys."
6. "Now I'm the rich guy. Four hundred dollars a lesson." (laugh)
7. "Ladies, the real gains were the debt." (applause out)

**Updated top 3 to test first:** (1) Charlotte stand-up set for X (the strongest persona fit and the most shareable format, ~180 cr); (2) Charlotte matchday mood meter (~3 cr); (3) Camille "Rating American things" (36 cr).
