import sys,cv2,numpy as np
from insightface.app import FaceAnalysis
a=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);a.prepare(ctx_id=-1,det_size=(640,640))
fs={'r3_4':'camille_v2/raw/r3_4.png','old_3q':'camille_v3/raw/three_quarter.png','old_neu':'camille_v3/raw/neutral_off.png'}
for n in ['tq_A','tq_B','neu_A','neu_B']: fs[n]='camille_v3/raw_b/%s.png'%n
E={}
for n,p in fs.items():
    im=cv2.imread(p);f=a.get(im)
    x=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]));x0,y0,x1,y1=[max(0,int(v)) for v in x.bbox]
    c=cv2.cvtColor(im[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY);c2=cv2.resize(c,(256,256))
    # sheen: fraction of bright specular px in central skin region (cheeks/nose)
    h,w=c.shape;r=c[int(h*.3):int(h*.8),int(w*.2):int(w*.8)]
    sp=(r>np.percentile(c,99)*0.0+ 215).mean()
    E[n]=x.normed_embedding
    print(n,'facepx',x1-x0,'lap %.0f lap256 %.0f'%(cv2.Laplacian(c,cv2.CV_64F).var(),cv2.Laplacian(c2,cv2.CV_64F).var()),'spec>215 %.3f'%sp,'p99 %d'%np.percentile(r,99),'cos_r34 %.2f'%float(E[n]@E['r3_4']))
