import json
FREEZE=("Take the face exactly from photo 1: same facial structure, eyes, nose, lips, jaw, brows and blonde braided hair as photo 1. Body proportions as in photo 2 (full natural rounded C-cup bust, slim toned waist, flat stomach with light ab definition, curvy hips, slim athletic hourglass build, long toned legs, even golden tan). Candid unedited iPhone 26mm photo, face fully in frame with generous headroom above the head, matte unretouched skin with visible pores, mild natural asymmetry, light natural tan, minimal makeup, phone noise, not glossy, no text, no other people.")
S={3:"New scene: sitting at a cafe table with an iced coffee, black ribbed scoop-neck top, window light, front view, off-centre.",
5:"New scene: standing by a plain white wall in a simple navy scoop-neck one-piece swimsuit, front view, flat natural daylight, off-centre.",
6:"New scene: on a quiet sandy beach in a plain white bikini top and denim shorts, three-quarter view, overcast flat light, off-centre."}
print(json.dumps({k:v+" "+FREEZE for k,v in S.items()}))
