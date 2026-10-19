#!/usr/bin/env python3
"""VZ-4 C1 rule checker: per-rule citation resolution + rule-block hashes for the
`## Queue-drain craft` section of SKILL.md.

Usage:
  c1-rulecheck.py <rev-or-file> [--root DIR]
  c1-rulecheck.py --diff <ref_a> <ref_b>       # per-rule identity diff (first N)

A ref may be a git rev, a file path, or `<rev>:<path>`. Resolution logic mirrors
SCORECARD.md recipe A (rule = block split on `^- \*\*`; a rule resolves when it
names >=1 corpus/knowledge file and every cited range lies inside that file).
"""
import hashlib
import json
import pathlib
import re
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
PATTERN = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"


def read_ref(ref):
    if ref.startswith("tree:"):
        return pathlib.Path(ref[5:], "SKILL.md").read_text(encoding="utf-8")
    if ref.endswith(".md") or ref.endswith(".py") or "/" in ref and not re.fullmatch(r"[0-9a-f]{7,40}", ref):
        if pathlib.Path(ref).exists():
            return pathlib.Path(ref).read_text(encoding="utf-8")
    if ":" in ref:
        rev, path = ref.split(":", 1)
        return subprocess.check_output(["git", "-C", REPO, "show", f"{rev}:{path}"], text=True)
    return subprocess.check_output(["git", "-C", REPO, "show", f"{ref}:SKILL.md"], text=True)


def github_file_text(rev, name):
    if rev.startswith("tree:"):
        return pathlib.Path(rev[5:], "corpus/knowledge", name).read_text(encoding="utf-8")
    return subprocess.check_output(
        ["git", "-C", REPO, "show", f"{rev}:corpus/knowledge/{name}"], text=True)


def rules_of(text):
    craft = text.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    return re.split(r"(?m)^- \*\*", craft)[1:]


def check(rev, skill_text=None):
    text = skill_text if skill_text is not None else read_ref(rev)
    rows = []
    for i, rule in enumerate(rules_of(text), 1):
        title = rule.split("**", 1)[0][:70]
        refs = re.findall(PATTERN, rule)
        detail, ok = [], bool(refs)
        for name, first, last in refs:
            try:
                count = len(github_file_text(rev, name).splitlines())
                start, end = int(first or 1), int(last or first or 1)
                good = 1 <= start <= end <= count
                ok = ok and good
                detail.append("%s:%s-%s/%d %s" % (name, start, end, count, "ok" if good else "OUT-OF-RANGE"))
            except subprocess.CalledProcessError:
                ok = False
                detail.append("%s MISSING" % name)
        rows.append({"n": i, "title": title, "resolved": ok,
                     "rule_sha256": hashlib.sha256(rule.encode()).hexdigest()[:16],
                     "refs": detail})
    return rows


def main():
    if "--diff" in sys.argv:
        a, b = sys.argv[sys.argv.index("--diff") + 1:][:2]
        ra, rb = check(a), check(b)
        print("rules: A=%d B=%d" % (len(ra), len(rb)))
        n = min(len(ra), len(rb))
        same = sum(1 for i in range(n) if ra[i]["rule_sha256"] == rb[i]["rule_sha256"])
        for i in range(n):
            tag = "SAME" if ra[i]["rule_sha256"] == rb[i]["rule_sha256"] else "CHANGED"
            if tag == "CHANGED":
                print("  rule %d %s  A=%s B=%s  %s" % (i + 1, tag, ra[i]["rule_sha256"],
                                                       rb[i]["rule_sha256"], ra[i]["title"]))
        print("first-%d identical: %d/%d" % (n, same, n))
        for j in range(n, len(rb)):
            print("  NEW rule %d %s  %s" % (j + 1, rb[j]["rule_sha256"], rb[j]["title"]))
        print("A resolved %d/%d ; B resolved %d/%d"
              % (sum(r["resolved"] for r in ra), len(ra),
                 sum(r["resolved"] for r in rb), len(rb)))
        return
    ref = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "HEAD"
    rows = check(ref)
    print(json.dumps({"ref": ref, "rule_blocks": len(rows),
                      "resolved": sum(r["resolved"] for r in rows)}, sort_keys=True))
    for r in rows:
        print("  %2d %-8s %s  %s" % (r["n"], "resolved" if r["resolved"] else "UNRESOLVED",
                                     r["rule_sha256"], r["title"]))
        for d in r["refs"]:
            print("       %s" % d)


if __name__ == "__main__":
    main()
