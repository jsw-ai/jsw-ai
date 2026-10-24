# pf.sh name : 4 fps per-frame centroid
cd /workspace/hf-test/zen/posting/camille_oct20; N=$1; D=frames/pf_$N; mkdir -p $D; rm -f $D/*
ffmpeg -v error -i raw/$N.mp4 -vf fps=4 $D/%03d.png
/workspace/.face-venv/bin/python ../identity_gate.py img --model camille_v3_draft $D/*.png 2>/dev/null | rg -o "^(PASS|FAIL) \S+|score_centroid': [0-9.None]+" | paste - - | awk '{split($2,a,".");printf "%.2fs %s %s\n",(a[1]-1)/4,$1,$4}' | tr '\n' ' '; echo
