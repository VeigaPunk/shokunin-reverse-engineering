#!/usr/bin/env python3
"""Lexical audit for unqualified find/du use over /fast/scratch.

The tool reads only the explicit UTF-8 transcript/receipt paths given on argv.
It never walks a directory tree. A hit is a lexical command invocation whose
same simple-command arguments mention /fast/scratch: bare `find`/`du` are RED,
exactly `/usr/bin/find` and `/usr/bin/du` are GREEN, any other path-qualified
command is RED.

Exit: 0 no red, 1 red hit(s), 2 could-not-evaluate (bad path, non-UTF-8, usage).

`--selftest` runs 14 in-memory lexical cases plus 3 outer CLI cases over
isolated tiny fixture files under the fixed authorized scratch root
`/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard` (never the install/live tree):
red literal find (exit 1, bare-find), green absolute find/du (exit 0), and a
missing file (exit 2). Each outer case asserts the child exit code and the
stable finding rows, then removes its unique fixture tree.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from typing import NamedTuple

LIMITATION_QUOTED_PROSE = (
    "quoted-prose limitation: the scan is lexical, so a command quoted, echoed, "
    "commented, or cited in prose is indistinguishable from an executed command. "
    "RED hits can be false positives, and GREEN lines do not prove execution."
)
LIMITATION_SCOPE = (
    "scope limitation: only an explicit /fast/scratch argument in the same simple "
    "command is seen; cwd (cd /fast/scratch && find .), variables, aliases, and "
    "command substitution are not resolved."
)

_SELFTEST_TIMEOUT = 30
_SELFTEST_ROOT = "/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard"

_FAST_SCRATCH = re.compile(r"(?<![A-Za-z0-9_.-])/fast/scratch(?![A-Za-z0-9_.-])")
_COMMAND = re.compile(
    r"""(?<![\w.:])(?P<path>(?:\.{1,2}/|~/|/)(?:[^\s;|&()`'"]*/)*?(?P<pname>find|du))(?![A-Za-z0-9_.-])"""
    r"""|(?<![\w./])(?P<name>find|du)(?![A-Za-z0-9_./-])"""
)
_BREAK = re.compile(r"&&|\|\||[;|`]")


class Hit(NamedTuple):
    line: int
    kind: str
    rule: str
    text: str


def _logical_lines(text: str) -> list[tuple[int, str]]:
    """Join backslash continuations, keeping the first physical line number."""
    physical = text.splitlines()
    rows: list[tuple[int, str]] = []
    index = 0
    while index < len(physical):
        start = index + 1
        current = physical[index]
        while index + 1 < len(physical):
            trailing = len(current) - len(current.rstrip("\\"))
            if trailing % 2 == 0:
                break
            current = current[:-1] + " " + physical[index + 1]
            index += 1
        rows.append((start, current))
        index += 1
    return rows


def _simple_tail(line: str, start: int) -> str:
    boundary = _BREAK.search(line, start)
    return line[start : boundary.start()] if boundary else line[start:]


def _snippet(line: str) -> str:
    text = " ".join(line.split())
    return text if len(text) <= 240 else text[:237] + "..."


def audit_text(text: str) -> tuple[list[Hit], int]:
    hits: list[Hit] = []
    rows = _logical_lines(text)
    for lineno, line in rows:
        for match in _COMMAND.finditer(line):
            if match.group("path") is not None:
                command = match.group("path")
                name = match.group("pname")
                if command == "/usr/bin/" + name:
                    kind, rule = "GREEN", "absolute-" + name
                else:
                    kind, rule = "RED", "other-path-" + name
            else:
                name = match.group("name")
                kind, rule = "RED", "bare-" + name
            if not _FAST_SCRATCH.search(_simple_tail(line, match.end())):
                continue
            hits.append(Hit(lineno, kind, rule, _snippet(line)))
    return hits, len(rows)


def scan_file(path: str) -> tuple[list[Hit], int, str | None]:
    if not os.path.isfile(path):
        return [], 0, "not a regular file"
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except OSError as exc:
        return [], 0, "read error: %s" % exc
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [], 0, "not UTF-8: %s" % exc
    hits, line_count = audit_text(text)
    return hits, line_count, None


def run_files(paths: list[str]) -> int:
    print("LIMITATION\tquoted-prose\t" + LIMITATION_QUOTED_PROSE)
    print("LIMITATION\tscope\t" + LIMITATION_SCOPE)
    errors = red = green = lines = hits_total = 0
    for path in paths:
        hits, line_count, error = scan_file(path)
        lines += line_count
        if error is not None:
            errors += 1
            print("ERROR\t%s\t%s" % (path, error))
            continue
        hits_total += len(hits)
        for hit in hits:
            if hit.kind == "RED":
                red += 1
            else:
                green += 1
            print("%s\t%s:%d\t%s\t%s" % (hit.kind, path, hit.line, hit.rule, hit.text))
    print(
        "SUMMARY\tfiles=%d\tlines=%d\thits=%d\tred=%d\tgreen=%d\terrors=%d"
        % (len(paths), lines, hits_total, red, green, errors)
    )
    if errors:
        print("RESULT\tERROR")
        return 2
    if red:
        print("RESULT\tFAIL")
        return 1
    print("RESULT\tPASS")
    return 0


SELFTEST_CASES: list[tuple[str, str, list[tuple[int, str, str]]]] = [
    ("red-literal-find", "find /fast/scratch/hyaku -maxdepth 1", [(1, "RED", "bare-find")]),
    ("red-literal-du", "du -sh /fast/scratch/hyaku/kaidoku-r33", [(1, "RED", "bare-du")]),
    (
        "green-absolute-find",
        "/usr/bin/find /fast/scratch/hyaku -maxdepth 1",
        [(1, "GREEN", "absolute-find")],
    ),
    (
        "green-absolute-du",
        "/usr/bin/du -sh /fast/scratch/hyaku/kaidoku-r33",
        [(1, "GREEN", "absolute-du")],
    ),
    ("green-unrelated-path", "du -sh /home/vgpnk/Projects", []),
    ("green-prefix-boundary", "find /fast/scratchpad -maxdepth 1", []),
    (
        "red-env-wrapper",
        "env FOO=1 find /fast/scratch/hyaku -type f | wc -l",
        [(1, "RED", "bare-find")],
    ),
    (
        "red-relative-path",
        "./find /fast/scratch/hyaku -maxdepth 1",
        [(1, "RED", "other-path-find")],
    ),
    ("red-du-option", "du --max-depth=1 /fast/scratch", [(1, "RED", "bare-du")]),
    ("red-after-and", "du -sh /home && find /fast/scratch", [(1, "RED", "bare-find")]),
    (
        "green-red-mixed",
        "/usr/bin/du -sh /fast/scratch && du -sh /fast/scratch",
        [(1, "GREEN", "absolute-du"), (1, "RED", "bare-du")],
    ),
    (
        "quoted-prose-limitation",
        "Never run `find /fast/scratch` from a shell builtin.",
        [(1, "RED", "bare-find")],
    ),
    (
        "joined-continuation",
        "find \\\n/fast/scratch/hyaku -maxdepth 1",
        [(1, "RED", "bare-find")],
    ),
    ("green-prose-slash-compound", "NEVER run du/find over /fast/scratch through bash builtins.", []),
]


def _invoke_cli(script: str, target: str) -> subprocess.CompletedProcess[str]:
    python = sys.executable or "python3"
    return subprocess.run(
        [python, "-I", "-B", script, target],
        capture_output=True,
        text=True,
        timeout=_SELFTEST_TIMEOUT,
    )


def _hit_rows(stdout: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for line in stdout.splitlines():
        fields = line.split("\t")
        if len(fields) >= 3 and fields[0] in ("RED", "GREEN"):
            rows.append((fields[0], fields[1], fields[2]))
    return rows


def _outer_case(
    name: str,
    script: str,
    target: str,
    want_rc: int,
    want_hits: list[tuple[str, str, str]],
    want_result: str,
    want_error: str | None = None,
) -> bool:
    try:
        proc = _invoke_cli(script, target)
    except (OSError, subprocess.SubprocessError, UnicodeError) as exc:
        print("OUTER\tFAIL\t%s\tinvoke_error=%s" % (name, exc))
        return False
    lines = proc.stdout.splitlines()
    got_hits = _hit_rows(proc.stdout)
    ok = (
        proc.returncode == want_rc
        and got_hits == want_hits
        and ("RESULT\t" + want_result) in lines
        and (want_error is None or want_error in lines)
    )
    if ok:
        print("OUTER\tPASS\t%s\texit=%d\thits=%s" % (name, proc.returncode, got_hits))
    else:
        print(
            "OUTER\tFAIL\t%s\texit=%d\texpected_exit=%d\thits=%s\texpected_hits=%s\tstderr=%r"
            % (name, proc.returncode, want_rc, got_hits, want_hits, proc.stderr)
        )
    return ok


def _cli_selftest(script: str) -> tuple[int, int, int, bool]:
    """Run the three outer CLI cases over isolated fixtures under the fixed scratch root."""
    total = 3
    passed = failed = 0
    cleanup_ok = True
    fixtures: str | None = None
    try:
        # Selftest writes only under the fixed authorized scratch root, never the
        # install/live tree. mkdtemp gives each run an isolated unique child; only
        # that child is removed, so the authorized root survives.
        os.makedirs(_SELFTEST_ROOT, exist_ok=True)
        fixtures = tempfile.mkdtemp(prefix="selftest-fixtures-", dir=_SELFTEST_ROOT)
        red_path = os.path.join(fixtures, "red-literal-find.txt")
        green_path = os.path.join(fixtures, "green-absolute.txt")
        missing_path = os.path.join(fixtures, "missing-file.txt")
        with open(red_path, "w", encoding="utf-8") as handle:
            handle.write("find /fast/scratch/hyaku -maxdepth 1\n")
        with open(green_path, "w", encoding="utf-8") as handle:
            handle.write(
                "/usr/bin/find /fast/scratch/hyaku -maxdepth 1\n"
                "/usr/bin/du -sh /fast/scratch/hyaku\n"
            )
        cases = [
            (
                "outer-red-literal-find",
                red_path,
                1,
                [("RED", red_path + ":1", "bare-find")],
                "FAIL",
                None,
            ),
            (
                "outer-green-absolute",
                green_path,
                0,
                [
                    ("GREEN", green_path + ":1", "absolute-find"),
                    ("GREEN", green_path + ":2", "absolute-du"),
                ],
                "PASS",
                None,
            ),
            (
                "outer-missing-file",
                missing_path,
                2,
                [],
                "ERROR",
                "ERROR\t%s\tnot a regular file" % missing_path,
            ),
        ]
        for name, target, want_rc, want_hits, want_result, want_error in cases:
            if _outer_case(name, script, target, want_rc, want_hits, want_result, want_error):
                passed += 1
            else:
                failed += 1
    except OSError as exc:
        print("OUTER\tFAIL\tsetup\t%s" % exc)
        failed = total - passed
    finally:
        if fixtures is not None:
            try:
                shutil.rmtree(fixtures)
                print("CLEANUP\tPASS\t%s" % fixtures)
            except OSError as exc:
                cleanup_ok = False
                print("CLEANUP\tFAIL\t%s\t%s" % (fixtures, exc))
    return passed, failed, total, cleanup_ok


def selftest() -> int:
    print("LIMITATION\tquoted-prose\t" + LIMITATION_QUOTED_PROSE)
    print("LIMITATION\tscope\t" + LIMITATION_SCOPE)
    passed = failed = 0
    for name, text, expected in SELFTEST_CASES:
        hits, _ = audit_text(text)
        got = [(hit.line, hit.kind, hit.rule) for hit in hits]
        if got == expected:
            passed += 1
            print("SELFTEST\tPASS\t%s\t%s" % (name, got))
        else:
            failed += 1
            print("SELFTEST\tFAIL\t%s\texpected=%s\tgot=%s" % (name, expected, got))
    outer_passed, outer_failed, outer_total, cleanup_ok = _cli_selftest(os.path.abspath(__file__))
    total_pass = passed + outer_passed
    total_fail = failed + outer_failed
    print(
        "SELFTEST SUMMARY\tlexical=%d\touter=%d\tcases=%d\tpass=%d\tfail=%d\tcleanup=%s"
        % (
            len(SELFTEST_CASES),
            outer_total,
            len(SELFTEST_CASES) + outer_total,
            total_pass,
            total_fail,
            "PASS" if cleanup_ok else "FAIL",
        )
    )
    if total_fail or not cleanup_ok:
        print("RESULT\tFAIL")
        return 1
    print("RESULT\tPASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit explicit UTF-8 transcripts for unqualified find/du over /fast/scratch."
    )
    parser.add_argument("--selftest", action="store_true", help="run the built-in case battery")
    parser.add_argument("files", nargs="*", metavar="FILE", help="explicit UTF-8 file paths")
    args = parser.parse_args()
    if args.selftest:
        if args.files:
            print("ERROR\tusage\t--selftest takes no FILE arguments", file=sys.stderr)
            return 2
        return selftest()
    if not args.files:
        print(
            "ERROR\tusage\tlist explicit UTF-8 file paths or use --selftest",
            file=sys.stderr,
        )
        return 2
    return run_files(args.files)


if __name__ == "__main__":
    sys.exit(main())
