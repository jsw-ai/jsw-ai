Here is the result of "fetch" for the Page with URL https://app.notion.com/p/400f29949b298195aa8ac98f2e306717 as of 2026-10-21T15:39:18.890Z:
<page url="https://app.notion.com/p/400f29949b298195aa8ac98f2e306717">
<ancestor-path>
<parent-page url="https://app.notion.com/p/3d5f29949b298167a5efc5920f09f973" title="JSW AI"/>
<ancestor-2-page url="https://app.notion.com/p/3d5f29949b2981de934ce8472408dfdd" title="Brixmont Operations Hub"/>
</ancestor-path>
<properties>
{"title":"SOP: Sienna creation process"}
</properties>
<iconMetadata>null</iconMetadata>
<content>
Scope: the creation part of Sienna's day (Australian surfer and singer, Gold Coast then Bali), from the weekly story to handing finished files to the JSW Content Reviewer. Every step comes from these sources: VALENTINA\_[PIPELINE.md](http://PIPELINE.md), finish\_[v4C.py](http://v4C.py), /workspace/jsw\_tiktok/sienna/ (SIENNA\_LOCKED\_BODY\_LINE.txt, sienna\_v4C\_reference\_sheet.jpg, the 2026-10-21 [NOTES.md](http://NOTES.md)), the jsw-daily-content-process skill, FANVUE\_ACADEMY\_[PLAYBOOK.md](http://PLAYBOOK.md), and the Notion pages "Sienna – Week of Oct 19" and "Fanvue first-payout push plan".

## Hard rules (apply to every step)

