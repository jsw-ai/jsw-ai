import json,re,statistics as st
rows=json.load(open('/workspace/jsw_tracker/out/pp_0700.json'))
T={}
def s(idx,tag):
  for i in idx: T[i]=tag
s([0,18,22,77,81],'thirst trap')
s([1,13,14,43,66,67,68,73,74,75,76,84,89,90,91],'punchline')
s([2,45,46,47,48,58,59,60,61],'dance')
s([9,10,19,20,21,28,29,30,31,37,38,39,40],'comedy')
s([3,11,24,25,26,27,32,33,53,54,55,56,57,62,63,64,65,69,70,71,72,86,87,88,92,111,112,113,114,115],'lifestyle')
s([4,5,41,78,79,80,82,83],'unknown')
s([6,8],'photo carousel')
s([7,12,17,23],'text-only')
s([15,42,44,49,50,51,52],'swipe/transition')
s([16,106,107,108,109],'question/engagement')
s([34,35,36],'music promo')
s([85],'intro')
s([93],'POV')
s([94,95,96,97,98,99,100,101,102,103,104,105,110],'sports reaction')
assert len(T)==len(rows), (len(T),len(rows),[i for i in range(len(rows)) if i not in T])
for i,r in enumerate(rows):
  n=r.get('Notes') or ''
  m=re.search(r'Platform: (\w+)',n); r['plat']= m.group(1) if m else r['Platform']
  if r['plat']=='Other': r['plat']='?'
  r['ctag']=T[i]
  r['newFormat']=f"{T[i]} | {r['Format']}"
json.dump(rows,open('/workspace/jsw_tracker/out/pp_0700_tagged.json','w'))
print(set(r['plat'] for r in rows))
