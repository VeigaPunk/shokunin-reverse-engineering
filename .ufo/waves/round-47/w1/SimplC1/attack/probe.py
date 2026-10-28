#!/usr/bin/env python3
"""Forgery probe against a copy of tools/round-47/exact.py.

Calls the module's own score() with a dict-backed file reader (the same seam the
module's selftest uses) and reports exit + failing for a matrix of forged blocks.
Usage: probe.py <path-to-exact.py-copy>
"""
import hashlib
import importlib.util
import json
import os
import sys

path = sys.argv[1]
spec = importlib.util.spec_from_file_location("exact_probe", path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

src = open(path).read()
base = {"plans/round-47-claims.md": m.CLAIMS_BODY,
        "corpus/lessons/round-46.md": "lesson line\n" * 240,
        "tools/round-47/exact.py": src,
        "tools/round-46/gate.py": open(os.path.join(os.path.dirname(path),
                                                    "..", "round-46", "gate.py")).read()}
PIN = hashlib.sha256(src.encode()).hexdigest()


def run(name, skill, profile="v3"):
    files = dict(base, **{"SKILL.md": skill})
    code, rec = m.score(skill, lambda p: files.get(p), profile, "deadbeef", battery=None)
    return {"case": name, "profile": profile, "exit": code,
            "failing": rec.get("failing") or rec.get("reason"),
            "refs": rec.get("refs"), "cited": rec.get("cited")}


cases = []
cases.append(run("genuine", m.skill_text(m.good_block())))
# P1: only ONE line-selected citation; pad the ref count with SELF mentions.
cases.append(run("refs-padded-with-self-mentions", m.skill_text(m.good_block(
    refs="`corpus/lessons/round-46.md:1-2`, `tools/round-47/exact.py`"))))
# P2: the same, but with no line selector at all on the only real source.
cases.append(run("one-selector-only", m.skill_text(m.good_block(
    refs="`corpus/lessons/round-46.md:1-2`"))))
# P3: two conflicting pins; the first is correct, the second is stale.
blk = m.good_block() + "  stale pin: mutations_sha256:" + "0" * 64 + "\n"
cases.append(run("second-pin-conflicts", m.skill_text(blk)))
# P4: two conflicting interpreter pins; the first correct, the second bogus.
blk = m.good_block() + "  stale pin: interpreter_sha256:" + "0" * 64 + "\n"
cases.append(run("second-interpreter-pin-conflicts", m.skill_text(blk)))
# P5: routed id named in the v2-hole cell only (not the trigger cell).
rows = [("R46-CL2", "also R46-CL3 here", "symbol", "1"),
        ("R46-CL3", "b", "once", "1"), ("R46-CL4", "c", "digest", "1"),
        ("R46-CL6", "d", "order", "1")]
cases.append(run("id-in-hole-cell-not-trigger", m.skill_text(m.good_block(rows=rows))))
# P6: marker text parked in a non-craft section (block count stays 1).
skill = m.skill_text(m.good_block())
cases.append(run("marker-outside-craft", skill + "\n<!-- exactness-table v3 -->\n"))
# P7: a 5th all-separator line inside the table (is it a row?).
blk = m.good_block().replace("  Refs:", "| --- | --- | --- | --- |\n\n  Refs:")
cases.append(run("separator-line-in-body", m.skill_text(blk)))
# P8: arm cell with surrounding prose but exact token after strip.
rows = [(r[0], r[1], "`" + r[2] + "`", r[3]) for r in m.GOOD_ROWS]
cases.append(run("backticked-arm-token", m.skill_text(m.good_block(rows=rows))))
# P9: exit column all "1" although clause 1 rows are met (digits vs meanings).
rows = [(r[0], r[1], r[2], "1") for r in m.GOOD_ROWS]
cases.append(run("all-exit-one", m.skill_text(m.good_block(rows=rows))))
# P10: refs >= 3 met, must-cite present, but the must-cite citation is out of range.
cases.append(run("must-cite-out-of-range", m.skill_text(m.good_block(
    refs="`corpus/lessons/round-46.md:900-999`, `plans/round-47-claims.md:1`, "
         "`plans/round-47-claims.md:2`"))))
print(json.dumps(cases, indent=1))
