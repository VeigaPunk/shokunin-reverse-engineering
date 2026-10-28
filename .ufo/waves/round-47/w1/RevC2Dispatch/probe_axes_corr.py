#!/usr/bin/env python3
"""Show that `- corrects axes ...` is never parsed: CORR alternation is (seats|window|path|rev).
usage: probe_axes_corr.py <lane-root> <rev>
"""
import importlib.util, json, subprocess, sys
root, rev = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("rec", root + "/tools/round-47/record.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
tip = subprocess.run(["git", "-C", root, "rev-parse", rev], capture_output=True,
                     text=True).stdout.strip()
card = subprocess.run(["git", "-C", root, "show", tip + ":SCORECARD.md"],
                      capture_output=True, text=True).stdout
def files(p):
    r = subprocess.run(["git", "-C", root, "show", tip + ":" + p], capture_output=True,
                       text=True)
    return r.stdout if r.returncode == 0 else None
def run(name, text):
    code, rec = m.evaluate_text(text, files, root, tip, battery=None)
    return {name: {"exit": code, "corrections": rec["corrections"],
                   "exempted": [a["atom"] for a in rec["exempted"]],
                   "mismatch_classes": [x["class"] for x in rec["mismatches"]],
                   "failing": rec["failing"]}}
out = {"rev": tip, "corr_regex": m.CORR.pattern, "corr_head": m.CORR_HEAD}
import re as _re
false_card = _re.sub(r"(?m)^\| coverage \|([^|]*)\|(\s*)(\d+)/(\d+)",
                     lambda m: "| coverage |%s|%s999/999" % (m.group(1), m.group(2)),
                     card, count=1)
assert false_card != card, "coverage row not matched"
out["P1_injected"] = _re.search(r"(?m)^\| coverage \|.*$", false_card).group(0)[:80]
out.update(run("P1-false-axes-claim-plus-axes-correction",
               false_card + "- corrects axes coverage: 138/138\n"))
body = card.split(m.CORR_HEAD)[1].split("\n## ", 1)[0]
kept = "\n".join(l for l in body.splitlines() if not l.startswith("- corrects"))
out.update(run("P2-axes-corrections-only",
               card.split(m.CORR_HEAD)[0] + m.CORR_HEAD + "\n" + kept
               + "\n- corrects axes coverage: 138/138\n- corrects axes depth: 23/23\n"))
print(json.dumps(out, indent=1))
sys.exit(0 if out["P2-axes-corrections-only"]["corrections"] == 0 else 1)
