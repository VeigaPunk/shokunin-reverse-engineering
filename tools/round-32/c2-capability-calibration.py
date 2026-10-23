#!/usr/bin/env python3
"""R32-C2 counter (calibration): the lane's self-declared repertoire, the SCORECARD.md
`## Capabilities` table, against the outside closure record of capabilities credited to
kaidoku rounds (fleet MANIFEST.json at a pinned fleet commit, written by non-author closures).

Predicate label `P2-match`, frozen in .ufo/waves/round-32/claims.json:
  Forward: a statement is one `capabilities_added` item of a MANIFEST round entry with
  lane "kaidoku" at the pinned fleet commit. It matches when the `## Capabilities` section of
  SCORECARD.md at REV (from the line `## Capabilities` to the next `## ` heading) holds a
  table row whose first cell matches the statement's frozen key pattern and whose last cell
  names that round (`round[- ]?N` with N the MANIFEST round number, not followed by a digit).
  Reverse: every row of that section whose last cell names a round `round[- ]?N` that has a
  kaidoku MANIFEST closure entry must be the matching row of a forward statement for that N
  (a row naming a MANIFEST-closed round that credits no capability is a mismatch).
  The statement set is closed: the frozen key list must cover every capabilities_added item
  at the pin (else exit 2).
Target line: statements=4 match=4 target=4 reverse_mismatch=0, exit 0.
Exit 2: a pinned input is absent or the key list does not cover the MANIFEST set.

Usage: c2-capability-calibration.py --root <LANE> --rev <REV> [--fleet <FLEET>] | --selftest
"""

import argparse
import json
import os
import re
import subprocess
import sys

TARGET = 4
FLEET_PIN = "cef00867ab3279ac2c2d10421e3e62c0e5d693f3"
# (MANIFEST round, frozen key pattern over the row's first cell); one per capabilities_added item.
KEYS = [
    (13, r"source(-curation)? registry"),
    (14, r"quote.{0,40}regression audit"),
    (17, r"Ghidra-session log capture"),
    (27, r"cross-pin evidence-ID attribution"),
]
LABEL = "P2-match"


def git(root, *args):
    return subprocess.run(["git", "-C", root] + list(args), capture_output=True, text=True)


def show(root, rev, rel):
    p = git(root, "show", rev + ":" + rel)
    return p.stdout if p.returncode == 0 else None


def manifest_statements(manifest_text):
    m = json.loads(manifest_text)
    stmts, closed = [], set()
    for r in m.get("rounds", []):
        if r.get("lane") != "kaidoku":
            continue
        if r.get("admitted") is not None:
            closed.add(r["round"])
        for item in r.get("capabilities_added") or []:
            stmts.append((r["round"], item))
    return stmts, closed


def section_rows(scorecard):
    rows, inside = [], False
    for ln in scorecard.splitlines():
        if ln.strip() == "## Capabilities":
            inside = True
            continue
        if inside and ln.startswith("## "):
            break
        if inside and ln.startswith("|") and not re.match(r"\|\s*-", ln) and not re.match(r"\|\s*Capability\s*\|", ln):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 4:
                rows.append(cells)
    return rows


def names_round(cell, n):
    return re.search(r"round[- ]?%d(?!\d)" % n, cell) is not None


def judge(stmts, closed, rows):
    results, used = [], set()
    for n, item in stmts:
        pats = [p for (k, p) in KEYS if k == n and re.search(p, item, re.I)]
        if not pats:
            return None, "key list does not cover MANIFEST round %d item %r" % (n, item[:60])
        hit = None
        for i, cells in enumerate(rows):
            if re.search(pats[0], cells[0], re.I) and names_round(cells[-1], n):
                hit = i
                break
        if hit is None:
            results.append((n, "P2-mismatch", "no `## Capabilities` row matches /%s/ naming round %d" % (pats[0], n)))
        else:
            used.add(hit)
            results.append((n, LABEL, "row %d" % (hit + 1)))
    reverse = []
    for i, cells in enumerate(rows):
        for n in sorted(closed):
            if names_round(cells[-1], n) and i not in used:
                reverse.append("row %d names MANIFEST-closed round %d without a credited capability" % (i + 1, n))
    return results, reverse


