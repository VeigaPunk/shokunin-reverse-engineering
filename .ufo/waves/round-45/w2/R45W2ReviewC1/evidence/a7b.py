import os,sys,json,subprocess,tempfile,hashlib,time
sys.path.insert(0,'/fast/scratch/hyaku/kaidoku-r45/R45W2ReviewC1')
import attack as A
d=tempfile.mkdtemp(dir=A.S,prefix="fx-latin1b-")
A.git(d,"init","-q"); A.git(d,"config","user.email","x@y"); A.git(d,"config","user.name","x")
files={"SKILL.md":A.CRAFT_HEAD+A.plain(21)+A.good_block()}
files.update(A.corpus())
for p,t in files.items():
    full=os.path.join(d,p); os.makedirs(os.path.dirname(full),exist_ok=True); open(full,"w").write(t)
blob=b"#!/usr/bin/env python3\nprint('PREFLIGHT_SELFTEST: cases=11 failures=0')\n# \xff\xfe\n"
sha=subprocess.run(["git","-C",d,"hash-object","-w","--stdin"],input=blob,capture_output=True).stdout.decode().strip()
A.git(d,"add","-A")
A.git(d,"update-index","--add","--cacheinfo",f"100755,{sha},tools/round-45/frozen-path-preflight.py")
A.git(d,"commit","-q","-m","freeze with non-utf8 interpreter")
f=A.git(d,"rev-parse","HEAD").stdout.strip()
out=os.path.join(A.OUT,"A7b-non-utf8.json")
argv=[sys.executable,"-I","-B",A.COUNTER,"--root",d,"--freeze",f,"--rev",f,"--json-out",out]
p=subprocess.run(argv,capture_output=True,text=True,env=dict(os.environ,TMPDIR=A.S,HYAKU_SCRATCH=A.S),cwd=d)
rec={"case":"A7b-non-utf8-at-freeze-and-rev","attacks":"A5: decoding of the interpreter bytes at rev",
     "expect":2,"exit":p.returncode,"ok":p.returncode==2,"met_target":None,
     "stderr_tail":p.stderr.strip().splitlines()[-1] if p.stderr.strip() else "",
     "json_out_written":os.path.exists(out),
     "stdout_sha256":hashlib.sha256(p.stdout.encode()).hexdigest(),
     "utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"argv":" ".join(argv)}
json.dump(rec,open(os.path.join(A.OUT,"A7b-non-utf8.record.json"),"w"),indent=1)
print(json.dumps(rec,indent=1))
