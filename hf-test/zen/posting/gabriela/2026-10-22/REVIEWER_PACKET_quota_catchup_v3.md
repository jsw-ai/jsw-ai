# Gabriela: Reviewer packet, quota catch-up v3 (Thu 10/22), replaces v1 and redo v2
Day dir: /workspace/hf-test/zen/posting/gabriela/2026-10-22. Pipeline: Seedream single ref fin/paulista_a_v4C.jpg (media b321b222) → finish_v4C → identity gate + body check → Kling 3.0 std, Element 8b128aab, sound off, low motion. No knit, no green satin, no lip-sync. Manifests: v3man/<item>_manifest.json (per-shot jobs and gates). Side-by-sides: v2/sbs/ (reference_set_gabriela.jpg, both sides 1280 px). Builds: qc/builds_b2.json keys *_v3. Nothing has been scheduled.

## T1: final/gabriela_tiktok_20261022_paulistanos-thursday_v3.mp4
- md5 cd6ed2a76b29c879509531d5f0ada24b | final gate median 0.857, min 0.764, PASS | sbs v2/sbs/gabriela_tiktok_20261022_paulistanos-thursday_v3_sbs.jpg | manifest v3man/T1_manifest.json
- shot k_paul_2 0.00–2.80 s, Kling pre-redo clip (original job, Element 8b128aab), clip gate {'median': 0.861, 'min': 0.779, 'pass': True}
- shot kv2_ibira 0.50–4.00 s, Kling 80ccb814, clip gate {'median': 0.828, 'min': 0.767, 'pass': True}
- burned-in text (exact): how Paulistanos do Thursday: / Paulista at noon | how Paulistanos do Thursday: / Ibirapuera at sunset
- caption: how Paulistanos do Thursday ☀️ #saopaulo #brasil | track 07_samba_no_pe.mp3 | suggested slot Fri 10/23 ~11 AM ET

## T2: final/gabriela_tiktok_20261022_spvsmiami-ep1_v2.mp4
- md5 765a10fa83f9fe26c95795976bf8de4f | final gate median 0.824, min 0.780, PASS | sbs v2/sbs/gabriela_tiktok_20261022_spvsmiami-ep1_v2_sbs.jpg | manifest v3man/T2_manifest.json
- shot k2_miamiglass 0.00–2.60 s, Kling pre-redo clip (original job, Element 8b128aab), clip gate median .849, min .796, PASS (gated today)
- shot kv2_beco 0.00–3.40 s, Kling ecb34a30, clip gate {'median': 0.833, 'min': 0.773, 'pass': True}
- burned-in text (exact): São Paulo vs Miami / ep. 1 | Miami me | São Paulo me
- caption: São Paulo vs Miami, ep. 1 🇧🇷🌴 #saopaulo #miami | track 01_bom_dia_miami.mp3 | suggested slot Fri ~2 PM ET

## T3: final/gabriela_tiktok_20261022_fan-reveal_v3.mp4
- md5 0e183958f637b7d12165f89789973fbe | final gate median 0.827, min 0.746, PASS | sbs v2/sbs/gabriela_tiktok_20261022_fan-reveal_v3_sbs.jpg | manifest v3man/T3_manifest.json
- shot k2_fancover 0.00–1.00 s, Kling pre-redo clip (original job, Element 8b128aab), clip gate segment 0–1.0 s ≈.82, PASS
- shot kv2_wynwood 0.00–3.60 s, Kling bc098d7b, clip gate {'median': 0.829, 'min': 0.754, 'pass': True}
- burned-in text (exact): hoodie mode | Wynwood mode
- caption: hoodie mode → Wynwood mode 👋 #wynwood #miami | track 04_golaco.mp3 | suggested slot Fri ~5 PM ET

## Y1: final/gabriela_yt_20261022_caipirinha-kiss_v2.mp4
- md5 3edf6e02e6fb17837eeb39bac85c00f3 | final gate median 0.808, min 0.754, PASS | sbs v2/sbs/gabriela_yt_20261022_caipirinha-kiss_v2_sbs.jpg | manifest v3man/Y1_manifest.json
- shot kv2_beachbar 0.00–1.20 s, Kling 2a3b2882, clip gate {'median': 0.746, 'min': 0.581, 'pass': False}
- shot kv2_beachbar 3.84–5.04 s, Kling 2a3b2882, clip gate {'median': 0.746, 'min': 0.581, 'pass': False}
- shot k2_miamisway 0.00–5.00 s, Kling pre-redo clip (original job, Element 8b128aab), clip gate median .836, min .780, PASS
- shot kv2_keybis 0.00–5.00 s, Kling 828c6cf5, clip gate {'median': 0.806, 'min': 0.759, 'pass': True}
- burned-in text (exact): Caipirinha Kiss | sour and sweet, / I can't resist | lime on my lips, / you won't forget this
- caption: Caipirinha Kiss 🍋 coming soon #shorts #brazilianmusic | track 05_caipirinha_kiss.mp3 | suggested slot Fri ~1 PM ET

