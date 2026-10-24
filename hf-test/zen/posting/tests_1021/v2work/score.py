import sys,json,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting')
import identity_gate as g
refs,cent=g.get_refs('camille_v3_draft')
cap=cv2.VideoCapture(sys.argv[1]);out=[];i=0
while True:
    ok,f=cap.read()
    if not ok:break
    fs,_=g.faces(f); fs=[x for x in fs if x.det_score>=0.55]
    if fs:
        m=max(fs,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
        out.append((i,float(cent@m.normed_embedding),float(m.det_score),[int(v) for v in m.bbox]))
    else: out.append((i,None,None,None))
    i+=1
json.dump(out,open(sys.argv[2],'w'))
s=[o[1] for o in out if o[1] is not None]
print('frames',i,'scored',len(s),'min',min(s),'median',np.median(s))
print('low:',[(o[0],round(o[1],3)) for o in out if o[1] is not None and o[1]<0.78])
print('unscored:',[o[0] for o in out if o[1] is None])
