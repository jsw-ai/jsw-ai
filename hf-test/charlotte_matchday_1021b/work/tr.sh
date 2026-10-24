# tr.sh NAME START ZOOM OUT
set -e; cd /workspace/hf-test/charlotte_matchday_1021b/work; N=$1; S=$2; Z=$3; F=$4
D0=$(python3 -c "print(round(5.04-$S,3))"); FO=$(python3 -c "print(round(5.04-$S-0.5,3))")
ffmpeg -v error -y -ss $S -i raw_$N.mp4 -i c477.mp3 -filter_complex "[0:v]crop=iw/$Z:ih/$Z:(iw-iw/$Z)/2:max(0\,min(ih-ih/$Z\,ih*0.33-ih/$Z/2)),scale=1080:1920:flags=lanczos:out_range=tv,fps=30,setpts=PTS-STARTPTS[v];[1:a]atrim=0:$D0,volume=0.8,afade=t=in:st=0:d=1.5,afade=t=out:st=$FO:d=0.5,aresample=48000[a]" -map "[v]" -map "[a]" -c:v libx264 -profile:v main -crf 18 -pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart -c:a aac -b:a 160k -shortest $F
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $F); Q=q_$(basename $F .mp4); rm -rf $Q; mkdir $Q
for k in 0 1 2 3 4 5; do t=$(python3 -c "print(round($D*($k+0.5)/6,3))"); ffmpeg -v error -y -ss $t -i $F -frames:v 1 $Q/fr${k}_$t.png; done
cd /workspace/hf-test && /workspace/.face-venv/bin/python zen/posting/identity_gate.py img --model charlotte --source seedream charlotte_matchday_1021b/work/$Q/*.png 2>/dev/null | grep -E "^(PASS|FAIL)" | grep -o "centroid': [0-9.]*" | tr '\n' ' '; echo
