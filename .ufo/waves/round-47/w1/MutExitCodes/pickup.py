import json, os, subprocess, sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/MutExitCodes")
from drive2 import run, S, LANE
C1=LANE+"/tools/round-47/exact.py"; C2=LANE+"/tools/round-47/record.py"
HEAD=subprocess.run(["git","-C",LANE,"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
F1="5017e1f7299c3a812e87e7950148f54313dd279e"
run("c1-root-not-a-repo",["python3","-I","-B",C1,"--root",os.path.join(S,"not-a-repo"),
    "--freeze",HEAD,"--rev",HEAD,"--no-battery"],2,"a plain directory is not a git repo")
run("c1-root-missing",["python3","-I","-B",C1,"--root",os.path.join(S,"does-not-exist"),
    "--freeze",HEAD,"--rev",HEAD,"--no-battery"],2)
run("c2-root-not-a-repo",["python3","-I","-B",C2,"--root",os.path.join(S,"not-a-repo"),
    "--rev",HEAD,"--no-battery"],2)
run("c1-rev-noncommit-object",["python3","-I","-B",C1,"--root",LANE,"--freeze",F1,
    "--rev","HEAD:SKILL.md","--no-battery"],2,"a blob id is not a commit")
run("c1-argparse-missing-freeze",["python3","-I","-B",C1,"--root",LANE,"--rev",HEAD],2,"usage error")
run("c2-argparse-unknown-flag",["python3","-I","-B",C2,"--root",LANE,"--rev",HEAD,"--freeze","x"],2)
run("c1-jsonout-escape-symlink",["python3","-I","-B",C1,"--root",LANE,"--freeze",F1,
    "--rev",F1,"--no-battery","--json-out",os.path.join(S,"outside.json")],2,
    "--json-out outside the lane root is refused")
run("c1-selftest-with-required-args",["python3","-I","-B",C1,"--root","/nonexistent",
    "--freeze","x","--rev","y","--selftest"],0,"the liveness check itself")
run("c2-selftest-with-required-args",["python3","-I","-B",C2,"--root","/nonexistent",
    "--rev","y","--selftest"],0,"the liveness check itself")
with open(os.path.join(S,"receipts-pickup.jsonl"),"w") as fh:
    for x in []: pass
import drive2
with open(os.path.join(S,"receipts-pickup.jsonl"),"w") as fh:
    for x in drive2.OUT: fh.write(json.dumps(x)+"\n")
print("pickup rows", len(drive2.OUT))
