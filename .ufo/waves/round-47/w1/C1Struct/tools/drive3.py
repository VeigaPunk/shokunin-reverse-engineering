#!/usr/bin/env python3
"""C1Struct: clause-8 citation probes with record.py present in the fixture."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
src = open(os.path.join(HERE, "drive.py")).read().split('base = show("SKILL.md")')[0]
exec(compile(src, "drive.py:prefix", "exec"))  # noqa: S102 — scratch-only reuse

NEEDED.append("tools/round-47/record.py")
base = show("SKILL.md")

variants = {
    "cite-gate46-99": ", `tools/round-46/gate.py:99` (the flag-order literal)",
    "cite-record47-242-260": ", `tools/round-47/record.py:242-260` (the corrections re-derivation)",
    "cite-record47-no-selector": ", `tools/round-47/record.py` (no selector)",
    "cite-round46-no-selector": ", `corpus/lessons/round-46.md` (no selector)",
    "cite-round46-out-of-range": ", `corpus/lessons/round-46.md:400-420` (past the file)",
    "cite-absent-knowledge": ", `corpus/knowledge/nonexistent-r47.md:1`",
}

out = {"cases": []}
for tag, extra in variants.items():
    block = BLOCK_B.replace("(the predicate these rows are scored by).",
                            "(the predicate these rows are scored by)" + extra + ".", 1)
    files = fixture_files(insert_block(base, block))
    d, rev = exact._repo(files, S, prefix="c1struct-")
    try:
        f = lambda p: gate.show(d, rev, p)  # noqa: E731
        code, rec = exact.score(files["SKILL.md"], f, "v3", rev, battery=None)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    row = {"case": tag, "exit": code, "failing": rec.get("failing"),
           "refs": rec.get("refs"), "cited": rec.get("cited"),
           "unresolved_citations": rec.get("unresolved_citations")}
    out["cases"].append(row)
    print(json.dumps(row))
with open(os.path.join(HERE, "cites.json"), "w") as fh:
    json.dump(out, fh, indent=1)
