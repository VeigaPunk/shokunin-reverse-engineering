#!/usr/bin/env python3
"""R47-C1 structural attacks, in-process against the frozen exact.py score().

Each case builds synthetic SKILL.md text around the frozen `good_block()` helper (the
counter's own fixture generator) and scores it with the counter's own `score()` over the
repo's real bytes for every file the block cites. Reported truth: exit code and failing[].

A pass here is a clause that does not discriminate: the artefact is structurally different
from the one block 24 must be, and the counter says met.
"""
import hashlib
import json
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "3186f69b49798f2cc05727bbfd1604505fcee03b"
sys.path.insert(0, os.path.join(LANE, "tools/round-47"))
sys.path.insert(0, os.path.join(LANE, "tools/round-46"))
import exact  # noqa: E402
import gate  # noqa: E402

PATHS = ("corpus/lessons/round-46.md", "tools/round-46/gate.py",
         "tools/round-47/exact.py", "plans/round-47-claims.md")
FILES = {p: gate.show(LANE, REV, p) for p in PATHS}
FILES = {k: v for k, v in FILES.items() if v is not None}


def score(name, skill):
    code, rec = exact.score(skill, lambda p: FILES.get(p), "v3", REV, battery=None)
    return {"case": name, "exit": code,
            "failing": rec.get("failing") or rec.get("reason"),
            "arm_tokens": rec.get("arm_tokens"),
            "routed_counts": rec.get("routed_counts")}


out = []
base = exact.skill_text(exact.good_block())

out.append(score("control-genuine", base))
# clause 5 positive control: the R46-CL2 defect class must be caught in v3
out.append(score("control-arm-blobberish", exact.skill_text(exact.good_block(
    rows=[r[:2] + ("blobberish",) + r[3:] for r in exact.GOOD_ROWS]))))

# A1: a 25th craft rule appended as a heading, not as a `- **` bullet. Block 24 is no
# longer the last craft rule, but block_is_last is computed over `^- \*\*` splits only.
heading_25 = ("\n### 25. A later craft rule written as a heading, after block 24.\n"
              "This rule body carries no citation.\n")
skill = base.replace("\n## Next section", heading_25 + "\n## Next section")
out.append(score("A1-later-rule-as-heading", skill))

# A1b: the same 25th rule as a bullet with a different marker (no `- **` opener).
bullet_25 = ("\n* **25. A later craft rule with a star bullet.** body text\n")
skill = base.replace("\n## Next section", bullet_25 + "\n## Next section")
out.append(score("A1b-later-rule-star-bullet", skill))

# A2: the arm token is an equality, but nothing binds an arm to the hole it answers:
# rotate the four tokens across the four routed ids.
rotated = [(r[0], r[1], exact.VOCAB[(i + 1) % 4], r[3])
           for i, r in enumerate(exact.GOOD_ROWS)]
out.append(score("A2-arm-token-rotated-against-holes",
                 exact.skill_text(exact.good_block(rows=rotated))))

# A2b: every row's v2-hole cell emptied and every trigger cell replaced by prose that
# still names the id once. The arm column keeps a token. Content-free rows.
empty_holes = [("`" + r[0] + "`", "--", r[2], r[3]) for r in exact.GOOD_ROWS]
out.append(score("A2b-hole-column-emptied",
                 exact.skill_text(exact.good_block(rows=empty_holes))))

print(json.dumps({"rev": REV, "cases": out}, indent=1))
