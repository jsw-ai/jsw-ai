# usage: build3.py cfg.json   cfg: {name,dur,a0,shots:[{clip,still,job,in,out,sp}]}
import json,subprocess,os,sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
WAV='/workspace/music/distrokid/charlotte/02_proper_gorgeous.wav'; FONTS=os.path.abspath('../work/fonts')
cfg=json.load(open(sys.argv[1])); name=cfg['name']; dur=cfg['dur']; A0=cfg.get('a0',118.5)
def r(c,to=900): print(' '.join(c)[:140],flush=True); subprocess.run(['bash','gw.sh']+c,check=True,timeout=to)
def ts(t):return f'{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}'
T=f'seg/{name}'; os.makedirs(T,exist_ok=True); lst=[]; man=[]; t=0
for i,s in enumerate(cfg['shots']):
    sp=s.get('sp',1.0); L=(s['out']-s['in'])/sp; NF=round(L*30); o=f'{T}/s{i:02d}.mp4'
    vf=f"trim={s['in']}:{s['out']},setpts=(PTS-STARTPTS)/{sp},fps=30,scale=-2:1920:flags=lanczos,crop=1080:1920,setsar=1,scale=out_range=tv,format=yuv420p"
    if not os.path.exists(o):
        r(['ffmpeg','-nostdin','-v','error','-y','-i',s['clip'],'-vf',vf,'-frames:v',str(NF),'-an','-c:v','libx264','-preset','veryfast','-crf','12','-threads','2',o],300)
    man.append(dict(t0=round(t,3),t1=round(t+NF/30,3),clip=os.path.abspath(s['clip']),kling_job=s['job'],clip_window_s=[s['in'],s['out']],speed=sp,source_still=s['still'],motion='Kling 3.0 std + Element 8f87f513, 5 s, sound off, hard cut'))
    lst.append(o); t+=NF/30
open(f'{T}/list.txt','w').write(''.join(f"file '{os.path.abspath(x)}'\n" for x in lst))
hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,MontserratR2,46,&H00FFFFFF,&H00FFFFFF,&H00181818,&H78000000,1,0,0,0,100,100,0,0,1,3,2,2,60,60,525,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev=[f"Dialogue: 1,{ts(0.2)},{ts(4.5)},L,,0,0,0,,{{\\fad(250,300)}}Charlotte Hayes\\NProper Gorgeous",
    f"Dialogue: 1,{ts(dur-4.0)},{ts(dur)},L,,0,0,0,,{{\\fad(300,0)}}{cfg.get('end','Proper Gorgeous · out now')}"]
assf=f'{T}/{name}.ass'; open(assf,'w').write(hdr+'\n'.join(ev)+'\n')
out=f'final/{name}.mp4'; v=f'{T}/v.mp4'; a=f'{T}/a.m4a'
r(['ffmpeg','-nostdin','-v','error','-y','-f','concat','-safe','0','-i',f'{T}/list.txt','-vf',f"subtitles={assf}:fontsdir={FONTS},format=yuv420p",'-an','-threads','2','-c:v','libx264','-profile:v','main','-level','4.1','-pix_fmt','yuv420p','-color_range','tv','-preset','medium','-crf','16','-maxrate','9M','-bufsize','16M','-r','30','-t',str(dur),v],1500)
r(['ffmpeg','-nostdin','-v','error','-y','-ss',str(A0),'-t',str(dur),'-i',WAV,'-af',f"afade=t=in:d=0.05,afade=t=out:st={dur-1.5}:d=1.5",'-c:a','aac','-b:a','160k','-ar','48000',a])
r(['ffmpeg','-nostdin','-v','error','-y','-i',v,'-i',a,'-map','0:v','-map','1:a','-c','copy','-map_metadata','-1','-movflags','+faststart','-shortest',out])
json.dump(dict(file=os.path.abspath(out),song='Charlotte Hayes - Proper Gorgeous (album Proper Gorgeous)',audio=WAV,audio_start=A0,duration=dur,size='1080x1920',codec='H.264 Main, yuv420p, +faststart, 30 fps',ass=os.path.abspath(assf),text='title card + end card only, y 1280-1395, no lyrics burned in',process='Approved v4C stills -> Kling 3.0 std + Element (simple motion). No Seedance, no lip-sync, no still push-ins. Full-frame cover crop, hard cuts.',shots=man),open(f'final/{name}_manifest.json','w'),indent=1)
open('../../progress.md','a').write(f'- built v2/{out}\n'); print('ok',out)
