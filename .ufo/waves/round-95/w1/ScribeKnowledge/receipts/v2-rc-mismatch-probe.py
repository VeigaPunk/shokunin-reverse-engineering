import json, os, subprocess, sys
root, work = sys.argv[1], sys.argv[2]
fx = os.path.join(work, "rcfix"); os.makedirs(fx, exist_ok=True)
for f in os.listdir(fx): os.remove(os.path.join(fx,f))
rec = {"label": "repaired 0 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 0 of 12; fresh-roundtrip 0 of 2",
       "met_target": False, "exit": 1,
       "counts": {"repaired":0,"scored":12,"wrong":0,"unsafe":0,"intact":6,"far_refused":0,"far":12,"fresh_roundtrip":0,"fresh_scored":2},
       "revision": "b5331db1fb0ce0bf93695ce1730cf831effef6a9",
       "verdict_sha256": "x"*64, "counter_sha256": "y"*64, "tool": "tools/round-94/stop-boundary-repair-battery-v4.py"}
open(os.path.join(fx,"p-F1.json"),"w").write(json.dumps(rec))
open(os.path.join(fx,"p-F1.stdout"),"w").write(rec["label"] + " met False exit 1\n")
open(os.path.join(fx,"p-F1.rc"),"w").write("7\n")   # rc disagrees with the receipt's exit 1
out = subprocess.run([sys.executable, "-I", "-B", os.path.join(root,"tools/round-95/c1-agreement-v2.py"),
                      "--root", root, "--dir", fx, "--prefix", "p", "--case", "F1",
                      "--rev", "b5331db1fb0ce0bf93695ce1730cf831effef6a9",
                      "--expect", "repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2"],
                     capture_output=True, text=True)
d = json.loads(out.stdout)
print("rc", out.returncode, "reasons:", d["rows"][0]["reasons"])
