import json
ID="A strikingly beautiful woman in her mid 20s with mixed heritage, warm olive-tan glowing skin, tight defined tidy black ringlet curls (springy coiled ringlets, shoulder length, well-shaped), large bright expressive dark brown eyes with long lashes, defined high cheekbones, balanced symmetrical features, soft straight nose, full natural lips, strong dark shaped brows. "
BODY="Fit toned shapely hourglass figure with a narrow waist, rounded hips, toned arms, and a moderate-to-full proportionate bust (not oversized), natural healthy proportions, neither skinny nor heavy. Fitted flattering outfit with a modest scoop neckline. Framed from head to mid-thigh, face large with headroom, flattering slightly-above eye-level angle, hands out of frame or relaxed at sides with correct fingers. "
SKIN="Healthy radiant luminous skin with a soft natural sheen and warm glow, light freckles across nose and cheeks, natural skin texture, subtle makeup with soft lip color, no heavy gloss. Candid phone photo shot on iPhone, warm golden-hour backlight with soft rim glow and gentle haze, low contrast, no blown highlights, not airbrushed, not plastic, no red shiny nose, no text, nobody else in frame."
sc=[
("Smiling warmly at the camera, standing on a sunlit rooftop terrace at golden hour, fitted rust-orange scoop-neck top and high-waisted cream trousers."),
("Confident soft gaze with a slight smile, leaning against a warm plaster wall outdoors, fitted emerald green scoop-neck top and light jeans."),
("Laughing softly, standing in a park with trees glowing behind, fitted white ribbed scoop-neck tank and denim shorts."),
("Slight smile, chin slightly lowered, by a seaside railing at sunset, fitted dusty-rose scoop-neck top and black high-waisted skirt."),
("Bright open smile, in a sunlit apartment by a large window, fitted cobalt blue scoop-neck knit top and light jeans."),
("Confident calm look with a hint of a smile, on a quiet city street at golden hour, fitted black scoop-neck bodysuit top and olive trousers."),
]
reqs=[{"index":i+1,"params":{"model":"seedream_v5_pro","prompt":ID+s+" "+BODY+SKIN,"aspect_ratio":"3:4","resolution":"2k","use_unlim":False}} for i,s in enumerate(sc)]
json.dump({"requests":reqs},open("req3.json","w"))
