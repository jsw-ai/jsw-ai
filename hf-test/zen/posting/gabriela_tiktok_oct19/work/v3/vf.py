# vf.py out.jpg clip1 clip2 ... : per clip, Gabriela face crops (max-sim face) at 6 times + per-0.25s score list to json
import sys,cv2,numpy as np,json,warnings;warnings.filterwarnings('ignore')
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(640,640))
def big(im):
    fs=app.get(im); return max(fs,key=lambda x:x.bbox[2]-x.bbox[0])
R=[big(cv2.imread(p)).normed_embedding for p in ['up/fk.jpg','up/b2.jpg']]
def best(im):
    fs=app.get(im)
    if not fs: return None,0
    sc=[np.mean([f.normed_embedding@r for r in R]) for f in fs]; i=int(np.argmax(sc)); return fs[i],sc[i]
rows=[];allsc={}
ref=cv2.resize(cv2.imread('up/fk.jpg')[150:900,250:950],(240,300))
for p in sys.argv[2:]:
    cap=cv2.VideoCapture(p);fps=cap.get(5);n=int(cap.get(7));row=[ref];scs=[]
    for k in range(0,n,max(1,int(fps/4))):
        cap.set(1,k);ok,fr=cap.read()
        if not ok: break
        f,s=best(fr);scs.append(round(float(s),3))
    for t in [0.2,1.0,1.8,2.6,3.4,4.2,4.9]:
        cap.set(1,int(t*fps));ok,fr=cap.read();f,s=best(fr)
        if f is None: c=np.zeros((300,240,3),np.uint8)
        else:
            x0,y0,x1,y1=f.bbox.astype(int);w=x1-x0;c=cv2.resize(fr[max(0,y0-w//4):y1+w//5,max(0,x0-w//5):x1+w//5],(240,300))
        cv2.putText(c,f'{p.split("/")[-1][:6]} {t} {s:.2f}',(4,20),0,0.55,(0,255,255),2);row.append(c)
    rows.append(np.hstack(row));allsc[p]=scs;print(p,'med',np.median(scs),'min',min(scs),scs)
cv2.imwrite(sys.argv[1],np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,85]);json.dump(allsc,open(sys.argv[1]+'.json','w'))
