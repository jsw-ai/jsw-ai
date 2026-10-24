#!/workspace/.face-venv/bin/python
# Per-frame gate (Hard Rule): median of scored face frames >= 0.78 and no scored frame < 0.70. No-face frames (turned away) are exempt.
import sys, json, cv2, numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting'); import identity_gate as g
refs,cent=g.get_refs('gabriela')
FPS=float(__import__('os').environ.get('GFPS','12'))
def run(p):
    cap=cv2.VideoCapture(p); fps=cap.get(cv2.CAP_PROP_FPS); n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); step=max(1.0,fps/FPS)
    out=[]; t=0.0
    while t<n:
        cap.set(cv2.CAP_PROP_POS_FRAMES,int(t)); ok,fr=cap.read()
        if not ok: break
        r=g.check_image(fr,refs,cent,ocr=False,video=True); s=r.get('score_centroid')
        out.append((round(int(t)/fps,3), None if s is None else round(float(s),3))); t+=step
    sc=np.array([s for _,s in out if s is not None])
    res=dict(file=p,frames=len(out),scored=int(len(sc)),median=float(np.median(sc)) if len(sc) else None,min=float(sc.min()) if len(sc) else None,
             n_below_070=int((sc<0.70).sum()),n_below_078=int((sc<0.78).sum()))
    res['pass_']=bool(len(sc) and res['median']>=0.78 and res['min']>=0.70)
    res['scores']=out
    json.dump(res,open(p.rsplit('.',1)[0]+'_pf.json','w'),indent=0)
    print({k:v for k,v in res.items() if k!='scores'}, flush=True)
for p in sys.argv[1:]: run(p)
