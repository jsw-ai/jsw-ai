import json,sys
FK="19afb002-3c36-48bf-be91-7591e4686ed1";R1="b9db2b67-be7a-4a9d-ae64-92c1ebbe8025";B2="dc5b25fc-9c7c-4616-9c2f-b9c4c6ce6a7c";BC="8fdd93c7-8a42-43cb-b2b5-77dcee23b7b8"
FACE="FACE LOCK: the woman's face must be exactly the face in photos 1 and 2 (same woman: same light green-hazel eyes, nose, lips, brow, jawline, face shape, very long dark brown wavy hair in a high ponytail); do not alter, beautify or restyle the face, keep her warm big friendly smile with visible teeth, and ignore any clothing or background in photos 1 and 2. "
BODY="BODY LOCK: the body must be an exact match of the figure in photos 3 and 4 (same woman): the same bust size and shape, narrow waist, flat toned stomach, wide curvy hips, same shoulder width, same slim athletic hourglass proportions and long toned legs; do NOT make her slimmer or flatter-chested than photos 3 and 4, keep the bust the same size even under clothing. Use only the body, never the outfits, of photos 3 and 4. Her skin is a deep golden-bronze sun-kissed tan exactly like photos 3 and 4, NOT pale. "
TAIL=" Warm golden-hour sun with slight haze, low contrast, no blown highlights. Candid unposed phone photo taken by a friend, visible natural skin texture and pores, tiny freckles, flyaway hair strands, matte unretouched skin, no glossy sheen, no airbrushing. Shot on iPhone, framed head to mid-thigh with headroom, nobody else anywhere in the frame, no text, no logos, natural hands with five fingers."
S={
1:"Scene: empty sand beach volleyball court at golden hour with a net behind her, she wears a fitted white scoop-neck athletic top and black bike shorts, holding a plain volleyball on her hip, laughing with a big open smile at the camera.",
2:"Scene: sunny outdoor table at a juice bar with nobody else around, she wears a fitted coral scoop-neck tank and denim shorts, holding a purple açaí bowl topped with banana slices and granola and a spoon, big happy smile at the camera.",
3:"Scene: sunny backyard patio with a charcoal grill and skewers of grilled meat, a brazilian Sunday churrasco feel, no other people, she wears a fitted yellow scoop-neck tee and white linen shorts, holding a skewer and tongs, big joyful smile at the camera.",
4:"Scene: empty palm-lined Miami sidewalk near the beach, pastel buildings with no signs or cars, she wears a fitted green wrap-style scoop-neck top and light denim shorts with a small tote bag, walking toward the camera with a big bright smile, hair in a ponytail swinging.",
5:"Scene: bright home kitchen in São Paulo style with tile backsplash, nobody else, she wears a fitted cobalt-blue scoop-neck top and cream shorts, holding a tray of freshly baked pão de queijo cheese bread and smiling big at the camera, warm window light.",
6:"Scene: empty beach at sunset, she wears a white scoop-neck crop top and light linen shorts, barefoot with flip-flops in one hand, a plain volleyball tucked under the other arm, walking along the wet sand and smiling widely at the camera.",
}
def R(ks):
    return [{"index":k,"params":{"model":"seedream_v5_pro","prompt":S[k]+" "+FACE+BODY+TAIL,"aspect_ratio":"3:4","count":1,"medias":[{"value":m,"role":"image_references"} for m in [FK,R1,B2,BC]]}} for k in ks]
if __name__=="__main__":
    json.dump(R([int(x) for x in sys.argv[1:]] or list(S)),open('requests.json','w'))
