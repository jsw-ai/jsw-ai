from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
B='/workspace/hf-test/zen/posting/'; O=B+'gabriela_setup_oct21/youtube_v3/'
G='/usr/share/fonts/truetype/sand-box/google/'
# Avatar from 02_acai (face bbox 437,192,685,555)
im=Image.open(B+'gabriela_carousel_oct18/final/02_acai.jpg').convert('RGB')
cx,cy=(437+685)/2,(192+555)/2; s=round(363/0.55)
av=im.crop((round(cx-s/2),round(cy-s/2),round(cx+s/2),round(cy+s/2))).resize((800,800),Image.LANCZOS)
av.save(O+'gabriela_yt_avatar_800.png')
p=av.copy(); d=ImageDraw.Draw(p); d.ellipse((0,0,799,799),outline='red',width=4)
d.line((400,0,400,800),fill=(255,0,0),width=1); d.line((0,400,800,400),fill=(255,0,0),width=1)
p.save(O+'preview_avatar_circle.jpg',quality=92)
# Banner
bg=Image.open(B+'gabriela_setup_oct21/banners_v2/pexels_28625882.jpg').convert('RGB')
bg=bg.resize((2048,1365),Image.LANCZOS).crop((0,120,2048,1272))
bg=ImageEnhance.Brightness(bg).enhance(0.92)
# dark gradient band behind safe area for text legibility
ov=Image.new('L',(2048,1152),0); od=ImageDraw.Draw(ov)
for y in range(1152):
    a=max(0,1-abs(y-576)/330); od.line((0,y,2048,y),fill=int(120*a))
bg=Image.composite(Image.new('RGB',bg.size,(10,20,35)),bg,ov)
# photo card from 04_miami_walk (face 429,162,612,435)
src=Image.open(B+'gabriela_carousel_oct18/final/04_miami_walk.jpg').convert('RGB')
cw,ch=300,318; fx,fy=(429+612)/2,(162+435)/2
sh=560; sw=sh*cw/ch
card=src.crop((round(fx-sw/2),round(fy-sh*0.42),round(fx+sw/2),round(fy+sh*0.58))).resize((cw,ch),Image.LANCZOS)
X,Y=1315,417
m=Image.new('L',(cw,ch),0); ImageDraw.Draw(m).rounded_rectangle((0,0,cw-1,ch-1),24,fill=255)
shadow=Image.new('L',(2048,1152),0); ImageDraw.Draw(shadow).rounded_rectangle((X+6,Y+10,X+cw+6,Y+ch+10),26,fill=140)
shadow=shadow.filter(ImageFilter.GaussianBlur(12)); bg=Image.composite(Image.new('RGB',bg.size,(0,0,0)),bg,shadow)
d=ImageDraw.Draw(bg); d.rounded_rectangle((X-5,Y-5,X+cw+4,Y+ch+4),28,fill=(250,246,238))
bg.paste(card,(X,Y),m)
f1=ImageFont.truetype(G+'DM Serif Display/DMSerifDisplay-Regular.ttf',106)
f2=ImageFont.truetype(G+'Poppins/Poppins-Medium.ttf',40)
tx=455
d.text((tx,470),'Gabriela Santos',font=f1,fill='white',stroke_width=2,stroke_fill=(0,0,0,0))
d.text((tx+6,640),'Miami  •  Brasil',font=f2,fill=(255,236,200))
print(d.textbbox((tx,470),'Gabriela Santos',font=f1),d.textbbox((tx+6,640),'Miami  •  Brasil',font=f2))
bg.save(O+'gabriela_yt_banner_2048x1152.png')
p=bg.copy(); ImageDraw.Draw(p).rectangle((406,407,1641,745),outline='red',width=4)
p.save(O+'preview_banner_safe_area.jpg',quality=92)
