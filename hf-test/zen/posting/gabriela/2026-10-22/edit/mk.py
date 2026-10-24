import subprocess,json,sys
from PIL import Image,ImageDraw,ImageFont
F='/usr/share/fonts/truetype/sand-box/google/Poppins/Poppins-Bold.ttf'
W='work/'; MU='/workspace/music/distrokid/gabriela/mp3/'
def txt_png(lines,out,ty=300,maxs=72):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im); s=maxs
    while True:
        f=ImageFont.truetype(F,s)
        if max(d.textlength(l,font=f) for l in lines)<=960: break
        s-=2
    lh=int(s*1.25); y0=ty-(len(lines)-1)*lh/2
    for i,l in enumerate(lines):
        d.text((540,y0+i*lh),l,font=f,fill='white',anchor='mm',stroke_width=max(3,s//14),stroke_fill='black')
    im.save(out); return s
def build(name,shots,texts,track,mstart,fg_y=420,bg='eq=brightness=-0.10',flash_at=None):
    """shots: (src,in,out,speed). texts: (t0,t1,[lines]). Output 1080x1920 30fps."""
    ins=[];fc=[];durs=[]
    for i,(s,a,b,sp) in enumerate(shots):
        d=(b-a)/sp; durs.append(d)
        ins+=['-ss',f'{a:.3f}','-t',f'{b-a:.3f}','-i',W+s]
        fc.append(f'[{i}:v]setpts=(PTS-STARTPTS)/{sp},fps=30,setsar=1,split[a{i}][b{i}];'
                  f'[a{i}]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,{bg}[bg{i}];'
                  f'[b{i}]scale=1080:-2:flags=lanczos[fg{i}];[bg{i}][fg{i}]overlay=0:{fg_y}[v{i}]')
    n=len(shots); T=sum(durs)
    fc.append(''.join(f'[v{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0[vc]')
    cur='vc'; k=n
    for j,(t0,t1,lines) in enumerate(texts):
        png=f'edit/{name}_t{j}.png'; txt_png(lines,png)
        ins+=['-loop','1','-t',f'{T:.3f}','-i',png]
        fc.append(f"[{cur}][{k}:v]overlay=0:0:enable='between(t,{t0},{t1})'[o{j}]"); cur=f'o{j}'; k+=1
    if flash_at is not None:
        fc.append(f"[{cur}]drawbox=x=0:y=0:w=iw:h=ih:color=white@0.85:t=fill:enable='between(t,{flash_at-0.034:.3f},{flash_at+0.05:.3f})'[fl]") ; cur='fl'
    fc.append(f'[{cur}]format=yuv420p[vo]')
    ins+=['-ss',f'{mstart:.3f}','-i',MU+track]
    fc.append(f'[{k}:a]atrim=duration={T:.3f},afade=t=in:d=0.1,afade=t=out:st={T-0.4:.3f}:d=0.4[ao]')
    out=f'final/gabriela_{name}.mp4'; sil=f'final/gabriela_{name}_silent.mp4'
    enc=['-t',f'{T:.3f}','-r','30','-c:v','libx264','-profile:v','main','-pix_fmt','yuv420p','-crf','20','-preset','slow','-maxrate','12M','-bufsize','24M','-movflags','+faststart','-map_metadata','-1']
    subprocess.run(['ffmpeg','-v','error','-y',*ins,'-filter_complex',';'.join(fc),'-map','[vo]','-map','[ao]',*enc,'-c:a','aac','-b:a','192k',out],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',out,'-an','-c:v','copy','-movflags','+faststart',sil],check=True)
    return dict(file=out,silent=sil,duration=round(T,2),shots=shots,texts=texts,track=track,music_start=mstart)
