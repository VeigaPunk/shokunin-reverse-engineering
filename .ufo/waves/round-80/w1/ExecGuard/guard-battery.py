#!/usr/bin/env python3
"""Round-80 receipt-guard battery: the nine `validate_receipt()` clauses, bound one-to-one to the
round-80 SKILL decision table and to one isolating selftest case each, and proved load-bearing by
deletion.

The round-79 mutation battery (`tools/round-79/gate-mutation.py`) proved that three of the
round-78 attack gate's `validate_receipt()` refusal clauses survive deletion with every selftest
case green, and its second finding names the class: each clause is a sentence of a frozen kill
rule with no isolating case.  This battery freezes the repair and measures it.

    --battery   enumerate `validate_receipt()`'s `defects.append(...)` clauses at a measured
                revision, parse the round-80 SKILL decision-table block, bind every clause to
                exactly one row, replace each clause statement with `pass` in a scratch copy of
                the gate, and judge each mutant by the row's declared selftest case.
    --selftest  unit cases for the battery's own helpers (parsing, binding, mutation, verdicts).
    --validate  re-derive a receipt's counts from the committed blobs and from its own lists.

BINDING.  A clause is bound when (a) it is named by exactly one row, (b) that row's backticked
message prefix is a prefix of the clause's message literal, (c) the row's backticked case name
occurs as `case("<name>"` (or `case('<name>'`) in the gate's `selftest()` source, and (d) no other
row names the same clause id or the same case name.  A row with no clause is an orphan, a row
whose prefix prefixes no clause or two clauses binds nothing, and a clause with two rows binds
nothing: each is a named defect, never resolved to the first candidate.

MESSAGE LITERAL.  A clause's message is the concatenation of the literal parts of its
`defects.append(...)` argument, with the interpolated holes elided.  So
`f"{fixture.get('id')}: fixture dir mismatch"` has the message `: fixture dir mismatch` and the
stable leading literal `: fixture dir mismatch`, which is the frozen row prefix.  A row prefix is
scored against that message, so a prefix can never match across a hole.

KILL.  A clause is killed only when it is bound AND its declared case is present in the mutant's
selftest output AND the case fails there.  An absent declared case is a survivor, never a pass
(round 79's rule).  A mutant whose anchor does not occur exactly once, whose copy does not
compile, or whose copy prints no `SELFTEST cases=<n> failures=<m>` summary is INCONCLUSIVE and
never a kill.  An unbound clause is a survivor regardless of what the mutant does, so the
do-nothing control - no table block and no isolating case - reports rows 0, bound 0, survivors 9.

Exit: 0 when guards > 0, rows == guards, bound == guards, survivors == 0 and pristine.failures
== 0; 1 otherwise; 2 could-not-evaluate.

Scratch: mutant copies live under --work (default: a fresh directory under $TMPDIR, never a bare
`/tmp` path); the caller passes a directory under $HYAKU_SCRATCH and removes it.
"""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROUND = 80
GATE = "tools/round-78/attack-gate.py"
SKILL = "SKILL.md"
BLOCK_BEGIN = "<!-- round-80 receipt-guard table: begin -->"
BLOCK_END = "<!-- round-80 receipt-guard table: end -->"
SELFTEST_LINE = re.compile(r"^SELFTEST cases=(?P<cases>\d+) failures=(?P<failures>\d+)$")
ROW_ID = re.compile(r"^G(?P<num>\d{2})-(?P<slug>[a-z0-9][a-z0-9-]*)$")
TICK = re.compile(r"`([^`]+)`")
CHILD_KEYS = ("HOME", "LANG", "PATH", "TMPDIR")
PREDICATE = (
    "R80-C3 is verified iff `python3 -I -B tools/round-80/guard-battery.py --root . --rev "
    "<measured> --json-out <receipt>` exits 0 with `guards 9`, `rows 9`, `bound 9`, "
    "`survivors 0`, `pristine.cases 37`, `pristine.failures 0`, `target_pin.matched true` and a "
    "defect-free `--validate`, while at base `16dfa009` the same command exits 1 with `guards 9`, "
    "`rows 0`, `bound 0`, `survivors 9`."
)


class Unevaluable(Exception):
    """Exit-2 class: the battery cannot score, so it claims nothing."""


# ----------------------------------------------------------------- helpers ---

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_commit(value) -> bool:
    return (isinstance(value, str) and len(value) == 40
            and all(ch in "0123456789abcdef" for ch in value))


def git_show(root: str, rev: str, path: str) -> bytes | None:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def resolve_commit(root: str, rev: str) -> str:
    """The 40-hex commit a symbolic or abbreviated revision names."""
    proc = subprocess.run(["git", "-C", root, "rev-parse", "--verify",
                           f"{rev}^{{commit}}"], capture_output=True, text=True)
    resolved = proc.stdout.strip()
    if proc.returncode != 0 or not is_commit(resolved):
        raise Unevaluable(f"{rev!r} is not a committed revision of {root}")
    return resolved


def find_function(tree: ast.AST, name: str):
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return node
    return None


# ------------------------------------------------------ clause enumeration ---

