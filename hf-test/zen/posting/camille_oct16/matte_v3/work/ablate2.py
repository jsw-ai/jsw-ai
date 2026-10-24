import sys,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting');sys.path.insert(0,'work')
import identity_gate as g, matte
refs,cent=g.get_refs('camille_v3_draft')
def sc(im):
    f,_=g.faces(im);m=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]));return float(cent@m.normed_embedding),m.normed_embedding
for src in ['../v2work/m_face1.png','../v2work/b2_new.png']:
    im=cv2.imread(src);c0,e0=sc(im);out=[f'{src.split("/")[-1]} orig {c0:.3f}']
    for name,kw in [('specL_only',dict(GL=0,TX=0,NZ=0,CH=0)),('chroma_only',dict(GL=0,TX=0,NZ=0,SP=1e-3,CH=1000)),('spec0.5',dict(GL=0,TX=0,NZ=0,SP=0.5)),('spec0.3',dict(GL=0,TX=0,NZ=0,SP=0.3))]:
        o,_=matte.process(im,**kw);c,e=sc(o);out.append(f'{name} {c:.3f}/{e@e0:.3f}')
    print(' | '.join(out),flush=True)
