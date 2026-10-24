import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont
P='/workspace/hf-test/zen/posting/camille_oct22/'
def f(a): return np.asarray(a).astype(np.float32)
def blur(x,r): return f(Image.fromarray(np.clip(x,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)))
def blurf(x,r):  # float-safe blur via offset
    return blur(x+128,r)-128
def grain(a,seed):
    rng=np.random.default_rng(seed)
    g=blurf(rng.normal(0,3.0,a.shape[:2]).astype(np.float32),0.4)[...,None]
    return a+g
def sharpen(a,amt=0.35):
    return a+(a-np.stack([blur(a[...,i],1.0) for i in range(3)],-1))*amt
def save(a,p): Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save(p,'JPEG',quality=90,subsampling=0,optimize=True)

import subprocess,sys,os
J=[l.strip() for l in sys.argv[1:]]
for k,name in enumerate(J):
    src=P+'raw/'+name+'.png'; tex=P+'raw/'+name+'_tex.png'
    subprocess.check_call(['python3','/workspace/hf-test/zen/posting/camille_oct22/work/skin_local.py',src,tex])
    o=Image.open(src).convert('RGB'); W=1080; H=round(o.height*W/o.width)
    o=o.resize((W,H),Image.LANCZOS); t=Image.open(tex).convert('RGB').resize((W,H),Image.LANCZOS)
    a=f(o); Y=f(o.convert('L')); Yt=f(t.convert('L'))
    ycc=f(o.convert('YCbCr')); Cb,Cr=ycc[...,1],ycc[...,2]
    m=((Cr>135)&(Cr<180)&(Cb>80)&(Cb<130)&(Y>60)).astype(np.float32)
    m=blur(m*255,5)/255
    e=np.abs(Y-blur(Y,2.0)); e=blur(e,3)
    prot=np.clip(1-(e-4)/6,0,1)
    mask=m*prot
    hp=Yt-blur(Yt,1.6); hp=np.clip(hp,-6,6)
    lo=np.clip(blur(Yt,6)-blur(Y,6),-8,4)
    b=a+((hp+lo*0.5)*mask*0.5)[...,None]
    b=sharpen(b,0.3); b=grain(b,k)
    save(b,P+'fin/'+name+'_v4C.jpg'); print('finished',name)
