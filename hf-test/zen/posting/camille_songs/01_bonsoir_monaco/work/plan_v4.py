import json,glob,random,re
EX={'M11_rooftopa','M11_rooftopb','M11_rooftopc','M11_rooftopd','M11_rooftope','M01_harbourc','M02_heelsc','M03_casinoc','M05_balconyc','M06_yachtc','M08_carc','M09_lightsc','M01_harbourd','M02_heelsd','M07_stepsd','M01_harboure','M02_heelse','M06_yachte','M07_stepse'}
G={}
for f in glob.glob('qc/gate_K4_*.json'):
  j=json.load(open(f)); n=re.search(r'K4_(.*)_v\.mp4',j['file'])[1]
  if n in EX or j['median']<0.78 or j['min']<0.70: continue
  G[n+'_v']=j['per_frame']
def wins(pf,d):
  out=[]
  for s in [x/10 for x in range(0,int((4.9-d)*10)+1)]:
    v=[q for t,q in pf if s<=t<=s+d and q]
    if v: out.append((min(v),s))
  return sorted(out,reverse=True)
scenes=sorted({n[:3] for n in G})
P=['tiktok','igreel','fb','x','reddit']
plan={p:[] for p in P}; use={}
from collections import defaultdict
by=defaultdict(list)
for n in sorted(G): by[n[:3]].append(n)
T=[];k=0
while any(by.values()):
  for sc in scenes:
    if by[sc]: T.append(by[sc].pop(0))
L=T+T
for p_i,p in enumerate(P):
  for n in L[p_i::5][:12]:
    d=2.0 if p=='x' else 1.75; k=use.get(n,[])
    W=[w for w in wins(G[n],d) if w[0]>=0.72 and all(abs(w[1]-u)>=d for u in k)] or [w for w in wins(G[n],d) if w[0]>=0.72]
    plan[p].append((n,W[0][1],round(W[0][0],3))); use.setdefault(n,[]).append(W[0][1])
openers=['M04','M09','M06','M12','M10']
for pi,p in enumerate(P):
  r=random.Random(pi*7+1); L2=plan[p]
  while True:
    r.shuffle(L2)
    if all(L2[i][0][:3]!=L2[i+1][0][:3] for i in range(len(L2)-1)): break
  c=[x for x in L2 if x[0][:3]==openers[pi]] or L2[:1]; op=max(c,key=lambda x:x[2]); L2.remove(op); L2.insert(0,op)
  if L2[1][0][:3]==op[0][:3]:
    j=next(j for j in range(2,len(L2)) if L2[j][0][:3]!=op[0][:3] and L2[j-1][0][:3]!=op[0][:3] and (j+1>=len(L2) or L2[j+1][0][:3]!=L2[1][0][:3])); L2[1],L2[j]=L2[j],L2[1]
json.dump({p:[(n,s) for n,s,_ in plan[p]] for p in P},open('work/v4_plan.json','w'),indent=0)
json.dump(plan,open('work/v4_plan_scores.json','w'),indent=0)
for p in P: print(p,[n for n,_,_ in plan[p]])
from itertools import combinations
for a,b in combinations(P,2):
  A={(n,s) for n,s,_ in plan[a]};B={(n,s) for n,s,_ in plan[b]};An={n for n,_,_ in plan[a]};Bn={n for n,_,_ in plan[b]}
  print(a,b,'same take',len(An&Bn),'same take+window',len(A&B))
