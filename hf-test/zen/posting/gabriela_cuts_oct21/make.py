import subprocess,json,os
from PIL import Image,ImageDraw,ImageFont
K='/workspace/hf-test/zen/posting/gabriela_tiktok_oct19/work/v2/kl/'
F='/usr/share/fonts/truetype/sand-box/google/Poppins/Poppins-Bold.ttf'
M='music/'
C={
 'TT':dict(track='Samba_Isobel.mp3',bpm=95.7,ph=0.31,shots=[('a1_2',0.5,6),('p1_1',0.1,6)],hook='POV: Brazilian girl snack break',crop=(0,1445),y=435,ty=330,bg='eq=brightness=-0.10'),
 'IG':dict(track='Latin_Lovers_mixkit39.mp3',bpm=136.0,ph=0.14,shots=[('p1_1',1.4,8),('a1_2',0.3,8)],hook='Team pão de queijo or team açaí?',crop=(0,1380),y=480,ty=380,bg='eq=brightness=-0.04:saturation=1.15,colorbalance=rs=0.06:bs=-0.04'),
 'RD':dict(track='Modern_Jazz_Samba.mp3',bpm=172.3,ph=0.24,shots=[('a1_2',1.4,10),('p1_1',0.2,11)],hook='São Paulo comfort food, made in Miami',crop=(65,1445),y=420,ty=320,bg='eq=brightness=-0.12:saturation=0.75'),
 'X':dict(track='BossaBossa.mp3',bpm=103.4,ph=0.03,shots=[('a1_2',2.6,4),('p1_1',1.0,6),('a1_2',0.0,3)],hook='Warm cheese bread + açaí, my weakness',crop=(0,1445),y=475,ty=360,bg='eq=brightness=0.0:saturation=1.05'),
}
def hook_png(t,ty,out):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im); s=72
    while True:
        f=ImageFont.truetype(F,s); w=d.textlength(t,font=f)
        if w<=980: break
        s-=2
    d.text((540,ty),t,font=f,fill='white',anchor='mm',stroke_width=max(3,s//14),stroke_fill='black'); im.save(out); return s
res={}
for k,c in C.items():
    per=60/c['bpm']; mstart=c['ph']+round((20-c['ph'])/per)*per
    durs=[n*per for _,_,n in c['shots']]; T=sum(durs)
    png=f'work/work_hook_{k}.png'; fs=hook_png(c['hook'],c['ty'],png)
    ins=[]; fc=[]
    for i,(s,st,n) in enumerate(c['shots']):
        ins+=['-ss',f'{st:.3f}','-t',f'{durs[i]:.3f}','-i',K+s+'.mp4']
        c0,c1=c['crop']
        fc.append(f'[{i}:v]fps=30,setsar=1,trim=duration={durs[i]:.3f},setpts=PTS-STARTPTS,split[a{i}][b{i}];'
                  f'[a{i}]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,{c["bg"]}[bg{i}];'
                  f'[b{i}]scale=1080:1445:flags=lanczos,crop=1080:{c1-c0}:0:{c0}[fg{i}];[bg{i}][fg{i}]overlay=0:{c["y"]}[v{i}]')
    n=len(c['shots'])
    fc.append(''.join(f'[v{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0[vc]')
    fc.append(f'[vc][{n}:v]overlay=0:0,format=yuv420p[vo]')
    fc.append(f'[{n+1}:a]atrim=duration={T:.3f},afade=t=in:d=0.15,afade=t=out:st={T-0.4:.3f}:d=0.4[ao]')
    base=['ffmpeg','-v','error','-y',*ins,'-loop','1','-i',png,'-ss',f'{mstart:.3f}','-i',M+c['track'],'-filter_complex',';'.join(fc),'-map','[vo]']
    enc=['-t',f'{T:.3f}','-r','30','-c:v','libx264','-profile:v','main','-pix_fmt','yuv420p','-crf','20','-preset','slow','-maxrate','12M','-bufsize','24M','-movflags','+faststart','-map_metadata','-1']
    out=f'tiktok_3_v2_cut{k}.mp4'; sil=f'tiktok_3_v2_cut{k}_silent.mp4'
    subprocess.run(base+['-map','[ao]']+enc+['-c:a','aac','-b:a','192k',out],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',out,'-an','-c:v','copy','-movflags','+faststart',sil],check=True)
    res[k]=dict(file=out,silent=sil,hook=c['hook'],font_px=fs,track=c['track'],music_start_s=round(mstart,2),bpm=c['bpm'],shots=[(s,st,n,round(n*per,3)) for s,st,n in c['shots']],duration=round(T,2),reframe=dict(fg_crop_rows=c['crop'],fg_y=c['y'],bg=c['bg']))
json.dump(res,open('cuts.json','w'),indent=1,ensure_ascii=False)
