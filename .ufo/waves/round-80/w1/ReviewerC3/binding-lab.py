#!/usr/bin/env python3
"""ReviewerC3 binding lab for R80-C3.

Scores a candidate gate against the frozen table-block contract and the
nine-clause deletion proof, and builds the four binding attacks.

Independent of ExecGate's mutants.py: clauses come from ast, the mutation is a
textual statement replacement, and every run is `python3 -I -B <copy> --selftest`
under a four-key child env.

Usage:
  binding-lab.py score  --gate PATH [--block PATH] --work DIR --json-out OUT
  binding-lab.py attacks --gate PATH --work DIR --json-out OUT
"""
import argparse
import ast
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

BEGIN = "<!-- round-80 receipt-guard table: begin -->"
END = "<!-- round-80 receipt-guard table: end -->"
CASE_ROW = re.compile(r"^\|\s*(G\d\d-[a-z0-9][a-z0-9-]*)\s*\|(.*)\|(.*)\|(.*)\|\s*$")
FROZEN = [
    ("G01", "duplicate fixture id"),
    ("G02", "fixture ids"),
    ("G03", ": fixture dir mismatch"),
    ("G04", ": base.accepted is not a bool"),
    ("G05", ": refused without a reason"),
    ("G06", ": refused by "),
    ("G07", "base_accepted does not re-derive"),
    ("G08", "refused does not re-derive"),
    ("G09", "instrument sha256 is not"),
]


# ------------------------------------------------------------- clauses ---

def clause_nodes(tree):
    fn = next((n for n in ast.walk(tree)
               if isinstance(n, ast.FunctionDef) and n.name == "validate_receipt"),
              None)
    if fn is None:
        raise SystemExit("no validate_receipt")
    out = []
    for node in ast.walk(fn):
        if not isinstance(node, ast.Expr) or not isinstance(node.value, ast.Call):
            continue
        call = node.value
        fnc = call.func
        if (isinstance(fnc, ast.Attribute) and fnc.attr == "append"
                and isinstance(fnc.value, ast.Name) and fnc.value.id == "defects"):
            out.append(node)
    return sorted(out, key=lambda n: (n.lineno, n.col_offset))


def template_of(node):
    arg = node.value.args[0]
    if isinstance(arg, ast.JoinedStr):
        parts = []
        for v in arg.values:
            if isinstance(v, ast.Constant):
                parts.append(str(v.value))
            else:
                parts.append("{" + ast.unparse(v.value) + "}")
        return "".join(parts)
    if isinstance(arg, ast.Constant):
        return str(arg.value)
    return ast.unparse(arg)


def suffix_of(template):
    """The text a frozen `: ` prefix can start with.

    Clauses 3-6 begin with the fixture-id placeholder; the frozen prefixes for
    them begin at the `: `.  Everything else has no leading placeholder.
    """
    if template.startswith("{"):
        close = template.find("}")
        if close != -1:
            return template[close + 1:]
    return template


def enumerate_clauses(src):
    tree = ast.parse(src)
    nodes = clause_nodes(tree)
    clauses = []
    for i, node in enumerate(nodes, start=1):
        tpl = template_of(node)
        clauses.append({"n": i, "line": node.lineno, "end_line": node.end_lineno,
                        "template": tpl, "suffix": suffix_of(tpl),
                        "col": node.col_offset})
    return clauses, nodes


# --------------------------------------------------------------- mutations ---

def mutate(src, node):
    lines = src.splitlines(keepends=True)
    indent = " " * node.col_offset
    return "".join(lines[: node.lineno - 1] + [f"{indent}pass\n"]
                   + lines[node.end_lineno:])


def _abs_offset(src, lineno, col):
    lines = src.splitlines(keepends=True)
    return sum(len(l) for l in lines[: lineno - 1]) + col


def condition_mutant(src, node):
    """Disable the clause's guard but keep its message literal in the file.

    A behavioural case must go red; a case that only asserts the message text
    is present in the source stays green.  This is the discriminator the
    frozen predicate does not run.
    """
    tree = ast.parse(src)
    target = None
    for n in ast.walk(tree):
        if (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                and isinstance(n.value.func, ast.Attribute)
                and n.value.func.attr == "append"
                and isinstance(n.value.func.value, ast.Name)
                and n.value.func.value.id == "defects"
                and n.lineno == node.lineno and n.col_offset == node.col_offset):
            target = n
    if target is None:
        raise SystemExit(f"append at line {node.lineno} lost in reparse")
    best = None
    for n in ast.walk(tree):
        if not isinstance(n, ast.If):
            continue
        if not any(s is target for s in ast.walk(n)):
            continue
        span = (n.end_lineno - n.lineno, n.end_col_offset - n.col_offset)
        if best is None or span < best[0]:
            best = (span, n)
    if best is None:
        raise SystemExit(f"no enclosing if for line {node.lineno}")
    test = best[1].test
    start = _abs_offset(src, test.lineno, test.col_offset)
    end = _abs_offset(src, test.end_lineno, test.end_col_offset)
    return src[:start] + "False" + src[end:]


