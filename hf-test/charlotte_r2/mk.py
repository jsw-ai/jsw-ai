import json,sys
sys.path.insert(0,'/workspace/hf-test/charlotte_test')
src=open('/workspace/hf-test/charlotte_test/mkprompts.py').read()
COMMON=src.split('COMMON=(',1)[1].split('")\n',1)[0].strip().lstrip('"')+'"'
COMMON=eval('"'+COMMON.strip('"')+'"') if False else COMMON.strip('"')
S=[
"standing at an outdoor farmers market produce stall with wooden crates of peaches, wearing a fitted terracotta scoop-neck top and jeans, smiling, holding a peach",
"stretching in a bright empty home gym corner on a yoga mat, wearing a fitted black scoop-neck sports top and high-waisted leggings, arms overhead, smiling",
"sitting in a car passenger seat with sunlight through the window, wearing a fitted white scoop-neck top, seatbelt on, laughing at camera",
"standing at a hiking trail overlook with distant hills behind, wearing a fitted olive scoop-neck tank and hiking shorts, hand shading eyes, smiling",
"browsing an empty bookstore aisle holding a book, wearing a fitted dusty-rose scoop-neck top and a long denim skirt, looking at camera with a soft smile",
"standing on a rooftop terrace at sunset with the city skyline behind, wearing a fitted cream scoop-neck top and light trousers, hair blowing, smiling",
"pushing a cart down a grocery store produce aisle, wearing a fitted navy scoop-neck top and jeans, glancing at camera and smiling",
"sitting on a sunny front porch step with a glass of lemonade, wearing a fitted yellow scoop-neck top and white shorts, relaxed smile",
"sitting on a beach towel on the sand, wearing a cobalt blue two-piece bikini, sunglasses pushed up in her hair, smiling at camera",
"standing on a wooden lake dock with calm water behind, wearing a coral two-piece swimsuit, hand in her hair, laughing",
"sitting at a brunch patio table with a plate of pancakes and a mimosa, wearing a fitted emerald scoop-neck top, smiling at camera",
"standing in a bright hallway doing an outfit check, wearing a fitted lavender scoop-neck top and light wide-leg jeans, hands on hips, smiling",
"standing in a grassy dog park holding a leash with a golden retriever beside her, wearing a fitted grey scoop-neck top and leggings, laughing",
"standing at a sidewalk coffee cart holding a paper cup, wearing a fitted burgundy scoop-neck top and black jeans, smiling at camera",
"lying back on a pool lounger by the water, wearing a white two-piece bikini, one knee bent, relaxed smile",
"walking on a quiet dirt path at sunset through tall grass, wearing a fitted peach scoop-neck top and a flowy skirt, glancing back at camera smiling",
]
reqs=[]
for i,s in enumerate(S,1):
    reqs.append({"index":i,"params":{"model":"seedream_v5_pro","prompt":"Scene: "+s+". "+COMMON,"aspect_ratio":"3:4","count":1,"medias":[{"value":"fd8e810e-e9b5-433b-8145-855b591fdc45","role":"image"},{"value":"b8d45ca6-dd40-48fb-93dc-861288165bfd","role":"image"}]}})
json.dump(reqs,open('reqs.json','w'),indent=1)
print(reqs[0]['params']['prompt']);
t=json.load(open('/workspace/hf-test/charlotte_test/batch.json'))['requests'][0]['params']['prompt']
print(t.split('. Take',1)[1]==reqs[0]['params']['prompt'].split('. Take',1)[1])
