import json
COMMON=("Take the face and identity from photo 1 (same woman: long wavy brown hair, hazel-brown eyes, freckles across nose and cheeks, same smile). Take the body exactly from photo 2: very full, large rounded bust as full as photo 2, clearly fuller than a slim model, narrow waist, wide curvy hips, not skinny. Her skin is a golden sun-kissed tan exactly like the reference, warm, not pale. Raw unretouched amateur phone photo taken by a friend, no beauty filter, no smoothing, no airbrushing, visible pores, fine lines, tiny freckles, uneven skin tone, flyaway hair strands, matte not glossy, mild shine only on nose and forehead, flat ordinary light, warm backlit golden-hour sun, slight haze, low contrast, no blown highlights, phone noise. Wider shot from head to mid-thigh, face not too large in frame, generous headroom above her head, she is alone, no text or logos anywhere.")
S=[
"Scene: sitting at a sunny cafe terrace table with an iced latte, wearing a fitted black scoop-neck top and jeans, smiling at camera.",
"Scene: walking along a sandy beach boardwalk, wearing a terracotta two-piece bikini, hair blowing slightly, laughing.",
"Scene: standing on a small city balcony with plants at golden hour, wearing a fitted cream scoop-neck top and denim shorts, hand in her hair, smiling.",
"Scene: strolling on a park path under trees, wearing a fitted white scoop-neck top and a light linen skirt, looking at camera with a relaxed smile.",
"Scene: standing in a bright home kitchen holding a coffee mug, wearing a fitted sage-green scoop-neck top and leggings, warm window light, smiling.",
"Scene: sitting on a sofa by a big window, wearing a fitted heather-grey scoop-neck tank top and soft shorts, leaning forward laughing.",
"Scene: walking down a quiet sunlit city street, wearing a fitted navy scoop-neck top and high-waisted jeans, glancing at camera and smiling.",
"Scene: sitting on the edge of a swimming pool deck with legs in the water, wearing a sage-green two-piece bikini, big smile, water glints.",
]
P=[s+" "+COMMON for s in S]
json.dump(P,open('prompts.json','w'))
open('prompts.txt','w').write("\n\n".join(f"c{i+1}: {p}" for i,p in enumerate(P)))
