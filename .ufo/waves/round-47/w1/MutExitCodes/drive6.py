#!/usr/bin/env python3
"""Sixth batch: claims-file shape edge cases (dir, tip-only tamper, nonexistent frozen path)."""
import json, os, sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/MutExitCodes")
import drive2 as D
from drive2 import sh, repo, put, commit, S, run, LANE, lane_show

FROZEN = "62e33f7d"
FILES = {"SKILL.md": lane_show(FROZEN, "SKILL.md"),
         "plans/round-47-claims.md": lane_show(FROZEN, "plans/round-47-claims.md"),
         "tools/round-47/exact.py": lane_show(FROZEN, "tools/round-47/exact.py"),
         "tools/round-46/gate.py": lane_show(FROZEN, "tools/round-46/gate.py")}
for p in ("corpus/lessons/round-46.md", "corpus/lessons/round-45.md"):
    b = lane_show(FROZEN, p)
    if b is not None:
        FILES[p] = b

def main():
    # claims is a directory at rev
    f = dict(FILES); f.pop("plans/round-47-claims.md")
    f["plans/round-47-claims.md/part.md"] = "x\n"
    d = repo("cl-dir", f); r = commit(d, "claims dir")
    run("c1-claims-is-a-directory", ["python3", "-I", "-B",
                                    os.path.join(d, "tools/round-47/exact.py"), "--root", d,
                                    "--freeze", r, "--rev", r, "--no-battery"], 2,
        "claims unreadable as a document at both ends")

    # valid at the freeze, empty frozen list at the tip (union arm's tip error)
    d = repo("cl-tipempty", FILES); base = commit(d, "base")
    put(d, {"plans/round-47-claims.md": "# claims\n\n## Frozen paths (exact)\n\nnone\n"})
    tip = commit(d, "tip empty")
    run("c1-claims-tip-empty-list", ["python3", "-I", "-B",
                                    os.path.join(d, "tools/round-47/exact.py"), "--root", d,
                                    "--freeze", base, "--rev", tip, "--no-battery"], 2,
        "frozen_set at the tip fails while the freeze end is valid")

    # well-formed claims naming a frozen path that exists nowhere
    ghost = dict(FILES)
    ghost["plans/round-47-claims.md"] = ("# claims\n\n## Frozen paths (exact)\n\n"
                                         "- `tools/round-47-ghost/`\n")
    d = repo("cl-ghost", ghost); r = commit(d, "ghost frozen path")
    rec = run("c1-claims-ghost-frozen-path", ["python3", "-I", "-B",
                                             os.path.join(d, "tools/round-47/exact.py"),
                                             "--root", d, "--freeze", r, "--rev", r,
                                             "--no-battery"], None,
              "coverage boundary: frozen_set does not require the path to exist")
    try:
        o = json.loads(rec["stdout"])
        print(json.dumps({"detail": "ghost frozen path", "exit": rec["exit"],
                          "frozen_derived": o.get("frozen_derived"),
                          "failing": o.get("failing")}))
    except Exception:
        print(json.dumps({"detail": "ghost frozen path", "exit": rec["exit"]}))
    with open(os.path.join(S, "receipts6.jsonl"), "w") as fh:
        for x in D.OUT:
            fh.write(json.dumps(x) + "\n")

main()
