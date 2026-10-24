import sys,json
from PIL import Image,ImageDraw
d=sys.argv[1]; names=sys.argv[3:]; out=sys.argv[2]
w,h=300,400; cols=4; rows=(len(names)+cols-1)//cols
S=Image.new('RGB',(w*cols,(h+16)*rows),'white');dr=ImageDraw.Draw(S)
for i,n in enumerate(names):
    im=Image.open(f'{d}/{n}').convert('RGB').resize((w,h)); x=(i%cols)*w;y=(i//cols)*(h+16)
    S.paste(im,(x,y+16));dr.text((x+4,y+2),n,fill='black')
S.save(out,quality=85)
