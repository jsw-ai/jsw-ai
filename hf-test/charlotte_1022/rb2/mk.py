import json,re
src=open('../rb/mkp.py').read()
TAIL=eval(re.search(r'TAIL=(".*?")\+open',src).group(1))+open('/workspace/hf-test/charlotte_ref/LOCKED_BODY.txt').read().strip()
SM="Same gentle natural smile as the photo, not a wide open-mouth laugh, not grinning,"
E="Edit this exact photo: same woman"
M={'S5':'543d3a0e-af9e-4067-abf6-e2015ad3f38a','c8':'d4a9f516-36e1-4953-a4e5-f849216e0946','c5':'daaf7ae0-65fe-41b3-9de0-b689029123ba','I4':'2108445c-a9a1-440d-921a-29323b6b781a','P1':'9fffb5b4-0f0b-4ee2-87e6-2cb7503f8e4c','c4':'de3b78a8-6378-4395-94c4-19bc87fa0f65'}
x3a=E+", same wooden sauna and same white towel wrapped and tucked securely under her arms, fully covering. New pose: she stands leaning one shoulder against the warm wooden sauna wall, body turned slightly, one hand lifting her hair up off the back of her neck, the other arm relaxed down holding the tucked edge of the towel, framing head to mid-thigh, light steam in the air. Not hands on hips, not seated."
x3b=E+", same wooden sauna and same white towel wrapped and tucked securely under her arms, fully covering. New pose and angle: she stands beside the sauna stove holding a wooden ladle, pouring water onto the hot stones so steam rises, her body turned three-quarters away while her head turns back to look over her shoulder straight into the camera, camera at a slightly low side angle, framing head to hips. Not hands on hips, not seated."
x5=E+". New scene and pose: she lies on her stomach across a rumpled white hotel bed in a bright Munich hotel room with sheer curtains in daylight, propped up on her elbows facing the camera, chin resting lightly on one hand, her lower legs raised and crossed behind her, wearing a fully covering black lace bralette and matching black briefs with an oversized white button shirt slipping off one shoulder, no nudity, framing head to hips."
r1=open('../rb/p/r1c.txt').read().split(' Keep her face')[0].replace("an oversized cream cable-knit sweater","an open oversized cream cable-knit cardigan worn over a plain white crew-neck cotton t-shirt with a high round neckline that fully covers her chest, no cleavage")
ice=E+", same spa recovery room. New pose: she now sits inside the steel ice-bath tub filled with ice cubes and cold water, submerged up to her chest, both forearms resting on the tub rim, same black sporty one-piece swimsuit straps visible on her shoulders, a few ice cubes around her, framing head to chest from the front, brave closed-mouth smile."
pil=E+", same pilates studio with reformer machines and same outfit. New pose: she stands in a deep forward lunge with her front foot up on the reformer's platform, one hand resting on her raised front knee and the other hand on her hip, body facing the camera, framing head to knees, bright morning daylight from the windows."
ok=E+". Change the setting to a sunny Munich beer garden in daylight under chestnut trees with long empty wooden tables and benches, nobody else there. Change her outfit to a traditional dirndl: green bodice, white blouse with a modest high neckline, blue apron. She holds a one-litre glass beer stein full of golden beer with white foam in her right hand at chest height, her left arm relaxed at her side. Framing waist-up, facing the camera."
items=[('x3a',x3a,'S5'),('x3a2',x3a,'S5'),('x3b',x3b,'S5'),('x3b2',x3b,'S5'),('x5e',x5,'c8'),('x5e2',x5,'c8'),('r1d',r1,'c5'),('r1d2',r1,'c5'),('iA',ice,'I4'),('iA2',ice,'I4'),('pB',pil,'P1'),('pB2',pil,'P1')]
R=[]
for i,(k,h,s) in enumerate(items):
    t=TAIL
    if k.startswith('x5'): t=t.replace(SM,"Soft playful closed-mouth smirk, relaxed eyebrows, not grinning,")
    if k in('iA','iA2'): t=t.replace(SM,"Brave soft closed-mouth smile, not grinning,")
    p=h+' '+t; open(f'p/{k}.txt','w').write(p)
    p=p.replace(" with clear visible cleavage","") if k.startswith("r1") else p; open(f"p/{k}.txt","w").write(p)
    R.append({'index':i,'params':{'model':'seedream_v5_pro','prompt':p,'aspect_ratio':'3:4','resolution':'2k','medias':[{'value':M[s],'role':'image_references'}]}})
json.dump({'requests':R},open('reqs.json','w'))
json.dump({'requests':[{'index':j,'params':{'model':'seedream_v5_pro','prompt':ok+' '+TAIL,'aspect_ratio':'3:4','resolution':'2k','medias':[{'value':M['c4'],'role':'image_references'}]}} for j in range(2)]},open('reqs_ok.json','w'))
open('p/kA.txt','w').write(ok+' '+TAIL)
print(len(R), r1[:400])
