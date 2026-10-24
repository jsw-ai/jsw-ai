import subprocess,sys,json
from PIL import ImageFont
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def fs(t):
    s=56
    while ImageFont.truetype(F,s).getbbox(t)[2]>1000: s-=2
    return s
def build(out,shots,texts,music=None,moff=0,keep_audio=False):
    inp=[];fc=[]
    for i,(c,a,b) in enumerate(shots):
        inp+=['-ss',str(a),'-t',str(round(b-a,3)),'-i',c]
        fc.append(f"[{i}:v]fps=30,setpts=PTS-STARTPTS,split[a{i}][b{i}];[a{i}]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.08[bg{i}];[b{i}]scale=1080:-2:flags=lanczos[fg{i}];[bg{i}][fg{i}]overlay=(W-w)/2:(H-h)/2,setsar=1[v{i}]")
    n=len(shots); dur=sum(b-a for _,a,b in shots)
    fc.append(''.join(f'[v{i}]' for i in range(n))+f"concat=n={n}:v=1:a=0,unsharp=5:5:0.25,noise=alls=3:allf=t[c0]")
    last='c0'
    for j,(t,a,b) in enumerate(texts):
        open(f'txt_{j}.txt','w').write(t)
        fc.append(f"[{last}]drawtext=fontfile={F}:textfile=txt_{j}.txt:fontsize={fs(t)}:fontcolor=white:borderw=5:bordercolor=black@0.85:x=(w-text_w)/2:y=100:enable='between(t,{a},{b})'[t{j}]"); last=f't{j}'
    amap=[]
    if music:
        inp+=['-ss',str(moff),'-t',str(dur),'-i',music]
        fc.append(f"[{n}:a]afade=t=in:d=0.15,afade=t=out:st={dur-0.6}:d=0.6,volume=0.9[am]"); amap=['-map','[am]']
    elif keep_audio: amap=['-map','0:a']
    cmd=['ffmpeg','-v','error','-y']+inp+['-filter_complex',';'.join(fc),'-map',f'[{last}]']+amap+['-c:v','libx264','-crf','19','-preset','slow','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','160k','-map_metadata','-1','-fflags','+bitexact','-flags:v','+bitexact','-flags:a','+bitexact','-movflags','+faststart','-t',str(dur),out]
    subprocess.check_call(cmd)
