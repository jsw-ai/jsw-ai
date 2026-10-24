#!/bin/bash
# cut.sh out mus mss hook1 hook2 t_switch  src1 ss1 dur1 src2 ss2 dur2 ...
set -e
out=$1; mus=$2; mss=$3; h1=$4; h2=$5; tsw=$6; shift 6
F=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
ins=""; fc=""; n=0; tot=0
while [ $# -gt 0 ]; do ins="$ins -ss $2 -t $3 -i $1"; fc="$fc[$n:v]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[v$n];"; tot=$(python3 -c "print($tot+$3)"); n=$((n+1)); shift 3; done
cc=""; for i in $(seq 0 $((n-1))); do cc="$cc[v$i]"; done
ffmpeg -y -loglevel error -threads 2 $ins -ss $mss -i $mus -filter_complex "$fc${cc}concat=n=$n:v=1:a=0,drawtext=fontfile=$F:textfile=$h1:fontsize=58:fontcolor=white:borderw=5:bordercolor=black:x=(w-tw)/2:y=260:enable='lt(t,$tsw)',drawtext=fontfile=$F:textfile=$h2:fontsize=58:fontcolor=white:borderw=5:bordercolor=black:x=(w-tw)/2:y=260:enable='gte(t,$tsw)',noise=alls=3:allf=t,format=yuv420p[v];[$n:a]afade=t=in:d=0.3,afade=t=out:st=$(python3 -c "print($tot-0.5)"):d=0.5,volume=0.9[m]" -map "[v]" -map "[m]" -t $tot -c:v libx264 -profile:v main -crf 20 -preset medium -c:a aac -b:a 128k -ar 44100 -map_metadata -1 -fflags +bitexact -movflags +faststart $out
md5sum $out
