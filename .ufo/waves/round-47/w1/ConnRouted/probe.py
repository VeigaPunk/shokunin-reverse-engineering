#!/usr/bin/env python3
"""ConnRouted round-47 probes: three attacks on the frozen C1/C2 instruments."""
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


# ---------------------------------------------------------------- E2: axes lines
card = gate.show(LANE, HEAD, "SCORECARD.md")
files = lambda p: gate.show(LANE, HEAD, p)  # noqa: E731


def run_card(label, text):
    code, rec = record.evaluate_text(text, files, LANE, HEAD, battery=None)
    emit(label, exit=code, corrections=rec.get("corrections"),
         corrections_bad=[b.get("detail") for b in rec.get("corrections_bad", [])],
         mismatch_classes=[m["class"] for m in rec.get("mismatches", [])],
         failing=rec.get("failing"))
    return code


run_card("E2-baseline-real-card", card)
run_card("E2-forged-axes-coverage-999",
         card.replace("corrects axes coverage: 138/138", "corrects axes coverage: 999/999"))
run_card("E2-forged-axes-depth-999",
         card.replace("corrects axes depth: 24/24", "corrects axes depth: 999/999"))
run_card("E2-ghost-axes-axis-speed",
         card.replace("corrects axes depth: 24/24", "corrects axes speed: 999/999"))
run_card("E2-control-seats-round46-true",
         card.replace("\n## Round 47 —", "\n- corrects seats round-46: 2 waves, 80 seats total\n\n## Round 47 —"))
run_card("E2-control-seats-round46-false-81",
         card.replace("\n## Round 47 —", "\n- corrects seats round-46: 3 waves, 81 seats total\n\n## Round 47 —"))

# ------------------------------------------------- E1: seats atom from a plan file
d = tempfile.mkdtemp(dir=S, prefix="fx-seats-")


def g(*a, **kw):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, **kw)


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
         "## Round 46 — x\n\nBase `%s`. Waves: 40 + 40 = 80 seats. "
         "`git log %s..%s -- tools/x/` is empty. Tree `.ufo/waves/round-46/w1-dispatch.json`.\n"
         % (base[:8], base[:8], tip[:8]))
ffiles = dict(base_files)
ffiles["SCORECARD.md"] = fcard
accessor = lambda p: ffiles.get(p)  # noqa: E731
for label, with_w2 in (("E1-plan-only-no-w2-dispatch-file", False),
                       ("E1-with-w2-dispatch-spawn40", True)):
    f = dict(ffiles)
    if with_w2:
        f[".ufo/waves/round-46/w2-dispatch.json"] = json.dumps({"counts": {"spawn": 40}})
    code, rec = record.evaluate_text(fcard, lambda p: f.get(p), d, tip, battery=None)
    emit(label, exit=code,
         seats=[{"atom": m["atom"][:60], "derived": m["derived"]}
                for m in rec.get("mismatches", []) if m["class"] == "seats"],
         mismatch_count=len(rec.get("mismatches", [])),
         atoms_by_class=rec.get("atoms_by_class"))
shutil.rmtree(d, ignore_errors=True)

# ------------------------------------------- E5: flag-order clause, semantic reorder
fx = exact._fixture_files(LANE, HEAD)
orig_gate = fx["tools/round-46/gate.py"]
assert orig_gate.count(exact.ORDER) == 1, orig_gate.count(exact.ORDER)
wrapped = orig_gate.replace(
    exact.ORDER,
    '"--diff-merges=first-parent",\n            "-m"')
commented = orig_gate.replace(
    exact.ORDER,
    '# order: "-m", "--diff-merges=first-parent"\n    ' + exact.REVERSED)
literal_swap = orig_gate.replace(exact.ORDER, exact.REVERSED)
for label, body in (("E5-live-literal-swap", literal_swap),
                    ("E5-linewrapped-reorder-plus-comment", wrapped),
                    ("E5-reversed-literal-plus-comment", commented)):
    f = dict(fx)
    f["tools/round-46/gate.py"] = body
    fd, frev = exact._repo(f, S)
    try:
        access = lambda p, _d=fd, _r=frev: gate.show(_d, _r, p)  # noqa: E731
        code, rec = exact.score(f["SKILL.md"], access, "v3", frev, battery=None)
        emit(label, exit=code,
             gate_order_literal=rec.get("gate_order_literal"),
             gate_order_reversed=rec.get("gate_order_reversed"),
             failing=rec.get("failing"))
    finally:
        shutil.rmtree(fd, ignore_errors=True)
    print("  forged gate live call:", repr(body.split("r = git(root, \"log\",")[1][:90]))

open(os.path.join(S, "probe-results.json"), "w").write(json.dumps(OUT, indent=1))
