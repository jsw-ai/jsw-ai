import sys,subprocess; sys.path.insert(0,'..'); from edit import build
b1=60/99.4; b3=60/112.3
K='kl/'
segs1=[(K+'c3_1.mp4',1.92,4*b1),(K+'c1_1.mp4',2.92,3*b1),(K+'c2_2.mp4',0.0,3*b1),(K+'c4_1.mp4',3.17,3*b1)]
segs3=[(K+'p1_1.mp4',0.1,6*b3),(K+'a1_2.mp4',0.0,8*b3)]
build(segs1,'m139.mp3',0.0+50*b1,['POV: your Brazilian','friend is on grill duty'],'tiktok_1_v2.mp4')
build(segs3,'m138.mp3',0.19+56*b3,['Brazilian comfort','food check'],'tiktok_3_v2.mp4')
for n in ('tiktok_1_v2','tiktok_3_v2'):
    subprocess.run(['ffmpeg','-v','error','-y','-i',n+'.mp4','-c:v','copy','-an','-map_metadata','-1',n+'_silent.mp4'],check=True)
