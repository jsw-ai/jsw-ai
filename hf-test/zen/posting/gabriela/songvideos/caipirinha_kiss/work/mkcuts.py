import json
H=['h01_beachbar','h02_muddle','h03_fairylights','h04_moon','h05_sandals','h06_oceandrive','h08_balcony','h09_guitar','h11_boat','h12_limes','h13_boardwalk','h14_tikinight','h15_palmpath']
V=['v01_beachbar','v02_fairylights','v03_moon','v05_slipdress','v06_oceandrive','v07_sheer','v08_boatdeck','v09_limecart','v10_tikinight','v11_hammock','v12_sunsetpier','v13_rooftopbar']
VX=['v05_slipdress','v07_sheer','v08_boatdeck','v11_hammock','v01_beachbar','v12_sunsetpier','v13_rooftopbar','v06_oceandrive','v10_tikinight','v03_moon','v09_limecart','v02_fairylights']
def win(n,d,lo,hi):
  s=json.load(open(f'kl/{n}_pf.json'))['scores'];best=None
  for t0 in [round(lo+k*0.1,2) for k in range(int((hi-d-lo)/0.1)+1)]:
    w=[x for t,x in s if x is not None and t0<=t<=t0+d]
    if not w or min(w)<0.70: continue
    m=sum(w)/len(w)
    if best is None or m>best[0]: best=(m,t0)
  assert best,n; return round(best[1],3)
OV={(0.2,'v09_limecart'):(1.95,4.0),(2.4,'v09_limecart'):(2.9,5.0)}
def shots(L,D,lo,hi):
  d=round(D/len(L),3); return [dict(n=n,ss=win(n,d,*OV.get((lo,n),(lo,hi))),d=d) for n in L]
L1=[[3.0,6.6,'Caipirinha kiss'],[6.9,10.5,"Sour and sweet, I can't resist"],[10.8,14.4,"Lime on my lips, you won't forget this"],[14.6,16.8,'Caipirinha kiss']]
L2=[[3.3,7.2,'Caipirinha kiss'],[7.5,11.4,"Sour and sweet, I can't resist"],[11.7,15.6,"Lime on my lips, you won't forget this"],[15.9,19.8,'Caipirinha kiss']]
C={'hook':dict(name='gabriela_caipirinha_kiss_hook_21s_1080x1920',W=1080,H=1920,a0=46.5,dur=21.0,title=2.6,card0=17.0,br='5M',lyr=L1,shots=shots(V,21.0,0.2,2.6)),
'x':dict(name='gabriela_caipirinha_kiss_x_24s_1080x1920',W=1080,H=1920,a0=46.5,dur=24.0,title=3.0,card0=20.0,br='5M',lyr=L2,shots=shots(VX,24.0,2.4,5.0)),
'yt':dict(name='gabriela_caipirinha_kiss_youtube_21s_1920x1080',W=1920,H=1080,a0=46.5,dur=21.0,title=2.6,card0=17.0,br='8M',lyr=L1,shots=shots(H,21.0,0.2,5.0))}
json.dump(C,open('work/cuts.json','w'),indent=1)
