import sys,cv2,numpy as np
from insightface.app import FaceAnalysis
app=FaceAnalysis(allowed_modules=['detection','landmark_2d_106'],providers=['CPUExecutionProvider']); app.prepare(ctx_id=-1,det_size=(640,640))
for f in sys.argv[1:]:
    cap=cv2.VideoCapture(f); fps=cap.get(5); e=[]
    while True:
        ok,im=cap.read()
        if not ok: break
        fs=app.get(cv2.resize(im,(540,960)))
        if not fs: e.append(np.nan); continue
        L=max(fs,key=lambda x:x.bbox[2]-x.bbox[0]).landmark_2d_106
        r=[np.ptp(L[a:b,1])/np.ptp(L[a:b,0]) for a,b in ((33,43),(87,97))]; e.append(np.mean(r))
    e=np.array(e); base=np.nanmedian(e); cl=e<0.6*base
    runs=[];i=0
    while i<len(cl):
        if cl[i]:
            j=i
            while j<len(cl) and cl[j]: j+=1
            runs.append((round(i/fps,2),round((j-i)/fps,2))); i=j
        else: i+=1
    print(f,'closed runs (start,dur):',runs)