def string_parts(node) -> list[tuple[str, str]] | None:
    """Ordered ('lit' | 'hole', text) parts of a string expression, or None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [("lit", node.value)]
    if isinstance(node, ast.JoinedStr):
        parts: list[tuple[str, str]] = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(("lit", value.value))
            elif isinstance(value, ast.FormattedValue):
                parts.append(("hole", ast.unparse(value.value)))
            else:
                return None
        return parts
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = string_parts(node.left)
        right = string_parts(node.right)
        if left is None or right is None:
            return None
        return left + right
    return None


def leading_literal(parts: list[tuple[str, str]], message: str) -> str:
    """Stable leading literal of a clause message, skipping a leading hole."""
    if parts and parts[0][0] == "lit" and parts[0][1]:
        return parts[0][1]
    for kind, text in parts[1:]:
        if kind == "lit" and text:
            return text
    return message


def enumerate_clauses(text: str) -> list[dict]:
    """Every `defects.append(...)` statement of validate_receipt(), in source order."""
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        raise Unevaluable(f"gate blob does not parse: {exc}") from exc
    function = find_function(tree, "validate_receipt")
    if function is None:
        raise Unevaluable("validate_receipt() is absent from the gate blob")
    statements = []
    for node in ast.walk(function):
        if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)):
            continue
        func = node.value.func
        if not (isinstance(func, ast.Attribute) and func.attr == "append"):
            continue
        if not (isinstance(func.value, ast.Name) and func.value.id == "defects"):
            continue
        statements.append(node)
    statements.sort(key=lambda node: (node.lineno, node.col_offset))
    if not statements:
        raise Unevaluable("validate_receipt() has no defects.append clause; the empty set "
                          "cannot be scored (empty-set gaming)")
    clauses: list[dict] = []
    for index, node in enumerate(statements, start=1):
        parts = string_parts(node.value.args[0]) if node.value.args else None
        message = "".join(text for kind, text in parts if kind == "lit") if parts else None
        template = ("".join(text if kind == "lit" else "{" + text + "}"
                            for kind, text in parts) if parts else None)
        clauses.append({
            "clause_id": f"G{index:02d}",
            "line": node.lineno,
            "end_line": node.end_lineno,
            "col_offset": node.col_offset,
            "message": message,
            "template": template,
            "prefix": leading_literal(parts, message) if parts else None,
            "literal_parts": len(parts) if parts else 0,
            "statement": ast.get_source_segment(text, node),
        })
    return clauses


def selftest_source(text: str) -> str:
    """The source of the gate's selftest() function."""
    tree = ast.parse(text)
    function = find_function(tree, "selftest")
    if function is None:
        raise Unevaluable("selftest() is absent from the gate blob")
    source = ast.get_source_segment(text, function)
    if not source:
        raise Unevaluable("selftest() source is not recoverable from the gate blob")
    return source


def case_declared(source: str, name: str) -> bool:
    """True when the selftest source declares `case("<name>"` (either quote style)."""
    return f'case("{name}"' in source or f"case('{name}'" in source


# --------------------------------------------------------- decision table ---

def split_row(line: str) -> list[str]:
    """Split a table row on unescaped `|`, unescaping `\\|`."""
    cells: list[str] = []
    current: list[str] = []
    index = 0
    while index < len(line):
        char = line[index]
        if char == "\\" and index + 1 < len(line) and line[index + 1] == "|":
            current.append("|")
            index += 2
            continue
        if char == "|":
            cells.append("".join(current))
            current = []
            index += 1
            continue
        current.append(char)
        index += 1
    cells.append("".join(current))
    return cells


def parse_skill(text: str) -> dict:
    """The round-80 receipt-guard table block: rows and named defects."""
    if BLOCK_BEGIN not in text or BLOCK_END not in text:
        return {"block_present": False, "rows": [], "defects": [], "ignored": [],
                "body_lines": 0}
    body = text.split(BLOCK_BEGIN, 1)[1].split(BLOCK_END, 1)[0]
    lines = body.splitlines()
    rows: list[dict] = []
    defects: list[str] = []
    ignored: list[str] = []
    for offset, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line or not line.startswith("|"):
            continue
        cells = split_row(line)
        if len(cells) >= 2 and not cells[0].strip() and not cells[-1].strip():
            inner = cells[1:-1]
        else:
            inner = cells
        if inner and all(re.fullmatch(r":?-{2,}:?", cell.strip() or "-")
                         for cell in inner):
            continue  # markdown separator row
        first = inner[0].strip() if inner else ""
        if not ROW_ID.match(first) and "`" not in line and not re.match(r"^[Gg]\d", first):
            continue  # prose line, not a data row
        if len(inner) != 4:
            defects.append(f"malformed row at block line {offset}: {len(inner)} cells, "
                           f"want 4: {line}")
            continue
        match = ROW_ID.match(first)
        if not match:
            if re.match(r"^[Gg]\d", first):
                defects.append(f"malformed row at block line {offset}: id {first!r} is "
                               f"not G<NN>-<slug>")
            else:
                ignored.append(line)  # a header or legend line, not a data row
            continue
        prefixes = TICK.findall(inner[2])
        if len(prefixes) != 1 or not prefixes[0].strip() or not prefixes[0]:
            defects.append(f"malformed row at block line {offset}: message cell is not "
                           f"exactly one non-empty backticked span")
            continue
        cases = TICK.findall(inner[3])
        if len(cases) != 1 or not cases[0].strip():
            defects.append(f"malformed row at block line {offset}: case cell is not "
                           f"exactly one non-empty backticked span")
            continue
        rows.append({
            "id": first,
            "clause_id": "G" + match.group("num"),
            "slug": match.group("slug"),
            "trigger": inner[1].strip(),
            "prefix": prefixes[0],
            "case": cases[0].strip(),
            "block_line": offset,
        })
    return {"block_present": True, "rows": rows, "defects": defects,
            "ignored": ignored, "body_lines": len(lines)}


# ---------------------------------------------------------------- binding ---

