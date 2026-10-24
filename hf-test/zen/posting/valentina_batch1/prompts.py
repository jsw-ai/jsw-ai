import json
FREEZE=("Take the face exactly from photo 1: same facial structure, dark brown eyes, nose, lips, wide smile, jaw, brows and long dark wavy hair as photo 1. "
"Take the body from photo 2: slim toned hourglass figure, defined waist, rounded hips, slim toned legs, but with a slightly larger, fuller and perkier, naturally lifted bust than photo 2, clearly not flat or skinny, natural proportions. Warm olive tan skin like photo 2, NOT pale, NOT desaturated, even indoors. "
"Raw unretouched candid iPhone photo taken by a friend, warm backlit soft golden light, slight haze, low contrast, no blown highlights, face fully in frame with headroom above the head, natural skin with visible pores, peach fuzz, tiny freckles and small skin marks, uneven tone, flyaway hair, matte not airbrushed, no beauty filter, no glossy sheen, phone noise, no text or logos, she is completely alone, no other people anywhere, empty background.")
SC={
1:"New scene: she stands in an empty bright home-gym corner with a rubber floor and dumbbells on a rack, wearing a fitted black scoop-neck sports top and black high-waist leggings, hair in a loose ponytail, holding a water bottle, front angle, shoulders square, wide smile, head to knees visible.",
2:"New scene: early morning at a quiet farmers market stall with crates of oranges and tomatoes (nobody else around), she holds a canvas tote with produce, wearing a fitted white scoop-neck tank top and light blue jeans, front angle, shoulders square, wide smile, head to hips visible, sun backlighting her hair.",
3:"New scene: she walks on an empty waterfront promenade at sunset, golden sun low behind her, wearing a fitted ribbed cream scoop-neck tank top and high-waist loose linen trousers, front angle, glancing at camera with a wide smile, head to knees visible.",
4:"New scene: car selfie, she sits in the driver seat of a parked car with the seatbelt on, phone held at arm's length at chest height, wearing a fitted scoop-neck dark green top, warm golden light through the window, relaxed wide smile, head to waist visible, nobody else in or around the car.",
5:"New scene: brunch on an empty sunny cafe patio table with a plate of avocado toast and a glass of orange juice, wearing a fitted terracotta scoop-neck knit top, front angle, laughing with a wide smile, head to waist visible, warm light behind her, no other diners.",
6:"New scene: she stands in an aisle of an empty cozy bookstore holding an open book, wearing an open oatmeal cardigan over a fitted white scoop-neck tank top and jeans, warm lamp light from behind, front angle, wide smile looking at camera, head to hips visible, no readable text.",
7:"New scene: she sits on a white pool lounger on a sunny day, nobody else around, wearing a modest plain dark emerald one-piece swimsuit with a scoop neckline, front angle, shoulders square, wide smile, head to mid-thigh visible, warm low sun behind her.",
8:"New scene: home workout in a sunlit living room, she stands next to a rolled-out yoga mat holding a water bottle, wearing a fitted lavender scoop-neck sports top and matching high-waist leggings, front angle, shoulders square, flushed relaxed wide smile, head to knees visible, warm window light behind.",
}
def p(i): return SC[i]+" "+FREEZE
if __name__=="__main__":
    json.dump({i:p(i) for i in SC},open('prompts.json','w'),indent=1)
