# export.py spec.json -> final/<name>.mp4 (+music) and final/<name>_silent.mp4
# seg: {"v":src,"a":..,"b":..,"sp":1} | {"img":path,"d":..,"z":[1.0,1.04]} ; "tr" on seg k = transition INTO seg k: "cut" | "hblur:0.4" | "white:0.25" | "fadewhite:0.3"
# "hold": seconds to freeze the final frame. texts: [txt,t0,t1,y,(fs)]
import json,sys,subprocess,os
S=json.load(open(sys.argv[1])); n=S['name']; W='/tmp/x_'+n; os.makedirs(W,exist_ok=True)
OUT='/workspace/hf-test/zen/posting/camille_oct22/final/'; os.makedirs(OUT,exist_ok=True)
F='/usr/share/fonts/truetype/sand-box/google/Poppins/Poppins-SemiBold.ttf'
post="fps=30,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,unsharp=5:5:0.3:5:5:0,noise=c0s=7:c0f=t+u,setsar=1,format=yuv420p"
parts=[]
for k,sg in enumerate(S['segs']):
    o=f'{W}/s{k}.mp4'
    if 'v' in sg:
        sp=sg.get('sp',1.0); nf=int(round((sg['b']-sg['a'])/sp*30))
        vf=f"setpts=(PTS-STARTPTS)/{sp},"+post
        if k==len(S['segs'])-1 and S.get('hold'): vf+=f",tpad=stop_mode=clone:stop_duration={S['hold']}"; nf+=int(round(S['hold']*30))
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(sg['a']),'-i',sg['v'],'-vf',vf,'-frames:v',str(nf),'-an','-c:v','libx264','-crf','12','-preset','fast','-r','30',o],check=True)
    else:
        nf=int(round(sg['d']*30)); z0,z1=sg.get('z',[1.0,1.04])
        vf=(f"scale=2160:-1:flags=lanczos,zoompan=z='{z0}+({z1}-{z0})*on/{nf}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={nf}:s=1080x1912:fps=30,"+post)
        subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-i',sg['img'],'-vf',vf,'-frames:v',str(nf),'-an','-c:v','libx264','-crf','12','-preset','fast','-r','30',o],check=True)
    d=float(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v','-show_entries','stream=nb_read_frames','-of','csv=p=0',o]))/30
    parts.append((o,d,sg.get('tr','cut')))
ins=[]; fl=[f'[{i}:v]settb=1/30,setpts=N/30/TB,setsar=1,fps=30[n{i}]' for i in range(len(parts))]; cur='[n0]'; T=parts[0][1]; cuts=[0.0]
for i,(o,d,tr) in enumerate(parts): ins+=['-i',o]
for i in range(1,len(parts)):
    o,d,tr=parts[i]; lab=f'[c{i}]'
    if tr=='cut':
        fl.append(f"{cur}[n{i}]concat=n=2:v=1:a=0,fps=30,settb=1/30{lab}"); cuts.append(round(T,3)); T+=d
    else:
        kind,du=tr.split(':'); du=float(du)
        if kind=='hblur': fl.append(f"{cur}[n{i}]xfade=transition=hblur:duration={du}:offset={T-du:.4f}{lab}"); cuts.append(round(T-du/2,3)); T+=d-du
        elif kind=='white': fl.append(f"[n{i}]fade=t=in:st=0:d={du}:color=white[f{i}];{cur}[f{i}]concat=n=2:v=1:a=0,fps=30,settb=1/30{lab}"); cuts.append(round(T,3)); T+=d
        elif kind=='fade': fl.append(f"{cur}[n{i}]xfade=transition=fade:duration={du}:offset={T-du:.4f}{lab}"); cuts.append(round(T-du/2,3)); T+=d-du
        elif kind=='fadewhite': fl.append(f"{cur}[n{i}]xfade=transition=fadewhite:duration={du}:offset={T-du:.4f}{lab}"); cuts.append(round(T-du/2,3)); T+=d-du
    cur=lab
dur=T
dt=[]; i=0
def tv(x): return cuts[int(x[3:])] if isinstance(x,str) else x
for tx in S['texts']:
    txt,t0,t1,yy=tx[:4]; fs=tx[4] if len(tx)>4 else S.get('fs',60); t0,t1=tv(t0),tv(t1)
    for j,line in enumerate(txt.split('\n')):
        p=f'{W}/t{i}.txt'; open(p,'w').write(line); i+=1
        dt.append(f"drawtext=fontfile={F}:textfile={p}:fontsize={fs}:fontcolor=white:borderw=4:bordercolor=black@0.9:shadowx=0:shadowy=3:shadowcolor=black@0.5:x=(w-text_w)/2:y={yy+j*int(fs*1.3)}:enable='gte(t,{t0-0.001})*lt(t,{t1-0.001})'")
fl.append(f"{cur}{','.join(dt) or 'null'},scale=out_range=tv,format=yuv420p[v]")
enc=['-c:v','libx264','-profile:v','main','-crf',str(S.get('crf',19)),'-preset','slow','-pix_fmt','yuv420p','-color_range','tv','-r','30','-maxrate','12M','-bufsize','24M','-map_metadata','-1','-fflags','+bitexact','-movflags','+faststart']
sil=OUT+n+'_silent.mp4'; full=OUT+n+'.mp4'
subprocess.run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',';'.join(fl),'-map','[v]','-an','-t',f'{dur:.4f}']+enc+[sil],check=True)
if S.get('music'):
    fo=max(dur-1.2,0); m=S['moff']
    subprocess.run(['ffmpeg','-v','error','-y','-i',sil,'-i',S['music'],'-filter_complex',f"[1:a]atrim={m}:{m+dur},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.3,afade=t=out:st={fo}:d=1.2,volume={S.get('vol',0.85)}[o]",'-map','0:v','-map','[o]','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart','-map_metadata','-1','-fflags','+bitexact',full],check=True)
print(n,'dur',round(dur,3),'cuts',cuts,'MB',round(os.path.getsize(full if S.get('music') else sil)/1e6,2))
