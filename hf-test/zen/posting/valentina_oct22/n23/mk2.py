import json,re
exec(open('mk.py').read().split('S={')[0])
N=" The neckline is a moderate scoop (or moderate square) that ends well above the bust: collarbones and upper chest visible, no cleavage visible at all, not a crew neck, not a high neck. Bright soft open shade on her face, evenly lit from the front."
S={
1:"Change her outfit to a white cotton peasant blouse with a moderate square neckline, standing in a colonial Cartagena room with tall open blue wooden shutters and a mustard-yellow wall behind her.",
2:"Change her outfit to a soft yellow fitted top with a moderate scoop neckline, holding a plain blank vinyl record sleeve with no print at chest height in both hands, in a sunny bedroom with a record player behind her.",
3:"Change her outfit to a cobalt-blue cotton sundress with a moderate square neckline and wide straps, standing in the shade of a colonial balcony in old-town Cartagena with pink bougainvillea and a painted wall behind her.",
4:"Change her outfit to a white fitted short-sleeve top with a moderate scoop neckline, standing in open shade against a pink colonial wall with a green wooden door in Cartagena, empty street.",
5:"Change her outfit to a peach fitted short-sleeve top with a moderate scoop neckline, standing in a bright home kitchen holding a small white cafecito cup at chest height.",
6:"Change her outfit to a navy fitted short-sleeve tee with a moderate scoop neckline and white shorts, standing in the shade of palm trees on an empty Miami beach boardwalk with the ocean behind her.",
7:"Change her outfit to a black fitted short-sleeve tee with a moderate scoop neckline, with over-ear headphones around her neck, standing in a small empty home music studio with a microphone behind her.",
8:"Change her outfit to a lilac fitted top with a moderate square neckline and wide straps, standing on a balcony at dusk with warm string lights behind her and soft warm light evenly on her face.",
9:"Change her outfit to a sage-green cotton sundress with a moderate square neckline and wide straps, standing in an empty lush garden with tropical plants behind her.",
10:"Change her outfit to a light denim short-sleeve top with a moderate scoop neckline, standing in a bright bedroom with a mirror and plants behind her.",
11:"Change her outfit to a blue-and-white striped fitted top with a moderate square neckline, standing in open shade on an empty palm-lined Miami street with pastel houses behind her.",
12:"Change her outfit to a black fitted tank top with a moderate scoop neckline and grey joggers, standing in an empty bright dance studio with a wall mirror and wooden floor behind her.",
}
R=[{"index":100+k,"params":{"model":"seedream_v5_pro","prompt":H+v+N+T,"aspect_ratio":"9:16","resolution":"2k","medias":[{"value":"d3329ec2-585c-4cb9-84a8-0f441f48a3de","role":"image_references"}]}} for k,v in S.items()]
json.dump({"requests":R},open('batchB.json','w'))
print(R[0]['params']['prompt'])
