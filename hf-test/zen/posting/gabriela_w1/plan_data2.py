import sys; sys.path.insert(0,'/workspace/hf-test/zen/posting/gabriela_w1')
from plan_data import IMG
P=[p for p in __import__('plan_data').P]
P=[list(p) for p in P]
# P16: reassign to existing still (cap 0 credits)
for p in P:
    if p[0]=='P16':
        p[4]='H'; p[5]="sunshine first, everything else second 🌿"; p[6]="#tuesday #sunnyday #garden"
# new slots: (id, day, platform, time, imgs, caption, tags)
N=[
('P22','Thu 10/15','Facebook (Page post)','12:00 PM','E',"golden hour does most of the work 🌅 hello from the beach","#goldenhour"),
('P23','Thu 10/15','YouTube (Community-style image post)','5:00 PM','F',"rooftop, low sun, zero plans ☀️ what's your favourite time of day?",""),
('P24','Fri 10/16','Facebook (Page post)','12:00 PM','A',"sand in my hair, no regrets 🌊","#beachwalk"),
('P25','Fri 10/16','YouTube (Community-style image post)','5:00 PM','C',"pool day question: pool or beach? 💦",""),
('P26','Sat 10/17','Facebook (Page post, 3-photo album)','12:00 PM','D,E,A',"saturday on the shoreline 🌊 which photo is your favourite?","#shoreline #goldenhour"),
('P27','Sat 10/17','YouTube Short (slideshow from stills, 15s, no voice, local render)','4:00 PM','D,E,A,C',"shoreline saturday 🌅","#shorts #goldenhour #beachday"),
('P28','Sun 10/18','Facebook (Page post)','12:00 PM','G',"balcony sunsets are my therapy 🌇","#sunset"),
('P29','Sun 10/18','YouTube (Community-style image post)','5:00 PM','H',"sunday reset: lawn, linen shirt, late sun. how are you spending yours?",""),
('P30','Mon 10/19','Facebook (Page post)','12:00 PM','B',"monday mood: found a sunny spot and laughing at nothing ☀️","#mondaymood"),
('P31','Mon 10/19','YouTube (Community-style image post)','5:00 PM','G',"poll idea: sunrise or sunset person? 🌇",""),
('P32','Tue 10/20','Facebook (Page post)','12:00 PM','H',"sunshine first, everything else second 🌿 beach, pool or garden?","#tuesday"),
('P33','Tue 10/20','YouTube (Community-style image post)','5:00 PM','D',"shoes in hand, sand between my toes. beach or pool? 👇",""),
('P34','Wed 10/21','Facebook (Page post, 5-photo album)','12:00 PM','A,E,D,C,F',"my week in 5 pics, golden hour edition 🌅","#weekrecap #goldenhour"),
('P35','Wed 10/21','YouTube Short (slideshow from stills, 15s, no voice, local render)','4:00 PM','A,E,D,C,F',"my week in 5 pics 🌅","#shorts #weekrecap #goldenhour"),
('P36','Sat 10/17','TikTok photo-mode (3 pics)','7:30 PM','B,F,H',"saturday sunshine dump 🌿 which one's your fave?","#saturday #sunnyday #photodump #fyp"),
('P37','Mon 10/19','X','12:30 PM','E',"monday needs more golden hour",""),
('P38','Wed 10/21','X','6:30 PM','G',"balcony, sunset, nowhere to be 🌇",""),
]
ALL=P+[list(n) for n in N]
dayorder=['Thu 10/15','Fri 10/16','Sat 10/17','Sun 10/18','Mon 10/19','Tue 10/20','Wed 10/21']
import datetime
def tk(t):
    return datetime.datetime.strptime(t,'%I:%M %p')
ALL.sort(key=lambda p:(dayorder.index(p[1]),tk(p[3])))
