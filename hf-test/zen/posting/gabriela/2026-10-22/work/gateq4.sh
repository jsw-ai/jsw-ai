#!/bin/bash
cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
while ! grep -qE "Q3DONE|TIMEOUT" work/gateq3.log; do sleep 20; done
bash work/gateq.sh collab/gabriela_collab_oktoberfest_saude_v3_silent.mp4; echo Q4DONE
