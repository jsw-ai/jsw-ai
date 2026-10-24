import re
exec(open('mk.py').read().split('items=')[0])
x3c=E+", same wooden sauna and same white towel wrapped and tucked securely under her arms, fully covering. New pose: she stands in the open wooden sauna doorway, one hand holding the wooden door frame beside her head, the other hand resting at the top of the tucked towel, body and face square to the camera, framing head to mid-thigh, light steam drifting out behind her. Not hands on hips, not seated."
x5f=E+". New scene and pose: she kneels upright on a rumpled white hotel bed, sitting back on her heels, both hands resting on her thighs, shoulders square to the camera, in a bright Munich hotel room with sheer curtains in daylight, wearing a fully covering black lace bralette and matching black briefs with an oversized white button shirt open and slipping off one shoulder, no nudity, framing head to knees. Not hands on hips."
tree=E+", same pilates studio with reformer machines and same outfit. New pose: she stands on one leg in a balanced tree pose beside the reformer, the sole of her other foot resting on her inner calf, palms pressed together at her chest, body and face square to the camera, framing head to knees, bright morning daylight from the windows."
F=" Her face is upright and square to the camera, evenly lit from the front."
A=[('x3c',x3c,'S5'),('x3c2',x3c,'S5'),('x3c3',x3c,'S5'),('x5f',x5,'c8'),('x5f2',x5f,'c8'),('x5f3',x5f,'c8'),('iB',ice,'I4'),('iB2',ice,'I4'),('pC',pil,'P1'),('pC2',tree,'P1'),('pC3',tree,'P1'),('kB',ok,'c4'),('kB2',ok,'c4'),('kB3',ok,'c4')]
A[3]=('x5f',x5f,'c8')
for k,h,s in A:
    t=TAIL
    if k.startswith('x5'): t=t.replace(SM,"Soft playful closed-mouth smirk, relaxed eyebrows, not grinning,")
    if k.startswith('iB'): t=t.replace(SM,"Brave soft closed-mouth smile, not grinning,")
    open(f'p/{k}.txt','w').write(h+F+' '+t)
    print(k,s,M[s])
