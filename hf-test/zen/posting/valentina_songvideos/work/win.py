import json,numpy as np
G=json.load(open('src_gate2.json'))
P='/workspace/hf-test/zen/posting/'
C=dict(kel='valentina_kling_element_test/kling_element_test.mp4',kB4='valentina_oct22/vid/kB4.mp4',kB6='valentina_oct22/vid/kB6.mp4',rk2='valentina_rosario_1021/work/k2.mp4',rk3='valentina_rosario_1021/work/k3.mp4',tt2='valentina_tiktok_oct19/raw/tt2.mp4',tt3='valentina_tiktok_oct19/raw/tt3.mp4',kS1='valentina_viral_1021/v3/kS1.mp4',kS2kit='valentina_viral_1021/v3/kS2kit.mp4',kS2pool='valentina_viral_1021/v3/kS2pool.mp4',kA2='valentina_viral_1021/work/kA2.mp4',kB1='valentina_viral_1021/work/kB1.mp4',kB2='valentina_viral_1021/work/kB2.mp4',kT1='valentina_oct22/vid/kT1.mp4',kD2='valentina_oct22/vid/kD2.mp4')
def best(k,L,avoid=None):
    per=G[P+C[k]]['per']; dur=G[P+C[k]]['dur']; res=[]
    for ss in np.arange(0.1,dur-L-0.1,0.1):
        if avoid and not (ss+L<=avoid[0] or ss>=avoid[1]): continue
        s=[x for t,x in per if ss-0.1<=t<=ss+L+0.1 and x is not None]
        if s: res.append((min(s),float(np.median(s)),round(float(ss),2)))
    return max(res)
if __name__=='__main__':
    for k in C: print(k, G[P+C[k]]['dur'], best(k,1.6), best(k,2.2))
