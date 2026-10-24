import json,re,difflib
W=json.load(open('words_med.json'))
n=lambda s:re.sub(r"[^a-z']","",s.lower())
L=[l.strip() for l in open('lyrics.txt') if l.strip()]
lw=[];owner=[]
for i,l in enumerate(L):
  for t in l.split(): lw.append(n(t));owner.append(i)
ww=[n(w[2]) for w in W]
sm=difflib.SequenceMatcher(None,lw,ww,autojunk=False)
m={}
for a,b,k in sm.get_matching_blocks():
  for j in range(k): m[a+j]=b+j
st=[None]*len(L);en=[None]*len(L)
for li,wi in m.items():
  i=owner[li];s,e=W[wi][0],W[wi][1]
  st[i]=s if st[i] is None else min(st[i],s); en[i]=e if en[i] is None else max(en[i],e)
# interpolate missing
for i in range(len(L)):
  if st[i] is None:
    p=max([j for j in range(i) if en[j] is not None],default=None); q=min([j for j in range(i+1,len(L)) if st[j] is not None],default=None)
    a=en[p] if p is not None else 10; b=st[q] if q is not None else a+4*(1)
    k=[j for j in range(len(L)) if (p is None or j>p) and (q is None or j<q)]
    d=(b-a)/len(k); st[i]=a+d*k.index(i); en[i]=st[i]+d; st[i]=st[i]; print('INTERP',i,L[i])
rows=[[round(st[i],2),round(en[i],2),L[i]] for i in range(len(L))]
for r in rows: print(r)
json.dump(rows,open('timings.json','w'),indent=0)
