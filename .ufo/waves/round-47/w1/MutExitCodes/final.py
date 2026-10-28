#!/usr/bin/env python3
import json, os, subprocess, hashlib, datetime
S="/fast/scratch/hyaku/kaidoku-r47/MutExitCodes"; L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
C1=os.path.join(L,"tools/round-47/exact.py"); C2=os.path.join(L,"tools/round-47/record.py")
OUT=[]
def run(name, cmd, expect=None, note="", env_extra=None):
    env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
    if env_extra is not None:
        env.update(env_extra)
    t=datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    r=subprocess.run(cmd,capture_output=True,text=True,cwd=S,env=env,timeout=1800)
    rec={"probe":name,"utc":t,"cmd":" ".join(cmd),"env":env_extra or {},"expect":expect,
         "exit":r.returncode,"verdict":"pass" if r.returncode==expect else ("info" if expect is None else "FAIL"),
         "stdout_sha256":hashlib.sha256(r.stdout.encode()).hexdigest(),
         "stdout":r.stdout[:1200].replace("\n"," "),"stderr":r.stderr[-300:].replace("\n"," "),"note":note}
    OUT.append(rec); print(json.dumps(rec)); return rec
HEAD=subprocess.run(["git","-C",L,"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
A2="62e33f7dd75c8e3285967b26419842c106f6c965"; F1="5017e1f7299c3a812e87e7950148f54313dd279e"
A6="f54b3b6de9085d3db449ed5d0916296cb29c1f6d"; BASE="13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5"
run("c1-freeze-eq-rev-HEAD",["python3","-I","-B",C1,"--root",L,"--freeze",HEAD,"--rev",HEAD,"--no-battery"],None,"control")
run("c1-freeze-A6-rev-HEAD",["python3","-I","-B",C1,"--root",L,"--freeze",A6,"--rev",HEAD,"--no-battery"],None,"last frozen-path commit before HEAD")
run("c1-freeze-A2-rev-HEAD",["python3","-I","-B",C1,"--root",L,"--freeze",A2,"--rev",HEAD,"--no-battery"],2,"the claims' A2 paragraph names this freeze")
run("c1-freeze-F1-rev-HEAD",["python3","-I","-B",C1,"--root",L,"--freeze",F1,"--rev",HEAD,"--no-battery"],2,"the prompt's freeze commit")
run("c1-freeze-F1-rev-F1",["python3","-I","-B",C1,"--root",L,"--freeze",F1,"--rev",F1,"--no-battery"],1,"the claims' 'Before' control: block absent at the freeze")
run("c1-unknown-rev",["python3","-I","-B",C1,"--root",L,"--freeze",HEAD,"--rev","deadbeef"*5,"--no-battery"],2)
run("c1-unknown-freeze",["python3","-I","-B",C1,"--root",L,"--freeze","cafe"*10,"--rev",HEAD,"--no-battery"],2)
run("c1-nonancestor-freeze",["python3","-I","-B",C1,"--root",L,"--freeze",HEAD,"--rev",BASE,"--no-battery"],2,"freeze is a descendant of rev")
run("c1-unknown-freeze-v2-profile",["python3","-I","-B",C1,"--root",L,"--freeze","cafe"*10,"--rev",HEAD,"--profile","v2","--no-battery"],2,"the profile must not weaken the exit contract")
run("c1-battery-on-freeze-A6-rev-HEAD",["python3","-I","-B",C1,"--root",L,"--freeze",A6,"--rev",HEAD],None,"the claims' counting command (battery on)")
run("c1-selftest",["python3","-I","-B",C1,"--selftest"],None)
run("c1-selftest-no-scratch",["python3","-I","-B",C1,"--selftest"],2,"no scratch root",{"HYAKU_SCRATCH":"","TMPDIR":""})
run("c1-selftest-tmp-scratch",["python3","-I","-B",C1,"--selftest"],2,"/tmp is refused",{"HYAKU_SCRATCH":"/tmp"})
run("c2-rev-HEAD-battery",["python3","-I","-B",C2,"--root",L,"--rev",HEAD],None,"the claims' counting command (battery on)")
run("c2-rev-HEAD-nobattery",["python3","-I","-B",C2,"--root",L,"--rev",HEAD,"--no-battery"],0)
run("c2-rev-A2",["python3","-I","-B",C2,"--root",L,"--rev",A2,"--no-battery"],None,"before the landing corrections")
run("c2-rev-base",["python3","-I","-B",C2,"--root",L,"--rev",BASE,"--no-battery"],1,"the claims' 'Before': mismatches 4")
run("c2-unknown-rev",["python3","-I","-B",C2,"--root",L,"--rev","not-a-rev","--no-battery"],2)
run("c2-selftest",["python3","-I","-B",C2,"--selftest"],None)
with open(os.path.join(S,"receipts-lane.jsonl"),"w") as fh:
    for r in OUT: fh.write(json.dumps(r)+"\n")
print("\nFAIL=%d"%len([r for r in OUT if r["verdict"]=="FAIL"]))
