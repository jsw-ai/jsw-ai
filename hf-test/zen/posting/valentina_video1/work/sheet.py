import sys,subprocess
from PIL import Image
v,out=sys.argv[1],sys.argv[2];ts=[float(x) for x in sys.argv[3:]]
im=Image.new('RGB',(300*len(ts),533))
for i,t in enumerate(ts):
    subprocess.check_call(['ffmpeg','-y','-v','error','-ss',str(t),'-i',v,'-frames:v','1','-vf','scale=300:533','s.png']);im.paste(Image.open('s.png'),(300*i,0))
im.save(out)
