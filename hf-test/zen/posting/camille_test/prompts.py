import json
FREEZE=("Take the face exactly from photo 1: same facial structure, brown eyes, nose, lips, jaw, brows and long black curly hair as photo 1. Body proportions as in photo 2 (full natural rounded bust that clearly fills the top, slim toned waist, curvy hips, slim athletic hourglass build, long toned legs, warm golden-brown tan). Candid unedited iPhone 26mm photo, face fully in frame with generous headroom above the head, matte unretouched skin with visible pores, mild natural asymmetry, light natural tan, minimal makeup, phone noise, not glossy, no text, no other people.")
S={1:"New scene: sitting at a cafe table with an iced coffee, black ribbed scoop-neck top, window light, front view, off-centre, head to waist visible.",
2:"New scene: standing in a bright home kitchen in a fitted white tee and jeans, front view, flat natural daylight, off-centre, head to mid-thigh visible.",
3:"New scene: on a sunny balcony in a fitted olive tank top and denim shorts, three-quarter view, soft daylight, head to mid-thigh visible.",
4:"New scene: standing by a plain white wall in a simple navy scoop-neck one-piece swimsuit, front view, flat natural daylight, off-centre, head to mid-thigh visible.",
5:"New scene: park path in the shade in a casual cream cardigan over a fitted tank top and leggings, laughing, three-quarter view, head to hips visible.",
6:"New scene: sitting on a sofa at home in a fitted heather-grey crop sweatshirt and joggers, front view, lamp and window light, head to knees visible."}
print(json.dumps({k:v+" "+FREEZE for k,v in S.items()}))
