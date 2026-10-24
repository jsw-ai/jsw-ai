import json,sys,statistics
g=json.load(open(sys.argv[1])); ks=sorted(g); sc=[g[k].get('score_centroid') for k in ks]
v=[s for s in sc if s is not None]
print(sys.argv[1],'n=%d scored=%d median=%.3f min=%.3f <.70=%d <.78=%d'%(len(sc),len(v),statistics.median(v),min(v),sum(s<.7 for s in v),sum(s<.78 for s in v)))
print(' '.join('%.2f'%s if s is not None else '--' for s in sc))
