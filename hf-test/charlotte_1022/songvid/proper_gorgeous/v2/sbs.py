# sbs.py name -> qc/<name>_sidebyside.jpg : per shot [source still | mid frame + score | face ref | body ref]
import json,sys,subprocess,os
from PIL import Image,ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
K='/workspace/hf-test/keepers/'
n=sys.argv[1]; man=json.load(open(f'final/{n}_manifest.json')); g=json.load(open(f'qc/{n}_gate.json'))
H=480; fr_=Image.open(K+'charlotte_face_keeper.png').convert('RGB'); bo=Image.open(K+'charlotte_body_keeper.png').convert('RGB')
rs=lambda im:im.resize((int(im.width*H/im.height),H))
rows=[]
for i,s in enumerate(man['shots']):
    t=(s['t0']+s['t1'])/2; p=f'/tmp/cpg_sbs_{i}.jpg'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',man['file'],'-frames:v','1',p],check=True)
    ims=[rs(Image.open(s['source_still']).convert('RGB')),rs(Image.open(p).convert('RGB')),rs(fr_),rs(bo)]
    R=Image.new('RGB',(sum(x.width for x in ims)+30,H),'white'); x=0
    for im in ims: R.paste(im,(x,0)); x+=im.width+10
    d=ImageDraw.Draw(R); sh=g['shots'][i]
    d.text((6,6),f"shot {i} still {os.path.basename(s['source_still'])}",fill='yellow')
    d.text((ims[0].width+16,6),f"video t={t:.1f}s med {sh['median']} min {sh['min']} {'PASS' if sh['pass'] else 'FAIL'}",fill='yellow')
    d.text((ims[0].width+ims[1].width+26,6),'REF face_keeper',fill='yellow'); d.text((x-ims[3].width,6),'REF body_keeper',fill='yellow')
    rows.append(R)
W=max(r.width for r in rows); S=Image.new('RGB',(W,H*len(rows)),'white')
for i,r in enumerate(rows): S.paste(r,(0,i*H))
S.save(f'qc/{n}_sidebyside.jpg',quality=85); print('ok',f'qc/{n}_sidebyside.jpg')
