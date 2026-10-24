import subprocess, os, textwrap
from PIL import Image, ImageDraw, ImageFont
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
W,H=1080,1920
def caption_png(text,path,y=1250,size=78):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    f=ImageFont.truetype(FONT,size)
    lines=textwrap.wrap(text,width=20)
    lh=int(size*1.25); total=lh*len(lines); yy=y-total//2
    for l in lines:
        w=d.textlength(l,font=f)
        d.text(((W-w)/2,yy),l,font=f,fill='white',stroke_width=7,stroke_fill='black'); yy+=lh
    im.save(path)
def run(cmd):
    r=subprocess.run(cmd,shell=True,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-1500:]); raise SystemExit(1)
def crop916(src,dst,cx=0.5,scale=1080):
    im=Image.open(src).convert('RGB'); w,h=im.size; cw=int(h*9/16)
    if cw>w: # too narrow: crop height instead
        ch=int(w*16/9); y=(h-ch)//2; im=im.crop((0,y,w,y+ch))
    else:
        x=int(min(max(cx*w-cw/2,0),w-cw)); im=im.crop((x,0,x+cw,h))
    im.resize((scale,int(scale*16/9)),Image.LANCZOS).save(dst,quality=95)
def segment(img,cap,dur,idx,out,work,mode,fps=30,capy=1250,capstart=0.0):
    cp=f'{work}/cap_{idx}.png'; caption_png(cap,cp,y=capy)
    if mode=='in': sc=f"1080*(1+0.14*t/{dur})"
    else: sc=f"1080*(1.14-0.14*t/{dur})"
    run(f'ffmpeg -y -loglevel error -loop 1 -framerate {fps} -t {dur} -i {img} -loop 1 -framerate {fps} -t {dur} -i {cp} -filter_complex '
        f'"[0:v]scale=w=\'trunc({sc}/2)*2\':h=-2:eval=frame:flags=bilinear,crop=1080:1920[v];'
        f'[1:v]format=rgba,fade=in:st={capstart}:d=0.2:alpha=1[c];[v][c]overlay=0:0:format=auto,format=yuv420p[o]" -map "[o]" -r {fps} -c:v libx264 -crf 17 -preset veryfast {out}')
def montage(items,bpm,music,out,work,beats_per=4,loop_dur=0.7):
    os.makedirs(work,exist_ok=True); beat=60/bpm; dur=beat*beats_per; segs=[]
    for i,(src,cap,cx) in enumerate(items):
        img=f'{work}/p{i}.jpg'; crop916(src,img,cx)
        sg=f'{work}/seg{i}.mp4'; segment(img,cap,dur,i,sg,work,'in' if i%2==0 else 'out',capstart=0.0 if i else 0.0); segs.append(sg)
    # loop tail = first image start, no caption of its own (hook caption reappears)
    tail=f'{work}/tail.mp4'
    run(f'ffmpeg -y -loglevel error -i {segs[0]} -t {loop_dur} -c:v libx264 -crf 17 {tail}')
    lst=f'{work}/list.txt'; open(lst,'w').write(''.join(f"file '{os.path.abspath(s)}'\n" for s in segs))
    body=f'{work}/body.mp4'; run(f'ffmpeg -y -loglevel error -f concat -safe 0 -i {lst} -c copy {body}')
    total=dur*len(segs); xd=0.35
    joined=f'{work}/joined.mp4'
    run(f'ffmpeg -y -loglevel error -i {body} -i {tail} -filter_complex "[0:v][1:v]xfade=transition=fade:duration={xd}:offset={total-xd}[v]" -map "[v]" -c:v libx264 -crf 17 {joined}')
    T=total-xd+loop_dur
    run(f'ffmpeg -y -loglevel error -i {joined} -i {music} -filter_complex "[1:a]atrim=0:{T},afade=t=in:d=0.3,afade=t=out:st={T-0.8}:d=0.8,volume=0.9[a]" -map 0:v -map "[a]" -t {T} -c:v libx264 -crf 23 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart -map_metadata -1 {out}')
    return T
