#!/usr/bin/env python3
"""EX-26 timing harness: interleaved A/B runs of the census instrument.

Usage: timeit.py LABEL_A pyA LABEL_B pyB RUNS ROOT OUT.tsv [--extra-args ...]
Runs alternate A,B,A,B... (5 each below) to control machine drift; each child
gets wall (perf_counter), user+sys CPU and max RSS (wait4 rusage), and its
stdout digest + verdict line so a timing pair can never be silently broken.
"""
import hashlib
import os
import resource
import subprocess
import sys
import time

lab_a, py_a, lab_b, py_b, runs, root, out_tsv = sys.argv[1:8]
extra = sys.argv[8:]
runs = int(runs)

rows = []


def one(label, py, i):
    args = [sys.executable, py, "--root", root] + extra
    t0 = time.perf_counter()
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    with open("/var/tmp/ex26/last.out", "wb") as fh, \
         open("/var/tmp/ex26/last.err", "wb") as eh:
        p = subprocess.run(args, stdout=fh, stderr=eh)
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    wall = time.perf_counter() - t0
    data = open("/var/tmp/ex26/last.out", "rb").read()
    verdict = ""
    for line in data.decode("utf-8", "replace").splitlines():
        if line.startswith("VERDICT:"):
            verdict = line.strip()
    row = {"label": label, "i": i, "wall_s": round(wall, 6),
           "cpu_s": round((r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime), 6),
           "user_s": round(r1.ru_utime - r0.ru_utime, 6),
           "sys_s": round(r1.ru_stime - r0.ru_stime, 6),
           "maxrss_kb": r1.ru_maxrss,  # high-water across all children
           "exit": p.returncode,
           "stdout_sha256": hashlib.sha256(data).hexdigest()[:16],
           "stdout_bytes": len(data),
           "verdict": verdict}
    rows.append(row)
    print("%(label)s run%(i)d wall=%(wall_s).4fs cpu=%(cpu_s).4fs exit=%(exit)d %(verdict)s sha=%(stdout_sha256)s" % row,
          flush=True)
    return row


for i in range(1, runs + 1):
    one(lab_a, py_a, i)
    one(lab_b, py_b, i)

with open(out_tsv, "w", encoding="utf-8") as fh:
    fh.write("label\trun\twall_s\tcpu_s\tuser_s\tsys_s\tmaxrss_kb\texit\tstdout_sha256\tstdout_bytes\tverdict\n")
    for r in rows:
        fh.write("\t".join(str(r[k]) for k in
                 ("label", "i", "wall_s", "cpu_s", "user_s", "sys_s", "maxrss_kb",
                  "exit", "stdout_sha256", "stdout_bytes", "verdict")) + "\n")


def med(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


print("\n== medians ==")
for lab in (lab_a, lab_b):
    w = [r["wall_s"] for r in rows if r["label"] == lab]
    c = [r["cpu_s"] for r in rows if r["label"] == lab]
    print("%s: wall median=%.6fs min=%.6f max=%.6f | cpu median=%.6fs | n=%d"
          % (lab, med(w), min(w), max(w), med(c), len(w)))
wa = [r["wall_s"] for r in rows if r["label"] == lab_a]
wb = [r["wall_s"] for r in rows if r["label"] == lab_b]
print("delta_wall_median=%.6fs ratio=%.4f" % (med(wb) - med(wa), med(wb) / med(wa)))
