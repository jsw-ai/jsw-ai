n=$1; base=$2; T2=../valentina_test2/fin; mkdir -p frames/$n
i=0; for t in 0.1 1 2 3 4 4.9; do ffmpeg -loglevel error -y -ss $t -i raw/$n.mp4 -frames:v 1 frames/$n/f$i.jpg; i=$((i+1)); done
ffmpeg -loglevel error -y -ss 2.5 -i final/$n.mp4 -frames:v 1 frames/${n}_mid.jpg
ffmpeg -loglevel error -y -i $T2/$base -i $T2/s1_a_v4C.jpg -i $T2/s4_a_v4C.jpg -i ../valentina_refs/valentina_cover.jpg -i ../valentina_refs/valentina_bikini1.jpg -i stills/${n}_a.png \
 -i frames/$n/f0.jpg -i frames/$n/f1.jpg -i frames/$n/f2.jpg -i frames/$n/f3.jpg -i frames/$n/f4.jpg -i frames/$n/f5.jpg -filter_complex \
"$(for k in $(seq 0 11); do printf "[$k]scale=360:480:force_original_aspect_ratio=decrease,pad=360:480:(ow-iw)/2:(oh-ih)/2[i$k];"; done)[i0][i1][i2][i3][i4][i5]hstack=6[top];[i6][i7][i8][i9][i10][i11]hstack=6[bot];[top][bot]vstack" qc/${n}_qc.jpg
