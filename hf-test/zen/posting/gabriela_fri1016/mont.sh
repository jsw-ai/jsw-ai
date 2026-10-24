# usage: mont.sh out dur "img|caption" ...
out=$1; d=$2; shift 2; i=0; list=""
FONT=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
for a in "$@"; do img=${a%%|*}; cap=${a#*|}
 n=$((d*25))
 if [ $((i%2)) = 0 ]; then Z="1+0.0014*on"; else Z="1.28-0.0014*on"; fi
 ffmpeg -y -loglevel error -loop 1 -i ../gabriela_w1/final/g_$img.jpg -vf "scale=-2:1920,crop=1080:1920,scale=2160:3840,zoompan=z='$Z':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$n:s=1080x1920:fps=25,drawtext=fontfile=$FONT:text='$cap':fontsize=64:fontcolor=white:borderw=5:bordercolor=black@0.8:x=(w-text_w)/2:y=300,format=yuv420p" -frames:v $n -c:v libx264 -crf 20 seg$i.mp4
 echo "file seg$i.mp4" >> l.txt; i=$((i+1)); done
ffmpeg -y -loglevel error -f concat -i l.txt -c copy $out; rm -f seg*.mp4 l.txt
