# usage: fc.py out.jpg img1 img2 ... ; face crops (biggest face, or ref top-left) + full thumbs + cosine to fk/b2
import sys,cv2,numpy as np,warnings;warnings.filterwarnings('ignore')
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(640,640))
def big(im):
    fs=app.get(im); return max(fs,key=lambda x:x.bbox[2]-x.bbox[0]) if fs else None
R=[big(cv2.imread(p)).normed_embedding for p in ['up/fk.jpg','up/b2.jpg']]
out=sys.argv[1];T=[];F=[]
for p in ['up/fk.jpg']+sys.argv[2:]:
    im=cv2.imread(p);f=big(im)
    th=cv2.resize(im,(360,int(360*im.shape[0]/im.shape[1])))[:480];th=cv2.copyMakeBorder(th,0,480-th.shape[0],0,0,0)
    if f is None: c=np.zeros((480,360,3),np.uint8);s=0
    else:
        x0,y0,x1,y1=f.bbox.astype(int);w=x1-x0;c=im[max(0,y0-w//3):y1+w//4,max(0,x0-w//4):x1+w//4];c=cv2.resize(c,(360,480));s=np.mean([f.normed_embedding@r for r in R])
    cv2.putText(c,f'{p.split("/")[-1][:14]} {s:.2f}',(5,25),0,0.7,(0,255,255),2);T.append(th);F.append(c);print(p,round(float(s),3))
cv2.imwrite(out,np.vstack([np.hstack(T),np.hstack(F)]),[cv2.IMWRITE_JPEG_QUALITY,85])
