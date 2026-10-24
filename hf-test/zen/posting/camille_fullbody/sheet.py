import cv2
from PIL import Image,ImageDraw,ImageFont
from insightface.app import FaceAnalysis
a=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);a.prepare(ctx_id=-1,det_size=(640,640))
def emb(p):
    f=a.get(cv2.imread(p));return max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])).normed_embedding if f else None
ref=emb('camille_v2/raw/r3_4.png')
items=[('1 laughing, looking away right (dress, street) [retry]','camille_fullbody/raw/fb1_retry.png'),('2 neutral, 3/4 looking off left (jeans, cafe wall)','camille_fullbody/raw/fb2.png'),('3 closed smile, glance over shoulder (skirt, boardwalk)','camille_fullbody/raw/fb3.png'),('4 squinting at sun, face up (athleisure, park)','camille_fullbody/raw/fb4.png')]
W,H=600,800;S=Image.new('RGB',(W*4,H+70),'white');d=ImageDraw.Draw(S)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
for i,(t,p) in enumerate(items):
    e=emb(p);c=float(e@ref) if e is not None else -1
    print(t,'cos %.2f'%c)
    im=Image.open(p).convert('RGB').resize((W,H));S.paste(im,(i*W,70))
    d.text((i*W+6,6),t[:46],fill='black',font=f);d.text((i*W+6,30),t[46:]+'  cos vs r3_4 %.2f'%c,fill='black',font=f)
S.save('camille_fullbody_sheet.jpg',quality=90)
