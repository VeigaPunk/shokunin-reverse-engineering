#!/usr/bin/env python3
"""Probes, second pass: E1 (two round sections), E5 (semantic reorder), E6 (flag semantics)."""
import json
import os
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r47/ConnRouted"
HEAD = "caafeffa330a15e59412bc037591f6942b51e5aa"
sys.path.insert(0, LANE + "/tools/round-47")
sys.path.insert(0, LANE + "/tools/round-46")
import gate          # noqa: E402
import record        # noqa: E402
import exact         # noqa: E402

OUT = []


def emit(label, **kw):
    OUT.append(dict(label=label, **kw))
    print(json.dumps(OUT[-1], sort_keys=True))


# ------------------------------------------------- E1: seats atom from a plan file
d = tempfile.mkdtemp(dir=S, prefix="fx-seats-")


def g(*a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


g("init", "-q")
g("config", "user.email", "fx@r47")
g("config", "user.name", "r47 fixture")
assert g("rev-parse", "--show-toplevel").stdout.strip() == d, "fixture toplevel mismatch"
base_files = {
    "tools/x/keep.md": "x\n",
    "corpus/knowledge/2026-10-01-x.md": "x\n",
    "corpus/README.md": "# readme\n\n## Coverage map\n\n- 2026-10-01-x — x\n\n## Gaps\n\ntail\n",
    "SKILL.md": "## Queue-drain craft (test) \n\n- **1. x** see `tools/x/keep.md:1`\n\n## After\n\ntail\n",
    ".ufo/waves/round-46/w1-dispatch.json": json.dumps({"counts": {"spawn": 40}}),
}
for p, body in base_files.items():
    full = os.path.join(d, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(body)
g("add", "-A")
g("commit", "-q", "-m", "base")
base = g("rev-parse", "HEAD").stdout.strip()
open(os.path.join(d, "note.md"), "w").write("n\n")
g("add", "-A")
g("commit", "-q", "-m", "tip")
tip = g("rev-parse", "HEAD").stdout.strip()
fcard = ("## Owned axes\n\n"
         "| Axis | Baseline → current score, 0–10 | Observable | Evidence | Round |\n"
         "|---|---|---|---|---|\n"
         "| coverage | 10.0 → 10.0 | 1/1 knowledge files mapped | x | r1 |\n"
         "| depth | 10.0 → 10.0 | 1/1 | x | r1 |\n\n"
         "## Round 45 — earlier, no atoms\n\nnothing.\n\n"
         "## Round 46 — x\n\nBase `%s`. Waves: 40 + 40 = 80 seats. "
         "`git log %s..%s -- tools/x/` is empty. Tree `.ufo/waves/round-46/w1-dispatch.json`.\n"
         % (base[:8], base[:8], tip[:8]))
ffiles = dict(base_files)
ffiles["SCORECARD.md"] = fcard
for label, with_w2 in (("E1-plan-only-no-w2-dispatch-file", False),
                       ("E1-with-w2-dispatch-spawn40", True)):
    f = dict(ffiles)
    if with_w2:
        f[".ufo/waves/round-46/w2-dispatch.json"] = json.dumps({"counts": {"spawn": 40}})
    code, rec = record.evaluate_text(fcard, lambda p: f.get(p), d, tip, battery=None)
    emit(label, exit=code,
         seats=[{"atom": m["atom"][:70], "derived": m["derived"]}
                for m in rec.get("mismatches", []) if m["class"] == "seats"],
         mismatch_count=len(rec.get("mismatches", [])),
         atoms_by_class=rec.get("atoms_by_class"),
         failing=rec.get("failing"))
shutil.rmtree(d, ignore_errors=True)

# -------------------------------------- E5: the literal clause vs a line-wrapped reorder
fx = exact._fixture_files(LANE, HEAD)
orig_gate = fx["tools/round-46/gate.py"]
assert orig_gate.count(exact.ORDER) == 1
wrapped = orig_gate.replace(
    exact.ORDER, '"--diff-merges=first-parent",\n            "-m"').replace(
    '    """Every path under `paths`',
    '    # clause residue: "-m", "--diff-merges=first-parent"\n    """Every path under `paths`')
assert wrapped.count(exact.ORDER) == 1 and wrapped.count(exact.REVERSED) == 0
assert wrapped != orig_gate
# syntax check: it must remain a working-looking python file
compile(wrapped, "gate_forged.py", "exec")
f = dict(fx)
f["tools/round-46/gate.py"] = wrapped
fd, frev = exact._repo(f, S)
try:
    access = lambda p, _d=fd, _r=frev: gate.show(_d, _r, p)  # noqa: E731
    code, rec = exact.score(f["SKILL.md"], access, "v3", frev, battery=None)
    emit("E5-linewrapped-reorder-with-clause-residue", exit=code,
         gate_order_literal=rec.get("gate_order_literal"),
         gate_order_reversed=rec.get("gate_order_reversed"),
         failing=rec.get("failing"), met_target=rec.get("met_target"))
finally:
    shutil.rmtree(fd, ignore_errors=True)
live = wrapped.split('r = git(root, "log",')[1][:80]
print("  forged live call:", repr(live))

# --------------------------------- E6: does the flag order actually change the output?
d2 = tempfile.mkdtemp(dir=S, prefix="fx-merge-")


def g2(*a):
    return subprocess.run(["git", "-C", d2, *a], capture_output=True, text=True)


g2("init", "-q")
g2("config", "user.email", "fx@r47")
g2("config", "user.name", "r47 fixture")
assert g2("rev-parse", "--show-toplevel").stdout.strip() == d2, "fixture toplevel mismatch"
open(os.path.join(d2, "base.md"), "w").write("b\n")
g2("add", "-A")
g2("commit", "-q", "-m", "base")
g2("checkout", "-q", "-b", "side")
open(os.path.join(d2, "side.md"), "w").write("s\n")
g2("add", "-A")
g2("commit", "-q", "-m", "side")
g2("checkout", "-q", "master" if g2("rev-parse", "--verify", "master").returncode == 0 else "main")
open(os.path.join(d2, "main.md"), "w").write("m\n")
g2("add", "-A")
g2("commit", "-q", "-m", "main")
g2("merge", "-q", "--no-ff", "-m", "merge side", "side")
merge = g2("rev-parse", "HEAD~0").stdout.strip()
first = g2("rev-parse", "HEAD~1").stdout.strip()
for label, argv in (
        ("E6-correct-order", ["log", "-m", "--diff-merges=first-parent",
                              "--name-status", "--format=%H", f"{first}..HEAD"]),
        ("E6-reversed-order", ["log", "--diff-merges=first-parent", "-m",
                               "--name-status", "--format=%H", f"{first}..HEAD"])):
    r = g2(*argv)
    emit(label, exit=r.returncode, merge_entries=r.stdout.count(merge),
         git=subprocess.run(["git", "--version"], capture_output=True,
                            text=True).stdout.strip(), argv=" ".join(argv))
shutil.rmtree(d2, ignore_errors=True)

open(os.path.join(S, "probe2-results.json"), "w").write(json.dumps(OUT, indent=1))
