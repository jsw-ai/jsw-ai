"""Sienna calibration (rebuilt 2026-10-14). Positives = approved finals only; group leave-one-out
(x2_dawn_v3 + x2_dawn_v4C are near-duplicates -> left out together; the 3 video-frame refs left out together).
Negatives = retrain/raw rejects, other models' keepers, older Sienna refs (dropped). Run: .face-venv/bin/python calibrate_gate.py"""
import sys,glob,json,os,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting'); import identity_gate as g
R='/workspace/hf-test/'; T=g.THRESH
pack=json.load(open(g.PACKS))['sienna']['face_refs']
grp=lambda p:'x2' if 'x2_dawn' in p else ('vid' if 'T1_wan' in p else p)
def run(p,excl=(),video=False):
    refs,c=g.get_refs('sienna',excl); im=cv2.imread(p if os.path.isabs(p) else R+p); return g.check_image(im,refs,c,ocr=False,video=video)
def ident_ok(r): return not any(x.startswith('identity') for x in r['reasons'])
def show(name,rows,video=False):
    ok=[ident_ok(r) for _,r in rows if r['score_centroid'] is not None]; n=len(rows)
    sc=[r['score_centroid'] for _,r in rows if r['score_centroid'] is not None]; bs=[r['score_best'] for _,r in rows if r['score_best'] is not None]
    print(f"{name}: n={n} identity-pass={sum(ok)} (no-face={n-len(sc)}) centroid {min(sc):.3f}-{max(sc):.3f} best {min(bs):.3f}-{max(bs):.3f}")
    return rows
print('thresholds',{k:T[k] for k in T if 'centroid' in k or 'best' in k or 'median' in k or 'floor' in k})
loo=[]
for p in pack:
    ex=[q for q in pack if grp(q)==grp(p)]; r=run(p,ex); loo.append((p,r))
    print(f"  LOO {os.path.basename(p):24s} cen={r['score_centroid']:.3f} best={r['score_best']:.3f} identity_ok={ident_ok(r)} {r['reasons']}")
stills=[(p,r) for p,r in loo if 'T1_wan' not in p]; vids=[(p,r) for p,r in loo if 'T1_wan' in p]
show('LOO approved stills (stills thresholds)',stills)
vl=[(p,run(p,[q for q in pack if grp(q)=='vid'],video=True)) for p,_ in vids]; show('LOO approved video-frame refs (video thresholds)',vl)
fr=sorted(glob.glob('/tmp/fr/*.png')); ex=[q for q in pack if 'T1_wan' in q]
held=[(f,run(f,ex,video=True)) for f in fr if os.path.basename(f) not in ('f02.png','f06.png','f10.png')]
for f,r in held: print('  heldout frame',os.path.basename(f),round(r['score_centroid'],3),round(r['score_best'],3),r['reasons'])
show('Held-out approved-video frames (video thresholds)',held)
neg=sorted(glob.glob(R+'posting_oct14/retrain/raw/*'))
def safe(p,v=False):
    try: return run(p,video=v)
    except Exception as e: return dict(pass_=False,reasons=['no_face'],score_centroid=None,score_best=None)
nr=[(p,safe(p)) for p in neg]; nr2=[(p,r) for p,r in nr if r['score_centroid'] is not None]
show('Retrain/raw rejects (stills thresholds)',nr2)
for p,r in nr: 
    if r['score_centroid'] is not None and ident_ok(r): print('   FALSE ACCEPT',os.path.basename(p),round(r['score_centroid'],3),round(r['score_best'],3))
show('Retrain/raw rejects (VIDEO thresholds)',[(p,safe(p,True)) for p,_ in nr2])
oth=[]
for m in ['camille','charlotte','madison','gabriela','valentina']:
    oth+=[p for p in sorted(glob.glob(R+f'keepers/{m}_*')) if p.endswith(('.png','.webp'))]
orr=[(p,safe(p)) for p in oth]; orr=[(p,r) for p,r in orr if r['score_centroid'] is not None]
show('Other models faces (stills thresholds)',orr); show('Other models faces (video thresholds)',[(p,safe(p,True)) for p,_ in orr])
old=['sienna_face_keeper.png','sienna_face_close.png','sienna_bikini1.png','sienna_bikini2.png','sienna_cover.png']
for n in old:
    r=safe(R+'keepers/'+n); print('  dropped ref',n,None if r['score_centroid'] is None else (round(r['score_centroid'],3),round(r['score_best'],3)),ident_ok(r))
