from PIL import Image,ImageDraw,ImageFont
def tile34(im,cx=None,cy=None,h=None):
    W,H=im.size
    if h is None: h=min(H,W*4/3)
    w=h*3/4
    if cx is None: cx=W/2
    if cy is None: cy=H/2
    x0=min(max(cx-w/2,0),W-w);y0=min(max(cy-h/2,0),H-h)
    return im.crop((int(x0),int(y0),int(x0+w),int(y0+h)))
D='/workspace/hf-test/zen/posting/camille_oct16/matte_v3/'
f1=Image.open(D+'face1_matte_v3.png').convert('RGB');f1=tile34(f1,f1.size[0]/2,f1.size[1]/2,f1.size[1])
items=[('Face 1',f1),('Face 2',tile34(Image.open(D+'face2_matte_v3.png').convert('RGB'))),('Face 3',Image.open(D+'face3_matte_v3.png').convert('RGB'))]+[(f'Body {i}',Image.open(D+f'body{i}_matte_v3.png').convert('RGB')) for i in range(1,6)]
W,H=480,640;L=44;fnt=ImageFont.load_default(size=22)
s=Image.new('RGB',(W*4+10*5,(H+L)*2+10),'white');d=ImageDraw.Draw(s)
for i,(n,im) in enumerate(items):
    im=tile34(im).resize((W,H),Image.LANCZOS);x=10+(i%4)*(W+10);y=10+(i//4)*(H+L)
    s.paste(im,(x,y));d.text((x+2,y+H+8),n,fill='black',font=fnt)
s.save('/workspace/hf-test/zen/posting/camille_oct16/REFERENCE_CONTACT_SHEET_v3.jpg',quality=92)
