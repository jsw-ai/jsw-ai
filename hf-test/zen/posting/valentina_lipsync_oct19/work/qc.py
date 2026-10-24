import sys,cv2,numpy as np,subprocess,os
sys.path.insert(0,'/workspace/hf-test/zen/posting')
import identity_gate as g
from PIL import Image,ImageDraw
exec(open('cmp.py').read().split("for t in sys.argv")[0])
exec(open('vsheet.py').read().split('if __name__')[0])
P='/workspace/hf-test/zen/posting/'
k=sys.argv[1]; v='../final/%s.mp4'%k
# per-frame face top / head top check at 5 fps
cap=cv2.VideoCapture(v); fps=cap.get(5); n=int(cap.get(7)); res=[]
for i in range(0,n,max(1,int(fps/5))):
    cap.set(1,i); ok,im=cap.read()
    if not ok: break
    f,_=g.faces(im); sc=1280/1920
    if not f: res.append((i/fps,None,None)); continue
    x=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
    y0=x.bbox[1]/sc; h=(x.bbox[3]-x.bbox[1])/sc
    res.append((i/fps, y0, float(x.normed_embedding@c)))
tops=[r[1] for r in res if r[1] is not None]; sims=[r[2] for r in res if r[2] is not None]
# hair top estimate ~ face bbox top - 0.45*face height; report min bbox top
print(k,'frames',len(res),'noface',sum(r[1] is None for r in res),'min face-box top y(1920)=%.0f'%min(tops),'sim min %.2f med %.2f max %.2f'%(min(sims),np.median(sims),max(sims)))
open('qc_%s.txt'%k,'w').write('\n'.join('%.2f %s %s'%r for r in res))
ts=[0.1,1.5,3.0,4.5,6.0,7.8]; W=300;H=533;S=300
canvas=Image.new('RGB',(W*7,H+S+60),'white'); d=ImageDraw.Draw(canvas)
for j,t in enumerate(ts):
    p='/tmp/%s_q%.1f.png'%(k,t); subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',v,'-frames:v','1',p])
    im=Image.open(p).convert('RGB'); canvas.paste(im.resize((W,H)),(j*W,20)); d.text((j*W+4,4),'%s %.1fs'%(k,t),fill='black')
    try: canvas.paste(crop(p,S),(j*W,H+40))
    except Exception as e: pass
ref=P+'valentina_test2/fin/s2_b_v4C.jpg'; r=Image.open(ref).convert('RGB')
canvas.paste(r.resize((W,int(r.height*W/r.width))).crop((0,0,W,H)),(6*W,20)); d.text((6*W+4,4),'test2 balcony (ref)',fill='black')
canvas.paste(crop(P+'valentina_test2/fin/s1_a_v4C.jpg',S),(6*W,H+40)); d.text((6*W+4,H+24),'test2 cafe face (ref)',fill='black')
canvas.save('../qc/%s_qc.jpg'%k,quality=90)
