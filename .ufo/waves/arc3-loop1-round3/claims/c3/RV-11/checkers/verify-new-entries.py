#!/usr/bin/env python3
"""RV-11 independent re-derivation of every NEW table entry's needle at HEAD.

Independent of the probe: resolves both the citing line and the cited target
with `git show HEAD:<path>`, applies the kind semantics directly, and reports
hit/miss plus a needle-strength count (how many lines of the target the needle
matches) so a generic needle cannot launder a pin.

Usage: verify-new-entries.py --root REPO --table TABLE.json --baseline REV
"""
import argparse, json, re, subprocess, sys


def show(root, path):
    p = subprocess.run(["git", "-C", root, "show", "HEAD:%s" % path], capture_output=True, text=True)
    return p.stdout.splitlines() if p.returncode == 0 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--table", required=True)
    ap.add_argument("--baseline", default="c07af80")
    a = ap.parse_args()
    new = json.load(open(a.table))
    base = json.loads(subprocess.run(["git", "-C", a.root, "show",
                                      "%s:.ufo/gates/citation-drift/pointer-table.json" % a.baseline],
                                     capture_output=True, text=True).stdout)
    bids = {e["id"] for e in base["entries"]} | {e["id"] for e in base.get("quoted", [])}
    rows = []
    for e in new["entries"]:
        if e["id"] in bids:
            continue
        kind = e["kind"]
        citing = show(a.root, e["file"])
        row = {"id": e["id"], "kind": kind, "file": e["file"], "line": e.get("line")}
        if citing is None:
            row.update(verdict="FILE_ABSENT")
            rows.append(row)
            continue
        if kind == "anchor":
            hits = [i + 1 for i, l in enumerate(citing) if re.search(e["must_match"], l)]
            row.update(verdict="HIT" if hits else "MISS", hits=hits[:5])
            rows.append(row)
            continue
        ln = e["line"]
        if not (1 <= ln <= len(citing)):
            row.update(verdict="OUT_OF_RANGE")
            rows.append(row)
            continue
        line = citing[ln - 1]
        if kind == "exact":
            row.update(verdict="HIT" if re.search(e["must_match"], line) else "MISS")
            rows.append(row)
            continue
        if kind == "extracted":
            m = re.search(e["pattern"], line)
            if not m:
                row.update(verdict="CITING_LINE_LACKS_PATTERN")
                rows.append(row)
                continue
            lo = int(m.group(e.get("target_group", 1)))
            hi = int(m.group(e.get("target_group_end", e.get("target_group", 1))) or lo)
            win = int(e.get("window", 0))
            lo, hi = lo - win, hi + win
            cited = show(a.root, e["target"])
            if cited is None:
                row.update(verdict="TARGET_ABSENT")
                rows.append(row)
                continue
            if not (1 <= lo <= hi <= len(cited)):
                row.update(verdict="TARGET_RANGE_OUT_OF_RANGE", range="%d-%d/%d" % (lo, hi, len(cited)))
                rows.append(row)
                continue
            blob = "\n".join(cited[lo - 1:hi])
            hit = bool(re.search(e["must_match"], blob, re.M))
            # needle strength: how many target lines the needle alone matches
            strength = sum(1 for l in cited if re.search(e["must_match"], l))
            row.update(verdict="HIT" if hit else "MISS", range="%d-%d" % (lo, hi),
                       needle_line_matches=strength, target_lines=len(cited))
            rows.append(row)
            continue
        row.update(verdict="UNKNOWN_KIND")
        rows.append(row)
    ok = [r for r in rows if r["verdict"] == "HIT"]
    print("new entries re-derived: %d  hit=%d" % (len(rows), len(ok)))
    for r in rows:
        extra = ""
        if "range" in r:
            extra = " range=%s" % r["range"]
        if "needle_line_matches" in r:
            extra += " needle-lines=%d/%d" % (r["needle_line_matches"], r["target_lines"])
        if "hits" in r:
            extra += " hits=%s" % r["hits"]
        print("  %-38s %-9s %-34s %s%s" % (r["id"], r["kind"], r["file"][:34], r["verdict"], extra))
    weak = [r for r in rows if "needle_line_matches" in r and r["needle_line_matches"] > 3]
    if weak:
        print("\nweak-needle class (needle matches >3 lines of the target):")
        for r in weak:
            print("  %s: %d matches" % (r["id"], r["needle_line_matches"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())