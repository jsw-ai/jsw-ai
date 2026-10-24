import sys,subprocess,glob,os,json
from PIL import Image,ImageDraw
name=sys.argv[1]; src=f'../{name}.mp4'
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]))
d=os.path.abspath(f'qc/{name}'); os.makedirs(d,exist_ok=True)
for f in glob.glob(d+'/*.jpg'): os.remove(f)
ts=[round(dur*(i+0.5)/6,2) for i in range(6)]
fs=[]
for i,t in enumerate(ts):
    p=f'{d}/f{i}_{t}s.jpg'; subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(t),'-i',src,'-frames:v','1','-q:v','2',p]); fs.append(p)
subprocess.run(['/workspace/.face-venv/bin/python','/workspace/hf-test/zen/posting/identity_gate.py','img','--model','charlotte','--source','seedream','--no-ocr','--json',d+'/gate.json']+fs,capture_output=True,cwd='/workspace/hf-test')
g=json.load(open(d+'/gate.json')); sc=[]
for f in fs:
    k=[v for kk,v in g.items() if kk.endswith(os.path.basename(f))]
    sc.append((k[0].get('score_centroid') or 0) if k else 0)
H=480
ref=Image.open('/workspace/hf-test/charlotte_ref/ref_sheet.jpg').convert('RGB')
rw=ref.width*H//ref.height; ref=ref.resize((rw,H))
tiles=[]
for i,f in enumerate(fs):
    im=Image.open(f).convert('RGB'); im=im.resize((im.width*H//im.height,H)); D=ImageDraw.Draw(im)
    D.rectangle((0,H-24,im.width,H),fill='black'); D.text((4,H-20),f"{ts[i]}s id {sc[i]:.2f}",fill='yellow'); tiles.append(im)
W=max(rw,sum(t.width for t in tiles))
S=Image.new('RGB',(W,2*H+30),'black'); D=ImageDraw.Draw(S)
D.text((4,4),'TOP: ref_sheet.jpg  |  BOTTOM: 6 clip frames, same tile height ('+name+')',fill='white')
S.paste(ref,(0,30)); x=0
for t in tiles: S.paste(t,(x,30+H)); x+=t.width
S.save(f'../{name}_montage.jpg',quality=88)
print(name,'dur %.2f'%dur,' '.join(f'{t}s:{s:.3f}' for t,s in zip(ts,sc)),'pass(>=.70) %d/6'%sum(s>=0.70 for s in sc))
