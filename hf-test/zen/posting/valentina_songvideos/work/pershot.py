import csv,json,sys,statistics as st
n=sys.argv[1];s=json.load(open(f'{n}_shots.json'))['shots']
r=[x for x in csv.DictReader(open(f'../gate_{n}.csv')) if x['centroid']]
with open(f'../gate_pershot_{n}.csv','w') as f:
  f.write('shot,scene,kind,t0,t1,frames_scored,min,median,pass78\n')
  for x in s:
    v=[float(a['centroid']) for a in r if x['t0']<=float(a['t'])<x['t1']]
    mn=min(v) if v else None; md=st.median(v) if v else None
    f.write(f"{x['i']},{x['scene']},{x['kind']},{x['t0']:.3f},{x['t1']:.3f},{len(v)},{'' if mn is None else round(mn,4)},{'' if md is None else round(md,4)},{'no-face' if mn is None else mn>=.78}\n")
print(open(f'../gate_pershot_{n}.csv').read())
