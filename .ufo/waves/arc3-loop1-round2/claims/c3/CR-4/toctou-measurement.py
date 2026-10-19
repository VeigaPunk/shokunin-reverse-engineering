import importlib.util, os, subprocess, sys, time, hashlib, json
spec = importlib.util.spec_from_file_location('rep', '/var/tmp/cr4-arc3r2/tool/receipt-replica.py')
rep = importlib.util.module_from_spec(spec); spec.loader.exec_module(rep)
TOOL='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py'
d='/var/tmp/cr4-arc3r2/bench/toctou'; os.makedirs(d, exist_ok=True)
p=os.path.join(d,'target.json')
A=b'A'*4096; B_=b'B'*200000          # markedly different sizes -> a receipt that mixes states is provable
open(p,'wb').write(A)
stop=os.path.join(d,'stop')
if os.path.exists(stop): os.remove(stop)
writer=f'''import os,sys,time
p={p!r}; stop={stop!r}; A=b"A"*4096; B=b"B"*200000
i=0
while not os.path.exists(stop):
    with open(p,"r+b") as f:
        f.write(B if i%2 else A); f.truncate(); f.flush(); os.fsync(f.fileno())
    i+=1
'''
wf=os.path.join(d,'writer.py'); open(wf,'w').write(writer)
w=subprocess.Popen([sys.executable, wf])
time.sleep(0.3)
shaA=hashlib.sha256(A).hexdigest(); shaB=hashlib.sha256(B_).hexdigest()
inconsistent=0; N=300; sta=0; pre_mismatch=0
for i in range(N):
    rec=rep.capture(p,'v2','ns')       # replica: lstat, then path-based open (same pattern as the tool)
    if not rec.get('stable',True): sta+=1
    if rec.get('pre_read_stat_matches_fd') is False: pre_mismatch+=1
    # internal inconsistency: SIZE (from stat) vs the digest of the bytes actually read
    if (rec['size']==len(A) and rec['sha256']==shaB) or (rec['size']==len(B_) and rec['sha256']==shaA):
        inconsistent+=1
open(stop,'w').write('x'); w.wait()
out={'captures':N,'replica_internal_inconsistency':inconsistent,'replica_unstable_read':sta,
     'replica_pre_stat_mismatch':pre_mismatch,'writer_iters_hint':'see writer.py'}
print(json.dumps(out))