def bind_rows(clauses: list[dict], rows: list[dict], source: str) -> dict:
    """Bind each clause to one row, one prefix and one declared selftest case."""
    defects: list[str] = []
    known = {clause["clause_id"] for clause in clauses}
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        grouped.setdefault(row["clause_id"], []).append(row)
    for clause_id in sorted(grouped):
        group = grouped[clause_id]
        if len(group) > 1:
            defects.append(f"duplicate clause id {clause_id}: {len(group)} rows declared "
                           f"(want exactly 1)")
    cases_seen: dict[str, list[str]] = {}
    for row in rows:
        cases_seen.setdefault(row["case"], []).append(row["id"])
        matches = [clause for clause in clauses
                   if isinstance(clause.get("message"), str)
                   and clause["message"].startswith(row["prefix"])]
        row["prefix_matches"] = [clause["clause_id"] for clause in matches]
        row["case_in_source"] = case_declared(source, row["case"])
        row["reason"] = None
        if row["clause_id"] not in known:
            defects.append(f"orphan row {row['id']}: no clause with id {row['clause_id']}")
            row["reason"] = "orphan"
            continue
        if not row["prefix"]:
            defects.append(f"row {row['id']}: empty message prefix")
            row["reason"] = "empty prefix"
            continue
        if not matches:
            defects.append(f"row {row['id']}: prefix {row['prefix']!r} prefixes no clause")
            row["reason"] = "no prefix match"
            continue
        if len(matches) > 1:
            defects.append(f"row {row['id']}: prefix {row['prefix']!r} matches "
                           f"{len(matches)} clauses ({', '.join(row['prefix_matches'])}); "
                           f"an ambiguous prefix binds nothing")
            row["reason"] = "ambiguous prefix"
            continue
        if matches[0]["clause_id"] != row["clause_id"]:
            defects.append(f"row {row['id']}: prefix {row['prefix']!r} binds "
                           f"{matches[0]['clause_id']}, not {row['clause_id']}")
            row["reason"] = "prefix binds another clause"
            continue
        if not row["case"]:
            defects.append(f"row {row['id']}: no case name")
            row["reason"] = "no case"
            continue
        if not row["case_in_source"]:
            defects.append(f"row {row['id']}: declared case {row['case']!r} is absent from "
                           f"the gate's selftest source")
            row["reason"] = "case absent from source"
            continue
        row["reason"] = "bound"
    for case, row_ids in sorted(cases_seen.items()):
        if len(row_ids) > 1:
            defects.append(f"selftest case {case!r} is declared by {len(row_ids)} rows "
                           f"({', '.join(row_ids)})")
    bound_ids: list[str] = []
    for clause in clauses:
        group = grouped.get(clause["clause_id"]) or []
        row = group[0] if len(group) == 1 else None
        bound = bool(row and row.get("reason") == "bound"
                     and len(cases_seen.get(row["case"], [])) == 1)
        clause["row"] = row
        clause["declared_case"] = row["case"] if row is not None else None
        clause["bound"] = bound
        if bound:
            bound_ids.append(clause["clause_id"])
    return {"bound_ids": bound_ids, "defects": defects}


# --------------------------------------------------------------- mutation ---

def mutate(text: str, clause: dict) -> tuple[str | None, str]:
    """Replace one clause's `defects.append(...)` statement with `pass`."""
    lines = text.splitlines(keepends=True)
    start = clause["line"] - 1
    end = clause["end_line"]
    if start < 0 or end > len(lines) or start >= end:
        return None, "statement line span is outside the blob"
    segment = "".join(lines[start:end])
    if not segment.strip():
        return None, "statement segment is empty"
    hits = text.count(segment)
    if hits != 1:
        return None, f"statement occurs {hits} times in the gate blob, want exactly 1"
    first_line = lines[start]
    if first_line[:clause["col_offset"]].strip():
        return None, "statement does not begin its line; in-place replacement refused"
    indent = first_line[:len(first_line) - len(first_line.lstrip())]
    replacement = indent + "pass" + ("\n" if segment.endswith("\n") else "")
    return text.replace(segment, replacement, 1), "applied"


def compile_check(source: str, filename: str) -> tuple[bool, str]:
    try:
        compile(source, filename, "exec")
        return True, ""
    except SyntaxError as exc:
        return False, f"{exc.__class__.__name__}: {exc}"


def run_selftest(path: str, env: dict, cwd: str) -> tuple[int, str, str]:
    proc = subprocess.run([sys.executable, "-I", "-B", path, "--selftest"],
                          capture_output=True, text=True, env=env, cwd=cwd,
                          timeout=300)
    return proc.returncode, proc.stdout, proc.stderr


def parse_selftest(stdout: str) -> tuple[dict[str, bool], int | None, int | None]:
    """Read the case JSON lines and the SELFTEST summary."""
    cases: dict[str, bool] = {}
    cases_n = failures_n = None
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            match = SELFTEST_LINE.match(line)
            if match:
                cases_n = int(match.group("cases"))
                failures_n = int(match.group("failures"))
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(entry, dict) and isinstance(entry.get("case"), str):
            cases[entry["case"]] = bool(entry.get("pass"))
    return cases, cases_n, failures_n


def judge_mutant(declared_case, compiled: bool, exit_code, parsed: dict) -> dict:
    """A clause's mutant verdict from its declared case and the copy's own output."""
    cases, cases_n, failures_n = parsed
    entry = {
        "compiled": bool(compiled),
        "exit": exit_code,
        "cases": cases_n,
        "failures": failures_n,
        "failed_cases": sorted(name for name, ok in cases.items() if not ok),
        "case_present": False,
        "case_failed": False,
        "status": "inconclusive",
        "reason": None,
    }
    if not compiled:
        entry["reason"] = "mutant copy does not compile"
        return entry
    if cases_n is None:
        entry["reason"] = "mutant copy printed no SELFTEST summary"
        return entry
    if declared_case is None:
        entry["status"] = "unbound"
        entry["reason"] = "no row declares a case for this clause"
        return entry
    entry["case_present"] = declared_case in cases
    entry["case_failed"] = entry["case_present"] and cases[declared_case] is False
    if not entry["case_present"]:
        entry["status"] = "survived"
        entry["reason"] = "declared case absent from the mutant output"
        return entry
    if not entry["case_failed"]:
        entry["status"] = "survived"
        entry["reason"] = "declared case passes on the mutant"
        return entry
    entry["status"] = "killed"
    return entry


# ------------------------------------------------------------- the counter ---

def verdict_exit(guards: int, rows: int, bound: int, survivors: int,
                 pristine_failures: int) -> int:
    if guards <= 0:
        return 1
    if rows != guards or bound != guards:
        return 1
    if survivors != 0 or pristine_failures != 0:
        return 1
    return 0


