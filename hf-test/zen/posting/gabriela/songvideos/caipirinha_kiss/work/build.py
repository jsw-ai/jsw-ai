# Caipirinha Kiss cut builder. usage: build.py <cut> ; cut in hook|x|yt
import json,subprocess,os,sys
R='/workspace/hf-test/zen/posting/gabriela/songvideos/caipirinha_kiss/'
os.chdir(R)
WAV='/workspace/music/distrokid/gabriela/05_caipirinha_kiss.wav'
FONTS='/workspace/music_video_test_2026-10-22/v3/r2/fonts'; FN='MontserratR2'
CFG=json.load(open('work/cuts.json'))
cut=sys.argv[1]; C=CFG[cut]; W,H=C['W'],C['H']; a0=C['a0']; D=C['dur']
def ts(t):t=max(0,t);return f'{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}'
T=f'work/tmp_{cut}';os.makedirs(T,exist_ok=True);lst=[];man=[];t=0
for i,s in enumerate(C['shots']):
    NF=round(s['d']*30); src='kl/'+s['n']+'.mp4'; o=f'{T}/s{i:02d}.mp4'
    vf=f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1,fps=30"
    subprocess.run(['ffmpeg','-v','error','-threads','2','-y','-ss',f"{s['ss']:.3f}",'-i',src,'-vf',vf,'-frames:v',str(NF),'-an','-c:v','libx264','-preset','medium','-crf','14','-pix_fmt','yuv420p','-r','30',o],check=True)
    lst.append(o); man.append(dict(t0=round(t,3),t1=round(t+NF/30,3),scene=s['n'],clip=os.path.abspath(src),src_in=s['ss'],src_out=round(s['ss']+NF/30,3)));t+=NF/30
open(f'{T}/list.txt','w').write(''.join(f"file '{os.path.abspath(x)}'\n" for x in lst))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{T}/list.txt','-c','copy',f'{T}/master.mp4'],check=True)
v=H>W
if v: ys=[1180,1262,1330]; szs=[64,52,48]; lsz=62; lmv=430; tagsz=34
else: ys=[700,790,860]; szs=[72,56,52]; lsz=62; lmv=110; tagsz=34
hdr=f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,{FN},{lsz},&H00FFFFFF,&H00FFFFFF,&H00181818,&H00000000,0,0,0,0,100,100,0,0,1,3,0,2,80,80,{lmv},1
Style: T,{FN},48,&H00FFFFFF,&H00FFFFFF,&H00181818,&H00000000,0,0,0,0,100,100,0,0,1,3,0,5,60,60,0,1
Style: G,{FN},{tagsz},&H00FFFFFF,&H00FFFFFF,&H00181818,&H00000000,0,0,0,0,100,100,0,0,1,2,0,3,50,50,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev=[];cx=W//2
def card(lines,a,b):
    for i,(tx,y,sz) in enumerate(zip(lines,ys,szs)):
        ev.append(f"Dialogue: 2,{ts(a+0.15*i)},{ts(b)},T,,0,0,0,,{{\\fad(300,300)\\pos({cx},{y})\\fs{sz}}}{tx}")
card(['Gabriela – Caipirinha Kiss','from the album Brisa de Miami',''],0,C['title'])
for a,b,tx in C['lyr']: ev.append(f"Dialogue: 1,{ts(a)},{ts(b)},L,,0,0,0,,{{\\fad(150,150)}}{tx}")
card(['Caipirinha Kiss','Brisa de Miami','coming soon'],C['card0'],D)
ev.append(f"Dialogue: 0,{ts(0)},{ts(C['card0'])},G,,0,0,0,,original audio by Gabriela")
assf=f'work/{cut}.ass';open(assf,'w').write(hdr+'\n'.join(ev)+'\n')
out=f"final/{C['name']}.mp4"
if os.path.exists(out): sys.exit('refusing to overwrite '+out)
fade=f"afade=t=in:d=0.05,afade=t=out:st={D-1.5:.2f}:d=1.5"
subprocess.run(['ffmpeg','-v','error','-threads','2','-y','-i',f'{T}/master.mp4','-ss',f'{a0:.3f}','-t',f'{D:.3f}','-i',WAV,'-filter_complex',
  f"[0:v]format=yuv420p,subtitles={assf}:fontsdir={FONTS}[v];[1:a]{fade}[au]",'-map','[v]','-map','[au]','-c:v','libx264','-profile:v','main','-level','4.1','-pix_fmt','yuv420p','-preset','slow','-b:v',C['br'],'-maxrate','6M','-bufsize','12M','-r','30',
  '-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart','-map_metadata','-1','-t',f'{D:.3f}',out],check=True)
json.dump(dict(file=os.path.abspath(out),W=W,H=H,duration=D,audio=WAV,audio_in=a0,audio_out=a0+D,ass=os.path.abspath(assf),shots=man),open(f"final/{C['name']}_shots.json",'w'),indent=1)
print('ok',out)
