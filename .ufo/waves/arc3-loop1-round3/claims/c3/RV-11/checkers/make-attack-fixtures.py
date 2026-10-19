#!/usr/bin/env python3
"""RV-11 attack fixtures: plant rule-#11 violations on a scratch copy of the
pointer table, so the audit's teeth are measured, not assumed.

Writes /var/tmp/rv11-arc3r3/attacks/table-attacks.json
       /var/tmp/rv11-arc3r3/attacks/expected-attacks.json
"""
import json, os, shutil

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
OUT = "/var/tmp/rv11-arc3r3/attacks"
os.makedirs(OUT, exist_ok=True)

table = json.load(open(os.path.join(REPO, ".ufo/gates/citation-drift/pointer-table.json")))
expected = json.load(open(os.path.join(REPO, ".ufo/gates/citation-drift/expected.json")))

attacks = [
    {   # A1 laundered pin: in-repo bytes, value = a dead config line number
        "id": "A1-laundered-config-line", "kind": "exact",
        "file": ".ufo/waves/arc3-loop1-round1/claims/c1/EX-01/config-pre-pair.txt",
        "line": 1, "must_match": "^:3225$",
        "note": "live stanza line for config.toml on 2026-10-18",
    },
    {   # A2 anchor laundering: grades an OM line-number token as content
        "id": "A2-anchor-launder", "kind": "anchor", "file": "SCORECARD.md",
        "must_match": "config\\.toml:\\d+",
        "note": "the config.toml pointer survives as content",
    },
    {   # A3 OM file graded by line number
        "id": "A3-om-graded", "kind": "exact", "file": "~/.kimi-code/config.toml",
        "line": 3225, "must_match": "\\[mcp_servers\\.rea\\]",
        "note": "live config stanza",
    },
    {   # A4 OM line number inside an append-only record but WITHOUT its stamp
        "id": "A4-no-stamp", "kind": "exact",
        "file": "corpus/lessons/2026-10-15-round-1.md", "line": 82,
        "must_match": "config\\.toml:1287",
        "note": "historical pointer to the kimi pin locus",
    },
    {   # A5 control: the sanctioned erratum form (append-only record + stamp)
        "id": "A5-conform-stamp", "kind": "exact",
        "file": "corpus/lessons/2026-10-15-round-1.md", "line": 202,
        "must_match": "drift-config-toml-20261018T191721Z\\.txt",
        "note": "pointer-refresh erratum appended 2026-10-18; names its receipt",
    },
    {   # A6 control (unpinned snapshot target)
        "id": "A6-snapshot-unpinned", "kind": "anchor",
        "file": "SCORECARD.md", "must_match": "config-toml-landmarks",
        "target": "@config-toml-landmarks-v2", "note": "graded against an unpinned snapshot",
    },
    {   # A7 control (pinned snapshot target)
        "id": "A7-snapshot-pinned", "kind": "anchor",
        "file": "SCORECARD.md", "must_match": "config-toml-landmarks",
        "target": "@config-toml-landmarks",
        "note": "graded against the receipt pinned in expected.json snapshots",
    },
]
table["entries"] = table["entries"] + attacks
json.dump(table, open(os.path.join(OUT, "table-attacks.json"), "w"), indent=1)

exp2 = json.loads(json.dumps(expected))
exp2["snapshots"]["config-toml-landmarks"] = "0" * 64
json.dump(exp2, open(os.path.join(OUT, "expected-attacks.json"), "w"), indent=1)
print("wrote %d baseline + %d attack entries" % (len(table["entries"]) - len(attacks), len(attacks)))