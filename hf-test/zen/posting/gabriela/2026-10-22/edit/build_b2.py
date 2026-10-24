import sys,json; sys.path.insert(0,'edit'); from mk2 import build
R={}
R['ep1']=build('tiktok_20261022_spvsmiami-ep1_v1',[('k2_miamiglass.mp4',0,2.6,1),('k2_knitstep.mp4',0,3.4,1)],
  [(0,6,['São Paulo vs Miami','ep. 1']),(0,2.6,['','','','Miami me']),(2.6,6,['','','','São Paulo me'])],'01_bom_dia_miami.mp3',8)
R['paul']=build('tiktok_20261022_paulistanos-thursday_v2',[('k2_knitbsway.mp4',0,2.8,1),('k2_roofglass.mp4',0.5,4.0,1)],
  [(0,2.8,['how Paulistanos do Thursday:','Paulista at noon']),(2.8,6.5,['how Paulistanos do Thursday:','rooftop by night'])],'07_samba_no_pe.mp3',20)
R['fan']=build('tiktok_20261022_fan-reveal_v1',[('k2_fancover.mp4',0,1.2,1),('k2_knitsway.mp4',0,3.6,1)],
  [(0,1.2,['hoodie mode']),(1.2,5,['Paulista mode'])],'04_golaco.mp3',30)
R['yt']=build('yt_20261022_caipirinha-kiss_v1',[('k2_roofglass.mp4',0,4.5,1),('k2_paulbrisk.mp4',0,4.0,1),('k2_knitbsway.mp4',0.5,4.5,1)],
  [(0,4.5,['Caipirinha kiss']),(4.5,8.5,['sour and sweet,',"I can't resist"]),(8.5,12.5,['lime on my lips,',"you won't forget this"])],'05_caipirinha_kiss.mp3',32)
json.dump(R,open('qc/builds_b2.json','w'),indent=1,default=str); print({k:v['file'] for k,v in R.items()})
