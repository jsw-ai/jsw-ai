# Reviewer submissions: Camille song videos, 2026-10-22
Album: Riviera Après Minuit, Camille Dubois. Song 01: Bonsoir Monaco.
Dir: /workspace/hf-test/zen/posting/camille_songs/01_bonsoir_monaco/
Pipeline: Seedream v5 pro single-ref edit from body1_v4C (62cab441), then finish_v4C, then Kling 3.0 std 5 s (Element e3a57e1a, low motion, sound off). Hard cuts only, no lip-sync, no talking to camera, SFW.
Audio: 01_bonsoir_monaco.wav. Chorus drop at about 52.2 s (energy analysis; whisper returned no text). Text: Montserrat Bold via libass at output resolution.

## 1. Hook, 21 s vertical 1080x1920: out/camille_bonsoir_monaco_hook_21s.mp4
- md5 21f37cf1a9d742ee5cfb87b13d7762d6. Audio 50.0–71.0 s. Title card 0–2.6 s, tag "original audio by Camille Dubois" 2.6–17.0 s, end card "Out now on Apple Music" 17.0–21 s.
- 12 unique scenes at 1.75 s each, all Kling clips; per-clip window picked from its per-frame gate.
- Manifest: out/camille_bonsoir_monaco_hook_21s_manifest.json. Gate: qc/gate_camille_bonsoir_monaco_hook_21s.json (GATE_HOOK)
- TikTok/IG caption: "Bonsoir, Monaco 🌙✨ the lights come on one by one… Bonsoir Monaco from my album Riviera Après Minuit, out now on Apple Music 🍷 #bonsoirmonaco #rivieraapresminuit #frenchpop #nudisco #monaco"

## 2. X cut, 24 s vertical, SFW: out/camille_bonsoir_monaco_x_24s.mp4
- md5 46d77b0073d0c84b592f3d05574f7b5e. Audio 49.6–73.6 s. Title card 0–3.0 s, end card from 20.0 s.
- 12 unique scenes at 2.0 s each, in a different order and from different clip windows than the hook. Not sensitive.
- Gate: GATE_X
- X caption: "Bonsoir, Monaco 🌙 Casino lights and the sea below. Bonsoir Monaco, the opener of Riviera Après Minuit, out now on Apple Music 🍷✨"

## 3. YouTube, 21 s horizontal 1920x1080: out/camille_bonsoir_monaco_youtube_21s.mp4
- md5 cdeb281de1be4fbc97ac1ecfd05c35d4. Built only from horizontal sources: no letterbox, no cropped verticals. Same hook in/out and cards as cut 1.
- 12 unique scenes: 10 horizontal Kling clips plus 2 horizontal Ken Burns stills (M02_heels_h, whose clip failed the frame gate at .696, and M09_lights_h, which has no clip).
- Gate: GATE_YT
- YouTube title: "Camille Dubois – Bonsoir Monaco (Riviera Après Minuit)"
- Description: "Bonsoir Monaco, the opener of my album Riviera Après Minuit. Out now on Apple Music: https://music.apple.com/us/album/riviera-apr%C3%A8s-minuit/6825779566 #bonsoirmonaco #frenchpop #nudisco"

Credits: Seedream 24 × 2.5 = 60; Kling 23 × 7.5 = 172.5; total 232.5.
