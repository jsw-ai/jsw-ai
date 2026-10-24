#!/workspace/.face-venv/bin/python
import sys,json,cv2,numpy as np,os
sys.path.insert(0,'/workspace/hf-test/zen/posting')
import identity_gate as g
refs,cent=g.get_refs('sienna')
for p in sys.argv[1:]:
    cap=cv2.VideoCapture(p); fps=cap.get(cv2.CAP_PROP_FPS); res=[]; i=0
    while True:
        ok,fr=cap.read()
        if not ok: break
        if True:
            f,_=g.faces(fr); f=[x for x in f if x.det_score>=0.55]; s=None
            if f:
                m=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])); s=round(float(cent@m.normed_embedding),3)
            res.append((round(i/fps,2),s))
        i+=1
    sc=[s for _,s in res if s is not None]
    out={'file':p,'model':'sienna','frames_scored':len(sc),'frames_no_face':len(res)-len(sc),'median':float(np.median(sc)) if sc else None,'min':float(min(sc)) if sc else None,'lt70':sum(s<0.70 for s in sc),'per_frame':res}
    k=os.path.basename(p).rsplit('.',1)[0]
    json.dump(out,open(f'/workspace/jsw_tiktok/sienna/2026-10-22_daily/gate/v_{k}.json','w'))
    print(k,'med',round(out['median'],3),'min',out['min'],'noface',out['frames_no_face'],flush=True)
    print(' ', ' '.join(f"{t}:{s}" for t,s in res),flush=True)
