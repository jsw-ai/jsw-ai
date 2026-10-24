import json
R='/workspace/hf-test/zen/posting/camille_oct22/raw/';M='/workspace/hf-test/zen/posting/camille_music/';F='/workspace/hf-test/zen/posting/camille_oct22/fin/'
S={}
S['TT1_slowmo']={"music":M+"camille_10_au_revoir_l_ete.mp3","moff":30.0,"hold":0.3,
 "segs":[{"v":R+"B2_t2.mp4","a":0.0,"b":1.0,"sp":0.8},{"v":R+"B2_t2.mp4","a":1.95,"b":4.3,"sp":0.8,"tr":"fade:0.3"}],
 "texts":[["Riviera mornings",0,99,260,64],["in slow motion",0,99,345,64]]}
S['IG_reel_workout']={"music":M+"camille_05_petit_dejeuner.mp3","moff":20.0,"hold":0.3,
 "segs":[{"v":R+"B1_t2.mp4","a":0.0,"b":1.6},{"v":R+"B1_t2.mp4","a":2.2,"b":3.3},{"v":R+"B1_t1.mp4","a":3.4,"b":5.04}],
 "texts":[["sea view: on.",0,99,1330,68],["pilates mat: out.","cut1",99,1418,68],["motivation: en vacances","cut2",99,1506,68]]}
S['YT1_silksunset']={"music":M+"camille_03_silk_and_sunset.mp3","moff":47.8,"hold":0.4,
 "segs":[{"img":F+"S6a_v4C.jpg","d":1.2,"z":[1.0,1.02]},{"v":R+"A2_t1.mp4","a":1.2,"b":5.04,"tr":"fade:0.3"}],
 "texts":[["silk and sunset",0,99,1420,74],["you and me",1.4,99,1516,64]]}
S['YT2_breakfast']={"music":M+"camille_01_bonsoir_monaco.mp3","moff":25.0,"hold":0.4,
 "segs":[{"v":R+"C2_t2.mp4","a":0.0,"b":1.8},{"v":R+"C2_t2.mp4","a":4.1,"b":5.04,"tr":"fade:0.3"}],
 "texts":[["Riviera breakfast:",0,99,1300,66],["one espresso.",0.6,99,1386,66],["that's it. c'est parfait","cut1",99,1472,64]]}
S['FB_ootd']={"music":M+"camille_02_champagne_sur_la_plage.mp3","moff":38.9,"hold":0.3,
 "segs":[{"v":R+"B2_t1.mp4","a":0.0,"b":1.0},{"v":R+"B2_t1.mp4","a":2.4,"b":3.2},{"v":R+"B2_t1.mp4","a":3.8,"b":5.04,"tr":"fade:0.25"}],
 "texts":[["Riviera outfit check",0,99,1380,68],["silk skirt + sea breeze ☀","cut1",99,1470,62]]}
S['T2_rating_american_v5']={"music":M+"camille_07_rue_de_paradis.mp3","moff":30.0,"hold":0.5,
 "segs":[{"v":R+"T2K_t1.mp4","a":0.0,"b":1.8},{"v":R+"T2K_t1.mp4","a":4.5,"b":5.6,"tr":"fade:0.35"},{"v":R+"T2K_t1.mp4","a":6.6,"b":8.0,"tr":"fade:0.35"}],
 "texts":[["rating American things",0,99,232,54],["as a Parisian",0,99,300,54],["American coffee",1.0,99,1300,64],["2/10",2.4,99,1390,90]]}
S['collab_parisian_vs_colombiana_v4']={"hold":0,
 "segs":[{"v":R+"K_t1.mp4","a":0.0,"b":0.85},{"v":R+"K_t1.mp4","a":2.1,"b":3.9},{"v":R+"K_t2.mp4","a":1.2,"b":2.05}],
 "texts":[["Parisian vs. Colombiana",0,99,250,64],["rates your things",0,99,333,64],["café con leche",0.2,2.2,1290,62],["mmm… 7/10",0.85,2.2,1385,80],["arepas",2.2,99,1290,62],["9/10. don't tell Paris",2.65,99,1385,72]]}
for k,v in S.items():
    v['name']='camille_oct22_'+k; json.dump(v,open('/workspace/hf-test/zen/posting/camille_oct22/work/spec_'+k+'.json','w'))
print(list(S))
