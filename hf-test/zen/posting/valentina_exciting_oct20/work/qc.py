import sys,subprocess,cv2
sys.path.insert(0,'/workspace/hf-test/zen/posting')
import identity_gate as g
from PIL import Image,ImageDraw
k,start=sys.argv[1],sys.argv[2]; ts=[float(x) for x in sys.argv[3].split(',')]
v='../final/%s.mp4'%k; T2='/workspace/hf-test/zen/posting/valentina_test2/fin/'
refs=[T2+'s1_a_v4C.jpg',T2+'s2_b_v4C.jpg',T2+'s4_a_v4C.jpg',T2+'s5_a_v4C.jpg','e_cover.jpg',start]
W,H,S=300,533,300
c=Image.new('RGB',(W*6,(H+S+40)*2),'white');d=ImageDraw.Draw(c)
def fc(p):
    im=cv2.imread(p); f,_=g.faces(im)
    if not f: return None
    x=max(f,key=lambda x:x.bbox[2]-x.bbox[0]); s=max(im.shape[:2])/1280
    x0,y0,x1,y1=[q*s for q in x.bbox]; cx=(x0+x1)/2; cy=(y0+y1)/2; h=(y1-y0)*0.8
    return Image.open(p).convert('RGB').crop((int(cx-h),int(cy-h),int(cx+h),int(cy+h))).resize((S,S))
def put(p,i,row,lab):
    y=row*(H+S+40); im=Image.open(p).convert('RGB'); s=min(W/im.width,H/im.height); im=im.resize((int(im.width*s),int(im.height*s)))
    c.paste(im,(i*W,y+16)); d.text((i*W+3,y+2),lab,fill='black'); f=fc(p)
    if f: c.paste(f,(i*W,y+H+24))
for i,p in enumerate(refs): put(p,i,0,'REF '+p.split('/')[-1][:22])
for i,t in enumerate(ts):
    p='qc_tmp_%s_%d.png'%(k,i); subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',v,'-frames:v','1',p]); put(p,i,1,'%s %.1fs'%(k,t))
c.save('../qc/%s_qc.jpg'%k,quality=88)
