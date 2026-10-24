import subprocess,sys,json
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def build(out,segs,texts,music,moff,snap_at=None,silent=False,fit=False,crf=20):
    inp=[];fc=[]
    for i,sg in enumerate(segs):
        f,a,b,z,yb=sg[:5]; xc=sg[5] if len(sg)>5 else None
        inp+=['-i',f]
        W=int(1080*z)//2*2;H=int(1920*z)//2*2
        if xc is not None:  # cover-crop: scale to fill 1920*z tall (aspect kept), crop 1080x1920 with horizontal centre at xc (0..1)
            fc.append(f"[{i}:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale=-2:{H}:flags=lanczos,crop=1080:1920:'min(max(iw*{xc}-540,0),iw-1080)':'(ih-1920)*{yb}',setsar=1[v{i}]")
        elif fit:  # aspect-preserving: clip scaled to 1080*z wide (centre-cropped to 1080 if z>1) over blurred 9:16 canvas
            fc.append(f"[{i}:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,split[bg{i}][fg{i}];[bg{i}]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.08[b{i}];[fg{i}]scale={W}:-2:flags=lanczos,crop=min(iw\\,1080):ih[f{i}];[b{i}][f{i}]overlay=(W-w)/2:(H-h)*{yb},setsar=1[v{i}]")
        else:
            fc.append(f"[{i}:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale={W}:{H}:flags=lanczos,crop=1080:1920:{(W-1080)//2}:{int((H-1920)*yb)},setsar=1[v{i}]")
    n=len(segs)
    fc.append(''.join(f'[v{i}]' for i in range(n))+f"concat=n={n}:v=1:a=0[c0]")
    last='c0'
    for j,(t,a,b) in enumerate(texts):
        open(f'/tmp/tx{j}.txt','w').write(t)
        fc.append(f"[{last}]drawtext=fontfile={F}:textfile=/tmp/tx{j}.txt:fontsize=58:line_spacing=12:fontcolor=white:borderw=5:bordercolor=black@0.85:x=(w-text_w)/2:y=70:enable='between(t,{a},{b})'[t{j}]");last=f't{j}'
    dur=sum(sg[2]-sg[1] for sg in segs)
    inp+=['-ss',str(moff),'-i',music]
    fc.append(f"[{n}:a]atrim=0:{dur},afade=t=in:d=0.15,afade=t=out:st={dur-0.7}:d=0.7,volume=0.85[m]")
    if snap_at is not None:
        fc.append(f"aevalsrc='0.9*exp(-t*180)*sin(2*PI*2400*t)*(random(0)*0.6+0.4)':s=48000:d=0.12,adelay={int(snap_at*1000)}:all=1,apad[s];[m][s]amix=inputs=2:duration=first:normalize=0[am]")
    else: fc.append("[m]anull[am]")
    cmd=['ffmpeg','-v','error','-y']+inp+['-filter_complex',';'.join(fc),'-map',f'[{last}]','-map','[am]','-c:v','libx264','-profile:v','main','-pix_fmt','yuv420p','-crf',str(crf),'-preset','slow','-maxrate','12M','-bufsize','24M','-r','30','-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart','-map_metadata','-1','-t',str(dur),out]
    subprocess.run(cmd,check=True)
    print(subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_name,profile,pix_fmt,width,height','-show_entries','format=size,duration','-of','compact',out],capture_output=True,text=True).stdout)
if __name__=='__main__':
    cfg=json.load(open(sys.argv[1]))
    for c in cfg: build(**c)
