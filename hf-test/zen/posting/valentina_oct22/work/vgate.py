# per-frame face gate on EVERY frame of a video vs valentina pack centroid
import sys,json,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting')
import identity_gate as g
E_,c=g.get_refs('valentina')
def score(fr):
    f,(W,H)=g.faces(fr); f=[x for x in f if x.det_score>=0.55]
    if not f: return None
    m=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
    return float(c@m.normed_embedding)
def run(p,step=1):
    cap=cv2.VideoCapture(p);fps=cap.get(5);out=[];i=0
    while True:
        ok,fr=cap.read()
        if not ok:break
        if i%step==0: out.append((round(i/fps,3),score(fr)))
        i+=1
    return out
if __name__=='__main__':
    p=sys.argv[1];step=int(sys.argv[2]) if len(sys.argv)>2 else 1
    r=run(p,step);s=[x for _,x in r if x is not None]
    res=dict(file=p,frames=len(r),scored=len(s),unscored=len(r)-len(s),median=float(np.median(s)) if s else None,min=float(min(s)) if s else None,
             below70=sum(x<0.70 for x in s),below78=sum(x<0.78 for x in s),per_frame=r)
    res['PASS']=bool(s) and res['median']>=0.78 and res['min']>=0.70
    out=sys.argv[3] if len(sys.argv)>3 else p.rsplit('.',1)[0]+'_gate.json'
    json.dump(res,open(out,'w'))
    print(p,'frames',res['frames'],'scored',res['scored'],'median %.3f min %.3f'%(res['median'] or 0,res['min'] or 0),'<.70:',res['below70'],'<.78:',res['below78'],'PASS' if res['PASS'] else 'FAIL')