def measure(root, rev, fleet):
    mt = show(fleet, FLEET_PIN, "MANIFEST.json")
    if mt is None:
        print("PIN MANIFEST.json absent at fleet %s" % FLEET_PIN)
        return 2
    sc = show(root, rev, "SCORECARD.md")
    if sc is None:
        print("PIN SCORECARD.md absent at %s" % rev)
        return 2
    stmts, closed = manifest_statements(mt)
    if len(stmts) != TARGET:
        print("PIN MANIFEST credits %d kaidoku capabilities at the pin, frozen %d" % (len(stmts), TARGET))
        return 2
    results, reverse = judge(stmts, closed, section_rows(sc))
    if results is None:
        print("PIN " + reverse)
        return 2
    for n, verdict, why in results:
        print("round-%d\t%s\t%s" % (n, verdict, why))
    for r in reverse:
        print("reverse\tP2-mismatch\t%s" % r)
    match = sum(v == LABEL for _, v, _ in results)
    print("statements=%d match=%d target=%d reverse_mismatch=%d" % (len(results), match, TARGET, len(reverse)))
    return 0 if match == TARGET and not reverse else 1


def selftest():
    fails = 0
    manifest = json.dumps({"rounds": [
        {"lane": "kaidoku", "round": 13, "admitted": True, "capabilities_added": ["source-curation registry (22 rows)"]},
        {"lane": "kaidoku", "round": 14, "admitted": True, "capabilities_added": ["local raw-quote/heading regression audit"]},
        {"lane": "kaidoku", "round": 17, "admitted": True, "capabilities_added": ["retained REA Ghidra-session log capture"]},
        {"lane": "kaidoku", "round": 27, "admitted": False, "capabilities_added": ["cross-pin evidence-ID attribution for saved REA envelopes"]},
        {"lane": "kaidoku", "round": 30, "admitted": True, "capabilities_added": None},
        {"lane": "kama", "round": 5, "admitted": True, "capabilities_added": ["x"]},
    ]})
    stmts, closed = manifest_statements(manifest)
    head = "## Capabilities\n\n| Capability | What | Evidence | First-working round |\n|---|---|---|---|\n"
    full = head + ("| curated source registry for x | a | b | arc3-loop1-round13 |\n"
                   "| local raw-quote/heading regression audit | a | b | round 14 |\n"
                   "| retained REA Ghidra-session log capture | a | b | round 17 |\n"
                   "| cross-pin evidence-ID attribution for saved REA envelopes | a | b | round 27 |\n"
                   "| version-symmetry battery | a | b | luna-round-8 |\n") + "\n## Saturation\n"
    cases = [
        ("all four rows", full, 4, 0),
        ("do-nothing: base section (only round 27)", head + "| cross-pin evidence-ID attribution for x | a | b | round 27 |\n", 1, 0),
        ("rows outside the section", head + "\n## Other\n| retained REA Ghidra-session log capture | a | b | round 17 |\n", 0, 0),
        ("label only: right round, wrong capability", head + "| something | a | b | round 17 |\n", 0, 1),
        ("right capability, wrong round", head + "| retained REA Ghidra-session log capture | a | b | round 18 |\n", 0, 0),
        ("round 170 is not round 17", head + "| retained REA Ghidra-session log capture | a | b | round 170 |\n", 0, 0),
        ("over-claim row for round 30", full.replace("\n## Saturation", "| new thing | a | b | round 30 |\n\n## Saturation"), 4, 1),
        ("prose, not a row", head + "retained REA Ghidra-session log capture round 17\n", 0, 0),
        ("empty", "", 0, 0),
    ]
    for name, text, want_match, want_rev in cases:
        results, reverse = judge(stmts, closed, section_rows(text))
        got = sum(v == LABEL for _, v, _ in results)
        ok = got == want_match and len(reverse) == want_rev
        fails += not ok
        print("%s\t%s\tmatch=%d reverse=%d" % ("ok" if ok else "FAIL", name, got, len(reverse)))
    uncovered = json.dumps({"rounds": [{"lane": "kaidoku", "round": 31, "admitted": True, "capabilities_added": ["new"]}]})
    s2, c2 = manifest_statements(uncovered)
    res, why = judge(s2, c2, [])
    ok = res is None
    fails += not ok
    print("%s\tuncovered MANIFEST item refuses\t%s" % ("ok" if ok else "FAIL", why))
    print("selftest cases=%d failures=%d" % (len(cases) + 1, fails))
    return 0 if fails == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.getcwd())
    ap.add_argument("--rev", default="main")
    ap.add_argument("--fleet", default="/home/vgpnk/Projects/shokunin")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    sys.exit(measure(os.path.abspath(a.root), a.rev, os.path.abspath(a.fleet)))


if __name__ == "__main__":
    main()
