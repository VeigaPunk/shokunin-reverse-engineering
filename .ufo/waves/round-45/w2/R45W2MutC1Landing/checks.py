import json, os, subprocess, sys, hashlib, time
LANE="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
C=LANE+"/tools/round-45/c1-counter.py"
S="/fast/scratch/hyaku/kaidoku-r45/R45W2MutC1Landing"
REP=LANE+"/.ufo/waves/round-45/w2/R45W2MutC1Landing"
def run(root,freeze,rev,tag):
    out=f"{REP}/check-{tag}.json"; t=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
    env=dict(os.environ,TMPDIR=S+"/tmp",HYAKU_SCRATCH=S+"/tmp"); os.makedirs(env["TMPDIR"],exist_ok=True)
    p=subprocess.run([sys.executable,"-I","-B",C,"--root",root,"--freeze",freeze,"--rev",rev,"--json-out",out],capture_output=True,text=True,env=env)
    r={"tag":tag,"utc":t,"exit":p.returncode,"cmd":f"python3 -I -B {C} --root {root} --freeze {freeze} --rev {rev} --json-out {out}",
       "stdout_sha256":hashlib.sha256(p.stdout.encode()).hexdigest()}
    try: r["receipt"]=json.loads(p.stdout)
    except Exception: r["receipt"]=None; r["stdout"]=p.stdout[:500]; r["stderr"]=p.stderr[-500:]
    return r
F="f762b7273e3f6ca3c710bb37d5de92a4a4417aec"
checks=[run(LANE,F,"1f4b27f82353d6544dc0c8048b3cfdadd8525d12","rev-A1-1f4b27f8"),
        run(LANE,F,F,"do-nothing-at-freeze"),
        run(LANE,F,"a63d109faa050207d4c184471889049741c9ebbf","rev-HEAD-a63d109f"),
        run(LANE,F,"e715263cb51b713c342ab992d527fe9d61d6f8ff","rev-landing-e715263c")]
# pristine fixture (m0)
base=S+"/base"; fx=S+"/fixtures/m0-pristine"
subprocess.run(["rm","-rf",fx]); subprocess.run(["cp","-a",base,fx])
for c in (["init","-q"],["config","user.email","mut@r45"],["config","user.name","r45 mutant"]):
    subprocess.run(["git","-C",fx]+c,capture_output=True)
top=subprocess.run(["git","-C",fx,"rev-parse","--show-toplevel"],capture_output=True,text=True).stdout.strip()
assert os.path.realpath(top)==os.path.realpath(fx),(top,fx)
subprocess.run(["git","-C",fx,"add","-A"],capture_output=True)
subprocess.run(["git","-C",fx,"commit","-q","-m","freeze"],capture_output=True)
f0=subprocess.run(["git","-C",fx,"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
checks.append(run(fx,f0,f0,"m0-pristine-fixture"))
json.dump(checks,open(REP+"/checks.json","w"),indent=1,sort_keys=True)
for c in checks:
    r=c["receipt"] or {}
    print(c["tag"],c["exit"],{k:r.get(k) for k in ("rule_blocks","block22_present","block22_rows","block22_refs","block22_unresolved_citations","block22_cites","preflight_selftest","met_target","failing","reason")})
