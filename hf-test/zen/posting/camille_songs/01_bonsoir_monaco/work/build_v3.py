import json,subprocess,os,sys,hashlib
P='/workspace/hf-test/zen/posting/camille_songs/01_bonsoir_monaco/'; os.chdir(P)
WAV='/workspace/music/distrokid/camille/01_bonsoir_monaco.wav'
FONTS='/workspace/music_video_test_2026-10-22/v3/r2/fonts'; FN='MontserratR2'
A0=[0]
BR=['5000k','8M']
LYR=[(53.2,55.15,'Bonsoir, Monaco'),(55.22,58.4,'Show me where the bright ones go'),(58.46,62.4,'Casino lights and the sea below'),(62.96,66.8,'Bonsoir, bonsoir, Monaco')]
def ts(t):t=max(0,t);return f'{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}'
def crop(W,H,yf):return f"crop='min(iw,ih*{W}/{H})':'min(ih,iw*{H}/{W})':'(iw-ow)/2':'(ih-oh)*{yf}'"
ENC=['-an','-c:v','libx264','-preset','medium','-crf','14','-pix_fmt','yuv420p','-r','30']
def shot(s,W,H,o):
    NF=round(s['d']*30)
    if s['k']=='clip':
        src=f"raw/K_{s['n']}.mp4"; s.setdefault('ss',0)
        vf=f"{crop(W,H,0.3)},scale={W}:{H}:flags=lanczos,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=2"
        cmd=['ffmpeg','-v','error','-y','-ss',str(s['ss']),'-i',src,'-vf',vf,'-frames:v',str(NF),*ENC,o]
    else:
        src=f"fin/{s['n']}_v4C.jpg"
        vf=f"{crop(W,H,0.3)},scale={W*2}:{H*2}:flags=lanczos,zoompan=z='1+0.08*on/{NF}':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.3':d=1:s={W}x{H}:fps=30,setsar=1"
        cmd=['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',src,'-vf',vf,'-frames:v',str(NF),*ENC,o]
    subprocess.run(cmd,check=True);return src,NF
def ass(path,W,H,dur,title,card0):
    v=H>W
    ys=[1150,1232,1300] if v else [690,780,850]; szs=[52,52,46] if v else [64,60,50]
    tagy=1780 if v else 60
    fl,ml,mv=(60,90,470) if v else (50,160,95)
    h=f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,{FN},{fl},&H00FFFFFF,&H00FFFFFF,&H00181818,&H00000000,0,0,0,0,100,100,0,0,1,3,0,2,{ml},{ml},{mv},1
Style: T,{FN},48,&H00FFFFFF,&H00FFFFFF,&H00181818,&H00000000,0,0,0,0,100,100,0,0,1,3,0,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    cx=W//2;ev=[]
    def card(a,b,lines):
        for i,(t,y,sz) in enumerate(zip(lines,ys,szs)):
            ev.append(f"Dialogue: 2,{ts(a+0.15*i)},{ts(b)},T,,0,0,0,,{{\\fad(300,300)\\pos({cx},{y})\\fs{sz}}}{t}")
    card(0,title,['Camille Dubois – Bonsoir Monaco –','Riviera Après Minuit'])
    for a,b,t in LYR:
        a-=A0[0];b-=A0[0]
        if a<title-0.01 or a>=card0: continue
        ev.append(f"Dialogue: 1,{ts(a)},{ts(min(b,card0-0.05))},L,,0,0,0,,{{\\fad(120,120)}}{t}")
    ev.append(f"Dialogue: 1,{ts(title)},{ts(card0)},T,,0,0,0,,{{\\fad(250,250)\\pos({cx},{tagy})\\fs{34 if v else 30}}}original audio by Camille Dubois")
    card(card0,dur,['Camille Dubois – Bonsoir Monaco –','Riviera Après Minuit','Out now on Apple Music'])
    open(path,'w').write(h+'\n'.join(ev)+'\n')
