import subprocess,json,sys
from PIL import Image,ImageDraw,ImageFont
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def card(text,path):
    d=ImageDraw.Draw(Image.new('RGB',(1,1))); fs=60
    while True:
        f=ImageFont.truetype(F,fs); w=d.textbbox((0,0),text,font=f)[2]
        if w+56<=900 or fs<=36: break
        fs-=2
    W=w+56;H=int(fs*1.3)+36
    im=Image.new('RGBA',(W,H),(0,0,0,0));D=ImageDraw.Draw(im)
    D.rounded_rectangle((0,0,W-1,H-1),22,fill=(255,255,255,240)); D.text((28,16),text,font=f,fill=(10,10,10)); im.save(path); return W
def build(name,shots,texts,track,mstart):
    inp=[];fc=[];tot=0
    for i,(c,s,d) in enumerate(shots):
        tot+=d; inp+=['-ss',str(s),'-t',str(d),'-i',f'clips/{c}.mp4']
        fc.append(f"[{i}:v]fps=30,scale=1084:-2:flags=lanczos,crop=1080:1920,unsharp=5:5:0.35,setsar=1,setpts=PTS-STARTPTS,trim=duration={d}[v{i}]")
    n=len(shots); fc.append(''.join(f'[v{i}]' for i in range(n))+f"concat=n={n}:v=1:a=0,noise=alls=3:allf=t[b0]")
    last='b0'
    for j,(t,a,b) in enumerate(texts):
        W=card(t,f'txt_{name}_{j}.png'); inp+=['-i',f'txt_{name}_{j}.png']
        fc.append(f"[{last}][{n+j}:v]overlay=(W-w)/2:1560:enable='between(t,{a},{b})'[o{j}]"); last=f'o{j}'
    k=n+len(texts); inp+=['-ss',str(mstart),'-t',str(tot),'-i',f'music/{track}.mp3']
    fc.append(f"[{k}:a]afade=t=in:d=0.05,afade=t=out:st={tot-0.5}:d=0.5,loudnorm=I=-14:TP=-1.5[ao]")
    out=f'../{name}.mp4'
    subprocess.check_call(['ffmpeg','-loglevel','error','-y']+inp+['-filter_complex',';'.join(fc),'-map',f'[{last}]','-map','[ao]','-t',str(tot),'-c:v','libx264','-profile:v','main','-crf','20','-maxrate','8M','-bufsize','16M','-preset','slow','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','128k','-ar','44100','-map_metadata','-1','-fflags','+bitexact','-movflags','+faststart',out])
    print(name,tot)
B=json.load(open('music/beats.json'))
cfg=json.load(open(sys.argv[1]))
for name,v in cfg.items(): build(name,v['shots'],v['texts'],v['track'],B.get(v['track'],{}).get('start',30))
