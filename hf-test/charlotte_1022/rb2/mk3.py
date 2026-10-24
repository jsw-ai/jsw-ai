exec(open('mk.py').read().split('items=')[0])
x5g=E+", same pose and framing, standing and facing the camera. Change the setting to a bright Munich hotel bedroom by a big window with sheer white curtains in soft daylight and a rumpled white bed behind her. Change her outfit to a fully covering black lace bralette and matching black high-waisted briefs under an oversized white button shirt worn open and slipping off one shoulder, no nudity. New pose: one hand holds the edge of the sheer curtain beside her, the other hand rests on the shirt collar at her collarbone. Not hands on hips."
kC=E+", same pose, same framing, same soft even daylight on her face as the photo. Change only her outfit and the background: she wears a traditional dirndl with a green bodice, a white blouse with a modest high neckline and a blue apron, and holds a one-litre glass beer stein full of golden beer with white foam in her right hand at chest height (plain glass, no logo, no label); the background becomes a sunny Munich beer garden in soft overcast daylight with chestnut trees and long empty wooden tables, nobody else there."
F=" Her face is upright and square to the camera, evenly lit from the front."
for k,h in [('x5g',x5g),('x5g2',x5g),('x5g3',x5g),('kC',kC),('kC2',kC),('kC3',kC),('kC4',kC)]:
    t=TAIL
    if k.startswith('x5'): t=t.replace(SM,"Soft playful closed-mouth smirk, relaxed eyebrows, not grinning,")
    open(f'p/{k}.txt','w').write(h+F+' '+t)
