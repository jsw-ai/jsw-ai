# export2.py spec.json -> final_v2/<name>_v2.mp4 + _v2_silent.mp4 ; full-frame 9:16, text drawn directly on video, centered, H.264 Main
import json,sys,subprocess,os
S=json.load(open(sys.argv[1])); n=S['name']; W='work/x_'+n; os.makedirs(W,exist_ok=True)
OUT='/workspace/hf-test/zen/posting/camille_oct20/final_v2/'; os.makedirs(OUT,exist_ok=True)
F='/usr/share/fonts/truetype/sand-box/google/Poppins/Poppins-SemiBold.ttf'
if not os.path.exists(F): F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
parts=[]
for k,(src,a,b) in enumerate(S['segs']):
    o=f'{W}/s{k}.mp4'; parts.append(o)
    vf="scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,unsharp=5:5:0.3,noise=alls=3:allf=t,fps=30,format=yuv420p"
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i',src,'-vf',vf,'-an','-c:v','libx264','-crf','14','-preset','fast',o],check=True)
open(f'{W}/l.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{W}/l.txt','-c','copy',f'{W}/cat.mp4'],check=True)
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{W}/cat.mp4']))
dt=[]; fs=S.get('fs',60); i=0
for txt,t0,t1,yy in S['texts']:
    for j,line in enumerate(txt.split('\n')):
        p=f'{W}/t{i}.txt'; open(p,'w').write(line); i+=1
        dt.append(f"drawtext=fontfile={F}:textfile={p}:fontsize={fs}:fontcolor=white:borderw=4:bordercolor=black@0.9:shadowx=0:shadowy=3:shadowcolor=black@0.5:x=(w-text_w)/2:y={yy+j*int(fs*1.3)}:enable='between(t,{t0},{t1})'")
vf=','.join(dt) or 'null'
enc=['-c:v','libx264','-profile:v','main','-crf','18','-preset','slow','-pix_fmt','yuv420p','-r','30','-map_metadata','-1','-fflags','+bitexact','-movflags','+faststart']
sil=OUT+n+'_v2_silent.mp4'; full=OUT+n+'_v2.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{W}/cat.mp4','-vf',vf,'-an']+enc+[sil],check=True)
ins=['-i',sil]; fl=[]; mix=[]; k=1
if S.get('music'):
    fo=max(dur-1.2,0); ins+=['-stream_loop','-1','-i',S['music']]
    fl.append(f"[{k}:a]atrim=0:{dur},aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.4,afade=t=out:st={fo}:d=1.2,volume={S.get('vol',0.8)}[m{k}]"); mix.append(f'[m{k}]'); k+=1
if S.get('own_audio'):  # [src,a,b] aligned to time 0
    src,a,b=S['own_audio']; ins+=['-i',src]
    fl.append(f"[{k}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=out:st={dur-0.3}:d=0.3[m{k}]"); mix.append(f'[m{k}]'); k+=1
for src,t,v in S.get('sfx',[]):
    ins+=['-i',src]; ms=int(t*1000)
    fl.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={v},adelay={ms}|{ms},apad[m{k}]"); mix.append(f'[m{k}]'); k+=1
if mix:
    fl.append(''.join(mix)+f"amix=inputs={len(mix)}:duration=first:normalize=0,atrim=0:{dur}[o]")
    subprocess.run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',';'.join(fl),'-map','0:v','-map','[o]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart','-map_metadata','-1',full],check=True)
print(n,round(dur,2))
