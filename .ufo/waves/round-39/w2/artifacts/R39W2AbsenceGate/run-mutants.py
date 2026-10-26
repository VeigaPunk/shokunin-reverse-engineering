#!/usr/bin/env python3
"""Run --selftest against every mutant; classify KILLED / SURVIVED."""
import hashlib
import os
import subprocess

S = os.path.dirname(os.path.abspath(__file__))
os.chdir(S)
os.makedirs("out", exist_ok=True)
env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH="/fast/scratch/hyaku")

rows = []
for fn in sorted(os.listdir("mut")):
    if not fn.endswith(".py"):
        continue
    name = fn[:-3]
    try:
        p = subprocess.run(["timeout", "120", "python3", "-I", "-B", os.path.join("mut", fn),
                            "--selftest"],
                           capture_output=True, text=True, env=env, timeout=150)
        rc, out = p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired as exc:
        rc, out = "TIMEOUT", (exc.stdout or b"").decode(errors="replace") + (exc.stderr or b"").decode(errors="replace")
    with open(os.path.join("out", "st-%s.txt" % name), "w") as fh:
        fh.write(out)
    fails = [l for l in out.splitlines() if l.startswith("FAIL")]
    lines = [l for l in out.strip().splitlines() if l.strip()]
    last = lines[-1] if lines else "(no output)"
    verdict = "SURVIVED" if rc == 0 else "KILLED"
    digest = hashlib.sha256(open(os.path.join("mut", fn), "rb").read()).hexdigest()
    rows.append((name, rc, verdict, len(fails), digest, last, fails))

for name, rc, verdict, nfails, digest, last, fails in rows:
    print("%-32s rc=%-4s %-8s failing_cases=%d" % (name, rc, verdict, nfails))
    print("    sha256=%s" % digest)
    print("    %s" % last)
    for f in fails:
        print("    %s" % f)
print("total=%d" % len(rows))
