# qc.py name mp4 outdir  -> frames every 0.5s, identity gate per frame, sheet = ref sheet | frame grid with scores
import sys,subprocess,os,re,glob,json
from PIL import Image,ImageDraw,ImageFont
name,mp4,out=sys.argv[1:4]
D=f'frames/{name}'; os.makedirs(D,exist_ok=True); [os.remove(f) for f in glob.glob(D+'/*.png')]
subprocess.run(['ffmpeg','-v','error','-y','-i',mp4,'-vf','fps=2','-start_number','0',D+'/f%03d.png'],check=True)
fs=sorted(glob.glob(D+'/f*.png'))
g=subprocess.run(['/workspace/.face-venv/bin/python','/workspace/hf-test/zen/posting/identity_gate.py','img','--model','camille_v3_draft']+fs,capture_output=True,text=True).stdout
sc={}
for blk in re.split(r'\n(?=PASS|FAIL)',g):
    m=re.match(r'(PASS|FAIL) (\S+)',blk); c=re.search(r"score_centroid': ([0-9.]+|None)",blk)
    if m: sc[os.path.basename(m.group(2))]=(c.group(1) if c else 'None')
json.dump(sc,open(D+'/scores.json','w'))
ref=Image.open('/workspace/hf-test/zen/posting/camille_oct16/REFERENCE_CONTACT_SHEET_v4.jpg').convert('RGB')
H=1400; ref=ref.resize((int(ref.width*H/ref.height),H))
cols=8; th=340; ims=[Image.open(f).convert('RGB') for f in fs]; tw=int(ims[0].width*th/ims[0].height)
rows=(len(ims)+cols-1)//cols; gh=rows*(th+26)
s=Image.new('RGB',(ref.width+cols*(tw+4)+10,max(H,gh)+40),'white'); d=ImageDraw.Draw(s); fnt=ImageFont.load_default(size=20)
d.text((5,5),f'{name}: left = approved REFERENCE_CONTACT_SHEET_v4 ; right = every 0.5 s, gate centroid',fill='black',font=fnt)
s.paste(ref,(0,36))
for k,(im,f) in enumerate(zip(ims,fs)):
    x=ref.width+10+(k%cols)*(tw+4); y=36+(k//cols)*(th+26)
    s.paste(im.resize((tw,th)),(x,y)); v=sc.get(os.path.basename(f),'?')
    col='green' if v not in('None','?') and float(v)>=0.78 else 'red'
    d.text((x,y+th+2),f'{k*0.5:.1f}s {v}',fill=col,font=fnt)
os.makedirs(out,exist_ok=True); s.save(f'{out}/{name}_sidebyside.jpg',quality=88)
vals=[float(v) for v in sc.values() if v not in('None',)]
print(name,'n',len(fs),'min',min(vals) if vals else None,'med',sorted(vals)[len(vals)//2] if vals else None,' '.join(f"{i*0.5:.1f}:{sc.get(os.path.basename(f))}" for i,f in enumerate(fs)))
