#!/usr/bin/env python3
"""RV-8 anchor grader — replicate the citation-drift probe's anchor/exact
semantics over arbitrary file bytes (no git needed).

The probe's Tree.lines() resolves a target via `git show <rev>:<path>`; this
script takes the file contents from a directory tree instead, so a patched file
can be graded before any commit exists.  The regexes are the table's own
`must_match` strings, compiled with re.M / re.search exactly as
`check_entry` does for kind=anchor.

usage: anchor-grader.py <root-dir> <table.json> [entry-id ...]
Prints one line per entry: OK / DEAD / NO-FILE, with the deciding detail.
"""
import json
import os
import re
import sys

root = sys.argv[1]
table_path = sys.argv[2]
wanted = set(sys.argv[3:])
table = json.load(open(table_path))

rows = list(table.get("entries", [])) + [dict(e, kind="quoted") for e in table.get("quoted", [])]

dead = ok = nofile = 0
for e in rows:
    eid = e.get("id", "<unnamed>")
    if wanted and eid not in wanted:
        continue
    path = e.get("file")
    if not path:
        continue
    kind = e.get("kind")
    target = os.path.join(root, path)
    if not os.path.isfile(target):
        print("%-46s NO-FILE   %s" % (eid, path))
        nofile += 1
        continue
    text = open(target, encoding="utf-8", errors="replace").read()
    lines = text.splitlines()
    pat = e.get("must_match", "")
    if kind == "exact":
        ln = e.get("line")
        if ln is None:
            # snapshot-pinned or unpinned external; skip (graded by digest path)
            print("%-46s SKIP      (no line pin)" % eid)
            continue
        if 1 <= ln <= len(lines) and re.search(pat, lines[ln - 1]):
            print("%-46s OK        exact %s:%s" % (eid, path, ln))
            ok += 1
        else:
            got = lines[ln - 1][:70] if 1 <= ln <= len(lines) else "<line absent>"
            print("%-46s DEAD      exact %s:%s lacks %r  got=%r" % (eid, path, ln, pat[:48], got))
            dead += 1
    elif kind == "anchor":
        hits = [i + 1 for i, l in enumerate(lines) if re.search(pat, l)]
        if hits:
            print("%-46s OK        anchor %s:%s" % (eid, path, ",".join(map(str, hits[:4]))))
            ok += 1
        else:
            print("%-46s DEAD      anchor %s: no line matches %r" % (eid, path, pat[:56]))
            dead += 1
    else:
        # kind in (extracted, quoted-with-range) — range/offset grading; report
        print("%-46s SKIP      kind=%s (range grading not replicated)" % (eid, kind))

print("ANCHOR-GRADER: ok=%d dead=%d nofile=%d exit=%d" % (ok, dead, nofile, 1 if dead else 0))
sys.exit(1 if dead else 0)
