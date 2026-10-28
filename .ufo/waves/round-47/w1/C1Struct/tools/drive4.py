#!/usr/bin/env python3
"""C1Struct: clause-1 destruction probe and clause-8 refs-count probe."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("HYAKU_SCRATCH", HERE)
src = open(os.path.join(HERE, "drive.py")).read().split('base = show("SKILL.md")')[0]
exec(compile(src, "drive.py:prefix", "exec"))  # noqa: S102 — scratch-only reuse

base = show("SKILL.md")
out = {"cases": []}


def score_skill(tag, skill):
    files = fixture_files(skill)
    d, rev = exact._repo(files, S, prefix="c1struct-")
    try:
        f = lambda p: gate.show(d, rev, p)  # noqa: E731
        code, rec = exact.score(files["SKILL.md"], f, "v3", rev, battery=None)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    row = {"case": tag, "exit": code, "rule_blocks": rec.get("rule_blocks"),
           "marker_occurrences": rec.get("marker_occurrences"),
           "block_present": rec.get("block_present"),
           "block_is_last": rec.get("block_is_last"),
           "refs": rec.get("refs"), "failing": rec.get("failing")}
    out["cases"].append(row)
    print(json.dumps(row))


# 1. craft section reduced to block 24 alone: is the survival of blocks 1..23 bound?
head, sep, tail = base.partition("## Queue-drain craft ")
body, sep2, rest = tail.partition("\n## ")
stripped = head + sep + "\n\n" + BLOCK_B.rstrip("\n") + "\n\n## " + rest
score_skill("craft-section-stripped-to-block24", stripped)

# 2. craft section reduced to block 24 plus one decoy: same question, two blocks
stripped2 = head + sep + "\n\n- **1. Surviving decoy.** text\n\n" + BLOCK_B.rstrip("\n") \
    + "\n\n## " + rest
score_skill("craft-section-stripped-then-two-blocks", stripped2)

# 3. refs: drop the claims citation, keep two selected refs + the SELF mention
two_refs = BLOCK_B.replace(
    ", `plans/round-47-claims.md:68-90` (the predicate these rows are scored by)", "", 1)
score_skill("refs-two-selected-plus-self-mention", insert_block(base, two_refs))

# 4. refs: two selected refs and no SELF path mention at all
no_self = two_refs.replace("Interpreter `tools/round-47/exact.py` `interpreter_sha256:",
                           "Interpreter pin `interpreter_sha256:", 1)
score_skill("refs-two-selected-no-self-mention", insert_block(base, no_self))

with open(os.path.join(HERE, "destroy.json"), "w") as fh:
    json.dump(out, fh, indent=1)
