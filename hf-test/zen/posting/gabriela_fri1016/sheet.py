from PIL import Image, ImageDraw, ImageFont
F='gabriela_w1/final/g_%s.jpg'
P={'A':'A_r2','B':'B_r3','D':'D_r6','G':'G_n7','C':'C_r5','H':'H_n8','F':'F_n2','E':'E_n1'}
def p(k): return F%P[k]+'' if False else 'gabriela_w1/final/g_%s_v4C.jpg'%P[k]
fn=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',17)
fs=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
# (time, site, format, crop, imgs, note)
S=[('8:00a','X','text post, numbered list',None,[],'text-only post'),
('10:00a','Instagram','Story 9:16 (+poll sticker)',(9,16),['H'],'crop/sticker variant'),
('12:00p','Facebook','Reel 9:16, 15s montage',(9,16),['G','H','F','D'],'mp4 made: zoom, cuts, loop'),
('12:30p','X','post + image 4:5',(4,5),['D'],''),
('2:00p','Instagram','Story 9:16 (+poll sticker)',(9,16),['B'],'stand-in B (plan N6 not generated)'),
('4:00p','Facebook','Page album x3, 4:5',(4,5),['B','E','A'],'stand-in (plan N4 not generated)'),
('4:30p','YouTube','Short 9:16, 15s montage',(9,16),['E','A','C','B'],'mp4 made; stand-in (plan N5 not gen)'),
('6:30p','X','post + image 4:5',(4,5),['C'],''),
('7:30p','TikTok','photo-mode 6 slides, 9:16',(9,16),['F','E','H','C','A','B'],'hook on slide 1; plan N1 swapped'),
('--','Instagram','feed/Reel: SKIPPED Fri',None,[],'plan skips IG Reel/carousel Fri/Sat')]
W,H=380,640;pad=14;cols=5;head=70;lab=84
sheet=Image.new('RGB',(cols*(W+pad)+pad,head+2*(H+lab+pad)+pad),(24,24,28))
d=ImageDraw.Draw(sheet)
d.text((pad,16),'Gabriela - Fri 10/16 (ET) preview - HOLD, nothing posted',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',24),fill=(255,255,255))
d.text((pad,48),'Replies (10-15) and Reddit comments (3-5) are text-only, not shown. Crops as planned from 1080x1443 finals.',font=fs,fill=(190,190,190))
def crop(k,r):
    im=Image.open(p(k)).convert('RGB');w,h=im.size;t=r[0]/r[1]
    if w/h>t: nw=int(h*t);im=im.crop(((w-nw)//2,0,(w-nw)//2+nw,h))
    else: nh=int(w/t);im=im.crop((0,0,w,nh))
    return im
for i,(t,site,fmt,r,imgs,note) in enumerate(S):
    x=pad+(i%cols)*(W+pad);y=head+(i//cols)*(H+lab+pad)
    box=Image.new('RGB',(W,H),(48,48,54));bd=ImageDraw.Draw(box)
    if not imgs or r is None:
        msg='TEXT ONLY' if 'text' in note else 'SKIPPED'
        bd.text((W//2-60,H//2-10),msg,font=fn,fill=(200,200,200))
    else:
        n=len(imgs);sw=W//n if n>1 else W
        if n>3 or (n==3 and r==(4,5)) or n==4:
            cols_=2 if n==4 else 3;rows_=(n+cols_-1)//cols_;cw=W//cols_;ch=int(cw*r[1]/r[0]) if rows_==1 else H//rows_
            for j,k in enumerate(imgs):
                c=crop(k,r).resize((cw-2,ch-2));box.paste(c,((j%cols_)*cw,(j//cols_)*ch+((H-rows_*ch)//2 if rows_==1 else 0)))
            imgs=[]
        for j,k in enumerate(imgs):
            if k in P:
                c=crop(k,r);c=c.resize((sw,H)) if n>1 else (c.resize((W,int(W*c.height/c.width))))
                if n==1: c=c.crop((0,0,W,min(c.height,H)))
                box.paste(c,(j*sw,(H-c.height)//2 if n==1 else 0))
            else:
                bd.rectangle((j*sw,0,j*sw+sw-2,H),fill=(70,40,40))
                bd.text((j*sw+8,H//2-10),'NOT YET\nGENERATED\n(%s)'%k,font=fn,fill=(255,200,200))
    sheet.paste(box,(x,y))
    d.text((x,y+H+6),'%s ET  |  %s'%(t,site),font=fn,fill=(255,255,255))
    d.text((x,y+H+30),fmt,font=fs,fill=(220,220,220))
    d.text((x,y+H+52),note,font=fs,fill=(255,170,120) if 'not' in note or 'SKIP' in fmt else (150,200,150))
sheet.save('gabriela_fri1016_preview.jpg',quality=90)
