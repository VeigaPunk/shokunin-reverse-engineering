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

Reading rule: in `--rev` mode every path is read with `git show REV:path` (S255: a committed
object's bytes, never a worktree file). `--worktree <dir>` is the selftest/fixture mode only.

Verdict: `mismatches` lists every atom id that is false. Exit 0 when `mismatches` is empty,
1 otherwise, 2 when an input cannot be read (a missing atom input is itself a mismatch only when
the record names it; an unreadable revision is exit 2).

Control (`--control substring-only`): the cheap rule that skips the re-derivation — an atom is
agreed when the file merely CONTAINS the token it talks about. It is expected to ACCEPT the
defective records (a record can carry the right word and the wrong value); that acceptance is
what makes this counter's target failable rather than satisfied by the record's shape.

Limits (declared): these are three finite record atoms, not a whole-card audit. A1's grammar is
one declared sentence shape; A2 is a sentence-level check, not a semantics proof; A3 checks that
the named receipt exists and is revision-stamped, not that the receipt's numbers are right.
"""

from __future__ import annotations

import argparse
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

STATUS_WORDS = ("inconclusive", "killed", "survived", "survivor")


class Unreadable(Exception):
    pass


def git_show(root: Path, rev: str, path: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(root), "show", f"{rev}:{path}"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise Unreadable(f"{rev}:{path}: {proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else 'git show failed'}")
    return proc.stdout


def split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def parse_registry(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", line)
        if not m:
            continue
        cells = split_row(line)
        rows.append({"id": m.group(1), "cells": cells, "line": line})
    return rows


# ---------------------------------------------------------------- atoms


def atom_supersede_count(read) -> tuple[bool, dict]:
    text = read(SOURCES)
    rows = parse_registry(text)
    if not rows:
        return False, {"why": "no registry rows parsed"}
    url_rows = [r["id"] for r in rows if URL_TOKEN in (r["cells"][1] if len(r["cells"]) > 1 else "")]
    sup = [r for r in rows if len(r["cells"]) > 6 and r["cells"][6].startswith("supersedes S303")]
    if not sup:
        return False, {"why": "no row whose teaches opens `supersedes S303`",
                       "url_rows": url_rows}
    row = sup[-1]
    teaches = row["cells"][6]
    # declared grammar: `... count N (S###/S###/...) ...` — the count is the integer that
    # follows the word `count`, and the id list is every id after it.
    m = re.search(r"count\s+(\d{1,3})(.*)$", teaches)
    prior = [i for i in url_rows if i not in (row["id"], "S303")]
    if not m:
        return False, {"why": "superseding row states no `count N` clause", "row": row["id"],
                       "teaches": teaches[:120]}
    declared = int(m.group(1))
    ids = [i for i in re.findall(r"\bS\d{3,}\b", m.group(2)) if i != row["id"]]
    ok = declared == len(prior) and sorted(set(ids)) == sorted(set(prior))
    return ok, {"superseding_row": row["id"], "declared_count": declared,
                "prior_rows": prior, "declared_ids": sorted(set(ids)),
                "url_rows_total": len(url_rows)}


def atom_docstring_status(read) -> tuple[bool, dict]:
    text = read(MUTATION_CLOSURE)
    lines = text.splitlines()
    label = None
    for i, line in enumerate(lines):
        if re.match(r"\s*(?:el)?if not case_present:\s*$", line):
            for follow in lines[i + 1:i + 6]:
                m = re.search(r'entry\["status"\]\s*=\s*"([a-z_]+)"', follow)
                if m:
                    label = m.group(1)
                    break
            break
    if label is None:
        return False, {"why": "no `elif not case_present:` branch with a status assignment"}
    m = re.search(r'"""(.*?)"""', text, re.S)
    if not m:
        return False, {"why": "no module docstring"}
    doc = re.sub(r"\s+", " ", m.group(1))
    sentences = [s for s in re.split(r"(?<=[.;:])\s+", doc) if "absent declared case" in s]
    if len(sentences) != 1:
        return False, {"why": "docstring does not name an absent declared case in exactly one sentence",
                       "code_status": label, "sentences": sentences}
    sentence = sentences[0]
    stem = label[:5]
    others = [w for w in STATUS_WORDS if w[:5] != stem and re.search(rf"\b{w}", sentence)]
    ok = stem in sentence and not others
    return ok, {"code_status": label, "sentence": sentence.strip(), "conflicting_words": others}


def atom_receipt_pointer(read) -> tuple[bool, dict]:
    card = read(CARD)
    rows = [line for line in card.splitlines() if line.startswith("| coverage |")]
    if len(rows) != 1:
        return False, {"why": f"expected exactly one `| coverage |` row, found {len(rows)}"}
    cells = split_row(rows[0])
    round_cell = cells[-1] if cells else ""
    m = re.match(r"\s*(\d{1,3})\b", round_cell)
    if not m:
        return False, {"why": "coverage row's last cell states no round", "cell": round_cell}
    claim_round = int(m.group(1))
    paths = re.findall(r"\.ufo/waves/round-(\d+)/l1/scores/([A-Za-z0-9._-]+\.json)", rows[0])
    if not paths:
        return False, {"why": "coverage row names no `.ufo/waves/round-M/l1/scores/*.json` receipt",
                       "claim_round": claim_round}
    newest = max(paths, key=lambda p: int(p[0]))
    receipt_round = int(newest[0])
    receipt = f".ufo/waves/round-{newest[0]}/l1/scores/{newest[1]}"
    if receipt_round < claim_round:
        return False, {"why": "named receipt predates the row's own round",
                       "claim_round": claim_round, "receipt": receipt,
                       "receipt_round": receipt_round}
    try:
        blob = read(receipt)
    except Unreadable as exc:
        return False, {"why": "named receipt is not a blob at this revision", "receipt": receipt,
                       "error": str(exc)}
    try:
        data = json.loads(blob)
    except json.JSONDecodeError as exc:
        return False, {"why": "named receipt is not JSON", "receipt": receipt, "error": str(exc)}
    rev = data.get("rev") if isinstance(data, dict) else None
    ok = isinstance(rev, str) and re.fullmatch(r"[0-9a-f]{40}", rev or "") is not None
    return ok, {"claim_round": claim_round, "receipt": receipt, "receipt_round": receipt_round,
                "receipt_rev": rev}


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


def evaluate(read, rev: str, root: Path) -> dict:
    atoms = []
    for atom_id, fn in ATOMS:
        try:
            ok, detail = fn(read)
        except Unreadable as exc:
            ok, detail = False, {"why": "input unreadable", "error": str(exc)}
        atoms.append({"id": atom_id, "ok": ok, "detail": detail})
    mismatches = [a["id"] for a in atoms if not a["ok"]]
    instrument = Path(__file__).resolve()
    return {
        "schema": "kaidoku-r86-record-agreement-v1",
        "rev": rev,
        "root": str(root),
        "instrument": {"path": str(instrument.relative_to(root)) if instrument.is_relative_to(root) else str(instrument),
                       "sha256": digest(instrument)},
        "atoms": atoms,
        "mismatches": mismatches,
        "agreed": len(atoms) - len(mismatches),
        "total": len(atoms),
        "ok": not mismatches,
    }


def run_control(name: str, read, rev: str, root: Path) -> dict:
    if name != "substring-only":
        raise SystemExit(f"unknown control {name}")
    atoms = control_substring_only(read)
    mismatches = [a["id"] for a in atoms if not a["ok"]]
    instrument = Path(__file__).resolve()
    return {
        "schema": "kaidoku-r86-record-agreement-v1-control",
        "control": name,
        "rev": rev,
        "instrument": {"path": str(instrument.relative_to(root)) if instrument.is_relative_to(root) else str(instrument),
                       "sha256": digest(instrument)},
        "atoms": atoms,
        "mismatches": mismatches,
        "ok": not mismatches,
        "note": "expected to ACCEPT the defective records: the cheap rule cannot fail on a record that carries the right word",
    }


# ---------------------------------------------------------------- selftest

FIXTURE_SOURCES_OK = """# SOURCES
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S001 | a | docs | A | x | x | t | mined | 2026-11-04 | 180d | |
| S083 | https://example.invalid/rea-agents-6.5.0.tgz | code | A | x | x | t | rejected | 2026-11-04 | 180d | |
| S090 | https://example.invalid/rea-agents-6.5.0.tgz | code | A | x | x | t | rejected | 2026-11-04 | 180d | |
| S119 | https://example.invalid/rea-agents-6.5.0.tgz | code | A | x | x | t | rejected | 2026-11-04 | 180d | |
| S303 | https://example.invalid/rea-agents-6.5.0.tgz | code | A | x | x | t | rejected | 2026-11-04 | 180d | |
| S305 | https://example.invalid/rea-agents-6.5.0.tgz | code | A | x | x | supersedes S303 — corrected prior-row count 3 (S083/S090/S119); still not anchored | rejected | 2026-11-04 | 180d | |
"""
FIXTURE_SOURCES_WRONG_COUNT = FIXTURE_SOURCES_OK.replace("count 3", "count 4")
FIXTURE_SOURCES_WRONG_IDS = FIXTURE_SOURCES_OK.replace("(S083/S090/S119)", "(S083/S090/S001)")
FIXTURE_SOURCES_NO_SUPERSEDE = FIXTURE_SOURCES_OK.replace(
    "corrected prior-row count 3 (S083/S090/S119); still not anchored",
    "prior-row count stated only in prose (see the round lesson); still not anchored")

FIXTURE_CODE_OK = '''#!/usr/bin/env python3
"""Counter: a status per mutant.

  survived      the mutant run did not fail the declared case
  inconclusive  an anchor does not occur exactly once

QUALITY 138: an absent declared case is a survivor, never a pass.
"""
def score(case_present):
    if not case_present:
        entry = {}
        entry["status"] = "survived"
        return entry
'''
FIXTURE_CODE_DRIFT = FIXTURE_CODE_OK.replace(
    "an absent declared case is a survivor, never a pass",
    "an absent declared case is inconclusive, never a pass")
FIXTURE_CODE_TWO_SENTENCES = FIXTURE_CODE_OK.replace(
    "QUALITY 138: an absent declared case is a survivor, never a pass.",
    "QUALITY 138: an absent declared case is a survivor, never a pass. An absent declared case is a survivor.")

FIXTURE_CARD_OK = (
    "| coverage | 9.0 -> 9.5 | evidence (`.ufo/waves/round-7/l1/scores/coverage.json`) | 7 (row) |\n"
    "| depth | 9.0 -> 9.0 | x | 5 |\n"
)
FIXTURE_CARD_STALE = FIXTURE_CARD_OK.replace("round-7/l1", "round-6/l1")
FIXTURE_CARD_NONE = FIXTURE_CARD_OK.replace("`.ufo/waves/round-7/l1/scores/coverage.json`", "`.ufo/waves/round-7/l1/scores/` (directory only, no receipt named)")
FIXTURE_RECEIPT = '{"rev": "%s", "ok": true}\n' % ("a" * 40)
FIXTURE_RECEIPT_BAD_REV = '{"rev": "abc123", "ok": true}\n'


def selftest() -> int:
    cases = []

    def case(name, expect_ok, files, atom_index):
        cases.append((name, expect_ok, files, atom_index))

    base = {
        "corpus/SOURCES.md": FIXTURE_SOURCES_OK,
        "tools/round-84/mutation-closure.py": FIXTURE_CODE_OK,
        "SCORECARD.md": FIXTURE_CARD_OK,
        ".ufo/waves/round-7/l1/scores/coverage.json": FIXTURE_RECEIPT,
    }
    case("genuine-agreement", True, base, None)
    case("a1-wrong-count", False, {**base, "corpus/SOURCES.md": FIXTURE_SOURCES_WRONG_COUNT}, 0)
    case("a1-wrong-id-set", False, {**base, "corpus/SOURCES.md": FIXTURE_SOURCES_WRONG_IDS}, 0)
    case("a1-no-superseding-row", False, {**base, "corpus/SOURCES.md": FIXTURE_SOURCES_NO_SUPERSEDE}, 0)
    case("a2-docstring-drift", False, {**base, "tools/round-84/mutation-closure.py": FIXTURE_CODE_DRIFT}, 1)
    case("a2-ambiguous-sentences", False, {**base, "tools/round-84/mutation-closure.py": FIXTURE_CODE_TWO_SENTENCES}, 1)
    case("a3-stale-receipt-round", False, {**base, "SCORECARD.md": FIXTURE_CARD_STALE}, 2)
    case("a3-no-receipt-named", False, {**base, "SCORECARD.md": FIXTURE_CARD_NONE}, 2)
    case("a3-receipt-absent-at-rev", False, {k: v for k, v in base.items() if not k.endswith("coverage.json")}, 2)
    case("a3-receipt-not-revision-stamped", False, {**base, ".ufo/waves/round-7/l1/scores/coverage.json": FIXTURE_RECEIPT_BAD_REV}, 2)

    failures = []
    with tempfile.TemporaryDirectory(prefix="r86-record-agreement-selftest-") as tmp:
        root = Path(tmp)
        for name, expect_ok, files, atom_index in cases:
            work = root / name
            for rel, text in files.items():
                target = work / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text)

            def read(path: str, _work: Path = work) -> str:
                try:
                    return (_work / path).read_text()
                except OSError as exc:
                    raise Unreadable(f"{path}: {exc}") from exc

            atoms = []
            for atom_id, fn in ATOMS:
                try:
                    ok, detail = fn(read)
                except Unreadable as exc:
                    ok, detail = False, {"error": str(exc)}
                atoms.append({"id": atom_id, "ok": ok, "detail": detail})
            if atom_index is None:
                ok = all(a["ok"] for a in atoms)
                if ok is not expect_ok:
                    failures.append(f"{name}: expected ok={expect_ok}, atoms={[a['ok'] for a in atoms]}")
            else:
                ok = atoms[atom_index]["ok"]
                if ok is not expect_ok:
                    failures.append(f"{name}: expected ok={expect_ok}, got {ok}")
            # the control must ACCEPT the defective record (it cannot fail on a word)
            if atom_index is not None:
                control_atoms = control_substring_only(read)
                if not control_atoms[atom_index]["ok"]:
                    failures.append(f"{name}: control refused a defective record (not a cheap-rule control)")
        # the control accepts the genuine world too
        work = root / "genuine-agreement"

        def genuine_read(path: str) -> str:
            return (work / path).read_text()

        control_atoms = control_substring_only(genuine_read)
        if not all(a["ok"] for a in control_atoms):
            failures.append("control refused the genuine world")

    print(f"SELFTEST cases={len(cases) + 1} failures={len(failures)}")
    for failure in failures:
        print(f"FAIL {failure}")
    return 0 if not failures else 1


# ---------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--worktree")
    ap.add_argument("--control", choices=["substring-only"])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json-out")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    root = Path(args.root).resolve()
    if not (root / SOURCES).exists() and not args.rev:
        print("UNEVALUABLE: root has no corpus/SOURCES.md and no --rev given", file=sys.stderr)
        return 2

    if args.worktree:
        work = Path(args.worktree).resolve()

        def read(path: str) -> str:
            try:
                return (work / path).read_text()
            except OSError as exc:
                raise Unreadable(f"{path}: {exc}") from exc

        rev = f"worktree:{work}"
    else:
        if not args.rev:
            print("UNEVALUABLE: --rev or --worktree is required", file=sys.stderr)
            return 2
        rev = args.rev

        def read(path: str) -> str:
            return git_show(root, rev, path)

    if args.control:
        receipt = run_control(args.control, read, rev, root)
    else:
        receipt = evaluate(read, rev, root)

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
