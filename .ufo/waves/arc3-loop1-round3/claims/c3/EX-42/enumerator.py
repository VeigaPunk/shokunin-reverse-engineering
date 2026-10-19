#!/usr/bin/env python3
"""EX-42 arc3-citation census — mechanical enumerator v2 (broad path token net).

Same inputs as v1; output /var/tmp/ex42-census/citations2.tsv with one row per
(citing_file, head_line, kind, token). Kinds:
  A path:NN[-NN]      stated line/range citation
  B file-level path   (backticked or bare; extensions + knowledge slugs)
  D section-key form  `FILE.md`'s `<section-name>` section
  E named receipt     receipt <stamp> / receipts/<path>
  C operator-mutable  config.toml:N
"""
import re
import subprocess
import json
import os

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
COMMITS = ["fbbbd45", "14b1682", "28aa7a9", "c07af80"]
CANON = {
    "SCORECARD.md": "SCORECARD.md",
    "corpus/README.md": "corpus/README.md",
    "SHONEN.md": "SHONEN.md",
    "SKILL.md": "SKILL.md",
    "LOG.md": "LOG.md",
    "PROVINCE.md": "PROVINCE.md",
    "corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md": "kb",
}

EXT = r"(?:md|py|json|txt|sol|hex|js|toml|cfg|sha256)"
SLUG = r"20\d\d-\d\d-\d\d-[a-z0-9][a-z0-9\-]+"
PATHTOK = r"(?:\.?\.?/)?[A-Za-z0-9_@./{},\-]*(?:\.%s|%s)" % (EXT, SLUG)
LINE_CITE = re.compile(r"(%s):(\d+)(?:-(\d+))?" % PATHTOK)
FILE_TOK = re.compile(r"(%s)" % PATHTOK)
STAMP = re.compile(r"receipt 20\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ")
RECEIPTS = re.compile(r"[\w./\-]*receipts/[A-Za-z0-9_./\-]+")
SECTIONKEY = re.compile(r"`([A-Za-z0-9_./\-]+\.md)`'s `(arc[23]-[a-z0-9\-]+)`")
CFG = re.compile(r"config\.toml:(\d+)(?:-(\d+))?")


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True).stdout.decode("utf-8", "replace")


def added_lines(commit, path):
    out = git("show", "--format=", "--unified=0", commit, "--", path)
    res = []
    for ln in out.splitlines():
        if ln.startswith("+++"):
            continue
        if ln.startswith("+"):
            res.append(ln[1:])
    return res


def head_lines(path):
    try:
        return open(os.path.join(ROOT, path), "rb").read().decode("utf-8").splitlines()
    except OSError:
        return []


def find_head_line(lines, needle):
    for i, ln in enumerate(lines):
        if needle and needle in ln:
            return i + 1
    return None


NOISE = {".sha256", "expected.json", "pointer-table.json", "SCORECARD.md", "LOG.md",
         "SKILL.md", "SHONEN.md", "PROVINCE.md", "config.toml", "QUALITY.md"}


def main():
    rows = []
    for commit in COMMITS:
        for path in CANON:
            hlines = head_lines(path)
            for added in added_lines(commit, path):
                if len(added.strip()) < 8:
                    continue
                hl = find_head_line(hlines, added.strip()[:40]) if len(added.strip()) >= 12 else None
                for m in LINE_CITE.finditer(added):
                    rows.append((commit, path, hl, "A", m.group(0)))
                for m in FILE_TOK.finditer(added):
                    tok = m.group(1)
                    rows.append((commit, path, hl, "B", tok))
                for m in STAMP.finditer(added):
                    rows.append((commit, path, hl, "E", m.group(0)))
                for m in RECEIPTS.finditer(added):
                    rows.append((commit, path, hl, "E", m.group(0)))
                for m in SECTIONKEY.finditer(added):
                    rows.append((commit, path, hl, "D", "%s's %s" % (m.group(1), m.group(2))))
                for m in CFG.finditer(added):
                    rows.append((commit, path, hl, "C", m.group(0)))
    seen, out = set(), []
    for r in rows:
        # a B token that is the path half of an A token on the same line is the
        # same citation; drop the duplicate B (keep A).
        key = (r[1], r[2], r[3], r[4])
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    # drop B rows that duplicate an A row's target on the same citing line
    a_targets = {(r[1], r[2], r[4].split(":")[0]) for r in out if r[3] == "A"}
    out = [r for r in out if not (r[3] == "B" and (r[1], r[2], r[4]) in a_targets)]
    with open("/var/tmp/ex42-census/citations2.tsv", "w") as fh:
        fh.write("commit\tciting\thead_line\tkind\ttoken\n")
        for r in out:
            fh.write("%s\t%s\t%s\t%s\t%s\n" % r)
    print("rows:", len(out))


if __name__ == "__main__":
    main()