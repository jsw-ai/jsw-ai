import numpy as np, wave, subprocess, os, textwrap
from PIL import Image, ImageDraw, ImageFont
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',58)
R='/workspace/hf-test/'
def beat(path,bpm,secs,seed):
    sr=44100;n=int(sr*secs);y=np.zeros(n);bl=60/bpm;rng=np.random.default_rng(seed)
    t=np.arange(int(sr*.25))/sr
    kick=np.sin(2*np.pi*(50+110*np.exp(-t*30))*t)*np.exp(-t*12)
    hat=rng.standard_normal(int(sr*.05))*np.exp(-np.arange(int(sr*.05))/sr*90)*.25
    clap=rng.standard_normal(int(sr*.12))*np.exp(-np.arange(int(sr*.12))/sr*35)*.5
    roots=[55,55,65.4,49]
    k=0
    while k*bl/2<secs:
        s=int(k*bl/2*sr)
        def add(x,g=1):
            e=min(n,s+len(x));y[s:e]+=x[:e-s]*g
        if k%2==0: add(kick,.9)
        if k%4==2: add(clap,.6)
        add(hat,.8 if k%2 else .5)
        k+=1
    # bass + pluck arp
    for b in range(int(secs/bl)+1):
        f=roots[(b//4)%4]*2
        s=int(b*bl*sr)
        if s>=n: break
        tt=np.arange(int(bl*sr*.9))/sr
        w=np.sin(2*np.pi*f*tt)*np.exp(-tt*3)*.35
        e=min(n,s+len(w));y[s:e]+=w[:e-s]
        for j,m in enumerate([4,5,6,8]):
            s2=s+int(j*bl/4*sr);tt=np.arange(int(sr*.15))/sr
            if s2>=n: continue
            w=np.sign(np.sin(2*np.pi*f*m*tt))*np.exp(-tt*18)*.07
            e=min(n,s2+len(w));y[s2:e]+=w[:e-s2]
    y=y/np.abs(y).max()*.8
    with wave.open(path,'w') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((y*32767).astype(np.int16).tobytes())
def overlay(text,path):
    im=Image.new('RGBA',(720,1280),(0,0,0,0));d=ImageDraw.Draw(im)
    lines=textwrap.wrap(text,20);h=len(lines)*72
    y0=860
    for i,l in enumerate(lines):
        w=d.textlength(l,font=F);x=(720-w)/2
        d.text((x,y0+i*72),l,font=F,fill='white',stroke_width=6,stroke_fill='black')
    im.save(path)
def make(name,shots,bpm,audioseed):
    dur=60/bpm*2*1.0  # 2 beats per shot
    segs=[]
    for i,(img,txt) in enumerate(shots):
        ov=f'mont/{name}_o{i}.png';overlay(txt,ov)
        out=f'mont/{name}_s{i}.mp4'
        fr=int(dur*30)
        z="zoompan=z='1.0+0.12*on/%d':x='iw/2-(iw/zoom/2)':y='ih*0.30-(ih/zoom*0.30)':d=%d:s=720x1280:fps=30"%(fr,fr) if i%2==0 else "zoompan=z='1.12-0.12*on/%d':x='iw/2-(iw/zoom/2)':y='ih*0.30-(ih/zoom*0.30)':d=%d:s=720x1280:fps=30"%(fr,fr)
        subprocess.run(['ffmpeg','-v','error','-y','-i',R+img,'-i',ov,'-filter_complex',
         f"[0:v]crop=ih*9/16:ih,scale=1440:2560,{z}[b];[b][1:v]overlay=0:0,format=yuv420p",
         '-t',str(dur),'-r','30','-c:v','libx264','-crf','17',out],check=True)
        segs.append(out)
    open(f'mont/{name}.txt','w').write(''.join(f"file '{os.path.abspath(s)}'\n" for s in segs))
    total=dur*len(shots)
    beat(f'mont/{name}.wav',bpm,total,audioseed)
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'mont/{name}.txt','-i',f'mont/{name}.wav',
     '-vf','noise=alls=5:allf=t,unsharp=3:3:0.4','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-map_metadata','-1','-shortest',f'{name}.mp4'],check=True)
A=[('charlotte_r3/fin/r7_v4C.jpg','Rating your chat-up lines'),
('charlotte_r3/fin/r13_v4C.jpg',"\"Do you come here often?\" 2/10"),
('charlotte_test/fin/c6_v4C.jpg',"\"Are you from Tesco?\" 3/10"),
('charlotte_r3/fin/r4_v4C.jpg',"\"Nice weather\" 5/10, you tried"),
('charlotte_test/fin/c7_v4C.jpg',"\"Fancy a brew?\" 10/10"),
('charlotte_r3/fin/r8b_v4C.jpg',"Tea & Confessions. Your turn")]
B=[('charlotte_test/fin/c4_v4C.jpg',"Things I'd never admit to my mum"),
('charlotte_r3/fin/r8_v4C.jpg',"I say \"nearly there\" from the sofa"),
('charlotte_r3/fin/r2_v4C.jpg',"I stretch for 2 mins and call it a workout"),
('charlotte_test/fin/c3_v4C.jpg',"I've left the group chat on read since Tuesday"),
('charlotte_test/fin/c8_v4C.jpg',"I've pretended to like running. Twice"),
('charlotte_r3/fin/r12_v4C.jpg',"Tea & Confessions. Your turn")]
make('montage1_chatup_ratings',A,124,1)
make('montage2_never_admit_to_mum',B,118,2)
