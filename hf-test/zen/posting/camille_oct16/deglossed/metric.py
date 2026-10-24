import cv2,numpy as np,sys
sys.path.insert(0,'.')
from pp import facebox
for n in (4,2,7,6):
    o=cv2.imread(f'../stills/camille_s{n}.jpg');b=facebox(o);x0,y0,x1,y1=[int(v) for v in b];w=x1-x0
    res=[]
    for f in (f'../stills/camille_s{n}.jpg',f'camille_s{n}_deglossed.jpg',f'camille_s{n}_extra_matte.jpg' if n!=2 else f'camille_s{n}_deglossed.jpg'):
        im=cv2.imread(f);L=cv2.cvtColor(im,cv2.COLOR_BGR2LAB)[...,0].astype(np.float32)
        c=L[y0+int(w*.15):y1-int(w*.1),x0+int(w*.15):x1-int(w*.15)]
        ycc=cv2.cvtColor(im,cv2.COLOR_BGR2YCrCb)[y0+int(w*.15):y1-int(w*.1),x0+int(w*.15):x1-int(w*.15)]
        sk=(ycc[...,1]>135)&(ycc[...,1]<185)&(ycc[...,2]>85)&(ycc[...,2]<135)
        base=cv2.GaussianBlur(c,(0,0),w*0.12);ex=np.clip(c-base,0,None)[sk]
        res.append('spec_excess %.2f  p99-med %.0f'%(ex.mean(),np.percentile(c[sk],99)-np.median(c[sk])))
    print(n,' | '.join(res))
