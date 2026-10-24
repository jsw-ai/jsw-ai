import subprocess, os
F='/workspace/hf-test/zen/posting/gabriela_w1/final/'
S={k:F+f for k,f in dict(A='g_A_r2_v4C.jpg',B='g_B_r3_v4C.jpg',C='g_C_r5_v4C.jpg',D='g_D_r6_v4C.jpg',E='g_E_n1_v4C.jpg',F='g_F_n2_v4C.jpg',G='g_G_n7_v4C.jpg',H='g_H_n8_v4C.jpg').items()}
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FPS=30
def seg(out,img,dur,zoom_in=True,zmax=1.15,cx=0.5,cy=0.4,text=None,tstart=0,tend=None,tsize=84,ty=1620):
    n=int(dur*FPS)
    z=f"1+({zmax}-1)*on/{n}" if zoom_in else f"{zmax}-({zmax}-1)*on/{n}"
    vf=(f"scale=-2:2400,crop=1620:2400:(iw-1620)/2:0,zoompan=z='{z}':x='(iw-iw/zoom)*{cx}':y='(ih-ih/zoom)*{cy}':d={n}:s=1080x1920:fps={FPS},"
        "unsharp=3:3:0.4,noise=alls=5:allf=t")
    if text:
        te=tend if tend else dur
        vf+=(f",drawtext=fontfile={FONT}:text='{text}':fontsize={tsize}:fontcolor=white:borderw=6:bordercolor=black@0.85:"
             f"x=(w-text_w)/2:y={ty}:enable='between(t,{tstart},{te})'")
    subprocess.run(['ffmpeg','-y','-v','error','-loop','1','-i',S[img],'-t',str(dur),'-vf',vf+',format=yuv420p','-r',str(FPS),'-c:v','libx264','-crf','17',out],check=True)
def concat(parts,out):
    open('list.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i','list.txt','-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-an','-movflags','+faststart','-map_metadata','-1',out],check=True)
D='/workspace/hf-test/zen/posting/gabriela_videos/'
# Video A: captions, 5 x 3s
A=[('E','golden hour does most of the work',0.0),('G','sun going down',0.6),('B','laughing at nothing',0.4),('D','shoes in hand',0.4),('H','nowhere to be',0.4)]
parts=[]
# add per-segment word pop: second line words
words={'E':'golden hour','G':'sun going down','B':'good mood','D':'sand between my toes','H':'late sun and no plans'}
for i,(k,t,_) in enumerate(A):
    o=f'a{i}.mp4'
    seg(o,k,3.0,zoom_in=(i%2==0),text=words[k] if i else 'golden hour mood',tstart=0.3,tend=2.8,tsize=76)
    parts.append(o)
concat(parts,D+'gabriela_captions_15s_1080x1920.mp4')
import sys; sys.exit()
order=['E','H','B','G','D','F','A','C']
cuts=[]
import itertools
pat=[(0.5,0.35,True,1.18),(0.5,0.5,False,1.12),(0.5,0.3,True,1.25),(0.5,0.45,False,1.1)]
for i in range(30):
    k=order[i%8]; d,cy,zi,zm=pat[(i//2+i)%4]
    o=f'b{i}.mp4'; seg(o,k,0.5,zoom_in=zi,zmax=zm,cx=0.5,cy=0.3 if i%3==0 else cy); cuts.append(o)
concat(cuts,D+'gabriela_beatcut_15s_1080x1920_silent.mp4')
