import cv2,numpy as np,sys
from insightface.app import FaceAnalysis
A=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);A.prepare(ctx_id=-1,det_size=(640,640))
c=np.load('../redo3/centroid.npy');crops=[]
for f in sys.argv[2:]:
  im=cv2.imread(f);F=max(A.get(im),key=lambda x:x.bbox[2]-x.bbox[0]);print(f,round(float(F.normed_embedding@c),3))
  x1,y1,x2,y2=F.bbox;w=x2-x1;cx,cy=(x1+x2)/2,(y1+y2)/2;r=w*1.0
  crops.append(cv2.resize(im[max(0,int(cy-r)):int(cy+r),max(0,int(cx-r)):int(cx+r)],(300,300)))
cv2.imwrite(sys.argv[1],np.hstack(crops))
