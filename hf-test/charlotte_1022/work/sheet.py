import sys,json
from PIL import Image, ImageDraw
# usage: sheet.py out.jpg gate.json img1 img2 ...
out,gj=sys.argv[1],sys.argv[2]; fs=sys.argv[3:]
g=json.load(open(gj)) if gj!='-' else {}
refs=['/workspace/hf-test/keepers/charlotte_face_keeper.png','/workspace/hf-test/keepers/charlotte_cover.png','/workspace/hf-test/charlotte_ref/f.png']
H=520
def tile(p,lab):
    im=Image.open(p).convert('RGB'); w=int(im.width*H/im.height); im=im.resize((w,H)); d=ImageDraw.Draw(im); d.rectangle((0,0,w,22),fill='black'); d.text((4,4),lab,fill='yellow'); return im
row1=[tile(r,r.split('/')[-1]) for r in refs]
rs=Image.open('/workspace/hf-test/charlotte_ref/ref_sheet.jpg').convert('RGB')
row2=[]
for f in fs:
    s=[v.get('score_centroid') for k,v in g.items() if k.endswith(f.split('/')[-1])]
    row2.append(tile(f,f.split('/')[-1]+(' %.3f'%s[0] if s and s[0] else '')))
W=max(sum(t.width for t in row1), sum(t.width for t in row2), 1600)
rsh=int(rs.height*W/rs.width); rs=rs.resize((W,rsh))
S=Image.new('RGB',(W,H*2+rsh),'white'); x=0
for t in row1: S.paste(t,(x,0)); x+=t.width
S.paste(rs,(0,H)); x=0
for t in row2: S.paste(t,(x,H+rsh)); x+=t.width
S.save(out,quality=85)
