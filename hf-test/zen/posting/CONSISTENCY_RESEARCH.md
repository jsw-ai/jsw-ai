# Consistent face+body across ALL photos and videos on Higgsfield — research (2026-10-18)
Research only: 0 credits spent, nothing trained/posted. Only read calls (elements list, show_characters list, models_explore, apps_search, generate_video get_cost preflight) + web search of higgsfield.ai help/blog.
Short answer: Higgsfield has NO single "train once, locked face+body for every photo and video" feature. Soul ID is face-centric, image-only (Soul 2/Cinema), one person per gen. Everything else is "anchor to reference images each generation". Our current Seedream ref-edit -> Seedance i2v pipeline is the closest, and is what the docs recommend as the video path, but it has drift in the video step (face narrower/hollow, bust bigger) and in body on slim outfits.

## 1. Already tried (per SHARED_LEARNINGS / MODEL_CONTENT_PROCESS / EXPERT_GUIDE)
| Approach | Result |
|---|---|
| Soul ID trained character + Soul 2.0 (all 7 bots have Souls; Sienna "Body v1") | Face ok (~83% gate, lock-test 1-5 approved for Sienna) but body drifts; retrain set only 3/36 passed gate; Soul ignores clothing prompts. |
| Seedream 5.0 Pro ref-edit (face ref + body ref, 3:4 2k, 2.5 cr) | Current workhorse. Face gate passes often, body/bust drifts on slim outfits unless wording "very full large rounded bust..." + scoop tops; Sam rejected ALL for Sienna. Madison/Camille/Valentina packs approved with fixes. |
| Nano Banana Pro ref-edit | 0/3 gate, different face. GPT Image: blocks swimwear refs. |
| Seedance 2.0 i2v: start_image + audio_references (lipsync, dance) | Works (36 cr / 8 s 720p) but audit found face drift (narrower/longer face, hollow cheeks, bigger bust vs refs), HF skin detail lost, sheen added. |
| Local finishers (v4C/v5), identity gate, deglossing | Post-fixes only. |
| Face Swap (Zen faceswap) | Never run (tool not available). |
| Elements (manage_reference_elements) | 7 Elements exist (one per bot, each ONE image; Sienna Body v1 etc.) but NO log of ever generating with `<<<element_id>>>` or `image_references`. |

## 2. Features that lock identity (face/body, images/video) and status
| # | Feature | Locks | Image/Video | Tried? | Notes / cost |
|---|---|---|---|---|---|
| 1 | Soul ID (show_characters, 5-20 imgs) | face (some body w/ full-body shots) | image only (Soul 2/Cinema); video only via Element from a Soul still | YES | Not exportable, 1 person/gen. Train cost ~25-40 cr. |
| 2 | Seedream/NBP/GPT ref-edit with face+body refs | face+body | image | YES | 2.5 cr/img |
| 3 | Elements `<<<uuid>>>` in generate_image/video (NBP, GPT Image 2, Seedream 4.5/5-lite, Cinema Studio img 2.5/vid 2/3.0/4.0, Seedance 2.0, Kling 3.0 [needs start_image]) | face (+ body if element image is full-body) | both, reused across gens | NO | Free-ish to create (not verified: do not create without OK); existing Elements are single face/body crops. Note Seedream 5.0 *Pro* (our model) is NOT in the Element list; Seedream 4.5 / 5-lite are. |
| 4 | Seedance 2.0 / 2.5 / Wan 3.0 / MiniMax H3 `image_references` (Seedance 2.0 up to 9 imgs, 3 video, 3 audio; 2.5 up to 30 imgs) alongside start_image | face+body per clip | video | NO (only start_image + audio used) | HF blog advice: one clean full-body front/back ref + ONE frontal face close-up; avoid multi-face sheets. Seedance 2.0 720p 5s = 22.5 cr (preflight), 2.5 omni 720p 5s = 35 cr. |
| 5 | Kling 3.0 Motion Control (`motion_control`: character still + driving video, 720p/1080p, scene_control image|video) | face+body come from the STILL; motion from driver | video | NO | Build the video from our approved still, so identity = still. Driver build/proportions can leak (Recast guide: match proportions). No get_cost param; est ~8-12 cr per 5 s [3P ~12 cr/5s 1080p]. |
| 6 | Genjutsu `hf_mult_motion_control` / `hf_mult_replace_object` via generate_video (source video 4-30 s + up to 30 ref photos, 480/720/1080p) | swaps character in existing footage with refs (fixes drifted clips, repeat a performance) | video | NO | Priced by source duration (cannot quote without a video). API list ~$0.32/s 480p, $0.68/s 720p -> est ~35-70 cr for 5 s 480p-720p [3P, unverified]. |
| 7 | Recast / Character Swap 2.0 (app) | whole persona incl. body+motion into any video | video, photo | NO (not exposed in MCP apps; apps_search only returns Match Cut + Tracelab) | 5-15 s clips; one person, frontal, proportion-matched. |
| 8 | Kling 3.0 Omni Edit (`kling_video_edit`, video_references + image_references) | edit/fix identity in a source video | video | NO | cost unquoted |
| 9 | Kling 3.0 multi-shot storyboard w/ start_image | identity across cuts in one gen | video | NO | 7.5 cr for 5 s std silent (preflight) |
| 10 | build_ai_influencer / Soul Cast (3-view character sheet: full-body front, back, face close-up) | face+body design sheet, no training | image; sheet feeds Elements/refs | NO | Meant for invented characters; could produce a front/back/face sheet from an approved still. Cost unquoted (ai_influencer_prepare not run). |
| 11 | Marketing Studio Reference Video (`marketing_studio_v2_reference2video`: input_video + character_image) | recreate a ref video w/ our character | video | NO | ad-oriented, cost unquoted |
| 12 | Wan 2.7 / Wan 3.0 / Gemini Omni "character-consistent" | claims | video | Wan T1_wan_b used once (Sienna) | not systematically tested |
| 13 | Face swap (photo/video) | face only | both | NO | looks pasted; last-resort rescue |
| 14 | Voice: separate from identity (Voices); we already lock via audio_references mp3 | voice | - | YES | |

