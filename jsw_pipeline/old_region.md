## Model settings

### Charlotte

Added 10/22 by Charlotte's bot from <code>/workspace/hf-test/charlotte_1022/pipeline_settings_row.md</code>. Each value comes from a box file. <b>TODO = unconfirmed.</b> Paths only, no secrets.

| Field | Value | Source |
| --- | --- | --- |
| identity\_pack key | <code>charlotte</code> (approved 2026-10-19 04:15 ET by Samuel) | zen/posting/identity\_packs.json |
| Gate face refs | keepers/charlotte\_face\_keeper.png, charlotte\_bikini1.png, charlotte\_bikini2.png, charlotte\_cover.png (under /workspace/hf-test) | identity\_packs.json |
| Body ref / sheet | keepers/charlotte\_body\_keeper.png; /workspace/hf-test/charlotte\_ref/ref\_sheet.jpg | identity\_packs.json |
| Generation refs, in order | keepers/charlotte\_face\_keeper.png, keepers/charlotte\_cover.png, charlotte\_ref/f.png, charlotte\_ref/ref\_sheet.jpg | jsw-charlotte-content [SKILL.md](http://SKILL.md) |
| Body line | /workspace/hf-test/charlotte\_ref/LOCKED\_BODY.txt (verbatim) | [SKILL.md](http://SKILL.md) |
| Reused approved v4C starts | /workspace/hf-test/charlotte\_1022/rb/up/c\_S5.jpg (.863), c\_D2 (.821), c\_P1 (.871), c\_I4 (.843) | rb/mkman\_[s.py](http://s.py), rb/man/\*.json |
| Stills | <code>seedream_v5_pro</code>, 3:4, 2k, single image\_reference | rb/[mkp.py](http://mkp.py) |
| Kling | Element <code>8f87f513-c3f6-41cc-95ac-c201e98d0d9c</code>; <code>kling3_0</code>, 5 s, 9:16, 720p, std, sound off | rb/man/\*.json |
| finish\_v4C | /workspace/hf-test/charlotte\_1022/rb/finish\_[v4C.py](http://v4C.py) (md5 f7c35257…; P repointed) | rb/finish\_[v4C.py](http://v4C.py) |
| Album | Proper Gorgeous, 10 clean tracks; WAV + lyrics /workspace/music/distrokid/charlotte/; mp3 /workspace/music/charlotte/mp3/ | [SKILL.md](http://SKILL.md), rb/[build2.py](http://build2.py) |
| Apple Music | [https://music.apple.com/us/album/proper-gorgeous/6825712667](https://music.apple.com/us/album/proper-gorgeous/6825712667) (TODO: from JSW AI; not yet in a box file) | JSW AI |
| Fanvue | [https://www.fanvue.com/char\_hayes](https://www.fanvue.com/char_hayes) (X bio, pinned post, Reddit only) | [SKILL.md](http://SKILL.md) |
| X | @char\_hayes\_26: <b>SPICY</b>, sensitive-marked teases (topless OK; no full nudity; never avatar/header) | work/ayr\_user\_1022.json; [jsw-charlotte-content.md](http://jsw-charlotte-content.md) |
| TikTok | @charlottehayes240: SFW | ayr\_user\_1022.json |
| Instagram | charlotte.england2626: SFW | ayr\_user\_1022.json |
| YouTube | @CharlotteHayesUK: SFW (her posted Short GBesH-nFrE0 is on this channel; Ayrshare's read-only data lists @charlottehayeswc26 for the same "Charlotte Hayes" account) | YouTube oEmbed for [youtube.com/shorts/GBesH-nFrE0](http://youtube.com/shorts/GBesH-nFrE0) (author\_url [youtube.com/@CharlotteHayesUK](http://youtube.com/@CharlotteHayesUK)), fetched 10/22 2:12 PM ET; SHARED\_LEARNINGS 10/21 |
| Facebook | Page "Charlotte Hayes" 1318821087988645: SFW | ayr\_user\_1022.json |
| Reddit | u/CharHayesWC26: SFW (posts only, never comments) | ayr\_user\_1022.json |
| AdsPower | <code>k1cwwgmo</code>, headless only, MacBook; never touch proxies | [SKILL.md](http://SKILL.md) |
| Profile key file | /home/box/agent-data/secrets/JSW-charlotte-ayrshare-profile-key.txt | /workspace/hf-test/[sched.py](http://sched.py) |
| Posting time zone | ET (America/Detroit, UTC-4 now); scheduleDate is sent in UTC | /workspace/jsw\_sched/charlotte\_x4\_1022.json: X4 slot "1:00 PM ET Thu Oct 22 2026" = scheduleDate 2026-10-22T17:00:00Z |

### Madison

Added 10/22 by Madison's bot from <code>/workspace/madison_oct22/submit/madison_pipeline_row.md</code>, with the TBDs resolved by JSW AI on 10/22. Paths are relative to <code>/workspace/hf-test/zen/posting/</code> unless absolute. Paths only, no secrets.

| Field | Value | Source |
| --- | --- | --- |
| identity\_pack key | <code>madison</code> (approved by Samuel 2026-10-14, Look A) | identity\_packs.json |
| Gate / eye-check refs | <code>keepers/madison_face_keeper.png</code>, <code>keepers/madison_body_keeper.png</code> (under /workspace/hf-test); sheet <code>reference_set_madison.png</code> | identity\_packs.json, jsw-madison-content [SKILL.md](http://SKILL.md) |
| Approved ref photos (single-ref edit bases) | <code>madison_test/fin/*_v4C.jpg</code>: m7–m10, n2, n3, n4, n6, w1–w7, w9, w10, w12–w16. Used 10/22: n2, n3, n6, m10 (uploaded as <code>/workspace/madison_oct22/up/base_*.jpg</code>) | madison\_test/fin/, MANIFEST\_[2026-10-22.md](http://2026-10-22.md) |
| Body line | <code>/workspace/madison_oct20/LOCKED_BODY_LINE.txt</code> (word for word in every image and video prompt) | [SKILL.md](http://SKILL.md) |
| Stills | <code>seedream_v5_pro</code> single-ref "Edit this exact photo" of one approved v4C final; soft even front light; <b>waist-up</b> framing | MANIFEST, work/prompt\_files/\*.txt |
| finish\_v4C | Full v4C: texture 0.5, sharpen 0.3, grain sigma 3 (<code>/workspace/madison_oct22/work/finish_v4C.py</code>). v4C-lite is dropped | work/finish\_[v4C.py](http://v4C.py) |
| Still gate | <code>identity_gate.py img --model madison --source seedream --body</code>, ≥ 0.78, plus an eye check against body\_keeper | [SKILL.md](http://SKILL.md) |
| Video gate | <code>/workspace/madison_oct22/work/fgate.py <video> 1 <out.json></code> on the final export: every frame ≥ 0.70, median ≥ 0.78 | qc/\*\_final.summary.json |
| Kling | Element <code>04d4157b-50ac-45e3-a442-4a7fca2c2eff</code> ("Madison-oct20-v4Clite"); <code>kling3_0</code>, 5 s, 720p std, sound off, low motion, native 9:16 | MANIFEST, SHARED\_LEARNINGS 10/20 |
| Lip-sync | Seedance 2.0 with <code>voicerefs-from-sam/madison.mp3</code> | [SKILL.md](http://SKILL.md), identity\_packs.json |
| Album | "Iced Coffee & Heartbreak" (artist Madison Cole, 10 clean tracks). WAV masters + lyrics <code>/workspace/music/distrokid/madison/</code>. Never reuse a track across clips or models | [release.md](http://release.md) |
| Apple Music | [https://music.apple.com/us/album/iced-coffee-heartbreak/6825712883](https://music.apple.com/us/album/iced-coffee-heartbreak/6825712883). In captions on X, YT, FB and Reddit; "link in bio" on TikTok and IG | JSW AI |
| Content | SFW on every platform (Madison stays tame while @MadisonCole69 is new). No Fanvue link until she is verified | [SKILL.md](http://SKILL.md) §0 |
| TikTok | @madisoncolewc26: SFW, <b>1 post a day</b> while throttled | Ayrshare (SHARED\_LEARNINGS 10/19); JSW AI 10/21 |
| Instagram | @madison\_cole\_26: SFW; <code>instagramOptions.isAIGenerated: true</code> | SHARED\_LEARNINGS 10/19, MANIFEST |
| YouTube | @madisoncolewc2026 per Ayrshare: SFW (the Tracker section reads @MadisonColeUSA via yt-dlp; confirm they're the same channel) | SHARED\_LEARNINGS 10/19 |
| Facebook | Page "Madison Cole" 61595403549538: SFW, linked in Ayrshare (Scheduler booked a FB post 10/22) | SHARED\_LEARNINGS 10/20; JSW AI |
| Reddit | u/Regular\_Affect\_4886, own profile only: SFW, posts only, never comments; Ayrshare Reddit = 1 image, no video | SHARED\_LEARNINGS 10/19 |
| X | @MadisonCole69 (new, live status unverified); old @madisoncole26 is suspended. Blocked for scheduling until verified and cleared by JSW AI | jsw\_process/CONFLICT\_REVIEW\_[2026-10-21.md](http://2026-10-21.md) |
| AdsPower | <code>k1cwwjw5</code>, headless only, Mac (machine 32d82b68); never touch proxies; never relaunch <code>k1cwvh25</code> | [SKILL.md](http://SKILL.md) §12b |
| Mac scripts | <code>~/adsbot/madison/</code>: eng\_[tt.py](http://tt.py), bios\_ai\_1022, fix\_1022, del\_golf\_1022, bios\_music\_1022 (names only; contents not documented on the box) | Mac folder listing |
| Profile key file | <code>/home/box/agent-data/secrets/JSW-madison-ayrshare-profile-key.txt</code> | jsw-content-scheduling [SKILL.md](http://SKILL.md) |
| Posting time zone | America/Detroit (ET) | JSW AI |

## Exceptions

### Charlotte

1. <b>Smile wording (stills):</b> "soft closed-mouth smile" fails her gate. Use "same gentle natural smile as the photo, not a wide open-mouth laugh, not grinning". (SHARED\_LEARNINGS 10/22; rb/[mkp.py](http://mkp.py))
2. <b>Face refs on edits:</b> single-ref plus 2-3 face refs scored +0.04 to +0.09, but the 10/22 rebuild was single-ref only (Valentina's process). TODO: the Reviewer decides which to use.
3. <b>Video gate scripts:</b> <code>rb/vgate.py <video> <fps> <out.json></code> and <code>rb/g.sh <clip> [fps]</code> score every frame (<code>identity_gate.py img --model charlotte --source seedream --no-ocr</code>). Pass = median ≥ .78 and no frame \< .70, on the final encode. Run one gate at a time, only with ≥ 3 GB free (<code>rb2/gw.sh</code> waits on <code>free -g</code>).
4. <b>Export size:</b> finals export at 1080x1920, full frame (cover crop, no blurred bands), per Reviewer note item 10; 720x1280 finals fail review. Keep text at y ≤ 1395 (930/1280 scaled to 1920). Re-gate the final 1080x1920 encode; [build2.py](http://build2.py) uses crf 14 slow.
5. <b>Fanvue:</b> she is one of two models (with Sienna) allowed a link, and only in the X bio, pinned post and Reddit.
6. <b>X sensitive flag:</b> TODO, unconfirmed. No box file says it can't be set through Ayrshare or that the account default is on; the files only say "mark sensitive".
7. <b>Reddit:</b> her 10/20 Ayrshare post went up as a link post. Use the image/video upload flow.
8. <b>Lyric videos:</b> one per day on top of quota, in album order. Timing: <code>charlotte_1022/lyric/work/tr.py</code> (faster\_whisper small, int8).
9. <b>No Seedance lip-sync or talking-to-camera clips</b> until the Reviewer passes her face test.
10. <b>Reviewer:</b> final exports must be 1080x1920. A 720x1280 export fails the full-frame rule.

### Madison

1. <b>Framing:</b> waist-up only. The 10/22 single-ref edits gated just 4 of 33 at .78; full-body scored .65–.77, while waist-up passed (s2b .809, s7b .797). (SHARED\_LEARNINGS 10/22)
2. <b>Bright outdoor / golf:</b> direct sun fails her gate (golf .72–.77). Fix: single-ref edit of a passing still with "open shade, even front light". Golf is a still only, with no club in her hands (Kling golf clips failed review 4 times, 184 cr).
3. <b>Video gate:</b> every frame ≥ .70 and median ≥ .78 on the final export (<code>work/fgate.py</code>). The 10/22 finals sat close to the floor (pickleball\_v8 min .704 / median .7925; fit\_rating\_v2 min .703 / median .7885), so leave \~.05 headroom on the raw clip.
4. <b>Export framing:</b> native Kling 9:16 from a 9:16 crop of the still (e.g. <code>v2/s7b_916L.jpg</code>), then crop-fill <code>scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920</code>: no blurred bands, never stretched. Encode <code>libx264 -profile:v main -crf 23 -maxrate 10M -bufsize 14M -preset veryfast -threads 2 -pix_fmt yuv420p</code>, AAC 48 kHz 128k, <code>-map_metadata -1 -movflags +faststart</code>, under 15 MB (<code>/workspace/madison_oct22/work/build_v8.sh</code>).
5. <b>Audio:</b> each clip carries a different track from her own album (e.g. <code>07_sweat_it_out.wav</code> from -ss 20 with a 0.7 s fade-out), not a silent track.
6. <b>TikTok:</b> throttled to 1 post a day until views recover (Samuel's rule, relayed by JSW AI 10/21).
7. <b>Reddit:</b> own profile only (no subreddits). The Apple Music link goes in song posts.
8. <b>Moderation:</b> no bikini or two-piece wording (NSFW-blocked for Madison and still charged); use tank, tee or scoop tops.
9. <b>Kling motion:</b> no hand-based transitions, never slow Kling footage, no wide laughs when the start still is under .85, keep props out of her hands, and keep the paddle inside the frame (pickleball v7 failed when it left the frame; v8 fixed it with a slow twirl close to her body).
10. <b>Engagement:</b> her own AdsPower profile <code>k1cwwjw5</code> on the Mac, headless. Check status first and leave it if Samuel has it open. Never touch proxies, never relaunch <code>k1cwvh25</code>, never post or upload through AdsPower. After copying helper scripts, grep for the profile id (on macOS use <code>sed -i ''</code>).
11. <b>Box resources:</b> one gate or encode at a time, only with ≥ 3 GB free (<code>free -g</code>). The 10/22 coffee final gate was OOM-killed (<code>qc/coffee_final.log</code>).
12. <b>X:</b> skip until @MadisonCole69 is verified live and JSW AI clears it.

## Camille settings

Added 10/22. No model settings table on this page yet, so this is a standalone block. Paths are relative to <code>/workspace/hf-test/</code>.

| Setting | Camille |
| --- | --- |
| Approved ref photos | Face: <code>zen/posting/camille_v3/refs/face_front.png</code>, <code>face_three_quarter_matte.png</code>, <code>face_neutral_off_matte.png</code>. Body: <code>zen/posting/camille_v3/refs/body_waistup.png</code>. Approved final: <code>zen/posting/camille_oct16/natural_v4/fin/body1_v4C.jpg</code> (Higgsfield media 62cab441). Source: <code>zen/posting/camille_v2/raw/r3_4.png</code>. Sheet: <code>zen/posting/camille_v3b_pack_sheet.jpg</code>. Use deglossed (matte) stills only; the shiny <code>face_three_quarter.png</code> / <code>face_neutral_off.png</code> are superseded. |
| identity\_pack key | <code>camille_v3</code> (gate with <code>--model camille_v3</code>; <code>camille</code> is retired) |
| Kling element ID | <code>e3a57e1a</code> |
| Album | Riviera Après Minuit by Camille Dubois, [Apple Music](https://music.apple.com/us/album/riviera-apr%C3%A8s-minuit/6825779566) |
| Platforms / handles | TikTok @camilledubois089, IG @camilledubois341, X @CamilleDubav, YouTube @camilledubois-r6m, FB Page 61595437087876, Reddit u/Pristine\_Culture\_693 |
| Content | SFW only: no spicy content, X sensitive flag off, no Fanvue |
| Posting time zone | America/Detroit (ET) |
| Exceptions | TikTok @camilledubois089 shows error 10221 in her logged-in view → post via Ayrshare; if blocked, TikTok quota shifts to Shorts/Reddit |

## Gabriela

Added 10/22 by Gabriela from the box files (identity\_packs.json, gabriela\_locked\_body\_[line.md](http://line.md), gabriela/2026-10-22/, Ayrshare /user read, /workspace/music/distrokid/gabriela/[release.md](http://release.md)). Box copy: <code>/workspace/hf-test/zen/posting/gabriela/SCRIPT_SETTINGS_ROW.md</code>. TBD = not documented on the box. No key values here.

### Gabriela settings

| Field | Gabriela |
| --- | --- |
| identity\_pack key | <code>gabriela</code> in <code>/workspace/hf-test/zen/posting/identity_packs.json</code> (approved by Samuel 2026-10-14 via reference\_set\_gabriela.jpg) |
| Approved face refs (gate refs) | <code>/workspace/hf-test/keepers/gabriela_face_keeper.png</code>, <code>keepers/gabriela_bikini1.png</code>, <code>keepers/gabriela_bikini2.png</code>, <code>keepers/gabriela_cover.png</code> |
| Approved body refs | <code>keepers/gabriela_bikini1.png</code>, <code>keepers/gabriela_bikini_candid.png</code>, <code>keepers/gabriela_refs/gabriela_ref1.png</code>, <code>ref3.png</code>, <code>ref4.png</code> (under /workspace/hf-test/) |
| Ref sheet, body spec, locked line | <code>zen/posting/reference_set_gabriela.jpg</code>, <code>zen/posting/gabriela_body_spec.md</code>, <code>zen/posting/gabriela_locked_body_line.md</code> (paste word for word in every prompt) |
| Gate-passed v4C finals, 10/22 (Reviewer verdict pending) | <code>gabriela/2026-10-22/fin/{paulista_a,paulista_b,knit_a,knit_b,rooftop_a}_v4C.jpg</code> (still gate .824-.845). padaria\_\* failed the body gate: don't use. Source media ids for single-ref edits: 6e054bfc-af71-4f06-8f9b-61aa3a7ce56d, bb198cab-6eb3-4a3c-96eb-5153576b7782 (file mapping TBD) |
| Kling Element ID | <code>8b128aab-61f8-4634-8119-7b9b79e0f2fb</code> ("Gabriela-matte-test"; kling3\_0, 5 s, sound off). Known issue: built from light-hazel-eye stills, so clips inherit lighter eyes. Replacement Element bf8d97db (full ID TBD) was never used or validated |
| Album | "Brisa de Miami" (artist Gabriela, 10 tracks). Masters <code>/workspace/music/distrokid/gabriela/</code>. Apple Music link: TBD (not live yet) |
| Platforms and handles (her own Ayrshare profile) | X @GabrielaSailq1 · IG @gabrielasantos.mia · TikTok @gabriela\_santos343 · YouTube @gabrielasantos-y5t1z · Reddit u/Fresh\_Membership8984 (<code>u_Fresh_Membership8984</code>) · FB: do not post |
| SFW or spicy | SFW on TikTok, IG, YouTube (no swimwear on YT), Reddit. Spicy on X only, no nudity, never in profile or header. No Fanvue links |
| Posting time zone | ET (America/New\_York, Miami persona). Slot times: set by the Scheduler |
| Engagement | AdsPower profile k1cwwmho, headless, attach only, never touch proxies |

### Gabriela exceptions

- FB is locked under appeal: skip Facebook in every posting step.
- The release card says "coming soon" until "Brisa de Miami" is live (captions stay on "coming soon" too, no Apple link yet).
- X posts get the sensitive flag from the X account default setting, because Ayrshare can't set it per post.

## Sienna: settings and exceptions (JSW Sienna)

Source: <code>/workspace/jsw_tiktok/sienna/sop/script_ready_row_sienna.md</code>

### Kling

- Element: Sienna-v2-1020, <code>2603afeb-5f21-4acc-a3de-8904d5a32cb9</code>
- Model <code>kling3_0</code>, sound off, low motion
- Generate natively at the target aspect ratio. If a clip comes out 3:4, cover-crop it with <code>scale=-2:1920,crop=1080:1920</code>. Never pad it, because padding creates blur bands.

### Reference stills

- Folder: <code>/workspace/hf-test/zen/posting/sienna_refs/</code>
- Files: <code>story1_a_v4C.jpg</code>, <code>story2_a_v4C.jpg</code>, <code>story3_b_v4C.jpg</code>, <code>reddit_x1_b_v4C.jpg</code>
- Use one reference image per Seedream job.
- Body line: <code>/workspace/jsw_tiktok/sienna/SIENNA_LOCKED_BODY_LINE.txt</code>

### Gates

- Stills must score 0.79 or higher: <code>identity_gate.py img --model sienna --source seedream --body</code>
- The script's default seedream\_centroid is 0.78, so check the score again after it runs.
- Video must score 0.78 or higher on 16 frames, against story1\_a\_v4C.

### Banned stills

- sC2\_b, sA2\_b, eB4\_b, eB4\_c

### Body check

- Even golden tan and a full, round, natural C-to-D cup bust.
- Check by eye against the reference sheet.

### Known face issue

- Seedream narrows her face in wider body shots and with closed-mouth smirks, and those score 0.64 to 0.77.
- Head-to-waist framing with a teeth smile and even front light passes.

### Music

- Masters: <code>/workspace/music/distrokid/sienna/01-10 *.wav</code>
- Lyrics: [release.md](http://release.md) in the same folder
- Wording: "out now on Apple Music" with [https://music.apple.com/us/album/salt-in-my-hair/6825685962](https://music.apple.com/us/album/salt-in-my-hair/6825685962)
- No Spotify mentions yet.

### Accounts

- AdsPower profile k1cwvh25: headless only, and never touch the proxy or fingerprint.
- Ayrshare can't post to Reddit user profiles (u\_ gives SUBREDDIT\_NOEXIST).
- Reddit returns 403 to the box, so use the AdsPower session.