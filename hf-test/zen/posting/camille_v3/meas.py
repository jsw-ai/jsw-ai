import sys,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting'); sys.path.insert(0,'/workspace/hf-test')
import insightface
from insightface.app import FaceAnalysis
a=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);a.prepare(ctx_id=-1,det_size=(640,640))
import glob
fs={'face_front':'camille_v3/refs/face_front.png','r3_4_full':'camille_v2/raw/r3_4.png','three_quarter':'camille_v3/raw/three_quarter.png','neutral_off':'camille_v3/raw/neutral_off.png'}
E={}
for n,p in fs.items():
    im=cv2.imread(p);f=a.get(im)
    if not f: print(n,'noface');continue
    x=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]));b=x.bbox.astype(int);x0,y0,x1,y1=[max(0,v) for v in b]
    c=cv2.cvtColor(im[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY)
    # also normalised to 256px face
    c2=cv2.resize(c,(256,256));E[n]=x.normed_embedding
    print(n,'facepx',x1-x0,'lap %.0f'%cv2.Laplacian(c,cv2.CV_64F).var(),'lap256 %.0f'%cv2.Laplacian(c2,cv2.CV_64F).var())
for n in E:print(n,{m:round(float(E[n]@E[m]),2) for m in E if m!=n})
