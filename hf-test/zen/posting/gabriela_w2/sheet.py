import sys
from PIL import Image,ImageDraw
D=sys.argv[1]; names=sys.argv[2:]; out=sys.argv[1].rstrip('/')+'_sheet.jpg'
ims=[Image.open(f).convert('RGB') for f in names]
w=360;h=480
ims=[i.resize((w,h)) for i in ims]
cols=5;rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(w*cols,h*rows))
d=ImageDraw.Draw(S)
for k,i in enumerate(ims):
    S.paste(i,((k%cols)*w,(k//cols)*h)); d.text(((k%cols)*w+6,(k//cols)*h+6),names[k].split('/')[-1],fill=(255,255,0))
S.save(out,quality=90);print(out)
