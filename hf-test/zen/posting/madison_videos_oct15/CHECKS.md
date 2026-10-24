# Checks (Oct 15)
| Clip | Transcript | Voice vs madison.mp3 | Lip-sync (frame strips) | Identity gate (video, 8-12 frames) | Visual face/body | No bg people |
|---|---|---|---|---|---|---|
| lipsync2 (reformer) | PASS "Reformer one me zero still cute though" = line, ends 4.5s | PASS median f0 213 Hz vs ref 208 Hz | OK, mouth moves with speech, no teeth drift seen at 1 fps | PASS 8/8, min centroid 0.632 | PASS, same face, tee/jeans stable | PASS |
| lipsync1 (new york) | PARTIAL: said "New York's growing on me, so are you." (dropped "Real talk?"); caption matches what is spoken | WEAK PASS: f0 184 Hz vs ref 208 Hz (lower, still American) | OK | PASS 8/8, min 0.681 | PASS, sweater/face stable | PASS |
| dance | n/a (no speech) | n/a | n/a | FAIL strict: 7/8 frames pass (87.5%) but one spin frame has her back to camera (centroid 0.01) | PASS: face/body/outfit held; hair flip + spin natural | PASS |
| montage1 | n/a | n/a | n/a | PASS 10/12 frames (83%), min 0.829 (failed frames = face-small/edge reasons, not identity) | PASS, 7 distinct stills, no repeats | PASS |
| montage2 | n/a | n/a | n/a | PASS 11/12, min 0.613 | PASS, 6 distinct stills; all s-stills are NEW and each fails the strict still gate (centroid 0.62-0.75 vs 0.78 Seedream bar), faces read as her by eye: Samuel's eye needed | PASS |
Seedance 8s 720p audio on = 36 cr (preflight exact). First lip-sync attempt (n6 crop, cleavage + shorts) came back status nsfw.
Lip-sync rule learned: Seedance speaks ~2.5 words/s but runs long; an 11-word line got cut off at 8s ("still look" ... missing "cute losing"). Keep lines <= 8 words.
