import subprocess, json, sys, os
from PIL import Image, ImageDraw, ImageFont
R='/workspace/hf-test/'
refs=['keepers/gabriela_face_keeper.png','keepers/gabriela_bikini1.png','keepers/gabriela_cover.png','keepers/gabriela_refs/gabriela_ref1.png']
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
def tile(im,h=520):
    im=im.convert('RGB'); return im.resize((int(im.width*h/im.height),h))
for i in (1,2,3):
    v=f'tiktok_{i}.mp4'; g=json.load(open(f'tiktok_{i}_gate12.json')); d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',v]))
    top=[tile(Image.open(R+r)) for r in refs]; bot=[]
    for k in range(6):
        t=d*(k+0.5)/6; f=f'work/sf{i}_{k}.jpg'; subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',v,'-frames:v','1',f])
        im=tile(Image.open(f)); dr=ImageDraw.Draw(im); sc=g['scores'][min(int(t*12),len(g['scores'])-1)]
        dr.rectangle([0,0,im.width,30],fill='black'); dr.text((6,3),f'{t:.1f}s gate {sc:.2f}',font=F,fill='lime' if sc>=0.78 else 'orange'); bot.append(im)
    W=max(sum(x.width for x in top),sum(x.width for x in bot)); S=Image.new('RGB',(W,520*2+50),'white'); dr=ImageDraw.Draw(S)
    dr.text((8,12),f'tiktok_{i}  REFS (top: face_keeper, bikini1, cover, ref1)  vs frames  | gate12 min {g["min"]:.3f} median {g["median"]:.3f} pass {g["pass_frac"]*100:.0f}%  {"PASS" if g["pass_"] else "FAIL"}',font=F,fill='black')
    x=0
    for t_ in top: S.paste(t_,(x,50)); x+=t_.width
    x=0
    for t_ in bot: S.paste(t_,(x,570)); x+=t_.width
    S.save(f'review_sheet_tiktok_{i}.jpg',quality=88)
fr=[Image.open(f'work/sf{i}_1.jpg').convert('RGB').resize((540,960)) for i in (1,2,3)]
C=Image.new('RGB',(1620,1010),'white'); d=ImageDraw.Draw(C)
for k,im in enumerate(fr): C.paste(im,(k*540,50)); d.text((k*540+10,12),f'tiktok_{k+1}',font=F,fill='black')
C.save('contact_sheet.jpg',quality=88)
