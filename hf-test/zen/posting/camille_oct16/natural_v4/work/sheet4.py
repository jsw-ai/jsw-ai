import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(640,640))
def tile34(im,cx=None,cy=None,h=None):
    W,H=im.size
    if h is None: h=min(H,W*4/3)
    w=h*3/4
    if cx is None: cx=W/2
    if cy is None: cy=H/2
    x0=min(max(cx-w/2,0),W-w);y0=min(max(cy-h/2,0),H-h)
    return im.crop((int(x0),int(y0),int(x0+w),int(y0+h)))
names=['face1','face2','face3','body1','body2','body3','body4','body5']
labels=['Face 1','Face 2','Face 3','Body 1','Body 2','Body 3','Body 4','Body 5']
V2=['v2work/m_face1.png','v2work/m_face2.png','v2work/face3_crop.jpg','v2work/m_body1.png','v2work/b2_new.png','v2work/f3_new.png','v2work/b4_new.png','v2work/b5_new.png']
V4=['natural_v4/fin/%s_v4C.jpg'%n for n in names]
def sheet(paths,out):
    W,H=480,640;fnt=ImageFont.load_default(size=22)
    s=Image.new('RGB',(W*4+50,(H+44)*2+10),'white');d=ImageDraw.Draw(s)
    for i,p in enumerate(paths):
        im=Image.open(p).convert('RGB');im=tile34(im).resize((W,H),Image.LANCZOS)
        x=10+(i%4)*(W+10);y=10+(i//4)*(H+44);s.paste(im,(x,y));d.text((x+2,y+H+8),labels[i],fill='black',font=fnt)
    s.save(out,quality=92)
sheet(V4,'REFERENCE_CONTACT_SHEET_v4.jpg')
def face(p):
    im=Image.open(p).convert('RGB');a=cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
    fs=app.get(a)
    if not fs:
        r=640/max(im.size);fs=[type('F',(),{'bbox':g.bbox/r,'normed_embedding':g.normed_embedding}) for g in app.get(cv2.resize(a,None,fx=r,fy=r))]
    f=max(fs,key=lambda f:(f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]));b=f.bbox;s=max(b[2]-b[0],b[3]-b[1])*1.5
    cx,cy=(b[0]+b[2])/2,(b[1]+b[3])/2
    return im.crop((int(cx-s/2),int(cy-s/2),int(cx+s/2),int(cy+s/2))).resize((400,400),Image.LANCZOS),f.normed_embedding
fnt=ImageFont.load_default(size=20)
c=Image.new('RGB',(8*410+10,2*400+90),'white');d=ImageDraw.Draw(c);cos={}
for i,(a,b) in enumerate(zip(V2,V4)):
    fa,ea=face(a);fb,eb=face(b);cos[names[i]]=float(ea@eb)
    c.paste(fa,(10+i*410,30));c.paste(fb,(10+i*410,440));d.text((10+i*410,5),'%s v2'%labels[i],fill='black',font=fnt);d.text((10+i*410,845),'v4 (cos %.2f)'%cos[names[i]],fill='black',font=fnt)
c.save('natural_v4/before_after_faces_v2_v4.jpg',quality=92)
# body side by side
b=Image.new('RGB',(5*(360*2+30),480+40),'white');d=ImageDraw.Draw(b)
for j,i in enumerate(range(3,8)):
    for k,p in enumerate((V2[i],V4[i])):
        im=tile34(Image.open(p).convert('RGB')).resize((360,480));b.paste(im,(j*750+k*365,30))
    d.text((j*750,5),labels[i]+' v2 | v4',fill='black',font=fnt)
b.save('natural_v4/before_after_bodies_v2_v4.jpg',quality=90)
print(cos)
