import json, os, sys, importlib.util, shutil
S=os.environ["HYAKU_SCRATCH"]; LANE=os.path.join(S,"lane")
spec=importlib.util.spec_from_file_location("kr2", os.path.join(LANE,"tools/round-96/kill-rule-v2.py"))
kr=importlib.util.module_from_spec(spec); spec.loader.exec_module(kr)
mutants=json.load(open(os.path.join(LANE,".ufo/waves/round-96/mutants.json")))
FROZEN=("repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2")
HEAD=open(os.path.join(S,"repro/head.txt")).read().split("=")[1].strip()
# P2: degenerate probe that always reports followed-symlink (ignores the writer)
P2={"name":"P2","kind":"probe","file":"tools/round-96/symlink-probe-v2.py",
    "find":"    ok = victim_intact and receipt_valid","replace":"    ok = False",
    "kills_via":"attack: degenerate probe, always followed-symlink"}
d=os.path.join(S,"kr-attack-work","P2"); shutil.rmtree(d,ignore_errors=True)
res=kr.run_mutant("P2",P2,LANE,FROZEN,HEAD,d,[],os.path.join(LANE,".ufo/waves/round-95/forgery"),
   "tools/round-94/stop-boundary-repair-battery-v4.py",".ufo/waves/round-93/controls/identity_noop.py",
   "tools/round-96/stop-boundary-repair-battery-v6.py","tools/round-92/upx-stop-boundary-search-repair.py")
print("P2 killed=",res["killed"], json.dumps(res["checks"],default=str)[:600])
# repro: which check killed each M-mutant, from the frozen repro json
rep=json.load(open(os.path.join(S,"repro/c1-kill-rule-at-head.json")))
for m in rep["mutants"]:
    bad=[k for k,v in m["checks"].items() if not v.get("ok")]
    print(m["name"], m["kind"], "killed=",m["killed"], "failing=",bad)
print("honest:", {k:(v.get("ok") if isinstance(v,dict) else v) for k,v in rep["honest"].items()})
print("K-probe honest:", rep["honest"]["K-probe"])
