#!/usr/bin/env python3
"""EX-26: low-noise in-process timing of the census main().

Loads two instrument revisions as modules and alternates calls to main()
(same interpreter, same page cache, same stdout sink), so the delta isolates
the instruments' own work from interpreter startup. Usage:

  inproc.py pyA pyB ROOT ITERS OUT.tsv
"""
import importlib.util
import io
import os
import resource
import sys
import time

py_a, py_b, root, iters, out_tsv = sys.argv[1:6]
iters = int(iters)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


A = load(py_a, "inst_a")
B = load(py_b, "inst_b")
devnull = open(os.devnull, "w")
rows = []


def one(tag, mod, i):
    sys.argv = ["census", "--root", root]
    old, olderr = sys.stdout, sys.stderr
    sys.stdout = devnull
    t0 = time.perf_counter()
    rc = mod.main()
    dt = time.perf_counter() - t0
    sys.stdout, sys.stderr = old, olderr
    rows.append((tag, i, dt, rc))
    return dt, rc


for i in range(iters):
    one("A", A, i)
    one("B", B, i)

devnull.close()
with open(out_tsv, "w", encoding="utf-8") as fh:
    for tag, i, dt, rc in rows:
        fh.write("%s\t%d\t%.6f\t%d\n" % (tag, i, dt, rc))


def stats(xs):
    xs = sorted(xs)
    n = len(xs)
    med = xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2
    return med, xs[0], xs[-1]


for tag in ("A", "B"):
    xs = [dt for t, i, dt, rc in rows if t == tag]
    med, lo, hi = stats(xs)
    print("%s: median=%.6fs min=%.6fs max=%.6fs n=%d rc_set=%s"
          % (tag, med, lo, hi, len(xs), sorted({rc for t, i, dt, rc in rows if t == tag})))
ma = stats([dt for t, i, dt, rc in rows if t == "A"])[0]
mb = stats([dt for t, i, dt, rc in rows if t == "B"])[0]
print("delta_median=%.6fs ratio=%.4f (A=%s B=%s root=%s iters=%d)"
      % (mb - ma, mb / ma, os.path.basename(py_a), os.path.basename(py_b), root, iters))
