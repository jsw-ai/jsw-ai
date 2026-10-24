import subprocess,textwrap,sys,numpy as np,wave,json
from PIL import Image
P='/workspace/hf-test/zen/posting/'
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def beat_track(name,bpm,dur,style):
    sr=44100;t=np.arange(int(sr*dur))/sr;a=np.zeros_like(t);b=60/bpm;rng=np.random.default_rng(2)
    for i in range(int(dur/b)):
        s=int(i*b*sr);n=int(0.25*sr);tt=np.arange(n)/sr
        k=np.sin(2*np.pi*(50+90*np.exp(-tt*30))*tt)*np.exp(-tt*12);seg=a[s:s+n];seg+=0.7*k[:len(seg)]
        off=0.5 if style=='A' else 0.667
        h=int((i*b+b*off)*sr);n=int(0.05*sr);seg=a[h:h+n];seg+=0.12*(rng.standard_normal(n)*np.exp(-np.arange(n)/sr*80))[:len(seg)]
        if i%2==1:
            n=int(0.12*sr);seg=a[s:s+n];seg+=0.25*(rng.standard_normal(n)*np.exp(-np.arange(n)/sr*30))[:len(seg)]
        if style=='B':
            f=[110,110,130.8,98][(i//2)%4];n=int(b*sr);tt=np.arange(n)/sr;seg=a[s:s+n];seg+=0.18*(np.sin(2*np.pi*f*tt)*np.exp(-tt*3))[:len(seg)]
    ch=[(220,.06),(277.2,.05),(329.6,.05)] if style=='A' else [(196,.05),(246.9,.05),(293.7,.05),(392,.03)]
    for f,g in ch: a+=g*np.sin(2*np.pi*f*t)*(0.7+0.3*np.sin(2*np.pi*t/b/4))
    a*=np.minimum(1,(dur-t)/0.4);a=a/np.max(np.abs(a))*0.8
    w=wave.open(name,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writestr=0
    w.writeframes((a*32767).astype(np.int16).tobytes());w.close()
def make(tag,imgs,caps,hook,bpm,beats,style,out):
    sd=beats*60/bpm;dur=sd*len(imgs);n=int(round(sd*30))
    beat_track(f'{tag}_beat.wav',bpm,dur,style)
    ins=[];fc=''
    for i,im in enumerate(imgs):
        ins+=['-i',im]
        z="min(zoom+0.0016,1.12)" if i%2==0 else "if(eq(on,0),1.12,max(zoom-0.0016,1.0))"
        z=z.replace('0.0016',str(round(0.12/n,5)))
        fc+=f"[{i}:v]scale=1440:-2,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)-60':d={n}:s=1080x1920:fps=30,setsar=1[v{i}];"
    fc+=''.join(f'[v{i}]' for i in range(len(imgs)))+f"concat=n={len(imgs)}:v=1:a=0[cat]"
    subprocess.check_call(['ffmpeg','-y','-v','error']+ins+['-filter_complex',fc,'-map','[cat]','-pix_fmt','yuv420p','-c:v','libx264','-crf','17',f'{tag}_cat.mp4'])
    open(f'{tag}_hook.txt','w').write(textwrap.fill(hook,26))
    st="borderw=4:bordercolor=black@0.8:fontcolor=white"
    hd=2.5
    vf=[f"drawtext=fontfile={FONT}:textfile={tag}_hook.txt:fontsize=54:{st}:line_spacing=12:x=(w-text_w)/2:y=150:enable='lt(t,{hd})'"]
    for i,c in enumerate(caps):
        open(f'{tag}_c{i}.txt','w').write(textwrap.fill(c,26))
        s=hd if i==0 else i*sd+0.15;e=(i+1)*sd-0.05
        vf.append(f"drawtext=fontfile={FONT}:textfile={tag}_c{i}.txt:fontsize=46:{st}:x=(w-text_w)/2:y=1500:enable='between(t,{s},{e})'")
    vf.append("noise=alls=6:allf=t,unsharp=3:3:0.4")
    subprocess.check_call(['ffmpeg','-y','-v','error','-i',f'{tag}_cat.mp4','-i',f'{tag}_beat.wav','-vf',','.join(vf),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest','-map_metadata','-1','-movflags','+faststart',out])
    k=len(imgs)*2+1;ts=[0.5,1.5]+[sd*i+sd*0.6 for i in range(1,len(imgs))]+[dur-0.1]
    sh=Image.new('RGB',(270*len(ts),480))
    for i,t in enumerate(ts):
        subprocess.check_call(['ffmpeg','-y','-v','error','-ss',str(t),'-i',out,'-frames:v','1','-vf','scale=270:480',f'{tag}_m.png']);sh.paste(Image.open(f'{tag}_m.png'),(270*i,0))
    sh.save(f'{tag}_sheet.png');print(tag,dur)
B2=P+'valentina_batch2/fin/';B1=P+'valentina_batch1/fin/'
O=P+'valentina_video1/'
if sys.argv[1]=='A':
    make('A',[B2+'b8_v4C.jpg',B2+'b1_v4C.jpg',B2+'b4_v4C.jpg',B2+'b2_v4C.jpg',B2+'b3_v4C.jpg'],
     ["6am me: \"I'm so disciplined\"","9am me: \"I'll meal prep today\" (buys everything orange)","1pm me: \"just one book\" (I bought six)","5pm me: \"quick walk\" (chases the sunset)","6pm me: \"I earned this toast\" now watch again, 6am me is back"],
     "gym girl confessions: my 6am self vs my 6pm self, be honest",120,6,'A',O+'valentina_montage_A_9x16.mp4')
else:
    make('B',[B1+'b2_v4C.jpg',B1+'b3_v4C.jpg',B1+'b5_v4C.jpg',B1+'b6_v4C.jpg',B1+'b7_v4C.jpg',B1+'b4_v4C.jpg'],
     ["\"I'll only buy vegetables\" (the oranges had other plans)","\"I'll stretch\" (I walk for an hour instead)","\"I'll skip brunch\" (laughs in avocado toast)","\"straight home\" (the bookstore says hi)","\"legs again tomorrow\" (pool day instead)","\"I'll start Monday\" you believed me, now watch again"],
     "gym girl confessions: things I swear I'll do after leg day",100,4,'B',O+'valentina_montage_B_9x16.mp4')
