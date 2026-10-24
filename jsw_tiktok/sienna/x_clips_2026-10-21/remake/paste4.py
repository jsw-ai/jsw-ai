import sys,cv2,numpy as np
from insightface.app import FaceAnalysis
src,dst,out=sys.argv[1:4]
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(640,640))
S=cv2.imread(src);D=cv2.imread(dst)
g=lambda im:max(app.get(im),key=lambda f:f.bbox[2]-f.bbox[0])
fs,fd=g(S),g(D)
M,_=cv2.estimateAffinePartial2D(fs.landmark_2d_106,fd.landmark_2d_106)
W=cv2.warpAffine(S,M,(D.shape[1],D.shape[0]),flags=cv2.INTER_LANCZOS4)
l=fd.landmark_2d_106.astype(np.int32);x0,y0,x1,y1=fd.bbox;w=int(x1-x0)
m=np.zeros(D.shape[:2],np.uint8);cv2.ellipse(m,(int((x0+x1)/2),int((y0+y1)/2)),(int(w*0.6),int((y1-y0)*0.66)),0,0,360,255,-1)
top=int(l[:,1].min()-0.12*w);m[:max(top,0)]=0
m=cv2.GaussianBlur(m.astype(np.float32)/255,(0,0),w/22)[...,None]
# colour match in LAB inside mask
Wl=cv2.cvtColor(W,cv2.COLOR_BGR2LAB).astype(np.float32);Dl=cv2.cvtColor(D,cv2.COLOR_BGR2LAB).astype(np.float32)
k=m[...,0]>0.5
for c in range(3):
    Wl[...,c]=(Wl[...,c]-Wl[...,c][k].mean())/(Wl[...,c][k].std()+1e-6)*Dl[...,c][k].std()+Dl[...,c][k].mean()
W=cv2.cvtColor(np.clip(Wl,0,255).astype(np.uint8),cv2.COLOR_LAB2BGR)
cv2.imwrite(out,(W*m+D*(1-m)).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,95])
