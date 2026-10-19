#!/usr/bin/env python3
"""RV-11 independent arc3-era in-repo pointer census.

Enumerates `path:line[-line]` pointer tokens introduced by the arc3-loop1
rounds 1-2 commits (work + records) and classifies each by resolvability at
HEAD and by rule #11 class:

  OM            the pointed-at file is operator-mutable -> rule #11 governs
                (content key + receipt; a bare line number is a violation)
  IN-REPO-OK    target resolves at HEAD (pinnable)
  IN-REPO-DEAD  target absent at HEAD (adjudicate: not pinnable)
  EXTERNAL      path outside the repo

Restricted by default to documentation-class files (the class the pointer
table grades); --all keeps wave-evidence receipts too.

Usage: arc3-pointer-census.py --root REPO --revs H1 H2 ... [--all] [--json OUT]
"""
import argparse, collections, json, os, re, subprocess, sys

OM = re.compile(r"(?:~|/home/vgpnk)/\.kimi-code/config\.toml|(?:^|/)config\.toml|"
                r"(?:~|/home/vgpnk)/\.config/devin/mcp_config\.json|mcp_config\.json|"
                r"(?:~|/home/vgpnk)/\.omp/agent/mcp\.json|(?:^|/)mcp\.json|"
                r"(?:~|/home/vgpnk)/\.bashrc|(?:^|/)\.bashrc|"
                r"(?:~|/home/vgpnk)/\.profile|(?:^|/)\.profile")
PTR = re.compile(r"(\.[A-Za-z0-9_][\w./-]*\.(?:md|json|py|txt|sh|toml|jsonl|patch)|"
                 r"[A-Za-z0-9_][\w./-]*\.(?:md|json|py|txt|sh|toml|jsonl|patch))"
                 r":(\d+)(?:\s*-\s*(\d+))?")
DOC_PREFIXES = ("SCORECARD.md", "PROVINCE.md", "SKILL.md", "SHONEN.md", "LOG.md",
                "corpus/", "evidence/", "README.md")


def added_doc_lines(root, rev, all_files):
    p = subprocess.run(["git", "-C", root, "show", "--unified=0", "--format=", rev],
                       capture_output=True, text=True)
    cur = None
    for line in p.stdout.splitlines():
        if line.startswith("+++ b/"):
            cur = line[6:]
            continue
        if not (line.startswith("+") and not line.startswith("+++")):
            continue
        if not all_files and cur and not cur.startswith(DOC_PREFIXES):
            continue
        yield cur, line[1:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revs", nargs="+", required=True)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    rows, seen = [], set()
    for rev in a.revs:
        for path, line in added_doc_lines(a.root, rev, a.all):
            for m in PTR.finditer(line):
                tgt = m.group(1)
                key = (path, tgt, m.group(2), m.group(3))
                if key in seen:
                    continue
                seen.add(key)
                if "://" in line[max(0, m.start() - 8):m.start()]:
                    continue
                if tgt.startswith("/") and not tgt.startswith("/home/vgpnk"):
                    cls = "EXTERNAL"
                elif OM.search(tgt) or tgt.startswith("~"):
                    cls = "OM"
                else:
                    cls = "IN-REPO-OK" if os.path.isfile(os.path.join(a.root, tgt)) else "IN-REPO-DEAD"
                rows.append({"rev": rev, "in": path, "ref": m.group(0), "target": tgt,
                             "class": cls, "text": line.strip()[:150]})
    counts = collections.Counter(r["class"] for r in rows)
    out = {"revs": a.revs, "pointers": len(rows), "counts": dict(counts), "rows": rows}
    if a.json:
        json.dump(out, open(a.json, "w"), indent=1)
    print("arc3-era in-repo pointers: %d  %s" % (len(rows), dict(counts)))
    for cls in ("OM", "IN-REPO-DEAD"):
        sub = [r for r in rows if r["class"] == cls]
        if not sub:
            continue
        print("\n== %s (%d) ==" % (cls, len(sub)))
        for r in sub:
            print("  %-22s %s" % (r["ref"], r["in"]))
    tally = collections.Counter(r["target"] for r in rows if r["class"] == "IN-REPO-OK")
    print("\n== IN-REPO-OK targets (top 25) ==")
    for t, c in tally.most_common(25):
        print("  %3d  %s" % (c, t))
    return 0


if __name__ == "__main__":
    sys.exit(main())