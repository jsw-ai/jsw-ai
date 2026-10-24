import json,subprocess,os,sys
W0='/workspace/hf-test/zen/posting/valentina_songvideos'; os.chdir(W0+'/work')
WAV='/workspace/music/distrokid/valentina/02_fuego_lento.wav'
FONTS=os.path.abspath('fonts'); FN='MontserratR2'
TITLE='Valentina Reyes – Fuego Lento – Corazón de Cartagena'
def ts(t):t=max(0,t);return f'{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}'
def crop(W,H,xf,yf,z=1.0):
    return f"crop='min(iw,ih*{W}/{H})/{z}':'min(ih,iw*{H}/{W})/{z}':'(iw-ow)*{xf}':'(ih-oh)*{yf}'"
def shot(s,W,H,o):
    NF=round(s['d']*30); xf=s.get('xf',0.5); yf=s.get('yf',0.3); z=s.get('z',1.0)
    enc=['-an','-threads','2','-c:v','libx264','-preset','veryfast','-crf','14','-pix_fmt','yuv420p','-r','30']
    if s['k']=='clip':
        sp=s.get('speed',1.0)
        vf=f"{crop(W,H,xf,yf,z)},scale={W}:{H}:flags=lanczos,setsar=1,setpts={1/sp:.4f}*(PTS-STARTPTS),fps=30,tpad=stop_mode=clone:stop_duration=2"
        cmd=['ffmpeg','-v','error','-y','-ss',f"{s.get('ss',0):.3f}",'-i',s['src'],'-vf',vf,'-frames:v',str(NF),*enc,o]
    else:
        zr=s.get('zr',0.08); mo=s.get('mo','in')
        ze=f"1+{zr}*on/{NF}" if mo=='in' else f"{1+zr}-{zr}*on/{NF}"
        px=s.get('px',0.5); py=s.get('py',0.3)
        vf=f"{crop(W,H,xf,yf,z)},scale={W*2}:{H*2}:flags=lanczos,zoompan=z='{ze}':x='(iw-iw/zoom)*{px}':y='(ih-ih/zoom)*{py}':d=1:s={W}x{H}:fps=30,setsar=1"
        cmd=['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',s['src'],'-vf',vf,'-frames:v',str(NF),*enc,o]
    subprocess.run(cmd,check=True); return NF
def ass(path,W,H,dur,a0,lyr,title_end,card0):
    v=H>W
    if v: fl,ml,mv=60,90,1920-1450; ys=[1150,1240]; szs=[50,40]; tagy=1880-30
    else: fl,ml,mv=50,160,95; ys=[700,780]; szs=[60,44]; tagy=1040
    h=f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,{FN},{fl},&H00FFFFFF,&H00FFFFFF,&H00181818,&H00000000,0,0,0,0,100,100,0,0,1,3,0,2,{ml},{ml},{mv},1
Style: T,{FN},48,&H00FFFFFF,&H00FFFFFF,&H00181818,&H00000000,0,0,0,0,100,100,0,0,1,3,0,5,{ml},{ml},0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev=[];cx=W//2
    t1=('Valentina Reyes – Fuego Lento\\N– Corazón de Cartagena' if v else TITLE)
    ev.append(f"Dialogue: 2,{ts(0)},{ts(title_end)},T,,0,0,0,,{{\\fad(300,350)\\pos({cx},{ys[0]})\\fs{szs[0]}}}{t1}")
    tag='original audio by Valentina Reyes'
    ev.append(f"Dialogue: 2,{ts(0.15)},{ts(title_end)},T,,0,0,0,,{{\\fad(300,350)\\pos({cx},{ys[1]+(60 if v else 0)})\\fs{szs[1]}}}{tag}")
    for j,(a,b,s) in enumerate(lyr):
        a-=a0;b-=a0
        if b<=title_end+0.3 or a>=card0: continue
        a=max(a,title_end+0.05)
        ev.append(f"Dialogue: 1,{ts(a)},{ts(min(b,card0)-0.05)},L,,0,0,0,,{{\\fad(120,120)}}{s}")
    ev.append(f"Dialogue: 2,{ts(card0)},{ts(dur)},T,,0,0,0,,{{\\fad(350,300)\\pos({cx},{ys[0]})\\fs{szs[0]+14}}}Out now on Apple Music")
    ev.append(f"Dialogue: 2,{ts(card0+0.15)},{ts(dur)},T,,0,0,0,,{{\\fad(350,300)\\pos({cx},{ys[0]+(95 if v else 85)})\\fs{szs[1]}}}Valentina Reyes – Fuego Lento")
    ev.append(f"Dialogue: 2,{ts(card0+0.3)},{ts(dur)},T,,0,0,0,,{{\\fad(350,300)\\pos({cx},{ys[0]+(160 if v else 145)})\\fs{szs[1]-4}}}original audio by Valentina Reyes")
    open(path,'w').write(h+'\n'.join(ev)+'\n')
def render(name,shots,W,H,a0,dur,lyr,title_end,card0,br,maxrate):
    T=f'tmp_{name}';os.makedirs(T,exist_ok=True);lst=[];man=[];t=0
    srcs=[(s['src'],s.get('ss',0)) for s in shots if s['k']=='clip']; assert len(srcs)==len(set(srcs)),'repeat clip'
    for i,s in enumerate(shots):
        o=f'{T}/s{i:02d}.mp4';NF=shot(s,W,H,o);lst.append(o)
        man.append(dict(i=i,t0=round(t,3),t1=round(t+NF/30,3),scene=s['scene'],kind=s['k'],source=s['src'],
          motion=(f"clip ss={s.get('ss',0)} speed={s.get('speed',1.0)}" if s['k']=='clip' else f"kenburns {s.get('mo','in')} zr={s.get('zr',0.08)}"),crop=dict(xf=s.get('xf',0.5),yf=s.get('yf',0.3),z=s.get('z',1.0)),note=s.get('note','')))
        t+=NF/30
    open(f'{T}/list.txt','w').write(''.join(f"file '{os.path.abspath(x)}'\n" for x in lst))
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{T}/list.txt','-c','copy',f'{T}/master.mp4'],check=True)
    assf=f'{name}.ass'; ass(assf,W,H,dur,a0,lyr,title_end,card0)
    out=f'{W0}/{name}.mp4'
    if os.path.exists(out): sys.exit('refusing to overwrite '+out)
    fade=f"afade=t=in:d=0.05,afade=t=out:st={dur-1.5:.2f}:d=1.5"
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'{T}/master.mp4','-ss',f'{a0:.3f}','-t',f'{dur:.3f}','-i',WAV,'-filter_complex',
      f"[0:v]scale=out_range=tv,format=yuv420p,subtitles={assf}:fontsdir={FONTS},setparams=range=tv[v];[1:a]{fade}[au]",
      '-map','[v]','-map','[au]','-threads','2','-c:v','libx264','-profile:v','main','-level','4.1','-pix_fmt','yuv420p','-color_range','tv','-preset','slow','-b:v',br,'-maxrate',maxrate,'-bufsize','10M','-r','30',
      '-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart','-map_metadata','-1','-t',f'{dur:.3f}',out],check=True)
    json.dump(dict(file=out,audio=WAV,audio_start=a0,duration=dur,W=W,H=H,shots=man),open(f'{name}_shots.json','w'),indent=1)
    print('ok',out)
