#!/usr/bin/env python3
"""C1Struct: structural score of the LANDED block 24 at a pinned rev (freeze guard bypassed).

`exact.score` is called directly so clauses 1-9 are measured even while the frozen-path
guard exits 2; the guard is measured separately by the CLI.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("HYAKU_SCRATCH", HERE)
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools/round-47"))
sys.path.insert(0, os.path.join(LANE, "tools/round-46"))
import exact  # noqa: E402
import gate  # noqa: E402

rev = os.environ.get("C1_REV") or gate.resolve(LANE, "HEAD")
skill = gate.show(LANE, rev, "SKILL.md")
files = lambda p: gate.show(LANE, rev, p)  # noqa: E731
code, rec = exact.score(skill, files, "v3", rev, battery=None)
craft = exact.craft_section(skill)
blocks = exact.blocks_of(skill)
marked = [b for b in blocks if exact.MARKER in b]
block = marked[0] if marked else ""
out = {
    "rev": rev,
    "score_exit": code,
    "rule_blocks": rec.get("rule_blocks"),
    "marker_occurrences": rec.get("marker_occurrences"),
    "block_present": rec.get("block_present"),
    "block_is_last": rec.get("block_is_last"),
    "block_title": rec.get("block_title"),
    "header": rec.get("header"),
    "rows": rec.get("rows"),
    "arm_tokens": rec.get("arm_tokens"),
    "routed_counts": rec.get("routed_counts"),
    "refs": rec.get("refs"),
    "cited": rec.get("cited"),
    "unresolved_citations": rec.get("unresolved_citations"),
    "mutations_sha256": rec.get("mutations_sha256"),
    "mutations_sha256_expected": rec.get("mutations_sha256_expected"),
    "interpreter_sha256": rec.get("interpreter_sha256"),
    "interpreter_sha256_expected": rec.get("interpreter_sha256_expected"),
    "gate_order_literal": rec.get("gate_order_literal"),
    "gate_order_reversed": rec.get("gate_order_reversed"),
    "failing": rec.get("failing"),
    "exact_py_sha256_at_rev": hashlib.sha256((files("tools/round-47/exact.py") or "").encode()).hexdigest(),
    "exact_py_sha256_at_freeze": hashlib.sha256((gate.show(
        LANE, "5017e1f7299c3a812e87e7950148f54313dd279e", "tools/round-47/exact.py") or "").encode()).hexdigest(),
    "craft_section_lines": len(craft.splitlines()),
    "landed_block_rows": [r for r in exact._rows(block)],
}
print(json.dumps(out, indent=1))
