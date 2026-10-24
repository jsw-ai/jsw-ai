import sys,json,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting'); import identity_gate as g
E_,c=g.get_refs('valentina')
def score(fr):
    f,_=g.faces(fr); f=[x for x in f if x.det_score>=0.55]
    if not f: return None
    m=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])); return float(c@m.normed_embedding)
out={}
for p in open('stills.txt').read().split():
    out[p]=dict(kind='still',score=score(cv2.imread(p))); print(p,out[p],flush=True)
for p in open('clips.txt').read().split():
    cap=cv2.VideoCapture(p);fps=cap.get(5);W=cap.get(3);H=cap.get(4);r=[];i=0
    while True:
        ok,fr=cap.read()
        if not ok:break
        if i%6==0: r.append((round(i/fps,3),score(fr)))
        i+=1
    out[p]=dict(kind='clip',W=W,H=H,fps=fps,dur=i/fps,per=r); s=[x for _,x in r if x]
    print(p,W,H,round(i/fps,2),'med %.3f min %.3f'%(np.median(s),min(s)) if s else 'noface',flush=True)
    json.dump(out,open('src_gate2.json','w'))
json.dump(out,open('src_gate2.json','w'))
