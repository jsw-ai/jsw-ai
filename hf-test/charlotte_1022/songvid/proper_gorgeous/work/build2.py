import json,subprocess,os,sys
os.chdir('/workspace/hf-test/charlotte_1022/songvid/proper_gorgeous/work')
WAV='/workspace/music/distrokid/charlotte/02_proper_gorgeous.wav'; FONTS=os.path.abspath('fonts')
FN=sys.argv[4] if len(sys.argv)>4 else 'MontserratR2'
name=sys.argv[1]; dur=float(sys.argv[2]); shots=sys.argv[3].split(',')
A0=118.5; W,H=1080,1920; sd=dur/len(shots)
def ts(t):return f'{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}'
T=f'tmp2_{name}';os.makedirs(T,exist_ok=True);lst=[];man=[];t=0
for i,n in enumerate(shots):
    NF=round(sd*30); o=f'{T}/s{i:02d}.mp4'; mo='in' if i%2==0 else 'out'
    ze=f"1+0.08*on/{NF}" if mo=='in' else f"1.08-0.08*on/{NF}"
    vf=f"crop='ih*9/16':ih:(iw-ow)/2:0,scale=2160:3840:flags=lanczos,zoompan=z='{ze}':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.3':d=1:s=1080x1920:fps=30,setsar=1,format=yuv420p"
    subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',f'stills/{n}.jpg','-vf',vf,'-frames:v',str(NF),'-an','-c:v','libx264','-preset','medium','-crf','14','-pix_fmt','yuv420p','-threads','2',o],check=True)
    lst.append(o); man.append(dict(t0=round(t,3),t1=round(t+NF/30,3),still=os.path.abspath(f'stills/{n}.jpg'),motion=f'Ken Burns zoom {mo} 1.00-1.08, hard cut'))
    t+=NF/30
open(f'{T}/list.txt','w').write(''.join(f"file '{os.path.abspath(x)}'\n" for x in lst))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{T}/list.txt','-c','copy',f'{T}/master.mp4'],check=True)
# lower third: bottom edge at y=1395 (MarginV=525), 2-line max ~110px -> top >=1280
hdr=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,{FN},54,&H00FFFFFF,&H00FFFFFF,&H00181818,&H78000000,1,0,0,0,100,100,0,0,1,3,2,2,60,60,525,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev=[f"Dialogue: 1,{ts(0.2)},{ts(5.0)},L,,0,0,0,,{{\\fad(250,300)}}Charlotte Hayes\\NProper Gorgeous",
    f"Dialogue: 1,{ts(dur-4.5)},{ts(dur)},L,,0,0,0,,{{\\fad(300,0)}}Proper Gorgeous\\Nout now on Apple Music"]
assf=f'{name}.ass'; open(assf,'w').write(hdr+'\n'.join(ev)+'\n')
out=f'../final/{name}.mp4'
if os.path.exists(out): sys.exit('refusing to overwrite '+out)
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{T}/master.mp4','-ss',str(A0),'-t',str(dur),'-i',WAV,'-filter_complex',
  f"[0:v]subtitles={assf}:fontsdir={FONTS},format=yuv420p[v];[1:a]afade=t=in:d=0.05,afade=t=out:st={dur-1.5}:d=1.5[a]",'-threads','2',
  '-map','[v]','-map','[a]','-c:v','libx264','-profile:v','main','-level','4.1','-pix_fmt','yuv420p','-color_range','tv','-preset','slow','-b:v','3800k','-maxrate','4500k','-bufsize','8M','-r','30',
  '-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart','-map_metadata','-1','-t',str(dur),out],check=True)
json.dump(dict(file=os.path.abspath(out),song='Charlotte Hayes - Proper Gorgeous',audio=WAV,audio_start=A0,duration=dur,size='1080x1920',ass=os.path.abspath(assf),text_zone='y 1280-1395 only',process='Approved v4C stills (finish_v4C, identity gate >=0.78), Ken Burns only; no new generation, no Seedance, no lip-sync',shots=man),open(f'../final/{name}_manifest.json','w'),indent=1)
print('ok',out)
