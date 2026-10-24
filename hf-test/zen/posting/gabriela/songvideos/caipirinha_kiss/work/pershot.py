import json,sys,statistics as st
for n in sys.argv[1:]:
  b=f'final/gabriela_caipirinha_kiss_{n}';S=json.load(open(b+'_shots.json'));P=json.load(open(b+'_pf.json'))['scores']
  for s in S['shots']:
    w=[x for t,x in P if x is not None and s['t0']<=t<s['t1']]
    print(n[:6],s['scene'],round(st.median(w),3),min(w),'OK' if st.median(w)>=.78 and min(w)>=.70 else 'BAD')
