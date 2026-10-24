import sys,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting');sys.path.insert(0,'work')
import identity_gate as g, matte
refs,cent=g.get_refs('camille_v3_draft')
def sc(im):
    f,_=g.faces(im);m=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]));return float(cent@m.normed_embedding),m.normed_embedding
for f in ['m_face1.png','b2_new.png']:
    im=cv2.imread('../v2work/'+f);c0,e0=sc(im);r=[f'{f} {c0:.3f}']
    for nm,kw in [('kn3',dict(KN=3)),('kn5',dict(KN=5)),('kn3_sp1.3',dict(KN=3,SP=1.3)),('kn3_specOnly',dict(KN=3,GL=0,TX=0,NZ=0))]:
        o,_=matte.process(im,**kw);c,e=sc(o);r.append(f'{nm} {c:.3f} ({e@e0:.3f})');cv2.imwrite(f'work/{nm}_{f}',o)
    print(' | '.join(r),flush=True)
