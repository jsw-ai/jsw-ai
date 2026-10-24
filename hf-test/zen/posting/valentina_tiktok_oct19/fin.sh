#!/bin/bash
# fin.sh raw.mp4 n
R=$1; n=$2; FONT=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
D="fontfile=$FONT:fontsize=64:fontcolor=white:borderw=5:bordercolor=black@0.85:line_spacing=10:x=(w-text_w)/2:y=300"
ffmpeg -loglevel error -y -i $R -f lavfi -i anullsrc=r=44100:cl=stereo -t 5 -filter_complex "[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.08[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,drawtext=$D:textfile=txt/${n}_h.txt:enable='lt(t,2.5)',drawtext=$D:textfile=txt/${n}_p.txt:enable='gte(t,2.5)',noise=alls=5:allf=t,format=yuv420p[v]" -map "[v]" -map 1:a -shortest -c:v libx264 -crf 20 -preset slow -r 30 -c:a aac -b:a 64k -map_metadata -1 -fflags +bitexact -movflags +faststart final/$n.mp4
