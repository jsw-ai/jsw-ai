import json,requests,mimetypes,os,datetime
S="/home/box/agent-data/secrets/"
a=open(S+"JSW-ayrshare-api-key.txt").read().strip();p=open(S+"JSW-charlotte-ayrshare-profile-key.txt").read().strip()
k=json.load(open(S+"x-ayrshare-consumer-keys.json"))
H={"Authorization":"Bearer "+a,"Profile-Key":p,"X-Twitter-OAuth1-Api-Key":k["consumer_key"],"X-Twitter-OAuth1-Api-Secret":k["consumer_secret"]}
A="https://app.ayrshare.com/api"
F="/workspace/hf-test/charlotte_test/fin/c%d_v4C.jpg";V="/workspace/hf-test/charlotte_video/"
C={1:"Iced latte o'clock, finally some sun ☀️ #cafe #goldenhour",
2:"Windswept and not even sorry 🌊 #beachday #boardwalk",
3:"Balcony plants are thriving, so am I 🌿 #balcony #goldenhour",
4:"Proper walk in the park before the clocks beat me 🍂 #parkwalk #autumn",
5:"Second brew, still not awake ☕ #morningroutine #tea",
6:"Caught mid-laugh, no idea what at 😂 #candid #sundayvibes",
7:"Quick stroll, quiet street, good light #citywalk",
8:"Feet in, phone away. Almost. 💦 #poolday #summer",
10:"Tea confession: I once fancied a bloke purely because he made a decent brew 🫖 #teatime #confession",
11:"Balcony dance break, neighbours can judge 💃 #dance #balcony",
12:"Rating your chat-up lines: \"Nice weather\" 5/10, you tried 😅 #chatuplines #ratings",
13:"Things I'd never admit to my mum, part one 🙈 #relatable #britishhumour"}
VF={10:"charlotte_lip2_tea_confession.mp4",11:"charlotte_dance_balcony.mp4",12:"charlotte_montage1_chatup_ratings.mp4",13:"charlotte_montage2_never_admit_to_mum.mp4"}
T={10:"Tea confession",11:"Balcony dance break",12:"Rating your chat-up lines",13:"Things I'd never admit to my mum"}
sl={"08:30":(7,30),"13:00":(12,0),"19:30":(18,30)}
plan=[("2026-10-18",[(1,"08:30"),(3,"13:00"),(5,"19:30")]),("2026-10-19",[(12,"08:30"),(2,"13:00"),(4,"19:30")]),("2026-10-20",[(10,"08:30"),(7,"13:00"),(6,"19:30")]),("2026-10-21",[(11,"08:30"),(8,"13:00"),(13,"19:30")])]
def up(path):
    n=os.path.basename(path);ct=mimetypes.guess_type(n)[0]
    j=requests.get(A+"/media/uploadUrl",params={"fileName":n,"contentType":ct},headers=H).json()
    requests.put(j["uploadUrl"],data=open(path,"rb"),headers={"Content-Type":ct}).raise_for_status()
    return j["accessUrl"]
log=open("/workspace/hf-test/charlotte_posted.log","a")
for d,items in plan:
  for n,s in items:
    vid=n in VF
    u=up(V+VF[n] if vid else F%n)
    h,m=sl[s]
    sd=d+"T%02d:%02d:00Z"%(h,m)
    body={"post":C[n],"platforms":["twitter","instagram"]+(["youtube"] if vid else []),"mediaUrls":[u],"scheduleDate":sd}
    if vid:
        body["youTubeOptions"]={"title":T[n],"shorts":True,"visibility":"public"}
        body["instagramOptions"]={"reels":True}
    r=requests.post(A+"/post",json=body,headers=H)
    j=r.json();print(n,sd,r.status_code,json.dumps(j)[:400])
    pid=j.get("id") or (j.get("posts") or [{}])[0].get("id")
    log.write("%s scheduled %s item %d twitter/instagram%s id=%s\n"%(sd,d,n,"/youtube" if vid else "",pid));log.flush()
