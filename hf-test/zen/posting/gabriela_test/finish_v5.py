import numpy as np, sys, cv2
from PIL import Image
sys.path.insert(0,'/workspace/hf-test/zen/posting')
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(640,640))
P='/workspace/hf-test/zen/posting/gabriela_test/'
G=lambda x,s: cv2.GaussianBlur(x,(0,0),s)
for k,name in enumerate(sys.argv[1:]):
    o=cv2.imread(P+'raw/%s.png'%name); W=1080; H=round(o.shape[0]*W/o.shape[1])
    o=cv2.resize(o,(W,H),interpolation=cv2.INTER_AREA); a=o.astype(np.float32)
    fs=app.get(o); f=max(fs,key=lambda f:(f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))
    x0,y0,x1,y1=f.bbox; cx,cy=(x0+x1)/2,(y0+y1)/2+ (y1-y0)*0.05; fw=x1-x0; fh=y1-y0
    yy,xx=np.mgrid[:H,:W].astype(np.float32)
    el=np.clip(1.25-np.sqrt(((xx-cx)/(fw*0.62))**2+((yy-cy)/(fh*0.66))**2),0,1); el=np.clip(el*1.6,0,1)
    # neck/chest/arms skin: broad skin mask w/ lower weight
    ycc=cv2.cvtColor(o,cv2.COLOR_BGR2YCrCb).astype(np.float32); Y=ycc[...,0];Cr=ycc[...,1];Cb=ycc[...,2]
    sk=((Cr>135)&(Cr<180)&(Cb>80)&(Cb<130)&(Y>50)).astype(np.float32); sk=G(sk,4)
    # protect eyes/brows/lips/hair edges: strong local edges
    e=G(np.abs(Y-G(Y,1.5)),2.5); prot=np.clip(1-(e-5)/7,0,1)
    mf=sk*np.clip(el,0,1)*prot; mb=sk*prot*0.45
    m=np.clip(np.maximum(mf,mb),0,1)[...,None]; mfa=mf[...,None]
    rng=np.random.default_rng(100+k)
    nz=lambda s:G(rng.normal(0,1,(H,W)).astype(np.float32),s)
    n1=nz(0.7);n1/=n1.std(); n2=nz(1.6);n2/=n2.std(); n3=nz(9);n3/=n3.std()
    lum=(Y/255)
    # pores: dark pits, mid-tone weighted
    pores=(n1*0.6+n2*0.4)
    pit=np.clip(-(nz(0.8)/nz(0.8).std())-1.4,0,3)  # sparse dark pits
    tex=pores*3.2 - pit*3.0
    # gloss compress: pull highlights in skin
    hl=np.clip((Y-185)/60,0,1)[...,None]
    a=a-hl*mfa*14 - hl*m*5
    # local contrast on skin (clarity): add detail layer from original
    yb=cv2.cvtColor(a.astype(np.uint8),cv2.COLOR_BGR2GRAY).astype(np.float32)
    det=yb-G(yb,2.2); mid=G(yb,5)-G(yb,18)
    a=a+((det*0.9+mid*0.35)*mf)[...,None]
    a=a+(tex*(0.5+0.5*(1-np.abs(lum-0.5)*1.4)))[...,None]*m*1.0
    # uneven tone: low-freq redness/yellow blotches (BGR)
    a=a+(n3*3.0)[...,None]*np.array([-0.8,0.2,1.0],np.float32)*mfa + (nz(4)/1*0)[...,None]
    # freckles / tiny marks, face only
    fr=np.clip(nz(1.3)/nz(1.3).std()-2.3,0,2.5); fr=G(fr,0.6)
    a=a-(fr*6)[...,None]*np.array([0.6,0.9,1.0],np.float32)*mfa
    # a couple faint blemishes
    for _ in range(3):
        bx=cx+rng.uniform(-0.38,0.38)*fw; by=cy+rng.uniform(-0.05,0.38)*fh
        d=np.exp(-(((xx-bx)**2+(yy-by)**2)/(2*(fw*0.012)**2)))
        a=a+(d*5)[...,None]*np.array([-1,0.2,1.0],np.float32)*mfa
    # overall stronger grain (luma + slight chroma)
    g=G(rng.normal(0,1,(H,W)).astype(np.float32),0.5)*4.5
    gc=G(rng.normal(0,1,(H,W,3)).astype(np.float32),0.8)*1.2
    a=a+g[...,None]*(0.8+0.4*(1-lum[...,None]))+gc
    cv2.imwrite(P+'fin2/%s_v5.jpg'%name,np.clip(a,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,90])
    print(name)
