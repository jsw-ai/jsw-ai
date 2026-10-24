import json
SKIN="Raw unretouched amateur phone photo taken by a friend, shot on iPhone, no beauty filter, no smoothing, no airbrushing, visible pores, fine lines, faint redness around the nose, small freckles across nose and cheeks, uneven skin tone, tiny blemishes, peach fuzz, mild shine only on nose and forehead, matte skin, slight asymmetry, minimal makeup, flyaway frizzy hair strands, soft phone-camera softness and light noise. Warm backlit golden-hour sun, slight haze, low contrast, soft light, no blown highlights, no studio light, not bright even daylight."
BODY="Very full large rounded bust that clearly fills the top, narrow waist, wide curvy hips, soft natural curvy build, not skinny, not athletic, warm light-tan golden-brown skin."
FRAME="Face large in frame (about half the frame height), generous headroom, head to waist visible, front view, off-centre, no text, no other people, natural relaxed hands."
base="A real woman in her mid 20s with long black curly hair (frizzy, flyaway), dark brown eyes, "
P={
1:base+"slightly round soft face, full natural brows, fuller lips, broad nose, gentle half-smile. Sitting at a cafe table by a window in a black ribbed scoop-neck top.",
2:base+"oval face with high cheekbones, slightly thick straight brows, small gap in front teeth showing in a laughing smile. Standing on a sunny balcony in a fitted cream scoop-neck tank top.",
3:base+"heart-shaped face, soft jaw, arched brows, small beauty mark on cheek, calm closed-mouth smile. Standing in a park path at golden hour in a fitted dark green scoop-neck top.",
4:base+"longer face with a defined chin, strong dark brows, slightly hooded eyes, wide natural smile with teeth. Sitting on a sofa at home with late sun through the window, fitted rust-orange scoop-neck top.",
5:base+"round cheeks, button nose, light dimples, freckled, soft smile looking just past the camera. Standing against a plain warm wall outdoors in a fitted white scoop-neck top and light jeans.",
6:base+"strong soft jawline, full cheeks, medium-wide nose, dark lashes, relaxed neutral expression with a slight smirk. Leaning on a railing by the sea at sunset in a fitted navy scoop-neck top.",
}
print(json.dumps({k:v+" "+BODY+" "+FRAME+" "+SKIN for k,v in P.items()}))
