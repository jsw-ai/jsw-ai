import json,os,statistics as st
F='/workspace/hf-test/zen/posting/gabriela/songvideos/caipirinha_kiss/'
H=json.load(open(F+'final/gabriela_caipirinha_kiss_hook_21s_1080x1920_manifest.json'));M={s['scene']:s for s in H['shots']}
Y=json.load(open(F+'final/gabriela_caipirinha_kiss_youtube_21s_1920x1080_manifest.json'));M.update({s['scene']:s for s in Y['shots']})
mi=json.load(open(F+'work/media_ids.json'))
NEW={'v14_linenset':('sunset_a','7b8ebc45'),'v15_mididress':('paulista_b','ffc95696')}
L=['# REVIEWER PACKET v2 – Gabriela "Caipirinha Kiss" (Brisa de Miami)','','Fixes in v2:','1. TikTok hook: v11_hammock replaced with the new v14_linenset (covered linen set, Kling job 7b8ebc45).','2. IG Reel: v11_hammock replaced with the new v15_mididress (high-neck midi dress, Kling job ffc95696). This is a different shot from the TikTok replacement.','3. X 24s: same edit and outfits, still flagged SENSITIVE. Only re-encoded at 4.4 Mb/s to get under 15,000,000 bytes.','4. YouTube 16:9: same edit re-encoded at 4.8 Mb/s to get under 15,000,000 bytes. Thumbnail regrabbed from the new file. Posts as a regular video, NOT a Short.','','All files are H.264 Main, yuv420p, +faststart, AAC. The release card says "coming soon". No mention of AI and no Fanvue links.','']
for n,note in [('hook_21s_1080x1920_v2','TikTok'),('igreel_21s_1080x1920_v2','IG Reel'),('x_24s_1080x1920_v2','X – SENSITIVE'),('youtube_21s_1920x1080_v2','YouTube regular video (not a Short)')]:
  b=F+'final/gabriela_caipirinha_kiss_'+n;S=json.load(open(b+'_shots.json'));P=json.load(open(b+'_pf.json'))
  rows=[]
  for i,s in enumerate(S['shots']):
    sc=s['scene'];m=M.get(sc,{});w=[x for t,x in P['scores'] if x is not None and s['t0']<=t<s['t1']]
    md,mn=st.median(w),min(w)
    ref=NEW[sc][0] if sc in NEW else m.get('v4C_ref','');job=NEW[sc][1] if sc in NEW else m.get('kling_job_prefix','')
    s.update(v4C_ref=ref,finished_still=f'fin/{sc}_v4C.jpg',finish='finish_v4C',element='bd5edf6e-488e-49ad-8cb2-66a73148ade5',kling_job_prefix=job,shot_median=round(md,3),shot_min=round(mn,3))
    rows.append(f"| {i+1} | {sc} | {s['t0']:.2f}–{s['t1']:.2f} | {s['src_in']}s | {ref} | {job} | {md:.3f} | {mn:.3f} | {'PASS' if md>=.78 and mn>=.70 else 'FAIL'} |")
  S['sensitive']=n.startswith('x_');S['youtube_type']='regular video' if n.startswith('youtube') else None
  json.dump(S,open(b+'_manifest.json','w'),indent=1)
  sz=os.path.getsize(b+'.mp4')
  L+=[f'## {note}: `{b}.mp4`',f"- {S['W']}x{S['H']}, {S['duration']} s, {sz:,} bytes; whole-file gate median {P['median']:.3f} / min {P['min']:.3f} {'PASS' if P['pass_'] else 'FAIL'}",f'- manifest `{b}_manifest.json`; side-by-side `{F}qc/{n}_sbs.jpg`'+(f'; thumbnail `{b}_thumb.jpg`' if n.startswith('youtube') else ''),'','| # | scene | time in cut (s) | clip in-point | single v4C ref | Kling job | shot median | shot min | gate |','|---|---|---|---|---|---|---|---|---|']+rows+['']
L+=['## Captions']+open(F+'final/captions.md').read().splitlines()[1:]
open('/workspace/hf-test/zen/posting/gabriela/songvideos/REVIEWER_PACKET_caipirinha_kiss_v2.md','w').write('\n'.join(L))
print('ok')
