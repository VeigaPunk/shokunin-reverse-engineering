#!/usr/bin/env python3
# Detector D-main (supplementary, not in the frozen kill rule): drives the v5 public main()
# in-process with a faked verdict (v3.score), so the receipt-writer + self-verify + fail-closed
# exit path is exercised. Prints one line per scenario: name exit.
import contextlib, importlib.util, io, os, sys
clone, work = sys.argv[1], sys.argv[2]
DECL = "4bda1d1dd3788973f10e61212b70df18b3b14ea0"
FROZEN = ("repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; "
          "fresh-roundtrip 2 of 2")
spec = importlib.util.spec_from_file_location(
    "v5under", os.path.join(clone, "tools/round-95/stop-boundary-repair-battery-v5.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
base = {"repaired": 12, "scored": 12, "wrong": 0, "unsafe": 0, "intact": 6, "far": 12,
        "far_refused": 12, "fresh_roundtrip": 2, "fresh_scored": 2}
other_counts = dict(base, far_refused=11)
scen = {
    "pos":        (DECL, FROZEN, base),
    "shortrev":   (DECL[:9], FROZEN, base),
    "rewrite":    (DECL, mod.recompute_label(other_counts, 6), other_counts),
    "notrecomp":  (DECL, FROZEN, dict(base, repaired=11)),
}
os.makedirs(work, exist_ok=True)
for name, (rev, label, counts) in scen.items():
    def fake(args, _label=label, _counts=counts):
        return 0, {"class": "detector", "label": _label, "met_target": True, "exit": 0,
                   "counts": _counts, "revision": args.rev, "fresh_cells": []}
    mod.v3.score = fake
    out = os.path.join(work, "d-main-%s.json" % name)
    with contextlib.redirect_stdout(io.StringIO()) as so, contextlib.redirect_stderr(io.StringIO()) as se:
        code = mod.main(["--root", clone, "--work", os.path.join(work, "w-" + name),
                         "--rev", rev, "--expect", FROZEN, "--json-out", out])
    reasons = [l for l in se.getvalue().splitlines() if l.startswith("selfverify reason")]
    print("D-main %-10s exit %d  %s" % (name, code, "; ".join(reasons) or "-"))
