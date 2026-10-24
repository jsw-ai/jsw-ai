# ev.sh name -> processed temp + drift 0.25
n=$1; ffmpeg -v error -y -i kl/$n.mp4 -vf "scale=1080:1920:flags=lanczos,unsharp=5:5:0.3,noise=alls=3:allf=t,fps=30,format=yuv420p" -c:v libx264 -crf 17 -an ed/p_$n.mp4
/workspace/.face-venv/bin/python /workspace/music/sienna/low_tide_lover/sample/valentina_method/qa/drift.py ed/p_$n.mp4 0.25 10 qc/dp_$n.json 2>&1 | grep -E "^[0-9]" | awk -v n=$n 'BEGIN{printf n" "} {printf "%s:%s ",$1,$2}'; echo
