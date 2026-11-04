#!/usr/bin/env python3
"""Round-87 registry-opened check: a registry row must record a document that was opened.

Mistake-mining fix for round-86 routed defect V86-2: `corpus/SOURCES.md` row S305 was admitted
with no opened document (its source cell reads "no document opened, see S303 for the URL" and
carries no URL or path). This check reads `corpus/SOURCES.md` at --base and --rev with
`git show REV:corpus/SOURCES.md` (committed bytes, never the worktree) and scores every row that
is new at --rev or whose line differs from every --base row with the same id.

A row is a line matching `^ {0,3}\\| S[0-9]{3,} \\|`; it is split on unescaped pipes (a
backslash-pipe is cell content, GFM tables) into cells. Per scored row, flags:

  cells       the row does not split into exactly 11 cells (the remaining atoms are skipped)
  opened      cell 9 (`opened`) holds no valid ISO calendar date YYYY-MM-DD
  no-document cell 6 (`anchor`) - or cell 2 (`source`), where S305 put it - says no document
                was opened ("no document opened", "not opened", "unopened", ...)
  no-locator  cell 2 (`source`) carries no URL (scheme://), DOI, absolute/home path, or
                relative path ending in a file extension

Exit 0 clean, 1 flagged (rows named on stdout JSON), 2 could-not-evaluate (git show failed or
the table header is missing at either revision). --selftest runs fixture cases with no git.

Limits (declared): the check reads the row text only. It does not fetch the URL, does not test
that a named path exists, and does not judge whether the anchor quote matches the document; a
row that names a locator it never opened passes. Unchanged rows are never scored.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

REGISTRY = "corpus/SOURCES.md"
HEADER = "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |"
ROW_RE = re.compile(r"^ {0,3}\| S[0-9]{3,} \|")
NCELLS = 11
SOURCE, ANCHOR, OPENED = 1, 5, 8
ISO_RE = re.compile(r"(?<![0-9])([0-9]{4})-([0-9]{2})-([0-9]{2})(?![0-9])")
NO_DOC_RE = re.compile(
    r"\bno\s+(?:document|doc|source|page|file|snapshot)s?\s+(?:was\s+|were\s+)?opened\b"
    r"|\b(?:not|never)\s+(?:been\s+)?opened\b|\bunopened\b",
    re.IGNORECASE,
)
LOCATOR_RES = (
    re.compile(r"\b[a-z][a-z0-9+.-]*://\S", re.IGNORECASE),           # URL
    re.compile(r"\bdoi:\s*10\.|\b10\.[0-9]{4,}/\S", re.IGNORECASE),   # DOI
    re.compile(r"(?:^|[\s`(\"',;])~?/[\w.@+-]+/[\w.@+/-]+"),        # absolute or ~/ path
    re.compile(r"(?:^|[\s`(\"',;])\.{0,2}/?(?:[\w.@+-]+/)+[\w@+-][\w.@+-]*\.[A-Za-z0-9]{1,8}(?![\w/])"),
)


class Unreadable(Exception):
    pass


def git_show(root: Path, rev: str, path: str) -> str:
    proc = subprocess.run(["git", "-C", str(root), "show", f"{rev}:{path}"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise Unreadable(f"{rev}:{path}: git show failed: {proc.stderr.strip()[:200]}")
    return proc.stdout


def split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def rows_of(text: str, label: str) -> dict[str, set[str]]:
    if HEADER not in text:
        raise Unreadable(f"{label}: registry table header not found")
    rows: dict[str, set[str]] = {}
    for line in text.splitlines():
        if ROW_RE.match(line):
            rid = line.split("|", 2)[1].strip()
            rows.setdefault(rid, set()).add(line.rstrip())
    return rows


def changed_rows(base_text: str, rev_text: str) -> list[tuple[str, str]]:
    base = rows_of(base_text, "base")
    rev = rows_of(rev_text, "rev")
    out = []
    for rid, lines in rev.items():
        for line in sorted(lines):
            if line not in base.get(rid, set()):
                out.append((rid, line))
    return sorted(out)


def has_iso_date(cell: str) -> bool:
    for y, m, d in ISO_RE.findall(cell):
        try:
            dt.date(int(y), int(m), int(d))
            return True
        except ValueError:
            continue
    return False


def has_locator(cell: str) -> bool:
    return any(r.search(cell) for r in LOCATOR_RES)


def score_row(line: str) -> list[str]:
    cells = split_row(line)
    if len(cells) != NCELLS:
        return [f"cells:{len(cells)}"]
    flags = []
    if not has_iso_date(cells[OPENED]):
        flags.append("opened")
    if NO_DOC_RE.search(cells[ANCHOR]) or NO_DOC_RE.search(cells[SOURCE]):
        flags.append("no-document")
    if not has_locator(cells[SOURCE]):
        flags.append("no-locator")
    return flags


def evaluate(base_text: str, rev_text: str) -> dict:
    scored = changed_rows(base_text, rev_text)
    flagged = []
    for rid, line in scored:
        flags = score_row(line)
        if flags:
            flagged.append({"id": rid, "flags": flags})
    return {"scored": [rid for rid, _ in scored], "flagged": flagged,
            "verdict": "flagged" if flagged else "clean"}


def _row(rid="S900", source="Doc - https://example.org/a", anchor="§1 \"quote\"",
         opened="2026-11-04") -> str:
    cells = [rid, source, "docs", "A", "scope", anchor, "teaches", "mined", opened,
             "on-release", "corpus/lessons/round-87.md"]
    return "| " + " | ".join(cells) + " |"


def _doc(*rows: str) -> str:
    return "# Sources\n\n" + HEADER + "\n|---|---|---|---|---|---|---|---|---|---|---|\n" + \
        "\n".join(rows) + "\n\n## Paths\n"


def selftest() -> int:
    base_row = _row("S100")
    base = _doc(base_row)
    s305 = ("| S305 | correction row for S303's scope count; no document opened, see S303 for the "
            "URL | code | A | Re-counts | Opened 2026-11-04; re-counted | supersedes S303 | rejected "
            "| 2026-11-04 | on-release | corpus/knowledge/x.md |")
    cases = [
        ("unchanged rows -> clean, nothing scored", base, base, "clean", [], []),
        ("added good URL row -> clean", base, _doc(base_row, _row()), "clean", ["S900"], []),
        ("added good abs-path row -> clean", base,
         _doc(base_row, _row(source="skill - `/home/u/.agents/skills/x/SKILL.md`")), "clean", ["S900"], []),
        ("added good relative-file row -> clean", base,
         _doc(base_row, _row(source="envelope - .ufo/waves/round-23/evidence/c1/a.envelope.json")),
         "clean", ["S900"], []),
        ("real S305 text -> no-document + no-locator", base, _doc(base_row, s305), "flagged", ["S305"],
         [{"id": "S305", "flags": ["no-document", "no-locator"]}]),
        ("opened cell without ISO date", base, _doc(base_row, _row(opened="pending")), "flagged",
         ["S900"], [{"id": "S900", "flags": ["opened"]}]),
        ("opened cell with impossible date", base, _doc(base_row, _row(opened="2026-13-40")), "flagged",
         ["S900"], [{"id": "S900", "flags": ["opened"]}]),
        ("anchor says no document opened", base,
         _doc(base_row, _row(anchor="No document was opened; see S303")), "flagged",
         ["S900"], [{"id": "S900", "flags": ["no-document"]}]),
        ("id-list slashes are not a path", base,
         _doc(base_row, _row(source="recount of S079/S080/S083")), "flagged",
         ["S900"], [{"id": "S900", "flags": ["no-locator"]}]),
        ("changed existing row is scored", base, _doc(_row("S100", opened="tbd")), "flagged",
         ["S100"], [{"id": "S100", "flags": ["opened"]}]),
        ("escaped pipe stays one cell", base,
         _doc(base_row, _row(anchor="regex a\\|b quoted")), "clean", ["S900"], []),
        ("wrong cell count flagged", base, _doc(base_row, _row()[:-2] + " | extra |"), "flagged",
         ["S900"], [{"id": "S900", "flags": ["cells:12"]}]),
        ("indented row (3 spaces) still scored", base, _doc(base_row, "   " + _row(opened="")),
         "flagged", ["S900"], [{"id": "S900", "flags": ["opened"]}]),
    ]
    failures = 0
    for name, b, r, verdict, scored, flagged in cases:
        got = evaluate(b, r)
        ok = got["verdict"] == verdict and got["scored"] == scored and got["flagged"] == flagged
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {name}" + ("" if ok else f" -> {got}"))
    unreadable_ok = False
    try:
        evaluate("no header here\n", base)
    except Unreadable:
        unreadable_ok = True
    failures += not unreadable_ok
    print(f"{'ok  ' if unreadable_ok else 'FAIL'} missing header -> could-not-evaluate")
    print(json.dumps({"selftest": "registry-opened-check", "cases": len(cases) + 1, "failures": failures}))
    return 0 if failures == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path)
    ap.add_argument("--base")
    ap.add_argument("--rev")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.root and a.base and a.rev):
        ap.error("--root, --base and --rev are required (or --selftest)")
    out = {"tool": "registry-opened-check", "registry": REGISTRY, "base": a.base, "rev": a.rev}
    try:
        out.update(evaluate(git_show(a.root, a.base, REGISTRY), git_show(a.root, a.rev, REGISTRY)))
    except Unreadable as e:
        out.update({"verdict": "could-not-evaluate", "error": str(e)})
        print(json.dumps(out, indent=2))
        return 2
    print(json.dumps(out, indent=2))
    return 1 if out["flagged"] else 0


if __name__ == "__main__":
    sys.exit(main())
