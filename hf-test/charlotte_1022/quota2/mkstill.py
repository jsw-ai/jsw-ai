import sys
from PIL import Image,ImageDraw,ImageFont
F='/usr/share/fonts/truetype/sand-box/google/Poppins/Poppins-Bold.ttf'
def story(src,out,lines,fs=62,y0=1280):
    a=Image.open(src).convert('RGB'); w,h=a.size; s=1920/h; a=a.resize((round(w*s),1920),Image.LANCZOS)
    x=(a.width-1080)//2; a=a.crop((x,0,x+1080,1920))
    d=ImageDraw.Draw(a); f=ImageFont.truetype(F,fs)
    for i,l in enumerate(lines):
        tw=d.textlength(l,font=f); d.text(((1080-tw)/2,y0+i*int(fs*1.3)),l,font=f,fill='white',stroke_width=5,stroke_fill='black')
    a.save(out,'JPEG',quality=92,subsampling=0)
