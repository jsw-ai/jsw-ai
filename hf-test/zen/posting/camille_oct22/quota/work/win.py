import json,sys,statistics as s
for f in sys.argv[1:]:
    d=[(t,v) for t,v in json.load(open(f)) if v]
    best=None
    for i in range(len(d)):
        for j in range(i,len(d)):
            L=d[j][0]-d[i][0]
            if L<6.8: continue
            w=[v for _,v in d[i:j+1]]
            if min(w)>=0.72:
                sc=(s.median(w),L)
                if not best or sc>best[0]: best=(sc,d[i][0],d[j][0],min(w))
    print(f,best)
