#!/usr/bin/env python3
"""EX-23: characterize the selftest flake seen once in census.py run 1
(guardA: no summary line, Traceback on stderr). 6 reps per variant."""
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
VARIANTS = {
    "baseline": os.path.join(BASE, "head-citation-drift-probe.py"),
    "guardA": os.path.join(BASE, "guardA.py"),
    "guardB": os.path.join(BASE, "guardB.py"),
    "guardC": os.path.join(BASE, "guardC.py"),
}
EXP = {"baseline": os.path.join(BASE, "head-expected.json"),
       "guardA": os.path.join(BASE, "expected-with-pin.json"),
       "guardB": os.path.join(BASE, "expected-with-pin.json"),
       "guardC": os.path.join(BASE, "expected-13.json")}

for name, probe in VARIANTS.items():
    tally = {}
    tb_tail = []
    for rep in range(6):
        p = subprocess.run([sys.executable, probe, "--selftest",
                            "--expected", EXP[name]],
                           capture_output=True, text=True, timeout=300)
        summary = [l for l in p.stdout.splitlines()
                   if l.startswith("CITATION_DRIFT_SELFTEST:")]
        s = summary[0] if summary else "<no-summary>"
        key = "exit=%d %s" % (p.returncode, s)
        tally[key] = tally.get(key, 0) + 1
        if "Traceback" in p.stderr:
            tb_tail.append(p.stderr.strip().splitlines()[-4:])
    print("== %s (6 reps) ==" % name)
    for k, v in tally.items():
        print("   %dx %s" % (v, k))
    for t in tb_tail:
        print("   TRACEBACK TAIL: %s" % t)
