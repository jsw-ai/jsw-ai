import sys,cv2,numpy as np
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',allowed_modules=['detection'],providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(640,640))
out=[]
for f in sys.argv[2:]:
    im=cv2.imread(f);b=app.get(im)[0].bbox.astype(int);w=b[2]-b[0]
    c=im[max(0,b[1]-w//2):b[3]+w//3,max(0,b[0]-w//2):b[2]+w//2];out.append(cv2.resize(c,(400,int(400*c.shape[0]/c.shape[1]))))
h=min(o.shape[0] for o in out);cv2.imwrite(sys.argv[1],np.hstack([o[:h] for o in out]))
