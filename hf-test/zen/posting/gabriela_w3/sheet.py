import sys
from PIL import Image,ImageDraw
names=sys.argv[2:];out=sys.argv[1]
w,h=300,400;cols=6
ims=[Image.open(f).convert('RGB').resize((w,h)) for f in names]
rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(w*cols,h*rows));d=ImageDraw.Draw(S)
for k,i in enumerate(ims):
    S.paste(i,((k%cols)*w,(k//cols)*h));d.text(((k%cols)*w+6,(k//cols)*h+6),names[k].split('/')[-1],fill=(255,255,0))
S.save(out,quality=90)
