import json
exec(open('mk.py').read().split('S={')[0])
N=" The neckline is a gentle moderate scoop (or moderate square) that sits high, ending well above the bust line: collarbones visible, fabric fully covering the chest, absolutely no cleavage visible, not a crew neck, not a high neck. Bright soft open shade on her face, evenly lit from the front."
S={
1:"Change her outfit to a white linen short-sleeve blouse with a moderate square neckline, standing in front of a bright yellow colonial wall with a wooden balcony in old-town Cartagena, empty street, holding a plain blank CD case with no print at waist height.",
2:"Change her outfit to a terracotta fitted short-sleeve top with a moderate scoop neckline, sitting on the steps of a colonial church plaza in Cartagena in open shade, empty plaza.",
3:"Change her outfit to a cream knit short-sleeve top with a moderate scoop neckline, standing in a sunny cafe interior holding a small coffee cup at chest height, empty cafe.",
4:"Change her outfit to a red fitted short-sleeve top with a moderate square neckline, standing in front of an empty colorful graffiti mural wall in Getsemani, Cartagena, in open shade.",
5:"Change her outfit to an olive-green fitted short-sleeve top with a moderate scoop neckline, standing in an empty home recording booth with a studio microphone beside her, wearing over-ear headphones on her head.",
6:"Change her outfit to a white fitted short-sleeve tee with a moderate scoop neckline and a light denim jacket worn open, standing on an empty Miami street at golden hour with soft light evenly on her face.",
7:"Change her outfit to a pastel pink fitted short-sleeve top with a moderate scoop neckline, standing in a bright kitchen with fresh mangoes on the counter behind her.",
8:"Change her outfit to a mustard-yellow fitted short-sleeve top with a moderate square neckline, standing among tall palm trees in an empty park in open shade.",
9:"Change her outfit to a light grey fitted short-sleeve tee with a moderate scoop neckline, sitting on a bed in a bright bedroom holding a phone, smiling.",
10:"Change her outfit to a turquoise fitted short-sleeve top with a moderate scoop neckline, standing on the old city walls of Cartagena with the sea behind her, open shade, empty.",
11:"Change her outfit to a soft white fitted short-sleeve top with a moderate scoop neckline and black joggers, standing in an empty bright dance studio with a wall mirror behind her, mid-laugh.",
12:"Change her outfit to a burgundy fitted short-sleeve top with a moderate square neckline, standing at an empty outdoor market stall with colorful fruit behind her, open shade.",
}
R=[{"index":200+k,"params":{"model":"seedream_v5_pro","prompt":H+v+N+T,"aspect_ratio":"9:16","resolution":"2k","medias":[{"value":"d3329ec2-585c-4cb9-84a8-0f441f48a3de","role":"image_references"}]}} for k,v in S.items()]
json.dump({"requests":R},open('batchC.json','w'))