## 3. Recommended tests (ONE small test each; await Samuel's OK before any spend)
### Test A — Seedance 2.0 with reference stack (face + full-body) on the approved start frame
- Why: only untried path that adds body info INSIDE the video model; matches HF's own "full-body + one face close-up" recipe; tests the exact weak spot (bust grows, face narrows in i2v).
- Setup (Madison, Look A): start_image = approved still; image_references = madison_face_keeper (1600px) + madison_body_keeper; prompt names roles ("@image2 face and identity, @image3 body proportions exactly, keep bust/hips as photo 3, matte skin"); 5 s, 720p, 9:16, generate_audio false.
- Cost: 22.5 cr exact (preflight). Add a same-still no-ref control only if Sam wants an A/B: +22.5 (total 45). Compare face gate + bust/hip eyeball vs the existing start-frame-only clip (0 extra cost, already have it).
- Optional variant: same via Element placeholder `<<<6329d3da-...>>>` (Madison Cole element, 1 image) instead of refs.

### Test B — Kling 3.0 Motion Control from approved full-body still + one of our own approved clips as the driver
- Why: video identity comes from the still itself (no re-interpretation of face/body), so any approved photo can become a video; driver can be an approved Seedance dance clip or a stock/own phone clip with a similar build.
- Setup: image_id = approved Madison full-body still (media_upload/PUT/media_confirm), motion_video_id = ~5 s driver, 720p, scene_control=image.
- Cost: est 8-12 cr (no preflight param; 3P ~12 cr/5 s at 1080p, 720p cheaper). Risk: swimwear/skin NSFW filter on Kling (flagged runs refunded), driver body shape can leak.
- If B wins: next step is Genjutsu replace_object (est 35-70 cr/5 s) to repair already-approved drifted clips.

Total for both: ~31-35 cr. Not recommended now: new Soul retrain (history: 3/36), face swap, Recast (not reachable via MCP).

## 4. Caveats
- Costs for 5, 9, 10 are estimates; Genjutsu/motion-control need a source video to preflight.
- Elements here are 1 image each; docs say Seedream 5.0 Pro (ours) is not Element-compatible (Seedream 4.5/5-lite are).
- Sources: higgsfield.ai help-center how-do-i-use-seedance; blog generating-with-seedance-2-0; geo.higgsfield.ai Soul ID video consistency; blog keep-ai-character-consistent (Genjutsu); blog AI-Face-Character-Swap PRO guide; apps/recast; blog case4k (3-view sheet). MCP schemas: manage_reference_elements, show_characters, motion_control, generate_video, models_explore.
