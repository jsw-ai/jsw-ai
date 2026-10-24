import subprocess,textwrap,sys,numpy as np,wave
sys.path.insert(0,'/workspace/hf-test/zen/posting/valentina_video1/work')
import importlib.util
src=open('/workspace/hf-test/zen/posting/valentina_video1/work/mont.py').read().split("def make(")[0]
exec(src)  # beat_track, FONT
P='/workspace/hf-test/zen/posting/'
B3=P+'valentina_batch3_tattoo/fin/'
O=P+'valentina_video2/'
def make(tag,imgs,caps,hook,bpm,beats,style,out):
    sd=beats*60/bpm;dur=sd*len(imgs);n=int(round(sd*30))
    beat_track(f'{tag}_beat.wav',bpm,dur,style)
    segs=[]
    for i,im in enumerate(imgs):
        z0,z1=(1.0,1.07) if i%2==0 else (1.07,1.0)
        zf=f"({z0}+({z1}-{z0})*t/{sd})"
        fc=("[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:6,eq=brightness=-0.3:saturation=0.8[bg];"
            f"[b]scale=w='trunc(1080*{zf}/2)*2':h=-2:eval=frame,crop=1080:1440:(iw-1080)/2:0[fg];[bg][fg]overlay=0:200,fps=30,format=yuv420p")
        sg=f'{tag}_seg{i}.mp4'
        subprocess.check_call(['ffmpeg','-y','-v','error','-loop','1','-framerate','30','-t',str(sd),'-i',im,'-filter_complex',fc,'-c:v','libx264','-crf','17',sg]);segs.append(sg)
    open(f'{tag}_list.txt','w').write(''.join(f"file '{s}'\n" for s in segs))
    subprocess.check_call(['ffmpeg','-y','-v','error','-f','concat','-i',f'{tag}_list.txt','-c','copy',f'{tag}_cat.mp4'])
    open(f'{tag}_hook.txt','w').write(textwrap.fill(hook,26))
    st="borderw=4:bordercolor=black@0.8:fontcolor=white"
    hd=2.5
    vf=[f"drawtext=fontfile={FONT}:textfile={tag}_hook.txt:fontsize=50:{st}:line_spacing=10:x=(w-text_w)/2:y=40:enable='lt(t,{hd})'"]
    for i,c in enumerate(caps):
        open(f'{tag}_c{i}.txt','w').write(textwrap.fill(c,26))
        s=hd if i==0 else i*sd+0.15;e=(i+1)*sd-0.05
        vf.append(f"drawtext=fontfile={FONT}:textfile={tag}_c{i}.txt:fontsize=44:{st}:line_spacing=8:x=(w-text_w)/2:y=1680:enable='between(t,{s},{e})'")
    vf.append("noise=alls=4:allf=t,unsharp=3:3:0.3")
    subprocess.check_call(['ffmpeg','-y','-v','error','-i',f'{tag}_cat.mp4','-i',f'{tag}_beat.wav','-vf',','.join(vf),'-map','0:v','-map','1:a','-c:v','libx264','-crf','23','-maxrate','6M','-bufsize','12M','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest','-map_metadata','-1','-movflags','+faststart',out])
    from PIL import Image
    ts=[0.5,1.5]+[sd*i+sd*0.6 for i in range(1,len(imgs))]+[dur-0.1]
    sh=Image.new('RGB',(270*len(ts),480))
    for i,t in enumerate(ts):
        subprocess.check_call(['ffmpeg','-y','-v','error','-ss',str(t),'-i',out,'-frames:v','1','-vf','scale=270:480',f'{tag}_m.png']);sh.paste(Image.open(f'{tag}_m.png'),(270*i,0))
    sh.save(f'{tag}_sheet.png');print(tag,dur)
if sys.argv[1]=='A':
    make('A',[B3+'s8_v4C.jpg',B3+'s1_v4C.jpg',B3+'s4_v4C.jpg',B3+'s2_v4C.jpg',B3+'s3_v4C.jpg'],
     ["6am me: \"I'm so disciplined\"","9am me: \"I'll meal prep today\" (buys everything orange)","1pm me: \"just one book\" (I bought six)","5pm me: \"quick walk\" (chases the sunset)","6pm me: \"I earned this toast\" now watch again, 6am me is back"],
     "gym girl confessions: my 6am self vs my 6pm self, be honest",120,6,'A',O+'valentina_montage_A_9x16.mp4')
else:
    make('B',[B3+'s7_v4C.jpg',B3+'s5_v4C.jpg',B3+'s3_v4C.jpg',B3+'s6_v4C.jpg',B3+'s1_v4C.jpg',B3+'s8_v4C.jpg'],
     ["\"I'll skip the iced latte\" (it's my third)","\"I'll start Monday\" (I know what you're about to say)","\"I'll stretch first\" (I talk for an hour)","\"straight home\" (one text and I'm gone)","\"I'll only buy vegetables\" (the oranges disagree)","\"legs again tomorrow\" you believed me, now watch again"],
     "gym girl confessions: things I swear I'll do after leg day",100,4,'B',O+'valentina_montage_B_9x16.mp4')
