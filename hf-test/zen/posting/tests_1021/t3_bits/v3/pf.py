# every-frame gate using identity_gate internals
import sys, json, numpy as np, cv2
sys.path.insert(0,'/workspace/hf-test/zen/posting'); import identity_gate as g
refs, cent = g.get_refs('charlotte'); cap=cv2.VideoCapture(sys.argv[1]); fps=cap.get(5); out=[]; i=0
while True:
    ok, fr = cap.read()
    if not ok: break
    f,_ = g.faces(fr); f=[x for x in f if x.det_score>=0.55]
    if f:
        m=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])); out.append((i, round(i/fps,2), float(cent@m.normed_embedding)))
    else: out.append((i, round(i/fps,2), None))
    i+=1
s=[x[2] for x in out if x[2] is not None]
print('frames',i,'scored',len(s),'median %.4f min %.4f'%(np.median(s),min(s)),'n<.70',sum(v<.70 for v in s),'noface',i-len(s))
json.dump(out,open(sys.argv[1]+'.pf.json','w'))
