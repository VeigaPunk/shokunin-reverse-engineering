#!/usr/bin/env python3
"""arc3-era citation census for the pointer-table extension (seat EX-41).

Surfaces: the non-wave files touched by the arc3 loop1 rounds 1-2 commits
(fbbbd45 work r1, 14b1682 records r1, 28aa7a9 work r2, c07af80 records r2).
For every ADDED line in those diffs, extract citation-like tokens
(path[:line[-line]]) and classify the target as in-repo / operator-mutable.

Read-only over the real tree; writes only stdout.
"""
import json
import os
import re
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
COMMITS = ["fbbbd45", "14b1682", "28aa7a9", "c07af80"]
# operator-mutable custody paths (rule #11): never pin a bare line number
OPERATOR = ["config.toml", "mcp_config.json", "mcp.json", ".bashrc", ".profile"]

TOKEN = re.compile(r"([A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:md|json|py|toml|txt|cfg|sha256|bin|js|sol))"
                   r"(?::(\d+)(?:-(\d+))?)?")


def added_lines(commit):
    proc = subprocess.run(
        ["git", "-C", ROOT, "show", "--unified=0", "--format=", commit,
         "--", ".", ":(exclude).ufo/waves/**"],
        capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit("git show failed for %s" % commit)
    cur = None
    for line in proc.stdout.splitlines():
        if line.startswith("+++ b/"):
            cur = line[6:]
            continue
        if line.startswith("+") and not line.startswith("+++"):
            yield cur, line[1:]


def in_repo(path):
    return os.path.exists(os.path.join(ROOT, path))


def main():
    rows = []
    for commit in COMMITS:
        for f, text in added_lines(commit):
            for m in TOKEN.finditer(text):
                tok, lo, hi = m.group(1), m.group(2), m.group(3)
                if lo is None:
                    continue  # file-level citation: not the drift class
                target = tok
                rows.append({
                    "commit": commit, "file": f, "token": m.group(0),
                    "target": target, "lo": int(lo),
                    "hi": int(hi) if hi else None,
                    "in_repo": in_repo(target),
                    "operator_mutable": any(o in target for o in OPERATOR),
                })
    # de-dup by (file, token)
    seen = {}
    for r in rows:
        key = (r["file"], r["token"])
        if key in seen:
            seen[key]["commits"].append(r["commit"])
            seen[key]["count"] += 1
        else:
            r["commits"] = [r["commit"]]
            r["count"] = 1
            seen[key] = r
    out = sorted(seen.values(), key=lambda r: (r["file"], r["lo"]))
    json.dump(out, open("/var/tmp/ex41/census-raw.json", "w"), indent=1)
    print("candidate cited-token rows: %d (raw hits %d)" % (len(out), len(rows)))
    for r in out:
        print("%-52s %-34s in_repo=%-5s op=%s commits=%s"
              % (r["file"], r["token"], r["in_repo"], r["operator_mutable"],
                 ",".join(r["commits"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())