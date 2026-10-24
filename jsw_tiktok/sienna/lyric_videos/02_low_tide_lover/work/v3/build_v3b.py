import json,subprocess,sys,os
mode=sys.argv[1]  # full | short
S='/workspace/jsw_tiktok/sienna/'; A=S+'2026-10-22_album/fin/'
# originals of surf_c / gc_surf_i / b1a were archived off-box 2026-10-22 03:25; comp/ holds track-1's 16:9 composites (fg 701x1242 at x753-1454)
# v3: only stills with verifiable v4C provenance on box; 16:9 = outpainted (Higgsfield outpaint, original pixels pasted back over the face/body)
# v3b: sC2_b replaced by v2sA2_c (0.808); surf_c/gc_surf_i/b1a = track-1 approved v4C strips, outpainted to 16:9
O='v3/op/'
P=[(O+'v2sA2_c_op169.png','crop=2730:1536:11:0'),(O+'surf_c_op169.png','crop=1840:1035:470:283'),(O+'eC2_a_169_final.png','crop=2730:1536:11:0'),(O+'gc_surf_i_op169.png','crop=1840:1035:467:0'),(O+'b1a_op169.png','crop=2200:1238:287:0')]
P9={O+'v2sA2_c_op169.png':(A+'v2sA2_c_v4C.jpg','crop=812:1443:134:0'),O+'surf_c_op169.png':('gate_src/surf_c_strip.png','crop=666:1184:0:0'),O+'eC2_a_169_final.png':(A+'eC2_a_v4C.jpg','crop=1075:1911:2:0'),O+'gc_surf_i_op169.png':('gate_src/gc_surf_i_strip.png','crop=666:1184:0:0'),O+'b1a_op169.png':('gate_src/b1a_strip.png','crop=666:1184:0:0')}
SC=[f'../scenes/scene_{i}.png' for i in (2,4,0,5,6,7,3,1)]  # towel, headland, ripples, rock pools, lifeguard dusk, horizon, bonnet chips, blue hour
NS=len(SC); NP=len(P)
rows=json.load(open('v3/timings_v3.json'))
W,H=(1920,1080) if mode=='full' else (1080,1920)
XF=1.0
if mode=='full':
  T0,T1=0.0,167.2; D=6.0
  order=[]; pi=si=0
  for k in range(int((T1-T0)/(D-XF))+1):
    if k%2==1: order.append(('s',SC[si%NS])); si+=1
    else: order.append(('p',P[pi%NP])); pi+=1
else:
  T0,T1=32.8,56.8  # chorus 1 hook (24 s) + end card inside last 4 s
  D=4.4; sc=lambda i:('s',f'../scenes/scene_{i}.png')
  order=[('p',P[4]),sc(5),('p',P[3]),sc(0),sc(4),sc(1)]  # b1a, rock pools, gc_surf_i, ripples, headland, blue hour (end card); v2sA2_c/eC2_a gated 0.772-0.779 in 9:16 -> full only
