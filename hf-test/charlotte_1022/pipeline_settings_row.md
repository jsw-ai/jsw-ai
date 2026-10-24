# Charlotte Hayes: settings row + exceptions for "JSW Pipeline: Script-ready steps"
Drafted 2026-10-22 ~2:15 PM ET. The shared page does not exist yet under the JSW AI home, so this file holds the row until it does. Every value comes from a file on the box (source in brackets). Unknowns are marked TODO. No secrets here, only file paths.

## (a) Settings row
| Field | Value | Source |
|---|---|---|
| Model | Charlotte Hayes, 25, UK ex-footballer, Arsenal fan, London-based | /workspace/jsw_process/charlotte/jsw-charlotte-content.md |
| identity_pack key | `charlotte` (status approved, 2026-10-19 04:15 ET by Samuel) | zen/posting/identity_packs.json |
| Gate face_refs (pack) | keepers/charlotte_face_keeper.png, keepers/charlotte_bikini1.png, keepers/charlotte_bikini2.png, keepers/charlotte_cover.png (relative to /workspace/hf-test) | identity_packs.json |
| Body ref (pack) | keepers/charlotte_body_keeper.png; ref sheet /workspace/hf-test/charlotte_ref/ref_sheet.jpg | identity_packs.json |
| Generation refs, in order | /workspace/hf-test/keepers/charlotte_face_keeper.png, /workspace/hf-test/keepers/charlotte_cover.png, /workspace/hf-test/charlotte_ref/f.png, /workspace/hf-test/charlotte_ref/ref_sheet.jpg | jsw-charlotte-content SKILL.md |
| Body line | /workspace/hf-test/charlotte_ref/LOCKED_BODY.txt (paste verbatim) | SKILL.md |
| Approved v4C start stills reused 10/22 | /workspace/hf-test/charlotte_1022/rb/up/c_S5.jpg (.863), c_D2.jpg (.821), c_P1 (.871), c_I4 (.843) | rb/mkman_s.py, rb/man/X2_pilates_vs_icebath.json |
| Kling element ID | `8f87f513-c3f6-41cc-95ac-c201e98d0d9c` (model `kling3_0`, 5 s, 9:16, 720p, std, sound off) | SKILL.md; rb/man/*.json |
| Still model | `seedream_v5_pro`, 3:4, 2k, single image_reference | rb/man/X3_sauna_tease.json, rb/mkp.py |
| finish_v4C | /workspace/hf-test/charlotte_1022/rb/finish_v4C.py (md5 f7c35257f0065b88e51f1cccd444ca70; P repointed, skin_local from charlotte_1022/work/) | rb/finish_v4C.py |
| Album | "Proper Gorgeous", 10 clean tracks; WAV masters + lyrics in /workspace/music/distrokid/charlotte/ (release.md); mp3s /workspace/music/charlotte/mp3/ | SKILL.md, rb/build2.py |
| Apple Music | https://music.apple.com/us/album/proper-gorgeous/6825712667 | given by JSW AI (parent); TODO: no box file has this link yet |
| Fanvue | https://www.fanvue.com/char_hayes (X bio, pinned post, Reddit only; never in captions) | SKILL.md |
| X | @char_hayes_26: SPICY, sensitive-marked teases OK (topless OK, X only; no full nudity; never as avatar/header) | work/ayr_user_1022.json; jsw-charlotte-content.md; jsw-content-scheduling SKILL.md |
| TikTok | @charlottehayes240: SFW (note: an old post once went to @charlotte_hayes_26; check the linked handle) | ayr_user_1022.json; SHARED_LEARNINGS.md |
| Instagram | charlotte.england2626: SFW | ayr_user_1022.json |
| YouTube | @CharlotteHayesUK: SFW (Short GBesH-nFrE0 is on this channel; Ayrshare lists @charlottehayeswc26) | YouTube oEmbed 10/22 |
| Facebook | Page "Charlotte Hayes" id 1318821087988645 (linked 10/20): SFW | ayr_user_1022.json |
| Reddit | u/CharHayesWC26: SFW (own profile; posts only, never comments) | ayr_user_1022.json; SKILL.md |
| Daily quota | X 5 (>=3 spicy teases), TikTok 3 (1 while throttled), IG 1 Reel + 3 stories, YT 2 Shorts, FB 1, Reddit 2 | SKILL.md |
| AdsPower profile | `k1cwwgmo` (headless only, on Samuel's MacBook, never touch proxies) | SKILL.md |
| Ayrshare credentials | file paths only: /home/box/agent-data/secrets/JSW-ayrshare-api-key.txt, JSW-charlotte-ayrshare-profile-key.txt, x-ayrshare-consumer-keys.json | /workspace/hf-test/sched.py |
| Posting time zone | ET (America/Detroit); scheduleDate in UTC | /workspace/jsw_sched/charlotte_x4_1022.json (X4 1:00 PM ET = 17:00Z) |

## (b) Exceptions (where Charlotte differs from the shared steps)
1. **Smile wording (stills):** "soft closed-mouth smile" fails her gate. Use "same gentle natural smile as the photo, not a wide open-mouth laugh, not grinning". [SHARED_LEARNINGS 10/22; rb/mkp.py TAIL]
2. **Face refs on edits:** single-ref edit plus 2-3 face refs (face_keeper, cover face crop, f.png) beat single-ref by +0.04 to +0.09. NOTE: her 10/22 rb rebuild was single-ref only (Hard Rule #1 / Valentina's process), so the Reviewer should decide which one wins. TODO. [SHARED_LEARNINGS 10/22]
3. **Video gate (Charlotte-specific scripts):** rb/vgate.py and rb/g.sh score every frame (`identity_gate.py img --model charlotte --source seedream --no-ocr`) and pass at median >= .78 with no frame < .70. Gate the final encode. Run one gate at a time, only when `free -g` shows >= 3 GB available (rb2/gw.sh wraps this). [rb/vgate.py, rb2/gw.sh, SHARED_LEARNINGS]
4. **Export size:** finals export at 1080x1920, full frame (cover crop, no blurred bands), per Reviewer note item 10; 720x1280 finals fail review. Keep text at y <= 1395 (930/1280 scaled to 1920). Re-gate the final 1080x1920 encode; build2.py uses crf 14 preset slow. [Reviewer note item 10; rb/build2.py]
5. **Fanvue link:** Charlotte (with Sienna) is one of only two models allowed a Fanvue link, and only in the X bio, pinned post and Reddit.
6. **X sensitive flag:** TODO, not confirmed. No file on the box says the X sensitive flag can't be set through Ayrshare, or that her account-level default is on. The files only say "mark sensitive". Confirm, then record the method. Also, X via Ayrshare needs the OAuth1 consumer-key headers or it returns 419. If X fails, resend X alone. [SHARED_LEARNINGS]
7. **Reddit via Ayrshare:** her 10/20 post went up as a media.ayrshare.com LINK post. Use the image/video upload flow. [SHARED_LEARNINGS]
8. **Lyric/song videos:** one per day on top of quota, starting the day the album is live, one track a day in album order. Lyric timing: charlotte_1022/lyric/work/tr.py (faster_whisper small, int8, 2 threads). [SKILL.md; tr.py]
9. **No Seedance lip-sync or talking-to-camera clips** until the Reviewer passes her face test. [SKILL.md]
