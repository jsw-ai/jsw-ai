import sys,cv2,numpy as np
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',allowed_modules=['detection','landmark_2d_106'],providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(640,640))
cap=cv2.VideoCapture(sys.argv[1]);i=0;out=[]
while True:
    ok,f=cap.read()
    if not ok: break
    if i%3==0:
        F=app.get(f)
        if F:
            L=F[0].landmark_2d_106
            # left eye 33-42, right eye 87-96
            def ear(idx):
                p=L[idx];return (p[:,1].max()-p[:,1].min())/(p[:,0].max()-p[:,0].min()+1e-6)
            out.append((i/24,round(ear(list(range(33,43))),3),round(ear(list(range(87,97))),3)))
    i+=1
for t,a,b in out: print('%.2f %.3f %.3f %s'%(t,a,b,'CLOSED?' if (a+b)/2<0.22 else ''))
