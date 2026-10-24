#!/bin/bash
cd /workspace/hf-test/zen/posting/gabriela/2026-10-22
for f in "$@"; do bash work/waitmem.sh || { echo TIMEOUT; exit 1; }; echo "$(date +%T) gate $f"; GFPS=${GFPS:-12} work/pf_gate.py "$f"; done; echo QDONE
