import os,subprocess,shutil
from PIL import Image,ImageDraw,ImageFont
FIN='/workspace/hf-test/zen/posting/madison_test/fin/'
OUT='/workspace/hf-test/zen/posting/madison_fri_oct16/'
TMP='/workspace/hf-test/zen/posting/madison_fri_oct16_build/tmp/'
os.makedirs(TMP,exist_ok=True)
FB='/usr/share/fonts/truetype/sand-box/google/Poppins/Poppins-Bold.ttf'
FS='/usr/share/fonts/truetype/sand-box/google/Poppins/Poppins-SemiBold.ttf'
# per-still horizontal focus for 9:16 crop (0=left,1=right)
FOCUS={'w1':0.35,'w2':0.45,'w3':0.5,'w4':0.5,'w5':0.45,'w6':0.5,'w7':0.5,'w9':0.5,'w10':0.5,'w12':0.4,'w13':0.4,'w14':0.45,'w15':0.5,'w16':0.5}
def load(n): return Image.open(FIN+f'{n}_v4C.jpg').convert('RGB')
def crop916(n):
    im=load(n); W,H=im.size; nw=round(H*1080/1920*1.0)  # 810 wide for 1440h
    sc=1920/H; im=im.resize((round(W*sc),1920),Image.LANCZOS)
    x=int((im.width-1080)*FOCUS.get(n,0.5)); return im.crop((x,0,x+1080,1920))
def crop45(n):
    im=load(n); W,H=im.size; return im.crop((0,10,W,10+1350))
def wrap(d,t,f,maxw):
    words=t.split(); lines=[];cur=''
    for w in words:
        c=(cur+' '+w).strip()
        if d.textlength(c,font=f)<=maxw: cur=c
        else: lines.append(cur);cur=w
    lines.append(cur);return lines
def caption_overlay(size,text,cy,fs=64):
    ov=Image.new('RGBA',size,(0,0,0,0));d=ImageDraw.Draw(ov);f=ImageFont.truetype(FB,fs)
    lines=wrap(d,text,f,size[0]*0.72);lh=int(fs*1.25);bh=lh*len(lines)+50
    bw=max(d.textlength(l,font=f) for l in lines)+80;x0=(size[0]-bw)/2;y0=cy-bh/2
    d.rounded_rectangle([x0,y0,x0+bw,y0+bh],radius=34,fill=(70,70,70,185))
    for i,l in enumerate(lines): d.text((size[0]/2,y0+25+i*lh+lh/2),l,font=f,fill='white',anchor='mm')
    return ov
def with_caption(im,text,cy,fs=64):
    im=im.convert('RGBA');im.alpha_composite(caption_overlay(im.size,text,cy,fs));return im.convert('RGB')
def poll(im,q,opts):
    im=im.convert('RGBA');ov=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(ov)
    W,H=im.size;x0,x1=70,W-70;y0=1130;y1=1450
    d.rounded_rectangle([x0,y0,x1,y1],radius=40,fill=(252,250,250,245))
    f=ImageFont.truetype(FB,50);d.text((W/2,y0+75),q,font=f,fill=(20,20,20),anchor='mm')
    f2=ImageFont.truetype(FS,46);bw=(x1-x0-90)/2
    for i,o in enumerate(opts):
        bx=x0+30+i*(bw+30);d.rounded_rectangle([bx,y0+150,bx+bw,y0+270],radius=26,fill=(235,235,240))
        d.text((bx+bw/2,y0+210),o,font=f2,fill=(20,20,20),anchor='mm')
    im.alpha_composite(ov);return im.convert('RGB')
def question(im,q,ph):
    im=im.convert('RGBA');ov=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(ov)
    W,H=im.size;x0,x1=70,W-70;y0=1170;y1=1440
    d.rounded_rectangle([x0,y0,x1,y1],radius=40,fill=(252,250,250,245))
    d.rounded_rectangle([x0,y0,x1,y0+120],radius=40,fill=(120,70,220))
    d.rectangle([x0,y0+80,x1,y0+120],fill=(120,70,220))
    d.text((W/2,y0+62),q,font=ImageFont.truetype(FB,50),fill='white',anchor='mm')
    d.rounded_rectangle([x0+40,y0+160,x1-40,y0+240],radius=24,fill=(235,235,240))
    d.text((x0+70,y0+200),ph,font=ImageFont.truetype(FS,40),fill=(130,130,140),anchor='lm')
    im.alpha_composite(ov);return im.convert('RGB')
def save(im,p): im.save(p,'JPEG',quality=90,subsampling=0,optimize=True)

