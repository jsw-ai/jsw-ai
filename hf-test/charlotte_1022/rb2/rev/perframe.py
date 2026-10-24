import sys,json,statistics
sys.path.insert(0,'/workspace/hf-test/zen/posting')
import identity_gate as g
E_,c=g.get_refs('charlotte')
out={}
for v in sys.argv[1:]:
    fr=[]
    for i,im in g.sample_frames(v,50):
        r=g.check_image(im,E_,c,ocr=False,video=True)
        fr.append(dict(frame=i,centroid=r['score_centroid'],reasons=r['reasons']))
    s=[x['centroid'] for x in fr if x['centroid'] is not None]
    out[v]=dict(frames=fr,scored=len(s),median=statistics.median(s),min=min(s),below70=sum(x<0.70 for x in s))
    print(v,len(s),round(out[v]['median'],3),round(out[v]['min'],3),out[v]['below70'])
json.dump(out,open('../rev/perframe.json','w'),indent=1)
