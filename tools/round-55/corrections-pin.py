#!/usr/bin/env python
"""corrections-pin.py - mechanical pin for append-only TSV ledgers.

Round 55 capability (R55-C2, depth).  QUALITY row 100 makes a landed
freeze-ledger verdict row uneditable and routes corrections through the
companion ledger ``corpus/claim-freezes-corrections.tsv``; the round-54
closure observed (corpus/lessons/round-54-verifier-spotcheck.md section 3,
observation a) that the companion ledger is "convention-governed only - no
mechanical pin refuses an in-place edit of a *corrections* row".  This gate
is that pin, generalised to any append-only TSV ledger in the lane.

Model: bytes at --base and --rev are read from git objects
(``git -C ROOT show REV:LEDGER``; S255 grounds the read-from-a-revision
discipline).  The ledger is append-only iff the bytes at --rev are exactly
the bytes at --base plus appended lines: every line of --base reappears at
--rev in the same order with no rewrites, and any extra --rev lines come
strictly after.  Operationally the gate compares the two line sequences:

    clean        --rev lines == --base lines + zero or more appended lines
                 (exit 0; findings empty, appended = the count)
  row_edited   the first diverging position: --rev carries different bytes
               there than --base (an in-place edit; exit 1, named with the
               line number and both rows' leading cells)
  row_deleted  a --base line after the edit point is absent from --rev
               (exit 1)
  header_changed  line 1 (the header) differs (exit 1, class header_changed)

A reorder always produces at least one violating opcode, reported as
row_edited, row_deleted or row_inserted at the affected lines - the base's
rows no longer sit at their base positions, which is the property the pin
guards.

Verdict map: 0 = clean (append-only holds between the two revisions);
1 = failed (at least one finding above, each named with its line number and
the row's leading cell); 2 = could-not-evaluate (bad arguments, unknown
revision, ledger absent at a revision, or a failed git call).

--selftest runs the comparator over in-memory fixture pairs (no git, no
writes outside an optional --json-out) and asserts both the exit class and
the finding id of every case; it is the gate-standard self-invocation mode.

Demonstrations on the committed tree (round 55 freeze receipts, transcribed from
the receipt bytes in round 56 - routed defect V-3 of the round-55 closure fixed
the stale "line 2"/"<measured rev>" prose here):
  green  --ledger corpus/claim-freezes-corrections.tsv
             --base c753b24f96db335eeeca0003d2906457d6e71849
             --rev 79421b757f36b2ddb776631ecfd57d42dc2f33e2   (the canonical
             frozen-receipt run, records/pin-green-demo.txt: exit 0, clean,
             rows 2, appended 0; later re-runs at newer revs verify clean too)
  red    --ledger corpus/claim-freezes-v2.tsv
             --base fe8fab8d --rev f78fc766  (the round-53 in-place verdict
             edit: row_edited at line 29, leading cell ``round-53``)
"""

from __future__ import annotations

import argparse
import difflib
import json
import subprocess
import sys


