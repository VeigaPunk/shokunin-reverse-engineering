#!/usr/bin/env python3
"""Calibration pre-check: mechanical SHONEN/SCORECARD statements vs git objects at REV.
usage: python3 -I -B calib-check.py --root <lane> --rev <rev> [--asserted FILE.json]
Reads only git objects (git show/ls-tree/cat-file/rev-parse); writes nothing; stdlib only.
Exit 0 when every row matches, 1 when any row mismatches, 2 on usage/git error.
Asserted values default to the base-49096c7e statements; for a landing edit ASSERTED below (or --asserted).
"""
import argparse, json, re, subprocess, sys

ASSERTED = {
  "craft_heading": 81, "craft_last": 375, "rule_blocks": 19,
  "rule_ranges": {"18": [316, 343], "19": [348, 375]},      # SHONEN L6 / depth row / cap row 629 as written
  "markers": {"v1": True, "v2": True},
  "knowledge_files": 130, "mapped": 130, "citations_resolved": 19,
  "province": {"adjacent_heading": 97, "safety": [116, 118], "tooling": [119, 125], "installer": [110, 115],
               "r39_heading": 378, "r39_row": 382, "r39_note": 384, "r40_heading": 386, "r40_note": 394,
               "pointer_157": 157, "pointer_376": 376},
}

def git(root, *a):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True)

def show(root, rev, path):
    p = git(root, "show", f"{rev}:{path}")
    if p.returncode: raise SystemExit(f"git show {rev}:{path} failed: {p.stderr.strip()}")
    return p.stdout

def skill_ranges(t):
    L = t.split("\n")
    ci = next(i for i, l in enumerate(L) if l.startswith("## Queue-drain craft ")) + 1
    nxt = next((i + 1 for i, l in enumerate(L) if l.startswith("## ") and i + 1 > ci), len(L) + 1)
    last = max(i + 1 for i in range(ci - 1, nxt - 1) if L[i].strip())
    starts = [i + 1 for i in range(ci - 1, nxt - 1) if L[i].startswith("- **")]
    rng = {}
    for k, a in enumerate(starts, 1):
        b = (starts[k] - 1) if k < len(starts) else last
        while not L[b - 1].strip(): b -= 1
        rng[str(k)] = [a, b]
    markers = {m: any(f"<!-- sqfs-triage-table {m} -->" in l for l in L) for m in ("v1", "v2", "v3")}
    return ci, last, rng, markers

def command_a(root, rev):
    paths = git(root, "ls-tree", "-r", "--name-only", rev, "--", "corpus/knowledge").stdout.splitlines()
    files = {p.rsplit("/", 1)[-1][:-3] for p in paths if p.endswith(".md")}
    sec = show(root, rev, "corpus/README.md").split("## Coverage map\n", 1)[1].split("\n## ", 1)[0]
    mapped = set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+", sec))
    craft = show(root, rev, "SKILL.md").split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    rules = re.split(r"(?m)^- \*\*", craft)[1:]
    pat = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
    ok = 0
    for r in rules:
        refs = re.findall(pat, r); v = bool(refs)
        for name, a, b in refs:
            p = git(root, "show", f"{rev}:corpus/knowledge/{name}")
            if p.returncode: v = False; continue
            n = len(p.stdout.splitlines()); s, e = int(a or 1), int(b or a or 1)
            v = v and 1 <= s <= e <= n
        ok += v
    return len(files & mapped), len(files), len(files - mapped), len(mapped - files), ok, len(rules)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--root", required=True); ap.add_argument("--rev", required=True)
    ap.add_argument("--asserted"); a = ap.parse_args()
    A = dict(ASSERTED)
    if a.asserted: A.update(json.load(open(a.asserted)))
    rev = git(a.root, "rev-parse", "--verify", a.rev + "^{commit}")
    if rev.returncode: print("bad rev", file=sys.stderr); return 2
    rev = rev.stdout.strip(); rows = []
    def row(name, asserted, observed): rows.append((name, asserted, observed, "match" if asserted == observed else "MISMATCH"))
    ci, last, rng, mk = skill_ranges(show(a.root, rev, "SKILL.md"))
    row("SKILL craft heading line", A["craft_heading"], ci)
    row("SKILL craft last non-blank line", A["craft_last"], last)
    row("SKILL rule blocks", A["rule_blocks"], len(rng))
    for k, v in A["rule_ranges"].items(): row(f"SKILL rule block {k} range", v, rng.get(k))
    row("SKILL marker v1 present", A["markers"]["v1"], mk["v1"]); row("SKILL marker v2 present", A["markers"]["v2"], mk["v2"])
    m, f, miss, dang, res, nr = command_a(a.root, rev)
    row("command A knowledge files", A["knowledge_files"], f); row("command A mapped", A["mapped"], m)
    row("command A missing+dangling", 0, miss + dang); row("command A citation_resolved_rules", A["citations_resolved"], res)
    P = show(a.root, rev, "PROVINCE.md").split("\n"); p = A["province"]
    def at(n): return P[n - 1] if n <= len(P) else ""
    row("PROVINCE :97 '## Adjacent'", True, at(p["adjacent_heading"]).startswith("## Adjacent"))
    row("PROVINCE :119-125 tooling bullet start", True, at(p["tooling"][0]).startswith("- **Tooling, dated 2026-10-26**"))
    row("PROVINCE :116-118 safety refusal", True, at(p["safety"][0]).startswith("- **Quality/safety verdicts"))
    row("PROVINCE :110-115 installer", True, at(p["installer"][0]).startswith("- **Installing engines"))
    row("PROVINCE :378 round-39 heading", True, at(p["r39_heading"]).startswith("## Round-39 additions to Core"))
    row("PROVINCE :382 squashfs_v4_be row", True, "squashfs_v4_be" in at(p["r39_row"]))
    row("PROVINCE :384 round-39 frontier note", True, at(p["r39_note"]).startswith("Round-39 frontier note"))
    row("PROVINCE :386 round-40 heading", True, at(p["r40_heading"]).startswith("## Round-40 measured, not promoted"))
    row("PROVINCE :394 round-40 frontier note", True, at(p["r40_note"]).startswith("Round-40 frontier note"))
    row("PROVINCE :157 dated round-39 pointer", True, "Round 39" in at(p["pointer_157"]))
    row("PROVINCE :376 round-38 note + round-39 pointer", True, at(p["pointer_376"]).startswith("Round-38 note") and "Round 39" in at(p["pointer_376"]))
    bad = 0
    for r in rows:
        print("\t".join(map(str, r))); bad += r[3] != "match"
    print(f"REV {rev} rows {len(rows)} mismatches {bad}")
    return 1 if bad else 0

if __name__ == "__main__": sys.exit(main())
