#!/usr/bin/env python3
"""R32-C2 counter v2 (calibration): the lane's self-declared repertoire, the SCORECARD.md
`## Capabilities` table, against the outside closure record of capabilities credited to
kaidoku rounds (fleet MANIFEST.json at a pinned fleet commit, written by non-author closures).

v2 supersedes v1 (tools/round-32/c2-capability-calibration.py, frozen at 9a73680a) before any
seat or data scored it: the L1's own pre-wave control found that ONE junk row naming all four
capability phrases and all four rounds met the v1 target, and that a row with names and
rounds but no evidence pointer met it too.  Recorded in .ufo/waves/round-32/claims-v2.json.

Predicate label `P2-match`, frozen in .ufo/waves/round-32/claims-v2.json:
  Forward: a statement is one `capabilities_added` item of a MANIFEST round entry with
  lane "kaidoku" at the pinned fleet commit. It matches when the `## Capabilities` section of
  SCORECARD.md at REV (from the line `## Capabilities` to the next `## ` heading) holds a
  table row, not matched by another statement, whose first cell matches the statement's frozen
  key pattern and no other key pattern, whose last cell names exactly one round and that round
  is the MANIFEST round (`round[- ]?N`, N not followed by a digit), and whose evidence cell
  (third cell) names at least one backticked lane path and every backticked lane path in it
  resolves to a file at REV.
  Reverse: every row of that section whose last cell names a round that has a kaidoku MANIFEST
  closure entry must be the matching row of a forward statement (a row naming a
  MANIFEST-closed round that credits no capability is a mismatch).
  The statement set is closed: the frozen key list must cover every capabilities_added item
  at the pin (else exit 2).
Target line: statements=4 match=4 target=4 reverse_mismatch=0, exit 0.

Usage: c2-capability-calibration-v2.py --root <LANE> --rev <REV> [--fleet <FLEET>] | --selftest
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
ROUND_RE = re.compile(r"round[- ]?(\d+)(?!\d)")
PATH_RE = re.compile(r"`([A-Za-z0-9_.][A-Za-z0-9_./-]*/[A-Za-z0-9_.-]+\.[A-Za-z0-9]+|[A-Za-z0-9_-]+\.(?:md|py|mjs|json|tsv|txt|sh))(?::[0-9,-]+)?`")


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


def rounds_named(cell):
    return {int(n) for n in ROUND_RE.findall(cell)}


def evidence_ok(cell, exists):
    paths = [m.group(1) for m in PATH_RE.finditer(cell) if "/" in m.group(1)]
    if not paths:
        return False, "evidence cell names no backticked lane path"
    dangling = [p for p in paths if not exists(p)]
    if dangling:
        return False, "evidence path(s) do not resolve: %s" % ", ".join(dangling[:3])
    return True, "evidence paths=%d" % len(paths)


def judge(stmts, closed, rows, exists):
    results, used = [], set()
    for n, item in stmts:
        pats = [p for (k, p) in KEYS if k == n and re.search(p, item, re.I)]
        if not pats:
            return None, "key list does not cover MANIFEST round %d item %r" % (n, item[:60])
        hit, why = None, "no `## Capabilities` row matches /%s/ naming round %d" % (pats[0], n)
        for i, cells in enumerate(rows):
            if i in used or not re.search(pats[0], cells[0], re.I):
                continue
            if sum(bool(re.search(p, cells[0], re.I)) for _, p in KEYS) != 1:
                why = "row %d first cell matches more than one capability key" % (i + 1)
                continue
            if rounds_named(cells[-1]) != {n}:
                why = "row %d last cell names rounds %s, not exactly round %d" % (i + 1, sorted(rounds_named(cells[-1])), n)
                continue
            ok, ewhy = evidence_ok(cells[2], exists)
            if not ok:
                why = "row %d %s" % (i + 1, ewhy)
                continue
            hit, why = i, "row %d %s" % (i + 1, ewhy)
            break
        if hit is None:
            results.append((n, "P2-mismatch", why))
        else:
            used.add(hit)
            results.append((n, LABEL, why))
    reverse = []
    for i, cells in enumerate(rows):
        named = rounds_named(cells[-1]) & closed
        if named and i not in used:
            reverse.append("row %d names MANIFEST-closed round(s) %s without a credited capability" % (i + 1, sorted(named)))
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
    tree = set(git(root, "ls-tree", "-r", "--name-only", rev).stdout.splitlines())
    results, reverse = judge(stmts, closed, section_rows(sc), lambda p: p in tree)
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
    exists = lambda p: p in {"corpus/SOURCES.md", "tools/a.py", "tools/b.py", "tools/c.py"}
    head = "## Capabilities\n\n| Capability | What | Evidence | First-working round |\n|---|---|---|---|\n"
    rows4 = ("| curated source registry for x | a | `corpus/SOURCES.md` | arc3-loop1-round13 |\n"
             "| local raw-quote/heading regression audit | a | `tools/a.py` | round 14 |\n"
             "| retained REA Ghidra-session log capture | a | `tools/b.py`; `tools/c.py:3-9` | round 17 |\n"
             "| cross-pin evidence-ID attribution for saved REA envelopes | a | `tools/c.py` | round 27 |\n"
             "| version-symmetry battery | a | b | luna-round-8 |\n")
    full = head + rows4 + "\n## Saturation\n"
    allin1 = head + ("| source registry, quote regression audit, Ghidra-session log capture, cross-pin evidence-ID attribution"
                     " | a | `tools/a.py` | round 13, round 14, round 17, round 27 |\n")
    cases = [
        ("all four rows", full, 4, 0),
        ("do-nothing: base section (only round 27)", head + "| cross-pin evidence-ID attribution for x | a | `tools/c.py` | round 27 |\n", 1, 0),
        ("one row naming all four capabilities and rounds", allin1, 0, 1),
        ("four copies of one row with four rounds each", head + ("| retained REA Ghidra-session log capture | a | `tools/b.py` | round 13, 14, 17, 27 |\n" * 4), 0, 4),
        ("names and rounds, no evidence path", full.replace("`tools/a.py`", "see card"), 3, 1),
        ("dangling evidence path", full.replace("`tools/a.py`", "`tools/zz.py`"), 3, 1),
        ("rows outside the section", head + "\n## Other\n| retained REA Ghidra-session log capture | a | `tools/b.py` | round 17 |\n", 0, 0),
        ("label only: right round, wrong capability", head + "| something | a | `tools/a.py` | round 17 |\n", 0, 1),
        ("right capability, wrong round", head + "| retained REA Ghidra-session log capture | a | `tools/b.py` | round 18 |\n", 0, 0),
        ("round 170 is not round 17", head + "| retained REA Ghidra-session log capture | a | `tools/b.py` | round 170 |\n", 0, 0),
        ("over-claim row for round 30", full.replace("\n## Saturation", "| new thing | a | `tools/a.py` | round 30 |\n\n## Saturation"), 4, 1),
        ("prose, not a row", head + "retained REA Ghidra-session log capture round 17\n", 0, 0),
        ("empty", "", 0, 0),
    ]
    for name, text, want_match, want_rev in cases:
        results, reverse = judge(stmts, closed, section_rows(text), exists)
        got = sum(v == LABEL for _, v, _ in results)
        ok = got == want_match and len(reverse) == want_rev
        fails += not ok
        print("%s\t%s\tmatch=%d reverse=%d" % ("ok" if ok else "FAIL", name, got, len(reverse)))
    uncovered = json.dumps({"rounds": [{"lane": "kaidoku", "round": 31, "admitted": True, "capabilities_added": ["new"]}]})
    s2, c2 = manifest_statements(uncovered)
    res, why = judge(s2, c2, [], exists)
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
