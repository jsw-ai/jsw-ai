import sys,glob,cv2,numpy as np
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']); app.prepare(ctx_id=-1,det_size=(640,640))
d,out=sys.argv[1],sys.argv[2]; fs=sorted(glob.glob(d+'/e_*.png')); tiles=[]
for f in fs:
    im=cv2.imread(f); fa=app.get(im)
    if not fa: t=np.zeros((300,240,3),np.uint8)
    else:
        x1,y1,x2,y2=max(fa,key=lambda a:(a.bbox[2]-a.bbox[0])).bbox; cx,cy=(x1+x2)/2,(y1+y2)/2; h=(y2-y1)*1.5; w=h*0.8
        X1,Y1=int(max(0,cx-w/2)),int(max(0,cy-h/2)); t=im[Y1:int(Y1+h),X1:int(X1+w)]; t=cv2.resize(t,(240,300),interpolation=cv2.INTER_AREA if t.shape[0]>300 else cv2.INTER_CUBIC)
    cv2.putText(t,f[-7:-4],(4,18),0,0.5,(0,255,255),1); tiles.append(t)
while len(tiles)%5: tiles.append(np.zeros((300,240,3),np.uint8))
rows=[np.hstack(tiles[i:i+5]) for i in range(0,len(tiles),5)]
cv2.imwrite(out,np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,92]); print(out,len(fs))
