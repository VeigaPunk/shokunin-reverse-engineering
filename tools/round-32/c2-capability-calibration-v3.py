#!/usr/bin/env python3
"""R32-C2 counter v3 (calibration): the lane's self-declared repertoire, the SCORECARD.md
`## Capabilities` table, against the outside closure record of capabilities credited to
kaidoku rounds (fleet MANIFEST.json at a pinned fleet commit, written by non-author closures).

History, all before any seat was dispatched and before any data (claims-v3.json):
  v1 (claims.json, 9a73680a): one junk row naming all four capability phrases and rounds met it.
  v2 (claims-v2.json, 9d54070b): an evidence path that resolves but has nothing to do with the
      capability (for example tools/round-31/sqlite_oracle.py) met it.
  v3 ties the evidence to frozen anchors.

Predicate label `P2-match`, frozen in .ufo/waves/round-32/claims-v3.json:
  Forward: a statement is one `capabilities_added` item of a MANIFEST round entry with lane
  "kaidoku" at the pinned fleet commit. Its anchor paths are the relative lane paths named in
  the MANIFEST item and in the evidence cells of every capability-table row outside the
  `## Capabilities` section of SCORECARD.md AT THE BASE 283aad7f whose first cell matches the
  statement's key. It matches when the `## Capabilities` section of SCORECARD.md at REV (from
  the line `## Capabilities` to the next `## ` heading) holds a table row, not matched by
  another statement, whose first cell matches the statement's frozen key pattern and no other
  key pattern, whose last cell names exactly one round and that round is the MANIFEST round
  (`round[- ]?N`, N not followed by a digit), and whose evidence cell (third cell) names, inside
  backticks, at least one anchor path that resolves to a file at REV, and whose what-it-can-do
  cell (second cell) shares at least 5 distinct words (letters, length >= 4, case-folded) with
  the anchored description: the MANIFEST item plus the second cell of every base capability row
  (inside or outside the section) whose first cell matches the key.
  Reverse: every row of that section whose last cell names a round that has a kaidoku MANIFEST
  closure entry must be the matching row of a forward statement.
  The statement set is closed: the frozen key list must cover every capabilities_added item at
  the pin, and every statement must have at least one anchor path (else exit 2).
Target line: statements=4 match=4 target=4 reverse_mismatch=0, exit 0.

Usage: c2-capability-calibration-v3.py --root <LANE> --rev <REV> [--fleet <FLEET>] | --selftest
"""

import argparse
import json
import os
import re
import subprocess
import sys

TARGET = 4
FLEET_PIN = "cef00867ab3279ac2c2d10421e3e62c0e5d693f3"
BASE = "283aad7fe56d82f4ed4f8e43f099c2e1ceed5525"
MIN_DESC_WORDS = 5
# (MANIFEST round, frozen key pattern over the row's first cell); one per capabilities_added item.
KEYS = [
    (13, r"source(-curation)? registry"),
    (14, r"quote.{0,40}regression audit"),
    (17, r"Ghidra-session log capture"),
    (27, r"cross-pin evidence-ID attribution"),
]
LABEL = "P2-match"
ROUND_RE = re.compile(r"round[- ]?(\d+)(?!\d)")
TICK_RE = re.compile(r"`([^`]*)`")
REL_PATH_RE = re.compile(r"(?<![\w/.*-])(\.?[A-Za-z0-9_][A-Za-z0-9_.-]*(?:/[A-Za-z0-9_.-]+)+\.[A-Za-z0-9]+)(?![\w/*])")


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


def table_rows(text, inside_section):
    """Capability-table rows inside (True) or outside (False) the `## Capabilities` section."""
    rows, section, in_cap_table = [], False, False
    for ln in text.splitlines():
        if ln.startswith("## "):
            section = ln.strip() == "## Capabilities"
        if re.match(r"\|\s*Capability\s*\|", ln):
            in_cap_table = True
            continue
        if not ln.startswith("|"):
            in_cap_table = False
            continue
        if re.match(r"\|\s*-", ln):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        if inside_section and section:
            rows.append(cells)
        elif not inside_section and not section and in_cap_table:
            rows.append(cells)
    return rows


def section_rows(scorecard):
    return table_rows(scorecard, True)


def rel_paths(text, ticked_only):
    spans = TICK_RE.findall(text) if ticked_only else [text]
    out = []
    for s in spans:
        out += [p for p in REL_PATH_RE.findall(s) if not p.startswith("/")]
    return out


