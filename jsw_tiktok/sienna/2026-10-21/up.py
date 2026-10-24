# up.py toolresult dir : PUT each file named in upload URLs
import re,sys,subprocess
t=open(sys.argv[1]).read()
for mid,fn,url in re.findall(r"- ([0-9a-f-]{36}): Upload the file using: curl -X PUT -H \"Content-Type: [^\"]+\" --data-binary @(\S+) '([^']+)'",t):
    ct={'jpg':'image/jpeg','png':'image/png','mp4':'video/mp4','mp3':'audio/mpeg','wav':'audio/wav'}[fn.rsplit('.',1)[1]]
    for _ in range(3):
        r=subprocess.run(['curl','-s','-o','/dev/null','-w','%{http_code}','-X','PUT','-H','Content-Type: '+ct,'-H','If-None-Match: *','--data-binary','@'+sys.argv[2]+'/'+fn,url],capture_output=True,text=True).stdout
        if r=='200': break
    print(mid,fn,r)
