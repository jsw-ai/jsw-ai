import sys,json
from PIL import Image,ImageDraw,ImageFont
# usage: sheet.py out.jpg tileH cols file[:label] ...
out=sys.argv[1]; H=int(sys.argv[2]); C=int(sys.argv[3]); items=sys.argv[4:]
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
tiles=[]
for it in items:
    p,_,lab=it.partition('::'); im=Image.open(p).convert('RGB'); W=int(im.width*H/im.height)
    im=im.resize((W,H),Image.LANCZOS); d=ImageDraw.Draw(im); d.rectangle([0,0,W,30],fill=(0,0,0)); d.text((5,3),lab or p.split('/')[-1],fill=(255,255,0),font=F); tiles.append(im)
rows=[tiles[i:i+C] for i in range(0,len(tiles),C)]
Wt=max(sum(t.width for t in r) for r in rows)
s=Image.new('RGB',(Wt,H*len(rows)),(30,30,30))
for j,r in enumerate(rows):
    x=0
    for t in r: s.paste(t,(x,j*H)); x+=t.width
s.save(out,quality=88)
