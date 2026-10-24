import json,subprocess,sys,os
src=open('v4/build4.py').read().split('def build')[0]; exec(src)
def r(c): print(' '.join(c)[:150],flush=True); subprocess.run(['bash','gw.sh']+c,check=True,timeout=1500)
for f in sys.argv[1:]:
    cfg=json.load(open(f)); n=cfg['name']; cat=cfg.get('cat',f'seg/{n}_cat.mp4'); out='final/'+cfg['out']
    if os.path.exists(out): continue
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',cat]))
    if 'vf' in cfg: vf=cfg['vf']
    else:
        dt=[]
        for tx in cfg['texts']:
            fs=tx.get('fs',68)
            for li,line in enumerate(tx['lines']):
                dt.append(f"drawtext=fontfile='{tx.get('font',FONT)}':text='{esc(line)}':fontsize={fs}:fontcolor=white:borderw={tx.get('bw',5)}:bordercolor=black@0.85:shadowx=2:shadowy=2:shadowcolor=black@0.5:x=(w-text_w)/2:y={tx['y']+li*int(fs*1.25)}:enable='between(t,{tx['t0']},{tx['t1']})'")
        vf=','.join(['unsharp=3:3:0.3','noise=alls=3:allf=t']+dt)
    v=f'v5/{n}_v.mp4'; a=f'v5/{n}_a.m4a'
    r(['ffmpeg','-nostdin','-loglevel','error','-y','-i',cat,'-vf',vf,'-an','-threads','2','-c:v','libx264','-profile:v','main','-pix_fmt','yuv420p','-crf','18','-preset','medium','-r','30',v])
    if cfg.get('track'):
        r(['ffmpeg','-nostdin','-loglevel','error','-y','-ss',str(cfg['music_start']),'-t',f'{dur:.3f}','-i',f"/workspace/music/charlotte/mp3/{cfg['track']}.mp3",'-af',f"afade=t=in:d=0.15,afade=t=out:st={dur-0.6:.2f}:d=0.6,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000",'-c:a','aac','-b:a','128k',a])
    else:
        r(['ffmpeg','-nostdin','-loglevel','error','-y','-f','lavfi','-t',f'{dur:.3f}','-i','anullsrc=r=48000:cl=stereo','-c:a','aac','-b:a','128k',a])
    r(['ffmpeg','-nostdin','-loglevel','error','-y','-i',v,'-i',a,'-map','0:v','-map','1:a','-c','copy','-map_metadata','-1','-movflags','+faststart','-shortest',out])
    open('progress.md','a').write(f'- encoded {out}\n'); print('done',out,flush=True)