def child_env(work):
    return {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "HOME": os.environ.get("HOME", str(work)),
            "TMPDIR": str(work), "LANG": "C.UTF-8"}


def run_selftest(path, work, env):
    proc = subprocess.run([sys.executable, "-I", "-B", str(path), "--selftest"],
                          cwd=str(work), env=env, capture_output=True, text=True)
    cases = {}
    summary = None
    for line in proc.stdout.splitlines():
        line = line.strip()
        if line.startswith("SELFTEST "):
            summary = line
        elif line.startswith("{"):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict) and "case" in obj and "pass" in obj:
                cases[obj["case"]] = bool(obj["pass"])
    m = re.search(r"cases=(\d+) failures=(\d+)", summary or "")
    return {"cases": cases, "count": len(cases),
            "failures": int(m.group(2)) if m else None,
            "summary": summary, "exit": proc.returncode,
            "stderr": proc.stderr.splitlines()[-2:] if proc.stderr else []}


# ----------------------------------------------------------------- block ---

def parse_block(text):
    if BEGIN not in text or END not in text:
        return None
    body = text.split(BEGIN, 1)[1].split(END, 1)[0]
    rows, nonconforming = [], []
    for raw in body.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-+:?", c) for c in cells if c):
            continue
        m = CASE_ROW.match(line)
        if m:
            rows.append({"id": m.group(1),
                         "trigger": m.group(2).strip(),
                         "prefix_cell": m.group(3).strip(),
                         "case_cell": m.group(4).strip()})
        else:
            nonconforming.append(line)
    out = []
    for row in rows:
        prefix = re.fullmatch(r"`(.*)`", row["prefix_cell"])
        case = re.fullmatch(r"`([^`]+)`", row["case_cell"])
        out.append({**row,
                    "prefix": prefix.group(1) if prefix else None,
                    "case": case.group(1) if case else None})
    return {"rows": out, "nonconforming": nonconforming}


def bind_rows(rows, clauses, matcher="total"):
    """Map rows to clause indices.

    matcher="total": a row carries every clause whose suffix startswith its
    prefix; a row with != 1 match is an orphan or ambiguous.
    matcher="first": a row binds the first matching clause only (the lax
    reading the frozen text does not forbid explicitly).
    """
    matches, issues = [], []
    for row in rows:
        p = row.get("prefix")
        hit = [c["n"] for c in clauses if p is not None and c["suffix"].startswith(p)]
        if matcher == "first":
            hit = hit[:1]
        matches.append({**row, "clause_matches": hit,
                        "bound": len(hit) == 1, "clause": hit[0] if len(hit) == 1 else None})
        if len(hit) != 1:
            issues.append({"row": row.get("id"), "prefix": p,
                           "matches": hit,
                           "why": "no clause" if not hit else "several clauses"})
    per_clause = {}
    for m in matches:
        for n in m["clause_matches"]:
            per_clause.setdefault(n, []).append(m["id"])
    for n, ids in sorted(per_clause.items()):
        if len(ids) > 1:
            issues.append({"clause": n, "rows": ids, "why": "more than one row"})
    for c in clauses:
        if c["n"] not in per_clause:
            issues.append({"clause": c["n"], "rows": [], "why": "no row"})
    ids = [r.get("id") for r in rows]
    dup_ids = sorted({i for i in ids if ids.count(i) > 1})
    return {"rows": matches, "issues": issues, "per_clause": per_clause,
            "duplicate_row_ids": dup_ids,
            "bound": sum(1 for m in matches if m["bound"]),
            "clauses_with_one_row": sum(1 for n, v in per_clause.items() if len(v) == 1),
            "rows_total": len(rows)}


# ----------------------------------------------------------------- score ---

