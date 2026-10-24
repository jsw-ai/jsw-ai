# sheet.sh video out step
v=$1; o=$2; s=${3:-0.25}; d=$(mktemp -d)
ffmpeg -v error -i $v -vf "fps=1/$s,scale=216:-2" $d/f_%03d.png
python3 - $d $o $s <<'P'
import sys,glob
from PIL import Image,ImageDraw
d,o,s=sys.argv[1],sys.argv[2],float(sys.argv[3]);fs=sorted(glob.glob(d+'/f_*.png'))
ims=[Image.open(f) for f in fs];w,h=ims[0].size;c=8;r=(len(ims)+c-1)//c
S=Image.new('RGB',(w*c,h*r))
for i,im in enumerate(ims):
  ImageDraw.Draw(im).text((4,4),f"{i*s:.2f}",fill=(255,0,0));S.paste(im,((i%c)*w,(i//c)*h))
S.save(o,quality=85)
P