def run_pristine(blob: bytes, work: str) -> dict:
    """Run the unmodified gate's own --selftest under a four-key child environment."""
    path = os.path.join(work, "attack-gate-pristine.py")
    with open(path, "wb") as handle:
        handle.write(blob)
    env = {key: os.environ.get(key, "") for key in CHILD_KEYS}
    env["TMPDIR"] = work
    exit_code, out, err = run_selftest(path, env, work)
    cases, cases_n, failures_n = parse_selftest(out)
    return {"exit": exit_code, "cases": cases_n, "failures": failures_n,
            "case_names": sorted(cases),
            "failed_cases": sorted(name for name, ok in cases.items() if not ok),
            "stderr_tail": err.strip().splitlines()[-1:]}


def build_receipt(clauses: list[dict], block: dict, binding: dict, pristine: dict,
                  pin: dict, rev: str, blob: bytes, expect_guards=None) -> dict:
    guards = len(clauses)
    rows_detail = block["rows"]
    rows = len(rows_detail)
    bound = sum(1 for clause in clauses if clause.get("bound"))
    killed = sum(1 for clause in clauses if clause.get("killed"))
    survivor_ids = [clause["clause_id"] for clause in clauses if not clause.get("killed")]
    defects = list(block["defects"]) + list(binding["defects"])
    for clause in clauses:
        case = clause.get("declared_case")
        if clause.get("bound") and case in (pristine.get("failed_cases") or []):
            defects.append(f"{clause['clause_id']}: declared case {case!r} also fails on "
                           f"the pristine instrument (not isolating)")
    if expect_guards is not None and guards != expect_guards:
        defects.append(f"guards {guards} != expected {expect_guards}")
    exit_code = verdict_exit(guards, rows, bound, len(survivor_ids),
                            pristine.get("failures") or 0)
    receipt = {
        "schema": "kaidoku-r80-guard-battery-v1",
        "round": ROUND,
        "predicate": PREDICATE,
        "checked_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "instrument": {"path": "tools/round-80/guard-battery.py",
                       "sha256": sha256_bytes(pathlib.Path(__file__).read_bytes())},
        "rev": rev,
        "target": {"path": GATE, "rev": rev, "bytes": len(blob),
                   "sha256": sha256_bytes(blob)},
        "target_pin": pin,
        "guards": guards,
        "rows": rows,
        "bound": bound,
        "killed": killed,
        "survivors": len(survivor_ids),
        "survivor_ids": survivor_ids,
        "pristine": pristine,
        "table": {"block_present": block["block_present"],
                  "body_lines": block["body_lines"],
                  "ignored_lines": block["ignored"]},
        "rows_detail": rows_detail,
        "guard_defects": defects,
        "clauses": clauses,
        "expect_guards": expect_guards,
    }
    receipt["exit"] = exit_code
    receipt["ok"] = bool(exit_code == 0 and pin.get("matched") and not defects)
    return receipt


def battery(root: str, rev: str, work: str, expect_sha256, expect_guards) -> dict:
    rev_input = rev
    rev = resolve_commit(root, rev)
    blob = git_show(root, rev, GATE)
    if blob is None:
        raise Unevaluable(f"{GATE} is not a committed blob at {rev}")
    skill_blob = git_show(root, rev, SKILL)
    if skill_blob is None:
        raise Unevaluable(f"{SKILL} is not a committed blob at {rev}")
    try:
        text = blob.decode("utf-8")
        skill_text = skill_blob.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Unevaluable(f"target blob is not UTF-8: {exc}") from exc
    clauses = enumerate_clauses(text)
    source = selftest_source(text)
    block = parse_skill(skill_text)
    binding = bind_rows(clauses, block["rows"], source)
    os.makedirs(work, exist_ok=True)
    run_root = tempfile.mkdtemp(prefix="guard-battery-", dir=work)
    env = {key: os.environ.get(key, "") for key in CHILD_KEYS}
    env["TMPDIR"] = run_root
    pristine = run_pristine(blob, run_root)
    pristine["ok"] = bool(pristine["exit"] == 0 and pristine["failures"] == 0
                          and pristine["cases"] is not None)
    for clause in clauses:
        mutated, note = mutate(text, clause)
        entry = {"applied": mutated is not None, "apply_note": note,
                 "compiled": False, "exit": None, "cases": None, "failures": None,
                 "failed_cases": [], "case_present": False, "case_failed": False,
                 "status": "inconclusive", "reason": note}
        if mutated is not None:
            compiled, compile_note = compile_check(mutated, clause["clause_id"])
            entry["compiled"] = compiled
            entry["compile_note"] = compile_note
            if compiled:
                copy = os.path.join(run_root, clause["clause_id"] + "-mutant.py")
                with open(copy, "w", encoding="utf-8") as handle:
                    handle.write(mutated)
                m_exit, m_out, m_err = run_selftest(copy, env, run_root)
                entry["stderr_tail"] = m_err.strip().splitlines()[-1:]
                entry.update(judge_mutant(clause.get("declared_case"), True, m_exit,
                                          parse_selftest(m_out)))
        clause["mutant"] = entry
        clause["killed"] = bool(clause.get("bound")) and entry["status"] == "killed"
    actual = sha256_bytes(blob)
    pin = {"expected": expect_sha256, "actual": actual,
           "matched": bool(isinstance(expect_sha256, str) and expect_sha256 == actual)}
    receipt = build_receipt(clauses, block, binding, pristine, pin, rev, blob,
                            expect_guards)
    receipt["rev_input"] = rev_input
    return receipt


# --------------------------------------------------------------- validate ---

