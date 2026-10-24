from PIL import Image,ImageDraw,ImageFont
K='keepers/'
face=[('camille_face_keeper',.844),('camille_face_from_talking4_b',.844),('camille_face_from_bikini1',.891),('camille_face_from_bikini_fromcover',.855),('camille_bikini1',.942),('camille_bikini2',.961),('camille_cover',.953)]
body=[('camille_bikini1',.942),('camille_bikini2',.961),('camille_bikini_fromcover',.899)]
W,H=320,427;f=ImageFont.load_default(size=15)
s=Image.new('RGB',(W*7,(H+40)*2+90),'white');d=ImageDraw.Draw(s)
d.text((8,6),"CAMILLE identity reference set - DRAFT / UNAPPROVED (face-gate centroid vs current pack shown)",fill='black',font=f)
def row(items,y,title,flags={}):
    d.text((8,y),title,fill='red',font=f)
    for i,(n,sc) in enumerate(items):
        im=Image.open(K+n+'.png').convert('RGB');im.thumbnail((W,H))
        s.paste(im,(i*W,y+22));d.text((i*W+4,y+24+H),f"{n[8:]}  {sc}{flags.get(n,'')}",fill='black',font=f)
row(face,30,"FACE REFS (7 candidates; pack lists first/5th/6th/7th = face_keeper,bikini1,bikini2,cover)",{'camille_cover':'  [gate: no_headroom]'})
row(body,30+H+60,"BODY REFS (3, only 2 distinct scenes: beach standing, pool seated)")
s.save('zen/posting/camille_contact_sheet.png')
