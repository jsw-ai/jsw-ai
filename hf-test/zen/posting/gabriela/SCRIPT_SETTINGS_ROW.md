# Gabriela: settings row for "JSW Pipeline: Script-ready steps" (Notion, JSW AI home)
Written 2026-10-22 ~2:20 PM ET from the files on the box (read-only, no gates or encodes run). Gabriela uses Valentina's pipeline (VALENTINA_PIPELINE.md); only the per-model settings and real differences are listed here. TBD = not documented on the box.

| Field | Gabriela |
|---|---|
| identity_pack key | `gabriela` in /workspace/hf-test/zen/posting/identity_packs.json (status: "APPROVED by Samuel Oberlin 2026-10-14 via reference_set_gabriela.jpg") |
| Approved face refs (gate refs) | /workspace/hf-test/keepers/gabriela_face_keeper.png, keepers/gabriela_bikini1.png, keepers/gabriela_bikini2.png, keepers/gabriela_cover.png |
| Approved body refs | keepers/gabriela_bikini1.png, keepers/gabriela_bikini_candid.png, keepers/gabriela_refs/gabriela_ref1.png, gabriela_ref3.png, gabriela_ref4.png (all under /workspace/hf-test/) |
| Reference sheet / body spec | zen/posting/reference_set_gabriela.jpg; zen/posting/gabriela_body_spec.md; locked body+hair line (paste word for word in every prompt): zen/posting/gabriela_locked_body_line.md |
| "Reference board, approved 10/19" (named in the skill) | Path TBD (not found on the box) |
| Single-ref source stills for 10/22 batch | Higgsfield media ids 6e054bfc-af71-4f06-8f9b-61aa3a7ce56d (paulista/knit/rooftop) and bb198cab-6eb3-4a3c-96eb-5153576b7782 (padaria), per gabriela/2026-10-22/work/req_stills.json. Which v4C files these ids are: TBD (mapping not saved) |
| Gate-passed v4C finals (10/22, Reviewer verdict pending) | gabriela/2026-10-22/fin/{paulista_a,paulista_b,knit_a,knit_b,rooftop_a}_v4C.jpg (still gate .824-.845). padaria_* FAILED the body gate (thigh proxy): do not use as refs |
| Kling Element ID | 8b128aab-61f8-4634-8119-7b9b79e0f2fb ("Gabriela-matte-test", built from carousel finals 02_acai, 03_churrasco, 04_miami_walk; used for the 10/22 collab, job e1126b61). Known issue: those stills carry light green-hazel eyes, so clips inherit lighter eyes (SHARED_LEARNINGS 10/20). A replacement Element bf8d97db was created 10/20 but never used or validated (full ID TBD) |
| Kling settings used | kling3_0, start_image = gated v4C still, 5 s, sound off (std 7.5 cr / pro 8.75 cr per 5 s), prompt includes `<<<8b128aab-61f8-4634-8119-7b9b79e0f2fb>>>` |
| Album | "Brisa de Miami" (artist "Gabriela", 10 tracks, Latin/Pop, EN+PT, not explicit). Masters: /workspace/music/distrokid/gabriela/NN_title.wav, MP3s in .../mp3/, notes in .../release.md, cover /workspace/music/covers/gabriela_cover_v1.jpg. Apple Music link: TBD (not live yet). Spotify link: TBD |
| Platforms and handles (Ayrshare, her own Profile-Key profile, not Default) | X @GabrielaSailq1 · Instagram @gabrielasantos.mia · TikTok @gabriela_santos343 · YouTube @gabrielasantos-y5t1z (channel UCuCbaErKFb9rXKwYz_6YsUg) · Reddit u/Fresh_Membership8984 (own profile; subs only per their rules/flair) · Facebook: DO NOT post (locked, under appeal) |
| SFW or spicy | SFW on TikTok, IG, YouTube (no swimwear on YouTube), Reddit and FB. Spicy captions/content allowed on X only, no nudity, never in profile/header. Sensitive flag comes from the X account default (Ayrshare can't set it). No Fanvue links for Gabriela anywhere |
| Posting time zone | ET (America/New_York; Miami-based persona; all handoffs and logs use ET). Specific slot times: set by the JSW Content Scheduler, TBD here |
| Engagement profile | AdsPower profile k1cwwmho ("profile 5"), headless, attach only; never touch proxies |
| Secrets (paths only) | Ayrshare/X consumer keys: secrets/JSW-x-ayrshare-consumer-keys.json; AdsPower: secrets/adspower-api-key.txt (secrets folders on the box: /home/box/agent-data/secrets, /home/box/sand-data/secrets). Never print values |

## Exceptions vs VALENTINA_PIPELINE.md (real differences only)
1. Facebook is locked and under appeal: skip FB in every posting/scheduling step.
2. The album release card says "coming soon" until "Brisa de Miami" is live (Apple link TBD); captions also stay on "coming soon" (no Apple link yet). Card design/text/duration: TBD (no build script for it found on the box).
3. X posts get the sensitive-media flag from the X account default setting ("mark media you post as containing sensitive material"), because Ayrshare can't set it per post.

## Other per-model notes (prompt settings, not pipeline changes)
- Hair: Gabriela keeps a high ponytail (locked body line); Valentina's "hair down, no ponytail" rule does not apply.
- Use Gabriela's locked body+hair line and deep golden-bronze tan; never write "light green-hazel eyes" (caused the light-eye drift).

## Conflict to resolve before scripting
- jsw-gabriela-content/SKILL.md §6 says "no nudity only on X marked sensitive"; the parent instruction for this row says "spicy allowed on X only, no nudity". This row follows "no nudity"; JSW AI should confirm and update the skill.
