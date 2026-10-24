import sys,subprocess,os
from PIL import Image,ImageDraw
REF='/workspace/hf-test/zen/posting/reference_set_gabriela.jpg'
def frames(p):
    if p.endswith('.mp4'):
        d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]))
        out=[]
        for i,t in enumerate([d*0.2,d*0.5,d*0.85]):
            f=f'/tmp/sbs_{os.getpid()}_{i}.jpg'; subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t:.2f}','-i',p,'-frames:v','1',f],check=True); out.append(Image.open(f).convert('RGB'))
        return out
    return [Image.open(p).convert('RGB')]
def sbs(p,out,H=1280):
    r=Image.open(REF).convert('RGB'); r=r.resize((int(r.width*H/r.height),H))
    ims=[i.resize((int(i.width*H/i.height),H)) for i in frames(p)]
    S=Image.new('RGB',(r.width+sum(i.width for i in ims)+10*len(ims),H+40),'white'); S.paste(r,(0,40)); x=r.width+10
    for i in ims: S.paste(i,(x,40)); x+=i.width+10
    ImageDraw.Draw(S).text((10,10),f'LEFT: reference_set_gabriela.jpg | RIGHT: {os.path.basename(p)} (same height {H}px)',fill='black')
    S.save(out,quality=85); print(out)
for p in sys.argv[1:]: sbs(p,'v2/sbs/'+os.path.basename(p).rsplit('.',1)[0]+'_sbs.jpg')
