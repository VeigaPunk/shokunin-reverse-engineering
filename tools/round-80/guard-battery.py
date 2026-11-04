#!/usr/bin/env python3
"""guard-battery.py - round-80 instrument (R80-C3 depth).

Binds each `defects.append(...)` refusal clause of
`tools/round-78/attack-gate.py`'s `validate_receipt()` to exactly one row of the
round-80 decision-table block in `SKILL.md` and exactly one declared selftest
case, then proves the case fails when the clause is deleted from a copy of the
instrument.  Round 79's mutation-tester found three of these clauses surviving
deletion with every selftest case green (gm-f, gm-g, gm-h) and named the class:
a clause exercised but not pinned is not covered.

Rule
  * A clause exists for every `defects.append(...)` statement inside
    `validate_receipt()` at `--rev`, in source order (G01..G09 at the base).
  * A table row declares a clause id, a message FRAGMENT and a case name.  The
    fragment must occur in the clause's message literal and must identify it
    uniquely: no two clauses may contain it, and no fragment may sit on another
    clause.  (The frozen word is "prefix"; three literals begin with an
    interpolation, so the implemented test is membership plus uniqueness - the
    frozen nine strings are unchanged and the test is strictly narrower than
    prefix matching on the six literals that do start with text.)
  * A declared case must appear in the gate's own `--selftest` source as
    `case("<name>"`.
  * A clause is KILLED only when its declared case is present in the mutated
    copy's output and FAILS there.  An absent declared case is a SURVIVOR.  A
    copy that does not compile or prints no `SELFTEST` summary is inconclusive.
  * `bound` counts clauses with a unique row and an existing declared case.

Modes
  (no mode)         run the battery; requires --rev and --work
  --selftest        the rule's cases
  --validate FILE   re-derive a saved receipt's counts
Exit: 0 guards>0, rows==guards, bound==guards, survivors==[], pristine green;
1 a defect (named); 2 could-not-evaluate.
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
SCHEMA = "kaidoku-r80-guard-battery-v1"
GATE = "tools/round-78/attack-gate.py"
SKILL = "SKILL.md"
BEGIN = "<!-- round-80 receipt-guard table: begin -->"
END = "<!-- round-80 receipt-guard table: end -->"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
CASE_DEF = re.compile(r'case\(\s*"([^"]+)"')

CHILD_ENV_KEYS = ("HOME", "LANG", "PATH", "TMPDIR")


class Unevaluable(Exception):
    """Exit-2 class: the inputs cannot be read."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: str, data) -> None:
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")