def validate_receipt(receipt: dict, root: str = ".", blobs: dict | None = None,
                     recheck_pristine: bool = True) -> dict:
    """Re-derive every count from the committed blobs and the receipt's own lists."""
    defects: list[str] = []
    instrument = receipt.get("instrument") or {}
    if instrument.get("sha256") != sha256_bytes(pathlib.Path(__file__).read_bytes()):
        defects.append("instrument sha256 is not this file's digest")
    if not receipt.get("checked_at"):
        defects.append("checked_at is absent")
    if receipt.get("round") != ROUND:
        defects.append(f"round is not {ROUND}")
    rev = receipt.get("rev")
    if not is_commit(rev):
        defects.append("rev is not a 40-hex commit")
    clauses = receipt.get("clauses") or []
    rows_detail = receipt.get("rows_detail") or []
    pristine = receipt.get("pristine") or {}
    pin = receipt.get("target_pin") or {}
    ids = [clause.get("clause_id") for clause in clauses]
    if len(ids) != len(set(ids)):
        defects.append("duplicate clause id")
    if not clauses:
        defects.append("empty clause set: no receipt-validation clause is enumerated")
    if ids != [f"G{index:02d}" for index in range(1, len(ids) + 1)]:
        defects.append("clause ids are not G01..Gnn in source order")
    if receipt.get("guards") != len(clauses):
        defects.append("guards does not re-derive from the clause list")
    if receipt.get("rows") != len(rows_detail):
        defects.append("rows does not re-derive from the row list")
    declared_cases = [row.get("case") for row in rows_detail]
    if len(declared_cases) != len(set(declared_cases)):
        defects.append("a selftest case is declared by two rows")
    row_ids = [row.get("id") for row in rows_detail]
    if len(row_ids) != len(set(row_ids)):
        defects.append("duplicate row id")
    bound = sum(1 for clause in clauses if clause.get("bound"))
    if receipt.get("bound") != bound:
        defects.append("bound does not re-derive from the clause list")
    killed = sum(1 for clause in clauses if clause.get("killed"))
    if receipt.get("killed") != killed:
        defects.append("killed does not re-derive from the clause list")
    survivor_ids = [clause["clause_id"] for clause in clauses if not clause.get("killed")]
    if receipt.get("survivor_ids") != survivor_ids:
        defects.append("survivor_ids do not re-derive from the clause list")
    if receipt.get("survivors") != len(survivor_ids):
        defects.append("survivors does not re-derive from the clause list")
    for clause in clauses:
        clause_id = clause.get("clause_id")
        mutant = clause.get("mutant") or {}
        if clause.get("bound"):
            row = clause.get("row") or {}
            prefix = row.get("prefix")
            if not row.get("id"):
                defects.append(f"{clause_id}: bound without a row")
            if not isinstance(prefix, str) or not prefix:
                defects.append(f"{clause_id}: bound on an empty or absent row prefix")
            elif not str(clause.get("message") or "").startswith(prefix):
                defects.append(f"{clause_id}: its row prefix is not a prefix of its message")
            if clause.get("declared_case") != row.get("case"):
                defects.append(f"{clause_id}: declared case differs from its row")
        else:
            if clause.get("killed"):
                defects.append(f"{clause_id}: killed while unbound")
        if (clause.get("bound")
                and clause.get("declared_case") in (pristine.get("failed_cases") or [])):
            defects.append(f"{clause_id}: declared case also fails on the pristine "
                           f"instrument (not isolating)")
        if clause.get("killed"):
            if not mutant.get("compiled"):
                defects.append(f"{clause_id}: killed from a copy that does not compile")
            if mutant.get("cases") is None:
                defects.append(f"{clause_id}: killed from a copy with no SELFTEST summary")
            if not (mutant.get("case_present") and mutant.get("case_failed")):
                defects.append(f"{clause_id}: killed without its declared case failing")
            if clause.get("declared_case") not in (mutant.get("failed_cases") or []):
                defects.append(f"{clause_id}: killed but its declared case is not in "
                               f"failed_cases")
        if (mutant.get("cases") is not None and pristine.get("cases") is not None
                and mutant.get("cases") != pristine.get("cases")):
            defects.append(f"{clause_id}: mutant summary cases {mutant.get('cases')} != "
                           f"pristine {pristine.get('cases')}")
    if pristine.get("cases") != len(pristine.get("case_names") or []):
        defects.append("pristine.cases does not re-derive from the case list")
    if pristine.get("failures") != len(pristine.get("failed_cases") or []):
        defects.append("pristine.failures does not re-derive from the failed list")
    if not set(pristine.get("failed_cases") or []) <= set(pristine.get("case_names") or []):
        defects.append("pristine.failed_cases names a case absent from the case list")
    expected = pin.get("expected")
    actual = pin.get("actual")
    if pin.get("matched") != bool(isinstance(expected, str) and expected == actual):
        defects.append("target_pin.matched does not re-derive")
    if receipt.get("exit") != verdict_exit(len(clauses), len(rows_detail), bound,
                                            len(survivor_ids),
                                            pristine.get("failures") or 0):
        defects.append("exit does not re-derive")
    expected_ok = bool(receipt.get("exit") == 0 and pin.get("matched")
                       and not receipt.get("guard_defects"))
    if bool(receipt.get("ok")) != expected_ok:
        defects.append("ok does not re-derive from exit, target_pin and guard_defects")
    if bool(pristine.get("ok")) != bool(pristine.get("failures") == 0
                                        and pristine.get("cases") is not None):
        defects.append("pristine.ok does not re-derive from its own counts")
    table = receipt.get("table") or {}
    if table.get("block_present") is False and rows_detail:
        defects.append("rows are reported with no table block present")
    if table.get("ignored_lines") is not None and not isinstance(
            table.get("ignored_lines"), list):
        defects.append("table.ignored_lines is not a list")
    gate_blob = skill_blob = None
    if blobs is not None:
        gate_blob = blobs.get("gate")
        skill_blob = blobs.get("skill")
    elif is_commit(rev):
        gate_blob = git_show(root, rev, GATE)
        skill_blob = git_show(root, rev, SKILL)
        if gate_blob is None or skill_blob is None:
            defects.append(f"target blobs are not re-derivable at {rev}")
    if gate_blob is not None:
        digest = sha256_bytes(gate_blob)
        if pin.get("actual") != digest:
            defects.append("target_pin.actual is not the committed gate blob digest")
        target = receipt.get("target") or {}
        if target.get("sha256") != digest:
            defects.append("target.sha256 is not the committed gate blob digest")
        try:
            fresh = enumerate_clauses(gate_blob.decode("utf-8"))
        except (Unevaluable, SyntaxError, UnicodeDecodeError) as exc:
            defects.append(f"re-derive: the gate blob does not yield clauses: {exc}")
            fresh = None
        if fresh is not None:
            if len(fresh) != len(clauses):
                defects.append("guards does not re-derive from the committed gate blob")
            for old, new in zip(clauses, fresh):
                if (old.get("clause_id") != new["clause_id"]
                        or old.get("line") != new["line"]
                        or old.get("message") != new["message"]):
                    defects.append(f"{old.get('clause_id')}: clause does not re-derive from "
                                   f"the committed gate blob")
        if skill_blob is not None:
            block = parse_skill(skill_blob.decode("utf-8"))
            if len(block["rows"]) != len(rows_detail):
                defects.append("rows do not re-derive from the committed SKILL block")
            else:
                for old, new in zip(rows_detail, block["rows"]):
                    if (old.get("id") != new["id"] or old.get("prefix") != new["prefix"]
                            or old.get("case") != new["case"]):
                        defects.append(f"{old.get('id')}: row does not re-derive from the "
                                       f"committed SKILL block")
            if fresh is not None:
                try:
                    source = selftest_source(gate_blob.decode("utf-8"))
                    rebind = bind_rows(fresh, block["rows"], source)
                except (Unevaluable, SyntaxError, UnicodeDecodeError):
                    rebind = None
                if rebind is not None and len(rebind["bound_ids"]) != bound:
                    defects.append("bound does not re-derive from the committed blobs")
        if recheck_pristine:
            created = tempfile.mkdtemp(prefix="guard-battery-validate-")
            try:
                fresh_pristine = run_pristine(gate_blob, created)
            finally:
                shutil.rmtree(created, ignore_errors=True)
            if (fresh_pristine["cases"] != pristine.get("cases")
                    or fresh_pristine["failures"] != pristine.get("failures")
                    or sorted(fresh_pristine["failed_cases"])
                    != sorted(pristine.get("failed_cases") or [])):
                defects.append("pristine does not re-derive from the gate blob's own "
                               "--selftest")
    return {"defects": defects, "guards": len(clauses), "rows": len(rows_detail),
            "bound": bound, "killed": killed, "survivors": len(survivor_ids),
            "exit": receipt.get("exit")}


