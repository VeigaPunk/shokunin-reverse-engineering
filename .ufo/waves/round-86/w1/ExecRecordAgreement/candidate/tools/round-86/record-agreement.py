#!/usr/bin/env python3
"""Round-86 record-agreement counter: three declared records re-derived from the bytes they describe.

The round-85 non-author spot-check routed three defects where the lane's own record text
disagreed with the committed bytes it describes (R85-3, R85-5, R85-6). This counter reads the
record and the described object at ONE revision and reports a mismatch per atom.

Atoms (frozen in `plans/round-86-claims.md`; never re-worded after data):

  A1 s303-supersede-count   `corpus/SOURCES.md` — the newest registry row whose `teaches` cell
                            opens `supersedes S303` must state, as its first integer, the exact
                            number of OTHER rows carrying the same canonical URL and must then
                            list exactly those rows' ids.
  A2 docstring-status       `tools/round-84/mutation-closure.py` — exactly one sentence of the
                            module docstring names an absent declared case, and it must name the
                            status the code assigns inside the `not case_present` branch; no
                            other status word may appear in that sentence.
  A3 receipt-pointer        `SCORECARD.md` `| coverage |` row — the row's own round R (its last
                            cell's leading integer) must be covered by a
                            `.ufo/waves/round-M/l1/scores/*.json` receipt with M >= R; that
                            receipt must be a blob at --rev and carry a 40-hex `rev` field.

Locating the objects (implementation, not atom text): the registry is the single table whose
header opens `| id |` and carries `source` and `teaches` columns; its rows are the directly
following `|` lines, 0-3 spaces indented, outside fenced code. The `| coverage |` row is the one
under `## Owned axes` (the current assessment); history rows in other sections are not the row.

Reading rule: in `--rev` mode every path is read as a committed blob (`git cat-file blob
REV:path`; S255: a committed object's bytes, never a worktree file). `--rev` must be a full
40-hex commit that resolves in --root, else exit 2. `--worktree <dir>` is FIXTURE MODE ONLY: it
reads a directory, is refused together with `--rev` (exit 2), and its receipt is labelled
`mode: worktree-fixture`, never a measurement.

Verdict: `mismatches` lists every atom id that is false. Exit 0 when `mismatches` is empty,
1 otherwise, 2 when the reading mode, revision, or control is unusable (UNEVALUABLE/REFUSED).

Control (`--control substring-only`): the cheap rule that skips the re-derivation — an atom is
agreed when the file merely CONTAINS the token it talks about. It is expected to ACCEPT the
defective records (a record can carry the right word and the wrong value); that acceptance is
what makes this counter's target failable rather than satisfied by the record's shape.

Limits (declared): these are three finite record atoms, not a whole-card audit. A1's grammar is
one declared sentence shape; A2 is a sentence-level check, not a semantics proof; A3 checks that
the named receipts exist and the covering one is revision-stamped, not that its numbers are right.
Residual: a non-covering receipt named by the row is not required to exist.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

URL_TOKEN = "rea-agents-6.5.0.tgz"
SOURCES = "corpus/SOURCES.md"
MUTATION_CLOSURE = "tools/round-84/mutation-closure.py"
CARD = "SCORECARD.md"
SCHEMA = "kaidoku-r86-record-agreement-v1"
CONTROL_NAME = "substring-only"

STATUS_WORDS = ("inconclusive", "killed", "survived", "survivor")
SUPERSEDE_RE = re.compile(r"supersedes S303(?!\d)")
COUNT_CLAUSE_RE = re.compile(r"\bcount\s+(\d{1,3})\b(.*)$", re.S)
ROW_RE = re.compile(r"^ {0,3}\|\s*S\d{3,}\s*\|")
ID_IN_TEXT_RE = re.compile(r"\bS\d{3,}\b")
RECEIPT_RE = re.compile(r"\.ufo/waves/round-(\d+)/l1/scores/[A-Za-z0-9._-]+\.json")
REV_RE = re.compile(r"[0-9a-f]{40}")
PIPE_OPEN_RE = re.compile(r"^ {0,3}\|")
FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
FENCE_CLOSE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})\s*$")


class Unreadable(Exception):
    pass


# ---------------------------------------------------------------- readers


def git_blob(root: Path, rev: str, path: str) -> str:
    """The committed blob at REV:PATH, as text. Anything else (tree, missing, binary) is unreadable."""
    spec = f"{rev}:{path}"
    kind = subprocess.run(["git", "-C", str(root), "cat-file", "-t", spec],
                          capture_output=True, text=True)
    if kind.returncode != 0 or kind.stdout.strip() != "blob":
        raise Unreadable(f"{spec}: not a blob at this revision")
    body = subprocess.run(["git", "-C", str(root), "cat-file", "blob", spec], capture_output=True)
    if body.returncode != 0:
        raise Unreadable(f"{spec}: cat-file failed")
    try:
        return body.stdout.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Unreadable(f"{spec}: not UTF-8 ({exc})") from exc


def rev_reader(root: Path, rev: str):
    def read(path: str) -> str:
        return git_blob(root, rev, path)
    return read


def worktree_reader(work: Path):
    def read(path: str) -> str:
        try:
            return (work / path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise Unreadable(f"{path}: {exc}") from exc
    return read


# ---------------------------------------------------------------- markdown locating


def split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def fenced_flags(lines: list[str]) -> list[bool]:
    flags, fence = [], None
    for line in lines:
        if fence is None:
            m = FENCE_OPEN_RE.match(line)
            flags.append(bool(m))
            if m:
                fence = m.group(1)
        else:
            flags.append(True)
            close = FENCE_CLOSE_RE.match(line)
            if close and close.group(1)[0] == fence[0] and len(close.group(1)) >= len(fence):
                fence = None
    return flags


def is_delimiter(line: str) -> bool:
    t = line.strip()
    return t.startswith("|") and set(t) <= set("|:- ") and "---" in t


def registry_rows(text: str):
    """Return (header, rows, problems, ignored) for corpus/SOURCES.md.

    A registry row is a line outside fenced code matching `^ {0,3}|\\s*S###` (the frozen row
    shape). It counts only when it directly follows a blank line, the registry header, or another
    registry row: a row-shaped line glued to prose is recorded in `ignored` and is not a row, so a
    superseding row written inside a paragraph cannot satisfy A1. Blank lines between rows are
    allowed (the registry is grouped in chunks). Exactly one `| id |` header with `source` and
    `teaches` columns must precede the rows; every counted row must carry the header's cell count.
    """
    lines = text.splitlines()
    fenced = fenced_flags(lines)
    head, delim_line, headers = None, None, 0
    rows, problems, ignored = [], [], []
    prev = "blank"
    for idx, line in enumerate(lines):
        if fenced[idx]:
            prev = "other"
            continue
        if line.strip() == "":
            prev = "blank"
            continue
        if idx == delim_line:
            prev = "header"
            continue
        if not PIPE_OPEN_RE.match(line):
            prev = "other"
            continue
        cells = split_row(line)
        if (cells[:1] == ["id"] and {"source", "teaches"} <= set(cells) and idx + 1 < len(lines)
                and not fenced[idx + 1] and is_delimiter(lines[idx + 1])):
            head, delim_line, headers = cells, idx + 1, headers + 1
            prev = "header"
            continue
        if not ROW_RE.match(line):
            prev = "other"
            continue
        if prev == "other":
            ignored.append(idx + 1)
            prev = "other"
            continue
        if head is None:
            problems.append(f"line {idx + 1}: registry row before any registry header")
        elif len(cells) != len(head):
            problems.append(f"line {idx + 1}: {len(cells)} cells, header has {len(head)}")
        else:
            rows.append({"id": cells[0], "cells": cells, "line": idx + 1})
        prev = "row"
    if headers != 1:
        return None, [], [f"expected exactly one registry header, found {headers}"], ignored
    return head, rows, problems, ignored


def owned_axes_coverage_rows(card: str):
    lines = card.splitlines()
    if "## Owned axes" not in [line.rstrip() for line in lines]:
        return None
    section, rows = None, []
    for line in lines:
        if line.startswith("## "):
            section = line[3:].strip()
        elif line.startswith("| coverage |") and section == "Owned axes":
            rows.append(line)
    return rows


# ---------------------------------------------------------------- atoms


def atom_supersede_count(read) -> tuple[bool, dict]:
    head, rows, problems, ignored = registry_rows(read(SOURCES))
    if head is None:
        return False, {"why": problems[0]}
    if problems:
        return False, {"why": "malformed registry row(s)", "problems": problems,
                       "ignored_row_shaped_lines": ignored}
    col_source, col_teaches = head.index("source"), head.index("teaches")
    url_rows = [r["id"] for r in rows if URL_TOKEN in r["cells"][col_source]]
    sup = [r for r in rows if SUPERSEDE_RE.match(r["cells"][col_teaches])]
    if not sup:
        return False, {"why": "no row whose teaches opens `supersedes S303`", "url_rows": url_rows}
    row = sup[-1]
    teaches = row["cells"][col_teaches]
    prior = sorted(i for i in url_rows if i not in (row["id"], "S303"))
    if len(re.findall(r"\bcount\b", teaches)) != 1:
        return False, {"why": "superseding row must state exactly one `count` clause",
                       "row": row["id"], "teaches": teaches[:120]}
    m = COUNT_CLAUSE_RE.search(teaches)
    if not m:
        return False, {"why": "superseding row states no `count N` clause", "row": row["id"],
                       "teaches": teaches[:120]}
    declared = int(m.group(1))
    # declared grammar: `... count N (S###/S###/...) ...` — the id list is every id after the count.
    listed = [i for i in ID_IN_TEXT_RE.findall(m.group(2)) if i != row["id"]]
    ok = (declared == len(prior) and len(listed) == declared
          and len(set(listed)) == len(listed) and sorted(listed) == prior)
    return ok, {"superseding_row": row["id"], "declared_count": declared,
                "prior_rows": prior, "declared_ids": sorted(listed),
                "url_rows_total": len(url_rows), "ignored_row_shaped_lines": ignored}


def _is_not_case_present(test: ast.expr) -> bool:
    return (isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not)
            and isinstance(test.operand, ast.Name) and test.operand.id == "case_present")


def atom_docstring_status(read) -> tuple[bool, dict]:
    try:
        tree = ast.parse(read(MUTATION_CLOSURE))
    except SyntaxError as exc:
        return False, {"why": f"target does not parse: {exc}"}
    branches = [n for n in ast.walk(tree) if isinstance(n, ast.If) and _is_not_case_present(n.test)]
    if len(branches) != 1:
        return False, {"why": f"expected exactly one `not case_present` branch, found {len(branches)}"}
    assigned = set()
    for stmt in branches[0].body:
        for node in ast.walk(stmt):
            if (isinstance(node, ast.Assign) and len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Subscript)
                    and isinstance(node.targets[0].slice, ast.Constant)
                    and node.targets[0].slice.value == "status"
                    and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)):
                assigned.add(node.value.value)
    if len(assigned) != 1:
        return False, {"why": "the `not case_present` branch must assign exactly one status",
                       "assigned": sorted(assigned)}
    label = assigned.pop()
    doc = ast.get_docstring(tree)
    if doc is None:
        return False, {"why": "no module docstring", "code_status": label}
    doc = re.sub(r"\s+", " ", doc)
    sentences = [s.strip() for s in re.split(r"(?<=[.;:])\s+", doc)
                 if "absent declared case" in s.lower()]
    if len(sentences) != 1:
        return False, {"why": "docstring does not name an absent declared case in exactly one sentence",
                       "code_status": label, "sentences": sentences}
    sentence = sentences[0]
    low = sentence.lower()
    stem = label[:5]
    names_status = re.search(rf"\b{re.escape(stem)}", low) is not None
    others = [w for w in STATUS_WORDS if w[:5] != stem and re.search(rf"\b{w}", low)]
    ok = names_status and not others
    return ok, {"code_status": label, "sentence": sentence, "conflicting_words": others}


def atom_receipt_pointer(read) -> tuple[bool, dict]:
    rows = owned_axes_coverage_rows(read(CARD))
    if rows is None:
        return False, {"why": "no `## Owned axes` section in SCORECARD"}
    if len(rows) != 1:
        return False, {"why": f"expected exactly one `| coverage |` row under `## Owned axes`, found {len(rows)}"}
    cells = split_row(rows[0])
    round_cell = cells[-1] if cells else ""
    m = re.match(r"\s*(\d{1,3})\b", round_cell)
    if not m:
        return False, {"why": "coverage row's last cell states no round", "cell": round_cell}
    claim_round = int(m.group(1))
    named = sorted({(int(r.group(1)), r.group(0)) for r in RECEIPT_RE.finditer(rows[0])})
    if not named:
        return False, {"why": "coverage row names no `.ufo/waves/round-M/l1/scores/*.json` receipt",
                       "claim_round": claim_round}
    newest = max(rnd for rnd, _ in named)
    covering = [path for rnd, path in named if rnd == newest]
    if newest < claim_round:
        return False, {"why": "named receipt predates the row's own round",
                       "claim_round": claim_round, "receipts": [p for _, p in named],
                       "receipt_round": newest}
    revs = {}
    for path in covering:
        try:
            blob = read(path)
        except Unreadable as exc:
            return False, {"why": "named receipt is not a blob at this revision", "receipt": path,
                           "error": str(exc)}
        try:
            data = json.loads(blob)
        except json.JSONDecodeError as exc:
            return False, {"why": "named receipt is not JSON", "receipt": path, "error": str(exc)}
        rev = data.get("rev") if isinstance(data, dict) else None
        if not (isinstance(rev, str) and REV_RE.fullmatch(rev)):
            return False, {"why": "named receipt is not a JSON object with a 40-hex `rev` field",
                           "receipt": path, "json_type": type(data).__name__}
        revs[path] = rev
    return True, {"claim_round": claim_round, "covering_receipts": covering,
                  "receipt_round": newest, "receipt_revs": revs}


ATOMS = (
    ("A1-s303-supersede-count", atom_supersede_count),
    ("A2-docstring-status", atom_docstring_status),
    ("A3-receipt-pointer", atom_receipt_pointer),
)


# ---------------------------------------------------------------- control


def control_substring_only(read) -> list[dict]:
    """The cheap rule: the record merely contains the token it is about."""
    out = []
    for atom_id, reader in (
        ("A1-s303-supersede-count", lambda: "supersedes S" in read(SOURCES)),
        ("A2-docstring-status", lambda: "surviv" in read(MUTATION_CLOSURE)),
        ("A3-receipt-pointer", lambda: ".ufo/waves" in read(CARD)),
    ):
        try:
            ok = bool(reader())
            detail = {"token_present": ok}
        except Unreadable as exc:
            ok, detail = False, {"error": str(exc)}
        out.append({"id": atom_id, "ok": ok, "detail": detail})
    return out


# ---------------------------------------------------------------- driver


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_atoms(read) -> list[dict]:
    atoms = []
    for atom_id, fn in ATOMS:
        try:
            ok, detail = fn(read)
        except Unreadable as exc:
            ok, detail = False, {"why": "input unreadable", "error": str(exc)}
        atoms.append({"id": atom_id, "ok": ok, "detail": detail})
    return atoms


def instrument_record(root: Path) -> dict:
    instrument = Path(__file__).resolve()
    rel = instrument.relative_to(root) if instrument.is_relative_to(root) else instrument
    return {"path": str(rel), "sha256": digest(instrument)}


def evaluate(read, rev: str, root: Path, mode: str) -> dict:
    atoms = run_atoms(read)
    mismatches = [a["id"] for a in atoms if not a["ok"]]
    return {
        "schema": SCHEMA,
        "mode": mode,
        "rev": rev,
        "root": str(root),
        "instrument": instrument_record(root),
        "atoms": atoms,
        "mismatches": mismatches,
        "agreed": len(atoms) - len(mismatches),
        "total": len(atoms),
        "ok": not mismatches,
    }


def run_control(read, rev: str, root: Path, mode: str) -> dict:
    atoms = control_substring_only(read)
    mismatches = [a["id"] for a in atoms if not a["ok"]]
    return {
        "schema": SCHEMA + "-control",
        "mode": mode,
        "control": CONTROL_NAME,
        "rev": rev,
        "instrument": instrument_record(root),
        "atoms": atoms,
        "mismatches": mismatches,
        "ok": not mismatches,
        "note": "expected to ACCEPT the defective records: the cheap rule cannot fail on a record that carries the right word",
    }


# ---------------------------------------------------------------- selftest

SOURCES_HEAD = (
    "# SOURCES\n\n## Registry\n\n"
    "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|\n"
)
URL = "https://example.invalid/rea-agents-6.5.0.tgz"
GOOD_TEACH = "supersedes S303 — corrected prior-row count 3 (S083/S090/S119); still not anchored"


def srow(rid: str, teaches: str, source: str = URL, indent: str = "") -> str:
    return f"{indent}| {rid} | {source} | code | A | x | x | {teaches} | rejected | 2026-11-04 | 180d | |"


def sources_doc(s305: str | None = GOOD_TEACH, s305_source: str = URL, s305_indent: str = "",
                extra: tuple[str, ...] = (), tail: str = "") -> str:
    rows = [srow("S001", "t", source="local note"), srow("S083", "t"), srow("S090", "t"),
            srow("S119", "t"), srow("S303", "t")]
    if s305 is not None:
        rows.append(srow("S305", s305, source=s305_source, indent=s305_indent))
    rows.extend(extra)
    return SOURCES_HEAD + "\n".join(rows) + "\n" + tail


CODE_OK = '''#!/usr/bin/env python3
"""Counter: a status per mutant.

  survived      the mutant run did not fail the declared case
  inconclusive  an anchor does not occur exactly once

