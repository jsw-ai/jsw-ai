import sys,json; sys.path.insert(0,'edit'); from mk2 import build
K='../v2/k/'
R={}
B={
'T1':('tiktok_20261022_paulistanos-thursday_v5',[(K+'k8_t1.mp4',0,4.5,1),(K+'kv2_ibira.mp4',0.5,4.0,1)],
  [(0,4.5,['how Paulistanos do Thursday:','Paulista at noon']),(4.5,8.0,['how Paulistanos do Thursday:','Ibirapuera at sunset'])],'07_samba_no_pe.mp3',40),
'T2':('tiktok_20261022_spvsmiami-ep1_v5',[(K+'kv4_t2mia.mp4',0,3.6,1),(K+'k8_t2sp.mp4',0,4.0,1)],
  [(0,7.6,['São Paulo vs Miami','ep. 1']),(0,3.6,['','','','Miami me']),(3.6,7.6,['','','','São Paulo me'])],'01_bom_dia_miami.mp3',50),
'REEL':('igreel_20261022_spvsmiami-ep1_v5',[(K+'kv2_havana.mp4',0.3,3.3,1),(K+'k8_reel.mp4',0,4.4,1)],
  [(0,7.4,['São Paulo vs Miami','ep. 1']),(0,3.0,['','','','Miami me']),(3.0,7.4,['','','','São Paulo me'])],'06_ocean_drive.mp3',20),
}
for k in sys.argv[1:]:
    n,s,t,tr,ms=B[k]; R[k]=build(n,s,t,tr,ms); print(k,R[k]['file'],flush=True)
try: old=json.load(open('qc/builds_b2.json'))
except Exception: old={}
for k,v in R.items(): old[k+'_v5']=v
json.dump(old,open('qc/builds_b2.json','w'),indent=1,default=str)
