#!/bin/bash
# export.sh in.mp4 out_basename
set -e
IN=$1; OUT=$2; F=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
M=Bossa_Antigua.mp3; OFF=46.742
VF="scale=1084:1922:flags=lanczos,crop=1080:1920,setsar=1,noise=alls=3:allf=t,drawtext=fontfile='$F':text='Cartagena said one more day':fontsize=54:fontcolor=white:borderw=6:bordercolor=black@0.6:x=(w-text_w)/2:y=1560,drawtext=fontfile='$F':text='and I listened':fontsize=54:fontcolor=white:borderw=6:bordercolor=black@0.6:x=(w-text_w)/2:y=1635"
ffmpeg -v error -y -i $IN -ss $OFF -i $M -filter_complex "[0:v]$VF[v];[1:a]atrim=0:4.75,afade=t=in:d=0.15,afade=t=out:st=4.15:d=0.6,volume=0.9[a]" -map "[v]" -map "[a]" -c:v libx264 -profile:v main -pix_fmt yuv420p -crf 20 -maxrate 12M -bufsize 24M -r 24 -c:a aac -b:a 160k -shortest -movflags +faststart -map_metadata -1 ../final/$OUT.mp4
ffmpeg -v error -y -i $IN -f lavfi -i anullsrc=r=48000:cl=stereo -vf "scale=1084:1922:flags=lanczos,crop=1080:1920,setsar=1,noise=alls=3:allf=t" -c:v libx264 -profile:v main -pix_fmt yuv420p -crf 20 -maxrate 12M -bufsize 24M -c:a aac -shortest -movflags +faststart -map_metadata -1 ../final/${OUT}_silent.mp4
ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height -show_entries format=size,duration -of compact ../final/$OUT.mp4
