# Review request: Sienna Blake per-platform cuts (2026-10-22). NOT posted.
JSW rule: one file per platform. Each cut below has its own opening shot, hook text and length, so every md5 is different.
Process: a re-edit of the passed v5e and v3c footage, using Valentina's process, with no new generations. The cuts reuse the text-free Ken Burns segments of those versions (01_salt_in_my_hair/work/v5es/seg_short, 02_low_tide_lover/work/v3/seg3c_short) and the same album WAV. The shots are reordered with 1 s crossfades. The synced lyrics are re-burned, the new top hook text shows from 0 to 2.9 s, and the end card covers the last 3.5 s. No new faces, Kling, Seedance or outpaints, and 0 credits.
Spec (all cuts): H.264 Main, yuv420p, AAC LC 48 kHz, faststart (moov at byte 36), 1080x1920, full frame (no bars or blur), all under 15 MB. End card: "Sienna Blake / '<title>' / out now on Apple Music". No Spotify. End cards checked by eye.
Uniqueness: each md5 was checked against every .mp4 and .jpg in 01_salt_in_my_hair/ and 02_low_tide_lover/ (work folders included). Each one matches only itself.
Face gate: identity_gate.py img --model sienna --source seedream, 16 frames per cut, taken from the fully visible face-shot windows. Each job ran on its own, and only when free -g showed 3 GB or more available. Every frame scored 0.78 or higher. Frames and JSON: lyric_videos/platformcuts_work/gate_<cut>/ and gate_<cut>.json.

## A) Salt in My Hair (from v5e 6ba89e9a593b3b406593d5b9f90c2a3c; TikTok GPnmjwyk stays on v5e)
v5e order: scene_2, scene_1, v2sA2_c (face), scene_0, scene_3, scene_7 end card. 24 s. No top hook.

| cut | path | md5 | bytes | len | what differs | gate min / median |
|---|---|---|---|---|---|---|
| X | 01_salt_in_my_hair/sienna_salt_in_my_hair_hook_short_1080x1920_v5e_x_u1.mp4 | 54cb5df152a850ee6901f6ff4a4e928d | 6,414,071 | 16.0 s | Opens on the face shot v2sA2_c. Order: face, scene_0, scene_2, scene_7 end card. Hook: "the title track / from my new album" | 0.790 / 0.793 (16/16) |
| YouTube Shorts | 01_salt_in_my_hair/sienna_salt_in_my_hair_hook_short_1080x1920_v5e_ytshorts_u1.mp4 | 4114d4c7863c6fd913a6efec790e7af9 | 7,951,747 | 20.0 s | Opens on scene_3 (rice terraces). Order: scene_3, face, scene_1, scene_0, scene_7. Hook: "no plan, no hurry, / nowhere to be" | 0.791 / 0.798 (16/16) |
| YT thumb | 01_salt_in_my_hair/sienna_salt_in_my_hair_hook_short_1080x1920_v5e_ytshorts_u1_thumb.jpg | cefdb3f8f65923fc0ac5e80a60534494 | | | Face frame at 6.2 s, 1080x1920 | (inside the gated window) |
| IG Reel | 01_salt_in_my_hair/sienna_salt_in_my_hair_hook_short_1080x1920_v5e_igreel_u1.mp4 | 2b0f913cc0707e9cb2837fa1bc0b9016 | 9,351,605 | 22.0 s | Opens on scene_1. Order: scene_1, scene_2, face, scene_3, scene_0, scene_7. Hook: "wrote this one / with wet hair" | 0.787 / 0.801 (16/16) |

Captions:
- X: the title track 🌊 new album Salt in My Hair out now on Apple Music https://music.apple.com/us/album/salt-in-my-hair/6825685962
- YouTube Shorts title: Sienna Blake – Salt in My Hair (title track) #shorts. Description: new album 'Salt in My Hair', out now on Apple Music: https://music.apple.com/us/album/salt-in-my-hair/6825685962 #siennablake #newmusic #indiepop (proposed, because no YT caption was given)
- IG Reel: Salt in My Hair 🌊 new album out now on Apple Music (no "link in bio")

## B) Low Tide Lover (from v3c 9fb32ce8064e3db8cafc0a291cfc995b; IG Reel Uqzjs0ZZ and TikTok jWfKag97 stay on v3c)
v3c order: gc_surf_i (face), scene 5, bal_p (face), scene 0, scene 4, scene 1 end card. 24 s. No top hook.

| cut | path | md5 | bytes | len | what differs | gate min / median |
|---|---|---|---|---|---|---|
| IG Story | 02_low_tide_lover/sienna_low_tide_lover_hook_short_1080x1920_v3c_igstory_u1.mp4 | 0d8a91d8b924f0aac3e1cdda6176ce61 | 4,459,516 | 12.0 s | Opens on bal_p (guitar balcony). Order: bal_p, headland, blue hour end card. Hook: "a song for the one / who never stays" | 0.797 / 0.816 (16/16) |
| X | 02_low_tide_lover/sienna_low_tide_lover_hook_short_1080x1920_v3c_x_u1.mp4 | 1dca8a3e527115d4f542785d2a1d5309 | 7,890,470 | 18.0 s | Opens on scene 0 (ripples). Order: ripples, gc_surf_i, rock pools, bal_p, blue hour end card. Hook: "track 2: / low tide lover" | 0.796 / 0.813 (16/16) |

Captions (kept from REVIEW_SUBMISSION_v3c.md):
- IG Story: new lyric video 🌊 'Low Tide Lover' – out now on Apple Music, link in bio
- X: he only shows up when the water's gone 🌊 low tide lover https://music.apple.com/us/album/salt-in-my-hair/6825685962

## Scheduling notes
- Reviewer flag: the v5e cuts use the face still v2sA2_c. Fact check: the v3c Short and these Low Tide Lover cuts only use gc_surf_i and bal_p. v2sA2_c is in the Low Tide Lover 16:9 lyric video, not the Short. As the reviewer asked, schedule the Salt in My Hair cuts and the Low Tide Lover posts on different days anyway.
- Do not put two cuts of the same song on the same platform on the same day. The originals keep their bookings (GPnmjwyk, Uqzjs0ZZ, jWfKag97).
- The first X and IG Story builds put the hook text over the forehead, and the gate dropped to 0.733. They were moved to platformcuts_work/rejected/ and never used. The hook was moved above the head and the cuts rebuilt, and the gate numbers above are from those rebuilt files.
