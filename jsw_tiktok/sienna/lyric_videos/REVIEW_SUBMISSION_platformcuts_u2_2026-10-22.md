# Review request: Sienna Blake per-platform cuts u2 (2026-10-22, built 19:05–19:50 EDT). NOT posted.
This replaces the failed u1 cuts, which used the v5e/v3c Ken Burns segments. Do not use the u1 files.

## Process
Static approved v4C stills with 0.5 s crossfades only. NO pans, NO zooms, NO Ken Burns, no motion of any kind on the stills. Each still was rendered as a fixed frame (`-loop 1`, a fixed crop, a single scale to 1080x1920, no zoompan or animated crop expressions). The source is build script platformcuts_work/build2.py. The segments are in platformcuts_work/static_segs/.
Face stills (approved v4C only): v2sA2_c_v4C (2026-10-22_album/fin), bal_p_v4C (x_clips_2026-10-21/remake/fin) and gc_surf_i_v4C (approved strip, 02_low_tide_lover/work/gate_src). No sC2_b, sA2_b, eB4_b or eB4_c. b1a and surf_c are not used. Other shots are people-free album scene stills, also static.
No Kling clips were needed. The brief allowed static stills, so no new generations and no new faces were made, and Kling Element Sienna-v2-1020 was not called.
**Credits used: 0** (Higgsfield/Kling 0, outpaint 0).
On top of the stills: the synced lyrics are burned in, a distinct top hook shows from 0 to 2.9 s, and the end card covers the last 3.5 s: "Sienna Blake / '<title>' / out now on Apple Music". There is no Spotify.
Spec (all cuts): H.264 Main, yuv420p, AAC LC 48 kHz, faststart (moov at byte 36), 1080x1920, full frame (no bars or blur), all under 15 MB.
Uniqueness: each md5 was checked against every .mp4 and .jpg in 01_salt_in_my_hair/ and 02_low_tide_lover/, work folders included. Each one matches only itself.
Gate: identity_gate.py img --model sienna --source seedream. 16 frames per cut, taken from the fully visible face windows. One job at a time, each only when free -g showed 3 GB or more available. Frames and JSON are in platformcuts_work/gate_<cut>_u2/ and gate_<cut>_u2.json. All 128 frames scored 0.78 or higher.

## A) Salt in My Hair (re-cuts of v5e content; scenes: 0 ocean, 1 beach, 2 surfboard, 3 rice terraces, 7 sunset sea end card)
| platform | path | md5 | bytes | len | opening / order | hook | gate min / median |
|---|---|---|---|---|---|---|---|
| TikTok (replaces v5e on GPnmjwyk) | 01_salt_in_my_hair/sienna_salt_in_my_hair_hook_short_1080x1920_v5e_tiktok_u2.mp4 | 31ff1a0854eafd9cfd569700a321deab | 8,928,725 | 24 s | surfboard › beach › v2sA2_c › ocean › terraces › end | "new album out now / this is the title track" | 0.801 / 0.807 |
| X | 01_salt_in_my_hair/sienna_salt_in_my_hair_hook_short_1080x1920_v5e_x_u2.mp4 | 10fdd6146a6bdf527ce1b2c45f416bad | 5,650,643 | 16 s | opens on v2sA2_c › ocean › surfboard › end | "the title track / from my new album" | 0.799 / 0.802 |
| YouTube Shorts | 01_salt_in_my_hair/sienna_salt_in_my_hair_hook_short_1080x1920_v5e_ytshorts_u2.mp4 | 13328413b534d737eba1c40b7d511ec8 | 7,191,311 | 20 s | terraces › v2sA2_c › beach › ocean › end | "no plan, no hurry, / nowhere to be" | 0.805 / 0.810 |
| YT thumbnail | 01_salt_in_my_hair/sienna_salt_in_my_hair_hook_short_1080x1920_v5e_ytshorts_u2_thumb.jpg | a94f5c804d79da28c4df5edafe18c372 | 478,324 | | the exact frame at 6.1 s of the ytshorts_u2 clip (v2sA2_c, inside the gated window), 1080x1920 | | |
| IG Reel | 01_salt_in_my_hair/sienna_salt_in_my_hair_hook_short_1080x1920_v5e_igreel_u2.mp4 | ecbaa57d52bab4577684362079fe39ba | 8,216,564 | 22 s | beach › surfboard › v2sA2_c › terraces › ocean › end | "wrote this one / with wet hair" | 0.804 / 0.807 |

