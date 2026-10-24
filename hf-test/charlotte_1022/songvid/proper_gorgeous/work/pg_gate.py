#!/workspace/.face-venv/bin/python
# usage: pg_gate.py OUTDIR step files...   (one process, model loaded once)
import sys,json,cv2,numpy as np,os
sys.path.insert(0,'/workspace/hf-test/zen/posting')
import identity_gate as g
refs,cent=g.get_refs('charlotte')
od=sys.argv[1]; step=int(sys.argv[2]); os.makedirs(od,exist_ok=True)
def sc(fr):
    f,_=g.faces(fr); f=[x for x in f if x.det_score>=0.55]
    if not f: return None
    m=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])); return round(float(cent@m.normed_embedding),4)
for p in sys.argv[3:]:
    k=os.path.basename(p).rsplit('.',1)[0]
    if p.lower().endswith(('.jpg','.png','.jpeg')):
        s=sc(cv2.imread(p)); out={'file':p,'still':s,'pass':s is not None and s>=0.78}
    else:
        cap=cv2.VideoCapture(p); fps=cap.get(cv2.CAP_PROP_FPS) or 30; res=[]; i=0
        while True:
            ok,fr=cap.read()
            if not ok: break
            if i%step==0: res.append((round(i/fps,3),sc(fr)))
            i+=1
        v=[s for _,s in res if s is not None]
        out={'file':p,'fps':fps,'step':step,'frames_scored':len(v),'no_face':len(res)-len(v),'median':float(np.median(v)) if v else None,'min':float(min(v)) if v else None,'lt70':sum(s<0.70 for s in v),'per_frame':res}
        out['pass']=bool(v) and out['median']>=0.78 and out['lt70']==0
    json.dump(out,open(f'{od}/{k}.json','w'))
    print(k,{x:out.get(x) for x in ('still','median','min','lt70','no_face','pass')},flush=True)
