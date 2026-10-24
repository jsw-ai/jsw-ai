# ex.sh NAME URL
set -e; cd /workspace/hf-test/charlotte_matchday_1021b/work; N=$1
curl -s -o raw_$N.mp4 "$2"
ffprobe -v error -show_entries stream=width,height:format=duration -of csv=p=0 raw_$N.mp4
F=$N.mp4
ffmpeg -v error -y -i raw_$N.mp4 -i c477.mp3 -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos:out_range=tv,crop=1080:1920,fps=30[v];[1:a]atrim=0:5,volume=0.8,afade=t=in:st=0:d=1.5,afade=t=out:st=4.5:d=0.5,aresample=48000[a]" -map "[v]" -map "[a]" -c:v libx264 -profile:v main -crf 20 -pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart -c:a aac -b:a 160k -shortest $F
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $F); rm -rf q_$N; mkdir q_$N
for k in 0 1 2 3 4 5; do t=$(python3 -c "print(round($D*($k+0.5)/6,3))"); ffmpeg -v error -y -ss $t -i $F -frames:v 1 q_$N/fr${k}_$t.png; done
cd /workspace/hf-test && /workspace/.face-venv/bin/python zen/posting/identity_gate.py img --model charlotte --source seedream --body charlotte_matchday_1021b/work/q_$N/*.png 2>/dev/null | grep -E "^(PASS|FAIL)" | sed -E "s/'body'.*//"
