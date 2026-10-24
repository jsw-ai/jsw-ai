import cv2,sys,numpy as np
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(1024,1024))
S=['v2work/m_face1.png','v2work/m_face2.png','v2work/face3_crop.jpg','v2work/m_body1.png','v2work/b2_new.png','v2work/f3_new.png','v2work/b4_new.png','v2work/b5_new.png']
tiles=[]
for p in (sys.argv[1:] or S):
    im=cv2.imread(p);fs=app.get(im)
    if not fs:
        pad=cv2.copyMakeBorder(im,400,400,400,400,cv2.BORDER_REFLECT);fs=app.get(pad);off=400;im2=pad
    else: off=0;im2=im
    f=max(fs,key=lambda f:(f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]));b=f.bbox.astype(int)
    m=int((b[2]-b[0])*0.15);c=im2[max(b[1]-m,0):b[3]+m,max(b[0]-m,0):b[2]+m]
    tiles.append(cv2.resize(c,(500,600)));print(p,b-off)
cv2.imwrite('matte_v3/work/orig_faces.jpg',np.vstack([np.hstack(tiles[:4]),np.hstack(tiles[4:])]))
