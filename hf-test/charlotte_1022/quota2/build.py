import json,subprocess,sys,os
FONT='/usr/share/fonts/truetype/sand-box/google/Poppins/Poppins-Bold.ttf'
W,H,FPS=1080,1920,30
def run(c): subprocess.run(c,check=True)
def esc(t): return t.replace('\\','\\\\').replace(':','\\:').replace("'","\u2019").replace('%','\\%')
COVER=f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1"
def build(cfg):
    name=cfg['name']; segs=[]
    for i,s in enumerate(cfg['segs']):
        out=f'seg/{name}_{i}.mp4'
        if s['type']=='clip':
            sp=s.get('speed',1.0)
            vf=f"{COVER},setpts={1/sp:.4f}*PTS,fps={FPS}"+(',reverse' if s.get('reverse') else '')+",format=yuv420p"
            run(['ffmpeg','-loglevel','error','-y','-ss',str(s['in']),'-to',str(s['out']),'-i',s['src'],'-vf',vf,'-an','-c:v','libx264','-crf','12','-preset','fast','-threads','2','-pix_fmt','yuv420p',out])
        else:
            d=s['dur'];n=int(d*FPS);z=s.get('zoom',0.06)
            vf=f"scale=2160:-2:flags=lanczos,zoompan=z='1+{z}*on/{n}':x='iw/2-(iw/zoom/2)':y='{s.get('yf',0.3)}*(ih-ih/zoom)':d={n}:s={W}x{int(W*1443/1080)}:fps={FPS},{COVER},format=yuv420p"
            run(['ffmpeg','-loglevel','error','-y','-i',s['src'],'-vf',vf,'-frames:v',str(n),'-c:v','libx264','-crf','12','-preset','fast','-threads','2','-pix_fmt','yuv420p',out])
        segs.append(out)
    open(f'seg/list_{name}.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
    run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',f'seg/list_{name}.txt','-c','copy',f'seg/{name}_cat.mp4'])
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'seg/{name}_cat.mp4']))
    dt=[]
    for tx in cfg['texts']:
        fs=tx.get('fs',52)
        for li,line in enumerate(tx['lines']):
            y=tx.get('y',1280)+li*int(fs*1.2)
            assert 1280<=y and y+fs<=1395, (line,y)
            dt.append(f"drawtext=fontfile={FONT}:text='{esc(line)}':fontsize={fs}:fontcolor=white:borderw=5:bordercolor=black@0.85:x=(w-text_w)/2:y={y}:enable='gte(t,{tx['t0']})*lt(t,{tx['t1']})'")
    vf=','.join(['noise=alls=3:allf=t']+dt+['format=yuv420p'])
    out=f"final/{cfg['out']}"
    run(['ffmpeg','-loglevel','error','-y','-i',f'seg/{name}_cat.mp4','-f','lavfi','-t',str(dur),'-i','anullsrc=r=48000:cl=stereo','-filter_complex',f"[0:v]{vf}[v]",'-map','[v]','-map','1:a','-c:v','libx264','-profile:v','main','-pix_fmt','yuv420p','-color_range','tv','-crf','18','-preset','slow','-threads','2','-r',str(FPS),'-c:a','aac','-b:a','128k','-map_metadata','-1','-fflags','+bitexact','-movflags','+faststart','-shortest',out])
    print('built',out,round(dur,2))
for f in sys.argv[1:]: build(json.load(open(f)))
