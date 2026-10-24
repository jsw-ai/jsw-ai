> Notion is the source of truth: https://app.notion.com/p/400f29949b29810fbe39cbcde5d3d9f4. If this file conflicts, Notion wins.

# Talking lip-sync clips: method for the JSW model bots
For Sienna, Camille, Charlotte, Madison, Gabriela, Valentina. Compiled 2026-10-15 from existing box files. **No clips were generated and no credits were spent to write this.**
Sources: `CONTENT_RECIPE.md` §3-6, `HIGGSFIELD_EXPERT_GUIDE.md` §5-7, `MODEL_CONTENT_PROCESS.md`, `voicerefs-*/MANIFEST.txt`, `api_notes.md`, the Aug-Oct build transcripts (talking1-4 clips) and the `generate_talking_head` tool schema.

## 0. Hard rules (read first)
1. Model bots make files only. A JSW Content Reviewer PASS on the exact file (path + md5) and exact captions is the approval; only the JSW Content Scheduler posts (Ayrshare). (Updated 10/21 to match Hard Rules.)
2. **No AI mention** in captions, hashtags, hooks, on-screen text or the spoken line. The platform "AI-generated / AI info / synthetic content" toggles stay ON as settings only.
3. **No background people.** Use plain or empty backgrounds (balcony, wall, empty path). Frozen extras look fake in video.
4. Get Samuel's OK on the credit estimate before each run. Never buy credits or enable auto top-up. No Fanvue links or NSFW on SFW platforms.
5. Retired, never post: old glossy clips such as `videos/sienna_talking1_web.mp4` (Sam rejected it as looking AI). Check the retired list before reusing any old `videos/*_talking*.mp4`.

## 1. Tool and settings that worked (the standard method)
**Higgsfield MCP (`user-Higgsfield`), model `seedance_2_0`, image-to-video with native audio.** Never text-to-video.
| Setting | Value |
|---|---|
| `start_image` | the approved, gated still (see §3) |
| `audio_references` | the model's locked voice mp3 (§2), imported fresh for each clip |
| `generate_audio` | on |
| aspect ratio / resolution | 9:16 / 720p (1080p costs about 2x) |
| duration | 8 s was the proven length (talking1-4 clips are 720x1280, ~8.06 s, h264 + aac) |
Prompt pattern (from `CONTENT_RECIPE.md`): she speaks the exact line to camera, slight handheld phone drift, natural blinks, small natural head movement, keep same face and body/outfit 100% consistent with the first frame, no other people, no on-screen text. Add the accent in the prompt: Sienna Australian, Charlotte British, Madison American, Camille French, Valentina Miami Latina, Gabriela Miami Latina (from the persona video config).
Flow per clip: serve the mp3 over https, then `media_import_url` (or `media_upload`) to get a temporary media_id, then `media_confirm`, then pass it as the audio reference. **Media IDs are temporary. Re-import every time.** Poll with `jobs_wait`, download, and check codec with ffprobe.
Fallback tools (not proven here):
- Legacy API `user-higgsfield-api generate_talking_head` (Speak v2): image_url + audio_url (**must be WAV, so convert the mp3**), prompt, quality high|mid, duration **5, 10 or 15 s only**, seed, ~2-3 min. **No record of it ever being used for a JSW clip** (see §8).
- The Seedance REST paths (`platform.higgsfield.ai/bytedance/seedance-2.0/*`) returned `model_disabled` / `model_blocked` on 2026-08-26. Use the MCP route, not REST.
- Zen `lipsync` is 3 cr per second of audio, max 35 s, and was never tested. Other Higgsfield lipsync models (Kling Lipsync, Wan Speak, Veo 3.1, Higgsfield Speak 2.0) are listed in the Expert Guide, but only as research.

## 2. Locked voices (do not change, do not substitute presets)
Do **not** use the built-in preset named "Sienna". Voices are mp3 reference samples, not cloned into Higgsfield. A Soul ID does not bind a voice.
| Model | Accent / sample line | Working copy on box | length |
|---|---|---|---|
| Sienna | Australian ("heaps cooked" / Messi) | `/workspace/hf-test/voicerefs-from-sam/sienna.mp3` | 8.1 s |
| Charlotte | British ("what England does to us") | `.../voicerefs-from-sam/charlotte.mp3` | 8.1 s |
| Madison | American ("World Cup is in America") | `.../voicerefs-from-sam/madison.mp3` | 5.1 s |
| Camille | French-coded ("it is just beautiful") | `.../voicerefs-from-sam/camille.mp3` | 8.1 s |
| Valentina | Miami ("the entire bar exploded") | `.../voicerefs-from-sam/valentina.mp3` | 8.1 s |
| Gabriela | soccer play-by-play | `.../voicerefs-from-sam/gabriela.mp3` | 8.1 s |
- Copies: `/workspace/hf-test/voicerefs-backup/` and `/workspace/hf-test/jsw-voicerefs-backup.zip` (backup dated 2026-08-29). Upstream source of truth: droplet `206.81.3.238:/opt/jsw-ai/content/voicerefs/<slug>.mp3`.
- Verified 2026-10-15: the md5 of the six `voicerefs-from-sam` files matches the MANIFEST and the backup. Never edit these files; work on copies.
- Unlabelled UUID-named mp3s sit in `/workspace/hf-test/voices/`. Those are the raw audio-library copies, so use the slug-named files instead.

