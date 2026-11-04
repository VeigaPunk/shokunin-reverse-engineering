#!/usr/bin/env python3
"""R83-C1 candidate: positive source-attribution grammar for knowledge entries.

Frozen house grammar (plans/round-83-claims.md, deliberately bounded):
  * exactly one line-start ``source:`` field within the first twelve lines;
  * its value begins with a nonempty comma-separated list of ``S`` followed
    by at least three ASCII digits, then space-em-dash-space;
  * only those leading ids are positive attribution; all remaining prose is
    commentary and never attributes;
  * duplicated source fields or malformed headers are unbound/false.

``entry_cites`` depends only on ``re`` and references no module globals, so
the frozen counter can extract the single function through AST.

CLI exit codes: 0 cited, 1 not cited, 2 unavailable (entry unreadable,
sid malformed, or finding could not be written).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SCHEMA = "kaidoku-r83-source-bind-v1"
SID_RE = re.compile(r"S[0-9]{3,}\Z")


# --------------------------------------------------------------------------
# grammar authority (self-contained; extracted by the frozen counter)
# --------------------------------------------------------------------------

def entry_cites(text: str, sid: str) -> bool:
    fields = [(index, line) for index, line in enumerate(text.splitlines())
              if line.startswith("source:")]
    if len(fields) != 1 or fields[0][0] >= 12:
        return False
    match = re.fullmatch(
        r"source: (S[0-9]{3,}(?:, *S[0-9]{3,})*) — .*", fields[0][1])
    if match is None:
        return False
    return sid in [part.strip() for part in match.group(1).split(",")]


# --------------------------------------------------------------------------
# stable finding: the extracted function is the only grammar implementation
# --------------------------------------------------------------------------

def assess_text(text: str, sid: str) -> dict:
    cites = entry_cites(text, sid)
    return {"schema": SCHEMA, "sid": sid, "cites": cites,
            "status": "attributed" if cites else "not-attributed"}


def emit(finding: dict, json_out: str | None) -> bool:
    if json_out is None:
        return True
    try:
        with open(json_out, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(finding, ensure_ascii=False) + "\n")
    except OSError as error:
        print(f"source-bind: cannot write {json_out}: {error}", file=sys.stderr)
        return False
    return True


def unavailable(sid: str, reason: str) -> dict:
    return {"schema": SCHEMA, "sid": sid, "cites": False,
            "status": "unavailable", "line": None, "ids": None,
            "reason": reason}


# --------------------------------------------------------------------------
# selftest: own CLI against private fixtures; working root preserved
# --------------------------------------------------------------------------

FIXTURES = (
    ("positive", "source: S286, S299 — paired primary sources\n", "S299", 0),
    ("withdrawn",
     "source: S286 — duplicate S299 withdrawn in-round\n"
     "verified-at: fixture\n\n# Entry\n\nbody mentions S299 in prose only\n",
     "S299", 1),
    ("malformed", "source: note: duplicate S299 withdrawn\n", "S299", 1),
    ("duplicate",
     "source: S299 — first field\nsource: S286 — second field\n", "S299", 1),
    ("duplicate-after-window",
     "source: S299 — first field\n" + "\n" * 11
     + "source: S286 — second field\n", "S299", 1),
    ("unavailable", None, "S299", 2),
)


def selftest(json_out: str | None) -> int:
    root = os.getcwd()
    work = tempfile.mkdtemp(prefix="source-bind-selftest-")
    script = os.path.abspath(__file__)
    checks: list[dict] = []
    try:
        for name, text, sid, expected in FIXTURES:
            entry = os.path.join(work, f"{name}.txt")
            if text is not None:
                with open(entry, "w", encoding="utf-8") as handle:
                    handle.write(text)
            findings = []
            exits = []
            for run in (0, 1):
                out = os.path.join(work, f"{name}-{run}.json")
                argv = [sys.executable, "-I", "-B", script,
                        "--entry", entry, "--sid", sid, "--json-out", out]
                completed = subprocess.run(argv, cwd=root)
                exits.append(completed.returncode)
                if os.path.exists(out):
                    with open(out, "r", encoding="utf-8") as handle:
                        findings.append(handle.read())
            stable = len(findings) == 2 and findings[0] == findings[1]
            expected_finding = (
                unavailable(sid, "entry-unreadable") if expected == 2 else
                {"schema": SCHEMA, "sid": sid, "cites": expected == 0,
                 "status": "attributed" if expected == 0 else "not-attributed"})
            ok = (exits == [expected, expected] and stable
                  and json.loads(findings[0]) == expected_finding)
            finding = json.loads(findings[0]) if findings else None
            checks.append({"case": name, "expected_rc": expected,
                           "rcs": exits, "stable": stable, "ok": ok,
                           "finding": finding})
    finally:
        shutil.rmtree(work, ignore_errors=True)
    passed = all(check["ok"] for check in checks) and os.getcwd() == root
    receipt = {"schema": SCHEMA + "-selftest", "passed": passed,
               "working_root_preserved": os.getcwd() == root,
               "checks": checks}
    if not emit(receipt, json_out):
        return 2
    for check in checks:
        print(f"selftest {check['case']}: "
              f"{'ok' if check['ok'] else 'FAIL'} rc={check['rcs']}")
    print(f"selftest: {'passed' if passed else 'FAILED'}")
    return 0 if passed else 1


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--entry")
    ap.add_argument("--sid")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest(args.json_out)
    if not args.entry or not args.sid:
        ap.error("--entry and --sid are required without --selftest")
    if not SID_RE.fullmatch(args.sid):
        emit(unavailable(args.sid, "sid-malformed"), args.json_out)
        return 2
    try:
        with open(args.entry, "r", encoding="utf-8") as handle:
            text = handle.read()
    except (OSError, UnicodeError):
        emit(unavailable(args.sid, "entry-unreadable"), args.json_out)
        return 2
    finding = assess_text(text, args.sid)
    if not emit(finding, args.json_out):
        return 2
    return 0 if finding["cites"] else 1


if __name__ == "__main__":
    sys.exit(main())
