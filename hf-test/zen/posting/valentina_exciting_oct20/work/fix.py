import subprocess,sys,json,textwrap
from PIL import ImageFont
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def lines(t,size=92,maxw=980):
    if '|' in t: return sum([lines(p,size,maxw) for p in t.split('|')],[])
    words=t.split();out=[];cur=''
    for w in words:
        c=(cur+' '+w).strip()
        if ImageFont.truetype(F,size).getbbox(c)[2]>maxw and cur: out.append(cur);cur=w
        else: cur=c
    out.append(cur);return out
def fix(src,out,crop,texts,afilt,pos='bottom',size=92,vf_pre=''):
    fc=[f"[0:v]{vf_pre}crop={crop},scale=1080:1920:flags=lanczos,setsar=1[c]"];last='c';k=0
    for t,a,b in texts:
        L=lines(t,size); lh=int(size*1.22); n=len(L)
        y0 = 150 if pos=='top' else 1920-300-n*lh   # stay inside TikTok safe area
        for i,l in enumerate(L):
            fn=f'/tmp/vt_{k}.txt';open(fn,'w').write(l);k+=1
            fc.append(f"[{last}]drawtext=fontfile={F}:textfile={fn}:fontsize={size}:fontcolor=white:borderw=7:bordercolor=black:box=1:boxcolor=black@0.35:boxborderw=14:x=(w-text_w)/2:y={y0+i*lh}:enable='between(t,{a},{b})'[t{k}]");last=f't{k}'
    cmd=['ffmpeg','-v','error','-y','-i',src,'-filter_complex',';'.join(fc),'-map',f'[{last}]','-map','0:a','-af',afilt,
         '-c:v','libx264','-profile:v','main','-crf','18','-preset','slow','-pix_fmt','yuv420p','-r','30',
         '-c:a','aac','-b:a','192k','-ar','48000','-map_metadata','-1','-movflags','+faststart',out]
    subprocess.check_call(cmd)
def loud(src,tp=-1.0,I=-14):
    r=subprocess.run(['ffmpeg','-hide_banner','-i',src,'-af',f'loudnorm=I={I}:TP={tp}:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
    s=r.rindex('{');j=json.loads(r[s:r.index('}',s)+1])
    return f"loudnorm=I={I}:TP={tp-0.2}:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=48000,alimiter=limit=0.89:level=false"
if __name__=='__main__':
    D='../final/'
    v=sys.argv[1]
    if v=='v2':
        fix(D+'v2.mp4',D+'v2_fix.mp4','808:1436:136:242',[('flying home to see my mom ✈️'.replace(' ✈️',''),0,3.5),('first class = emotional armor',3.5,8.01)],loud(D+'v2.mp4'))
    if v=='v4':
        fix(D+'v4.mp4',D+'v4_fix.mp4','810:1440:135:240',[('Cartagena by day',0,2.8),('mom: "home by|11, mija"|me at 11:',4.4,9.01)],loud(D+'v4.mp4'))
