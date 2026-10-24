cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
while ! grep -q Q16DONE v2/q16.log; do sleep 30; done
bash work/waitmem.sh; bash work/gateq.sh v2/k/k8_ft2.mp4; echo Q17DONE
