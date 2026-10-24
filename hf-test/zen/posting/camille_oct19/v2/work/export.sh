# export.sh in.mp4 out.mp4 "hook text"  -> 1080x1920 cover-crop, hook text 0-3s, H.264, no audio
IN=$1; OUT=$2; T="$3"
printf '%s' "$T" > /tmp/hook.txt
ffmpeg -v error -y -i "$IN" -an -vf "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,drawtext=fontfile='/usr/share/fonts/truetype/sand-box/google/Poppins/Poppins-SemiBold.ttf':textfile=/tmp/hook.txt:fontsize=50:fontcolor=white:borderw=5:bordercolor=black@0.85:x=(w-text_w)/2:y=h*0.17:enable='lt(t,3.5)'" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 24 -movflags +faststart "$OUT"
