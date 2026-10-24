import sys,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting');sys.path.insert(0,'work')
import identity_gate as g, matte
refs,cent=g.get_refs('camille_v3_draft')
def sc(im):
    f,_=g.faces(im);m=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]));return float(cent@m.normed_embedding),m.normed_embedding
S=['m_face1.png','m_face2.png','face3_crop.jpg','m_body1.png','b2_new.png','f3_new.png','b4_new.png','b5_new.png']
for sp in [0.6,0.75]:
    r=[]
    for i,f in enumerate(S):
        im=cv2.imread('../v2work/'+f);c0,e0=sc(im);o,_=matte.process(im,seed=i,SP=sp);c,e=sc(o);r.append(f'{f[:6]} {c0:.3f}->{c:.3f} ({e@e0:.3f})')
        cv2.imwrite(f'work/sp{sp}_{f.rsplit(".",1)[0]}.png',o)
    print(sp,' | '.join(r),flush=True)
