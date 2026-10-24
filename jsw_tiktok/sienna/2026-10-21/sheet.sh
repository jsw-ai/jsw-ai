# sheet.sh clip name step
v=$1; n=$2; s=${3:-0.5}; d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $v); rm -f qc/${n}_t*.png
for t in $(python3 -c "import sys;d=float('$d');s=float('$s');print(' '.join('%.2f'%(i*s) for i in range(int(d/s)+1) if i*s<d-0.05))"); do ffmpeg -v error -y -ss $t -i $v -frames:v 1 -vf scale=270:-2 qc/${n}_t$t.png; done
python3 -c "
from PIL import Image, ImageDraw;import glob
fs=sorted(glob.glob('qc/${n}_t*.png'),key=lambda f:float(f.split('_t')[-1][:-4]))
ims=[Image.open(f) for f in fs];W=6;H=ims[0].height;R=(len(ims)+W-1)//W
c=Image.new('RGB',(270*W,H*R))
for i,im in enumerate(ims):
  d=ImageDraw.Draw(im);d.text((5,5),fs[i].split('_t')[-1][:-4],fill='yellow');c.paste(im,((i%W)*270,(i//W)*H))
c.save('qc/${n}_sheet.jpg')"
