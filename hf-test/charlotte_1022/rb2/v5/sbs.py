import sys
from PIL import Image,ImageDraw
out=sys.argv[1]; ims=[]
for p in sys.argv[2:]:
    i=Image.open(p).convert('RGB'); i=i.resize((int(i.width*800/i.height),800)); ImageDraw.Draw(i).text((10,10),('REF ' if '/up/' in p else '')+p.split('/')[-1],fill='yellow'); ims.append(i)
c=Image.new('RGB',(sum(i.width for i in ims),800)); x=0
for i in ims: c.paste(i,(x,0)); x+=i.width
c.save(out,quality=85)
