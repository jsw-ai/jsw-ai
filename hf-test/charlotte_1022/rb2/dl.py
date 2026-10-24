import re,subprocess,sys
jobs={l.split()[1]:l.split()[0] for l in open('man/still_jobs.tsv')}
for f in sys.argv[1:]:
    for u in re.findall(r'https://\S+?\.png',open(f).read()):
        j=re.search(r'([0-9a-f-]{36})\.png',u).group(1); subprocess.run(['curl','-s','-o',f'raw/{jobs[j]}.png',u]); print(jobs[j],end=' ')
