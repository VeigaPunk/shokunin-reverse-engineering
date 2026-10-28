#!/usr/bin/env python3
"""Generate six single-point mutants of the frozen r45 c1-counter.py.

Every replacement asserts it occurs exactly once, so a mutant is exactly one
behavior-bearing change against the pristine bytes.
"""
import hashlib
import os
import sys

S = os.path.dirname(os.path.abspath(__file__))
PRISTINE = os.path.join(S, "pristine.py")
src = open(PRISTINE).read()

MARKER_CHECK = (
    '    if block22_present != 1:\n'
    '        reasons.append(f"block22_present {block22_present} != 1")\n'
)
UNRESOLVED_CHECK = (
    '    if unresolved:\n'
    '        reasons.append(f"unresolved citations: {unresolved}")\n'
)
FROZEN_ARM = (
    '    if changed:\n'
    '        return 2, {"reason": "frozen_path_changed", "frozen_path_changed": changed}\n'
)
EXIT_CELL = ('            if exit_col is None or exit_col >= len(row) '
             'or row[exit_col].strip("` ") not in {"0", "1", "2"}:\n')

MUTANTS = {
    # (m1) equality on the rule-block count becomes a lower bound: >= 22 accepted.
    "m1-rule-blocks-ge": [("    if rule_blocks != 22:\n", "    if rule_blocks < 22:\n")],
    # (m2) the marker-presence clause no longer contributes a reason.
    "m2-skip-marker-check": [(MARKER_CHECK, "")],
    # (m3) exit cells are no longer constrained to {0,1,2}.
    "m3-any-exit-cell": [(EXIT_CELL, "            if False:\n")],
    # (m4) unresolved citations are collected but never reported.
    "m4-ignore-unresolved": [(UNRESOLVED_CHECK, "")],
    # (m5) the interpreter selftest is never executed.
    "m5-skip-selftest": [("    if run_selftest and block22_present == 1:\n", "    if False:\n")],
    # (m6) the frozen_path_changed arm (exit 2) is dropped.
    "m6-drop-frozen-arm": [(FROZEN_ARM, "")],
}

for name, edits in MUTANTS.items():
    text = src
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            sys.exit(f"{name}: anchor occurs {n} times, expected 1: {old!r}")
        text = text.replace(old, new)
    if text == src:
        sys.exit(f"{name}: no change")
    out = os.path.join(S, name + ".py")
    with open(out, "w") as fh:
        fh.write(text)
    print(name, hashlib.sha256(text.encode()).hexdigest())
    print(name, "diff-bytes", len(src.encode()) - len(text.encode()))
