import subprocess,sys
from PIL import Image,ImageDraw,ImageFont
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26)
def fr(f,t):
    subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(t),'-i',f,'-frames:v','1','/tmp/f.png']);return Image.open('/tmp/f.png').convert('RGB')
def sheet(c,orig,new,out,ts=(2.0,3.5,6.0)):
    rows=[]
    for t in ts:
        a,b=fr(orig,t),fr(new,t);w,h=a.size
        a=a.crop((int(w*.1),int(h*.03),int(w*.9),int(h*.45)));b=b.crop((int(w*.1),int(h*.03),int(w*.9),int(h*.45)))
        for im,l in ((a,'ORIGINAL %.1fs'%t),(b,'SOFTENED %.1fs'%t)):
            d=ImageDraw.Draw(im);d.rectangle((0,0,im.width,36),fill=(0,0,0));d.text((6,4),l,font=F,fill=(255,255,255))
        r=Image.new('RGB',(a.width*2,a.height));r.paste(a,(0,0));r.paste(b,(a.width,0));rows.append(r)
    s=Image.new('RGB',(rows[0].width,sum(r.height for r in rows)));y=0
    for r in rows:s.paste(r,(0,y));y+=r.height
    s.thumbnail((1800,2400));s.save(out)
c=sys.argv[1];sheet(c,f'../../{c}.mp4',f'{c}_softened.mp4',f'cmp_{c}.jpg')
