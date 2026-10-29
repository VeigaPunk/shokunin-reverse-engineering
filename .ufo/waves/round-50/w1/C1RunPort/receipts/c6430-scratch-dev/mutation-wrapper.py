import subprocess, sys, os
real = os.environ['REAL']; mode = os.environ['MUT']
rc = subprocess.call([sys.executable, '-I', real] + sys.argv[1:])
if rc or '--files' not in sys.argv: sys.exit(rc)
f = sys.argv[sys.argv.index('--files')+1]; n = sys.argv[sys.argv.index('--nonregular')+1]
rows = open(f).read().split('\n')
if mode == 'sha':
    p = rows[10].split('\t'); p[1] = '0'*64; rows[10] = '\t'.join(p)
elif mode == 'drop':
    del rows[10]
elif mode == 'size':
    p = rows[10].split('\t'); p[2] = str(int(p[2])+1); rows[10] = '\t'.join(p)
elif mode == 'sym':
    nr = open(n).read().split('\n')
    for i, r in enumerate(nr):
        if '\tsymlink\t' in r:
            a = r.split('\t'); a[2] = 'zzz'; nr[i] = '\t'.join(a); break
    open(n, 'w').write('\n'.join(nr))
elif mode == 'dev':
    nr = open(n).read().split('\n')
    for i, r in enumerate(nr):
        if '\tchar-device\t' in r:
            a = r.split('\t'); a[2] = '1:1'; nr[i] = '\t'.join(a); break
    open(n, 'w').write('\n'.join(nr))
open(f, 'w').write('\n'.join(rows))