## 3. Input image rules
- Start frame = a still that passed `identity_gate.py` at 0.78 (face + body). Never raw or ungated output.
- **Not a mid-smile or mid-speech frame.** Use a neutral, soft or closed-mouth expression, or a clearly intentional one. Mid-smile frames make teeth and mouth drift when the model starts talking.
- **Vary the expression between clips** (soft smile, smirk, neutral, small laugh), so the feed is not the same face every time. See `valentina_batch2` for a set of varied-expression stills.
- Face fully in frame with headroom, waist-up or tighter, front or 3/4 angle, face not tiny. Face drift is worst at small face size.
- Plain background, no other people, no text or logos, ordinary clothes. For stills that show the body, run the body check too.
- Finish the still before animating (skin texture; no blur). Add light grain and mild sharpening to the clip afterwards.

## 4. Script rules
- Spoken line fits **8-25 s** of speech, written in the model's own voice and accent, with no AI mention.
- One Seedance clip is limited to about 4-15 s. The tested length is 8 s. **Plan 8-15 s per clip.** For 15-25 s, cut two clips on a natural pause and edit them together. That two-clip route is not tested here (§8).
- Write the exact words in the prompt and keep them short (about 2.5 words per second). Also keep a copy of the line for the transcript check.
- Generation takes a few minutes. Don't batch more clips than the approved credit cap.

## 5. Credit cost per clip (confirm with the cost/estimate option before running)
- Seedance 2.0, 8 s, 720p, audio on: **~36 credits per clip** (`CONTENT_RECIPE.md`). The Expert Guide figure is ~22 credits per 5 s at 720p, which scales to about 35.
- 1080p is about 45 credits per 5 s, so don't use it. Seedance Fast is ~17 per 5 s but is untested for lip-sync.
- Still keepers cost ~2.5 credits (Seedream 5.0 Pro), so fix the still first. A clip reroll costs ~36 credits.
- `generate_talking_head`: its cost is not documented on the box. Check the estimate first.

## 6. Checks before showing Samuel (each clip)
1. **Speech:** transcribe with faster-whisper (`/workspace/.whisper-venv`). It must match the line word for word, with no gibberish and no wrong language.
2. **Accent / voice:** the voice must sound like the model's reference mp3 (Australian, British, American, French-coded, Miami). Listen to the reference and the clip back to back. Wrong accent or a different voice = reroll.
3. **Lip-sync:** watch the first, middle and last second. The mouth must follow the words and not drift, with teeth and lips staying natural.
4. **Identity / body:** run `identity_gate.py video --model <slug> clip.mp4 --frames 8` (at least 85% of frames pass). Compare the face to the keeper side by side. Check that body and outfit don't morph.
5. **Scene:** no background people or frozen extras, no garbled text or logos, no extra fingers, and props match the line.
6. **Finish:** light grain and mild sharpening only (**no blur**), re-encode H.264/AAC, `-map_metadata -1`. Check it on a phone-size screen.
7. **No AI wording** in the caption draft, hashtags, on-screen text or spoken line.

## 7. Handoff
Save under `/workspace/hf-test/posting_<date>/<model>/` (clip, still, transcript, gate result). Record the credits spent in `SHARED_LEARNINGS.md`. Submit the file path + md5, captions, spoken line, transition, credit count and check results to the JSW Content Reviewer. A JSW Content Reviewer PASS on the exact file (path + md5) and exact captions is the approval; only the JSW Content Scheduler posts (Ayrshare). (Updated 10/21 to match Hard Rules.)

## 8. Could not verify (open items)
- `generate_talking_head` has no record of use on the box. The tool schema says WAV only and 5/10/15 s. Whether it is better than Seedance for these personas is unknown.
- **The exact working Seedance call** (full prompt text and parameters) for talking1-4 comes from a recipe and transcripts, not from a saved job file. The settings above are the documented recipe. The ~36 credit cost is a recipe figure, not read from the transaction log.
- Seedance's maximum clip length is ~15 s (CLI notes say ~4-15). The 15-25 s case needs a two-clip stitch, which was not tested.
- The "non-mid-smile" and "varied expression" rules are Samuel's brief; I found no older file that records a test of them.
- Madison's voice sample is only 5.1 s, so the other voices have more sample than hers.
- The `talking4` clips (Camille, Gabriela) are the ones Sam approved. I found no file or transcript for `v2`/`v3` talking clips beyond the numbered talking1-4 and collab v1-v3 videos.
- Some persona bios in older transcripts say "Openly AI". That conflicts with rule 2 for post content. Follow rule 2 until Samuel says otherwise.
