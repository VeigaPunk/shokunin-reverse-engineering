#!/usr/bin/env python3
"""P1c: is `--diff-merges=first-parent` load-bearing, and in which direction?

Compares `history_touched` alone (bypassing the blob arm, which would mask it) across
three flag forms on one merge matrix:

  A  -m --diff-merges=first-parent   (the frozen instrument)
  B  --diff-merges=first-parent -m   (the reorder R46-CL6 warns about)
  C  -m only                        (mutant m1)
  D  (no merge flags at all)         (R45-CL6's original hole, for reference)

Shapes:
  evil      the merge RESOLUTION is the only commit that touches the frozen file
  side      the SIDE COMMIT touches it and the merge keeps the result
  prefreeze the frozen file changed BEFORE the freeze; the merge introduces nothing

Direction matters: if B/C are SUPERSETS of A, the mutant over-reports (false exit 2)
and never under-reports; if any is a subset, it is a false-negative arm.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

S = os.environ["HYAKU_SCRATCH"]
FP = "tools/round-46/frozen.py"


def sh(d, *a, binary=False):
    return subprocess.run(["git", "-C", d, *a], capture_output=True,
                          text=not binary)


def build(shape):
    d = tempfile.mkdtemp(dir=S, prefix="p1c-")
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "p1c@r46"), ("user.name", "p1c")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    assert sh(d, "rev-parse", "--show-toplevel").stdout.strip() == d
    os.makedirs(os.path.join(d, "tools/round-46"), exist_ok=True)
    for rel, text in ((FP, "V0\n"), ("side.txt", "s0\n"), ("main.txt", "m0\n")):
        open(os.path.join(d, rel), "w").write(text)
    sh(d, "add", "-A")
    sh(d, "commit", "-q", "-m", "base")
    sh(d, "checkout", "-q", "-b", "side")
    if shape == "side":
        open(os.path.join(d, FP), "w").write("SIDE\n")
        sh(d, "commit", "-q", "-am", "side edits the frozen file")
    else:
        open(os.path.join(d, "side.txt"), "w").write("s1\n")
        sh(d, "commit", "-q", "-am", "side edits a non-frozen file")
    sh(d, "checkout", "-q", "main")
    if shape == "prefreeze":
        open(os.path.join(d, FP), "w").write("PRE\n")
    open(os.path.join(d, "main.txt"), "w").write("m1\n")
    sh(d, "add", "-A")
    sh(d, "commit", "-q", "-m", "mainline")
    freeze = sh(d, "rev-parse", "HEAD").stdout.strip()
    sh(d, "merge", "--no-ff", "--no-commit", "side")
    if shape == "evil":
        open(os.path.join(d, FP), "w").write("EVIL\n")
        sh(d, "add", FP)
    sh(d, "commit", "-q", "-m", "merge")
    rev = sh(d, "rev-parse", "HEAD").stdout.strip()
    return d, freeze, rev


def touched(d, freeze, rev, flags):
    r = sh(d, "log", *flags, "--name-status", "-z", "--format=",
           f"{freeze}..{rev}", "--", FP, binary=True)
    tokens = r.stdout.decode("utf-8", "surrogateescape").split("\0")
    out, i = set(), 0
    while i < len(tokens):
        if tokens[i].strip() and tokens[i].strip()[0] in "ACDMRTUXB" and i + 1 < len(tokens):
            if tokens[i + 1]:
                out.add(tokens[i + 1])
            i += 2
        else:
            i += 1
    return sorted(out)


FORMS = {"A_frozen": ["-m", "--diff-merges=first-parent"],
         "B_reorder": ["--diff-merges=first-parent", "-m"],
         "C_m_only": ["-m"],
         "D_no_flags": [],
         "E_fp_only": ["--diff-merges=first-parent"],
         "F_m_fp_fp": ["-m", "--diff-merges=first-parent", "--diff-merges=first-parent"]}

rows = []
for shape in ("evil", "side", "prefreeze"):
    d, freeze, rev = build(shape)
    try:
        row = {"shape": shape,
               "frozen_at_freeze": sh(d, "show", f"{freeze}:{FP}").stdout.strip(),
               "frozen_at_rev": sh(d, "show", f"{rev}:{FP}").stdout.strip(),
               "commits": [x for x in sh(d, "log", "--format=%s", f"{freeze}..{rev}")
                           .stdout.split("\n") if x]}
        for name, flags in FORMS.items():
            t = touched(d, freeze, rev, flags)
            row[name] = t
            row[name + "_sees"] = FP in t
        rows.append(row)
    finally:
        shutil.rmtree(d, ignore_errors=True)

print(json.dumps({"note": "touched[] for the frozen file only, per flag form", "rows": rows},
                 indent=1))
