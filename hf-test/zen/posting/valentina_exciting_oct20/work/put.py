import re,subprocess,sys
t=open(sys.argv[1]).read()
for mid,ct,f,u in re.findall(r'- (\S+): Upload the file using: curl -X PUT -H "Content-Type: ([^"]+)" --data-binary @(\S+) \'(https://[^\']+)\'',t):
    r=subprocess.run(['curl','-s','-o','/dev/null','-w','%{http_code}','-X','PUT','-H','Content-Type: '+ct,'-H','If-None-Match: *','--data-binary','@'+f,u],capture_output=True,text=True)
    print(f,mid,r.stdout)
