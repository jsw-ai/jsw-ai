import cv2,numpy as np,sys
from PIL import Image,ImageDraw,ImageFont
from insightface.app import FaceAnalysis
a=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);a.prepare(ctx_id=-1,det_size=(640,640))
def crop(p):
    im=cv2.imread(p);f=a.get(im);x=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
    x0,y0,x1,y1=x.bbox;cx,cy=(x0+x1)/2,(y0+y1)/2;s=max(x1-x0,y1-y0)*0.85
    H,W=im.shape[:2];box=[int(max(0,cx-s)),int(max(0,cy-s)),int(min(W,cx+s)),int(min(H,cy+s))]
    return Image.fromarray(cv2.cvtColor(im[box[1]:box[3],box[0]:box[2]],cv2.COLOR_BGR2RGB)).resize((600,600),Image.LANCZOS)
items=[('ORIGINAL r3_4 face (approved look)','camille_v2/raw/r3_4.png'),
('NEW 3/4 (tq_B) - picked','camille_v3/raw_b/'+sys.argv[1]+'.png'),
('NEW neutral off-cam (neu_A) - picked','camille_v3/raw_b/'+sys.argv[2]+'.png'),
('OLD shiny 3/4 (v3)','camille_v3/raw/three_quarter.png'),
('OLD shiny neutral (v3)','camille_v3/raw/neutral_off.png'),
('(rejected) '+'tq_A','camille_v3/raw_b/tq_A.png'),('(rejected) neu_B','camille_v3/raw_b/neu_B.png')]
items[1]=('NEW 3/4 (%s) - picked'%sys.argv[1],items[1][1]);items[2]=('NEW neutral (%s) - picked'%sys.argv[2],items[2][1])
rej=[n for n in ['tq_A','tq_B'] if n!=sys.argv[1]]+[n for n in ['neu_A','neu_B'] if n!=sys.argv[2]]
items[5]=('rejected %s'%rej[0],'camille_v3/raw_b/%s.png'%rej[0]);items[6]=('rejected %s'%rej[1],'camille_v3/raw_b/%s.png'%rej[1])
order=[0,1,2,3,4,5,6]
S=Image.new('RGB',(2400,1300),'white');d=ImageDraw.Draw(S)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26)
for i,(l,p) in enumerate(items):
    x=(i%4)*600;y=(i//4)*650;S.paste(crop(p),(x,y+50));d.text((x+10,y+10),l,fill='black',font=f)
S.save('posting_sheet.jpg',quality=92)