QUALITY 138: an absent declared case is a survivor, never a pass.
"""
import sys


def score(case_present):
    entry = {}
    if case_present:
        entry["status"] = "killed"
    if not case_present:
        entry["status"] = "survived"
    return entry
'''
CODE_ELIF = CODE_OK.replace('    if not case_present:\n', '    elif not case_present:\n')

CARD_OK = """# Scorecard

## Owned axes

| Axis | Baseline → current | Observable | Evidence | Last-change round |
|---|---|---|---|---|
| coverage | 9.0 → 9.5 | x | `.ufo/waves/round-7/l1/scores/coverage.json` | 7 |
| depth | 9.0 → 9.0 | x | x | 5 |

## Round history

| coverage | 8.0 → 9.0 | old | `.ufo/waves/round-3/l1/scores/old.json` | 3 |
"""
RECEIPT_PATH = ".ufo/waves/round-7/l1/scores/coverage.json"
RECEIPT_OK = '{"rev": "%s", "ok": true}\n' % ("a" * 40)
GENUINE = {"corpus/SOURCES.md": sources_doc(), MUTATION_CLOSURE: CODE_OK,
           CARD: CARD_OK, RECEIPT_PATH: RECEIPT_OK}


def _write_tree(root: Path, files: dict[str, str]) -> None:
    for rel, text in files.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(cwd), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def _commit_tree(root: Path, files: dict[str, str]) -> str:
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q")
    _write_tree(root, files)
    _git(root, "add", "-A")
    _git(root, "-c", "user.name=r86-selftest", "-c", "user.email=r86-selftest@invalid",
         "-c", "commit.gpgsign=false", "commit", "-q", "-m", "fixture")
    return _git(root, "rev-parse", "HEAD")


def _atom_cases() -> list[tuple[str, str, bool, dict]]:
    """(name, atom, expect_ok, files). atom is an atom id, or 'all' for the three together."""
    A1, A2, A3 = "A1-s303-supersede-count", "A2-docstring-status", "A3-receipt-pointer"
    g = dict(GENUINE)

    def with_src(text: str) -> dict:
        return {**g, "corpus/SOURCES.md": text}

    def with_code(text: str) -> dict:
        return {**g, MUTATION_CLOSURE: text}

    def with_card(text: str, extra: dict | None = None) -> dict:
        return {**g, CARD: text, **(extra or {})}

    return [
        ("genuine-agreement", "all", True, dict(g)),
        # A1 — registry row, count clause and id list
        ("a1-wrong-count", A1, False, with_src(sources_doc(GOOD_TEACH.replace("count 3", "count 4")))),
        ("a1-id-missing-and-foreign", A1, False,
         with_src(sources_doc(GOOD_TEACH.replace("(S083/S090/S119)", "(S083/S090/S001)")))),
        ("a1-id-list-longer-than-count", A1, False,
         with_src(sources_doc(GOOD_TEACH.replace("(S083/S090/S119)", "(S083/S090/S119/S119)")))),
        ("a1-superseding-row-states-no-count", A1, False,
         with_src(sources_doc(GOOD_TEACH.replace("corrected prior-row count 3 (S083/S090/S119)",
                                                 "prior-row count stated only in prose")))),
        ("a1-row-in-prose-paragraph", A1, False,
         with_src(sources_doc(None, tail="\nIn prose: | S305 | " + URL + " | code | A | x | x | "
                                         + GOOD_TEACH + " | rejected | 2026-11-04 | 180d | |\n"))),
        ("a1-row-indent-3-spaces-accepted", A1, True,
         with_src(sources_doc(GOOD_TEACH, s305_indent="   "))),
        ("a1-row-indent-4-spaces-refused", A1, False,
         with_src(sources_doc(GOOD_TEACH, s305_indent="    "))),
        ("a1-blank-lines-between-rows-accepted", A1, True,
         with_src(sources_doc(GOOD_TEACH).replace("\n" + srow("S119", "t"), "\n\n" + srow("S119", "t")))),
        ("a1-url-row-after-blank-line-is-counted", A1, False,
         with_src(sources_doc(GOOD_TEACH, extra=("", srow("S306", "t"))))),
        ("a1-row-glued-after-prose-line-refused", A1, False,
         with_src(sources_doc(None, tail="\nNote, the superseding row follows:\n"
                                         + srow("S305", GOOD_TEACH) + "\n"))),
        ("a1-row-inside-fenced-code", A1, False,
         with_src(sources_doc(None, tail="\n```\n" + srow("S305", GOOD_TEACH) + "\n```\n"))),
        ("a1-teaches-supersedes-other-id", A1, False,
         with_src(sources_doc(GOOD_TEACH.replace("supersedes S303 —", "supersedes S3031 —")))),
        ("a1-count-clause-repeated", A1, False,
         with_src(sources_doc(GOOD_TEACH + "; count 3 (S083/S090/S119)"))),
        ("a1-malformed-extra-pipe", A1, False,
         with_src(sources_doc(GOOD_TEACH + " | extra"))),
        ("a1-newest-superseding-row-wrong", A1, False,
         with_src(sources_doc(GOOD_TEACH, s305_source="local note",
                              extra=(srow("S306", GOOD_TEACH.replace("count 3", "count 4")),)))),
        ("a1-older-superseding-row-wrong-newest-right", A1, True,
         with_src(sources_doc(GOOD_TEACH.replace("count 3", "count 4"), s305_source="local note",
                              extra=(srow("S306", GOOD_TEACH),)))),
        # A2 — docstring sentence and code branch
        ("a2-absent-case-says-inconclusive", "A2-docstring-status", False,
         with_code(CODE_OK.replace("is a survivor, never a pass", "is inconclusive, never a pass"))),
        ("a2-two-absent-case-sentences", "A2-docstring-status", False,
         with_code(CODE_OK.replace("never a pass.\n", "never a pass. An absent declared case is a survivor.\n"))),
        ("a2-status-only-in-other-sentence", "A2-docstring-status", False,
         with_code(CODE_OK.replace("is a survivor, never a pass.", "is never a pass.")
                   .replace("inconclusive  an anchor does not occur exactly once",
                            "inconclusive  an anchor does not occur exactly once. Survived mutants are listed apart."))),
        ("a2-other-sentence-status-does-not-refuse", "A2-docstring-status", True,
         with_code(CODE_OK.replace("inconclusive  an anchor does not occur exactly once",
                                   "inconclusive  an anchor does not occur exactly once. An inconclusive mutant is reported apart."))),
        ("a2-conflicting-word-in-absent-sentence", "A2-docstring-status", False,
         with_code(CODE_OK.replace("is a survivor, never a pass.", "is a survivor, not inconclusive, never a pass."))),
        ("a2-second-not-case-present-branch", "A2-docstring-status", False,
         with_code(CODE_OK + '\n\ndef other(case_present):\n    entry = {}\n    if not case_present:\n'
                              '        entry["status"] = "killed"\n    return entry\n')),
        ("a2-elif-branch-form-accepted", "A2-docstring-status", True, with_code(CODE_ELIF)),
        # A3 — the Owned-axes coverage row and its receipt
        ("a3-stale-receipt-round", "A3-receipt-pointer", False, with_card(CARD_OK.replace("| 7 |", "| 8 |"))),
        ("a3-no-receipt-named", "A3-receipt-pointer", False,
         with_card(CARD_OK.replace("`.ufo/waves/round-7/l1/scores/coverage.json`",
                                   "`.ufo/waves/round-7/l1/scores/` (directory only)"))),
        ("a3-receipt-absent-at-rev", "A3-receipt-pointer", False,
         {k: v for k, v in g.items() if k != RECEIPT_PATH}),
        ("a3-receipt-rev-39-hex", "A3-receipt-pointer", False,
         with_card(CARD_OK, {RECEIPT_PATH: '{"rev": "%s", "ok": true}\n' % ("a" * 39)})),
        ("a3-receipt-rev-6-hex", "A3-receipt-pointer", False,
         with_card(CARD_OK, {RECEIPT_PATH: '{"rev": "abc123", "ok": true}\n'})),
        ("a3-receipt-json-list-not-object", "A3-receipt-pointer", False,
         with_card(CARD_OK, {RECEIPT_PATH: '["%s"]\n' % ("a" * 40)})),
        ("a3-receipt-not-json", "A3-receipt-pointer", False,
         with_card(CARD_OK, {RECEIPT_PATH: "{rev: aaaa"})),
        ("a3-two-receipts-only-older-exists", "A3-receipt-pointer", False,
         with_card(CARD_OK.replace("`.ufo/waves/round-7/l1/scores/coverage.json`",
                                   "`.ufo/waves/round-7/l1/scores/coverage.json`, "
                                   "`.ufo/waves/round-8/l1/scores/next.json`"))),
        ("a3-two-receipts-both-exist", "A3-receipt-pointer", True,
         with_card(CARD_OK.replace("`.ufo/waves/round-7/l1/scores/coverage.json`",
                                   "`.ufo/waves/round-7/l1/scores/coverage.json`, "
                                   "`.ufo/waves/round-8/l1/scores/next.json`"),
                   {".ufo/waves/round-8/l1/scores/next.json": RECEIPT_OK})),
        ("a3-history-row-does-not-count", "A3-receipt-pointer", True, dict(g)),
        ("a3-no-owned-axes-section", "A3-receipt-pointer", False,
         with_card(CARD_OK.replace("## Owned axes", "## Axes"))),
        ("a3-two-owned-axes-coverage-rows", "A3-receipt-pointer", False,
         with_card(CARD_OK.replace("| depth |", "| coverage | 1 → 2 | y | z | 7 |\n| depth |"))),
        ("a3-receipt-path-is-directory", "A3-receipt-pointer", False,
         {k: v for k, v in g.items() if k != RECEIPT_PATH}
         | {".ufo/waves/round-7/l1/scores/coverage.json/inner.txt": "x"}),
    ]


def _rev_cases() -> list[tuple[str, str, bool, dict, dict]]:
    """(name, atom, expect_ok, committed, worktree) — the reading rule is the case."""
    defective = dict(GENUINE)
    defective["corpus/SOURCES.md"] = sources_doc(GOOD_TEACH.replace("count 3", "count 4"))
    return [
        ("rev-reads-committed-bytes-not-worktree-edits", "all", True, dict(GENUINE), defective),
        ("rev-refuses-committed-defect-despite-clean-worktree", "A1-s303-supersede-count", False,
         defective, dict(GENUINE)),
    ]


def _cli(argv: list[str], cwd: Path) -> int:
    return subprocess.run([sys.executable, "-I", "-B", str(Path(__file__).resolve()), *argv],
                          capture_output=True, text=True, cwd=cwd).returncode


def _eval_atoms(read) -> tuple[list[dict], list[dict]]:
    return run_atoms(read), control_substring_only(read)


def _check(atoms, control, atom: str, expect: bool) -> tuple[bool, bool]:
    """Returns (got, passed). A defective-record case also requires the control to accept it."""
    by_id = {a["id"]: a for a in atoms}
    if atom == "all":
        got = all(a["ok"] for a in atoms)
        return got, got is expect
    got = by_id[atom]["ok"]
    passed = got is expect
    if not expect:
        ctrl = {a["id"]: a for a in control}[atom]["ok"]
        passed = passed and ctrl
    return got, passed


def selftest(out_json: str | None) -> int:
    results: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="r86-record-agreement-selftest-") as tmp:
        base = Path(tmp)
        for name, atom, expect, files in _atom_cases():
            work = base / name
            _write_tree(work, files)
            read = worktree_reader(work)
            atoms, control = _eval_atoms(read)
            got, passed = _check(atoms, control, atom, expect)
            results.append({"name": name, "kind": "worktree-atoms", "atom": atom,
                            "expect": expect, "got": got, "ok": passed})

        for name, atom, expect, committed, worktree in _rev_cases():
            repo = base / name
            rev = _commit_tree(repo, committed)
            _write_tree(repo, worktree)
            read = rev_reader(repo, rev)
            atoms, control = _eval_atoms(read)
            got, passed = _check(atoms, control, atom, expect)
            results.append({"name": name, "kind": "rev-atoms", "atom": atom,
                            "expect": expect, "got": got, "ok": passed})

        defect_repo = base / "cli-defect-repo"
        defect = dict(GENUINE)
        defect["corpus/SOURCES.md"] = sources_doc(GOOD_TEACH.replace("count 3", "count 4"))
        defect_rev = _commit_tree(defect_repo, defect)
        good_repo = base / "cli-good-repo"
        good_rev = _commit_tree(good_repo, dict(GENUINE))
        good_wt = base / "cli-good-worktree"
        _write_tree(good_wt, dict(GENUINE))

        cli_cases = [
            ("cli-worktree-with-rev-refused", 2,
             ["--root", str(good_repo), "--worktree", str(good_wt), "--rev", good_rev]),
            ("cli-unknown-control-refused", 2,
             ["--root", str(good_repo), "--rev", good_rev, "--control", "file-exists"]),
            ("cli-rev-not-full-sha-refused", 2, ["--root", str(good_repo), "--rev", "HEAD"]),
            ("cli-rev-unknown-refused", 2, ["--root", str(good_repo), "--rev", "b" * 40]),
            ("cli-no-mode-refused", 2, ["--root", str(good_repo)]),
            ("cli-rev-genuine-exits-0", 0, ["--root", str(good_repo), "--rev", good_rev]),
            ("cli-worktree-fixture-genuine-exits-0", 0, ["--worktree", str(good_wt)]),
            ("cli-rev-defect-exits-1", 1, ["--root", str(defect_repo), "--rev", defect_rev]),
            ("cli-control-accepts-defect-exits-0", 0,
             ["--root", str(defect_repo), "--rev", defect_rev, "--control", CONTROL_NAME]),
        ]
        for name, want, argv in cli_cases:
            code = _cli(argv, base)
            results.append({"name": name, "kind": "cli", "atom": "cli", "expect": want,
                            "got": code, "ok": code == want})

    failures = [r for r in results if not r["ok"]]
    for r in results:
        verdict = "PASS" if r["ok"] else "FAIL"
        print(f"CASE {r['name']} kind={r['kind']} atom={r['atom']} expect={r['expect']} "
              f"got={r['got']} {verdict}")
    summary = f"SELFTEST cases={len(results)} failures={len(failures)}"
    print(summary)
    for r in failures:
        print(f"FAIL {r['name']}: expected {r['expect']}, got {r['got']}")
    if out_json:
        out = Path(out_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"summary": summary, "exit": 0 if not failures else 1,
                                   "cases": results}, indent=1, sort_keys=True) + "\n")
    return 0 if not failures else 1


# ---------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description="Round-86 record-agreement counter (see module docstring).")
    ap.add_argument("--root", default=".", help="lane root; a git work tree for --rev")
    ap.add_argument("--rev", help="measured revision: full 40-hex commit; every path is read as its committed blob")
    ap.add_argument("--worktree", help="FIXTURE MODE ONLY: read paths from this directory; refused with --rev")
    ap.add_argument("--control", choices=[CONTROL_NAME], help="cheap-rule control (expected to accept the defective records)")
    ap.add_argument("--selftest", action="store_true", help="run the counter's selftest fixtures")
    ap.add_argument("--selftest-json", help="with --selftest: also write the case table to this path")
    ap.add_argument("--json-out", help="write the receipt to this path")
    args = ap.parse_args()

    if args.selftest:
        return selftest(args.selftest_json)
    if args.rev is not None and args.worktree is not None:
        print("REFUSED: --worktree is fixture mode only and cannot be combined with --rev", file=sys.stderr)
        return 2

    root = Path(args.root).resolve()
    if args.rev is not None:
        if not REV_RE.fullmatch(args.rev):
            print("REFUSED: --rev must be a full 40-hex commit id", file=sys.stderr)
            return 2
        probe = subprocess.run(["git", "-C", str(root), "rev-parse", "--verify", "--quiet",
                                f"{args.rev}^{{commit}}"], capture_output=True, text=True)
        if probe.returncode != 0 or probe.stdout.strip() != args.rev:
            print(f"UNEVALUABLE: {args.rev} is not a commit in {root}", file=sys.stderr)
            return 2
        rev, mode, read = args.rev, "rev", rev_reader(root, args.rev)
    elif args.worktree is not None:
        work = Path(args.worktree).resolve()
        if not work.is_dir():
            print(f"UNEVALUABLE: --worktree {work} is not a directory", file=sys.stderr)
            return 2
        rev, mode, read = f"worktree:{work}", "worktree-fixture", worktree_reader(work)
    else:
        print("UNEVALUABLE: --rev is required (or --worktree for fixture mode)", file=sys.stderr)
        return 2

    if args.control:
        receipt = run_control(read, rev, root, mode)
    else:
        receipt = evaluate(read, rev, root, mode)

    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n")
    print(text)
    if args.control:
        print(f"CONTROL {args.control} mismatches={len(receipt['mismatches'])} accepted={receipt['ok']}")
        return 0 if receipt["ok"] else 1
    print(f"RECORD_AGREEMENT agreed={receipt['agreed']}/{receipt['total']} "
          f"mismatches={receipt['mismatches']}")
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
