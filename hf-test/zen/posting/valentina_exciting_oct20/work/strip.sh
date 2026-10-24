# strip.sh clip.mp4 out.jpg [fps]
f=${3:-2}; d=$(mktemp -d -p .)
ffmpeg -v error -i $1 -vf "fps=$f,scale=240:-2" $d/%03d.png && python3 -c "
import glob;from PIL import Image,ImageDraw
fs=sorted(glob.glob('$d/*.png'));ims=[Image.open(x) for x in fs];w,h=ims[0].size;n=len(ims);c=8
C=Image.new('RGB',(w*c,h*((n+c-1)//c)),'white');d=ImageDraw.Draw(C)
for i,im in enumerate(ims):C.paste(im,((i%c)*w,(i//c)*h));d.text(((i%c)*w+3,(i//c)*h+3),'%.1f'%(i/$f),fill='red')
C.save('$2',quality=85)"; rm -r $d
