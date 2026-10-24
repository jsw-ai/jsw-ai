import json,subprocess,sys,os
FONT='/usr/share/fonts/truetype/sand-box/google/Poppins/Poppins-Bold.ttf'
W,H,FPS=720,1280,30
C='/workspace/hf-test/charlotte_1022/clips/'
def run(c): subprocess.run(c,check=True)
def seg(i,s,name):
    out=f'seg/{name}_{i}.mp4'
    if s['type']=='clip':
        vf=f"scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1"
        if s.get('speed'): vf=f"setpts=PTS/{s['speed']},"+vf
        run(['ffmpeg','-loglevel','error','-y','-ss',str(s['in']),'-to',str(s['out']),'-i',C+s['src'],'-vf',vf,'-an','-c:v','libx264','-crf','10','-preset','fast','-pix_fmt','yuv420p',out])
    elif s['type']=='freeze':
        run(['ffmpeg','-loglevel','error','-y','-ss',str(s['at']),'-i',C+s['src'],'-frames:v','1',f'seg/tmp_{name}.png'])
        run(['ffmpeg','-loglevel','error','-y','-loop','1','-t',str(s['dur']),'-i',f'seg/tmp_{name}.png','-vf',f"scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1",'-c:v','libx264','-crf','10','-preset','fast','-pix_fmt','yuv420p',out])
    elif s['type']=='flash':
        col=s.get('color','white')
        run(['ffmpeg','-loglevel','error','-y','-f','lavfi','-i',f"color=c={col}:s={W}x{H}:r={FPS}:d={s['frames']/FPS}",'-c:v','libx264','-crf','10','-pix_fmt','yuv420p',out])
    return out
def esc(t): return t.replace('\\','\\\\').replace(':','\\:').replace("'","\u2019").replace('%','\\%')
def build(cfg):
    name=cfg['name']; segs=[seg(i,s,name) for i,s in enumerate(cfg['segs'])]
    open(f'seg/list_{name}.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
    run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',f'seg/list_{name}.txt','-c','copy',f'seg/{name}_cat.mp4'])
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'seg/{name}_cat.mp4']))
    dt=[]
    for tx in cfg['texts']:
        y=tx.get('y',930); 
        for li,line in enumerate(tx['lines']):
            dt.append(f"drawtext=fontfile={FONT}:text='{esc(line)}':fontsize={tx.get('fs',46)}:fontcolor=white:borderw=4:bordercolor=black@0.85:shadowx=2:shadowy=2:shadowcolor=black@0.5:x=(w-text_w)/2:y={y+li*int(tx.get('fs',46)*1.25)}:enable='between(t,{tx['t0']},{tx['t1']})'")
    vf=','.join(['unsharp=3:3:0.3','noise=alls=3:allf=t']+dt)
    # audio: track window + sfx
    ins=['-i',f'seg/{name}_cat.mp4','-ss',str(cfg['music_start']),'-t',str(dur),'-i',f"/workspace/music/charlotte/mp3/{cfg['track']}.mp3"]
    af=f"[1:a]afade=t=in:d=0.15,afade=t=out:st={dur-0.6:.2f}:d=0.6,volume=1.0[m]"
    mix='[m]'; n=2
    for sx in cfg.get('sfx',[]):
        ins+=['-i',sx['file']]; d=int(sx['t']*1000)
        af+=f";[{n}:a]adelay={d}|{d},volume={sx.get('vol',0.8)}[s{n}]"; mix+=f'[s{n}]'; n+=1
    af+=f";{mix}amix=inputs={n-1}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]"
    out=f"/workspace/hf-test/charlotte_1022/final/{cfg['out']}"
    run(['ffmpeg','-loglevel','error','-y']+ins+['-filter_complex',f"[0:v]{vf}[v];{af}",'-map','[v]','-map','[a]','-c:v','libx264','-profile:v','main','-pix_fmt','yuv420p','-crf','14','-preset','slow','-r',str(FPS),'-c:a','aac','-b:a','160k','-ar','48000','-map_metadata','-1','-fflags','+bitexact','-movflags','+faststart','-shortest',out])
    print('built',out,round(dur,2))
for f in sys.argv[1:]: build(json.load(open(f)))
