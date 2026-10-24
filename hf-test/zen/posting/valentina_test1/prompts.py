FREEZE=("Take the face exactly from photo 1: same facial structure, dark brown eyes, nose, lips, wide smile, jaw, brows and long dark wavy hair as photo 1. "
"Body proportions as in photo 2: slim toned hourglass figure, defined waist, rounded hips, slim toned legs, warm olive tan skin. "
"Candid unedited iPhone 26mm photo, face fully in frame with headroom above the head, matte unretouched skin with visible pores, mild natural asymmetry, light natural tan, minimal makeup, phone noise, not glossy, no text, no other people, empty background.")
SC={
1:"New scene: she sits at a small cafe table by a window with a coffee cup, wearing a plain white tee and light jeans, front angle, relaxed wide smile, waist-up.",
2:"New scene: she stands on an apartment balcony in morning light, wearing a plain fitted grey tank top and jeans, 3/4 angle, looking at camera with a wide smile, head to hips visible.",
3:"New scene: she walks along an empty sandy beach path with dune grass, wearing a plain linen shirt over a simple black one-piece swimsuit, 3/4 angle, laughing, head to mid-thigh visible.",
4:"New scene: she stands in a living room, wearing a plain black t-shirt tucked into blue jeans, front angle, shoulders square to camera, wide smile, head to knees visible.",
5:"New scene: she stands by a pool edge on a sunny day wearing a plain navy one-piece swimsuit, front angle, shoulders square, wide smile, head to mid-thigh visible, nobody else around.",
6:"New scene: she stands on a quiet park path under trees wearing a plain olive sundress, 3/4 angle, wide smile, head to knees visible.",
7:"New scene: she sits on a sofa at home wearing a cream knit sweater and jeans, front angle, holding a phone, relaxed smile, waist-up.",
8:"New scene: she stands in a kitchen leaning on the counter wearing a plain white fitted tee and denim shorts, front angle, wide smile, head to mid-thigh visible.",
}
def p(i): return SC[i]+" "+FREEZE
