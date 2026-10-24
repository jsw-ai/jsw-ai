#!/workspace/.face-venv/bin/python
# 12 fps per-frame gate at 0.78 centroid cutoff, built on identity_gate.py
import sys, json, cv2, numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting'); import identity_gate as g
CUT=0.78
refs,cent=g.get_refs('gabriela')
def run(p, out=None):
    if p.lower().endswith(('.jpg','.png')):
        r=g.check_image(cv2.imread(p),refs,cent,ocr=False); print(p, round(r['score_centroid'] or 0,3)); return
    cap=cv2.VideoCapture(p); fps=cap.get(cv2.CAP_PROP_FPS); n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); step=fps/12
    sc=[]; t=0.0
    while t<n:
        cap.set(cv2.CAP_PROP_POS_FRAMES,int(t)); ok,fr=cap.read()
        if not ok: break
        r=g.check_image(fr,refs,cent,ocr=False,video=True); sc.append(r['score_centroid'] or 0.0); t+=step
    sc=np.array(sc); below=sc<CUT; run_=mx=0
    for b in below: run_=run_+1 if b else 0; mx=max(mx,run_)
    res=dict(file=p,frames=len(sc),min=float(sc.min()),median=float(np.median(sc)),pass_frac=float((~below).mean()),longest_below_s=mx/12,
             pass_=bool((~below).mean()>=0.8 and mx/12<=0.5),scores=[round(float(x),3) for x in sc])
    print({k:v for k,v in res.items() if k!='scores'})
    if out: json.dump(res,open(out,'w'),indent=1)
    return res
if __name__=='__main__':
    for p in sys.argv[1:]: run(p, p.rsplit('.',1)[0]+'_gate12.json' if p.endswith('.mp4') else None)