## REEL: final/gabriela_igreel_20261022_spvsmiami-ep1_v3.mp4
- md5 77bd1e611933354cda2e32a0b8e70913 | final gate median 0.834, min 0.735, PASS | sbs v2/sbs/gabriela_igreel_20261022_spvsmiami-ep1_v3_sbs.jpg | manifest v3man/REEL_manifest.json
- shot kv2_havana 0.30–3.00 s, Kling 99a76edd, clip gate {'median': 0.786, 'min': 0.735, 'pass': True}
- shot k_paul_1 0.00–3.40 s, Kling pre-redo clip (original job, Element 8b128aab), clip gate {'median': 0.852, 'min': 0.803, 'pass': True}
- burned-in text (exact): São Paulo vs Miami / ep. 1 | Miami me | São Paulo me
- caption: São Paulo vs Miami, ep. 1 🇧🇷🌴 | track 06_ocean_drive.mp3 | suggested slot Fri ~12 PM ET

- Y1 thumbnail: final/gabriela_yt_20261022_caipirinha-kiss_v2_thumb.jpg (md5 a2f14e0e…), taken from the 1.0 s "Caipirinha Kiss" title card. Y1 uses only the clean beachbar segments (0–1.2 s and 3.84–5.04 s; the full clip fails at 1.25–3.8 s).
- T3 build record: builds_b2.json key T3_v3. The reveal lands on a new outfit and place (red floral wrap dress, Wynwood) with a wave. The hoodie cut was trimmed to 1.0 s because frame 1.167 scored .482.

## Oktoberfest clink (collab): collab/gabriela_collab_oktoberfest_clink_v8_silent.mp4
- md5 95d216be2c30…; 5.033 s, 30 fps, H.264 Main, yuv420p, faststart, no audio. Kling a9819f17 from okt_c_v4C (media 36611065). Gate median .856, min .712, PASS (v7 failed at min .662 and was dropped). Text: "São Paulo: saúde!". sbs v2/sbs/gabriela_collab_oktoberfest_clink_v8_silent_sbs.jpg; manifest v3man/clink_manifest.json.
- Outfit: green and red cotton dirndl. This is not satin, but flag it if green is out entirely.
- TikTok caption: "São Paulo: saúde! 🍻 with @<CHARLOTTE_HANDLE>". The Scheduler needs to supply the handle.

## IG Stories (3 fresh stills, final/stories_v3/; each gated with a JSON)
- S1 gabriela_igstory_20261022_s1_cafe-sp_v3.jpg md5 f20d3019…: seated in a café (not walking), navy turtleneck. Text "café first, always". Gate v2/gate_v2s1.json PASS .80.
- S2 …s2_sp-skyline_v3.jpg md5 67323d07…: São Paulo rooftop. Text "São Paulo from up here". Gate v2/gate_v2s2.json PASS .781.
- S3 …s3_paodequeijo_v3.jpg md5 90cc7321…: padaria, striped top. Text "bom dia, pão de queijo first". Gate v2/gate_v2s3.json PASS .80. This is a new still; padaria_f is not used here.
- Side-by-sides for all three are in v2/sbs/.

## padaria_f
- Used in one place only: the X pão de queijo image final/gabriela_x_20261022_paodequeijo_v3.jpg (sbs in v2/sbs/). No other item uses it.

## Friday 10/23 Reddit
- foot_b rebuilt without knit: final/gabriela_reddit_20261023_foot_b_v3.jpg (md5 0339afda…), navy sports top on the Copacabana promenade. Seedream a399d577, finish_v4C, gate PASS .810. The pose detector could not measure the body (waist-up crop), so the body check was done by eye and passes. sbs v2/sbs/v3rdfoot_v4C_sbs.jpg.
- Destination: Gabriela's profile only (u_Fresh_Membership8984). Subreddit AI-rule screenshots were NOT captured this round, so no subreddit posting until those exist.
- The second Reddit still (Arpoador) failed twice (.763, then .776). It is NOT delivered.
- sunset_a and miami_c go to X only: final/gabriela_x_20261023_sunset_a_v1.jpg (6576dc7f), final/gabriela_x_20261023_miami_v1.jpg (516ad244). sbs in v2/sbs/.

## Disclosures
- The ibira source still scored .771 (FAIL). Its Kling clip passes (.828/.767), and T1's final gate passes .857/.764.
- k_paul_1 (REEL) and k_paul_2 (T1) are different clips, but both show the same white-tee look. Both also appeared in the earlier, unposted packet-1 "paulistano-walk" TikTok and X cut. If either of those went live, swap the clip.
- k2_miamiglass (T2) and k2_miamisway (Y1) share the miami_c look with the Friday X miami still.
- No file reuses a prior md5 (checked against every mp4/jpg/png in the day dir).

## Not delivered
- Friday TikTok ×3, IG Reel + 3 stories, YT ×2 and X extras are not produced.
- The Reddit Arpoador still is not delivered.
- Subreddit AI-rule screenshots are not captured.
- FB is still locked under appeal, so nothing is planned for FB.
