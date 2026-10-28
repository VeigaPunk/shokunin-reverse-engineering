#!/usr/bin/env python3
"""CritBattery: score C1 forgery variants against the frozen exact.py scorer.

Read-only: imports tools/round-47/exact.py from the lane; every fixture repo is in scratch.
Prints one JSON object per case: name, v2_exit, v3_exit, failing lists.
"""
import hashlib
import json
import shutil
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, LANE + "/tools/round-47")
sys.path.insert(0, LANE + "/tools/round-46")
import gate  # noqa: E402
import exact  # noqa: E402

REV = sys.argv[1] if len(sys.argv) > 1 else "1e2c3102"
SCRATCH = sys.argv[2] if len(sys.argv) > 2 else None

skill = gate.show(LANE, REV, "SKILL.md")
block = [b for b in exact.blocks_of(skill) if exact.MARKER in b][0]
base = exact._fixture_files(LANE, REV)
rows = [r[:] for r in exact.table(block)[1]]


def score(skill_text, overrides=None, self_text=None):
    files = dict(base)
    files.update(overrides or {})
    if self_text is not None:
        files[exact.SELF] = self_text
    files["SKILL.md"] = skill_text
    d, frev = exact._repo(files, SCRATCH)
    try:
        f = lambda p: gate.show(d, frev, p)  # noqa: E731
        c2, r2 = exact.score(files["SKILL.md"], f, "v2", frev, battery=None)
        c3, r3 = exact.score(files["SKILL.md"], f, "v3", frev, battery=None)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return {"v2_exit": c2, "v2_failing": r2.get("failing") or r2.get("reason"),
            "v3_exit": c3, "v3_failing": r3.get("failing") or r3.get("reason")}


def with_rows(new_rows):
    return skill.replace(block, exact.rewrite_rows(block, new_rows), 1)


cases = {}


def case(name, text, **kw):
    cases[name] = score(text, **kw)
    cases[name]["name"] = name
    print(json.dumps(cases[name]))


# 0. positive control: the genuine block
case("genuine", skill)

# 1. the claims' kill-rule example: `blobberish` in ONE v3-arm cell
r = [x[:] for x in rows]
r[0][2] = "`blobberish`"
case("blobberish-one-arm", with_rows(r))

# 2. the block's own counter: one arm cell "order-ish" (substring of `order`)
r = [x[:] for x in rows]
r[0][2] = "`order-ish`"
case("order-ish-one-arm", with_rows(r))

# 3. duplicate routed id in a FOUR-row table: row 1 names two ids
r = [x[:] for x in rows]
r[0][0] = r[0][0] + " " + rows[1][0]
case("dup-id-4rows-double-cell", with_rows(r))

# 4. order lie carried by the block, gate.py correct: does clause 7 see the block?
r = [x[:] for x in rows]
r[3][2] = "`order`"
r[3][1] = ("the argument order is a convention no clause reads; the correct invocation is "
           "`--diff-merges=first-parent -m`")
case("block-asserts-reversed-order", with_rows(r))

# 5. positive control: delete a mutation from the counter's own list (R46-CL4's real defect)
src = open(LANE + "/tools/round-47/exact.py").read()
cut = src.replace('MUTATIONS = [("substring-arm", _m_substring_arm),',
                  'MUTATIONS = [("substring-arm", _m_substring_arm),', 1)
short = src.replace('             ("flag-order-drift", _m_flag_order)]', "]")
assert short != src, "mutation-list cut did not apply"
case("counter-list-deleted", skill, self_text=short)

# 6. the pin recomputed for the shortened list (a forger who owns both sides)
print(json.dumps({"note": "next: block re-pinned for the 3-name list"}))
rows_ok = [x[:] for x in rows]
short_digest = hashlib.sha256("\n".join(
    n for n, _ in [("substring-arm", None), ("duplicate-routed-id", None),
                   ("stale-mutations-digest", None)]).encode()).hexdigest()
re_pinned = block.replace(exact.MUT_DIGEST, short_digest, 1)
case("counter-list-deleted-block-repinned", skill.replace(block, re_pinned, 1),
     self_text=short)

print(json.dumps({"cases": list(cases)}))
