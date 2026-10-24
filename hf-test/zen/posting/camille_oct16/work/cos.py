import cv2,sys,numpy as np
from insightface.app import FaceAnalysis
a=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);a.prepare(ctx_id=-1,det_size=(640,640))
def emb(p):
    im=cv2.imread(p);h,w=im.shape[:2];s=1280/max(h,w);im=cv2.resize(im,(int(w*s),int(h*s)))
    f=a.get(im);
    if not f: return None,0
    x=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]));return x.normed_embedding,(x.bbox[3]-x.bbox[1])/im.shape[0]
refs=[emb(p)[0] for p in ['camille_v2/raw/r3_4.png','camille_v3/refs/face_front.png','camille_v3/refs/face_three_quarter_matte.png','camille_v3/refs/face_neutral_off_matte.png']]
for p in sys.argv[1:]:
    e,fr=emb(p)
    print(p.split('/')[-1], 'NOFACE' if e is None else ' '.join('%.2f'%float(e@r) for r in refs)+'  facefrac %.2f'%fr)
