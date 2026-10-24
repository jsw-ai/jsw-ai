import json,subprocess,os,sys,hashlib
P='/workspace/hf-test/zen/posting/camille_songs/01_bonsoir_monaco/'; os.chdir(P)
WAV='/workspace/music/distrokid/camille/01_bonsoir_monaco.wav'
FONTS='/workspace/music_video_test_2026-10-22/v3/r2/fonts'; FN='MontserratR2'
def ts(t):t=max(0,t);return f'{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}'
def crop(W,H,yf):return f"crop='min(iw,ih*{W}/{H})':'min(ih,iw*{H}/{W})':'(iw-ow)/2':'(ih-oh)*{yf}'"
ENC=['-an','-c:v','libx264','-preset','medium','-crf','14','-pix_fmt','yuv420p','-r','30']
def shot(s,W,H,o):
    NF=round(s['d']*30)
    if s['k']=='clip':
        src=f"raw/K_{s['n']}.mp4"
        vf=f"{crop(W,H,0.3)},scale={W}:{H}:flags=lanczos,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=2"
        cmd=['ffmpeg','-v','error','-y','-ss',str(s['ss']),'-i',src,'-vf',vf,'-frames:v',str(NF),*ENC,o]
    else:
        src=f"fin/{s['n']}_v4C.jpg"
        vf=f"{crop(W,H,0.3)},scale={W*2}:{H*2}:flags=lanczos,zoompan=z='1+0.08*on/{NF}':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.3':d=1:s={W}x{H}:fps=30,setsar=1"
        cmd=['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',src,'-vf',vf,'-frames:v',str(NF),*ENC,o]
    subprocess.run(cmd,check=True);return src,NF
def ass(path,W,H,dur,title,card0):
    v=H>W
    ys=[1150,1232,1300] if v else [690,780,850]; szs=[60,50,46] if v else [68,56,50]
    tagy=1780 if v else 1010
    h=f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: T,{FN},48,&H00FFFFFF,&H00FFFFFF,&H00181818,&H00000000,0,0,0,0,100,100,0,0,1,3,0,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    cx=W//2;ev=[]
    def card(a,b,lines):
        for i,(t,y,sz) in enumerate(zip(lines,ys,szs)):
            ev.append(f"Dialogue: 2,{ts(a+0.15*i)},{ts(b)},T,,0,0,0,,{{\\fad(300,300)\\pos({cx},{y})\\fs{sz}}}{t}")
    card(0,title,['Camille Dubois – Bonsoir Monaco','Riviera Après Minuit'])
    ev.append(f"Dialogue: 1,{ts(title)},{ts(card0)},T,,0,0,0,,{{\\fad(250,250)\\pos({cx},{tagy})\\fs{34 if v else 30}}}original audio by Camille Dubois")
    card(card0,dur,['Camille Dubois – Bonsoir Monaco','Riviera Après Minuit','Out now on Apple Music'])
    open(path,'w').write(h+'\n'.join(ev)+'\n')
def render(name,shots,W,H,a0,dur,title,card0):
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
      '-map','[v]','-map','[au]','-c:v','libx264','-profile:v','main','-level','4.1','-pix_fmt','yuv420p','-preset','slow','-b:v','5000k','-maxrate','8M','-bufsize','12M','-r','30',
      '-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart','-map_metadata','-1','-t',f'{dur:.3f}',out],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',out,'-an','-c','copy',f'out/{name}_silent.mp4'],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-ss','8','-i',out,'-frames:v','1',f'out/{name}_thumb.jpg'],check=True)
    md5=hashlib.md5(open(out,'rb').read()).hexdigest()
    json.dump(dict(file=P+out,md5=md5,audio=WAV,audio_start=a0,duration=dur,W=W,H=H,title_card=[0,title],end_card=[card0,dur],ass=P+assf,shots=man),open(f'out/{name}_shots.json','w'),indent=1)
    print('ok',out,md5)
V=['M01_v','M02_v','M03_v','M04_v','M05_v','M06_v','M07_v','M08_v','M09_v','M10_v','M11_v','M12_v']
order=[0,3,1,2,8,5,4,9,6,7,10,11]
which=sys.argv[1]
SS=json.load(open('work/ss.json'))
if which=='hook':
    render('camille_bonsoir_monaco_hook_21s',[dict(k='clip',n=V[i],d=1.75,ss=SS[V[i]+'|1.75']) for i in order],1080,1920,50.0,21.0,2.6,17.0)
if which=='x':
    o2=[11,2,8,0,4,9,3,6,1,10,5,7]
    render('camille_bonsoir_monaco_x_24s',[dict(k='clip',n=V[i],d=2.0,ss=SS[V[i]+'|2.0']) for i in o2],1080,1920,49.6,24.0,3.0,20.0)
if which=='yt':
    Hn=['M01_h','M04_h','M02_heels_h','M03_h','M09_lights_h','M06_h','M05_h','M10_h','M07_h','M08_h','M11_h','M12_h']
    sh=[dict(k='still',n=n,d=1.75) if n in('M09_lights_h','M02_heels_h') else dict(k='clip',n=n,d=1.75,ss=SS[n+'|1.75']) for n in Hn]
    render('camille_bonsoir_monaco_youtube_21s',sh,1920,1080,50.0,21.0,2.6,17.0)
