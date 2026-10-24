import subprocess, sys, json
from PIL import Image, ImageDraw, ImageFont
FONT='/usr/share/fonts/truetype/sand-box/google/Montserrat/Montserrat-VariableFont_wght.ttf'
def text_png(lines, out):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
    f=ImageFont.truetype(FONT,80)
    try: f.set_variation_by_name('ExtraBold')
    except Exception as e: print('font var',e)
    y=230
    for ln in lines:
        w=d.textlength(ln,font=f); x=(1080-w)/2-40  # nudge left, away from right-edge buttons
        d.text((x,y),ln,font=f,fill='white',stroke_width=6,stroke_fill='black'); y+=100
    im.save(out)
def build(segs, music, mstart, lines, out):
    # segs: list of (clip, t0, dur)
    text_png(lines,'txt_'+out+'.png')
    ins=[]; fc=[]
    for i,(c,t0,du) in enumerate(segs):
        ins+=['-ss',str(t0),'-t',str(du),'-i',c]
        fc.append(f'[{i}:v]fps=30,setsar=1,trim=duration={du},setpts=PTS-STARTPTS,split[a{i}][b{i}];[a{i}]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.08[bg{i}];[b{i}]scale=1080:-2:flags=lanczos[fg{i}];[bg{i}][fg{i}]overlay=0:H-h-40[v{i}]')
    n=len(segs); T=sum(s[2] for s in segs)
    fc.append(''.join(f'[v{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0,unsharp=5:5:0.35:5:5:0,noise=alls=3:allf=t,eq=contrast=1.02:saturation=0.97[vc]')
    ins+=['-loop','1','-i','txt_'+out+'.png','-ss',str(mstart),'-t',str(T),'-i',music]
    fc.append(f'[vc][{n}:v]overlay=0:0:shortest=1,format=yuv420p[vo]')
    fc.append(f'[{n+1}:a]afade=t=in:d=0.05,afade=t=out:st={T-0.4}:d=0.4,loudnorm=I=-14:TP=-1.5[ao]')
    cmd=['ffmpeg','-v','error','-y',*ins,'-filter_complex',';'.join(fc),'-map','[vo]','-map','[ao]','-t',str(T),'-c:v','libx264','-crf','18','-preset','slow','-profile:v','high','-c:a','aac','-b:a','192k','-movflags','+faststart','-map_metadata','-1',out]
    subprocess.run(cmd,check=True); print(out,T)
