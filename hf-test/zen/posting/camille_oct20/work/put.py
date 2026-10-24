# usage: put.py <media_upload result file> <dir>  -- PUTs each @file to its URL (with If-None-Match), retries 520
import re,sys,subprocess,os
t=open(sys.argv[1]).read(); d=sys.argv[2]
for mid,ct,fn,url in re.findall(r"- ([0-9a-f-]{36}): .*?-H \"Content-Type: ([^\"]+)\" --data-binary @(\S+) '([^']+)'",t):
    for k in range(4):
        c=subprocess.run(['curl','-s','-o','/dev/null','-w','%{http_code}','-X','PUT','-H','Content-Type: '+ct,'-H','If-None-Match: *','--data-binary','@'+os.path.join(d,fn),url],capture_output=True,text=True).stdout
        if c=='200': break
    print(mid,fn,c)
