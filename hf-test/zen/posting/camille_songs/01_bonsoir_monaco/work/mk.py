import json
S=json.load(open('/workspace/hf-test/zen/posting/camille_oct22/work/stills_prompts.json'))['S6']
pre=S.split('Change only her outfit, pose and setting:')[0]
body='Framed from head to hips, face large and sharp.'+S.split('Framed from head to hips, face large and sharp.')[1]
body=body.replace('Soft daylight evenly lit from the front on her face','Warm soft light evenly lit from the front on her face')
SILVER='a silver satin slip midi dress with thin straps and a modest straight neckline, small silver drop earrings'
SC={
'M01_harbour':f'she stands on the harbour promenade of Monaco at pink twilight, rows of white superyachts and the lit hillside city behind her. She wears {SILVER}. Hands relaxed at her sides.',
'M02_heels':f'she walks barefoot on an empty old cobblestone street in Monaco at dusk, warm street lamps glowing, holding a pair of silver high heels by the straps in her left hand at hip height. She wears {SILVER}.',
'M03_casino':f'she stands in an empty grand plaza in front of an ornate Belle Epoque casino building lit in gold at night, palm trees and a lit fountain behind her. She wears {SILVER}. One hand on her hip.',
'M04_rose_bar':f'she sits at a small marble table on an empty terrace bar at night overlooking the lit harbour, a glass of pale rosé on the table in front of her, her hand resting beside it. She wears {SILVER}.',
'M05_balcony':f'she stands at a wrought-iron balcony railing at night, the glittering lights of Monaco and the dark sea far below behind her. She wears {SILVER}. Both hands resting lightly on the railing.',
'M06_yacht':'she stands on the teak deck of an empty white yacht moored in the harbour at dusk, the lit marina behind her. She wears a white satin slip midi dress with thin straps and a modest neckline, small gold hoop earrings. One hand lightly on the chrome deck rail.',
'M07_steps':f'she stands halfway up a wide empty marble staircase lined with warm lanterns at night in Monaco old town. She wears {SILVER}. One hand on the stone banister.',
'M08_car':f'she leans casually against a parked vintage cream convertible sports car on an empty harbour road at pink twilight, yachts and the sea behind her. She wears {SILVER}. Arms relaxed.',
'M09_lights':'she stands on an empty seaside walkway at blue hour as the strings of café lights above her switch on one by one, the sea and the lit coastline behind her. She wears a red satin slip midi dress with thin straps and a modest neckline, small gold hoop earrings. Hands relaxed at her sides.',
'M10_lobby':f'she stands in an empty grand hotel lobby with gold chandeliers and marble columns at night. She wears {SILVER}. One hand holding a small silver clutch at her hip.',
'M11_rooftop':'she stands at the edge of an empty rooftop terrace with a softly lit pool at night, the lights of Monaco and the harbour behind her. She wears a black satin slip midi dress with thin straps and a modest neckline, small gold hoop earrings. Hands relaxed.',
'M12_waterfront':f'she stands at a stone sea wall at night with the moon over the dark sea and the lit Monaco skyline curving behind her, a light sea breeze. She wears {SILVER}. Hands relaxed at her sides.',
}
req=[];i=0
for asp in ['9:16','16:9']:
  for k,v in SC.items():
    p=pre+'Change only her outfit, pose and setting: '+v+' '+body
    if asp=='16:9': p=p.replace('Framed from head to hips, face large and sharp.','Horizontal wide frame: she stands slightly off-centre, framed from head to hips, with the setting visible on both sides, face large and sharp.').replace('Realistic candid vertical phone photo','Realistic candid horizontal photo')
    req.append(dict(index=i,name=k+('_v' if asp=='9:16' else '_h'),params=dict(model='seedream_v5_pro',prompt=p,aspect_ratio=asp,resolution='2k',medias=[dict(value='62cab441-d244-48c5-ba32-4e4fbb9c5834',role='image_references')])));i+=1
json.dump(req,open('stills_req.json','w'),indent=1)
print(len(req), len(req[0]['params']['prompt']))
