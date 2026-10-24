import subprocess,sys,json
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def build(out,segs,texts,music,moff,snap_at,xc1=0.45):
    inp=[];fc=[]
    for i,(f,a,b,sp,xc) in enumerate(segs):
        inp+=['-i',f]
        fc.append(f"[{i}:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{sp},fps=30,scale=-2:1920:flags=lanczos,crop=1080:1920:'min(max(iw*{xc}-540,0),iw-1080)':0,setsar=1[v{i}]")
    n=len(segs)
    fc.append(''.join(f'[v{i}]' for i in range(n))+f"concat=n={n}:v=1:a=0,unsharp=5:5:0.35:5:5:0,noise=c0s=3:allf=t[c0]")
    last='c0'
    for j,(t,a,b,y) in enumerate(texts):
        tf=f'{out}.tx{j}.txt';open(tf,'w').write(t)
        fc.append(f"[{last}]drawtext=fontfile={F}:textfile={tf}:fontsize=62:line_spacing=12:fontcolor=white:borderw=6:bordercolor=black@0.85:x=(w-text_w)/2:y={y}:enable='between(t,{a},{b})'[t{j}]");last=f't{j}'
    dur=round(sum((b-a)/sp for _,a,b,sp,_ in segs),3)
    inp+=['-ss',str(moff),'-i',music]
    fc.append(f"[{n}:a]atrim=0:{dur},afade=t=in:d=0.1,afade=t=out:st={dur-0.7}:d=0.7,volume=0.85[m]")
    fc.append(f"aevalsrc='0.9*exp(-t*180)*sin(2*PI*2400*t)*(random(0)*0.6+0.4)':s=48000:d=0.12,adelay={int(snap_at*1000)}:all=1,apad[s];[m][s]amix=inputs=2:duration=first:normalize=0[am]")
    cmd=['ffmpeg','-v','error','-y']+inp+['-filter_complex',';'.join(fc),'-map',f'[{last}]','-map','[am]','-c:v','libx264','-profile:v','main','-pix_fmt','yuv420p','-crf','19','-preset','slow','-maxrate','12M','-bufsize','24M','-r','30','-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart','-map_metadata','-1','-t',str(dur),out]
    subprocess.run(cmd,check=True); print(out,dur)
for c in json.load(open(sys.argv[1])): build(**c)
