import json,requests,sys;sys.path.insert(0,'/workspace')
from ayr_sienna import H
h={**H(True),'Profile-Key':open('/home/box/agent-data/secrets/JSW-madison-ayrshare-profile-key.txt').read().strip()}
B='https://api.ayrshare.com/api'
for i in ['tnckEIfhccMCltlIHxpb','I86L2VhmnWCXsDBExTop','wAWpaI25KwZxCSC2KPNa']:
  g=requests.get(B+'/post/'+i,headers=h).json(); print(i,g.get('status'),repr(g.get('post')),g.get('mediaUrls'),g.get('twitterOptions'),g.get('errors'))
