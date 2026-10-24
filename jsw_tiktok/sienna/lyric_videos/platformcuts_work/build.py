import subprocess,sys,json,re,os
L='/workspace/jsw_tiktok/sienna/lyric_videos/'
SRC={'A':dict(seg=L+'01_salt_in_my_hair/work/v5es/seg_short/',ass=L+'01_salt_in_my_hair/work/v5es/short.ass',wav='/workspace/music/distrokid/sienna/01_salt_in_my_hair.wav',T0=38.2,out=L+'01_salt_in_my_hair/sienna_salt_in_my_hair_hook_short_1080x1920_v5e',
  end="Sienna Blake\\N'Salt in My Hair'\\Nout now on Apple Music"),
 'B':dict(seg=L+'02_low_tide_lover/work/v3/seg3c_short/',ass=L+'02_low_tide_lover/work/v3/short3c.ass',wav='/workspace/music/distrokid/sienna/02_low_tide_lover.wav',T0=32.8,out=L+'02_low_tide_lover/sienna_low_tide_lover_hook_short_1080x1920_v3c',
  end="{\\fs48}Sienna Blake\\N{\\fs76}'Low Tide Lover' –\\Nout now on Apple Music")}
song,plat,order,Ldur,hook=sys.argv[1],sys.argv[2],[int(x) for x in sys.argv[3].split(',')],float(sys.argv[4]),sys.argv[5]
s=SRC[song]; out=f"{s['out']}_{plat}_u1.mp4"
assert not os.path.exists(out),out
def ts(t): h=int(t//3600);m=int(t%3600//60);return f"{h}:{m:02d}:{t%60:05.2f}"
def tp(x): h,m,sec=x.split(':');return int(h)*3600+int(m)*60+float(sec)
lines=open(s['ass']).read().splitlines(); hdr=[l for l in lines if not l.startswith('Dialogue')]
ev=[]
for l in lines:
  if l.startswith('Dialogue') and ',L,' in l:
    p=l.split(',',9); st,en=tp(p[1]),tp(p[2]); EC=Ldur-3.6
    if st>=EC: continue
    p[2]=ts(min(en,EC)); ev.append(','.join(p))
hs=hdr[:]; i=[k for k,l in enumerate(hs) if l.startswith('Style: E')][0]
hs.insert(i+1,'Style: H,DejaVu Sans,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,1,0,1,3,3,8,90,90,'+(sys.argv[6] if len(sys.argv)>6 else '300')+',1')
ev.append(f"Dialogue: 1,0:00:00.00,{ts(2.9)},H,,0,0,0,,{{\\q2\\fad(0,250)}}{hook}")
ev.append(f"Dialogue: 0,{ts(Ldur-3.5)},{ts(Ldur)},E,,0,0,0,,{{\\q2\\fad(300,0)}}{s['end']}")
open(f'{song}_{plat}.ass','w').write('\n'.join(hs+ev)+'\n')
inp=[];fc='';last='0:v';off=0
for k,i in enumerate(order): inp+=['-i',s['seg']+f'{i:03d}.mp4']
for k in range(1,len(order)):
  off+=4.8333-1.0; fc+=f'[{last}][{k}:v]xfade=transition=fade:duration=1:offset={off:.4f}[x{k}];'; last=f'x{k}'
fc+=f'[{last}]trim=duration={Ldur},setpts=PTS-STARTPTS,ass={song}_{plat}.ass,scale=out_range=tv,format=yuv420p[v];'
n=len(order); fc+=f"[{n}:a]atrim={s['T0']}:{s['T0']+Ldur},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={Ldur-1.5}:d=1.5[a]"
subprocess.run(['ffmpeg','-v','error','-n',*inp,'-i',s['wav'],'-filter_complex',fc,'-map','[v]','-map','[a]','-c:v','libx264','-profile:v','main','-pix_fmt','yuv420p','-b:v','3500k','-maxrate','4500k','-bufsize','9000k','-preset','medium','-r','30','-c:a','aac','-b:a','192k','-ar','48000','-t',str(Ldur),'-movflags','+faststart','-map_metadata','-1',out],check=True)
# face windows (fully-on) for the gate
fw=[(k*3.8333+1.05,min(k*3.8333+3.78,Ldur-3.6)) for k,i in enumerate(order) if (song,i) in [('A',2),('B',0),('B',2)]]
json.dump(dict(out=out,order=order,face_windows=fw),open(f'{song}_{plat}.json','w'))
print(out,fw)
