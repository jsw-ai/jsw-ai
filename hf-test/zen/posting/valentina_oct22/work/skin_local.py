# Rebuilt 2026-10-22 from the spec in VALENTINA_PIPELINE.md §4.1 because
# /workspace/hf-test/posting_oct14/v3/raw/skin_local.py is missing (dir recreated empty 03:28 ET).
import sys, numpy as np
from PIL import Image, ImageFilter
def f(a): return np.asarray(a).astype(np.float32)
def blur(x,r): return f(Image.fromarray(np.clip(x,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)))
def blurf(x,r): return blur(x+128,r)-128
src,dst=sys.argv[1],sys.argv[2]
o=Image.open(src).convert('RGB'); a=f(o); Y=f(o.convert('L'))
ycc=f(o.convert('YCbCr')); Cb,Cr=ycc[...,1],ycc[...,2]
m=((Cr>135)&(Cr<180)&(Cb>80)&(Cb<130)&(Y>60)).astype(np.float32)
m=blur(m*255,6)/255
a=a-(np.clip((Y-200)/55,0,1)*m*14)[...,None]
rng=np.random.default_rng(7)
n1=blurf(np.clip(rng.normal(0,1,Y.shape)*40,-127,127),0.9)
n2=blurf(np.clip(rng.normal(0,1,Y.shape)*40,-127,127),4)
tex=(n1*0.18+n2*0.10)*(0.6+0.4*Y/255)
b=a+(tex*m)[...,None]
Image.fromarray(np.clip(b,0,255).astype(np.uint8)).save(dst)
