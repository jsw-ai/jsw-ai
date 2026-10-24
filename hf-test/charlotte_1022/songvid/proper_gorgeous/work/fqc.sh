#!/bin/bash
# usage: fgate.sh NAME  -> 1fps frames, identity gate, summary, side-by-side
n=$1; F=../qc/frames_$n; mkdir -p $F ../qc/final_$n
ffmpeg -v error -y -i ../final/$n.mp4 -vf fps=1 -q:v 2 $F/f%03d.jpg
./runq.sh ./pg_gate.py ../qc/final_$n 1 $F/*.jpg > ../qc/final_$n.log 2>&1
python3 - "$n" <<'P'
import json,glob,sys,os
from PIL import Image,ImageDraw
n=sys.argv[1]; R=[json.load(open(f)) for f in sorted(glob.glob(f'../qc/final_{n}/f*.json'))]
v=[r['still'] for r in R if r['still'] is not None]
import statistics as st
s=dict(file=os.path.abspath(f'../final/{n}.mp4'),frames=len(R),no_face=len(R)-len(v),median=round(st.median(v),4),min=min(v),below_078=sum(x<0.78 for x in v),per_frame=[(os.path.basename(r['file']),r['still']) for r in R])
s['pass']=s['median']>=0.78 and s['no_face']==0 and s['min']>=0.70
json.dump(s,open(f'../qc/{n}_gate.json','w'),indent=1); print({k:s[k] for k in ('median','min','below_078','no_face','pass')})
ref=Image.open('stills/r2_r8.jpg').resize((540,722)); fr=sorted(glob.glob(f'../qc/frames_{n}/f*.jpg'))[1::4][:6]
S=Image.new('RGB',(540+len(fr)*406,722),'white'); S.paste(ref,(0,0)); d=ImageDraw.Draw(S); d.text((8,8),'APPROVED REF r2_r8 (.856)',fill='yellow')
sc=dict(s['per_frame'])
for i,f in enumerate(fr):
    im=Image.open(f).resize((406,722)); S.paste(im,(540+i*406,0)); d.text((548+i*406,8),f'{os.path.basename(f)} {sc.get(os.path.basename(f))}',fill='yellow')
S.save(f'../qc/{n}_sidebyside.jpg',quality=90)
P