def score(gate, block_text, work, matcher="total", declare=None):
    src = pathlib.Path(gate).read_text()
    clauses, nodes = enumerate_clauses(src)
    env = child_env(work)
    clauses_ok = len(clauses) == 9 and all(
        clauses[i]["suffix"].startswith(FROZEN[i][1]) for i in range(min(9, len(clauses))))

    pristine_path = work / "candidate-pristine.py"
    pristine_path.write_text(src)
    pristine = run_selftest(pristine_path, work, env)

    mutant_runs = []
    for i, node in enumerate(nodes, start=1):
        path = work / f"candidate-mut-{i:02d}.py"
        text = mutate(src, node)
        try:
            ast.parse(text)
            compiles = True
        except SyntaxError:
            compiles = False
        path.write_text(text)
        run = run_selftest(path, work, env)
        mutant_runs.append({"n": i, "compiles": compiles, "run": run,
                            "sha256": hashlib.sha256(text.encode()).hexdigest()})

    failing_by_mutant = {m["n"]: {c for c, ok in m["run"]["cases"].items() if not ok}
                         for m in mutant_runs}

    block = parse_block(block_text) if block_text else None
    rows = block["rows"] if block else []
    binding = bind_rows(rows, clauses, matcher) if rows else None

    declared = declare or {}
    per_clause = []
    for c in clauses:
        row = None
        if binding:
            row = next((m for m in binding["rows"] if m["clause"] == c["n"]), None)
        case = (row or {}).get("case") or declared.get(str(c["n"])) or declared.get(c["n"])
        exists = case in pristine["cases"] if case else False
        pristine_pass = pristine["cases"].get(case) if case else None
        own = failing_by_mutant.get(c["n"], set())
        killed = case in own if case else False
        others = sorted(n for n, fs in failing_by_mutant.items()
                        if n != c["n"] and case and case in fs)
        per_clause.append({
            "n": c["n"],
            "prefix": FROZEN[c["n"] - 1][1],
            "suffix": c["suffix"],
            "line": c["line"],
            "row": (row or {}).get("id"),
            "declared_case": case,
            "declared_in_block": bool(row),
            "exists": exists,
            "pristine_pass": pristine_pass,
            "killed_by_its_mutant": killed,
            "fails_on_other_mutants": others,
            "isolating_frozen": bool(exists and pristine_pass and killed),
            "isolating_strict": bool(exists and pristine_pass and killed and not others),
        })
    distinct = len({p["declared_case"] for p in per_clause if p["declared_case"]})
    bound = sum(1 for p in per_clause if p["declared_in_block"] and p["isolating_frozen"])
    isolated_without_row = sum(1 for p in per_clause
                               if p["isolating_frozen"] and not p["declared_in_block"])
    return {
        "gate": str(gate),
        "gate_sha256": hashlib.sha256(src.encode()).hexdigest(),
        "guards": len(clauses),
        "clause_prefixes_match_frozen": clauses_ok,
        "clause_lines": [c["line"] for c in clauses],
        "pristine": {"cases": pristine["count"], "failures": pristine["failures"],
                     "exit": pristine["exit"], "summary": pristine["summary"]},
        "mutants": [{"n": m["n"], "compiles": m["compiles"],
                     "cases": m["run"]["count"], "failing": sorted(failing_by_mutant[m["n"]]),
                     "exit": m["run"]["exit"], "sha256": m["sha256"]}
                    for m in mutant_runs],
        "block": {"present": block is not None,
                  "rows_total": len(rows),
                  "nonconforming": (block or {}).get("nonconforming", [])},
        "binding": {k: binding[k] for k in
                    ("bound", "clauses_with_one_row", "rows_total",
                     "duplicate_row_ids", "issues")} if binding else None,
        "rows": len(rows),
        "bound": bound,
        "survivors": len(per_clause) - bound,
        "isolated_without_row": isolated_without_row,
        "distinct_declared_cases": distinct,
        "per_clause": per_clause,
        "matcher": matcher,
        "strict_isolating": sum(1 for p in per_clause if p["isolating_strict"]),
    }


# ---------------------------------------------------------------- attacks ---

MARKER = '    failures = [c for c in cases if not c["pass"]]'


def inject(src, block, work, name):
    if MARKER not in src:
        raise SystemExit(f"marker missing for {name}")
    text = src.replace(MARKER, block + "\n" + MARKER, 1)
    path = work / name
    path.write_text(text)
    return path


