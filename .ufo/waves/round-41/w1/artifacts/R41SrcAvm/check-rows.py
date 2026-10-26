#!/usr/bin/env python3
"""Lint the two drafted round-41 SOURCES rows against the lane's 11-column contract.

usage: check-rows.py [sources-rows.txt] [--base REV] [--lane DIR] [--selftest]

The row regex is copied from tools/round-35/c1-coverage-counter.py:ROW_RE (the lane's
own 11-column reader), so a row that passes here parses there. Read-only: the only git
call is `git show REV:corpus/SOURCES.md`.

Exit: 0 all checks pass, 1 a check failed, 2 usage/environment error.
"""
import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
BASE = "49096c7e6f226af0c750c4b003be58883cb6049f"
USED_BY = "corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md"
COLUMNS = ["id", "source", "kind", "tier", "scope", "anchor", "teaches",
           "status", "opened", "recheck", "used-by"]

ROW_RE = re.compile(
    r"(?m)^\|\s*(S\d{3,})\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|"
    r"([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|"
)


def base_registry(lane, rev):
    r = subprocess.run(["git", "-C", lane, "show", "%s:corpus/SOURCES.md" % rev],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("cannot read base registry: %s" % r.stderr.strip())
    return r.stdout


def split_cells(row):
    parts = row.split("|")
    if parts[0] != "" or parts[-1] != "":
        return None
    cells = [p.strip() for p in parts[1:-1]]
    return cells if len(cells) == len(COLUMNS) else None


def check(text, base_text, label=""):
    fails = []
    matches = list(ROW_RE.finditer(text))
    lines = [l for l in text.split("\n") if l.strip()]
    if len(matches) != len(lines):
        fails.append("row regex matched %d of %d non-empty lines" % (len(matches), len(lines)))
    base_ids = set(re.findall(r"(?m)^\|\s*(S\d{3,})\s*\|", base_text))
    ids = []
    for i, row in enumerate([l for l in text.split("\n") if l.strip()]):
        cells = split_cells(row)
        if cells is None:
            fails.append("row %d: not 11 cells separated by 12 pipes" % (i + 1))
            continue
        cell = dict(zip(COLUMNS, cells))
        ids.append(cell["id"])
        if not re.fullmatch(r"S\d{3,}", cell["id"]):
            fails.append("%s: bad id" % cell["id"])
        if cell["id"] in base_ids:
            fails.append("%s: id already in the base registry" % cell["id"])
        if cell["kind"] != "dataset":
            fails.append("%s: kind != dataset (%r)" % (cell["id"], cell["kind"]))
        if cell["tier"] != "A":
            fails.append("%s: tier != A (%r)" % (cell["id"], cell["tier"]))
        if cell["status"] != "mined":
            fails.append("%s: status != mined (%r)" % (cell["id"], cell["status"]))
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", cell["opened"]):
            fails.append("%s: opened is not an ISO date (%r)" % (cell["id"], cell["opened"]))
        if not (re.fullmatch(r"\d+d", cell["recheck"])
                or re.fullmatch(r"\d{4}-\d{2}-\d{2}", cell["recheck"])):
            fails.append("%s: recheck is not NNd or an ISO date (%r)" % (cell["id"], cell["recheck"]))
        if cell["used-by"] != USED_BY:
            fails.append("%s: used-by != %s (%r)" % (cell["id"], USED_BY, cell["used-by"]))
        urls = re.findall(r"https?://\S+", cell["source"])
        if not urls or any(not u.startswith("https://") for u in urls):
            fails.append("%s: source has no https URL (%r)" % (cell["id"], cell["source"]))
        for name in ("scope", "anchor", "teaches"):
            if not cell[name]:
                fails.append("%s: empty %s" % (cell["id"], name))
        quote = re.search(r'"([^"]+)"', cell["anchor"])
        if not quote:
            fails.append("%s: anchor carries no quoted line" % cell["id"])
        elif len(quote.group(1).split()) > 25:
            fails.append("%s: located quote is %d words (>25)"
                         % (cell["id"], len(quote.group(1).split())))
        for token in ("Product:", "Version:"):
            if token not in cell["anchor"]:
                fails.append("%s: anchor quote lacks %r (product + version required)" % (cell["id"], token))
    if len(set(ids)) != len(ids):
        fails.append("duplicate ids: %r" % ids)
    return fails, ids


def selftest():
    good = open(os.path.join(HERE, "sources-rows.txt")).read()
    base = base_registry(LANE, BASE)
    fails, ids = check(good, base)
    ok = not fails and ids == ["S127", "S128"]
    print("[selftest] green row set -> %s ids=%r" % ("PASS" if ok else "FAIL " + repr(fails), ids))
    mutations = {
        "pipe injected into scope": good.replace("| dataset | A |", "| dataset | A|B |", 1),
        "id collides with base (S126)": good.replace("| S127 |", "| S126 |", 1),
        "quote lengthened past 25 words": good.replace(
            '"Product: FRITZ!Box 5490 / Version: FRITZ!OS 7.31 / Release date: 09/04/2023"',
            '"%s"' % " ".join(["word"] * 26), 1),
        "status flipped": good.replace("| mined | 2026-10-26 |", "| rejected | 2026-10-26 |", 1),
        "used-by repointed": good.replace(USED_BY, "corpus/lessons/round-41.md", 1),
        "recheck becomes prose": good.replace("| 180d |", "| on-release |", 1),
    }
    red = 0
    for name, text in mutations.items():
        f, _ = check(text, base)
        hit = bool(f)
        red += hit
        print("[selftest] red %-32s -> %s %s" % (name, "PASS" if hit else "FAIL", f[:1]))
    return ok and red == len(mutations)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rows", nargs="?", default=None)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--lane", default=LANE)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.rows is None:
        a.rows = os.path.join(HERE, "sources-rows.txt")
    if a.selftest:
        return 0 if selftest() else 1
    try:
        text = open(a.rows).read()
    except OSError as e:
        print("cannot read %s: %s" % (a.rows, e))
        return 2
    base = base_registry(a.lane, a.base)
    base_ids = sorted(set(re.findall(r"(?m)^\|\s*(S\d{3,})\s*\|", base)))
    print("base %s: %d registry rows, max id %s" % (a.base, len(base_ids), base_ids[-1]))
    fails, ids = check(text, base)
    for i, row in enumerate(text.split("\n")):
        if row.strip():
            cells = split_cells(row)
            print("row %s: %d cells, %d chars, pipes %d"
                  % (cells[0] if cells else "?", len(cells) if cells else 0, len(row), row.count("|")))
    if fails:
        for f in fails:
            print("FAIL:", f)
        return 1
    print("PASS: ids %r parse as 11 columns, novel against the base, mined, 2026-10-26, 180d, used-by %s"
          % (ids, USED_BY))
    return 0


if __name__ == "__main__":
    sys.exit(main())
