import cv2
from PIL import Image,ImageDraw,ImageFont
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(1024,1024))
def tile34(im,cx=None,cy=None,h=None):
    W,H=im.size
    if h is None: h=min(H,W*4/3)
    w=h*3/4
    if cx is None: cx=W/2
    if cy is None: cy=H/2
    x0=min(max(cx-w/2,0),W-w);y0=min(max(cy-h/2,0),H-h)
    return im.crop((int(x0),int(y0),int(x0+w),int(y0+h)))
# face3 crop from s4 deglossed
p='deglossed/camille_s4_deglossed.jpg';im=Image.open(p).convert('RGB')
f=max(app.get(cv2.imread(p)),key=lambda f:(f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]));b=f.bbox
fh=b[3]-b[1];c=tile34(im,(b[0]+b[2])/2,(b[1]+b[3])/2+fh*0.1,fh*2.6);c.save('v2work/face3_crop.jpg',quality=94)
def face_crop(path):
    cvp=cv2.imread(path);im=Image.open(path).convert('RGB')
    fs=app.get(cvp)
    if not fs:
        return tile34(im)
    f=max(fs,key=lambda f:(f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]));b=f.bbox;fh=b[3]-b[1]
    return tile34(im,(b[0]+b[2])/2,(b[1]+b[3])/2+fh*0.1,fh*2.6)
f1=Image.open('v2work/m_face1.png').convert('RGB')
f1=tile34(f1,f1.size[0]/2,f1.size[1]/2,f1.size[1])
f2=Image.open('v2work/m_face2.png').convert('RGB');f2=tile34(f2)
items=[('Face 1',f1),('Face 2',f2),('Face 3',c),('Body 1',Image.open('v2work/m_body1.png').convert('RGB')),
('Body 2',Image.open('v2work/b2_new.png').convert('RGB')),('Body 3',Image.open('v2work/f3_new.png').convert('RGB')),
('Body 4',Image.open('v2work/b4_new.png').convert('RGB')),('Body 5',Image.open('v2work/b5_new.png').convert('RGB'))]
W,H=480,640;L=44
fnt=ImageFont.load_default(size=22)
s=Image.new('RGB',(W*4+10*5,(H+L)*2+10),'white');d=ImageDraw.Draw(s)
for i,(n,im) in enumerate(items):
    im=tile34(im).resize((W,H),Image.LANCZOS)
    x=10+(i%4)*(W+10);y=10+(i//4)*(H+L)
    s.paste(im,(x,y));d.text((x+2,y+H+8),n,fill='black',font=fnt)
s.save('REFERENCE_CONTACT_SHEET_v2.jpg',quality=92)
