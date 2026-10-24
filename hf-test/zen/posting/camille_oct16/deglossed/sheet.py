import cv2,numpy as np,sys
sys.path.insert(0,'.')
from pp import facebox
from PIL import Image,ImageDraw,ImageFont
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
def lab(im,t):
    im=im.copy();d=ImageDraw.Draw(im);d.rectangle((0,0,im.width,30),fill=(0,0,0));d.text((6,3),t,font=F,fill=(255,255,255));return im
rows=[]
for n in (4,2,7,6):
    o=cv2.imread(f'../stills/camille_s{n}.jpg');b=facebox(o);x0,y0,x1,y1=[int(v) for v in b];w=x1-x0
    def crop(f):
        i=cv2.imread(f);return cv2.resize(i[max(0,y0-int(w*.3)):y1+int(w*.2),max(0,x0-int(w*.3)):x1+int(w*.3)],(380,430))
    def full(f):
        i=cv2.imread(f);return cv2.resize(i,(322,430))
    em=f'camille_s{n}_extra_matte.jpg' if n!=2 else f'camille_s{n}_deglossed.jpg'
    items=[(full(f'../stills/camille_s{n}.jpg'),f's{n} BEFORE'),(full(f'camille_s{n}_deglossed.jpg'),f's{n} AFTER'),
      (crop(f'../stills/camille_s{n}.jpg'),'BEFORE face'),(crop(f'camille_s{n}_deglossed.jpg'),'AFTER face (edit)'),(crop(em),'AFTER + extra matte' if n!=2 else 'same as AFTER (no pp)')]
    r=np.hstack([np.array(lab(Image.fromarray(cv2.cvtColor(a,cv2.COLOR_BGR2RGB)),t)) for a,t in items]);rows.append(r)
Image.fromarray(np.vstack(rows)).save('before_after_sheet.jpg',quality=90);print(np.vstack(rows).shape)
