import json,requests,sys
S='/home/box/agent-data/secrets/'
A='https://api.ayrshare.com/api'
H={"Authorization":"Bearer "+open(S+'JSW-ayrshare-api-key.txt').read().strip(),"Profile-Key":open(S+'JSW-madison-ayrshare-profile-key.txt').read().strip()}
