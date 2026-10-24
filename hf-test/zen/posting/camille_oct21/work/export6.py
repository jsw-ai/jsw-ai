# export3.py spec.json -> final_v3/<name>_v3.mp4 + _v6_silent.mp4
# segs: [src,a,b] or [src,a,b,speed]; every segment is an exact number of 30 fps frames, cut times printed;
# text times may be numbers or "cutK" (= start time of segment K) so captions switch exactly on the cut frame.
import json,sys,subprocess,os
S=json.load(open(sys.argv[1])); n=S['name']; W='x_'+n; os.makedirs(W,exist_ok=True)
OUT='/workspace/hf-test/zen/posting/camille_oct21/final/'; os.makedirs(OUT,exist_ok=True)
F='/usr/share/fonts/truetype/sand-box/google/Poppins/Poppins-SemiBold.ttf'
if not os.path.exists(F): F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
parts=[]; cuts=[0.0]; T=0
for k,sg in enumerate(S['segs']):
    src,a,b=sg[:3]; sp=sg[3] if len(sg)>3 else 1.0
    nf=int(round((b-a)/sp*30)); o=f'{W}/s{k}.mp4'; parts.append(o)
    vf=f"setpts=(PTS-STARTPTS)/{sp},fps=30,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,noise=alls=3:allf=t,format=yuv420p"
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-i',src,'-vf',vf,'-frames:v',str(nf),'-an','-c:v','libx264','-crf','12','-preset','fast','-r','30',o],check=True)
    T+=nf/30; cuts.append(round(T,4))
open(f'{W}/l.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{W}/l.txt','-c','copy',f'{W}/cat.mp4'],check=True)
dur=T
def tv(x): return cuts[int(x[3:])] if isinstance(x,str) else x
dt=[]; fs=S.get('fs',60); i=0
for txt,t0,t1,yy in S['texts']:
    t0,t1=tv(t0),tv(t1)
    for j,line in enumerate(txt.split('\n')):
        p=f'{W}/t{i}.txt'; open(p,'w').write(line); i+=1
        dt.append(f"drawtext=fontfile={F}:textfile={p}:fontsize={fs}:fontcolor=white:borderw=4:bordercolor=black@0.9:shadowx=0:shadowy=3:shadowcolor=black@0.5:x=(w-text_w)/2:y={yy+j*int(fs*1.3)}:enable='gte(t,{t0-0.001})*lt(t,{t1-0.001})'")
vf=','.join(dt) or 'null'
enc=['-c:v','libx264','-profile:v','main','-crf',str(S.get('crf',19)),'-preset','slow','-pix_fmt','yuv420p','-r','30','-maxrate','12M','-bufsize','24M','-map_metadata','-1','-fflags','+bitexact','-movflags','+faststart']
sil=OUT+n+'_v6_silent.mp4'; full=OUT+n+'_v6.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{W}/cat.mp4','-vf',vf,'-an']+enc+[sil],check=True)
ins=['-i',sil]; fl=[]; mix=[]; k=1
if S.get('music'):
    fo=max(dur-1.2,0); ins+=['-stream_loop','-1','-i',S['music']]
    fl.append(f"[{k}:a]atrim={S.get('moff',0)}:{S.get('moff',0)+dur},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.4,afade=t=out:st={fo}:d=1.2,volume={S.get('vol',0.8)}[m{k}]"); mix.append(f'[m{k}]'); k+=1
if S.get('own_audio'):
    src,a,b=S['own_audio']; ins+=['-i',src]
    fl.append(f"[{k}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=out:st={dur-0.3}:d=0.3[m{k}]"); mix.append(f'[m{k}]'); k+=1
for src,t,v in S.get('sfx',[]):
    t=tv(t) if isinstance(t,str) else t
    ins+=['-i',src]; ms=int(t*1000)
    fl.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={v},adelay={ms}|{ms},apad[m{k}]"); mix.append(f'[m{k}]'); k+=1
fl.append(''.join(mix)+f"amix=inputs={len(mix)}:duration=first:normalize=0,apad,atrim=0:{dur}[o]")
subprocess.run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',';'.join(fl),'-map','0:v','-map','[o]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart','-map_metadata','-1',full],check=True)
print(n,'dur',round(dur,3),'cuts',cuts,'MB',round(os.path.getsize(full)/1e6,2))
