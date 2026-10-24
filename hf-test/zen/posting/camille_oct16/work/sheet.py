import sys
from PIL import Image,ImageDraw,ImageFont
out=sys.argv[1];items=sys.argv[2:]
W,H=420,560;n=len(items);cols=min(n,5);rows=(n+cols-1)//cols
S=Image.new('RGB',(W*cols,(H+24)*rows),'white');d=ImageDraw.Draw(S);f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
for i,p in enumerate(items):
    im=Image.open(p).convert('RGB');im.thumbnail((W,H));x=(i%cols)*W;y=(i//cols)*(H+24)
    S.paste(im,(x,y+24));d.text((x+4,y+3),p.split('/')[-1],fill='black',font=f)
S.save(out,quality=88)
