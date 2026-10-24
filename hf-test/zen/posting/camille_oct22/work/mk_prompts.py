import json
LB=open('/workspace/hf-test/zen/posting/camille_oct22/LOCKED_BODY.txt').read().strip().split('\n')[1].strip()
HEAD=("Edit this exact photo: same woman, keep her face exactly identical (same round-oval face shape, same eyes, brows, nose and lips, same freckles), "
"same voluminous jet-black tight ringlet curls in the same shoulder-length bob with side part, worn down loose, same body and body proportions, same bust size. "
"Change only her outfit, pose and setting: ")
TAIL=(" The same woman: "+LB+" Soft daylight evenly lit from the front on her face, no harsh shadows, no backlight on her face. "
"Soft closed-mouth smile, lips together, eyes fully open looking into the camera, head upright. No other people anywhere in frame, no text, no logos. "
"Unretouched natural skin with fine pores and faint light freckles, light natural skin texture, dry matte skin, no shine, no sheen, no glow, no highlighter, no airbrushing. "
"Realistic candid vertical phone photo, not a studio shot, not CGI.")
S={
"S1":"she stands on a sunny private terrace high above the Mediterranean sea on the French Riviera in the morning, white stone balustrade behind her, turquoise sea and coastline far below, a rolled yoga mat leaning on the balustrade. She wears a cream ribbed fitted sports crop top with a soft scoop neckline and matching cream ribbed high-waisted shorts. Arms relaxed at her sides, hands empty. Framed from head to hips, face large and sharp.",
"S2":"she stands on the same kind of sunny private terrace high above the Mediterranean sea on the French Riviera in the morning, white stone balustrade behind her, turquoise sea and coastline far below. She wears a cream ribbed fitted sports crop top with a soft scoop neckline and an ivory silk wrap midi skirt tied at the waist over it, small gold hoop earrings. One hand resting on her hip, the other relaxed at her side. Framed from head to hips, face large and sharp.",
"S3":"she stands on a sunny private terrace above the Mediterranean sea on the French Riviera, a white sun lounger and potted olive tree behind her, sea far below. She wears a black fitted cropped long-sleeve workout top with a scoop neckline and black high-waisted workout shorts. Arms crossed loosely under her chest, unimpressed calm deadpan look with a tiny closed-mouth smirk, brows relaxed. Framed from head to hips, face large and sharp.",
"S5":"she stands at the white stone balustrade of a sunny private terrace above the Mediterranean sea on the French Riviera in the morning, a small round bistro table beside her with a croissant on a plate and a white espresso cup. She wears a crisp white linen button-up shirt with the sleeves rolled up and the top two buttons open, small gold hoop earrings. She holds a small white espresso cup in her right hand at chest height, well below her chin, five fingers visible. Framed from head to hips, face large and sharp.",
"S6":"she stands at the white stone balustrade of a private terrace above the Mediterranean sea on the French Riviera in the early evening, warm pink and peach sky over the sea behind her, but her face is softly and evenly lit from the front. She wears an emerald green silk slip dress with thin straps and a soft cowl neckline, small gold hoop earrings. She holds a stemmed glass of pale rosé in her right hand at chest height, well below her chin, five fingers visible. Framed from head to hips, face large and sharp.",
"S7":"she leans one hand on the white stone balustrade of a sunny private terrace above the Mediterranean sea on the French Riviera, sea and coastline far below. She wears a fitted cream sports bra and high-waisted wide-leg white linen trousers, small gold hoop earrings, toned midriff visible. Framed from head to hips, face large and sharp.",
"S9":"she sits at a small round marble cafe table on a sunny terrace above the Mediterranean sea on the French Riviera, a white espresso cup on a saucer on the table in front of her. She wears a fitted navy-and-white Breton striped long-sleeve top with a boat neckline, small gold hoop earrings. Both forearms resting on the table, hands relaxed and empty, five fingers visible. Calm, unimpressed, judging look with a tiny closed-mouth smirk, brows relaxed. Framed from head to waist, face large and sharp.",
}
P={k:HEAD+v+TAIL for k,v in S.items()}
json.dump(P,open('/workspace/hf-test/zen/posting/camille_oct22/work/stills_prompts.json','w'),indent=1)
reqs=[];i=0
for k in ["S1","S1","S2","S2","S3","S3","S5","S5","S6","S6","S7","S9"]:
    reqs.append({"index":i,"params":{"model":"seedream_v5_pro","prompt":P[k],"aspect_ratio":"9:16","resolution":"2k","medias":[{"value":"62cab441-d244-48c5-ba32-4e4fbb9c5834","role":"image_references"}]}}); i+=1
json.dump(reqs,open('/workspace/hf-test/zen/posting/camille_oct22/work/batch1.json','w'))
print(len(P['S1']))
