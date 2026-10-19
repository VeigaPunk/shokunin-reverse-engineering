#!/usr/bin/env python3
"""EX-21 independent creep auditor — SCOPE-table byte/row comparison + run invariance.

Written independently of EX-16's own audit and of the round-1 CR-5 tool (which is
also run verbatim as a second opinion). Two modes:

  compare <before.py> <after.py>
      Emits the round-1 scope-diff output grammar (rows/ADDED/REMOVED/CHANGED/
      CREEP FLAGS) plus: SCOPE-literal sha256 on both sides, scoped-file set,
      per-row full-tuple equality, and extra creep rules. Exit 0 iff the SCOPE
      literal is byte-identical; 1 if changed; 2 if either table is unparseable.

  invariance <before.py> <after.py> --root R
      Runs both censuses against root R (executes each with the current
      interpreter), compares per-file lines/loci, verdict, and the four
      verdict counters, and the current-ok locus count. Exit 0 iff invariant.

Row parsing uses ast.literal_eval per row (no regex over tuple internals), so a
row written in a non-literal form fails loudly instead of being skipped.
"""
import ast
import hashlib
import json
import re
import subprocess
import sys

ROW_RE = re.compile(r"^\s*\(.*\),?\s*$")
SCOPE_RE = re.compile(r"(?m)^SCOPE\s*=\s*\[(.*?)^\]", re.S)
DETECTORS = ("PIN", "VER", "PTR", "CACHE", "REA_GATE", "INLINE_MARKER",
             "HOLDING", "HOLDING_OK", "RECEIPT", "ANCHORS")


def literal(txt):
    m = SCOPE_RE.search(txt)
    if not m:
        return None
    return m.group(1)


def rows_of(lit, path):
    rows, bad = [], []
    for line in lit.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if not ROW_RE.match(line):
            bad.append(line)
            continue
        try:
            t = ast.literal_eval(s.rstrip(","))
        except (ValueError, SyntaxError) as ex:
            bad.append("%s  (%s)" % (line.strip(), ex))
            continue
        if not (isinstance(t, tuple) and len(t) == 6):
            bad.append("%s  (row arity %d, expected 6)" % (line.strip(), len(t)))
            continue
        rows.append(t)
    return rows, bad


def detector_table(txt):
    out = {}
    for name in DETECTORS:
        m = re.search(r"(?m)^%s\s*=\s*(.*)$" % name, txt)
        out[name] = m.group(1).strip() if m else None
    return out


def key(r):
    return (r[0], r[1], r[2])


def load(path):
    txt = open(path, encoding="utf-8").read()
    lit = literal(txt)
    if lit is None:
        return None
    rows, bad = rows_of(lit, path)
    return {"txt": txt, "lit": lit, "lit_sha": hashlib.sha256(lit.encode()).hexdigest(),
            "rows": rows, "bad": bad, "det": detector_table(txt),
            "file_sha": hashlib.sha256(txt.encode()).hexdigest(),
            "lines": len(txt.splitlines())}


def compare(before, after):
    bset = {key(r): r for r in before["rows"]}
    aset = {key(r): r for r in after["rows"]}
    added = [r for k, r in aset.items() if k not in bset]
    removed = [r for k, r in bset.items() if k not in aset]
    changed = [(bset[k], aset[k]) for k in sorted(bset.keys() & aset.keys()) if bset[k] != aset[k]]
    flags = []
    nlines = after["lines"]
    for r in added:
        f, s, e, cls = r[0], r[1], r[2], r[3]
        if e >= 9000:
            flags.append("CREEP open-ended bound: %s %d-%d %s" % (f, s, e, cls))
        if e == nlines:
            flags.append("CREEP bound reaches last line of file: %s %d-%d %s" % (f, s, e, cls))
        if cls == "DATED" and (e - s) > 150:
            flags.append("CREEP wide added DATED row: %s %d-%d (%d lines)" % (f, s, e, e - s + 1))
    for r in removed:
        flags.append("CREEP row removed (coverage loss): %s %d-%d %s" % (r[0], r[1], r[2], r[3]))
    for (bf, ba) in [(r, s) for r in added for s in removed
                     if r[0] == s[0] and r[1] <= s[1] and r[2] >= s[2]
                     and (r[1] < s[1] or r[2] > s[2])]:
        flags.append("CREEP widen-by-add/remove: %s %d-%d %s replaced %d-%d %s"
                     % (bf[0], bf[1], bf[2], bf[3], ba[1], ba[2], ba[3]))
    for (b, a) in changed:
        if b[3] == "CURRENT" and a[3] == "DATED":
            flags.append("CREEP class flip CURRENT->DATED: %s %d-%d -> %d-%d"
                         % (b[0], b[1], b[2], a[1], a[2]))
        if a[1] != b[1] or a[2] != b[2]:
            flags.append("CREEP bound moved (class %s): %s %d-%d -> %d-%d"
                         % (a[3], b[0], b[1], b[2], a[1], a[2]))
        if b[4] is not None and a[4] is not None and a[4] > b[4]:
            flags.append("CREEP marker line moved later: %s %d-%d marker %s->%s"
                         % (a[0], a[1], a[2], b[4], a[4]))
        if b[3] == "DATED" and a[3] == "CURRENT":
            flags.append("CREEP class flip DATED->CURRENT (merge risk): %s %d-%d"
                         % (a[0], a[1], a[2]))
        if b[5] != a[5]:
            flags.append("CREEP marker regex changed: %s %d-%d %r -> %r"
                         % (a[0], a[1], a[2], b[5], a[5]))
    bfiles = sorted({r[0] for r in before["rows"]})
    afiles = sorted({r[0] for r in after["rows"]})
    if bfiles != afiles:
        flags.append("CREEP scoped file set changed: %r -> %r" % (bfiles, afiles))
    return added, removed, changed, flags, bfiles, afiles


