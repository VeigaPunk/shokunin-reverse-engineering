#!/usr/bin/env python3
"""RV-6 non-vacuity suite for scope-creep-audit.py (round-1 blind-instrument
lesson: an audit that never fires is indistinguishable from a clean one).

Each fixture mutates the SCOPE literal by exact source-substring replacement
(rest of the file byte-identical) in a scratch copy, then runs the auditor and
asserts the declared verdict class: flags-present?, exit code, delta counts.

Count semantics (same as CR-5's scope-diff.py): a row is keyed by
(file, start, end), so any bound move shows up as added+removed, never as
"changed"; `changed` is reserved for marker/marker_line edits at a fixed key.

Usage:
  creep-fixture-suite.py <before.py> <scratch_root> <outdir>
Exit 0 iff every fixture behaves as declared.
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.join(HERE, "scope-creep-audit.py")


def row_src(f, s, e, cls, ml, mr):
    mls = "None" if ml is None else str(ml)
    mrs = "None" if mr is None else 'r"%s"' % mr
    return '("%s", %d, %d, "%s", %s, %s)' % (f, s, e, cls, mls, mrs)


def R(*a):
    return row_src(*a)


FIXTURES = [
    # name, mutate, expect_flags, expect_exit, expect_counts
    ("F0 identity (negative control)", lambda t: t, False, 0,
     {"added_keys": 0, "removed_keys": 0, "changed_rows": 0}),
    ("F1 DATED end widened 273-326 -> 273-330",
     lambda t: t.replace(R("SCORECARD.md", 273, 326, "DATED", 273, "2026-10-16"),
                         R("SCORECARD.md", 273, 330, "DATED", 273, "2026-10-16")),
     True, 1, {"added_keys": 1, "removed_keys": 1, "changed_rows": 0}),
    ("F2 CURRENT->DATED flip SCORECARD 56-60",
     lambda t: t.replace(R("SCORECARD.md", 56, 60, "CURRENT", None, None),
                         R("SCORECARD.md", 56, 60, "DATED", 56, "2026-10-16")),
     True, 1, {"changed_rows": 1}),
    ("F3 added row to EOF SCORECARD 856-1417",
     lambda t: t.replace('    ' + R("SCORECARD.md", 769, 855, "DATED", 769, "arc2-loop1-round3") + ',',
                         '    ' + R("SCORECARD.md", 769, 855, "DATED", 769, "arc2-loop1-round3") + ',\n'
                         '    ' + R("SCORECARD.md", 856, 1417, "DATED", 856, "arc3-loop1-round1") + ','),
     True, 1, {"added_keys": 1}),
    ("F4 widen-by-add/remove 703-768 absorbed into 636-702",
     lambda t: t.replace(R("SCORECARD.md", 636, 702, "DATED", 636, "2026-10-18"),
                         R("SCORECARD.md", 636, 768, "DATED", 636, "2026-10-18")
                         ).replace('    ' + R("SCORECARD.md", 703, 768, "DATED", 704, "arc2-loop1-round2") + ',\n', ''),
     True, 1, {"added_keys": 1, "removed_keys": 2}),
    ("F5 DATED start moved earlier PROVINCE 45-62 -> 44-62",
     lambda t: t.replace(R("PROVINCE.md", 45, 62, "DATED", 45, "2026-10-13"),
                         R("PROVINCE.md", 44, 62, "DATED", 45, "2026-10-13")),
     True, 1, {"added_keys": 1, "removed_keys": 1}),
    ("F6 added wide DATED row 1000-1200 (201 lines)",
     lambda t: t.replace('    ' + R("SCORECARD.md", 769, 855, "DATED", 769, "arc2-loop1-round3") + ',',
                         '    ' + R("SCORECARD.md", 769, 855, "DATED", 769, "arc2-loop1-round3") + ',\n'
                         '    ' + R("SCORECARD.md", 1000, 1200, "DATED", 1000, "arc2-loop1-round9") + ','),
     True, 1, {"added_keys": 1}),
    ("F7 range-neutral marker-only re-key marker_line 45 -> 46",
     lambda t: t.replace(R("PROVINCE.md", 45, 62, "DATED", 45, "2026-10-13"),
                         R("PROVINCE.md", 45, 62, "DATED", 46, "2026-10-13")),
     False, 0, {"changed_rows": 1}),
    ("F8 legitimate +1 renumber of 3 rows (r8 precedent)",
     lambda t: t.replace(R("SCORECARD.md", 636, 702, "DATED", 636, "2026-10-18"),
                         R("SCORECARD.md", 637, 703, "DATED", 637, "2026-10-18")
                         ).replace(R("SCORECARD.md", 703, 768, "DATED", 704, "arc2-loop1-round2"),
                                   R("SCORECARD.md", 704, 769, "DATED", 705, "arc2-loop1-round2")
                                   ).replace(R("SCORECARD.md", 769, 855, "DATED", 769, "arc2-loop1-round3"),
                                             R("SCORECARD.md", 770, 856, "DATED", 770, "arc2-loop1-round3")),
     False, 1, {"added_keys": 3, "removed_keys": 3, "changed_rows": 0}),
    ("F9 add a narrow legitimate DATED row 856-900 (45 lines)",
     lambda t: t.replace('    ' + R("SCORECARD.md", 769, 855, "DATED", 769, "arc2-loop1-round3") + ',',
                         '    ' + R("SCORECARD.md", 769, 855, "DATED", 769, "arc2-loop1-round3") + ',\n'
                         '    ' + R("SCORECARD.md", 856, 900, "DATED", 856, "arc3-loop1-round1") + ','),
     False, 1, {"added_keys": 1}),
    ("F10 added row 1268-1417 (150 lines, ends at SCORECARD EOF)",
     lambda t: t.replace('    ' + R("SCORECARD.md", 769, 855, "DATED", 769, "arc2-loop1-round3") + ',',
                         '    ' + R("SCORECARD.md", 769, 855, "DATED", 769, "arc2-loop1-round3") + ',\n'
                         '    ' + R("SCORECARD.md", 1268, 1417, "DATED", 1268, "arc3-loop1-round1") + ','),
     True, 1, {"added_keys": 1}),
    ("F11 pure row deletion (SCORECARD 534-560 removed)",
     lambda t: t.replace('    ' + R("SCORECARD.md", 534, 560, "DATED", 534, "2026-10-16") + ',\n', ''),
     True, 1, {"removed_keys": 1}),
]


def main():
    before_p, root, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(outdir, exist_ok=True)
    base = open(before_p, encoding="utf-8").read()
    results = []
    for name, mutate, want_flags, want_exit, want_counts in FIXTURES:
        mutated = mutate(base)
        change_expected = not name.startswith("F0")
        applied = (mutated != base) == change_expected
        path = os.path.join(outdir, re.sub(r"\W+", "-", name) + ".py")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(mutated)
        p = subprocess.run([sys.executable, AUDIT, before_p, path,
                            "--root", root, "--expect-rows", "20"],
                           capture_output=True, text=True)
        out = p.stdout
        m = re.search(r"CREEP FLAGS \((\d+)\)", out)
        nflags = int(m.group(1)) if m else -1
        got_counts = {"added_keys": int(re.search(r"added_keys=(\d+)", out).group(1)),
                      "removed_keys": int(re.search(r"removed_keys=(\d+)", out).group(1)),
                      "changed_rows": int(re.search(r"changed_rows=(\d+)", out).group(1))}
        ok = ((nflags > 0) == want_flags and p.returncode == want_exit
              and all(got_counts[k] == v for k, v in want_counts.items())
              and applied)
        results.append((name, ok))
        print("FIXTURE %-52s %s exit=%d flags=%d %s applied=%s"
              % (name, "PASS" if ok else "FAIL", p.returncode, nflags,
                 got_counts, applied))
        if not ok:
            print("  --- auditor output ---")
            print("  " + out.strip().replace("\n", "\n  "))
    bad = [r[0] for r in results if not r[1]]
    print("FIXTURE-SUMMARY: passed=%d failed=%d" % (len(results) - len(bad), len(bad)))
    for name in bad:
        print("  FAILED: %s" % name)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
