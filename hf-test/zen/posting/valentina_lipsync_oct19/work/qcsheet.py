import sys,cv2,numpy as np,subprocess,os
sys.path.insert(0,'/workspace/hf-test/zen/posting')
import identity_gate as g
from PIL import Image,ImageDraw
exec(open('cmp.py').read().split("for t in sys.argv")[0])
exec(open('vsheet.py').read().split('if __name__')[0])
P='/workspace/hf-test/zen/posting/'


k=sys.argv[1]; v='../final/%s.mp4'%k
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
