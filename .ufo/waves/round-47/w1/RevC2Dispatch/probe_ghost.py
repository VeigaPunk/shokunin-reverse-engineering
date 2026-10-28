#!/usr/bin/env python3
"""Isolate the battery's third forgery: `ghost_atom` appends `- corrects path <nonexistent>`
at EOF. `corrections()` parses only the body between CORR_HEAD and the next `\n## `, so at a
card whose corrections section is followed by `## Round N` the appended line is invisible.

usage: probe_ghost.py <lane-root> <rev>
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
ghost = "\n- corrects path does/not/exist/at/any/revision.md: never\n"
out = {"rev": tip, "corrections_heading_before_next_section":
       card.index(m.CORR_HEAD) < card.index("\n## Round 4", card.index(m.CORR_HEAD))
       if m.CORR_HEAD in card else None}
for name, text in (("as-battery-appends-at-EOF", card + ghost),
                   ("inserted-inside-corrections-body",
                    card.replace(m.CORR_HEAD, m.CORR_HEAD + "\n" + ghost.strip() + "\n", 1))):
    code, rec = m.evaluate_text(text, files, root, tip, battery=None)
    out[name] = {"exit": code, "corrections": rec["corrections"],
                 "corrections_bad": [c["detail"] for c in rec["corrections_bad"]],
                 "mismatches": len(rec["mismatches"])}
print(json.dumps(out, indent=1))
sys.exit(0 if out["as-battery-appends-at-EOF"]["exit"] == 0 else 1)