# --------------------------------------------------------------- selftest ---

SYNTHETIC_GATE = '''\
def validate_receipt(receipt):
    defects = []
    if receipt.get("bad"):
        defects.append("synthetic bad flag")
    return {"defects": defects}


def selftest():
    cases = []

    def case(name, got, want):
        cases.append(name)

    case("red-synthetic-bad", True, True)
    print(f"SELFTEST cases={len(cases)} failures=0")
'''

SYNTHETIC_SKILL = f"""\
# synthetic

{BLOCK_BEGIN}
| G01-synthetic-bad | the receipt carries the synthetic bad flag | `synthetic bad flag` | `red-synthetic-bad` |
{BLOCK_END}
"""


def synthetic_receipt():
    """A consistent receipt over the synthetic blobs, for the validator's own cases."""
    blobs = {"gate": SYNTHETIC_GATE.encode(), "skill": SYNTHETIC_SKILL.encode()}
    clauses = enumerate_clauses(SYNTHETIC_GATE)
    block = parse_skill(SYNTHETIC_SKILL)
    binding = bind_rows(clauses, block["rows"], selftest_source(SYNTHETIC_GATE))
    for clause in clauses:
        clause["mutant"] = {"applied": True, "apply_note": "applied", "compiled": True,
                            "exit": 1, "cases": 1, "failures": 1,
                            "failed_cases": ["red-synthetic-bad"],
                            "case_present": True, "case_failed": True,
                            "status": "killed", "reason": None}
        clause["killed"] = True
    pristine = {"exit": 0, "cases": 1, "failures": 0,
                "case_names": ["red-synthetic-bad"], "failed_cases": [], "ok": True}
    digest = sha256_bytes(blobs["gate"])
    pin = {"expected": digest, "actual": digest, "matched": True}
    receipt = build_receipt(clauses, block, binding, pristine, pin, "a" * 40,
                            blobs["gate"])
    return receipt, blobs


