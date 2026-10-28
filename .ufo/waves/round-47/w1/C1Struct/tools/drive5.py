#!/usr/bin/env python3
"""C1Struct: isolate clause 8's `refs >= 3` count — does the bare interpreter path count?"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("HYAKU_SCRATCH", HERE)
src = open(os.path.join(HERE, "drive.py")).read().split('base = show("SKILL.md")')[0]
exec(compile(src, "drive.py:prefix", "exec"))  # noqa: S102 — scratch-only reuse

base = show("SKILL.md")
TWO = ("  Refs: `corpus/lessons/round-46.md:57-59` (R46-CL2, the substring arm), "
       "`plans/round-47-claims.md:68-90` (the predicate).")

lines = BLOCK_B.splitlines()
refs_at = next(i for i, l in enumerate(lines) if l.startswith("  Refs: "))
two_refs = "\n".join(lines[:refs_at] + [TWO]) + "\n"
no_self = two_refs.replace("Interpreter `tools/round-47/exact.py` `interpreter_sha256:",
                           "Interpreter pin `interpreter_sha256:", 1)

out = {"cases": []}
for tag, block in (("two-selected-refs-plus-bare-self-path", two_refs),
                   ("two-selected-refs-no-self-path", no_self)):
    files = fixture_files(insert_block(base, block))
    d, rev = exact._repo(files, S, prefix="c1struct-")
    try:
        f = lambda p: gate.show(d, rev, p)  # noqa: E731
        code, rec = exact.score(files["SKILL.md"], f, "v3", rev, battery=None)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    row = {"case": tag, "exit": code, "refs": rec.get("refs"),
           "cited": rec.get("cited"),
           "unresolved_citations": rec.get("unresolved_citations"),
           "failing": rec.get("failing")}
    out["cases"].append(row)
    print(json.dumps(row))
with open(os.path.join(HERE, "refs-count.json"), "w") as fh:
    json.dump(out, fh, indent=1)
