#!/usr/bin/env python3
"""CR-5 seat (arc3-loop1-round3) — INDEPENDENT arc3-era citation census.

Scope (my reading of the C3 claim's named debt): every in-repo citation
introduced by arc3 rounds 1-2 (work commits fbbbd45 / 28aa7a9, records commits
14b1682 / c07af80) in the lane documents those rounds landed, plus the r1
knowledge entry, the arc3 SCORECARD sections, the round-2 registry rows and the
custody receipt conventions.

Method: diff base e845c2b -> HEAD c07af80 for non-wave files; take the ADDED
lines; locate each added line's HEAD line number; extract citation tokens
(path:line, path:line-range, bare :N / :N-M) and classify the target.

Output: census-cr5.json + census-cr5.txt (deterministic, re-runnable).
"""
import json
import re
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
BASE = "e845c2b"          # operator-halt commit before arc3 round 1
HEAD = "c07af80"          # arc3 round-2 records commit

FILES = [
    "corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md",
    "corpus/README.md",
    "SCORECARD.md",
    "LOG.md",
    "SKILL.md",
    "SHONEN.md",
    ".ufo/gates/citation-drift/expected.json",
    ".ufo/gates/custody-pair/README.md",
    ".ufo/reports/arc3-loop1-round1/kaidoku.md",
    ".ufo/reports/arc3-loop1-round2/kaidoku.md",
]

OPERATOR_MUTABLE = {
    "~/.config/devin/mcp_config.json", "~/.omp/agent/mcp.json",
    "~/.kimi-code/config.toml", "~/.bashrc", "~/.profile",
    "config.toml", "mcp_config.json", "~/.bashrc",
}

RANGE = re.compile(r"([A-Za-z0-9_~][A-Za-z0-9_./~-]*?\.(?:md|json|py|txt|toml|sol|sh|js)):(\d+)(?:-(\d+))?")
BARE = re.compile(r"(?<![\w./~:-]):(\d+)(?:-(\d+))?(?![\d-])")


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True).stdout.decode()


def added_lines_with_head_numbers(path):
    """Return list of (head_line_no, text) for lines ADDED between BASE and HEAD."""
    diff = git("diff", "-U0", "%s..%s" % (BASE, HEAD), "--", path)
    head_text = git("show", "%s:%s" % (HEAD, path))
    if not head_text and head_text == "":
        return []
    out = []
    for hunk in re.finditer(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", diff, re.M):
        start = int(hunk.group(1))
        n = int(hunk.group(2) or 1)
        for i in range(n):
            ln = start + i
            line = head_text.splitlines()[ln - 1] if ln - 1 < len(head_text.splitlines()) else ""
            out.append((ln, line))
    return out


def target_class(target):
    if any(o in target for o in OPERATOR_MUTABLE):
        return "operator-mutable"
    if target.startswith(".ufo/waves/"):
        return "wave-artifact"
    if target.startswith(".ufo/gates/"):
        return "gate"
    if target.startswith("corpus/") or target in ("SCORECARD.md", "LOG.md", "SKILL.md",
                                                  "SHONEN.md", "PROVINCE.md", "README.md"):
        return "in-repo-doc"
    return "other"


def exists_at_head(target):
    if target.startswith("~") or target in OPERATOR_MUTABLE:
        return "outside-repo"
    p = subprocess.run(["git", "-C", REPO, "cat-file", "-e", "%s:%s" % (HEAD, target)],
                       capture_output=True)
    return "present" if p.returncode == 0 else "absent"


def main():
    census = {}
    for path in FILES:
        rows = []
        for ln, text in added_lines_with_head_numbers(path):
            toks = []
            for m in RANGE.finditer(text):
                tgt, lo, hi = m.group(1), int(m.group(2)), m.group(3)
                toks.append({"target": tgt, "lo": lo,
                             "hi": int(hi) if hi else None,
                             "class": target_class(tgt), "head": exists_at_head(tgt)})
            for m in BARE.finditer(text):
                toks.append({"target": "<bare :%s%s>" % (m.group(1), "-" + m.group(2) if m.group(2) else ""),
                             "lo": int(m.group(1)),
                             "hi": int(m.group(2)) if m.group(2) else None,
                             "class": "bare-line-ref", "head": "n/a"})
            if toks:
                rows.append({"head_line": ln, "text": text.rstrip("\n"), "tokens": toks})
        census[path] = rows
    json.dump(census, open("/var/tmp/cr5-r3/census/census-cr5.json", "w"), indent=1)
    total = 0
    with open("/var/tmp/cr5-r3/census/census-cr5.txt", "w") as f:
        for path in FILES:
            rows = census[path]
            n = len(rows)
            total += n
            f.write("## %s  added-citation-lines=%d\n" % (path, n))
            for r in rows:
                f.write("  @%s | %s\n" % (r["head_line"], r["text"][:160]))
                for t in r["tokens"]:
                    f.write("      -> %s:%s%s [%s / %s]\n" % (t["target"], t["lo"],
                            ("-" + str(t["hi"])) if t["hi"] else "", t["class"], t["head"]))
    print("files scanned:", len(FILES), "citation-bearing added lines:", total)
    print("wrote /var/tmp/cr5-r3/census/census-cr5.{json,txt}")


if __name__ == "__main__":
    sys.exit(main())