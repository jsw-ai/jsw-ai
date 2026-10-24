# export.py spec.json -> final/<name>.mp4 (music or own audio) + final/<name>_silent.mp4
import json,sys,subprocess,os
S=json.load(open(sys.argv[1])); n=S['name']; W='work/x_'+n; os.makedirs(W,exist_ok=True)
F='/usr/share/fonts/truetype/sand-box/google/Poppins/Poppins-SemiBold.ttf'
if not os.path.exists(F): F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
parts=[]
for k,(src,a,b) in enumerate(S['segs']):
    o=f'{W}/s{k}.mp4'; parts.append(o)
    y=S.get('clip_y','(H-h)/2')
    vf=(f"[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.08[bg];"
        f"[b]scale=1080:-2:flags=lanczos,unsharp=5:5:0.3[fg];[bg][fg]overlay=(W-w)/2:{y},noise=alls=3:allf=t,fps=30,format=yuv420p")
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i',src,'-filter_complex',vf,'-an','-c:v','libx264','-crf','16','-preset','fast',o],check=True)
open(f'{W}/l.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{W}/l.txt','-c','copy',f'{W}/cat.mp4'],check=True)
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{W}/cat.mp4']))
dt=[]
for i,(txt,t0,t1,yy) in enumerate(S['texts']):
    open(f'{W}/t{i}.txt','w').write(txt)
    dt.append(f"drawtext=fontfile={F}:textfile={W}/t{i}.txt:fontsize={S.get('fs',58)}:fontcolor=white:borderw=5:bordercolor=black@0.85:line_spacing=12:x=(w-text_w)/2:y={yy}:enable='between(t,{t0},{t1})'")
vf=','.join(dt) or 'null'
enc=['-c:v','libx264','-crf','19','-preset','slow','-pix_fmt','yuv420p','-r','30','-map_metadata','-1','-fflags','+bitexact','-movflags','+faststart']
os.makedirs('final',exist_ok=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{W}/cat.mp4','-vf',vf,'-an']+enc+[f'final/{n}_silent.mp4'],check=True)
if S.get('music'):
    fo=max(dur-1.2,0)
    af=f"[1:a]atrim=0:{dur},afade=t=in:d=0.4,afade=t=out:st={fo}:d=1.2,volume={S.get('vol',0.8)}[m]"
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'final/{n}_silent.mp4','-stream_loop','-1','-i',S['music'],'-filter_complex',af,'-map','0:v','-map','[m]','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',f'final/{n}.mp4'],check=True)
elif S.get('audio'):  # list of [src,a,b] audio pieces aligned with segs (None = silence)
    ins=[];fl=[]
    for k,(src,a,b) in enumerate(S['segs']):
        ins+=['-i',src]; d=b-a
        if S['audio'][k]: fl.append(f"[{k+1}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[a{k}]")
        else: fl.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{d}[a{k}]")
    fl.append(''.join(f'[a{k}]' for k in range(len(S['segs'])))+f"concat=n={len(S['segs'])}:v=0:a=1,afade=t=out:st={dur-0.3}:d=0.3[o]")
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'final/{n}_silent.mp4']+ins+['-filter_complex',';'.join(fl),'-map','0:v','-map','[o]','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',f'final/{n}.mp4'],check=True)
print(n,round(dur,2))
