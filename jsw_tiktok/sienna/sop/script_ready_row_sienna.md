# Sienna: settings row and exceptions for "JSW Pipeline: Script-ready steps"

## Kling
- Element: Sienna-v2-1020, 2603afeb-5f21-4acc-a3de-8904d5a32cb9
- Model kling3_0, sound off, low motion
- Generate natively at the target aspect ratio. If a clip comes out 3:4, cover-crop it with scale=-2:1920,crop=1080:1920. Never pad it, because padding creates blur bands.

## Reference stills
- Folder: /workspace/hf-test/zen/posting/sienna_refs/
- Files: story1_a_v4C.jpg, story2_a_v4C.jpg, story3_b_v4C.jpg, reddit_x1_b_v4C.jpg
- Use one reference image per Seedream job.
- Body line: /workspace/jsw_tiktok/sienna/SIENNA_LOCKED_BODY_LINE.txt

## Gates
- Stills must score 0.79 or higher: identity_gate.py img --model sienna --source seedream --body
- The script's default seedream_centroid is 0.78, so check the score again after it runs.
- Video must score 0.78 or higher on 16 frames, against story1_a_v4C.

## Banned stills
- sC2_b, sA2_b, eB4_b, eB4_c

## Body check
- Even golden tan and a full, round, natural C-to-D cup bust.
- Check by eye against the reference sheet.

## Known face issue
- Seedream narrows her face in wider body shots and with closed-mouth smirks, and those score 0.64 to 0.77.
- Head-to-waist framing with a teeth smile and even front light passes.

## Music
- Masters: /workspace/music/distrokid/sienna/01-10 *.wav
- Lyrics: release.md in the same folder
- Wording: "out now on Apple Music" with https://music.apple.com/us/album/salt-in-my-hair/6825685962
- No Spotify mentions yet.

## Accounts
- AdsPower profile k1cwvh25: headless only, and never touch the proxy or fingerprint.
- Ayrshare can't post to Reddit user profiles (u_ gives SUBREDDIT_NOEXIST).
- Reddit returns 403 to the box, so use the AdsPower session.
