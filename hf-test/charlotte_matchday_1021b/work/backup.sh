set -e
cd /workspace/hf-test/charlotte_matchday_1021b/work; rm -rf seq; mkdir seq
python3 - <<'P'
from PIL import Image
im=Image.open('/workspace/hf-test/charlotte_clips_1021/work/fin/N1_v4C.jpg').convert('RGB').resize((1084,1920),Image.LANCZOS).crop((2,0,1082,1920))
W,H=1080,1920;cx,cy=620,790;N=int(3.8*30)
for i in range(N):
    t=i/(N-1); t=t*t*(3-2*t); z=1.15-0.15*t
    w,h=W/z,H/z; x=min(max(cx-w/2,0),W-w); y=min(max(cy-h/2,0),H-h)
    im.transform((W,H),Image.EXTENT,(x,y,x+w,y+h),Image.BICUBIC).save(f'seq/{i:04d}.jpg',quality=95)
P
ffmpeg -v error -y -framerate 30 -i seq/%04d.jpg -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p a.mp4
ffmpeg -v error -y -t 1.2 -i /workspace/hf-test/charlotte_clips_1021/work/clips/N.mp4 -vf "scale=1084:1920:flags=lanczos,crop=1080:1920,fps=30" -an -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p b.mp4
F=../charlotte_matchday_awayend_1021b_BACKUP_nocredit.mp4
ffmpeg -v error -y -i a.mp4 -i b.mp4 -i c477.mp3 -filter_complex "[0:v][1:v]concat=n=2:v=1[v];[2:a]atrim=0:5,afade=t=in:d=0.3,afade=t=out:st=4.5:d=0.5,aresample=48000[a]" -map "[v]" -map "[a]" -c:v libx264 -profile:v main -crf 20 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 160k -shortest $F
ffprobe -v error -show_entries stream=codec_name,profile,width,height,pix_fmt:format=duration,size -of compact $F
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $F); mkdir -p qcb; rm -f qcb/*
for k in 0 1 2 3 4 5; do t=$(python3 -c "print(round($D*($k+0.5)/6,3))"); ffmpeg -v error -y -ss $t -i $F -frames:v 1 qcb/fr${k}_$t.png; done
cd /workspace/hf-test && /workspace/.face-venv/bin/python zen/posting/identity_gate.py img --model charlotte --source seedream charlotte_matchday_1021b/work/qcb/*.png 2>/dev/null | grep -E "^(PASS|FAIL)" | cut -c1-120
