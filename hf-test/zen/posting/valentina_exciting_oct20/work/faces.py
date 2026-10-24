import sys,cv2
sys.path.insert(0,'/workspace/hf-test/zen/posting')
import identity_gate as g
from PIL import Image,ImageDraw
out=sys.argv[1]; ims=sys.argv[2:]
S=260;c=Image.new('RGB',(S*len(ims),S+16),'white');d=ImageDraw.Draw(c)
for k,p in enumerate(ims):
  im=cv2.imread(p); f,_=g.faces(im)
  if not f: d.text((k*S+4,S),'noface '+p[-12:],fill='red'); continue
  x=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])); s=max(im.shape[:2])/1280
  x0,y0,x1,y1=[v*s for v in x.bbox]; cx=(x0+x1)/2; cy=(y0+y1)/2; h=(y1-y0)*0.8
  pi=Image.open(p).convert('RGB').crop((int(cx-h),int(cy-h),int(cx+h),int(cy+h))).resize((S,S))
  c.paste(pi,(k*S,0)); d.text((k*S+4,S+2),p.split('/')[-1][:20],fill='black')
c.save(out,quality=90)
