# usage: finish.sh k raw.mp4 hook_end
k=$1; raw=$2; he=${3:-3.5}
python3 -c "
exec(open('texts.py').read()); a,b=T['$k']; open('${k}_h.txt','w').write(a); open('${k}_p.txt','w').write(b)"
F=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
ffmpeg -v error -y -i $raw -vf "scale=1080:1920:flags=lanczos,unsharp=5:5:0.3,noise=alls=3:allf=t,drawtext=fontfile=$F:textfile=${k}_h.txt:fontsize=54:fontcolor=white:borderw=4:bordercolor=black@0.85:line_spacing=10:x=(w-text_w)/2:y=50:enable='lt(t,$he)',drawtext=fontfile=$F:textfile=${k}_p.txt:fontsize=54:fontcolor=white:borderw=4:bordercolor=black@0.85:line_spacing=10:x=(w-text_w)/2:y=50:enable='gte(t,$he)'" -c:v libx264 -crf 19 -preset slow -pix_fmt yuv420p -c:a aac -b:a 160k -map_metadata -1 -fflags +bitexact -flags:v +bitexact -flags:a +bitexact -movflags +faststart ../final/$k.mp4
