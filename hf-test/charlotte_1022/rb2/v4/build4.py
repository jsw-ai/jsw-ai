import json,subprocess,sys,os
FONT='/usr/share/fonts/truetype/sand-box/google/Poppins/Poppins-Bold.ttf'
W,H,FPS=1080,1920,30
def run(c): subprocess.run(c,check=True)
def esc(t): return t.replace('\\','\\\\').replace(':','\\:').replace("'","\u2019").replace('%','\\%')
def build(cfg):
    name=cfg['name']; segs=[]
    for i,s in enumerate(cfg['segs']):
        out=f'seg/{name}_{i}.mp4'
        cx=s.get('crop')  # [w,h,x,y] in source px, must be 9:16
        vf=(f"crop={cx[0]}:{cx[1]}:{cx[2]}:{cx[3]}," if cx else f"scale={W}:{H}:force_original_aspect_ratio=increase,")+f"scale={W}:{H}:flags=lanczos,crop={W}:{H},fps={FPS},setsar=1"
        run(['ffmpeg','-loglevel','error','-y','-ss',str(s['in']),'-to',str(s['out']),'-i',s['src'],'-vf',vf,'-an','-c:v','libx264','-threads','2','-crf','10','-preset','fast','-pix_fmt','yuv420p',out]); segs.append(out)
    open(f'seg/list_{name}.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
    run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',f'seg/list_{name}.txt','-c','copy',f'seg/{name}_cat.mp4'])
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'seg/{name}_cat.mp4']))
    dt=[]
    for tx in cfg['texts']:
        fs=tx.get('fs',68)
        for li,line in enumerate(tx['lines']):
            dt.append(f"drawtext=fontfile={tx.get('font',FONT)}:text='{esc(line)}':fontsize={fs}:fontcolor={tx.get('color','white')}:borderw={tx.get('bw',5)}:bordercolor=black@0.85:shadowx=2:shadowy=2:shadowcolor=black@0.5:x=(w-text_w)/2:y={tx['y']+li*int(fs*1.25)}:enable='between(t,{tx['t0']},{tx['t1']})'")
    vf=','.join(['unsharp=3:3:0.3','noise=alls=3:allf=t']+dt)
    out=f"final/{cfg['out']}"
    if cfg.get('track'):
        ins=['-i',f'seg/{name}_cat.mp4','-ss',str(cfg['music_start']),'-t',str(dur),'-i',f"/workspace/music/charlotte/mp3/{cfg['track']}.mp3"]
        af=f"[1:a]afade=t=in:d=0.15,afade=t=out:st={dur-0.6:.2f}:d=0.6,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]"
    else:
        ins=['-i',f'seg/{name}_cat.mp4','-f','lavfi','-t',str(dur),'-i','anullsrc=r=48000:cl=stereo']; af='[1:a]anull[a]'
    run(['ffmpeg','-nostdin','-loglevel','error','-y','-filter_complex_threads','1']+ins+['-filter_complex',f"[0:v]{vf}[v];{af}",'-map','[v]','-map','[a]','-threads','2','-c:v','libx264','-profile:v','main','-pix_fmt','yuv420p','-crf','18','-preset','slow','-r',str(FPS),'-c:a','aac','-b:a','128k','-ar','48000','-map_metadata','-1','-fflags','+bitexact','-movflags','+faststart','-shortest',out])
    print('built',out,round(dur,3))
for f in sys.argv[1:]: build(json.load(open(f)))
