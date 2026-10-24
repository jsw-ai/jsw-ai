import json
FK="5e2fc02d-f686-45bc-a6be-84836df5882f";FC="2752bdf5-7a66-46ed-83b1-9520474ec0f6";F6="03124490-bf76-4b18-9807-6c574973c4dc"
B4="f33b193c-ca5b-4f36-b909-4611ef9bd059";B7="096115b9-1982-4e2b-8bd5-933ff0373af8"
FACE="FACE LOCK: the woman's face must be exactly the face in photos 1 and 2 (same woman: same light green-hazel eyes, same nose, lips, brow, jawline and face shape, same very long dark brown wavy hair); do not alter, beautify or restyle the face, change ONLY the expression and head angle as described, and ignore any clothing or background in photos 1 and 2. "
BODY="BODY LOCK: the body must be an exact match of the figure in photos 3 and 4 (same woman): the same bust size and shape, the same narrow waist, flat toned stomach, wide curvy hips, same shoulder width, same athletic hourglass proportions and long toned legs; do NOT make her slimmer, flatter-chested or more slender than photos 3 and 4, and keep the bust the same size even under clothing. Use only the body, never the outfits, of photos 3 and 4. Her skin is a deep golden-bronze sun-kissed tan exactly like photos 3 and 4, NOT pale. "
TAIL=" Light warm golden-hour sun with slight haze, low contrast, no blown highlights. Candid unposed phone photo, visible natural skin texture and pores, tiny freckles, flyaway hair strands, matte unretouched skin, no glossy sheen. Shot on iPhone, framed head to mid-thigh with headroom, nobody else anywhere in the frame, no text, no logos."
S={
1:("Scene: empty sunlit rooftop terrace in Miami, she wears an emerald-green two-piece swimsuit with a modest scoop top, leaning back on the railing with her head thrown back, eyes crinkled shut in a spontaneous open-mouth LAUGH, face tilted up and to the left.","smile"),
2:("Scene: empty white-sand beach path with sea oats, she wears a white two-piece string swimsuit, standing relaxed with a calm NEUTRAL RELAXED face, lips closed, soft eyes, head level, looking straight at the camera with a flat resting expression, no smile.","calm"),
3:("Scene: empty pool deck with palm trees in Miami, she wears a coral two-piece swimsuit, torso angled 3/4 to the camera (front of body visible), head in three-quarter view LOOKING OFF-CAMERA far to the right at the horizon, lips slightly parted, distant gaze, no smile.","calm"),
4:("Scene: quiet empty rooftop bar at sunset with a palm skyline, she wears a fitted lilac ribbed scoop-neck crop tee and denim shorts, seated on a stool holding an iced coffee with a straw, taking a SIP mid-sip with lips around the straw, eyes on the cup.","calm"),
5:("Scene: empty beach boardwalk, she wears an olive-green two-piece swimsuit and white linen shorts, SQUINTING AT THE SUN with scrunched eyes and furrowed brow, one hand shielding her eyes, mouth slightly tense, not smiling.","calm"),
6:("Scene: empty Miami balcony with ocean view, she wears a fitted mustard ribbed scoop-neck crop tank and high-waist cream shorts, a SOFT CLOSED-MOUTH SMILE (lips together, no teeth), head tilted slightly, eyes just past the camera, relaxed shoulders.","smile"),
7:("Scene: empty sandy dune path with sea grass, she wears a turquoise two-piece swimsuit, a PLAYFUL SMIRK with one corner of the mouth raised and one eyebrow slightly lifted, chin lowered, eyes looking up at the camera through her lashes, hand on hip.","smile"),
8:("Scene: empty shoreline with gentle waves, she wears a fitted black scoop-neck crop top and light denim shorts, torso turned 3/4 to the camera (front of the bust visible), GLANCING OVER HER SHOULDER at the camera, lips closed, hair swept to one side.","smile"),
9:("Scene: empty pastel peach Art Deco wall (plain, no signs, no cars, no pedestrians), she wears a fitted cobalt-blue ribbed scoop tank and white jeans, SURPRISED AND AMUSED: eyebrows raised, eyes wide, mouth open in a small 'oh!', looking off to the left at something out of frame.","calm"),
10:("Scene: empty seaside bench in a Miami park with palms, she wears a fitted dusty-rose ribbed scoop-neck tank and cream shorts, seated with a THOUGHTFUL LOOK DOWN: eyes cast down at her phone in her hand, head slightly bowed, lips closed and relaxed, no smile.","calm"),
}
def R(ks):
    out=[]
    for k in ks:
        t,kind=S[k]
        faces=[FC,F6] if kind=="smile" else [FK,FC]
        out.append({"index":k,"params":{"model":"seedream_v5_pro","prompt":t+" "+FACE+BODY+TAIL,"aspect_ratio":"3:4","count":1,"medias":[{"value":m,"role":"image_references"} for m in faces+[B4,B7]]}})
    return out
if __name__=="__main__":
    import sys;print(json.dumps(R([int(x) for x in sys.argv[1:]] or list(S))))
