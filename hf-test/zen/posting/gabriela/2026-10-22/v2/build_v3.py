import sys,json; sys.path.insert(0,'edit'); from mk2 import build
K='../v2/k/'
R={}
which=sys.argv[1:]
B={
'T1':('tiktok_20261022_paulistanos-thursday_v3',[('k_paul_2.mp4',0,2.8,1),(K+'kv2_ibira.mp4',0.5,4.0,1)],
  [(0,2.8,['how Paulistanos do Thursday:','Paulista at noon']),(2.8,6.5,['how Paulistanos do Thursday:','Ibirapuera at sunset'])],'07_samba_no_pe.mp3',40),
'T2':('tiktok_20261022_spvsmiami-ep1_v2',[('k2_miamiglass.mp4',0,2.6,1),(K+'kv2_beco.mp4',0,3.4,1)],
  [(0,6,['São Paulo vs Miami','ep. 1']),(0,2.6,['','','','Miami me']),(2.6,6,['','','','São Paulo me'])],'01_bom_dia_miami.mp3',50),
'T3':('tiktok_20261022_fan-reveal_v3',[('k2_fancover.mp4',0,1.0,1),(K+'kv2_wynwood.mp4',0,3.6,1)],
  [(0,1.0,['hoodie mode']),(1.0,4.6,['Wynwood mode'])],'04_golaco.mp3',45),
'REEL':('igreel_20261022_spvsmiami-ep1_v3',[(K+'kv2_havana.mp4',0.3,3.0,1),('k_paul_1.mp4',0,3.4,1)],
  [(0,6.2,['São Paulo vs Miami','ep. 1']),(0,2.7,['','','','Miami me']),(2.7,6.2,['','','','São Paulo me'])],'06_ocean_drive.mp3',20),
'Y1':('yt_20261022_caipirinha-kiss_v2',[(K+'kv2_beachbar.mp4',0,1.2,1),(K+'kv2_beachbar.mp4',3.84,5.04,1),('k2_miamisway.mp4',0,5.0,1),(K+'kv2_keybis.mp4',0,5.0,1)],
  [(0,2.4,['Caipirinha Kiss']),(2.4,7.4,['sour and sweet,',"I can't resist"]),(7.4,12.4,['lime on my lips,',"you won't forget this"])],'05_caipirinha_kiss.mp3',32),
}
for k in which:
    n,s,t,tr,ms=B[k]; R[k]=build(n,s,t,tr,ms); print(k,R[k]['file'],flush=True)
try: old=json.load(open('qc/builds_b2.json'))
except Exception: old={}
for k,v in R.items(): old[k+'_v3']=v
json.dump(old,open('qc/builds_b2.json','w'),indent=1,default=str)