def selftest() -> int:
    cases: list[dict] = []

    def case(name, got, want):
        cases.append({"case": name, "got": got, "want": want, "pass": got == want})

    # clause enumeration and message extraction
    one = enumerate_clauses(SYNTHETIC_GATE)
    case("green-clause-message",
         (len(one), one[0]["clause_id"], one[0]["message"], one[0]["prefix"]),
         (1, "G01", "synthetic bad flag", "synthetic bad flag"))
    nested = ('def validate_receipt(r):\n'
              '    defects = []\n'
              '    if r:\n'
              '        for x in r:\n'
              '            defects.append(f"{x}: second")\n'
              '    if not r:\n'
              '        defects.append("first")\n'
              '    return defects\n'
              'def selftest():\n'
              '    case("red-x", 1, 1)\n')
    ordered = enumerate_clauses(nested)
    case("green-source-order", [(c["clause_id"], c["line"], c["message"], c["prefix"])
                                for c in ordered],
         [("G01", 5, ": second", ": second"), ("G02", 7, "first", "first")])
    case("red-empty-clause-set", _empty_clause_code(), 2)
    case("green-hole-elided", ordered[0]["message"], ": second")

    # table parsing
    block = parse_skill(SYNTHETIC_SKILL)
    case("green-table-parse", (block["block_present"], len(block["rows"]),
                               block["defects"], block["rows"][0]["prefix"],
                               block["rows"][0]["case"]),
         (True, 1, [], "synthetic bad flag", "red-synthetic-bad"))
    good_row = ("| G01-a | trigger prose | `first` | `red-x` |")
    bad_row = ("| G01-a | trigger prose | `first` |")
    parsed_bad = parse_skill(f"{BLOCK_BEGIN}\n{bad_row}\n{BLOCK_END}\n")
    case("red-malformed-row", (len(parsed_bad["rows"]), len(parsed_bad["defects"])), (0, 1))
    tucked = parse_skill(f"{BLOCK_BEGIN}\n| clause | trigger | `prefix` | `case` |\n"
                         f"| --- | --- | --- | --- |\n{good_row}\n{BLOCK_END}\n")
    case("green-header-tolerated",
         (len(tucked["rows"]), tucked["defects"], len(tucked["ignored"])), (1, [], 1))
    typo = parse_skill(f"{BLOCK_BEGIN}\n| G1-a | t | `first` | `red-x` |\n{BLOCK_END}\n")
    case("red-typo-row-id", len(typo["defects"]), 1)
    case("green-separator-skipped",
         parse_skill(f"{BLOCK_BEGIN}\n| --- | --- | --- | --- |\n{good_row}\n"
                     f"{BLOCK_END}\n")["defects"], [])
    case("red-empty-block", (parse_skill("no block here\n")["block_present"],
                             parse_skill("no block here\n")["rows"]), (False, []))
    escaped = parse_skill(f"{BLOCK_BEGIN}\n| G01-a | a \\| b | `first` | `red-x` |\n"
                          f"{BLOCK_END}\n")
    case("green-escaped-pipe", (len(escaped["rows"]), escaped["defects"],
                                escaped["rows"][0]["trigger"] if escaped["rows"] else None),
         (1, [], "a | b"))

    # binding
    binding_source = ('def validate_receipt(r):\n'
                      '    defects = []\n'
                      '    defects.append("alpha")\n'
                      '    defects.append("beta")\n'
                      '    return defects\n'
                      'def selftest():\n'
                      '    case("red-alpha", 1, 1)\n'
                      '    case("red-beta", 1, 1)\n')
    clauses = enumerate_clauses(binding_source)
    source = selftest_source(binding_source)
    good_rows = [{"id": "G01-alpha", "clause_id": "G01", "slug": "alpha",
                  "trigger": "t", "prefix": "alpha", "case": "red-alpha",
                  "block_line": 1},
                 {"id": "G02-beta", "clause_id": "G02", "slug": "beta",
                  "trigger": "t", "prefix": "beta", "case": "red-beta",
                  "block_line": 2}]
    bound = bind_rows([dict(c) for c in clauses], [dict(r) for r in good_rows], source)
    case("green-bound", (bound["bound_ids"], bound["defects"]),
         (["G01", "G02"], []))
    unbound = bind_rows([dict(c) for c in clauses], [dict(good_rows[0])], source)
    case("red-unbound-clause", (unbound["bound_ids"], unbound["defects"]),
         (["G01"], []))
    orphan = bind_rows([dict(c) for c in clauses],
                       [dict(good_rows[0]), dict(good_rows[1], id="G07-gamma",
                                                 clause_id="G07", prefix="gamma",
                                                 case="red-beta")], source)
    case("red-orphan-row", any("orphan row G07-gamma" in d for d in orphan["defects"]), True)
    duplicated = bind_rows([dict(c) for c in clauses],
                           [dict(good_rows[0]), dict(good_rows[0])], source)
    case("red-duplicate-clause-id",
         (duplicated["bound_ids"], any("duplicate clause id G01" in d
                                       for d in duplicated["defects"])), ([], True))
    ambiguous = bind_rows(
        [{"clause_id": "G01", "message": "instrument sha256 is not a digest",
          "bound": False, "killed": False},
         {"clause_id": "G02", "message": "instrument sha256 is not this file's digest",
          "bound": False, "killed": False}],
        [{"id": "G01-x", "clause_id": "G01", "slug": "x", "trigger": "t",
          "prefix": "instrument sha256 is not", "case": "red-alpha", "block_line": 1}],
        'case("red-alpha", 1, 1)\n')
    case("red-ambiguous-prefix",
         (ambiguous["bound_ids"], any("matches 2 clauses" in d
                                      for d in ambiguous["defects"])), ([], True))
    absent_case = bind_rows([dict(c) for c in clauses],
                            [dict(good_rows[0], case="red-ghost")], "def selftest(): pass\n")
    case("red-case-absent-from-source",
         (absent_case["bound_ids"],
          any("absent from the gate's selftest source" in d
              for d in absent_case["defects"])), ([], True))
    same_case = bind_rows([dict(c) for c in clauses],
                          [dict(good_rows[0]),
                           dict(good_rows[1], case="red-alpha")], source)
    case("red-case-declared-twice",
         (same_case["bound_ids"], any("declared by 2 rows" in d
                                      for d in same_case["defects"])), ([], True))

    # mutation and the mutant verdict
    mutant_text = ("def validate_receipt(r):\n"
                   "    defects = []\n"
                   "    defects.append(\"alpha\")\n"
                   "    return defects\n")
    mutated, note = mutate(mutant_text, enumerate_clauses(mutant_text)[0])
    case("green-mutate", (note, "pass" in (mutated or ""),
                         "defects.append" not in (mutated or "")),
         ("applied", True, True))
    duplicated_text = mutant_text + '    defects.append("alpha")\n'
    case("red-mutate-nonunique", mutate(duplicated_text,
                                       enumerate_clauses(duplicated_text)[0])[0], None)
    case("red-compile", compile_check("def f(:\n", "x")[0], False)
    parsed = parse_selftest('{"case": "a", "got": 1, "want": 1, "pass": true}\n'
                            '{"case": "b", "got": 1, "want": 2, "pass": false}\n'
                            "SELFTEST cases=2 failures=1\n")
    case("green-parse-summary", (parsed[1], parsed[2], sorted(parsed[0])),
         (2, 1, ["a", "b"]))
    killed = judge_mutant("red-alpha", True, 1, ({"red-alpha": False}, 1, 1))
    case("green-killed", (killed["status"], killed["killed"] if "killed" in killed
                          else killed["status"] == "killed"), ("killed", True))
    passing = judge_mutant("red-alpha", True, 0, ({"red-alpha": True}, 1, 0))
    case("red-case-passes-on-mutant", passing["status"], "survived")
    absent = judge_mutant("red-alpha", True, 0, ({"other": False}, 1, 1))
    case("red-case-absent-in-mutant", (absent["status"], absent["case_present"]),
         ("survived", False))
    uncompiled = judge_mutant("red-alpha", False, None, ({}, None, None))
    case("red-noncompiling-mutant", (uncompiled["status"],
                                     uncompiled["reason"]), ("inconclusive",
                                                             "mutant copy does not compile"))
    summaryless = judge_mutant("red-alpha", True, 0,
                               ({"red-alpha": False}, None, None))
    case("red-summaryless-mutant", (summaryless["status"], summaryless["reason"]),
         ("inconclusive", "mutant copy printed no SELFTEST summary"))

    # the verdict and the validator
    case("red-empty-set-verdict", (verdict_exit(0, 0, 0, 0, 0),
                                   verdict_exit(0, 0, 0, 0, 0) != 0), (1, True))
    receipt, blobs = synthetic_receipt()
    validated = validate_receipt(receipt, blobs=blobs, recheck_pristine=False)
    case("green-validate-consistent", validated["defects"], [])
    forged = json.loads(json.dumps(receipt))
    forged["clauses"][0]["mutant"]["case_failed"] = False
    case("red-validate-killed-without-case",
         any("killed without its declared case failing" in d
             for d in validate_receipt(forged, blobs=blobs,
                                       recheck_pristine=False)["defects"]), True)
    forged_cases = json.loads(json.dumps(receipt))
    forged_cases["pristine"]["cases"] = 99
    case("red-validate-pristine-cases",
         any("pristine.cases does not re-derive" in d
             for d in validate_receipt(forged_cases, blobs=blobs,
                                       recheck_pristine=False)["defects"]), True)
    forged_bound = json.loads(json.dumps(receipt))
    forged_bound["bound"] = 0
    case("red-validate-bound",
         any("bound does not re-derive" in d
             for d in validate_receipt(forged_bound, blobs=blobs,
                                       recheck_pristine=False)["defects"]), True)
    polluted = json.loads(json.dumps(receipt))
    polluted["pristine"]["failed_cases"] = ["red-synthetic-bad"]
    polluted["pristine"]["failures"] = 1
    polluted["exit"] = verdict_exit(1, 1, 1, 0, 1)
    polluted["ok"] = False
    case("red-non-isolating-case",
         any("not isolating" in d for d in
             validate_receipt(polluted, blobs=blobs,
                              recheck_pristine=False)["defects"]), True)
    failures = [entry for entry in cases if not entry["pass"]]
    for entry in cases:
        print(json.dumps(entry, sort_keys=True))
    print(f"SELFTEST cases={len(cases)} failures={len(failures)}")
    return 0 if not failures else 1


