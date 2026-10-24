import json
from PIL import Image, ImageDraw, ImageFont
R='/workspace/hf-test/zen/posting/'; L=R+'lock_test/'
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',13); f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
S=json.load(open(L+'v2/gate_soul_newchecks.json')); O=json.load(open(L+'v2/gate_oldsd_newchecks.json'))
N={}
for k in ('gate_fin_b1.json',): N=json.load(open(L+'v2/'+k))
def key(d,n): return [v for k,v in d.items() if n in k][0]
def info(r,src):
    b=r['body']; face_ok=not any(x.startswith('identity') for x in r['reasons'])
    body_ok=not any(x.startswith('body_') for x in r['reasons'])
    bt='n/a(unmeasurable)' if not b['measurable'] else ('PASS' if body_ok else 'FAIL')
    meas='bust %.2f'%b['bust_w']+(' thigh %.2f'%b['thigh_w'] if b.get('thigh_w') else '')+' sh %.2f'%b['sh_w']
    return face_ok,body_ok,['FACE %s c%.2f b%.2f%s'%('PASS' if face_ok else 'FAIL',r['score_centroid'],r['score_best'],' (sd>=.78)' if src=='sd' else ''),'BODY %s %s'%(bt,meas),'VISUAL: Sam to confirm']
items=[('1 kitchen',L+'fin/soul_1_v4C.jpg',key(S,'soul_1'),'Soul'),('2 balcony',L+'fin/soul_2_v4C.jpg',key(S,'soul_2'),'Soul'),('3 beach path',L+'fin/soul_4_v4C.jpg',key(S,'soul_4'),'Soul'),('4 park',L+'fin/soul_7_v4C.jpg',key(S,'soul_7'),'Soul'),
 ('5 sofa',L+'fin/soul_8_v4C.jpg',key(S,'soul_8'),'Soul'),('6 cafe NEW v2',L+'v2/fin/sd_3_b1_v4C.jpg',key(N,'sd_3_b1'),'sd'),('7 one-piece NEW v2',L+'v2/fin/sd_5_b1_v4C.jpg',key(N,'sd_5_b1'),'sd'),('8 beach NEW v2',L+'v2/fin/sd_6_b1_v4C.jpg',key(N,'sd_6_b1'),'sd')]
old=[('OLD 6 cafe (v1)',L+'fin/sd_3_a1_v4C.jpg',key(O,'sd_3_a1'),'sd'),('OLD 7 one-piece (v1)',L+'fin/sd_5_a1_v4C.jpg',key(O,'sd_5_a1'),'sd'),('OLD 8 beach (v1)',L+'fin/sd_6_a1_v4C.jpg',key(O,'sd_6_a1'),'sd')]
W,H,HD=300,400,62
def cell(S_,x,y,name,p,r,src):
    fo,bo,lines=info(r,src); ok=fo and bo
    d.rectangle([x,y,x+W,y+HD],fill=(20,120,40) if ok else (170,25,25)); d.text((x+4,y+3),('PASS ' if ok else 'FAIL ')+name,font=F,fill='white')
    for i,l in enumerate(lines): d.text((x+4,y+19+i*14),l,font=f,fill='white')
    im=Image.open(p).convert('RGB'); im.thumbnail((W,H)); S_.paste(im,(x,y+HD))
rows=[items[:4],items[4:],old]
Hs=HD+H+4
S_=Image.new('RGB',(4*W+0,3*Hs+48),'white'); d=ImageDraw.Draw(S_)
for ri,row in enumerate(rows):
    for ci,(n,p,r,src) in enumerate(row): cell(S_,ci*W,ri*Hs,n,p,r,src)
d.text((4,3*Hs+6),'FACE = identity_gate centroid(c)/best-ref(b); Seedream also needs c>=0.78.  BODY = body_check.py proxy: bust width, thigh width, shoulder width (face-heights).',font=f,fill='black'); d.text((4,3*Hs+24),'VISUAL = mandatory human check, NOT automated. Bottom row = rejected v1 photos 6-8 re-scored with the new checks (all three now FAIL).',font=f,fill='black')
S_.save(R+'higgsfield_lock_test_v2.jpg',quality=90)
