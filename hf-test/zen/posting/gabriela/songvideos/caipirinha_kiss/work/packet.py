import json
F='/workspace/hf-test/zen/posting/gabriela/songvideos/caipirinha_kiss/final/gabriela_caipirinha_kiss_'
L=['# REVIEWER PACKET – Gabriela "Caipirinha Kiss" (Brisa de Miami)','All clips are new Kling 3.0 clips made today (Element bd5edf6e). None are shared with Y1 or any other post today. No yellow/green knit. Lyrics appear as title cards. Release card says "coming soon". Encode: Main, yuv420p, +faststart.','']
for n,note in [('hook_21s_1080x1920','TikTok hook, opens on v01 beachbar'),('igreel_21s_1080x1920','IG Reel, its own order, opens on v12 sunsetpier'),('x_24s_1080x1920','X cut, opens on v05 slipdress. FLAG SENSITIVE (suggestive outfits, no nudity)'),('youtube_21s_1920x1080','YouTube horizontal, native 16:9 clips only, thumb _thumb.jpg')]:
  S=json.load(open(F+n+'_manifest.json'))
  try: g=json.load(open(F+n+'_pf.json'));gs=f"median {g['median']:.3f} / min {g['min']:.3f} {'PASS' if g['pass_'] else 'FAIL'}"
  except Exception: gs='gate pending (running)'
  L+=[f'## {n}: {F}{n}.mp4',f'- {note}; {S["duration"]}s {S["W"]}x{S["H"]}; final gate {gs}',f'- manifest {F}{n}_manifest.json; sbs caipirinha_kiss/qc/{n}_sbs.jpg','- scenes ('+str(len(S['shots']))+' unique): '+', '.join(f"{s['scene']}@{s['src_in']}s (clip gate {s['clip_gate']})" for s in S['shots']),'']
L+=['## Captions','']+open(F.rsplit('/',1)[0]+'/captions.md').read().splitlines()[1:]
L+=['','Notes: the green satin and green bikini (h02, h12, h14, v01, v07) are not knit, and the v02 crochet is cream. v05 and v09 fail as full clips, so only windows where every frame scores ≥.70 are used.']
open('/workspace/hf-test/zen/posting/gabriela/songvideos/REVIEWER_PACKET_caipirinha_kiss.md','w').write('\n'.join(L))
