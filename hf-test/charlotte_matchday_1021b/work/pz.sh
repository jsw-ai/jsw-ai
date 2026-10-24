# pz.sh NAME ZOOM YC(center fraction)
set -e; cd /workspace/hf-test/charlotte_matchday_1021b/work; N=$1; Z=$2; Y=$3; F=${N}_z$Z.mp4
ffmpeg -v error -y -i raw_$N.mp4 -i c477.mp3 -filter_complex "[0:v]crop=iw/$Z:ih/$Z:(iw-iw/$Z)/2:max(0\,min(ih-ih/$Z\,ih*$Y-ih/$Z/2)),scale=1080:1920:flags=lanczos:out_range=tv,fps=30[v];[1:a]atrim=0:5,volume=0.8,afade=t=in:st=0:d=1.5,afade=t=out:st=4.5:d=0.5,aresample=48000[a]" -map "[v]" -map "[a]" -c:v libx264 -profile:v main -crf 18 -pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart -c:a aac -b:a 160k -shortest $F
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $F); rm -rf q_${N}z; mkdir q_${N}z
for k in 0 1 2 3 4 5; do t=$(python3 -c "print(round($D*($k+0.5)/6,3))"); ffmpeg -v error -y -ss $t -i $F -frames:v 1 q_${N}z/fr${k}_$t.png; done
cd /workspace/hf-test && /workspace/.face-venv/bin/python zen/posting/identity_gate.py img --model charlotte --source seedream charlotte_matchday_1021b/work/q_${N}z/*.png 2>/dev/null | grep -E "^(PASS|FAIL)" | grep -o "fr[0-9]_[0-9.]*png\|centroid': [0-9.]*" | paste - - | tr '\n' ' '; echo
