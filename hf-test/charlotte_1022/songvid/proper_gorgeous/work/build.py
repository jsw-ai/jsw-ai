import json,subprocess,os,sys
os.chdir('/workspace/hf-test/charlotte_1022/songvid/proper_gorgeous/work')
WAV='/workspace/music/distrokid/charlotte/02_proper_gorgeous.wav'
FONTS=os.path.abspath('fonts'); FN='MontserratR2'
LYR=json.load(open('lyrics.json'))  # [[start,end,text],...] song time
def ts(t):t=max(0,t);return f'{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}'
ENC=['-an','-c:v','libx264','-preset','medium','-crf','14','-pix_fmt','yuv420p','-r','30','-threads','2']
def shot(s,W,H,o):
    NF=round(s['d']*30); v=H>W; yf=s.get('yf',0.5 if v else 0.12)
    crop=f"crop='min(iw,ih*{W}/{H})':'min(ih,iw*{H}/{W})':'(iw-ow)/2':'(ih-oh)*{yf}'"
    if s['k']=='clip':
        src=f"clips/k_{s['n']}.mp4"
        vf=f"{crop},scale={W}:{H}:flags=lanczos,unsharp=5:5:0.4,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=2"
        cmd=['ffmpeg','-v','error','-y','-ss',f"{s.get('ss',0):.3f}",'-i',src,'-vf',vf,'-frames:v',str(NF),*ENC,o]
    else:
        src=f"stills/{s['n']}.jpg"; zr=0.08; mo=s.get('mo','in')
        ze=f"1+{zr}*on/{NF}" if mo=='in' else f"{1+zr}-{zr}*on/{NF}"
        vf=f"{crop},scale={W*2}:{H*2}:flags=lanczos,zoompan=z='{ze}':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.3':d=1:s={W}x{H}:fps=30,setsar=1"
        cmd=['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',src,'-vf',vf,'-frames:v',str(NF),*ENC,o]
    subprocess.run(cmd,check=True); return src,NF
def ass(path,W,H,dur,a0,title_end,card0):
    v=H>W
    if v: lsz,ml,mv,tsz,tag_y,ty,cy=62,80,430,62,150,1180,1180
    else: lsz,ml,mv,tsz,tag_y,ty,cy=58,160,90,64,70,800,800
    h=f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,{FN},{lsz},&H00FFFFFF,&H00FFFFFF,&H00181818,&H64000000,0,0,0,0,100,100,0,0,1,3,2,2,{ml},{ml},{mv},1
Style: T,{FN},{tsz},&H00FFFFFF,&H00FFFFFF,&H00181818,&H64000000,0,0,0,0,100,100,0,0,1,3,2,5,{ml},{ml},0,1
Style: G,{FN},34,&H00FFFFFF,&H00FFFFFF,&H00181818,&H64000000,0,0,0,0,100,100,0,0,1,2,1,8,{ml},{ml},{tag_y},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    cx=W//2; ev=[]
    title='Charlotte Hayes –\\NProper Gorgeous –\\NProper Gorgeous' if v else 'Charlotte Hayes – Proper Gorgeous – Proper Gorgeous'
    ev.append(f"Dialogue: 2,{ts(0)},{ts(title_end)},T,,0,0,0,,{{\\fad(250,300)\\pos({cx},{ty})}}{title}")
    ev.append(f"Dialogue: 2,{ts(0)},{ts(dur)},G,,0,0,0,,original audio by Charlotte Hayes")
    rel='Out now on\\NApple Music' if v else 'Out now on Apple Music'
    ev.append(f"Dialogue: 2,{ts(card0)},{ts(dur)},T,,0,0,0,,{{\\fad(250,0)\\pos({cx},{cy})\\fs{tsz+14}}}{rel}")
    for j,(a,b,s) in enumerate(LYR):
        if j+1<len(LYR): b=min(b,LYR[j+1][0]-0.04)
        a-=a0;b-=a0
        if b<=title_end+0.3 or a>=card0: continue
        a=max(a,title_end); b=min(b,card0-0.05)
        ev.append(f"Dialogue: 1,{ts(a)},{ts(b)},L,,0,0,0,,{{\\fad(100,100)}}{s}")
    open(path,'w').write(h+'\n'.join(ev)+'\n')
def render(name,shots,W,H,a0,dur,title_end,card0,br,maxrate):
    T=f'tmp_{name}';os.makedirs(T,exist_ok=True);lst=[];man=[];t=0
    for i,s in enumerate(shots):
        o=f'{T}/s{i:02d}.mp4';src,NF=shot(s,W,H,o);lst.append(o)
        man.append(dict(t0=round(t,3),t1=round(t+NF/30,3),scene=s['n'],kind=s['k'],source=os.path.abspath(src),ss=s.get('ss'),motion='Kling 3.0 clip, speed 1.0, hard cut' if s['k']=='clip' else f"Ken Burns {s.get('mo','in')} on approved still"))
        t+=NF/30
    open(f'{T}/list.txt','w').write(''.join(f"file '{os.path.abspath(x)}'\n" for x in lst))
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{T}/list.txt','-c','copy',f'{T}/master.mp4'],check=True)
    assf=f'{name}.ass'; ass(assf,W,H,dur,a0,title_end,card0)
    out=f'../final/{name}.mp4'
    if os.path.exists(out): sys.exit('refusing to overwrite '+out)
    fade=f"afade=t=in:d=0.05,afade=t=out:st={dur-1.5:.2f}:d=1.5"
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'{T}/master.mp4','-ss',f'{a0:.3f}','-t',f'{dur:.3f}','-i',WAV,'-filter_complex',
      f"[0:v]format=yuv420p,subtitles={assf}:fontsdir={FONTS}[v];[1:a]{fade}[au]",'-threads','2',
      '-map','[v]','-map','[au]','-c:v','libx264','-profile:v','high','-level','4.1','-pix_fmt','yuv420p','-preset','slow','-b:v',br,'-maxrate',maxrate,'-bufsize','12M','-r','30',
      '-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart','-map_metadata','-1','-t',f'{dur:.3f}',out],check=True)
    json.dump(dict(file=os.path.abspath(out),audio=WAV,audio_start=a0,duration=dur,W=W,H=H,ass=os.path.abspath(assf),shots=man),open(f'{name}_shots.json','w'),indent=1)
    print('ok',out)
