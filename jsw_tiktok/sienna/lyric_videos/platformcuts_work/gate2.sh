set -e
for j in B_igstory_u2 B_x_u2; do
 mkdir -p gate_$j; [ -n "$(ls gate_$j 2>/dev/null)" ] || python3 - $j <<'P'
import json,sys,subprocess
j=sys.argv[1];d=json.load(open(j+'.json'));fw=d['face_windows'];N=16;tot=sum(b-a for a,b in fw);ts=[]
for a,b in fw:
  n=max(1,round(N*(b-a)/tot)); ts+=[a+(b-a)*(i+0.5)/n for i in range(n)]
for k,t in enumerate(ts[:N]):
  subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t:.2f}','-i',d['out'],'-frames:v','1','-q:v','2',f'gate_{j}/f{k+1:02d}_t{t:.2f}.jpg'],check=True)
P
 while [ $(free -g | awk '/Mem/{print $7}') -lt 3 ]; do sleep 20; done
 free -g | awk '/Mem/{print "avail",$7}'
 (cd /workspace/hf-test/zen/posting && /workspace/.face-venv/bin/python identity_gate.py img --model sienna --source seedream --no-ocr --json /workspace/jsw_tiktok/sienna/lyric_videos/platformcuts_work/gate_$j.json /workspace/jsw_tiktok/sienna/lyric_videos/platformcuts_work/gate_$j/*.jpg > /workspace/jsw_tiktok/sienna/lyric_videos/platformcuts_work/gate_$j.log 2>&1)
done