- Use only approved v4C photos of Sienna as references and start frames. Light on the face is even and from the front: no sunset light, side light or golden-hour backlight on the face.
- Paste the locked body and hair line from /workspace/jsw\_tiktok/sienna/SIENNA\_LOCKED\_BODY\_LINE.txt word for word into every image prompt and every video prompt.
- Content is sexy but SFW and shows an exciting life. Never generic walking around.
- Never mention AI and never deny it. Apply each platform's AI label.
- TikTok, IG, YT and FB stay clean: no Fanvue, no spicy content, no swearing.
- X: short clips are the core, with photos mixed in. Teases are X-only, posted with sensitive media on, can swear, and carry no URL ("link in bio"). The Fanvue link goes only in the X bio, in a pinned post set by hand, and on Reddit.
- Never touch /workspace/music/sienna/low\_tide\_lover/out/sienna\_low\_tide\_lover\_SAMPLE\_flow\_[v5b.mp](http://v5b.mp)4.
- AdsPower is headless only, and is not used at all while Samuel's freeze is on.
- The bot never posts. A Reviewer PASS means approval to schedule, and the JSW Content Scheduler schedules.
- Cadence: 1 to 2 new clips a day, each with 2 to 3 recut hooks. X gets 4 to 6 posts a day, at least half of them teases.

## Steps

1. Read the weekly story. Open the current "Sienna – Week of …" page under Weekly Content Research and pick today's beat (week of Oct 19: Gold Coast Mon-Tue, Low Tide Lover teaser Tue evening, song drop Wed, first-class flight to Bali Thu, Bali Fri-Sat, acoustic beach-bar gig plus recap Sun). Take the hook, format, sound, setting, outfit and caption idea for today's video, and today's X lines.
2. Research live. Check public X trends and what is driving reach on each platform. Live-search to confirm any real event before you use it, and do it before generating video, because spoken or sung lines get baked in. Never invent an event. Check every sound in TikTok's commercial library before you use it.
3. Write the plan for each clip: the scene, the 2 to 3 recut hooks, the target platforms (cutA TikTok, cutB IG, cutC Shorts, cutD FB, plus any X version), the captions per platform, and the X posts for the day (4 to 6, at least half teases).
4. Check the plan before generating, against (a) the export spec in step 13, which means framing that works as full 9:16 with no blurred bands, and (b) the weekly story. Also check it against the hard rules: sexy but SFW, an exciting life rather than walking around, clean versions for TikTok/IG/YT/FB, X-only teases with no URL, and no outfit or wording that moderation blocks (bikini or cleavage start frames, "bare midriff/minimal fabric/tiny" wording). Rewrite anything that fails before you spend credits.
5. Pick the references: approved v4C finals of Sienna only (for example story1\_a\_v4C / story2\_a\_v4C), with sienna\_v4C\_reference\_sheet.jpg as the body and hair standard. Prefer mid framings (waist-up to mid-thigh). Keep hair down or in her locked styles, no ponytail. Use empty scenes, because busy public places leak background people.
6. Upload the references to Higgsfield (user-Higgsfield): media\_upload, then a curl PUT to the presigned URL with Content-Type and If-None-Match: \*, then media\_confirm. If a PUT returns a transient 520, retry the same URL. Media ids stay valid across calls.
7. Generate the stills: generate\_image, model seedream\_v5\_pro, resolution 2k, the refs as image\_references in order. Prompt = scene + the locked body and hair line pasted word for word + the skin/face tail (unretouched phone photo, matte dry skin, visible pores, no shine or glow, no airbrushing, faint freckles, even front light on the face, eyes open looking into the camera, soft closed-mouth smile, no other people, no tattoos). For a new outfit or setting, prefer a single-ref "Edit this exact photo" pass over an approved final. Quote the cost first (2.5 cr per image) and log every job id, including redos.
8. Finish every still with finish\_[v4C.py](http://v4C.py) (copy it from /workspace/jsw\_tiktok/sienna/2026-10-21/finish\_[v4C.py](http://v4C.py) and repoint P to today's folder). It reads raw/\<name>.png and writes fin/\<name>\_v4C.jpg: skin\_[local.py](http://local.py) texture source, resize to 1080 wide, texture transfer at 0.5, sharpen 0.3, grain sigma 3, JPEG q90. Do not use finish\_v5.
9. Face gate each still: /workspace/.face-venv/bin/python identity\_[gate.py](http://gate.py) --source seedream --body, 0.78 cut on the centroid. Treat ±0.01 around 0.78 as borderline. A score alone is not a pass: also look at the face (jaw and cheek width, eyes, nose, lips) and the body and hair against sienna\_v4C\_reference\_sheet.jpg. Only gated stills go on to video. Identity in video is set by the start still.
10. Generate the video: Kling 3.0 (kling3\_0) with the Element Sienna-v2-1020 (2603afeb-5f21-4acc-a3de-8904d5a32cb9), written as \<\<\<2603afeb-5f21-4acc-a3de-8904d5a32cb9>>> in the prompt, and a gated v4C still as start\_image, 9:16. In the prompt, paste the locked body and hair line word for word and add "keep the same expression, smile with eyes open, natural blinks only", "keep freckles and skin texture", "matte skin, no sheen", "camera locked, no zoom". Describe only low, natural motion. Sound is off unless the clip is talking or singing. Run get\_cost first. If the "IN THE DARK" preset notice comes up, resubmit with declined\_preset\_id (free). If you get 400 "Reference element is not ready", resubmit a few seconds later.
11. Lip-sync for talking or singing clips: Sync Lipsync (sync\_so, cut\_off) on the Kling take, driven by the compressed and loudness-normalised vocal stem. Check the mouth against the words (qa/[sync.py](http://sync.py)) and redo it if it is weak.
12. Self-check the clip. Sample frames across the whole clip, not only the first frame (drift shows at 3 to 5 s), and put them next to the face and body references. Run [drift.py](http://drift.py) (every 0.5 s) and the eye check (eye aspect under \~0.22 for 4 or more samples in a row means closed eyes; trim them). Also check expression, hands (five fingers, no melting), on-screen text, glossy or smoothed skin, odd arms or tattoos, and props that morph. Cut around bad ranges or redo.
13. Export every clip with ffmpeg: -c:v libx264 -profile:v main -pix\_fmt yuv420p -movflags +faststart, full 9:16 (1080x1920) with no blurred bands or padding, under 15 MB. Strip metadata (-map\_metadata -1). Confirm with ffprobe.
14. Make 4 platform cuts per clip, with 2 to 3 recut hooks across the day: \<clipname>\_cutA\_[tiktok.mp](http://tiktok.mp)4, \_cutB\_[instagram.mp](http://instagram.mp)4, \_cutC\_[shorts.mp](http://shorts.mp)4, \_cutD\_[facebook.mp](http://facebook.mp)4 (see /workspace/jsw\_tiktok/sienna/recuts/). Each cut gets the step 13 export and check. Then make \<clipname>\_thumb.jpg for Shorts: a sharp frame with a clear face, not mid-blink, and no text over the face.
15. Build the X set for the day: short clips as the core with photos mixed in, 4 to 6 posts, at least half of them teases. Teases are X-only, marked sensitive, can swear, carry no URL ("link in bio"), and stay SFW. The pinned post with the Fanvue link is set by hand and is not part of the scheduled set.
16. Write the captions per platform in Sienna's voice. TikTok/IG/YT/FB: clean, no Fanvue, no swearing, no AI mention. Apply the platform AI label (AI-generated toggle or label) everywhere it is required. On Fanvue, the AI disclosure in the bio and captions stays.
17. Build the review montage: frames from the clip or stills at the same scale next to sienna\_v4C\_reference\_sheet.jpg, with a short body and hair note (build, bust, waist and hips, hair colour, length and style, tan and freckles).
18. Submit to the JSW Content Reviewer. Every submission includes: the exact files (cuts, thumb, X media); the credits spent, including redos (from Higgsfield transactions, your jobs only); the target platforms; the AI label line plus the X-only tag on teases; the caption for each post; confirmation that the locked body and hair line was pasted word for word into every image and video prompt; and the same-scale montage with the body/hair note. Log it in the Content Review Log.
19. After the review: on FAIL, fix exactly what was flagged and resubmit (count the redo credits). On PASS, hand the passed files and captions to the JSW Content Scheduler. The bot never posts and never schedules.
20. Save [NOTES.md](http://NOTES.md) in today's folder (/workspace/jsw\_tiktok/sienna/YYYY-MM-DD/): final file specs, prompts, job ids, gate scores, QC results, credits, and what worked.

## Daily routine (America/Detroit time)

Gold Coast (AEST, UTC+10) is Detroit time + 14 h. Bali (WITA, UTC+8) is Detroit time + 12 h. Her waking day of about 6 AM to 11 PM local is about 4 PM to 9 AM in Detroit on the Gold Coast, and about 6 PM to 11 AM in Detroit in Bali.

- 2:30 PM EDT: steps 1 to 4 (story, live research, plan, plan check). It is pre-dawn on the Gold Coast (4:30 AM AEST).
- 3:00 to 6:00 PM EDT: clip 1, steps 5 to 18, submitted to the Reviewer by 6:00 PM EDT (8 AM AEST / 6 AM WITA), so her morning posts can go out.
- 8:00 to 10:30 PM EDT: clip 2 (optional second clip) plus the rest of the day's X set, submitted by 10:30 PM EDT (12:30 PM AEST / 10:30 AM WITA).
- Proposed X slots for the Scheduler (local time → EDT). Gold Coast: 7 AM → 5 PM, 10 AM → 8 PM, 1 PM → 11 PM, 5 PM → 3 AM, 8 PM → 6 AM, 10 PM → 8 AM. Bali: 7 AM → 7 PM, 10 AM → 10 PM, 1 PM → 1 AM, 5 PM → 5 AM, 8 PM → 8 AM, 10 PM → 10 AM.
- 9:00 AM EDT the next morning: step 20 notes, and check overnight Reviewer verdicts.
</content>
</page>