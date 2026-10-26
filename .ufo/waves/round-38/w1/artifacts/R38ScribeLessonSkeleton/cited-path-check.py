#!/usr/bin/env python3
"""Pre-report cited-path checker (fix for R37-CL1: cite only what is committed).

Every backticked repo-relative path in a report or lesson must resolve under one
of the given roots, and a directory cited as holding receipts must hold at least
one receipt file (*.json). Exit 1 on the first unresolvable citation set, naming
each offender with its line number.

usage: cited-path-check.py DOC ROOT [ROOT ...]
  DOC     markdown file to check
  ROOT    directory a relative path may resolve under (e.g. lane root, fleet root)

No network, no writes. A `path:12` or `path:12-34` suffix is stripped before
resolution and, when the target is a file, its line range is verified against the
file's length. A directory is only held to the receipts rule when the line offers
it *as the place receipts are* ("receipts in/at/are …"), so a lesson that
describes the defect keeps quoting it. A line carrying the forward-pointer marker
[L1-FILL], and every line under a heading that carries it, is skipped and counted:
those name targets that integration creates.
"""
import os
import re
import sys

PATH_CHARS = re.compile(r"^[A-Za-z0-9_.~/][A-Za-z0-9_./~-]*$")
LINE_SUFFIX = re.compile(r"^(?P<p>[^:]+):(?P<a>\d+)(?:-(?P<b>\d+))?$")
TICK = re.compile(r"`([^`\n]+)`")
RECEIPT_CLAIM = re.compile(r"receipts?\s+(?:are|is|in|at|live|sit)\b", re.IGNORECASE)
FORWARD = "[L1-FILL]"


def candidate(span: str) -> bool:
    span = span.strip()
    if not span or " " in span or "*" in span or "{" in span or "|" in span:
        return False
    if span.startswith("/") or span.startswith("http") or span.startswith("$"):
        return False
    if "/" not in span:
        return False
    if not PATH_CHARS.match(span):
        return False
    # reject version strings and sha fragments
    if re.fullmatch(r"[0-9a-f]{7,64}", span):
        return False
    return span.startswith((".", "corpus/", "tools/", "plans/", "scripts/", "PROVINCE", "SHONEN", "SCORECARD", "SKILL", "README"))


def resolve(path: str, roots: list[str]) -> str | None:
    if path.startswith("~/"):
        p = os.path.join(os.path.expanduser("~"), path[2:])
        return p if os.path.exists(p) else None
    for root in roots:
        p = os.path.join(root, path)
        if os.path.exists(p):
            return p
    return None


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__.strip().splitlines()[-4], file=sys.stderr)
        return 2
    doc = argv[1]
    roots = [os.path.abspath(r) for r in argv[2:]]
    failures: list[str] = []
    checked = 0
    forward = 0
    in_forward = False
    with open(doc, encoding="utf-8") as fh:
        lines = fh.readlines()
    for lineno, line in enumerate(lines, 1):
        if line.lstrip().startswith("#"):
            in_forward = FORWARD in line
        if FORWARD in line or in_forward:
            forward += 1
            continue
        for span in TICK.findall(line):
            raw = span.strip().rstrip(".,;:")
            if not candidate(raw):
                continue
            path, rng = raw, None
            m = LINE_SUFFIX.match(raw)
            if m and not os.path.exists(os.path.join(roots[0], raw)):
                path, rng = m.group("p"), (int(m.group("a")), int(m.group("b") or m.group("a")))
            target = resolve(path, roots)
            checked += 1
            if target is None:
                failures.append(f"{doc}:{lineno}: unresolved path `{raw}`")
                continue
            if rng and os.path.isfile(target):
                with open(target, "rb") as f:
                    n = sum(1 for _ in f)
                if rng[1] > n:
                    failures.append(f"{doc}:{lineno}: line range `{raw}` beyond file ({n} lines)")
            if os.path.isdir(target) and RECEIPT_CLAIM.search(line):
                receipts = [e for e in os.listdir(target) if e.endswith(".json")]
                if not receipts:
                    failures.append(
                        f"{doc}:{lineno}: `{raw}` cited for receipts holds no *.json receipt "
                        f"({len(os.listdir(target))} entries)")
    if failures:
        print("\n".join(failures))
        print(f"cited-path-check: FAIL ({len(failures)} of {checked} citations)", file=sys.stderr)
        return 1
    print(f"cited-path-check: ok ({checked} citations resolved under {len(roots)} root(s); "
          f"{forward} forward-pointer line(s) skipped under {FORWARD})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
