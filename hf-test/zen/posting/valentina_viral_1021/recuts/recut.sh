#!/bin/bash
# recut.sh src out crop co_start co_end t1 t2 t2_at
set -e; F=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
src=$1; out=$2; crop=$3; a=$4; b=$5; printf '%b' "$6" > /tmp/t1.txt; printf '%b' "$7" > /tmp/t2.txt; at=$8
co=$(python3 -c "print(round($b-$a,3))")
ffmpeg -v error -y -i $src -filter_complex "[0:v]${crop}scale=1080:1920:flags=lanczos,setsar=1,fps=30,split[v1][v2];[v1]trim=$a:$b,setpts=PTS-STARTPTS[c];[v2]setpts=PTS-STARTPTS[m];[0:a]asplit[a1][a2];[a1]atrim=$a:$b,asetpts=PTS-STARTPTS,afade=t=out:st=$(python3 -c "print($co-0.08)"):d=0.08[ca];[a2]asetpts=PTS-STARTPTS[ma];[c][ca][m][ma]concat=n=2:v=1:a=1[vv][aa];[vv]unsharp=5:5:0.25,noise=alls=3:allf=t,drawtext=fontfile=$F:textfile=/tmp/t1.txt:fontsize=58:fontcolor=white:line_spacing=12:borderw=5:bordercolor=black@0.85:x=(w-text_w)/2:y=70:enable='lt(t,$at)',drawtext=fontfile=$F:textfile=/tmp/t2.txt:fontsize=58:fontcolor=white:line_spacing=12:borderw=5:bordercolor=black@0.85:x=(w-text_w)/2:y=70:enable='gte(t,$at)'[vo]" -map "[vo]" -map "[aa]" -c:v libx264 -profile:v main -pix_fmt yuv420p -crf 20 -preset slow -c:a aac -b:a 160k -movflags +faststart -map_metadata -1 $out
ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height -show_entries format=size,duration -of compact $out
