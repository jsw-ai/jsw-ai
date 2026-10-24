import sys,glob,numpy as np,cv2
sys.path.insert(0,'/workspace/hf-test/zen/posting')
import identity_gate as g
def emb(p):
    im=cv2.imread(p); f,_=g.faces(im)
    if not f: return None,None
    x=max(f,key=lambda x:(x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
    return x.normed_embedding,x
P='/workspace/hf-test/zen/posting/'
refs={}
for p in sorted(glob.glob(P+'valentina_test2/fin/s*_v4C.jpg')): 
    if 'try' in p: continue
    refs['t2_'+p.split('/')[-1][:5]]=p
for p in glob.glob(P+'valentina_video3/work/f*.png'): refs['cafe_'+p.split('/')[-1]]=p
refs['cafe_start']=P+'valentina_video3/work/start.jpg'
for k in ['cover','bikini1','bikini2']: refs[k]=P+f'valentina_refs/valentina_{k}.jpg'
refs['REJECTED_v4']=P+'valentina_video4_x/work/f3.png'
E={}
for k,p in refs.items():
    e,_=emb(p)
    if e is not None:E[k]=e
good=[k for k in E if not k.startswith('REJ')]
c=np.mean([E[k] for k in good if k.startswith(('t2','cafe','cover','bikini'))],0);c/=np.linalg.norm(c)
print('REJECTED vs centroid',float(E['REJECTED_v4']@c))
for t in sys.argv[1:]:
    e,_=emb(t)
    if e is None: print(t,'noface');continue
    print(t,'centroid %.3f'%float(e@c))
    print('  '+' '.join('%s:%.2f'%(k,float(e@E[k])) for k in E))
