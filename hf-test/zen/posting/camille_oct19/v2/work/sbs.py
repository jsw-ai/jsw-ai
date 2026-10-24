import sys,subprocess,os,json
from PIL import Image,ImageDraw,ImageFont
P='/workspace/hf-test/zen/posting/camille_oct19/v2/'
R='/workspace/hf-test/zen/posting/camille_oct16/natural_v4/fin/'
name,mp4,start=sys.argv[1],sys.argv[2],sys.argv[3]
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',mp4]).decode())
ts=[0.1]+[dur*k/5 for k in range(1,5)]+[dur-0.1]
os.makedirs(P+'frames/'+name,exist_ok=True); fr=[]
for i,t in enumerate(ts):
    o=P+'frames/%s/f%d_%.1fs.png'%(name,i,t); subprocess.run(['ffmpeg','-v','error','-y','-ss','%.2f'%t,'-i',mp4,'-frames:v','1',o],check=True); fr.append((o,'%.1fs'%t))
refs=[(R+'face1_v4C.jpg','v4 Face 1'),(R+'face2_v4C.jpg','v4 Face 2'),(R+'face3_v4C.jpg','v4 Face 3'),(R+'body1_v4C.jpg','v4 Body 1 (bust std)'),(start,'start still')]
H=560;fnt=ImageFont.load_default(size=22)
def row(items):
    ims=[]
    for p,l in items:
        im=Image.open(p).convert('RGB'); im=im.resize((int(im.width*H/im.height),H),Image.LANCZOS); ims.append((im,l))
    return ims
r1=row(refs); r2=row(fr)
W=max(sum(i.width+8 for i,_ in r) for r in (r1,r2))+8
s=Image.new('RGB',(W,2*(H+36)+50),'white');d=ImageDraw.Draw(s)
d.text((8,8),'%s: top = approved v4 refs + start, bottom = 6 frames across clip (%.2fs)'%(name,dur),fill='black',font=fnt)
for k,r in enumerate((r1,r2)):
    x=8;y=44+k*(H+36)
    for im,l in r: s.paste(im,(x,y)); d.text((x+2,y+H+4),l,fill='black',font=fnt); x+=im.width+8
s.save(P+'%s_sidebyside.jpg'%name,quality=90)
json.dump([f for f,_ in fr],open(P+'frames/%s/list.json'%name,'w'))
print('ok',dur)
