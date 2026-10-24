#!/bin/bash
# usage: fin_v2.sh in.mp4 audio.mp3 "caption" out.mp4 ss dur [lyric_text lyric_start]
in=$1; au=$2; cap=$3; out=$4; ss=$5; d=$6; ly=$7; lys=$8
F=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
vf="trim=start=$ss:duration=$d,setpts=PTS-STARTPTS,fps=30,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920${DELOGO:+,delogo=$DELOGO},noise=alls=6:allf=t,drawtext=fontfile=$F:text='$cap':fontsize=58:fontcolor=white:borderw=4:bordercolor=black@0.85:x=(w-tw)/2:y=270"
if [ -n "$ly" ]; then printf "%s" "$ly" > /tmp/ly_$$.txt; vf="$vf,drawtext=fontfile=$F:textfile=/tmp/ly_$$.txt:fontsize=60:line_spacing=10:fontcolor=white:borderw=4:bordercolor=black@0.85:x=(w-tw)/2:y=860:enable='gte(t,$lys)'"; fi
ffmpeg -loglevel error -y -i "$in" -i "$au" -filter_complex "[0:v]$vf[v];[1:a]atrim=0:$d,asetpts=PTS-STARTPTS,afade=t=out:st=$(awk -v d=$d "BEGIN{print d-0.3}"):d=0.3[a]" -map "[v]" -map "[a]" -c:v libx264 -profile:v main -pix_fmt yuv420p -crf 20 -preset slow -c:a aac -b:a 192k -ar 48000 -map_metadata -1 -fflags +bitexact -movflags +faststart -t $d "$out"
ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height:format=duration,size -of compact "$out"
