# Camille music-video test, week of Oct 19-25, 2026 (DRAFT, nothing generated, 0 credits spent)

## Song
**02 Champagne Sur la Plage** (Single 1, 122 BPM, disco strings, euphoric). It's the lead single and matches this week's French Riviera story.
Audio: camille_02_champagne_sur_la_plage.mp3 (clean, 3:29). Same file in Drive: JSW Content/Camille/04 Music. Master: /workspace/music/distrokid/camille/02_champagne_sur_la_plage.wav. The explicit "Sur le Yacht" is NOT used (X only, marked sensitive).

## Hook line (first chorus, lyrics from /workspace/music/distrokid/camille/release.md)
> Champagne sur la plage / Dancing in the sun, no age / Glitter on my shoulders, sand on my feet / Champagne sur la plage, so sweet

The lip-sync uses the first two lines ("Champagne sur la plage / Dancing in the sun, no age", about 4-5 s at 122 BPM) plus lines 3-4 if the take holds. TODO: find the chorus start time by ear or with whisper (faster-whisper isn't in .lipsync-venv right now). Cut the audio so the "Pop, pop, the corks go high" pre-chorus ends exactly at 0.0-1.0 s, which puts the first "Champagne" on the downbeat at about 1 s.

## Scene (mood: sunny, glamorous, playful beach club)
Saint-Tropez/Pampelonne-style beach club in late-afternoon gold light: a row of white umbrellas, sea behind her, champagne coupe in hand, light linen or white swim cover-up, a little glitter on her shoulders. Keep the background simple (plain sand, umbrellas, sea): busy railings and flowers melt in video.

## Shots (target 12-13 s, 9:16)
1. **0-1.5 s HOOK OPENER (virality first 1-2 s):** close-mid shot. Camille lifts the coupe to the lens on "Pop, pop, the corks go high", the bubbles catch the sun, and she's already moving to the beat in frame 1. Lyric text "Champagne sur la plage" in the top band from 0.0 s. No fade-in. (Kling 3.0 + Element, 5 s, sound off, cut to 1.5 s.)
2. **1.5-9.5 s LIP-SYNC:** chest/waist-up, eyes on camera, singing the hook lines (Seedance 2.0 i2v, 8 s, with the song's vocal stem/section as audio_reference).
3. **9.5-12.5 s OUTRO BEAT:** wider shot, a small sway or dance step with the coupe raised, sea behind her; hard cut on a beat into a loop back to shot 1. (Kling, 5 s, cut to 3 s.) Optional freeze-frame on the last beat (free, see the SHARED_LEARNINGS Madison freeze note).

## Recipe (adapted from the "Valentina LIP-SYNC RECIPE", SHARED_LEARNINGS.md line 833, plus VALENTINA_PIPELINE.md)
1. **Stills (Seedream 5.0 Pro, 2.5 cr each, 3:4 2k):** a single-ref edit of an approved Camille still (current approved pack in identity_packs.json `camille`, v3b/v8 sheet) into the beach-club scene. Use the pipeline's "keep face identical" edit tail, the unretouched skin block, and "skin stays dry and matte". For the lip-sync start frame, use the passing pack's natural smile (not a smirk, which narrows the face). Make 3 stills (opener, lip-sync start, outro) plus up to 3 rerolls.
2. **GATE stills:** identity_gate.py face at 0.78 or higher (aim for .85+ on the Seedance start still) and body_check.py vs the Camille body spec. No video until both pass.
3. **Audio for Seedance:** cut the exact 8 s hook section from the clean mp3 (ffmpeg -ss <chorus_start-0.2> -t 8). Ideally isolate the vocal (demucs) so the reference is mostly voice. Upload via media_upload -> curl PUT (If-None-Match: *) -> media_confirm, with image and audio confirmed separately.
4. **Lip-sync (Seedance 2.0 i2v, `seedance_2_0`, 720p 9:16 8 s, about 36 cr; run get_cost first):** start_image = the gated still used as-is, audio_references = the hook clip. Prompt: low motion, phone camera held still, eyes on camera, natural blinks, "she begins singing immediately in the first second, mouth moving in sync with the sung lyrics, finishes by about 7.5 seconds", gentle sway to a 122 BPM beat, "skin stays dry and matte, no shine, no glow", no other people, no text. Don't describe face or body. Avoid the "in the dark" and "looks at the viewer and says" phrasing.
5. **Opener and outro (Kling 3.0 + the Camille Element, 5 s sound off, about 7.5-8.75 cr each):** low motion, no laugh, no blown kiss, keep the hands away from the face.
6. **QC:** whisper the lip-sync audio against the lyric (sung words are looser than speech, so check that mouth shapes land on "Cham-pagne"/"plage" by eye at 0.5x). Gate the raw frames at 10 fps at 0.78, then gate every export frame again. Check mid AND late frames against the approved sheet.
7. **Finish:** replace the Seedance audio with the ORIGINAL clean song section, sample-aligned to the generated mouth (offset check), so the master audio is the real track. Scale aspect-preserving (no stretch). Text in the top/bottom band only. H.264 Main yuv420p faststart, under 15 MB. Re-gate the export.
8. **Reviewer:** submit to the JSW Content Reviewer (it runs the Higgsfield virality predictor, so the first 1.5 s must already show the hook). Post only after a PASS.

## Credit estimate (Higgsfield)
- Stills: 3 + 3 rerolls x 2.5 = 7.5-15
- Seedance lip-sync: 1 take 36, plus 1 retake 36 = 36-72
- Kling opener and outro: 2 x ~8 = 16, plus 1 redo = up to 24
- **Total: about 60 cr best case, about 110 cr with retakes.** Run get_cost preflight before every job.
