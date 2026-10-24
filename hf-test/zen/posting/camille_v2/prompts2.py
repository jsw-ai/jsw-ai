import json
SKIN=open('prompts.py').read().split('SKIN="')[1].split('"\n')[0]
BODY="Slim narrow waist, slim toned athletic-hourglass figure, proportionate moderate (not large) bust, slim toned thighs, flat stomach, slender arms, fit and lean. NOT heavy, NOT curvy-plus, NOT large bust, no cleavage emphasis. Warm light-tan golden-brown skin."
FRAME="Three-quarter shot framed from head to mid-thigh so the hips and both hands are fully visible, standing, camera at chest height, off-centre, no text, no other people, natural relaxed hands with correct five fingers."
base="A real slim woman in her mid 20s with tight, defined black ringlet curls (springy coiled ringlets, shoulder to chest length), dark brown eyes. Face identity: same woman as the reference photo(s). "
S={
1:("c2","Oval face with high cheekbones, slightly thick straight brows, small gap in front teeth in a laughing smile. Standing on a sunny balcony in a fitted cream tank top and high-waisted light jeans."),
2:("c2","Oval face with high cheekbones, slightly thick straight brows, soft smile. Standing in a park path at golden hour in a fitted dark green crop-sleeve top and high-waisted black trousers."),
3:("c4","Longer face with defined chin, strong dark brows, slightly hooded eyes, wide natural smile with teeth. Standing in a sunlit living room with late sun through the window, fitted rust-orange top and high-waisted jeans, one hand in pocket and one hand relaxed."),
4:("c4","Longer face with defined chin, strong dark brows, hooded eyes, gentle half-smile. Standing against a warm plaster wall outdoors in a fitted white tee tucked into light jeans."),
5:("c6","Strong soft jawline, medium-wide nose, dark lashes, relaxed slight smirk. Standing by a railing by the sea at sunset in a fitted navy top and light denim shorts, hands resting on the railing."),
6:("c6","Strong soft jawline, medium-wide nose, dark lashes, small natural smile. Standing on a city street at golden hour in a fitted black ribbed top and high-waisted olive trousers, hands loosely at sides."),
}
ids={"c2":"63bdd129-19b5-4286-aa4d-ed7d189a2524","c4":"188e7816-22fd-447c-9f66-3eda16fc95f1","c6":"c6f0c729-23e5-463f-b8b1-436de1acbcdf"}
reqs=[{"index":k,"params":{"model":"seedream_v5_pro","prompt":base+v[1]+" "+BODY+" "+FRAME+" "+SKIN,"aspect_ratio":"3:4","resolution":"2k","use_unlim":False,"medias":[{"value":ids[v[0]],"role":"image_references"}]}} for k,v in S.items()]
json.dump({"requests":reqs},open('req2.json','w'))
print(json.dumps(reqs[0]))
