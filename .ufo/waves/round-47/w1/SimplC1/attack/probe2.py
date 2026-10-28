#!/usr/bin/env python3
"""Candidate selftest cases: does the check already bite when the case is supplied?
Each case is a block the current counter should score red; a red here proves the
check works and only the selftest case is missing.
"""
import hashlib
import importlib.util
import json
import os
import sys

path = sys.argv[1]
spec = importlib.util.spec_from_file_location("exact_probe2", path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
src = open(path).read()
base = {"plans/round-47-claims.md": m.CLAIMS_BODY,
        "corpus/lessons/round-46.md": "lesson line\n" * 240,
        "tools/round-47/exact.py": src,
        "tools/round-46/gate.py": open(os.path.join(os.path.dirname(path),
                                                    "..", "round-46", "gate.py")).read()}
PIN = hashlib.sha256(src.encode()).hexdigest()


def run(name, skill, expect=None, battery=None):
    files = dict(base, **{"SKILL.md": skill})
    code, rec = m.score(skill, lambda p: files.get(p), "v3", "deadbeef", battery=battery)
    return {"case": name, "expect": expect, "exit": code,
            "failing": rec.get("failing") or rec.get("reason")}


cases = []
# block not last: a 25th block after the marked one
cases.append(run("red-block-not-last",
                 m.skill_text(m.good_block()).replace("## Next section",
                                                      "- **25. later rule.** body\n\n## Next section"), 1))
# a row with three cells only
rows = [("R46-CL2", "a", "symbol"), ("R46-CL3", "b", "once", "1"),
        ("R46-CL4", "c", "digest", "1"), ("R46-CL6", "d", "order", "1")]
cases.append(run("red-row-three-cells", m.skill_text(m.good_block(rows=rows)), 1))
# exit cell outside {0,1,2}
rows = [r[:3] + ("3",) for r in m.GOOD_ROWS]
cases.append(run("red-exit-outside", m.skill_text(m.good_block(rows=rows)), 1))
# mutation names absent from the block text
blk = (m.good_block().replace("names substring-arm, duplicate-routed-id, "
                              "stale-mutations-digest, flag-order-drift.", "names the mutations."))
cases.append(run("red-names-absent", m.skill_text(blk), 1))
# must-cite absent
cases.append(run("red-must-cite-absent", m.skill_text(m.good_block(
    refs="`plans/round-47-claims.md:1-2`, `plans/round-47-claims.md:3-4`, "
         "`plans/round-47-claims.md:5-6`")), 1))
# inverted citation range
cases.append(run("red-ref-range-inverted", m.skill_text(m.good_block(
    refs="`corpus/lessons/round-46.md:60-10`, `plans/round-47-claims.md:1`, "
         "`plans/round-47-claims.md:2`")), 1))
# battery counters wrong
cases.append(run("red-battery-counts", m.skill_text(m.good_block()),
                 battery={"forgeries_total": 3, "v2_green": 4, "v3_green": 0,
                          "genuine_green": 1, "crash": 0}, expect=1))
# a valid-path citation that is absent at rev (isolates the dangling check from the allowlist)
cases.append(run("red-ref-absent-at-rev", m.skill_text(m.good_block(
    refs="`corpus/lessons/round-46.md:1-2`, `corpus/lessons/round-44.md:1`, "
         "`plans/round-47-claims.md:2`")), 1))
print(json.dumps(cases, indent=1))
