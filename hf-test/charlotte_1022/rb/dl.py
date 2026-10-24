import re,sys,subprocess
jobs=dict(l.split()[::-1] for l in open('man/still_jobs.tsv'))
for f in sys.argv[1:]:
    for u in re.findall(r'https://\S+?\.png',open(f).read()):
        jid=re.search(r'([0-9a-f-]{36})\.png',u).group(1)
        if jid in jobs:
            subprocess.run(['curl','-s','-o',f'raw/{jobs[jid]}.png',u]); print(jobs[jid])
