#!/usr/bin/env python3
"""EX-32 (late join) — per-entry needle sweep against a tree, using the probe's
own grader. Grades every table entry individually so a single reddened needle is
attributable to its entry id, not just counted by the aggregate verdict.

Usage: per-entry-sweep.py <repo-root> [rev]
Exit 0 when every entry is clean, 1 otherwise.
"""
import importlib.util
import json
import os
import sys


def load_probe(root):
    path = os.path.join(root, ".ufo/gates/citation-drift/citation-drift-probe.py")
    spec = importlib.util.spec_from_file_location("probe", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    rev = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
    probe = load_probe(root)
    tdir = os.path.join(root, ".ufo/gates/citation-drift")
    table = json.load(open(os.path.join(tdir, "pointer-table.json")))
    expected = json.load(open(os.path.join(tdir, "expected.json")))
    entries = list(table["entries"]) + [dict(e, kind="quoted") for e in table.get("quoted", [])]

    clean, bad = 0, []
    for entry in entries:
        findings = probe.Findings()
        tree = probe.Tree(root, rev, None, expected, findings)
        probe.check_entry(dict(entry), tree, findings)
        if findings.rows:
            bad.append((entry["id"], [r[0] for r in findings.rows], findings.rows[0][2]))
        else:
            clean += 1

    print("PER_ENTRY_SWEEP root=%s rev=%s graded=%d clean=%d non_clean=%d"
          % (root, rev, len(entries), clean, len(bad)))
    for eid, ids, detail in bad:
        print("  NON_CLEAN id=%s findings=%s detail=%s" % (eid, ",".join(ids), detail))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
