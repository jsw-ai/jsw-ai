import json
exec(open('../rb/mkp.py').read().split('E="Edit')[0])  # TAIL
FR=" Photo 1 is the photo to edit. Photos 2, 3 and 4 are the same woman's face, use them only for her facial identity (face shape, eyes, nose, lips, freckles), not for outfit, hair styling or background."
E="Edit photo 1: same woman"
J={
"L1":("c_c4.jpg",E+", same framing and pose, waist-up. Change the setting to an empty lakeside promenade path at Lake Tegernsee in Bavaria, calm blue-grey lake and green wooded alpine hills behind her, bright overcast autumn daylight. Change her outfit to a light cream chunky knit cardigan worn open over the same plain white crew-neck tee, with blue jeans."),
"P1":("c_c1.jpg",E+", same framing, waist-up, seated at a small wooden table in an empty cosy Munich bakery cafe with soft daylight from the window. Same plain black top with a modest neckline. She holds one large golden-brown Bavarian pretzel up in one hand at chest height, well below her face, a small cup of coffee on the table. No iced drink."),
"G1":("c_P1.jpg",E+", same standing pose with hands on hips and same framing, head to knees. Change the setting to a bright tidy Munich hotel room with a big window and white bed behind her, soft daylight from the front. Change her outfit to dark blue straight-leg jeans, a cream cable-knit jumper with a crew neck, and white trainers."),
"G2":("c_P1.jpg",E+", same standing pose with hands on hips and same framing, head to knees. Change the setting to a bright tidy Munich hotel room with a big window and white bed behind her, soft daylight from the front. Change her outfit to a short red rain jacket zipped half up over a plain white crew-neck tee, black straight-leg jeans and white trainers."),
"R1":("c_c5.jpg",E+", same pose holding the same mug in both hands at chest height, same framing, waist-up. Change the setting to an empty wooden lakeside cafe terrace at Lake Tegernsee with the calm lake and green alpine hills behind her, bright overcast daylight. Change her outfit to a soft forest-green crew-neck knit jumper. The mug holds hot chocolate."),
"Y1":("c_D2.jpg",E+", same standing pose and framing, waist-up. Change the setting to the end of an empty wooden boat jetty on Lake Tegernsee with calm water, a few small moored wooden rowing boats and green alpine hills behind her, bright overcast daylight. Change her outfit to a navy quilted puffer vest over a plain white long-sleeve crew-neck top and blue jeans."),
"S1":("c_c4.jpg",E+", same framing and pose, waist-up. Change the setting to a quiet empty Bavarian village street with white alpine houses, painted wooden balconies and red geranium flower boxes, bright daylight. Change her outfit to a camel wool coat open over the same plain white tee."),
"S2":("c_c1.jpg",E+", same framing, waist-up, seated at a wooden table in an empty cosy traditional alpine restaurant room with wooden panelled walls and soft daylight from the window, a plate of Kaiserschmarrn (torn fluffy pancake with powdered sugar) and a small bowl of apple sauce on the table in front of her. Change her outfit to a soft oatmeal crew-neck knit jumper."),
"S3":("c_c4.jpg",E+", same framing and pose, waist-up. Change the setting to an empty pebble lakeshore at Lake Tegernsee with calm clear water and wooded alpine mountains behind her, bright overcast daylight. Change her outfit to a dark green zip-up fleece jacket over the same plain white tee, and she holds one small flat grey stone between her fingers at chest height."),
"F1":("c_c5.jpg",E+", same framing, waist-up, both hands holding the same mug at chest height. Change the setting to the doorway of an old dark-wood lakeside boathouse at Lake Tegernsee with the lake glimpsed beside it, bright overcast daylight. Change her outfit to a cream wool roll-neck jumper and a plain red-and-white knitted scarf (no crest, no logo)."),
"X1":("c_c8.jpg",E+", same seated pose and framing. Change the setting to the edge of an empty wooden lake jetty on Lake Tegernsee, calm water and green alpine hills behind her, bright overcast daylight. Change her swimwear to a plain classic red triangle bikini with full coverage bottoms, no nudity, a grey knitted beanie on her head with her hair loose below it."),
"X2":("c_D2.jpg",E+", same standing pose and framing, head to mid-thigh. Change the setting to a bright hotel room with a big window looking out over Lake Tegernsee and alpine hills, sheer curtains, soft daylight on her face from the front. Change her outfit to a fully covering black lace bralette and matching black lace high-waisted briefs, no nudity."),
}
two=["L1","P1","G1","R1","Y1"]
ids=json.load(open('man/media_ids.json'))
reqs=[];keys=[]
for k,(src,p) in J.items():
  for v in (["a","b"] if k in two else ["a"]):
    full=p+FR+TAIL; open(f'p/{k}{v}.txt','w').write(full); keys.append((k+v,src))
    reqs.append({"index":len(reqs),"params":{"model":"seedream_v5_pro","prompt":"$file:/workspace/hf-test/charlotte_1022/quota2/p/%s%s.txt"%(k,v),"aspect_ratio":"3:4","resolution":"2k","medias":[{"value":ids[src],"role":"image_references"}]+[{"value":ids[f],"role":"image_references"} for f in ['q2_facekeeper.jpg','q2_coverface.jpg','q2_f.jpg']]}})
json.dump(keys,open('man/still_index.json','w'))
for i in range(0,len(reqs),4): print(json.dumps({"requests":[dict(r,index=j) for j,r in enumerate(reqs[i:i+4])]}))
