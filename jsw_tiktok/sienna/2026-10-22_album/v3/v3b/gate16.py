import sys,json,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting'); import identity_gate as g
E,c=g.load_embs(['/workspace/hf-test/zen/posting/sienna_refs/story1_a_v4C.jpg']),None
ref=E[0]; out=[]
for i,fr in g.sample_frames(sys.argv[1],16):
    F,(W,H)=g.faces(fr); m=max(F,key=lambda x:x.bbox[2]-x.bbox[0])
    out.append([round(i/30,3),round(float(ref@m.normed_embedding),3),round(float((m.bbox[0]+m.bbox[2])/2/W),3),round(float(m.det_score*100),1)])
json.dump(out,open(sys.argv[2],'w')); print(out); print('min',min(o[1] for o in out))
