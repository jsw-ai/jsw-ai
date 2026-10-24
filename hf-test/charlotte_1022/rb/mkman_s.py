import json,hashlib,shutil,glob
G={}
for f in glob.glob('qc/gate_s*.json'): G.update(json.load(open(f)))
J=dict(l.split('\t')[:2] for l in open('man/still_jobs.tsv').read().split('\n') if '\t' in l)
SRC={'S5':'/workspace/hf-test/charlotte_1022/rb/up/c_S5.jpg (approved v4C, gate .863)','D2':'/workspace/hf-test/charlotte_1022/rb/up/c_D2.jpg (approved v4C, gate .821)'}
items={
 'X3_sauna_tease':dict(platform='X',sensitive=True,stills=[('x3a','S5'),('x3b','S5')],caption="warming back up after the plunge. the full version's in my bio 🔥"),
 'X5_recovered_mostly_tease':dict(platform='X',sensitive=True,stills=[('x5c','S5')],caption="recovered. mostly. full version in bio, darling 😇",note='only 1 of 2 regenerated stills passed (x5d .747 failed); single-image post'),
 'Reddit1_recovery_day':dict(platform='Reddit',sensitive=False,stills=[('r1c','D2')],caption="Recovery day in Munich after a 2-2 away day"),
 'Reddit2_away_kit_check':dict(platform='Reddit',sensitive=False,stills=[('r2b','D2')],caption="Away day kit check from Munich"),
}
for name,it in items.items():
  out=[]
  for k,s in it['stills']:
    fp='fin/%s_v4C.jpg'%k; g=G[fp]; dst='final/%s_%s.jpg'%(name,k); shutil.copy(fp,dst)
    out.append(dict(file='/workspace/hf-test/charlotte_1022/rb/'+dst,md5=hashlib.md5(open(dst,'rb').read()).hexdigest(),
      source_ref=SRC[s],model='seedream_v5_pro, 3:4, 2k, single image_reference',job_id=J[k],seed='not exposed by Higgsfield API (job id recorded)',
      finish_v4C='applied (rb/finish_v4C.py md5 f7c35257f0065b88e51f1cccd444ca70)',gate=dict(centroid=round(g['score_centroid'],3),pass_=g['pass_'],reasons=g['reasons']),eye_check='matte skin, no plastic look, framing ok',prompt_file='rb/p/%s.txt'%k))
  m=dict(item=name,**{x:y for x,y in it.items() if x!='stills'},assets=out,ai_mention=False)
  json.dump(m,open('man/%s.json'%name,'w'),indent=1,ensure_ascii=False); print(name,[ (a['gate']['centroid'],a['md5']) for a in out])