def git(root: str, *argv: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", root, *argv], capture_output=True)


def git_blob(root: str, rev: str, path: str) -> bytes | None:
    proc = git(root, "show", f"{rev}:{path}")
    return proc.stdout if proc.returncode == 0 else None


def child_env(tmpdir: str) -> dict:
    env = {"HOME": os.environ.get("HOME", "/tmp"),
           "LANG": os.environ.get("LANG", "C.UTF-8"),
           "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
           "TMPDIR": tmpdir}
    return {key: env[key] for key in CHILD_ENV_KEYS}


def run_selftest(source: bytes, work: str, tag: str) -> dict:
    """Write a copy of the instrument and run its --selftest."""
    path = pathlib.Path(work) / f"{tag}.py"
    path.write_bytes(source)
    proc = subprocess.run(["python3", "-I", "-B", str(path), "--selftest"],
                          capture_output=True, text=True,
                          env=child_env(work))
    cases: dict[str, bool] = {}
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            record = json.loads(line)
        except ValueError:
            continue
        if isinstance(record, dict) and isinstance(record.get("case"), str) \
                and "pass" in record:
            cases[record["case"]] = bool(record["pass"])
    summary = re.search(r"SELFTEST cases=(\d+) failures=(\d+)", proc.stdout)
    return {"exit": proc.returncode,
            "cases": cases,
            "cases_count": int(summary.group(1)) if summary else None,
            "failures": int(summary.group(2)) if summary else None,
            "summary": summary.group(0) if summary else "",
            "stderr_tail": proc.stderr.strip().splitlines()[-1:] or []}


def clause_message(node: ast.AST) -> str:
    """The literal text of one defects.append argument (f-string parts joined)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return "".join(v.value for v in node.values
                       if isinstance(v, ast.Constant) and isinstance(v.value, str))
    return ""


def enumerate_clauses(source: str) -> list[dict]:
    tree = ast.parse(source)
    func = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "validate_receipt":
            func = node
            break
    if func is None:
        raise Unevaluable("validate_receipt() is absent")
    clauses: list[dict] = []
    statements = [node for node in ast.walk(func)
                  if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)]
    statements.sort(key=lambda node: (node.lineno, node.col_offset))
    for stmt in statements:
        call = stmt.value
        func_node = call.func
        if not (isinstance(func_node, ast.Attribute) and func_node.attr == "append"
                and isinstance(func_node.value, ast.Name)
                and func_node.value.id == "defects"):
            continue
        clauses.append({
            "index": len(clauses) + 1,
            "line": stmt.lineno,
            "end_line": stmt.end_lineno,
            "col": stmt.col_offset,
            "end_col": stmt.end_col_offset,
            "message": clause_message(call.args[0]) if call.args else "",
        })
    return clauses


def parse_table(skill_text: str) -> tuple[list[dict], list[str]]:
    rows: list[dict] = []
    defects: list[str] = []
    if BEGIN not in skill_text or END not in skill_text:
        return rows, defects
    block = skill_text.split(BEGIN, 1)[1].split(END, 1)[0]
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        if set(line) <= set("|-: "):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 4:
            defects.append(f"malformed row ({len(cells)} cells): {line[:70]}")
            continue
        clause_id, trigger, fragment, case = cells
        if clause_id.lower() in ("clause", "clause id"):
            continue
        if not re.fullmatch(r"G\d{2}-[a-z0-9-]+", clause_id):
            defects.append(f"clause id is not G<NN>-<slug>: {clause_id}")
            continue
        frag = fragment.strip("`")
        case = case.strip("`")
        if not frag or not case:
            defects.append(f"{clause_id}: fragment or case is empty")
            continue
        rows.append({"clause_id": clause_id, "trigger": trigger,
                     "fragment": frag, "case": case})
    return rows, defects


def bind(clauses: list[dict], rows: list[dict], gate_source: str) -> dict:
    defects: list[str] = []
    ids = [r["clause_id"] for r in rows]
    if len(ids) != len(set(ids)):
        defects.append("duplicate clause id in the table")
    cases = CASE_DEF.findall(gate_source)
    bound = 0
    per_clause: list[dict] = []
    for clause in clauses:
        hits = [r for r in rows if r["fragment"] in clause["message"]]
        entry = {"index": clause["index"], "line": clause["line"],
                 "message": clause["message"],
                 "row": hits[0]["clause_id"] if len(hits) == 1 else "",
                 "case": hits[0]["case"] if len(hits) == 1 else "",
                 "clause_bound": False}
        if not hits:
            defects.append(f"G{clause['index']:02d}: no table row binds this clause")
        elif len(hits) > 1:
            defects.append(f"G{clause['index']:02d}: {len(hits)} rows bind this clause")
        else:
            if hits[0]["case"] not in cases:
                defects.append(f"{hits[0]['clause_id']}: case {hits[0]['case']!r} "
                               f"is absent from the gate's selftest")
            else:
                entry["clause_bound"] = True
                bound += 1
        per_clause.append(entry)
    used = {e["index"] for e in per_clause if e["clause_bound"]}
    for row in rows:
        hits = [c for c in clauses if row["fragment"] in c["message"]]
        if not hits:
            defects.append(f"{row['clause_id']}: fragment matches no clause")
        elif len(hits) > 1:
            defects.append(f"{row['clause_id']}: fragment matches "
                           f"{len(hits)} clauses")
        elif hits[0]["index"] not in used:
            defects.append(f"{row['clause_id']}: clause {hits[0]['index']} is unbound")
    return {"bound": bound, "per_clause": per_clause, "defects": defects,
            "case_names": sorted(set(cases))}


def mutate(source: bytes, clause: dict) -> bytes:
    lines = source.decode().splitlines(keepends=True)
    first = clause["line"] - 1
    last = clause["end_line"] - 1
    head = lines[first][:clause["col"]]
    tail = lines[last][clause["end_col"]:]
    if not tail.endswith("\n"):
        tail += "\n"
    return "".join(lines[:first] + [head + "pass" + tail] + lines[last + 1:]).encode()


def battery(root: str, rev: str, work: str, expect_sha256: str | None) -> dict:
    if not HEX40.match(rev):
        raise Unevaluable(f"--rev {rev!r} is not a 40-hex commit")
    gate = git_blob(root, rev, GATE)
    skill = git_blob(root, rev, SKILL)
    if gate is None:
        raise Unevaluable(f"{GATE} is absent at {rev}")
    if skill is None:
        raise Unevaluable(f"{SKILL} is absent at {rev}")
    clauses = enumerate_clauses(gate.decode())
    rows, table_defects = parse_table(skill.decode())
    bound = bind(clauses, rows, gate.decode())
    run_dir = pathlib.Path(work)
    run_dir.mkdir(parents=True, exist_ok=True)
    pristine = run_selftest(gate, str(run_dir), "pristine")
    killed: list[dict] = []
    survivors: list[dict] = []
    inconclusive: list[dict] = []
    for entry in bound["per_clause"]:
        clause = clauses[entry["index"] - 1]
        if not entry["clause_bound"]:
            survivors.append({"clause": entry["index"], "line": clause["line"],
                              "message": clause["message"], "reason":
                              "no declared case bound to this clause"})
            continue
        mutant = mutate(gate, clause)
        if mutant == gate:
            inconclusive.append({"clause": entry["index"], "reason":
                                 "the mutation changed no byte"})
            continue
        result = run_selftest(mutant, str(run_dir), f"m{entry['index']:02d}")
        declared = entry["case"]
        present = declared in result["cases"]
        failed = result["cases"].get(declared) is False
        record = {"clause": entry["index"], "case": declared,
                  "present": present, "failed": failed,
                  "exit": result["exit"], "summary": result["summary"],
                  "failing": sorted(name for name, ok in result["cases"].items()
                                    if not ok)}
        if result["failures"] is None:
            inconclusive.append({**record, "reason": "no SELFTEST summary"})
        elif present and failed:
            killed.append(record)
        else:
            survivors.append({**record, "reason":
                              "declared case absent" if not present
                              else "declared case stayed green"})
    actual = sha256_bytes(gate)
    receipt = {
        "schema": SCHEMA,
        "round": ROUND,
        "checked_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "instrument": {"path": "tools/round-80/guard-battery.py",
                       "sha256": sha256_bytes(pathlib.Path(__file__).read_bytes())},
        "rev": rev,
        "guards": len(clauses),
        "rows": len(rows),
        "bound": bound["bound"],
        "survivors": survivors,
        "survivors_count": len(survivors),
        "killed": killed,
        "inconclusive": inconclusive,
        "pristine": {"cases": pristine["cases_count"],
                     "failures": pristine["failures"],
                     "exit": pristine["exit"],
                     "summary": pristine["summary"]},
        "table_defects": table_defects,
        "binding_defects": bound["defects"],
        "clauses": clauses,
        "table_rows": rows,
        "per_clause": bound["per_clause"],
        "target_pin": {"path": GATE, "actual": actual,
                       "expected": expect_sha256 or "",
                       "matched": bool(expect_sha256) and expect_sha256 == actual},
    }
    receipt["would_pass"] = bool(
        receipt["guards"] > 0 and receipt["rows"] == receipt["guards"]
        and receipt["bound"] == receipt["guards"] and not survivors
        and not inconclusive and pristine["failures"] == 0
        and not table_defects and not bound["defects"])
    receipt["ok"] = receipt["would_pass"]
    return receipt


def validate_receipt(receipt: dict) -> dict:
    defects: list[str] = []
    clauses = receipt.get("clauses") or []
    if receipt.get("guards") != len(clauses):
        defects.append("guards does not re-derive from the clause list")
    rows = receipt.get("table_rows") or []
    if receipt.get("rows") != len(rows):
        defects.append("rows does not re-derive from the table rows")
    per_clause = receipt.get("per_clause") or []
    if receipt.get("bound") != sum(1 for c in per_clause if c.get("clause_bound")):
        defects.append("bound does not re-derive from per_clause")
    survivors = receipt.get("survivors") or []
    if receipt.get("survivors_count") != len(survivors):
        defects.append("survivors_count does not re-derive from survivors")
    killed = receipt.get("killed") or []
    for entry in killed:
        if not entry.get("present") or not entry.get("failed"):
            defects.append(f"clause {entry.get('clause')}: killed with a case that "
                           f"is absent or green")
    pristine = receipt.get("pristine") or {}
    if pristine.get("cases") is None or pristine.get("failures") is None:
        defects.append("pristine case summary is absent")
    elif receipt.get("ok") and pristine.get("failures") != 0:
        defects.append("ok true with a failing pristine selftest")
    if receipt.get("ok") and survivors:
        defects.append("ok true with survivors")
    if receipt.get("ok") and receipt.get("guards") == 0:
        defects.append("ok true over an empty clause set")
    if receipt.get("ok") and receipt.get("table_defects"):
        defects.append("ok true with table defects")
    for row in rows:
        if not isinstance(row.get("case"), str) or not row["case"]:
            defects.append("a table row declares no case")
    pin = receipt.get("target_pin") or {}
    if pin.get("matched") and not HEX64.match(pin.get("expected") or ""):
        defects.append("target pin matched without a 64-hex expectation")
    if not HEX40.match(receipt.get("rev") or ""):
        defects.append("rev is not a 40-hex commit")
    if not receipt.get("checked_at"):
        defects.append("checked_at is absent")
    inst = receipt.get("instrument") or {}
    if inst.get("sha256") != sha256_bytes(pathlib.Path(__file__).read_bytes()):
        defects.append("instrument sha256 is not this file's digest")
    return {"defects": defects, "guards": len(clauses), "rows": len(rows),
            "survivors": len(survivors)}


def selftest() -> int:
    cases: list[dict] = []

    def case(name, got, want):
        cases.append({"case": name, "got": got, "want": want, "pass": got == want})

    src = (
        "def validate_receipt(receipt):\n"
        "    defects = []\n"
        "    if receipt.get('a'):\n"
        "        defects.append('duplicate fixture id')\n"
        "    if receipt.get('b'):\n"
        "        defects.append(f\"{receipt['id']}: refused by {receipt['rule']}, \"\n"
        "                       \"not its declared rule\")\n"
        "    if receipt.get('c'):\n"
        "        defects.append('refused does not re-derive from the fixture list')\n"
        "    return defects\n")
    clauses = enumerate_clauses(src)
    case("clause-count", len(clauses), 3)
    case("clause-message-fstring",
         clauses[1]["message"],
         ": refused by , not its declared rule")
    case("clause-lines", [c["line"] for c in clauses], [4, 6, 9])

    block = (BEGIN + "\n"
             "| clause | trigger | fragment | case |\n"
             "|---|---|---|---|\n"
             "| G01-duplicate | two ids | `duplicate fixture id` | `red-dup` |\n"
             "| G02-other-rule | wrong rule | `: refused by ` | `red-rule` |\n"
             "| G03-refused-count | miscount | `refused does not re-derive` | `red-cnt` |\n"
             + END + "\n")
    gate_with_cases = src + "\ndef selftest():\n" + "".join(
        f'    case("{n}", 1, 1)\n' for n in ("red-dup", "red-rule", "red-cnt"))
    rows, table_defects = parse_table("text\n" + block)
    case("table-rows", len(rows), 3)
    case("table-clean", table_defects, [])
    bound = bind(clauses, rows, gate_with_cases)
    case("binding-bound", bound["bound"], 3)
    case("binding-clean", bound["defects"], [])

    missing = [r for r in rows if r["case"] != "red-cnt"]
    case("red-absent-case-unbound",
         bind(clauses, missing, gate_with_cases)["bound"], 2)

    two_rows = rows + [{"clause_id": "G04-dup", "trigger": "x",
                        "fragment": "duplicate fixture id", "case": "red-dup"}]
    case("red-duplicate-fragment-defect",
         any("matches 3 clauses" in d or "2 rows bind" in d or "matches 2 clauses" in d
             for d in bind(clauses, two_rows, gate_with_cases)["defects"]), True)

    orphan = rows + [{"clause_id": "G05-orphan", "trigger": "x",
                      "fragment": "no such message", "case": "red-dup"}]
    case("red-orphan-row",
         any("matches no clause" in d for d in bind(clauses, orphan,
                                                    gate_with_cases)["defects"]), True)

    short = [r for r in rows if r["fragment"] != "refused does not re-derive"]
    case("red-unbound-clause-named",
         any("no table row binds" in d for d in bind(clauses, short,
                                                     gate_with_cases)["defects"]), True)

    malformed, malformed_defects = parse_table(
        "x\n" + BEGIN + "\n| G01-x | t | `frag` |\n" + END + "\n")
    case("red-malformed-row-named", bool(malformed_defects), True)
    case("red-malformed-row-not-bound", malformed, [])

    mangled = gate_with_cases.replace("defects.append('duplicate fixture id')",
                                      "defects.append('dup fixture id')")
    case("red-fragment-not-in-message",
         [e["clause_bound"] for e in
          bind(enumerate_clauses(mangled), rows, mangled)["per_clause"]],
         [False, True, True])

    mutant = mutate(src.encode(), clauses[0])
    case("mutation-is-one-statement",
         b"pass" in mutant and mutant != src.encode()
         and mutant.count(b"defects.append") == 2, True)

    # validate: consistent receipt clean, tampered counts named
    receipt = {"clauses": clauses, "guards": 3,
               "table_rows": rows, "rows": 3,
               "per_clause": [{"clause_bound": True}] * 3, "bound": 3,
               "survivors": [], "survivors_count": 0,
               "killed": [{"clause": 1, "present": True, "failed": True}],
               "pristine": {"cases": 30, "failures": 0},
               "table_defects": [], "target_pin": {},
               "rev": "a" * 40, "checked_at": "2026-11-04T00:00:00-03:00",
               "ok": True, "instrument": {
                   "sha256": sha256_bytes(pathlib.Path(__file__).read_bytes())}}
    case("green-validate-consistent", validate_receipt(receipt)["defects"], [])
    tampered = json.loads(json.dumps(receipt))
    tampered["survivors"] = [{"clause": 2}]
    case("red-validate-tampered-survivors",
         validate_receipt(tampered)["defects"][:1],
         ["survivors_count does not re-derive from survivors"])
    fake_kill = json.loads(json.dumps(receipt))
    fake_kill["killed"] = [{"clause": 1, "present": True, "failed": False}]
    case("red-validate-fake-kill",
         validate_receipt(fake_kill)["defects"][:1],
         ["clause 1: killed with a case that is absent or green"])
    empty = json.loads(json.dumps(receipt))
    empty.update({"clauses": [], "guards": 0, "table_rows": [], "rows": 0,
                  "per_clause": [], "bound": 0})
    case("red-validate-empty-set",
         validate_receipt(empty)["defects"][:1],
         ["ok true over an empty clause set"])

    failures = [c for c in cases if not c["pass"]]
    for case_ in cases:
        print(json.dumps(case_, sort_keys=True))
    print(f"SELFTEST cases={len(cases)} failures={len(failures)}")
    return 0 if not failures else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--work")
    ap.add_argument("--expect-sha256")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--validate")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.validate:
        data = json.loads(pathlib.Path(args.validate).read_text())
        result = validate_receipt(data)
        print(json.dumps(result, sort_keys=True))
        return 0 if not result["defects"] else 1
    if not args.rev:
        ap.error("--rev is required")
    work = args.work
    temp = None
    if not work:
        temp = tempfile.mkdtemp(prefix="guard-battery-")
        work = temp
    try:
        receipt = battery(args.root, args.rev, work, args.expect_sha256)
    except Unevaluable as exc:
        print(json.dumps({"unevaluable": str(exc), "exit": 2}))
        return 2
    finally:
        if temp:
            shutil.rmtree(temp, ignore_errors=True)
    check = validate_receipt(receipt)
    receipt["validate"] = check
    if check["defects"]:
        receipt["ok"] = False
    if args.json_out:
        write_json(args.json_out, receipt)
    print(json.dumps({k: receipt[k] for k in
                      ("guards", "rows", "bound", "survivors_count", "ok")},
                     sort_keys=True))
    print(json.dumps({"survivors": [s.get("clause") for s in receipt["survivors"]],
                      "pristine": receipt["pristine"],
                      "validate_defects": check["defects"]}, sort_keys=True))
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
