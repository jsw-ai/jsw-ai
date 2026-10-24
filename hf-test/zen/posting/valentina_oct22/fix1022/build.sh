#!/bin/bash
# usage: build.sh out opener ss body body_ss music music_ss hookfile
set -e
out=$1; op=$2; ss=$3; body=$4; bss=$5; mus=$6; mss=$7; hook=$8
F=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
ffmpeg -y -threads 2 -ss $ss -t 1.6 -i $op -ss $bss -i $body -ss $mss -i $mus -filter_complex \
"[0:v]fps=30,scale=-2:1920:flags=lanczos,crop=1080:1920,setsar=1,drawtext=fontfile=$F:textfile=$hook:fontsize=54:fontcolor=white:borderw=5:bordercolor=black:x=(w-tw)/2:y=200[a];\
[1:v]fps=30,scale=1080:1920,setsar=1[b];[a][b]concat=n=2:v=1:a=0,noise=alls=3:allf=t,scale=out_range=tv,format=yuv420p[v];\
[2:a]afade=t=in:d=0.3,volume=0.9[m]" -map "[v]" -map "[m]" -shortest -c:v libx264 -profile:v main -crf 20 -preset slow -color_range tv -c:a aac -b:a 128k -ar 44100 \
-map_metadata -1 -fflags +bitexact -movflags +faststart $out
