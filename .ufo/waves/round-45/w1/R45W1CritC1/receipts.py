import hashlib,json,os,subprocess,sys,datetime
S="/fast/scratch/hyaku/kaidoku-r45/R45W1CritC1"
COUNTER=os.path.join(S,"counter.py")
env=dict(os.environ,TMPDIR=S,HYAKU_SCRATCH=S)
rows=[]
def utc(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def run(label,d,freeze,rev,extra=()):
    cmd=[sys.executable,"-I","-B",COUNTER,"--root",d,"--freeze",freeze,"--rev",rev,*extra]
    p=subprocess.run(cmd,capture_output=True,text=True,env=env,timeout=900)
    rows.append({"label":label,"cmd":" ".join(cmd),"cwd":d,"exit":p.returncode,
                 "stdout_sha256":hashlib.sha256(p.stdout.encode()).hexdigest(),
                 "stdout_head":p.stdout.strip().splitlines()[-1][:300] if p.stdout.strip() else "",
                 "stderr_sha256":hashlib.sha256(p.stderr.encode()).hexdigest(),
                 "stderr_tail":p.stderr.strip().splitlines()[-1][:160] if p.stderr.strip() else "",
                 "utc":utc()})
    print(json.dumps({k:rows[-1][k] for k in ("label","exit","stdout_sha256","utc")}))
for d in sorted(os.listdir(S)):
    if not d.startswith(("fx-","fx2-")): continue
    path=os.path.join(S,d)
    freeze=subprocess.run(["git","-C",path,"rev-list","--max-parents=0","HEAD"],capture_output=True,text=True).stdout.strip()
    head=subprocess.run(["git","-C",path,"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
    rev=freeze if d=="fx-a1-do-nothing" else head
    run(d,path,freeze,rev)
R="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
run("real-freeze-do-nothing",R,"f762b7273e3f6ca3c710bb37d5de92a4a4417aec","f762b7273e3f6ca3c710bb37d5de92a4a4417aec")
run("real-head",R,"f762b7273e3f6ca3c710bb37d5de92a4a4417aec","HEAD")
run("counter-selftest",R,"","",("--selftest",))
json.dump(rows,open(os.path.join(S,"receipts.json"),"w"),indent=1)
