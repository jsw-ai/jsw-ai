import sys,cv2,numpy as np
from insightface.app import FaceAnalysis
src,dst,out=sys.argv[1:4]
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(640,640))
S=cv2.imread(src);D=cv2.imread(dst)
fs=max(app.get(S),key=lambda f:f.bbox[2]-f.bbox[0]);fd=max(app.get(D),key=lambda f:f.bbox[2]-f.bbox[0])
M,_=cv2.estimateAffinePartial2D(fs.landmark_2d_106,fd.landmark_2d_106)
W=cv2.warpAffine(S,M,(D.shape[1],D.shape[0]),flags=cv2.INTER_LANCZOS4)
x0,y0,x1,y1=fd.bbox;cx,cy=(x0+x1)/2,(y0+y1)/2-0.05*(y1-y0)
m=np.zeros(D.shape[:2],np.float32);cv2.ellipse(m,(int(cx),int(cy)),(int((x1-x0)*float(sys.argv[4] if len(sys.argv)>4 else 0.62)),int((y1-y0)*0.72)),0,0,360,1,-1)
k=int((x1-x0)*0.25)|1;m=cv2.GaussianBlur(m,(k,k),0)[...,None]
cv2.imwrite(out,(W*m+D*(1-m)).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,95]);print(out)