dur=T1-T0
n=len(order); D=(dur+XF*(n-1))/n; D=round((D-XF)*30)/30+XF
segs=[]
os.makedirs(f'v3/seg3_{mode}',exist_ok=True)
fps=30
for k,(kind,it) in enumerate(order):
  out=f'v3/seg3_{mode}/{k:03d}.mp4'; segs.append(out)
  if os.path.exists(out): continue
  dirn=k%4 if kind=='s' else (k//2+k//10)%4
  if kind=='s':
    src=it
    if mode=='full': pre=f'scale=2208:-2'   # 2208x1247 pan room
    else: pre=f'crop=ih*9/16:ih,scale=1242:2208'
  else:
    src,cr=it
    if mode=='full':
      pre=cr+',scale=2208:1242:flags=lanczos'
    else:
      src,cr=P9[src]; pre=cr+',scale=1242:2208:flags=lanczos'
  zx=f'(iw-{W})'; zy=f'(ih-{H})'
  if kind=='p': xs=[f'{zx}/2*(1-t/{D})+0',f'{zx}/2*(t/{D})+{zx}/4',f'{zx}/2',f'{zx}*(1-t/{D})/2+{zx}/4'][dirn]; ys=f'{zy}*0.3*(t/{D})' if dirn%2 else f'{zy}*0.3*(1-t/{D})'
  else: xs=[f'{zx}*t/{D}',f'{zx}*(1-t/{D})',f'{zx}/2',f'{zx}/2'][dirn]; ys=[f'{zy}/2',f'{zy}/2',f'{zy}*t/{D}',f'{zy}*(1-t/{D})'][dirn]
  vf=f"{pre},fps={fps},crop={W}:{H}:'{xs}':'{ys}',setsar=1,format=yuv420p"
  subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate',str(fps),'-i',src,'-t',f'{D:.3f}','-vf',vf,'-c:v','libx264','-crf','16','-preset','fast',out],check=True)
# ASS
fs=62 if mode=='full' else 64; mv=80 if mode=='full' else 560
def ts(x):
  x=max(0,x); h=int(x//3600); m=int(x%3600//60); s=x%60; return f'{h}:{m:02d}:{s:05.2f}'
ass=f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,DejaVu Sans,{fs},&H00FFFFFF,&H00FFFFFF,&H50000000,&H78000000,1,0,0,0,100,100,1,0,1,2.2,2,2,{160 if mode=='full' else 110},{160 if mode=='full' else 110},{mv},1
Style: E,DejaVu Sans,{fs},&H00FFFFFF,&H00FFFFFF,&H50000000,&H78000000,1,0,0,0,100,100,1,0,1,2.2,2,5,110,110,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
for i,(s,e,t) in enumerate(rows):
  nxt=rows[i+1][0] if i+1<len(rows) else e+3
  e2=min(max(e+0.4,s+1.8),nxt-0.05,s+7)
  s2,e2=s-0.15-T0,e2-T0
  if e2<=0 or s2>=dur: continue
  if mode=='short' and s2>dur-4: continue
  e2=min(e2,dur-4.05) if mode=='short' else e2
  ass+=f"Dialogue: 0,{ts(s2)},{ts(e2)},L,,0,0,0,,{{\\fad(150,150)}}{t}\n"
ec=(dur-4) if mode=='short' else 160.0
card=("{\\fs48}Sienna Blake\\N{\\fs76}'Low Tide Lover' –\\Ncoming soon" if mode=='short' else "{\\fs44}Sienna Blake\\N{\\fs72}'Low Tide Lover' – coming soon")
ass+=f"Dialogue: 0,{ts(ec)},{ts(dur)},E,,0,0,0,,{{\\q2\\fad(300,0)}}"+card+"\n"
open(f'v3/{mode}3.ass','w').write(ass)
# chain (chunked to keep memory low)
G=3; step=D-XF; chunks=[]
fcv=f"tpad=stop_mode=clone:stop_duration=3,ass=v3/{mode}3.ass,scale=out_range=tv,format=yuv420p"
if mode=='short': fcv+=",fade=t=in:d=0.4"
for g0 in range(0,n,G):
  idx=list(range(max(0,g0-1),min(n,g0+G)))
  cf=f'v3/chunk3_{mode}_{g0:03d}.mp4'; chunks.append(cf)
  if os.path.exists(cf): continue
  inp=[];fc='';last='0:v';off=0
  for s_ in idx: inp+=['-i',segs[s_]]
  for k in range(1,len(idx)):
    off+=step; fc+=f'[{last}][{k}:v]xfade=transition=fade:duration={XF}:offset={off:.4f}[x{k}];'; last=f'x{k}'
  skip=step if g0>0 else 0
  length=len(idx)*step+XF-skip if g0+G>=n else (len(idx)*step-skip)
  fc+=f'[{last}]trim=start={skip:.4f}:duration={length:.4f},setpts=PTS-STARTPTS[v]'
  subprocess.run(['ffmpeg','-v','error',*inp,'-filter_complex',fc,'-map','[v]','-c:v','libx264','-crf','12','-preset','fast','-pix_fmt','yuv420p','-r','30',cf],check=True)
open(f'v3/chunks3_{mode}.txt','w').write(''.join(f"file '{os.path.basename(c)}'\n" for c in chunks))
af=f"atrim={T0}:{T1},asetpts=PTS-STARTPTS"+(f",afade=t=in:d=0.3,afade=t=out:st={dur-1.5}:d=1.5" if mode=='short' else '')
outp=sys.argv[2]
assert not os.path.exists(outp)
br=['-crf','18'] if mode=='full' else ['-b:v','3500k','-maxrate','4500k','-bufsize','7000k']
subprocess.run(['ffmpeg','-v','error','-f','concat','-safe','0','-i',f'v3/chunks3_{mode}.txt','-i','/workspace/music/distrokid/sienna/02_low_tide_lover.wav','-filter_complex',f'[0:v]{fcv}[v];[1:a]{af}[a]','-map','[v]','-map','[a]','-c:v','libx264','-profile:v','main','-pix_fmt','yuv420p','-color_range','tv',*br,'-preset','medium','-r','30','-c:a','aac','-b:a','192k','-ar','48000','-t',f'{dur:.3f}','-movflags','+faststart','-map_metadata','-1',outp],check=True)
print('done',outp,n,D)