def render(name,shots,W,H,a0,dur,title,card0):
    A0[0]=a0
    if os.path.exists(f'out/{name}.mp4'): sys.exit('refusing to overwrite')
    T=f'tmp/{name}';os.makedirs(T,exist_ok=True);lst=[];man=[];t=0
    assert len(set(s['n'] for s in shots))==len(shots)
    for i,s in enumerate(shots):
        o=f'{T}/s{i:02d}.mp4';src,NF=shot(s,W,H,o);lst.append(o)
        man.append(dict(t0=round(t,3),t1=round(t+NF/30,3),scene=s['n'],kind=s['k'],source=P+src,ss=s.get('ss')));t+=NF/30
    open(f'{T}/list.txt','w').write(''.join(f"file '{P}{x}'\n" for x in lst))
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{T}/list.txt','-c','copy',f'{T}/master.mp4'],check=True)
    assf=f'work/{name}.ass';ass(assf,W,H,dur,title,card0)
    out=f'out/{name}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-threads','2','-i',f'{T}/master.mp4','-ss',f'{a0:.3f}','-t',f'{dur:.3f}','-i',WAV,'-filter_complex',
      f"[0:v]format=yuv420p,subtitles={assf}:fontsdir={FONTS}[v];[1:a]afade=t=in:d=0.05,afade=t=out:st={dur-1.5:.2f}:d=1.5[au]",
      '-map','[v]','-map','[au]','-c:v','libx264','-profile:v','main','-level','4.1','-pix_fmt','yuv420p','-preset','slow','-b:v',BR[0],'-maxrate',BR[1],'-bufsize','12M','-r','30',
      '-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart','-map_metadata','-1','-t',f'{dur:.3f}',out],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',out,'-an','-c','copy',f'out/{name}_silent.mp4'],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-ss','8','-i',out,'-frames:v','1',f'out/{name}_thumb.jpg'],check=True)
    md5=hashlib.md5(open(out,'rb').read()).hexdigest()
    json.dump(dict(file=P+out,md5=md5,audio=WAV,audio_start=a0,duration=dur,W=W,H=H,title_card=[0,title],end_card=[card0,dur],ass=P+assf,shots=man),open(f'out/{name}_shots.json','w'),indent=1)
    print('ok',out,md5)
V=['M01_v','M02t_v','M03_v','M04_v','M05_v','M06_v','M07_v','M08_v','M09_v','M10_v','M11_v','M12_v']
which=sys.argv[1]
SS=json.load(open('work/ss.json')); SS.update(json.load(open('work/ss_v3.json')))
def mk(o,d):
    sh=[dict(k='clip',n=V[i],d=d,ss=SS[V[i]+'|'+str(d)]) for i in o]
    for x in sh:
        if x['n']=='M05_v' and d==1.75: x['ss']=3.25
        if x['n']=='M09_v' and d==2.0: x['ss']=2.4
    assert 'M02_v' not in [x['n'] for x in sh]; return sh
if which=='hook': render('camille_bonsoir_monaco_hook_21s_v3',mk([0,3,1,2,8,5,4,9,6,7,10,11],1.75),1080,1920,50.0,21.0,2.6,17.0)
if which=='x':
    BR[:]=['4300k','4.6M']; render('camille_bonsoir_monaco_x_24s_v3',mk([11,2,8,0,4,9,3,6,1,10,5,7],2.0),1080,1920,49.6,24.0,3.0,20.0)
PL={'tiktok':[2,9,0,6,10,4,1,7,11,5,8,3],'igreel':[5,10,3,0,8,1,11,6,2,9,4,7],'fb':[9,4,11,1,7,2,6,0,10,3,5,8],'reddit':[10,6,1,8,3,11,0,5,9,2,7,4],'ytshorts':[1,7,5,11,0,9,2,10,4,8,3,6]}
if which in PL: render(f'camille_bonsoir_monaco_{which}_21s_v3',mk(PL[which],1.75),1080,1920,50.0,21.0,2.6,17.0)
