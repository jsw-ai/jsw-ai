#!/workspace/.face-venv/bin/python
import sys,json,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting')
import identity_gate as g
refs,cent=g.get_refs('camille_v3')
for p in sys.argv[1:]:
    k=p.split('/')[-1].replace('camille_oct22_','').replace('_silent.mp4','')
    cap=cv2.VideoCapture(p); fps=cap.get(cv2.CAP_PROP_FPS); n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); res=[]; i=0
    while True:
        ok,fr=cap.read()
        if not ok: break
        if i%3==0:
            f,_=g.faces(fr); f=[x for x in f if x.det_score>=0.55]
            s=None
            if f:
                m=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])); s=round(float(cent@m.normed_embedding),3)
            res.append((round(i/fps,2),s))
        i+=1
    sc=[s for _,s in res if s is not None]
    out={'file':p,'model':'camille_v3','step_s':0.1,'frames_scored':len(sc),'frames_no_face':len(res)-len(sc),'median':float(np.median(sc)),'min':float(min(sc)),'lt70':sum(s<0.70 for s in sc),'per_frame':res}
    json.dump(out,open(f'/workspace/hf-test/zen/posting/camille_oct22/qc/gate_final_{k}.json','w'),indent=0)
    print(k,'med',round(out['median'],3),'min',out['min'],'noface',out['frames_no_face'],flush=True)
