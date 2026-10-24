# Higgsfield Full Audit (2026-10-21, ET)
Sources: live MCP schemas (user-Higgsfield, user-higgsfield-api), live catalogs (get_presets viral=87, soul styles=33, genjutsu, apps_search), cost preflights. Balance at start 9555 cr (Ultra, shared). This audit spent ~1.1 cr (2 tests). Nothing trained, bought or posted.
Note: the namespace listing returned ~150 named tools (incl. 3D Jutsu, websites, projects, billing, TikTok publish); all relevant ones are covered below.

## 1. What we use now
Seedream 5.0 Pro ref-edit (2.5 cr, best face+body), Kling 3.0 elements, Seedance 2.0 i2v + audio_references lip-sync (36 cr 720p/8s, 96 at 1080p), Soul 2 + trained soul_id (Sienna face/body), outpaint_image (2 cr), virality_predictor, local ffmpeg finishing + identity_gate.py.

## 2. Feature map (what / MCP tool / cost / face-consistent / SFW-safe)
| Feature | MCP tool | Cost | Takes our face refs? | SFW platforms |
|---|---|---|---|---|
| Viral effect presets (87: boarding pass, 2000's paparazzi, Superstar, Clones, Selfie twin, Frozen in motion, Earth zoom, Orbit 360, Race track, Scrapbook collage, Action figure, Sticker peel, Vanish...) | get_presets source=viral -> execute_preset | not quoted in schema; video chains, est. 20-60 cr (check widget price) | Yes: 1 input image (our gated still) | Yes (fun/surreal, no nudity) |
| Genjutsu motion transfer / dance templates | generate_video model=hf_mult_motion_control (+ trending gallery) ; legacy motion_control (Kling 3.0) | priced per driving-video second (needs upload to quote) | Yes: image role = our still | Yes if driving video is clean; use our own/licensed driving clips |
| Character/object/outfit swap in a video | generate_video model=hf_mult_replace_object | per second | Yes (ref images) | Yes; never swap onto real people's footage |
| Face swap (photo/video) | NOT exposed in MCP; nearest = Seedream ref-edit / replace_object | - | - | Skip (impersonation risk) |
| Soul 2 + soul_id + curated style (33: Disposable camera, Old smartphone, Digital camera, Subtle flash, Y2K street, Flash editorial, Warm vivid film...) | generate_image soul_2 style_id+soul_id | 0.12 cr | Sienna only (trained) | Yes |
| Reference Elements (instant 1-image character) | manage_reference_elements create, <<<id>>> in prompt; nano_banana_pro/2, gpt_image_2, seedream_v4_5/v5_lite, cinematic_studio, seedance_2_0, kling3_0 | free to create; seedream_v5_lite 1 cr | Yes (1 image) | Yes |
| Talking head / Speak v2 | user-higgsfield-api generate_talking_head (WAV) ; Seedance audio_references (preferred) | n/a / 36 | Yes | Yes |
| Voice clone + TTS | create_voice_from_confirmed_audio, generate_audio seed_audio voice_type=element | small (clone charge once) | locked voice | Yes |
| Dubbing (18 languages, lip-synced) | dubbing | per video | keeps face | Yes |
| Voice change | voice_change | per video | - | Yes |
| UGC / ad templates | marketing_studio_video, show_marketing_studio_v2, ads_studio_* | 20-100+ | avatar/custom | Yes; brand-deal use only |
| Shorts Studio (restyle a source video into clips) | shorts_studio_create (+get_cost) | per second | partial (restyle) | Yes |
| Popcorn / storyboard / multi-shot | kling3_0 multi-shot, cinematic_studio_3_0, seedance_2_5 | 30-100 | Elements | Yes |
| Upscalers | upscale_image (bytedance 2k/4k), upscale_video (bytedance/topaz) | flat small | keeps | Yes (watch gate scale artifact) |
| Reframe video / outpaint | reframe, outpaint_image | ~2 / per sec | repaints face slightly | Yes |
| Background removal | remove_background (img/video) | small | keeps | Yes (green-screen comedy bits) |
| Match Cut + Tracelab app (facecut, retropop, VHS, Nokia, CRT, thermal, scrapboard, wordstack, commentcut, typewriter) | apps_search/apps_describe/apps_invoke | per render | uses our footage | Yes |
| Video analysis (scene-by-scene, YouTube URL) | video_analysis_create | low | - | trend-remix research |
| Virality predictor | virality_predictor | low | - | already used |
| AI Influencer builder / character sheets | build_ai_influencer | per sheet | 1 identity ref | not needed (we have identities) |
| TikTok publish + trending licensed music | tiktok_connect/prepare_publish, tiktok_music_trending | free | - | needs account connect (none yet) |
| 3D Jutsu, websites, Katana | scene_builder_3d_*, create_website, get_katana_config | - | - | skip |

## 3. Top 10 to adopt (ranked by engagement impact)
1. **Viral presets via execute_preset** (boarding pass, 2000's paparazzi, Superstar, Selfie twin, Clones, Frozen in motion, Earth zoom). Scroll-stopping hooks with our gated still as the only input. Ideas: Sienna boarding pass Bali->Byron->Hawaii surf looks; Camille paparazzi exiting a Paris hotel; Charlotte Superstar jumbotron at an Emirates-style stadium (no real club marks); Madison Clones in the gym; Gabriela Earth zoom into Miami Beach; Valentina Selfie twin at a Buenos Aires cafe. Cost: quote in widget first (est. 20-60).
2. **Genjutsu motion transfer (hf_mult_motion_control)** for trend dances/walks from a clean driving clip, our still as identity. One per model per week on the week's trending sound. Per-second pricing; preflight with the uploaded clip.
3. **Soul 2 curated styles (0.12 cr)**: Disposable camera / Old smartphone / Digital camera / Subtle flash = the "photo dump" look that wins on IG carousels. Tested: PASS .831. Sienna now; others need a trained Soul (training not done in this audit).
4. **Reference Elements** for instant identity on nano_banana_pro / seedream / seedance / kling3_0 for all six models (no training). Tested: face recognisable but gate .75 (fail at .78 Seedream bar); good for drafts and multi-character shots (two models in one frame: collabs!). Use Seedream 5.0 Pro 2-ref edit for finals.
5. **Locked voice + seed_audio TTS + Seedance lip-sync** for talking hooks; **dubbing** into Spanish/Portuguese/Italian/French for Gabriela, Valentina, Camille cross-posts (doubles reach per asset).
6. **Match Cut + Tracelab app**: retropop/VHS/Nokia/CRT/commentcut overlays on existing clips (cheap re-use of approved footage).
7. **Shorts Studio** restyle of a single approved clip into several variants (A/B hooks).
8. **upscale_video (topaz 1080p)** on 720p Seedance/Kling finals before posting (run gate on the original, not the upscale).
9. **remove_background (video)** for green-screen reaction bits (Charlotte Arsenal reactions over a scoreline card).
10. **tiktok_music_trending + tiktok_prepare_publish** once accounts connect: licensed trending sounds = algorithm boost. Needs Samuel to connect TikTok.

## 4. Skip and why
Face swap onto real people/footage (impersonation, platform bans); AI Influencer builder (we already have identities); Marketing/Ads Studio (only for brand deals); 3D Jutsu, websites, Katana (no engagement value now); sonilo/mirelo music (game-pipeline only, not allowed); user-higgsfield-api old Soul/DoP/Kling 2.1 (superseded; create_character costs 40 cr); Wan lip-sync (failed gate before); NSFW-leaning presets (Melting, Vanish clothes collapse = suggestive risk).

## 5. Tests (1.12 cr total)
- T1 soul_2 + Sienna soul_id ba97f512 + style Disposable camera (0.12 cr): identity_gate PASS centroid .831 / best .795; body unmeasurable (shirt). By eye: Sienna, natural film look, beach bar. Note bust/cleavage reads stronger than SFW-safe-for-video; fine for IG still.
- T2 Element "Sienna-Blake-face" (9de8b3e5-6561-41b8-b105-b16b0ad9b0f3, from story1_a_v4C) + seedream_v5_lite first-class cabin (1 cr): gate FAIL centroid .75 (best .805), body pass. By eye: close, slightly younger/rounder, braids. Drafts only.
- Viral preset execution NOT tested (no cost quote available pre-submit; likely >10 cr cap).
Files: hf_audit_1021/{soul2_disposable.png, element_seedream_lite.png, sheet.jpg, clip_sample_10s.mp4}.
