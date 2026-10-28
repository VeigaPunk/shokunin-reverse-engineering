import subprocess
t=subprocess.run(['git','show','55bcce69:corpus/SOURCES.md'],capture_output=True,text=True).stdout
for i,l in enumerate(t.splitlines(),1):
    if l.startswith('| S138') or l.startswith('| S139'):
        c=[x.strip() for x in l.strip().strip('|').split('|')]
        print(i,'id='+c[0],'kind='+c[2],'tier='+c[3],'status='+c[7],'opened='+c[8],'recheck='+c[9],'used-by='+c[10],'ncols='+str(len(c)))
# the four load-bearing cells for every pre-existing row, base vs rev
def cells(rev):
    out={}
    txt=subprocess.run(['git','show',rev+':corpus/SOURCES.md'],capture_output=True,text=True).stdout
    for l in txt.splitlines():
        if l.startswith('| S') and l.split('|')[1].strip().startswith('S'):
            c=[x.strip() for x in l.strip().strip('|').split('|')]
            if len(c)==11: out[c[0]]=(c[7],c[9],c[10])
    return out
b,r=cells('c29360e3'),cells('55bcce69')
changed=[k for k in b if k in r and b[k]!=r[k]]
print('base_rows',len(b),'rev_rows',len(r),'added',sorted(set(r)-set(b)),'dropped',sorted(set(b)-set(r)),'status_recheck_usedby_changed',changed)