def _empty_clause_code() -> int:
    """Exit code the battery returns for a gate whose validate_receipt has no clause."""
    try:
        enumerate_clauses("def validate_receipt(r):\n    return {}\n")
    except Unevaluable:
        return 2
    return 0


# ------------------------------------------------------------------- main ---

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".")
    parser.add_argument("--rev")
    parser.add_argument("--work")
    parser.add_argument("--json-out")
    parser.add_argument("--expect-sha256")
    parser.add_argument("--expect-guards", type=int)
    parser.add_argument("--battery", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--validate")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    root = os.path.abspath(args.root)
    if args.validate:
        try:
            receipt = json.loads(pathlib.Path(args.validate).read_text())
        except (OSError, json.JSONDecodeError) as exc:
            print(json.dumps({"defects": [f"receipt unreadable: {exc}"], "exit": 2}))
            return 2
        result = validate_receipt(receipt, root=root)
        print(json.dumps(result, sort_keys=True))
        return 0 if not result["defects"] else 1
    if not args.battery and not args.rev:
        print("usage: --battery --rev <rev> [--work <dir>] [--json-out <path>] | "
              "--selftest | --validate <receipt>", file=sys.stderr)
        return 2
    if not args.rev:
        print("--rev is required for --battery", file=sys.stderr)
        return 2
    created = None
    work = args.work
    if not work:
        created = tempfile.mkdtemp(prefix="guard-battery-work-")
        work = created
    try:
        receipt = battery(root, args.rev, work, args.expect_sha256, args.expect_guards)
    except Unevaluable as exc:
        print(json.dumps({"ok": False, "unevaluable": str(exc), "exit": 2}))
        return 2
    finally:
        if created:
            shutil.rmtree(created, ignore_errors=True)
    text = json.dumps(receipt, indent=1, sort_keys=True) + "\n"
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as handle:
            handle.write(text)
    print(json.dumps({"guards": receipt["guards"], "rows": receipt["rows"],
                      "bound": receipt["bound"], "killed": receipt["killed"],
                      "survivors": receipt["survivors"],
                      "survivor_ids": receipt["survivor_ids"],
                      "pristine_cases": receipt["pristine"]["cases"],
                      "pristine_failures": receipt["pristine"]["failures"],
                      "target_pin_matched": receipt["target_pin"]["matched"],
                      "guard_defects": receipt["guard_defects"],
                      "ok": receipt["ok"], "exit": receipt["exit"]}, sort_keys=True))
    return receipt["exit"]


if __name__ == "__main__":
    sys.exit(main())
