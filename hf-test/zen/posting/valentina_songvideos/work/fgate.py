import sys,json,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting'); import identity_gate as g
E_,c=g.get_refs('valentina')
def score(fr):
    f,_=g.faces(fr); f=[x for x in f if x.det_score>=0.55]
    if not f: return None
    m=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])); return float(c@m.normed_embedding)
for n in (sys.argv[1:] if __name__=="__main__" else []):
    p=f'../{n}.mp4';cap=cv2.VideoCapture(p);i=0;rows=[]
    while True:
        ok,fr=cap.read()
        if not ok:break
        if i%3==0: rows.append((i,round(i/30,3),score(fr)))
        i+=1
    with open(f'../gate_{n}.csv','w') as f:
        f.write('frame,t,centroid\n'); [f.write(f"{a},{b},{'' if s is None else round(s,4)}\n") for a,b,s in rows]
    s=[x for *_,x in rows if x is not None]
    print(n,'frames',len(rows),'scored',len(s),'median %.3f min %.3f'%(np.median(s),min(s)),'<.70',sum(x<.7 for x in s),'<.78',sum(x<.78 for x in s),'PASS' if np.median(s)>=.78 and min(s)>=.70 else 'FAIL',flush=True)
