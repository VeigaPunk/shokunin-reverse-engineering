#!/usr/bin/env python3
"""quote-check.py — offline locator for the round-50 attempt-2 Gate quotes.

Seat ScribeLessonGate, wave 3, attempt 2.  Offline only: it reads a fetched
body from disk and asserts that each (line, substring) pair named by the
lesson's Gate table is present at that line.  It never touches the network
and never writes into the lane tree.

Usage:
    python3 -I -B quote-check.py --body <file> \
        --expect <line>:<substring> [--expect <line>:<substring> ...] \
        [--label <name>]

Exit codes (lane semantics):
    0  every expectation located
    1  at least one expectation missing (violation)
    2  could not evaluate (missing body / bad arguments)

Output: one TSV line per expectation, then a summary line
`located=<n> missing=<m>` and the body's sha256.
"""

from __future__ import annotations

import argparse
import hashlib
import sys


def die(msg: str, code: int) -> "int":
    print(msg, file=sys.stderr)
    return code


def main(argv: "list[str]") -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--body", required=True)
    ap.add_argument("--expect", action="append", default=[])
    ap.add_argument("--label", default="")
    args = ap.parse_args(argv)

    try:
        with open(args.body, "rb") as fh:
            raw = fh.read()
    except OSError as exc:
        return die("cannot read body: %s" % exc, 2)
    if not args.expect:
        return die("no --expect given", 2)

    digest = hashlib.sha256(raw).hexdigest()
    lines = raw.decode("utf-8", errors="replace").split("\n")

    located = 0
    missing = 0
    label = args.label or args.body
    for spec in args.expect:
        lineno, _, needle = spec.partition(":")
        try:
            lineno = int(lineno)
        except ValueError:
            return die("bad --expect (no line number): %r" % spec, 2)
        if lineno < 1 or lineno > len(lines):
            print("%s\tMISS\t:%d\t%s" % (label, lineno, needle))
            missing += 1
            continue
        text = lines[lineno - 1]
        if needle in text:
            print("%s\tOK\t:%d\t%s" % (label, lineno, needle))
            located += 1
        else:
            print("%s\tMISS\t:%d\t%s" % (label, lineno, needle))
            missing += 1

    print("located=%d missing=%d sha256=%s" % (located, missing, digest))
    return 0 if missing == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
