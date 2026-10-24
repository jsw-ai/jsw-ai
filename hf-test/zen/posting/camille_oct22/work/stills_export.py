from PIL import Image, ImageDraw, ImageFont
P='/workspace/hf-test/zen/posting/camille_oct22/'
FONT=[l for l in open('/tmp/fonts.txt').read().split('\n') if 'SemiBold' in l][0].split(':')[0]
def fit(src):
    im=Image.open(P+'fin/'+src+'_v4C.jpg').convert('RGB'); w,h=im.size; s=1920/h
    im=im.resize((round(w*s),1920),Image.LANCZOS); W=im.size[0]; x=(W-1080)//2
    return im.crop((x,0,x+1080,1920))
def text(im,t,y=1600,size=54):
    d=ImageDraw.Draw(im); f=ImageFont.truetype(FONT,size)
    bb=d.textbbox((0,0),t,font=f); tw=bb[2]-bb[0]; x=(1080-tw)//2
    d.text((x,y),t,font=f,fill='white',stroke_width=4,stroke_fill=(0,0,0))
    return im
jobs=[('S7','x_tease1_S7_XONLY',None),('S6a','x_tease2_S6a_XONLY',None),('S1b','x_tease3_S1b_XONLY',None),
('S1a','ig_story1_S1a','bonjour from the terrace'),('S5a','ig_story2_S5a','petit déjeuner, no rush'),('S6a','ig_story3_S6a','à demain, Monaco'),
('S6b','reddit_photo1_S6b',None),('S2a','reddit_photo2_S2a',None)]
for s,n,t in jobs:
    im=fit(s)
    if t: im=text(im,t)
    im.save(P+'platform/stills/'+n+'.jpg',quality=93,optimize=True)  # PIL writes no EXIF unless given
    print(n)
