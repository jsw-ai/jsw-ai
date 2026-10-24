import sys,json,cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(640,640))
P='/workspace/hf-test/zen/posting/camille_oct19/';R='/workspace/hf-test/zen/posting/camille_oct16/natural_v4/fin/'
name=sys.argv[1];items=[(R+'face1_v4C.jpg','v4 Face 1'),(R+'body1_v4C.jpg','v4 Body 1')]+[(p,p.split('_')[-1][:-4]) for p in json.load(open(P+'frames/%s/list.json'%name))] if name!='still' else [(R+'face1_v4C.jpg','v4 Face 1'),(R+'body1_v4C.jpg','v4 Body 1'),(P+'fin/park_still_v4C.jpg','park still')]
fnt=ImageFont.load_default(size=20);S=300
s=Image.new('RGB',(len(items)*(S+8)+8,S+40),'white');d=ImageDraw.Draw(s)
for i,(p,l) in enumerate(items):
    im=Image.open(p).convert('RGB');a=cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR);f=max(app.get(a),key=lambda f:(f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]));b=f.bbox
    z=max(b[2]-b[0],b[3]-b[1])*1.4;cx,cy=(b[0]+b[2])/2,(b[1]+b[3])/2
    s.paste(im.crop((int(cx-z/2),int(cy-z/2),int(cx+z/2),int(cy+z/2))).resize((S,S),Image.LANCZOS),(8+i*(S+8),8));d.text((8+i*(S+8),S+12),l,fill='black',font=fnt)
s.save(P+'work/%s_faces.jpg'%name,quality=90);print('ok')
