import json
from PIL import Image,ImageDraw,ImageFont
P='/workspace/hf-test/zen/posting/camille_oct19/';R='/workspace/hf-test/zen/posting/camille_oct16/natural_v4/fin/'
H=520;g=8;fb=ImageFont.load_default(size=30);f=ImageFont.load_default(size=20)
def fit(p):
    im=Image.open(p).convert('RGB');return im.resize((int(im.width*H/im.height),H),Image.LANCZOS)
c1=json.load(open(P+'frames/clip1_seaside/list.json'));c2=json.load(open(P+'frames/clip2_cafe/list.json'));t1=json.load(open(P+'frames/clip2_cafe_try1/list.json'))
lab=lambda L:[x.split('_')[-1][:-4] for x in L]
rows=[
 ('APPROVED v4 REFERENCES (Samuel, Oct 19)',[(R+'face1_v4C.jpg','Face 1'),(R+'face2_v4C.jpg','Face 2'),(R+'face3_v4C.jpg','Face 3'),(R+'body1_v4C.jpg','Body 1 = bust standard')]),
 ('POST 3 - STILL  camille_oct19_still_autumn_park.jpg  | gate 0.866 PASS | by eye face+body PASS',[(P+'camille_oct19_still_autumn_park.jpg','autumn park still (v4C)'),(P+'fin/cafe_start_v4C.jpg','(clip 2 start still, not a post)')]),
 ('POST 1 - CLIP  camille_oct19_clip1_seaside.mp4 (5.04s, silent) | frames 6/6, video 8/8 min 0.836 | PASS',list(zip(c1,lab(c1)))),
 ('POST 2 - CLIP  camille_oct19_clip2_cafe.mp4 (5.04s, silent, retry) | frames 6/6, video 8/8 min 0.799 | PASS',list(zip(c2,lab(c2)))),
 ('REJECTED - clip2 try 1 (eyes closed/looking down ~0.6s at 2.9-3.4s) - not for posting',list(zip(t1,lab(t1)))),
]
built=[(t,[(fit(p),l) for p,l in it]) for t,it in rows]
W=max(sum(i.width+g for i,_ in r) for _,r in built)+g
Ht=sum(H+90 for _ in built)+60
s=Image.new('RGB',(W,Ht),'white');d=ImageDraw.Draw(s)
d.text((g,10),'Camille - Mon Oct 19, 2026 - review sheet (NOTHING POSTED)',fill='black',font=fb);y=60
for t,r in built:
    d.text((g,y),t,fill=(160,0,0) if t.startswith('REJ') else 'black',font=f);x=g;y+=28
    for im,l in r: s.paste(im,(x,y));d.text((x+2,y+H+4),l,fill='black',font=f);x+=im.width+g
    y+=H+62
s.save(P+'review_sheet.jpg',quality=88);print(s.size)