Captions:
- TikTok: Salt in My Hair 🌊 new album out now on Apple Music, link in bio
- X: the title track 🌊 new album Salt in My Hair out now on Apple Music https://music.apple.com/us/album/salt-in-my-hair/6825685962
- YouTube Shorts (proposed): title "Sienna Blake – Salt in My Hair (title track) #shorts". Description: new album 'Salt in My Hair', out now on Apple Music: https://music.apple.com/us/album/salt-in-my-hair/6825685962 #siennablake #newmusic #indiepop
- IG Reel: Salt in My Hair 🌊 new album out now on Apple Music, link in bio

## B) Low Tide Lover (re-cuts of v3c content; scenes: 0 ripples, 1 blue hour end card, 4 headland, 5 rock pools)
| platform | path | md5 | bytes | len | opening / order | hook | gate min / median |
|---|---|---|---|---|---|---|---|
| TikTok (replaces v3c on jWfKag97) | 02_low_tide_lover/sienna_low_tide_lover_hook_short_1080x1920_v3c_tiktok_u2.mp4 | e8047987a5c04ed2dbbfe18c0ec4d773 | 8,860,481 | 24 s | gc_surf_i › rock pools › bal_p › ripples › headland › end | "he left his towel / at mine again" | 0.811 / 0.818 |
| IG Reel (replaces v3c on Uqzjs0ZZ) | 02_low_tide_lover/sienna_low_tide_lover_hook_short_1080x1920_v3c_igreel_u2.mp4 | 80544db0ce9fa4339d51cc719e26674a | 8,351,163 | 22 s | bal_p › ripples › gc_surf_i › rock pools › headland › end | "only shows up when / the water's gone" | 0.809 / 0.818 |
| IG Story | 02_low_tide_lover/sienna_low_tide_lover_hook_short_1080x1920_v3c_igstory_u2.mp4 | 634eff5ebe65c183dbaf2bc1e0c64b39 | 3,927,129 | 12 s | bal_p › headland › end | "a song for the one / who never stays" | 0.816 / 0.821 |
| X | 02_low_tide_lover/sienna_low_tide_lover_hook_short_1080x1920_v3c_x_u2.mp4 | 6168ac4f6f440f584faf2f18f57a608a | 6,494,849 | 18 s | ripples › gc_surf_i › rock pools › bal_p › end | "track 2: / low tide lover" | 0.805 / 0.815 |

Captions (from REVIEW_SUBMISSION_v3c.md):
- TikTok: wrote this one on the bonnet with a bag of hot chips after he left his towel at mine again 🌊 'Low Tide Lover' out now on Apple Music, link in bio #lowtidelover #newmusic #goldcoast #surfergirl
- IG Reel: he only ever turns up when the tide's out… so I wrote him a song 🌊 'Low Tide Lover' out now on Apple Music, link in bio #lowtidelover #newmusic #indiepop #goldcoast
- IG Story: new lyric video 🌊 'Low Tide Lover' – out now on Apple Music, link in bio
- X: he only shows up when the water's gone 🌊 low tide lover https://music.apple.com/us/album/salt-in-my-hair/6825685962

## Scheduling notes
- The three bookings (GPnmjwyk, jWfKag97, Uqzjs0ZZ) still point at the old Ken Burns files. The Scheduler has to swap them to the u2 files above. I changed no bookings.
- The Salt cuts all use v2sA2_c. The Low Tide Lover cuts use only bal_p and gc_surf_i. As the reviewer asked, schedule the two songs on different days, and don't post two cuts of the same song on the same platform on the same day.
- Rejected or partial build files are in platformcuts_work/rejected/ and must not be used.