BLOCK_ROWS = [
    ("G01-duplicate-fixture-id", "the fixture id appears twice", "duplicate fixture id"),
    ("G02-fixture-id-set", "the fixture id set differs from the declared set", "fixture ids"),
    ("G03-fixture-dir", "a fixture row names another fixture directory", ": fixture dir mismatch"),
    ("G04-base-accepted-bool", "base.accepted is absent or not a bool", ": base.accepted is not a bool"),
    ("G05-refused-no-reason", "a refused fixture carries no reasons", ": refused without a reason"),
    ("G06-refused-other-rule", "a refusal names another rule", ": refused by "),
    ("G07-base-accepted-count", "base_accepted is not re-derived", "base_accepted does not re-derive"),
    ("G08-refused-count", "refused is not re-derived", "refused does not re-derive"),
    ("G09-instrument-digest", "the digest is not the running file's", "instrument sha256 is not"),
]

EXECGATE_CASES = {
    "G01-duplicate-fixture-id": "red-validate-duplicate-fixture-id",
    "G02-fixture-id-set": "red-validate-fixture-id-set",
    "G03-fixture-dir": "red-validate-fixture-dir",
    "G04-base-accepted-bool": "red-validate-base-accepted-bool",
    "G05-refused-no-reason": "red-validate-refused-no-reason",
    "G06-refused-other-rule": "red-validate-refused-other-rule",
    "G07-base-accepted-count": "red-validate-base-accepted-count",
    "G08-refused-count": "red-validate-refused-count",
    "G09-instrument-digest": "red-validate-instrument-digest",
}
SRC_CASES = {rid: f"red-g{i:02d}-src" for i, (rid, _, _) in enumerate(BLOCK_ROWS, 1)}
SRC_CASES["G05-refused-no-reason"] = "red-validate-refused-no-reason"


def render_block(cases_by_id, prefix_override=None):
    lines = [BEGIN]
    for rid, trigger, prefix in BLOCK_ROWS:
        p = (prefix_override or {}).get(rid, prefix)
        lines.append(f"| {rid} | {trigger} | `{p}` | `{cases_by_id[rid]}` |")
    lines.append(END)
    return "\n".join(lines) + "\n"


GOOD_BLOCK = render_block(EXECGATE_CASES)
ATK_B_BLOCK = render_block(SRC_CASES)
ATK_C_BLOCK = render_block({rid: "red-g99-append-count" for rid, _, _ in BLOCK_ROWS})
ATK_A_BLOCK = render_block(EXECGATE_CASES,
                           {"G05-refused-no-reason": ": refused"})


def attacks(base_gate, candidate_gate, work):
    src = pathlib.Path(base_gate).read_text()
    out = {}

    # B: eight source-text cases + the existing behaviour case for clause 5.
    #    Lands pristine.cases 37 with eight vacuous assertions.  Each needle is
    #    split so the case's own source line cannot satisfy it.
    b_cases = []
    for name, frag in [
            ("red-g01-src", ('"duplicate "', '"fixture id"')),
            ("red-g02-src", ('"fixture "', '"ids"')),
            ("red-g03-src", ('": fixture dir "', '"mismatch"')),
            ("red-g04-src", ('": base.accepted is "', '"not a bool"')),
            ("red-g06-src", ('": refused "', '"by "')),
            ("red-g07-src", ('"base_accepted does "', '"not re-derive"')),
            ("red-g08-src", ('"refused does "', '"not re-derive"')),
            ("red-g09-src", ('"instrument sha256 is "', '"not this file\'s digest"'))]:
        b_cases.append(f'    _src = pathlib.Path(__file__).read_text()\n'
                       f'    case("{name}", {frag[0]} + {frag[1]} in _src, True)')
    b = inject(src, "\n".join(b_cases), work, "atk-b-source.py")
    (work / "atk-b-block.md").write_text(ATK_B_BLOCK)
    out["B_source_literal"] = score(b, ATK_B_BLOCK, work, "total")

    # C: one all-mutant-killing case + seven pads = 37; the same case declared
    #    for every row.
    c_block = ("    _lines = pathlib.Path(__file__).read_text().splitlines()\n"
               '    case("red-g99-append-count",\n'
               '         len([ln for ln in _lines if ("defects." + "append") in ln]), 17)\n'
               + "\n".join(f'    case("green-pad-{i}", True, True)' for i in range(1, 8)))
    c = inject(src, c_block, work, "atk-c-universal.py")
    out["C_universal_case"] = score(c, ATK_C_BLOCK, work, "total")

    # A: a row whose prefix matches two clauses.
    a = score(candidate_gate, ATK_A_BLOCK, work, "total")
    out["A_two_clause_prefix_total"] = a
    a_first = score(candidate_gate, ATK_A_BLOCK, work, "first")
    out["A_two_clause_prefix_first"] = {
        k: a_first[k] for k in ("rows", "bound", "survivors",
                                "distinct_declared_cases", "binding",
                                "per_clause")}

    # D: two clauses merged into one defects.append.
    src_lines = src.splitlines(keepends=True)
    merged = src_lines[:790] + [
        '        if (not isinstance((fixture.get("base") or {}).get("accepted"), bool)\n'
        '                or (fixture.get("refused") and not fixture.get("reasons"))):\n'
        '            defects.append(f"{fixture.get(\'id\')}: base.accepted is not a bool")\n'
    ] + src_lines[794:]
    d_path = work / "atk-d-merged.py"
    d_path.write_text("".join(merged))
    try:
        ast.parse("".join(merged))
        compiles = True
    except SyntaxError:
        compiles = False
    d_clauses, _ = enumerate_clauses("".join(merged)) if compiles else ([], [])
    d_run = run_selftest(d_path, work, child_env(work))
    out["D_merged_clause"] = {
        "compiles": compiles,
        "guards": len(d_clauses),
        "clause_lines": [c["line"] for c in d_clauses],
        "pristine_cases": d_run["count"],
        "pristine_failures": d_run["failures"],
        "guards_target_9_met": len(d_clauses) == 9,
    }
    return out


