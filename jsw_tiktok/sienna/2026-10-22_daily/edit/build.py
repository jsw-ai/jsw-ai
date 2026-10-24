# Clip1 builder: A = k2 [a0,a1], synthetic whip pan, B = k3 [b0,b1]; 1080x1920 cover crop
import subprocess,sys,os,numpy as np
from PIL import Image
a0,a1,b0,b1=map(float,sys.argv[1:5]); out=sys.argv[5]
D='/workspace/jsw_tiktok/sienna/2026-10-22_daily'
def frames(src,t0,t1,tag):
    d=f'fr_{tag}'; os.makedirs(d,exist_ok=True); [os.remove(os.path.join(d,f)) for f in os.listdir(d)]
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t0),'-to',str(t1),'-i',src,'-vf','fps=24,scale=-2:1920:flags=lanczos,crop=1080:1920',f'{d}/%04d.png'],check=True)
    return [os.path.join(d,f) for f in sorted(os.listdir(d))]
A=frames(f'{D}/kl/k2.mp4',a0,a1,'A'); B=frames(f'{D}/kl/k3.mp4',b0,b1,'B')
def hblur(arr,w):
    w=int(w)|1; p=w//2
    a=np.pad(arr.astype(np.float32),((0,0),(p+1,p),(0,0)),mode='edge'); c=np.cumsum(a,axis=1)
    return ((c[:,w:,:]-c[:,:-w,:])/w)[:, :arr.shape[1]]
la=np.array(Image.open(A[-1]).convert('RGB')); fb=np.array(Image.open(B[0]).convert('RGB'))
W=[]
for sh,bl in [(-160,180),(-420,320),(-760,480)]:
    W.append(np.roll(hblur(la,bl),sh,axis=1))
for sh,bl in [(760,480),(420,320),(160,180)]:
    W.append(np.roll(hblur(fb,bl),sh,axis=1))
os.makedirs('fr_all',exist_ok=True); [os.remove('fr_all/'+f) for f in os.listdir('fr_all')]
seq=[np.array(Image.open(f).convert('RGB')) for f in A]+W+[np.array(Image.open(f).convert('RGB')) for f in B]
for i,fr in enumerate(seq): Image.fromarray(np.clip(fr,0,255).astype(np.uint8)).save(f'fr_all/{i:04d}.png')
n=len(seq); print('frames',n,'dur',n/24,'A',len(A),'whip',len(W),'B',len(B))
open('cuts.txt','w').write(f'{len(A)} {len(W)} {len(B)}\n')
