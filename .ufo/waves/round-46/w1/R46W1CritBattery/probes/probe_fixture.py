"""(c) probe: fixture coverage and the missing-at-rev path.

1. `need` for the landed block: every citation the block names, plus the pin,
   the claims file and round-45.md -- compare with what fixture_repo actually writes.
2. fixture_repo with a path that does not exist at --rev: silent skip or error?
"""
import json
import os
import sys

S = os.environ["HYAKU_SCRATCH"]
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(S, "tools", "round-46"))
import attest  # noqa: E402
import gate  # noqa: E402

spec = attest.SPECS["r46"]
skill = gate.show(LANE, "HEAD", "SKILL.md")
block = [b for b in attest.craft_blocks(skill) if spec["marker"] in b][0]
need = {"SKILL.md", spec["pin"] or "", attest.CLAIMS, "corpus/lessons/round-45.md"}
need |= {name for name, _, _ in attest.refs_in(block, True)}
need = sorted(p for p in need if p)
missing_at_rev = [p for p in need if gate.show(LANE, "HEAD", p) is None]

d, rev = attest.fixture_repo(LANE, "HEAD", skill,
                             need + ["corpus/lessons/round-45.md.bak"],
                             os.path.join(S, "sc-fixture"))
written = sorted(os.path.relpath(os.path.join(r, f), d)
                 for r, _, fs in os.walk(d) for f in fs if ".git" not in r)
print(json.dumps({
    "need": need,
    "missing_at_rev": missing_at_rev,
    "extra_nonexistent_path_silently_skipped": "corpus/lessons/round-45.md.bak" not in written,
    "fixture_files": written,
    "refs_named_by_block": len(attest.refs_in(block, True)),
}, indent=1))
