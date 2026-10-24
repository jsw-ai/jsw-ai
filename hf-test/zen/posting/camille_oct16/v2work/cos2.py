import cv2,numpy as np,itertools
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(1024,1024))
def emb(p):
    im=cv2.imread(p);h,w=im.shape[:2];s=1280/max(h,w)
    if s<1: im=cv2.resize(im,None,fx=s,fy=s)
    fs=app.get(im)
    if not fs:
        im=cv2.copyMakeBorder(im,300,300,300,300,cv2.BORDER_CONSTANT,value=(128,128,128));fs=app.get(im)
    if not fs: return None
    f=max(fs,key=lambda f:(f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]));return f.normed_embedding
P={'face1_orig':'refs/ref_face_front.jpg','face2_orig':'refs/ref_face_tq_matte.jpg','body1_orig':'refs/ref_body_waistup.jpg',
'face1_m':'v2work/m_face1.png','face2_m':'v2work/m_face2.png','body1_m':'v2work/m_body1.png',
'b2_old':'v2work/u_s2.jpg','b2_new':'v2work/b2_new.png','b4_old':'v2work/u_s6.jpg','b4_new':'v2work/b4_new.png','b5_old':'v2work/u_s7.jpg','b5_new':'v2work/b5_new.png','b3_old':'v2work/u_s10.jpg','b3_new':'v2work/f3_new.png','s4_deg':'deglossed/camille_s4_deglossed.jpg'}
E={k:emb(v) for k,v in P.items()}
ref=np.mean([E['face1_orig'],E['face2_orig'],E['body1_orig']],0);ref/=np.linalg.norm(ref)
for k,e in E.items():
    print(k, None if e is None else (round(float(e@ref),3), round(float(e@E['face1_orig']),3)))
for a,b in [('face1_m','face1_orig'),('face2_m','face2_orig'),('body1_m','body1_orig'),('b2_new','b2_old'),('b4_new','b4_old'),('b5_new','b5_old'),('b3_new','b3_old')]:
    print('pair',a,b,round(float(E[a]@E[b]),3))
