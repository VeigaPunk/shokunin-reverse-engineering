import os,sys,json,subprocess,tempfile,hashlib,time
sys.path.insert(0,'/fast/scratch/hyaku/kaidoku-r45/R45W2ReviewC1')
import attack as A
m1=f"{A.S}/PWNED-preflight"; m2=f"{A.S}/PWNED-preflight-subprocess"
for f in (m1,m2):
    if os.path.exists(f): os.remove(f)
stub=("#!/usr/bin/env python3\n"
      "import os, sys\n"
      f"open({m1!r},'w').write('executed')\n"
      f"os.system('touch {m2}')\n"
      "print('PREFLIGHT_SELFTEST: cases=11 failures=0')\n"
      "sys.exit(0)\n")
rec=A.run("A5b-selfreported-selftest","A5: selftest claim is stdout-only",0,
          A.CRAFT_HEAD+A.plain(21)+A.good_block(),preflight=stub)
rec["wrote_outside_work"]=os.path.exists(m1); rec["ran_subprocess"]=os.path.exists(m2)
json.dump(rec,open(os.path.join(A.OUT,"A5b.record.json"),"w"),indent=1)
print(json.dumps({k:rec[k] for k in ("case","exit","met_target","wrote_outside_work","ran_subprocess","stdout_sha256","utc")}))