def anchors_for(item, pattern, base_scorecard):
    paths = set(rel_paths(item, False))
    for cells in table_rows(base_scorecard, False):
        if re.search(pattern, cells[0], re.I):
            paths |= set(rel_paths(cells[2], True))
    return paths


def words(text):
    return {w.lower() for w in re.findall(r"[A-Za-z][A-Za-z-]{3,}", text)}


def desc_anchor_words(item, pattern, base_scorecard):
    """Words of the MANIFEST item and of the what-it-can-do cell of every base capability row
    (inside or outside the section) whose first cell matches the key."""
    ws = words(item)
    for inside in (True, False):
        for cells in table_rows(base_scorecard, inside):
            if re.search(pattern, cells[0], re.I):
                ws |= words(cells[1])
    return ws


def rounds_named(cell):
    return {int(n) for n in ROUND_RE.findall(cell)}


def judge(stmts, closed, rows, base_scorecard, exists):
    results, used = [], set()
    for n, item in stmts:
        pats = [p for (k, p) in KEYS if k == n and re.search(p, item, re.I)]
        if not pats:
            return None, "key list does not cover MANIFEST round %d item %r" % (n, item[:60])
        anchors = anchors_for(item, pats[0], base_scorecard)
        if not anchors:
            return None, "no anchor path for MANIFEST round %d" % n
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
            good = sorted(p for p in set(rel_paths(cells[2], True)) if p in anchors and exists(p))
            if not good:
                why = "row %d evidence names no resolving anchor path (anchors: %s)" % (i + 1, ", ".join(sorted(anchors))[:160])
                continue
            shared = words(cells[1]) & desc_anchor_words(item, pats[0], base_scorecard)
            if len(shared) < MIN_DESC_WORDS:
                why = "row %d what-it-can-do cell shares %d words with the anchored description (< %d)" % (i + 1, len(shared), MIN_DESC_WORDS)
                continue
            hit, why = i, "row %d anchor evidence %s; description words %d" % (i + 1, ", ".join(good), len(shared))
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
    base_sc = show(root, BASE, "SCORECARD.md")
    if sc is None or base_sc is None:
        print("PIN SCORECARD.md absent at %s or at the base %s" % (rev, BASE[:12]))
        return 2
    stmts, closed = manifest_statements(mt)
    if len(stmts) != TARGET:
        print("PIN MANIFEST credits %d kaidoku capabilities at the pin, frozen %d" % (len(stmts), TARGET))
        return 2
    tree = set(git(root, "ls-tree", "-r", "--name-only", rev).stdout.splitlines())
    results, reverse = judge(stmts, closed, section_rows(sc), base_sc, lambda p: p in tree)
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
        {"lane": "kaidoku", "round": 27, "admitted": False, "capabilities_added": ["cross-pin evidence-ID attribution (tools/x/attr.mjs)"]},
        {"lane": "kaidoku", "round": 30, "admitted": True, "capabilities_added": None},
        {"lane": "kama", "round": 5, "admitted": True, "capabilities_added": ["x"]},
    ]})
    stmts, closed = manifest_statements(manifest)
    files = {"corpus/SOURCES.md", "tools/q/fid.py", "tools/g/run.sh", "tools/x/attr.mjs", "tools/other.py"}
    exists = lambda p: p in files
    hdr = "| Capability | What | Evidence | First-working round |\n|---|---|---|---|\n"
    base = ("## Capabilities\n\n" + hdr +
            "| cross-pin evidence-ID attribution for x | a | `tools/x/attr.mjs` | round 27 |\n\n## Round 13\n\n" + hdr +
            "| curated source registry for x | a | `corpus/SOURCES.md`; `/abs/tool.sh --root /abs` | round13 |\n\n## Round 14\n\n" + hdr +
            "| local raw-quote/heading regression audit | a | `python3 -I tools/q/fid.py --selftest` | round-14 |\n\n## Round 17\n\n" + hdr +
            "| retained REA Ghidra-session log capture | a | `bash tools/g/run.sh <L>`; `runs/*/r.json` | round-17 |\n")
    desc = "keeps opened scoped study sources with ordered paths and recheck cadences"
    base = base.replace("| a |", "| %s |" % desc)
    head = "## Capabilities\n\n" + hdr
    rows4 = ("| curated source registry for x | a | `corpus/SOURCES.md` | arc3-loop1-round13 |\n"
             "| local raw-quote/heading regression audit | a | `python3 -I tools/q/fid.py --selftest` | round 14 |\n"
             "| retained REA Ghidra-session log capture | a | `bash tools/g/run.sh <L>` | round 17 |\n"
             "| cross-pin evidence-ID attribution for saved REA envelopes | a | `tools/x/attr.mjs` | round 27 |\n"
             "| version-symmetry battery | a | b | luna-round-8 |\n")
    rows4 = rows4.replace("| a |", "| %s |" % desc)
    full = head + rows4 + "\n## Saturation\n"
    allin1 = head + ("| source registry, quote regression audit, Ghidra-session log capture, cross-pin evidence-ID attribution"
                     " | a | `corpus/SOURCES.md` | round 13, round 14, round 17, round 27 |\n")
    cases = [
        ("all four rows", full, 4, 0),
        ("do-nothing: base section (only round 27)", base, 1, 0),
        ("one row naming all four capabilities and rounds", allin1, 0, 1),
        ("four copies of one row with four rounds each", head + ("| retained REA Ghidra-session log capture | a | `bash tools/g/run.sh` | round 13, 14, 17, 27 |\n" * 4), 0, 4),
        ("names and rounds, no evidence path", full.replace("`python3 -I tools/q/fid.py --selftest`", "see card"), 3, 1),
        ("irrelevant but resolving evidence path", full.replace("`bash tools/g/run.sh <L>`", "`tools/other.py`"), 3, 1),
        ("anchor path unticked", full.replace("`corpus/SOURCES.md` | arc3", "corpus/SOURCES.md | arc3"), 3, 1),
        ("junk what-it-can-do cell", full.replace("| %s | `bash" % desc, "| junk | `bash"), 3, 1),
        ("anchor path not in the tree", full, 3, 1, {"tools/q/fid.py", "tools/g/run.sh", "tools/x/attr.mjs"}),
        ("rows outside the section", head + "\n## Other\n| retained REA Ghidra-session log capture | a | `bash tools/g/run.sh` | round 17 |\n", 0, 0),
        ("label only: right round, wrong capability", head + "| something | a | `tools/x/attr.mjs` | round 17 |\n", 0, 1),
        ("right capability, wrong round", head + "| retained REA Ghidra-session log capture | a | `bash tools/g/run.sh` | round 18 |\n", 0, 0),
        ("round 170 is not round 17", head + "| retained REA Ghidra-session log capture | a | `bash tools/g/run.sh` | round 170 |\n", 0, 0),
        ("over-claim row for round 30", full.replace("\n## Saturation", "| new thing | a | `tools/x/attr.mjs` | round 30 |\n\n## Saturation"), 4, 1),
        ("prose, not a row", head + "retained REA Ghidra-session log capture round 17 `bash tools/g/run.sh`\n", 0, 0),
        ("empty", "", 0, 0),
    ]
    for case in cases:
        name, text, want_match, want_rev = case[:4]
        ex = (lambda p, f=case[4]: p in f) if len(case) > 4 else exists
        results, reverse = judge(stmts, closed, section_rows(text), base, ex)
        got = sum(v == LABEL for _, v, _ in results)
        ok = got == want_match and len(reverse) == want_rev
        fails += not ok
        print("%s\t%s\tmatch=%d reverse=%d" % ("ok" if ok else "FAIL", name, got, len(reverse)))
    # Anchors come from the frozen base text, not from REV: a fake outside row added later does not count.
    fake = full.replace("`bash tools/g/run.sh <L>`", "`tools/other.py`")
    results, _ = judge(stmts, closed, section_rows(fake + "\n## Later\n" + hdr + "| retained REA Ghidra-session log capture | a | `tools/other.py` | round-17 |\n"), base, exists)
    ok = sum(v == LABEL for _, v, _ in results) == 3
    fails += not ok
    print("%s\tfake outside anchor row added at REV is ignored\tmatch=%d" % ("ok" if ok else "FAIL", sum(v == LABEL for _, v, _ in results)))
    uncovered = json.dumps({"rounds": [{"lane": "kaidoku", "round": 31, "admitted": True, "capabilities_added": ["new"]}]})
    s2, c2 = manifest_statements(uncovered)
    res, why = judge(s2, c2, [], base, exists)
    ok = res is None
    fails += not ok
    print("%s\tuncovered MANIFEST item refuses\t%s" % ("ok" if ok else "FAIL", why))
    print("selftest cases=%d failures=%d" % (len(cases) + 2, fails))
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
