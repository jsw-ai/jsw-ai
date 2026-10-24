import sys,cv2,numpy as np
sys.path.insert(0,'/workspace/hf-test/zen/posting')
import identity_gate as g
from PIL import Image
files=sys.argv[2:];out=sys.argv[1]
tiles=[]
for f in ['/workspace/hf-test/keepers/gabriela_face_keeper.png']+files:
    im=cv2.imread(f);fs,_=g.faces(im)
    h,w=im.shape[:2]
    if max(h,w)>1280:
        s=1280/max(h,w);im=cv2.resize(im,(int(w*s),int(h*s)))
    if not fs: tiles.append(np.zeros((300,300,3),np.uint8));continue
    b=max(fs,key=lambda x:(x.bbox[2]-x.bbox[0])).bbox.astype(int)
    cx,cy=(b[0]+b[2])//2,(b[1]+b[3])//2;r=int(max(b[2]-b[0],b[3]-b[1])*0.85)
    p=cv2.copyMakeBorder(im,r,r,r,r,cv2.BORDER_CONSTANT,value=(60,60,60))
    c=p[cy:cy+2*r,cx:cx+2*r];tiles.append(cv2.resize(c,(300,300)))
cols=6;rows=(len(tiles)+cols-1)//cols
S=np.zeros((300*rows,300*cols,3),np.uint8)
for k,t in enumerate(tiles):S[(k//cols)*300:(k//cols+1)*300,(k%cols)*300:(k%cols+1)*300]=t
cv2.imwrite(out,S)
