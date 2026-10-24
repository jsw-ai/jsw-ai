# build.py spec.json : segments [{src,ss,to}], texts [{t,a,b}], music, music_ss, out
import json,subprocess,sys,os,tempfile
sp=json.load(open(sys.argv[1]));F='/usr/share/fonts/truetype/sand-box/google/Poppins/Poppins-Bold.ttf'
tmp=tempfile.mkdtemp(dir=os.path.dirname(sp['out']));parts=[]
for i,s in enumerate(sp['segments']):
    o=f'{tmp}/p{i}.mp4'
    vf=s.get("vf","scale=-2:1920,crop=1080:1920")+",fps=30,setsar=1"
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(s['ss']),'-to',str(s['to']),'-i',s['src'],'-filter_complex',vf,'-an','-c:v','libx264','-crf','12','-preset','fast',o],check=True)
    parts.append(o)
lst=f'{tmp}/l.txt';open(lst,'w').write(''.join(f"file '{p}'\n" for p in parts))
cat=f'{tmp}/cat.mp4';subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',lst,'-c','copy',cat],check=True)
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',cat],capture_output=True,text=True).stdout)
dt=[]
for j,t in enumerate(sp['texts']):
    tf=f'{tmp}/t{j}.txt';open(tf,'w').write(t['t'])
    dt.append(f"drawtext=fontfile={F}:textfile={tf}:fontsize={t.get('fs',58)}:fontcolor=white:borderw=5:bordercolor=black:x=(w-text_w)/2:y={t.get('y',150)}:enable='between(t,{t['a']},{t['b']})'")
vf=','.join(dt+[f"noise=alls={sp.get('noise',4)}:allf=t"]) if dt else f"noise=alls={sp.get('noise',4)}:allf=t"
a=f"[1:a]atrim=0:{dur},afade=t=in:d=0.3,afade=t=out:st={dur-0.6}:d=0.6,volume={sp.get('vol',0.9)}[aa]"
subprocess.run(['ffmpeg','-v','error','-y','-i',cat,'-ss',str(sp.get('music_ss',0)),'-i',sp['music'],'-filter_complex',f'[0:v]{vf}[v];{a}','-map','[v]','-map','[aa]',
 '-c:v','libx264','-profile:v','main','-pix_fmt','yuv420p','-crf','19','-maxrate','14M','-bufsize','28M','-preset','medium','-threads','2','-r','30','-c:a','aac','-b:a','128k','-ar','48000',
 '-map_metadata','-1','-movflags','+faststart','-t',str(dur),sp['out']],check=True)
subprocess.run(['rm','-rf',tmp]);print(sp['out'],round(dur,2),os.path.getsize(sp['out'])//1024,'KB')
