import sys,subprocess,numpy as np
from PIL import Image,ImageDraw
k=sys.argv[1]; v='../final/%s.mp4'%k
subprocess.run(['ffmpeg','-v','error','-y','-i',v,'-vf','fps=2,crop=1080:520:0:0,scale=270:130','/tmp/%s_top_%%02d.png'%k])
import glob
fs=sorted(glob.glob('/tmp/%s_top_*.png'%k))
c=Image.new('RGB',(270*4,135*((len(fs)+3)//4)),'white'); d=ImageDraw.Draw(c)
for i,f in enumerate(fs):
    x=(i%4)*270;y=(i//4)*135; c.paste(Image.open(f),(x,y)); d.line([(x,y+75),(x+270,y+75)],fill='red'); d.text((x+2,y+118),'%.1fs'%(i*0.5),fill='yellow')
c.save('../qc/%s_textclear.jpg'%k)
