import json
HEAD="Candid iphone photo of the woman from photo 1 (keep her exact face, long wavy darker golden-brown hair with honey highlights, warm brown eyes, warm wide smile with teeth, even golden tan). Take the body exactly from photo 2: very full, large rounded bust as full as photo 2, clearly fuller than a slim model, narrow waist, flat toned stomach, wide curvy hips, long toned legs. "
TAIL=" Natural skin texture with visible pores, no retouching, no text, no logos, no other people anywhere, empty background. Head to mid-thigh visible, face fully in frame with headroom, camera at eye level, front or three-quarter angle."
S={
"n1":"She wears a fitted navy scoop-neck tee (plain, no logo) and high-waist light jeans, holding an iced coffee, standing on an empty elevated park walkway in New York with greenery, soft overcast daylight, laughing.",
"n2":"She wears a black fitted scoop-neck sports bra and black high-waist leggings, standing on a yoga mat in an empty bright pilates studio with a plain wall and a reformer behind, hands on hips, big smile.",
"n3":"She wears a fitted white scoop-neck top and light blue jeans, seated at a small empty cafe table by a window with an iced coffee and a plate of pancakes, leaning on one hand, natural window light, wide shot from across the table.",
"n4":"She wears a red two-piece bikini and light denim shorts, standing on an empty rooftop terrace with wooden deck and city skyline behind at golden hour, one hand pushing hair back, smiling.",
"n5":"She wears a fitted plain navy scoop-neck tee and grey joggers, sitting on a living room sofa with a bowl of popcorn, a TV glowing softly behind, cheering with a fist raised, evening lamp light.",
"n6":"She wears a fitted tan scoop-neck tank top, denim shorts and brown cowboy boots, standing on a sunny wooden porch with a plain white railing and trees behind, hand on the railing, smiling.",
"n7":"She wears a fitted black scoop-neck long-sleeve top and dark jeans, holding an iced coffee, standing on an empty New York brick-lined sidewalk in soft autumn light, walking toward camera, laughing.",
"n8":"She wears a navy sporty bikini top and matching bikini bottoms, standing on an empty sandy beach path with dune grass and ocean behind, bright sun, hand shading her eyes, smiling.",
}
json.dump({k:HEAD+v+TAIL for k,v in S.items()},open('/workspace/hf-test/zen/posting/madison_test/prompts_r3.json','w'),indent=1)
