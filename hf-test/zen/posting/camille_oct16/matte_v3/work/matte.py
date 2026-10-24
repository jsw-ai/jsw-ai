import cv2,numpy as np,sys,os
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(1024,1024))
def getface(im):
    fs=app.get(im);off=0
    if not fs:
        off=400;fs=app.get(cv2.copyMakeBorder(im,off,off,off,off,cv2.BORDER_REFLECT))
    f=max(fs,key=lambda f:(f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))
    return f.bbox-off,f.landmark_2d_106-off
def masks(im,b,lm):
    h,w=im.shape[:2];bw,bh=b[2]-b[0],b[3]-b[1]
    # face region: hull of jaw contour (0-32) + forehead extension
    jaw=lm[0:33];brow=lm[43:52].tolist()+lm[97:106].tolist()
    top=np.array(brow);cx=lm[:,0].mean()
    fore=top.copy();fore[:,1]-=bh*0.28
    hull=cv2.convexHull(np.vstack([jaw,top,fore]).astype(np.int32))
    F=np.zeros((h,w),np.float32);cv2.fillConvexPoly(F,hull,1)
    # exclude eyes (35-42 left, 89-96 right) & brows a bit
    E=np.zeros((h,w),np.uint8)
    for idx in (range(33,43),range(87,97)):
        pts=lm[list(idx)].astype(np.int32);hl=cv2.convexHull(pts)
        cv2.fillConvexPoly(E,hl,1)
    E=cv2.dilate(E,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(bw*0.06)|1,)*2)).astype(np.float32)
    M=np.zeros((h,w),np.uint8);cv2.fillConvexPoly(M,cv2.convexHull(lm[52:72].astype(np.int32)),1)
    M=cv2.GaussianBlur(M.astype(np.float32),(0,0),bw*0.01)
    ycc=cv2.cvtColor(im,cv2.COLOR_BGR2YCrCb).astype(int);cr,cb=ycc[...,1],ycc[...,2]
    sk=((cr>133)&(cr<180)&(cb>80)&(cb<130)).astype(np.float32)
    sk=cv2.GaussianBlur(sk,(0,0),max(2,bw*0.01))
    F=cv2.GaussianBlur(F,(0,0),bw*0.03)
    E=cv2.GaussianBlur(E,(0,0),bw*0.015)
    skin=F*sk*(1-E)*(1-M)
    return np.clip(skin,0,1),np.clip(M*F,0,1),bw
def process(im,seed=0,S=1.0,SP=0.6,CH=1.0,KN=1.0,GL=1.0,TX=1.0,NZ=1.0):
    rng=np.random.default_rng(seed)
    b,lm=getface(im);skin,lips,bw=masks(im,b,lm);h,w=im.shape[:2]
    lab=cv2.cvtColor(im,cv2.COLOR_BGR2LAB).astype(np.float32);L=lab[...,0]*100/255
    # 1) specular: L above local base (soft knee), compress toward diffuse
    base=cv2.GaussianBlur(L,(0,0),bw*0.06)
    Ls=cv2.GaussianBlur(L,(0,0),max(1.5,bw*0.008))   # keep fine texture: only compress low-freq sheen
    ex=Ls-base-KN
    ex=np.where(ex>0,ex,0)
    spec=0.6*ex
    spec=cv2.GaussianBlur(spec,(0,0),max(1,bw*0.003))
    L2=L-SP*spec*skin*S-SP*0.45*np.clip(L-base-2,0,None)*lips*S
    # 2) de-glow: reduce positive mid-frequency bloom (clarity glow), gently
    g=cv2.GaussianBlur(L2,(0,0),bw*0.02)-cv2.GaussianBlur(L2,(0,0),bw*0.10)
    L2=L2-GL*0.22*np.clip(g,0,None)*skin*S
    # 3) pore texture
    ps=max(0.7,bw/450)
    n=rng.standard_normal((h,w)).astype(np.float32)
    pore=cv2.GaussianBlur(n,(0,0),ps)-cv2.GaussianBlur(n,(0,0),ps*3);pore/=pore.std()+1e-6
    pore=np.where(pore<0,pore*1.3,pore*0.5)
    fine=cv2.GaussianBlur(rng.standard_normal((h,w)).astype(np.float32),(0,0),ps*0.5);fine/=fine.std()+1e-6
    hf=L-cv2.GaussianBlur(L,(0,0),ps*2);var=np.sqrt(cv2.GaussianBlur(hf*hf,(0,0),bw*0.03))
    smooth=np.clip(1.1-var/1.5,0.25,1.0)
    # texture a bit stronger on hot zones (where shine hid it)
    hot=np.clip(spec/4,0,1)
    L2=L2+TX*(0.6*pore+0.25*fine)*skin*smooth*(1+0.6*hot)*S
    lab[...,0]=np.clip(L2*255/100,0,255)
    # 4) hot spots: pull chroma to surrounding diffuse skin colour (stops grey patches), tiny desat
    hm=(CH*SP*hot*skin*S)[...,None]
    abl=cv2.GaussianBlur(lab[...,1:],(0,0),bw*0.05)
    lab[...,1:]=lab[...,1:]*(1-0.8*hm)+abl*(0.8*hm)
    lab[...,1:]=128+(lab[...,1:]-128)*(1-0.06*hm)
    out=cv2.cvtColor(lab.astype(np.uint8) if False else np.clip(lab,0,255).astype(np.uint8),cv2.COLOR_LAB2BGR).astype(np.float32)
    # 5) mild phone sensor noise over whole frame (luma + faint chroma), scale with resolution
    s=max(0.6,w/1800)
    ln=cv2.GaussianBlur(rng.standard_normal((h,w)).astype(np.float32),(0,0),0.6*s)
    ln=ln/ln.std()*1.1
    cn=cv2.GaussianBlur(rng.standard_normal((h,w,3)).astype(np.float32),(0,0),1.5*s);cn=cn/cn.std()*0.45
    out=out+NZ*(ln[...,None]+cn)
    return np.clip(out,0,255).astype(np.uint8),dict(skin=skin)
if __name__=='__main__':
    S=float(os.environ.get('S','1'))
    for i,(src,dst) in enumerate(zip(sys.argv[1::2],sys.argv[2::2])):
        im=cv2.imread(src);o,d=process(im,seed=i,S=S)
        cv2.imwrite(dst,o,[cv2.IMWRITE_PNG_COMPRESSION,3]) if dst.endswith('png') else cv2.imwrite(dst,o,[cv2.IMWRITE_JPEG_QUALITY,95])
        cv2.imwrite(dst.rsplit('.',1)[0]+'_mask.jpg',(d['skin']*255).astype(np.uint8));print(dst)
