import sys,json,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting'); import identity_gate as g
E_,c=g.get_refs('charlotte'); out={}
for p in sys.argv[1:]:
    cap=cv2.VideoCapture(p); i=0; s=[]
    while True:
        ok,fr=cap.read()
        if not ok: break
        if i%4==0:
            f,_=g.faces(fr)
            s.append((i,float(c@max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])).normed_embedding) if f else None))
        i+=1
    out[p]=s; v=[x for _,x in s if x is not None]
    print(p,'min',round(min(v),3),'avg',round(np.mean(v),3),'none',sum(x is None for _,x in s),'low',[(i,round(x,3)) for i,x in s if x is None or x<0.78])
json.dump(out,open(sys.argv[0]+'.json','w'))
