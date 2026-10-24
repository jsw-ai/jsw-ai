#!/bin/bash
# usage: post.sh tag model file schedISO platformsJSON caption title
set -e
S=/home/box/agent-data/secrets; K=$(cat $S/JSW-ayrshare-api-key.txt)
tag=$1 m=$2 f=$3 sd=$4 pl=$5 cap=$6 title=$7
[ -f "$f" ] || { echo "MISSING $f"; exit 1; }
PK=(); [ "$m" != sienna ] && PK=(-H "Profile-Key: $(cat $S/JSW-$m-ayrshare-profile-key.txt)")
u=$(curl -s -H "Authorization: Bearer $K" "${PK[@]}" "https://api.ayrshare.com/api/media/uploadUrl?fileName=$(basename $f)&contentType=mp4")
up=$(jq -r .uploadUrl <<<"$u"); acc=$(jq -r .accessUrl <<<"$u")
[ "$up" != null ] || { echo "UPLOADURL FAIL $(jq -c 'del(.uploadUrl)' <<<"$u")"; exit 1; }
curl -sf -X PUT -H "Content-Type: video/mp4" --upload-file "$f" "$up" >/dev/null || { echo PUT FAIL; exit 1; }
body=$(jq -n --arg p "$cap" --arg u "$acc" --arg sd "$sd" --argjson pl "$pl" --arg t "$title" '{post:$p,platforms:$pl,mediaUrls:[$u],isVideo:true,scheduleDate:$sd,
 tikTokOptions:{isAIGenerated:true}, instagramOptions:{isAIGenerated:true,shareReelsFeed:true},
 youTubeOptions:{title:$t,containsSyntheticMedia:true,shorts:true,visibility:"public"}}')
r=$(curl -s -X POST -H "Authorization: Bearer $K" "${PK[@]}" -H "Content-Type: application/json" -d "$body" https://api.ayrshare.com/api/post)
echo "$r" > res_$tag.json
echo "$tag $(jq -c '{status,id,scheduleDate,errors:[.errors[]?|{platform,message}],warnings}' <<<"$r")"
