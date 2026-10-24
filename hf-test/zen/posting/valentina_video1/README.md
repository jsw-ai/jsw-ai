# Valentina video batch 1 (Oct 15 2026): for Samuel's approval, NOTHING POSTED
Series: "Gym Girl Confessions". No AI mention anywhere. All 1080x1920 H.264/AAC, metadata stripped, light grain + mild sharpen.

## Credits (exact, from preflight and submit; Seedance 2.0, 720p, 8 s)
| item | job id | credits |
|---|---|---|
| lipsync1 (pool smirk, b2-05) | 05e1641d-81e3-4f10-a2f7-8a117159920d | 36 |
| lipsync2 (car, b2-06) | 89eca2f4-1e6f-405f-a203-234120a395de | 36 |
| dance1 (home workout still b1-08r, audio off) | a35cd0d3-0f04-4506-aeab-bb07bfeaa92e | 36 |
| montage A, montage B (ffmpeg, synthetic beat) | n/a | 0 |
**Total 108 credits.** Shared balance moved 2093.8 -> 1494.8 in this window (others are spending too; mine is 108).

## Files
1. `valentina_lipsync1_pool_9x16.mp4` 6.3 s. Still: batch2 pool soft smirk. Voice: valentina.mp3 ref. Line: "Okay, I'm not saying I told you so... but I totally told you so." Hook: "gym girl confessions: that moment you get to say I told you so". Caption IG/TikTok: "I called it. you know I called it." #gymgirlconfessions #itoldyouso #gymtok #poolday
2. `valentina_lipsync2_car_9x16.mp4` 8.0 s. Still: batch2 car, shy smile. Line: "Okay so I got in the car to leave, and then I saw one text and just sat here smiling for five minutes." Hook: "gym girl confessions: one text and I forgot I was even leaving". Caption: "the most productive five minutes of my day". #gymgirlconfessions #storytime #girltalk #carselfie
3. `valentina_dance1_9x16.mp4` 8.0 s, no voice, beat track added. Hook: "gym girl confessions: this is how I dance after leg day, don't judge". Captions "me pretending my legs work" / "(they do not) now watch again". Caption: "legs: gone. vibes: unbothered". #gymgirlconfessions #legday #dancechallenge #gymtok
4. `valentina_montage_A_9x16.mp4` 15 s, 120 bpm, cut every 6 beats (3 s). Stills (batch2): gym neutral, market laugh, bookstore surprise, sunset squint, brunch mid-speech. Hook: "gym girl confessions: my 6am self vs my 6pm self, be honest". Captions: 6am/9am/1pm/5pm/6pm "me" jokes. Caption: "which one are you". #gymgirlconfessions #6amvs6pm #gymtok #relatable
5. `valentina_montage_B_9x16.mp4` 14.4 s, 100 bpm, cut every 4 beats (2.4 s). Stills (batch1): farmers market, sunset, brunch, bookstore, pool, car. Hook: "gym girl confessions: things I swear I'll do after leg day". Caption: "number 3 is every single weekend". #gymgirlconfessions #legday #weekendvibes #gymtok
Hashtags: keep 3-5 per post. `work/` holds raw model outputs, beats, check sheets (`*_sheet.png`, `L*f.png`, `dfin.png`).

## Checks (frames extracted and viewed; whisper transcript)
- lipsync1: transcript word-for-word correct (en). Voice pitch median 182 Hz vs ref 193 Hz (same voice character; not an ear test). Likeness good, textured skin, no artifacts seen, mouth follows words. Weakness: the model idles ~2.0 s before speaking, so I trimmed the first 1.7 s: final is 6.3 s (< the 8-15 s ask). Slight softness, strongly backlit. Pool chairs behind her stay empty, no people.
- lipsync2: transcript word-for-word correct, speech starts at 0.0 s, ends 7.6 s. Likeness good in close-ups (checked mouth/teeth at full res; natural). Camera pulls back vs the still so she sits left of center and the face is smaller than the still. Seatbelt/clothes stable.
- dance1: moves naturally (sway, bounce, spin toward camera), outfit, room, face consistent across 8 s; no morphing seen. Wide shot so face small early on. Plain room, no other people.
- montageA/B: text fits frame, hook visible in first 2.5 s, captions burned in, cuts land on beats of the synthetic track.

## Honest limits
- Music is a simple synthesized beat (no licensed or trending track on the box). Swap in a trending in-app sound at posting time.
- "Looped end": last caption says "watch again" and the last slide is chosen to match the hook's tone, but there is a hard cut, not a crossfade to frame 1.
- Batch1 stills (montage B, dance) were not part of the batch2 set Samuel approved; he should OK them. Batch1 and batch2 share scenes (market, bookstore, sunset, brunch, pool), so do not post A and B back to back.
- Montage B is all smiles (batch1); expression variety is in A only. The "mirror / walking / getting ready" motion shots were not made yet (each is another ~36 cr).
- Face gate (identity_gate) was not run on video frames.
