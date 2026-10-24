import subprocess
from PIL import Image, ImageDraw, ImageFont
FONT='/usr/share/fonts/truetype/sand-box/google/Montserrat/Montserrat-VariableFont_wght.ttf'
TEXT='Landed in SP. Mom lit the grill.'
b=60/129.199
segs=[('kl/A_2.mp4',1.30,8*b),('kl/C_2.mp4',0.0,5*b),('kl/D_1.mp4',0.0,6*b)]
MUSIC='music/SambaIsobel.mp3'; MSTART=77.601
im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
size=64
while True:
    f=ImageFont.truetype(FONT,size)
    try: f.set_variation_by_name('ExtraBold')
    except Exception: pass
    w=d.textlength(TEXT,font=f)
    if w<=960: break
    size-=2
d.text(((1080-w)/2-30,250),TEXT,font=f,fill='white',stroke_width=5,stroke_fill='black'); im.save('txt.png'); print('font',size,'w',w)
ins=[];fc=[]
for i,(c,t0,du) in enumerate(segs):
    ins+=['-ss',f'{t0:.3f}','-t',f'{du+0.1:.3f}','-i',c]
    fc.append(f'[{i}:v]fps=30,setsar=1,trim=duration={du:.4f},setpts=PTS-STARTPTS,split[a{i}][b{i}];[a{i}]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.08[bg{i}];[b{i}]scale=1080:-2:flags=lanczos[fg{i}];[bg{i}][fg{i}]overlay=0:H-h-40[v{i}]')
n=len(segs);T=sum(s[2] for s in segs)
fc.append(''.join(f'[v{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0,unsharp=5:5:0.3:5:5:0,noise=alls=3:allf=t[vc]')
ins+=['-loop','1','-i','txt.png','-ss',str(MSTART),'-t',f'{T:.3f}','-i',MUSIC]
fc.append(f'[vc][{n}:v]overlay=0:0:shortest=1,format=yuv420p[vo]')
fc.append(f'[{n+1}:a]afade=t=in:d=0.03,afade=t=out:st={T-0.4:.3f}:d=0.4,loudnorm=I=-14:TP=-1.5[ao]')
out='../../tiktok_1_v3.mp4'
enc=['-c:v','libx264','-profile:v','main','-pix_fmt','yuv420p','-crf','20','-preset','slow','-maxrate','10M','-bufsize','20M','-r','30']
subprocess.run(['ffmpeg','-v','error','-y',*ins,'-filter_complex',';'.join(fc),'-map','[vo]','-map','[ao]','-t',f'{T:.3f}',*enc,'-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart','-map_metadata','-1',out],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',out,'-map','0:v','-c:v','copy','-an','-map_metadata','-1','-movflags','+faststart','../../tiktok_1_v3_silent.mp4'],check=True)
print('T',T)