BEFORE_PATH = AFTER_PATH = ""


def print_table(before, after, added, removed, changed, flags, bfiles, afiles):
    print("before: %s  sha256=%s lines=%d scope-literal-sha256=%s"
          % (BEFORE_PATH, before["file_sha"], before["lines"], before["lit_sha"]))
    print("after : %s  sha256=%s lines=%d scope-literal-sha256=%s"
          % (AFTER_PATH, after["file_sha"], after["lines"], after["lit_sha"]))
    print("scoped files before=%r after=%r" % (bfiles, afiles))
    print("rows before=%d after=%d" % (len(before["rows"]), len(after["rows"])))
    if before["bad"] or after["bad"]:
        print("UNPARSEABLE ROWS before=%r after=%r" % (before["bad"], after["bad"]))
    print("ADDED (%d):" % len(added))
    for r in added:
        print("  + %r" % (r,))
    print("REMOVED (%d):" % len(removed))
    for r in removed:
        print("  - %r" % (r,))
    print("CHANGED (%d):" % len(changed))
    for b, a in changed:
        print("  ~ %r\n      -> %r" % (b, a))
    print("DETECTOR CONSTANTS:")
    for name in DETECTORS:
        bb, aa = before["det"][name], after["det"][name]
        mark = "same" if bb == aa else "DIFF"
        print("  [%s] %s = %s" % (mark, name, aa))
    print("CREEP FLAGS: %r" % flags)


def run_census(path, root):
    p = subprocess.run([sys.executable, path, "--root", root, "--json"],
                       capture_output=True, text=True)
    try:
        j = json.loads(p.stdout)
    except ValueError:
        j = None
    return p.returncode, j, p.stdout, p.stderr


def invariance(before, after, root):
    rc_b, j_b, out_b, err_b = run_census(BEFORE_PATH, root)
    rc_a, j_a, out_a, err_a = run_census(AFTER_PATH, root)
    print("run before: exit=%d" % rc_b)
    print("run after : exit=%d" % rc_a)
    if err_b.strip() or err_a.strip():
        print("stderr before=%r after=%r" % (err_b.strip(), err_a.strip()))
    checks = []
    if j_b is None or j_a is None:
        print("JSON PARSE FAILURE — cannot compare runs")
        print("stdout before=%r" % out_b[:400])
        print("stdout after =%r" % out_a[:400])
        return 3
    checks.append(("exit", rc_b, rc_a))
    checks.append(("verdict", j_b["verdict"], j_a["verdict"]))
    checks.append(("counts", j_b["counts"], j_a["counts"]))
    checks.append(("live", j_b["live"], j_a["live"]))
    checks.append(("g2_ok", j_b["g2_ok"], j_a["g2_ok"]))
    checks.append(("g11", j_b["g11"], j_a["g11"]))
    checks.append(("g7", j_b["g7"], j_a["g7"]))
    checks.append(("scope_errors", j_b["scope_errors"], j_a["scope_errors"]))
    checks.append(("current_ok_n", len(j_b["current_ok"]), len(j_a["current_ok"])))
    checks.append(("historical_n", len(j_b["historical"]), len(j_a["historical"])))
    bad = 0
    for (name, b, a) in checks:
        same = (b == a)
        if not same:
            bad += 1
        print("  [%s] %-14s before=%r after=%r" % ("same" if same else "DIFF", name, b, a))
    print("INVARIANCE: %s" % ("HOLDS" if bad == 0 else "BROKEN (%d diffs)" % bad))
    return 0 if bad == 0 else 1


def main():
    global BEFORE_PATH, AFTER_PATH
    mode = sys.argv[1]
    BEFORE_PATH, AFTER_PATH = sys.argv[2], sys.argv[3]
    before, after = load(BEFORE_PATH), load(AFTER_PATH)
    if before is None or after is None:
        print("SCOPE table not found in %s" % (sys.argv[2] if before is None else sys.argv[3]))
        return 2
    if mode == "compare":
        added, removed, changed, flags, bfiles, afiles = compare(before, after)
        print_table(before, after, added, removed, changed, flags, bfiles, afiles)
        if before["bad"] or after["bad"]:
            return 2
        return 0 if before["lit"] == after["lit"] else 1
    if mode == "invariance":
        return invariance(before, after, sys.argv[4])
    print("unknown mode %r" % mode)
    return 2


if __name__ == "__main__":
    sys.exit(main())
