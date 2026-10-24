import sys; sys.path.insert(0,'work')
from lib import *
F='/workspace/hf-test/zen/posting/madison_test/fin/'; S='stills/'
A=[(F+'n2_v4C.jpg',"reformer: 1. me: 0",0.5),
 (F+'m10_v4C.jpg',"and yes, i'm going back tomorrow",0.5),
 (F+'n3_v4C.jpg',"iced coffee: 1. me: 0 (i lost happily)",0.55),
 (F+'n4_v4C.jpg',"rooftop sunset: 1. me: 0",0.55),
 (F+'m9_v4C.jpg',"your bad joke: 1. me: 0 (i laughed anyway)",0.5),
 (F+'n6_v4C.jpg',"texas me: 1. new york me: 1",0.6),
 (F+'m7_v4C.jpg',"tied. don't tell the reformer",0.55)]
B=[(S+'s6.png',"me: 'one quick text'. 40 minutes later...",0.5),
 (S+'s7.png',"i see you looking over my iced coffee",0.5),
 (S+'s5.png',"over my shoulder like: you coming?",0.5),
 (S+'s3.png',"thinking about brunch. and maybe you",0.55),
 (S+'s8.png',"sun on my face, no notes",0.5),
 (S+'s4.png',"laughing at your joke. it was bad",0.5)]
import shutil;shutil.rmtree('work/m1',ignore_errors=True);shutil.rmtree('work/m2',ignore_errors=True)
T=montage(A,104,'music/track_brunch_pop.wav','montage1_scoreboard.mp4','work/m1'); print('m1',T)
T=montage(B,120,'music/track_late_night_house.wav','montage2_flirty_glances.mp4','work/m2'); print('m2',T)