def video(out,segs,fps=30):
    """segs: list of (still, seconds, caption or None, zoom_in bool)"""
    parts=[];i=0
    for n,sec,cap,zin in segs:
        base=TMP+f'b{i}.png';crop916(n).save(base)
        fr=int(sec*fps)
        Z="1+0.045*on/%d"%fr if zin else "1.045-0.045*on/%d"%fr
        inputs=['-loop','1','-i',base]
        flt=f"[0:v]scale=2160:3840,zoompan=z='{Z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps={fps}[v]"
        if cap:
            ovp=TMP+f'o{i}.png';caption_overlay((1080,1920),cap,1000).save(ovp)
            inputs+=['-i',ovp];flt+=";[v][1:v]overlay=0:0,format=yuv420p[o]"
        else: flt+=";[v]format=yuv420p[o]"
        sp=TMP+f's{i}.mp4'
        subprocess.check_call(['ffmpeg','-y','-loglevel','error']+inputs+['-filter_complex',flt,'-map','[o]','-frames:v',str(fr),'-c:v','libx264','-crf','19','-preset','medium','-pix_fmt','yuv420p','-r',str(fps),sp])
        parts.append(sp);i+=1
    lst=TMP+'list.txt';open(lst,'w').write(''.join(f"file '{p}'\n" for p in parts))
    subprocess.check_call(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',lst,'-c','copy','-map_metadata','-1','-an',out])

# ---------- clean old files
for sub in ['instagram','tiktok','x','youtube_HELD','facebook_HELD']:
    for f in os.listdir(OUT+sub): os.remove(OUT+sub+'/'+f)
# ---------- X
save(crop45('w12'),OUT+'x/x_post2_w12_108pm.jpg')
save(crop45('w1'),OUT+'x/x_post3_w1_511pm.jpg')
# ---------- IG carousel (4:5)
save(with_caption(crop45('w1'),'a week of movement, coffee & matcha mornings',800,60),OUT+'instagram/ig_carousel_1_w1_744pm.jpg')
save(crop45('w12'),OUT+'instagram/ig_carousel_2_w12_744pm.jpg')
save(crop45('w5'),OUT+'instagram/ig_carousel_3_w5_744pm.jpg')
save(crop45('w14'),OUT+'instagram/ig_carousel_4_w14_744pm.jpg')
# ---------- Stories
save(poll(crop916('w6'),'gym or pilates?',['gym','pilates']),OUT+'instagram/ig_story1_w6_914am_poll.jpg')
save(question(crop916('w3'),'post-workout order? go','type something...'),OUT+'instagram/ig_story2_w3_252pm_question.jpg')
save(poll(crop916('w2'),'iced or hot after class?',['iced','hot']),OUT+'instagram/ig_story3_w2_847pm_poll.jpg')
# ---------- TikTok slides
tt=[('w1','pilates girl era: my 7am routine and everything after class'),('w14','2. coffee refill, non-negotiable'),('w15','3. brunch is the reward'),('w10','4. boots on for errands'),('w4','5. park reset before the leaves are gone'),('w7','6. couch time, no notes'),('w12','7. repeat tomorrow, 7am')]
for i,(n,c) in enumerate(tt,1): save(with_caption(crop916(n),c,1000),OUT+f'tiktok/tt_slide{i}_{n}.jpg')
video(OUT+'tiktok/tt_slideshow_preview.mp4',[(n,1.7 if i else 1.9,c,i%2==0) for i,(n,c) in enumerate(tt)][:7])
# ---------- IG Reel 13s
reel=[('w1',2.5,'pilates 4x a week and I\'m still the loudest one in the studio',True),('w12',2,'home pilates on rest days too',False),('w14',2,'coffee refill, the real reward',True),('w15',2,'brunch is earned, avocado toast optional',False),('w10',1.5,'boots on, errands done',True),('w4',1.5,'park reset before the leaves are gone',False),('w1',1.5,'see you at 7 tomorrow',True)]
video(OUT+'instagram/ig_reel_pilates_1148am.mp4',reel)
# ---------- YT 18s (loops)
yt=[('w12',3,'a pilates day in nyc: what I do after class, start to finish',True),('w14',3,'coffee first, always',False),('w15',3,'brunch stop',True),('w10',3,'errands in boots',False),('w7',3,'couch reset',True),('w12',3,None,False)]
video(OUT+'youtube_HELD/yt_short_224pm.mp4',yt)
# ---------- FB reel 10s + post
fb=[('w1',3,'morning reset before the city wakes up',True),('w16',2.5,'slow walks, slower plans',False),('w13',2.5,'bench time counts as cardio',True),('w1',2,'back at it tomorrow',False)]
video(OUT+'facebook_HELD/fb_reel_1005am.mp4',fb)
save(crop45('w5'),OUT+'facebook_HELD/fb_post_w5_625pm.jpg')
# ---------- preview = IG reel + TikTok slideshow
lst=TMP+'pl.txt';open(lst,'w').write(f"file '{OUT}instagram/ig_reel_pilates_1148am.mp4'\nfile '{OUT}tiktok/tt_slideshow_preview.mp4'\n")
subprocess.check_call(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',lst,'-c','copy','-map_metadata','-1',OUT+'preview.mp4'])
print('built')