# ------------------------------------------------------------------- main ---

def discriminate(gate, block_text, work):
    """Run the condition-disabled mutant for every clause and report which
    declared cases still pass (i.e. never observed the clause's behaviour)."""
    src = pathlib.Path(gate).read_text()
    clauses, nodes = enumerate_clauses(src)
    env = child_env(work)
    pristine_path = work / "disc-pristine.py"
    pristine_path.write_text(src)
    pristine = run_selftest(pristine_path, work, env)
    block = parse_block(block_text) if block_text else None
    rows = bind_rows(block["rows"], clauses, "total")["rows"] if block else []
    out = []
    for c, node in zip(clauses, nodes):
        path = work / f"disc-cond-{c['n']:02d}.py"
        text = condition_mutant(src, node)
        try:
            ast.parse(text)
            compiles = True
        except SyntaxError:
            compiles = False
        path.write_text(text)
        run = run_selftest(path, work, env)
        failing = {name for name, ok in run["cases"].items() if not ok}
        row = next((r for r in rows if r.get("clause") == c["n"]), None)
        case = (row or {}).get("case")
        out.append({
            "n": c["n"],
            "prefix": FROZEN[c["n"] - 1][1],
            "declared_case": case,
            "compiles": compiles,
            "pristine_cases": run["count"],
            "failing": sorted(failing),
            "case_present": case in run["cases"] if case else None,
            "case_observed_behaviour": (case in failing) if case else None,
            "case_still_green_on_condition_mutant":
                (case in run["cases"] and run["cases"][case]) if case else None,
        })
    return {"gate": str(gate),
            "pristine": {"cases": pristine["count"],
                         "failures": pristine["failures"]},
            "clauses": out,
            "behavioural": sum(1 for c in out if c["case_observed_behaviour"]),
            "source_text_only": sum(1 for c in out
                                    if c["case_observed_behaviour"] is False
                                    and c["case_present"])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("score", "attacks", "discriminate"))
    ap.add_argument("--gate", required=True)
    ap.add_argument("--candidate-gate")
    ap.add_argument("--block")
    ap.add_argument("--declare")
    ap.add_argument("--work", required=True)
    ap.add_argument("--json-out")
    args = ap.parse_args()
    work = pathlib.Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)

    if args.mode == "score":
        block_text = pathlib.Path(args.block).read_text() if args.block else None
        declare = json.loads(pathlib.Path(args.declare).read_text()) if args.declare else None
        receipt = score(args.gate, block_text, work, declare=declare)
    elif args.mode == "discriminate":
        receipt = discriminate(args.gate,
                               pathlib.Path(args.block).read_text() if args.block else None,
                               work)
    else:
        receipt = {"attacks": attacks(args.gate, args.candidate_gate or args.gate,
                                      work)}
    text = json.dumps(receipt, indent=2, sort_keys=True)
    print(text)
    if args.json_out:
        pathlib.Path(args.json_out).write_text(text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
