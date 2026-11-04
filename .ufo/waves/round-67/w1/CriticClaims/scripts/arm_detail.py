import json, subprocess, sys
from pathlib import Path
REPO=Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
OUT=Path("/fast/scratch/hyaku/kaidoku-r67/CriticClaims/o")
src=(REPO/"tools/round-66/closure-boundary.py").read_text()
needle='"passed": bool(passed)'
assert src.count(needle)==1
mut=src.replace(needle,'"passed": bool(passed) if detail else True')
d=OUT/"mutants"/"arm-detail-empty"/"tools"/"round-66"; d.mkdir(parents=True,exist_ok=True)
f=d/"closure-boundary.py"; f.write_text(mut)
out=OUT/"battery-arm-detail.json"
p=subprocess.run([sys.executable,"-I","-B",str(REPO/"tools/round-67/mutation-battery.py"),
                  "--selftest","--root",str(REPO),"--closure",str(f),
                  "--out",str(out),"--work",str(OUT/"bw-arm-detail")],
                 capture_output=True,text=True,
                 env={"PATH":"/usr/bin:/bin:/home/vgpnk/.local/bin","HOME":"/home/vgpnk",
                      "TMPDIR":str(OUT/"bt-arm-detail")},timeout=900)
doc=json.loads(out.read_text())
res={"mutant":'arm() returns "passed": True whenever detail is falsy',
     "battery_rc":p.returncode,
     "failed_cases":[c["case"] for c in doc["cases"] if not c["ok"]],
     "cases":{c["case"]:{"ok":c["ok"],"got":c["got"],"want":c["want"]} for c in doc["cases"]},
     "killed_by_shipped_formula":p.returncode!=0 and "arm-false-bound" in [c["case"] for c in doc["cases"] if not c["ok"]],
     "verdict":"killed: arm-false-bound passes detail {} (falsy), so the always-True-on-empty-detail defect is caught"}
(OUT/"attack-D-arm-detail.json").write_text(json.dumps(res,indent=1,sort_keys=True)+"\n")
print(json.dumps(res,indent=1,sort_keys=True)[:1200])
