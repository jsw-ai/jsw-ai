#!/workspace/.face-venv/bin/python
# per-frame face gate vs camille_v3 centroid. usage: vgate.py clip.mp4 [step_s=0.1] [out.json]
import sys,json,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting')
import identity_gate as g
refs,cent=g.get_refs('camille_v3')
p=sys.argv[1]; step=float(sys.argv[2]) if len(sys.argv)>2 else 0.1
cap=cv2.VideoCapture(p); fps=cap.get(cv2.CAP_PROP_FPS); n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
res=[]; t=0.0
while t< n/fps-1e-3:
    cap.set(cv2.CAP_PROP_POS_FRAMES,int(round(t*fps))); ok,fr=cap.read()
    if not ok: break
    f,_=g.faces(fr); f=[x for x in f if x.det_score>=0.55]
    if f:
        m=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
        res.append((round(t,2),round(float(cent@m.normed_embedding),3)))
    else: res.append((round(t,2),None))
    t+=step
sc=[s for _,s in res if s is not None]
line=' '.join(f"{t:.1f}:{'--' if s is None else f'{s:.2f}'}" for t,s in res)
print(p.split('/')[-1], f"fps={fps:.0f} dur={n/fps:.2f} scored={len(sc)} min={min(sc) if sc else None} med={np.median(sc) if sc else None:.3f} lt78={sum(s<0.78 for s in sc)}")
print(line)
if len(sys.argv)>3: json.dump(res,open(sys.argv[3],'w'))
