#!/bin/bash
# contact sheet of 6 frames
f=$1; o=${f%.mp4}_qs.jpg
ffmpeg -loglevel error -y -i $f -vf "fps=1.2,scale=240:-2,tile=6x1" -frames:v 1 $o; echo $o
