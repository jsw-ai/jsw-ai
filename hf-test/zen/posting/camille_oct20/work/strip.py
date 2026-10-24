import sys,subprocess
from PIL import Image
f=sys.argv[1]; o=sys.argv[2]; d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
ts=[round(d*k/11,2)+0.05 for k in range(12)]; ims=[]
for t in ts:
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',f,'-frames:v','1','/workspace/hf-test/zen/posting/camille_oct20/work/_s.png']); ims.append(Image.open('/workspace/hf-test/zen/posting/camille_oct20/work/_s.png').convert('RGB').resize((270,480)))
s=Image.new('RGB',(270*6,960))
for i,im in enumerate(ims): s.paste(im,((i%6)*270,(i//6)*480))
s.save(o,quality=85)
