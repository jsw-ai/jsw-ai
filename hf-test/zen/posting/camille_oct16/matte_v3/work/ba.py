import cv2,numpy as np,sys
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(1024,1024))
pairs=[l.split(',') for l in sys.argv[2:]];out=sys.argv[1]
rows=[]
for a,bp in pairs:
    im=cv2.imread(a);fs=app.get(im);off=0;A=im;B=cv2.imread(bp)
    if not fs:
        off=400;A=cv2.copyMakeBorder(im,off,off,off,off,cv2.BORDER_REFLECT);B=cv2.copyMakeBorder(B,off,off,off,off,cv2.BORDER_REFLECT);fs=app.get(A)
    f=max(fs,key=lambda f:(f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]));b=f.bbox.astype(int);m=int((b[2]-b[0])*0.12)
    sl=(slice(max(b[1]-m,0),b[3]+m),slice(max(b[0]-m,0),b[2]+m))
    rows.append((cv2.resize(A[sl],(420,520),interpolation=cv2.INTER_AREA),cv2.resize(B[sl],(420,520),interpolation=cv2.INTER_AREA)))
n=len(rows);half=(n+1)//2
def strip(rs):
    top=np.hstack([r[0] for r in rs]);bot=np.hstack([r[1] for r in rs]);return np.vstack([top,bot])
s1=strip(rows[:half]);s2=strip(rows[half:]) if n>half else None
if s2 is not None and s2.shape[1]<s1.shape[1]: s2=np.hstack([s2,np.full((s2.shape[0],s1.shape[1]-s2.shape[1],3),255,np.uint8)])
img=np.vstack([s1,np.full((20,s1.shape[1],3),255,np.uint8),s2]) if s2 is not None else s1
cv2.imwrite(out,img,[cv2.IMWRITE_JPEG_QUALITY,92])
