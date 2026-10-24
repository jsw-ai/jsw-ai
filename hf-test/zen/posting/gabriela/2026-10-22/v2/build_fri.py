import sys,json; sys.path.insert(0,'edit'); from mk2 import build
K='../v2/k/'
B={
'FT1':('tiktok_20261023_studio-warmup_v2',[(K+'k8_ft1.mp4',0,8.0,1)],[(0,8.0,['Friday warm-up in São Paulo'])],'02_rebola.mp3',30),
'FT2':('tiktok_20261023_miami-pier_v3',[(K+'k8_ft2.mp4',0,8.0,1)],[(0,8.0,['POV: Friday morning in Miami'])],'10_brisa.mp3',25),
'FT3':('tiktok_20261023_guarana-cheers_v1',[(K+'kf_t3b.mp4',0,5.0,1)],[(0,5.0,['sextou! 🇧🇷'])],'09_rio_bound.mp3',35),
'FY1':('yt_20261023_studio-day_v2',[(K+'k8_fyt1.mp4',0,8.0,1)],[(0,8.0,['new song coming soon'])],'08_lua_cheia.mp3',30),
'FY2':('yt_20261023_rooftop-night_v2',[(K+'k8_fyt2.mp4',0,8.0,1)],[(0,8.0,['São Paulo nights'])],'03_saudade_sunset.mp3',40),
}
R={}
for k in sys.argv[1:]:
    n,s,t,tr,ms=B[k]; R[k]=build(n,s,t,tr,ms); print(k,R[k]['file'],flush=True)
old=json.load(open('qc/builds_b2.json'))
for k,v in R.items(): old[k]=v
json.dump(old,open('qc/builds_b2.json','w'),indent=1,default=str)
