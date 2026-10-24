import subprocess,sys,json,os
L='/workspace/jsw_tiktok/sienna/lyric_videos/'; S='/workspace/jsw_tiktok/sienna/'
F={'v2sA2_c':(S+'2026-10-22_album/fin/v2sA2_c_v4C.jpg','crop=812:1443:134:0'),
   'bal_p':(S+'x_clips_2026-10-21/remake/fin/bal_p_v4C.jpg','crop=1075:1911:2:0'),
   'gc_surf_i':(L+'02_low_tide_lover/work/gate_src/gc_surf_i_strip.png','crop=666:1184:0:0')}
SRC={'A':dict(sc=L+'01_salt_in_my_hair/scenes/',ass=L+'01_salt_in_my_hair/work/v5es/short.ass',wav='/workspace/music/distrokid/sienna/01_salt_in_my_hair.wav',T0=38.2,out=L+'01_salt_in_my_hair/sienna_salt_in_my_hair_hook_short_1080x1920_v5e',
  end="Sienna Blake\\N'Salt in My Hair'\\Nout now on Apple Music"),
 'B':dict(sc=L+'02_low_tide_lover/scenes/',ass=L+'02_low_tide_lover/work/v3/short3c.ass',wav='/workspace/music/distrokid/sienna/02_low_tide_lover.wav',T0=32.8,out=L+'02_low_tide_lover/sienna_low_tide_lover_hook_short_1080x1920_v3c',
  end="{\\fs48}Sienna Blake\\N{\\fs76}'Low Tide Lover' –\\Nout now on Apple Music")}
song,plat,order,Ldur,hook=sys.argv[1],sys.argv[2],sys.argv[3].split(','),float(sys.argv[4]),sys.argv[5]
s=SRC[song]; out=f"{s['out']}_{plat}_u2.mp4"; assert not os.path.exists(out),out
XF=0.5; n=len(order); D=(Ldur+XF*(n-1))/n
def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
def tp(x): h,m,sec=x.split(':');return int(h)*3600+int(m)*60+float(sec)
lines=open(s['ass']).read().splitlines(); hdr=[l for l in lines if not l.startswith('Dialogue')]; ev=[]
for l in lines:
  if l.startswith('Dialogue') and ',L,' in l:
    p=l.split(',',9); st,en=tp(p[1]),tp(p[2])
    if st>=Ldur-3.6: continue
    p[2]=ts(min(en,Ldur-3.6)); ev.append(','.join(p))
i=[k for k,l in enumerate(hdr) if l.startswith('Style: E')][0]
hdr.insert(i+1,'Style: H,DejaVu Sans,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,1,0,1,3,3,8,90,90,90,1')
ev.append(f"Dialogue: 1,0:00:00.00,{ts(2.9)},H,,0,0,0,,{{\\q2\\fad(0,250)}}{hook}")
ev.append(f"Dialogue: 0,{ts(Ldur-3.5)},{ts(Ldur)},E,,0,0,0,,{{\\q2\\fad(300,0)}}{s['end']}")
A=f'{song}_{plat}_u2.ass'; open(A,'w').write('\n'.join(hdr+ev)+'\n')
inp=[];pre=[]
for k,o in enumerate(order):
  if o in F: src,cr=F[o]; vf=cr
  else: src=s['sc']+f'scene_{o}.png'; vf='crop=ih*9/16:ih'
  os.makedirs('static_segs',exist_ok=True); sg=f'static_segs/{song}_{o}_{D:.3f}.mp4'
  if not os.path.exists(sg): subprocess.run(['ffmpeg','-v','error','-y','-threads','2','-loop','1','-framerate','30','-i',src,'-t',f'{D:.3f}','-vf',f'{vf},scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p','-c:v','libx264','-crf','14','-preset','fast','-tune','stillimage',sg],check=True)  # static still: no pan, no zoom
  inp+=['-i',sg]; pre.append(f'[{k}:v]null[p{k}];')
fc=''.join(pre); last='p0'; off=0
for k in range(1,n):
  off+=D-XF; fc+=f'[{last}][p{k}]xfade=transition=fade:duration={XF}:offset={off:.4f}[x{k}];'; last=f'x{k}'
fc+=f'[{last}]trim=duration={Ldur},setpts=PTS-STARTPTS,ass={A},scale=out_range=tv,format=yuv420p[v];'
fc+=f"[{n}:a]atrim={s['T0']}:{s['T0']+Ldur},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={Ldur-1.5}:d=1.5[a]"
subprocess.run(['ffmpeg','-v','error','-n','-threads','3',*inp,'-i',s['wav'],'-filter_complex',fc,'-map','[v]','-map','[a]','-c:v','libx264','-profile:v','main','-pix_fmt','yuv420p','-b:v','3500k','-maxrate','4500k','-bufsize','9000k','-preset','medium','-r','30','-c:a','aac','-b:a','192k','-ar','48000','-t',str(Ldur),'-movflags','+faststart','-map_metadata','-1',out],check=True)
fw=[(o,k*(D-XF)+XF+0.05,min(k*(D-XF)+D-XF-0.05,Ldur-3.6)) for k,o in enumerate(order) if o in F]
json.dump(dict(out=out,order=order,D=D,face_windows=[[a,b] for _,a,b in fw],faces=[o for o,_,_ in fw]),open(f'{song}_{plat}_u2.json','w'))
print(out,round(D,3),fw)