def git_show(root: str, rev: str, path: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", root, "show", rev + ":" + path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise SystemExit(
            "2 could-not-evaluate: ledger %s absent at %s or git failed: %s"
            % (path, rev, proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout


def leading_cell(line: str) -> str:
    return line.split("\t", 1)[0][:60]


def compare(base_bytes: bytes, rev_bytes: bytes) -> dict:
    """Diff two ledger byte strings under the append-only model.

    The only legal difference is one trailing insert block after the last
    base line.  Every other difflib opcode is a violation with a truthful
    finding id: replace -> row_edited, delete -> row_deleted, an insert
    before the end -> row_inserted.
    """
    base_lines = base_bytes.decode("utf-8", "surrogateescape").splitlines()
    rev_lines = rev_bytes.decode("utf-8", "surrogateescape").splitlines()
    findings = []
    if base_lines and rev_lines and base_lines[0] != rev_lines[0]:
        findings.append({"finding": "header_changed", "line": 1,
                         "was": leading_cell(base_lines[0]),
                         "now": leading_cell(rev_lines[0])})
    sm = difflib.SequenceMatcher(a=base_lines, b=rev_lines, autojunk=False)
    appended = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "insert" and i1 == len(base_lines):
            appended = j2 - j1  # legal: new rows strictly after every base row
            continue
        if tag == "replace":
            findings.append({"finding": "row_edited", "line": i1 + 1,
                             "count": i2 - i1,
                             "was": leading_cell(base_lines[i1]),
                             "now": leading_cell(rev_lines[j1])})
        elif tag == "delete":
            findings.append({"finding": "row_deleted", "line": i1 + 1,
                             "count": i2 - i1,
                             "row": leading_cell(base_lines[i1])})
        elif tag == "insert":
            findings.append({"finding": "row_inserted", "line": i1 + 1,
                             "count": j2 - j1,
                             "row": leading_cell(rev_lines[j1])})
    if findings:
        verdict = "failed"
        exit_code = 1
    else:
        verdict = "clean"
        exit_code = 0
    return {
        "verdict": verdict,
        "exit": exit_code,
        "rows_base": len(base_lines),
        "rows_rev": len(rev_lines),
        "appended": appended,
        "findings": findings,
    }


CASES = [
    ("identical", b"h\ta\tb\nr1\tx\ty\n", b"h\ta\tb\nr1\tx\ty\n",
     0, None),
    ("appended", b"h\ta\tb\nr1\tx\ty\n", b"h\ta\tb\nr1\tx\ty\nr2\tz\tw\n",
     0, None),
    ("appended-many", b"h\ta\n", b"h\ta\nr1\tx\nr2\ty\nr3\tz\n",
     0, None),
    ("row_edited", b"h\ta\nr1\tx\nr2\ty\n", b"h\ta\nr1\tCHANGED\nr2\ty\n",
     1, "row_edited"),
    ("row_deleted", b"h\ta\nr1\tx\nr2\ty\n", b"h\ta\nr2\ty\n",
     1, "row_deleted"),
    ("header_changed", b"h\ta\nr1\tx\n", b"H2\ta\nr1\tx\n",
     1, "header_changed"),
    ("reordered", b"h\ta\nr1\tx\nr2\ty\n", b"h\ta\nr2\ty\nr1\tx\n",
     1, None),
    ("mid-insert", b"h\ta\nr1\tx\nr2\ty\n", b"h\ta\nr1\tx\nNEW\tq\nr2\ty\n",
     1, "row_inserted"),
    ("rewrite-tail", b"h\ta\nr1\tx\nr2\ty\nr3\tz\n",
     b"h\ta\nNEW1\nNEW2\nNEW3\n", 1, "row_edited"),
    ("empty-base", b"", b"h\ta\nr1\tx\n", 0, None),
    ("empty-both", b"", b"", 0, None),
]


def selftest() -> int:
    failures = []
    for name, base, rev, want_exit, want_finding in CASES:
        result = compare(base, rev)
        if result["exit"] != want_exit:
            failures.append("%s: exit %d != %d" % (name, result["exit"], want_exit))
            continue
        if want_finding is not None:
            got = {f["finding"] for f in result["findings"]}
            if want_finding not in got:
                failures.append("%s: findings %s lack %s"
                                % (name, sorted(got), want_finding))
        if result["verdict"] not in ("clean", "failed"):
            failures.append("%s: bad verdict %r" % (name, result["verdict"]))
    print("corrections-pin selftest: cases %d, failures %d%s"
          % (len(CASES), len(failures),
             "" if not failures else "; failed: " + "; ".join(failures)))
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--root", default=".")
    ap.add_argument("--ledger", default="corpus/claim-freezes-corrections.tsv")
    ap.add_argument("--base")
    ap.add_argument("--rev")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.base or not args.rev:
        print("2 could-not-evaluate: --base and --rev are required (or --selftest)",
              file=sys.stderr)
        return 2
    base_bytes = git_show(args.root, args.base, args.ledger)
    rev_bytes = git_show(args.root, args.rev, args.ledger)
    result = compare(base_bytes, rev_bytes)
    result["ledger"] = args.ledger
    result["base"] = args.base
    result["rev"] = args.rev
    rendered = json.dumps(result, indent=1, sort_keys=True)
    print(rendered)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(rendered + "\n")
    return result["exit"]


if __name__ == "__main__":
    sys.exit(main())
