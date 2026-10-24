# usage: dl.sh resultfile outdir suffix
grep -oE '^  [0-9]+,[^,]+,completed,image,seedream_v5_pro,"[^"]+"' $1 | while IFS= read -r l; do i=$(echo "$l"|sed 's/^ *//'|cut -d, -f1); u=$(echo "$l"|cut -d'"' -f2); curl -s -o $2/w$i$3.png "$u"; done
