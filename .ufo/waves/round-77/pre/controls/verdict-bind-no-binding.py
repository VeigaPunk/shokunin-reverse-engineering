#!/usr/bin/env python3
"""verdict-bind.py - round-77 instrument (R77-C1 calibration).

Round 76's D24 atom admits a row whose evidence cell carries a FALSE verdict
beside a resolving path: the row `capability-row binding` said
`(... c1-at-landing.json (D24 true, mismatch_count 0))` while that receipt
records `exit 1`, `mismatch_count 1` and `D24_capability_rows false` (round-76
non-author spot-check, routed defect 5).  D24 checks that the path resolves and
never reads the verdict written next to it.

This instrument binds a claimed verdict to the receipt it names.  It reads the
record surface (frozen scope: SCORECARD `## Capabilities` rows whose
first-working-round numeral is >= 73, plus the PROVINCE `- **Core — ` bullets)
and parses every parenthesised annotation with a closed, declared grammar:

  P1  <field> <true|false|integer>     typed equality with a top-level receipt
                                       field, or an atom's `ok` when <field> is
                                       an atom id present in `atoms`
  P2  <field> <N> of <M>              receipt[field] == N and
                                       receipt[field + "_total"] == M
  P3  <N> mismatches                  receipt["mismatch_count"] == N
  P4  <N> survivors                   receipt["survivor_count"] == N
  P5  <N|word> atoms                  len(receipt["atoms"]) == N
  P6  pristine <N>[ cases]            receipt["pristine"]["cases"] == N
  P7  validate defect-free            receipt["validate"]["defects"] == []

A leading `<word>:` qualifier is stripped and retained.  A clause the grammar
cannot parse is recorded as unbound - the instrument never guesses, and a
prose annotation (no parsed clause) makes no claim.  A field the receipt does
not carry is unbound too, never a guessed pass.

A bound clause is re-derived at the measured revision from the receipt JSON the
cell names (the path immediately preceding the group, else the first path in
the cell).  Defects: `absent_receipt`, `no_json_receipt` (bound clauses but no
JSON pointer), `value_mismatch` (claimed vs actual, both printed), `no_atoms`,
`no_pristine`, `no_validate`, `bad_literal`.

Exit: 0 no defect; 1 defects named; 2 could-not-evaluate.  `--validate <file>`
re-checks a written receipt's internal honesty.  `--selftest` scores the
grammar cases (red and the legitimate look-alikes) before any record is read.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

SCORECARD = "SCORECARD.md"
PROVINCE = "PROVINCE.md"
CAPABILITIES_HEADING = "## Capabilities"
SCOPE_MIN_ROUND = 73
PREDICATE = (
    "R77-C1 is verified iff `python3 -I -B tools/round-77/verdict-bind.py --root . --rev <measured> --json-out <receipt>` exits 0 with `mismatch_count 0`, `population.bound_clauses >= 18`, `population.in_scope_rows >= 11` and a defect-free `validate`, every bound clause re-derived from the JSON receipt its cell names, while the same command at base 188562d4 exits 1 with `mismatch_count 4` naming exactly the `capability-row binding` row and PROVINCE.md line 585 (`D24 true` vs `false`, `mismatch_count 0` vs `1`), and the selftest's 15 cases carry one red fixture per failure shape plus their legitimate look-alikes."
)
PROVINCE_BULLET = "- **Core — "

NUM_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
             "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
             "twelve": 12}

GROUP_RE = re.compile(r"\(([^()]{2,220})\)")
JSON_PATH_RE = re.compile(r"(?<![A-Za-z0-9_./-])([A-Za-z0-9_./-]+\.json|"
                          r"\.ufo/[A-Za-z0-9_./-]+|[A-Za-z0-9_./-]+/"
                          r"[A-Za-z0-9_./-]+)")
JSON_ONLY_RE = re.compile(r"(?<![A-Za-z0-9_./-])(\.ufo/[A-Za-z0-9_./-]+\.json|"
                          r"[A-Za-z0-9_./-]+/[A-Za-z0-9_./-]+\.json)")
BACKTICK_PATH_RE = re.compile(r"`([^`]+\.json)`")
QUALIFIER_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*:\s*")
ATOM_ID_RE = re.compile(r"^[A-Z][0-9][0-9A-Za-z_]*$")

FIELD_RE = re.compile(r"^(?P<f>[A-Za-z_][A-Za-z0-9_]*)\s+"
                      r"(?P<v>true|false|-?\d+)$")
OF_RE = re.compile(r"^(?P<f>[A-Za-z_][A-Za-z0-9_]*)\s+(?P<n>\d+)\s+of\s+"
                   r"(?P<m>\d+)$")
MISMATCH_RE = re.compile(r"^(?P<n>\d+)\s+mismatches$")
SURVIVOR_RE = re.compile(r"^(?P<n>\d+)\s+survivors$")
ATOMS_RE = re.compile(r"^(?P<n>\d+|[A-Za-z]+)\s+atoms$")
PRISTINE_RE = re.compile(r"^pristine\s+(?P<n>\d+)(?:\s+cases)?$")
VALIDATE_RE = re.compile(r"^validate\s+defect-free$")

ROUND_NUM_RE = re.compile(r"\d+")


class Unevaluable(Exception):
    """Exit-2 class: the audit cannot score, so it claims nothing."""


# --------------------------------------------------------------------------
# byte access
# --------------------------------------------------------------------------

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def show(root: str, rev: str, path: str) -> str | None:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", "replace")


class Resolver:
    """Path -> parsed receipt (or None), cached per run."""

    def __init__(self, root: str, rev: str):
        self.root = root
        self.rev = rev
        self.cache: dict[str, dict | None] = {}

    def receipt(self, path: str) -> dict | None:
        if path in self.cache:
            return self.cache[path]
        raw = show(self.root, self.rev, path)
        if raw is None:
            self.cache[path] = None
            return None
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = None
        if not isinstance(data, dict):
            data = None
        self.cache[path] = data
        return data


# --------------------------------------------------------------------------
# grammar
# --------------------------------------------------------------------------

def split_clauses(group: str) -> list[str]:
    """Split on commas outside backticks; keep order, drop empties."""
    out: list[str] = []
    cur = ""
    tick = False
    for ch in group:
        if ch == "`":
            tick = not tick
        if ch == "," and not tick:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [c.strip() for c in out if c.strip()]


def parse_clause(clause: str) -> dict | None:
    """Return {'kind':..., ...} for a grammar clause, else None."""
    qualifier = None
    m = QUALIFIER_RE.match(clause)
    if m:
        qualifier = clause[:m.end() - 1].strip()
        clause = clause[m.end():].strip()
    for regex, kind in ((PRISTINE_RE, "pristine"), (OF_RE, "of"),
                        (MISMATCH_RE, "mismatch"), (SURVIVOR_RE, "survivor"),
                        (ATOMS_RE, "atoms"), (VALIDATE_RE, "validate"),
                        (FIELD_RE, "field")):
        m = regex.match(clause)
        if not m:
            continue
        groups = m.groupdict()
        out = {"kind": kind, "clause": clause, "qualifier": qualifier}
        out.update(groups)
        return out
    return None


def literal(text: str):
    if text == "true":
        return True
    if text == "false":
        return False
    return int(text)


def typed_equal(claimed, actual) -> bool:
    """Type-strict equality: True != 1, 0 != False, '0' != 0."""
    return type(claimed) is type(actual) and claimed == actual


def bind(clause: dict, receipt: dict) -> tuple[bool, str, dict]:
    """Score one parsed clause against a receipt.

    Returns (ok, status, detail).  status is one of
    'bound' | 'unbound' | 'defect'; detail carries claimed/actual.
    """
    kind = clause["kind"]
    if kind == "field":
        field = clause["f"]
        claimed = literal(clause["v"])
        atoms = receipt.get("atoms")
        if ATOM_ID_RE.match(field):
            if not isinstance(atoms, list):
                return False, "defect", {"reason": "no_atoms", "field": field}
            # An annotation may name an atom by its short id ("D24" for
            # "D24_capability_rows"): bind only when exactly one atom matches.
            matches = [r for r in atoms if isinstance(r, dict)
                       and (r.get("id") == field
                            or str(r.get("id", "")).startswith(field + "_"))]
            if len(matches) != 1:
                return False, "unbound", {
                    "reason": "unknown_atom" if not matches else "ambiguous_atom",
                    "field": field}
            actual = matches[0].get("ok")
            return (typed_equal(claimed, actual), "bound",
                    {"field": field, "claimed": claimed, "actual": actual})
        if field not in receipt:
            return False, "unbound", {"reason": "unknown_field", "field": field}
        actual = receipt[field]
        if not isinstance(actual, (bool, int, str)):
            return False, "unbound", {"reason": "non_scalar", "field": field}
        return (typed_equal(claimed, actual), "bound",
                {"field": field, "claimed": claimed, "actual": actual})
    if kind == "of":
        field = clause["f"]
        n, m_ = int(clause["n"]), int(clause["m"])
        # `arms_ok 3 of 3` pairs with `arms_total`; any other field pairs with
        # `<field>_total`.
        total_key = (field[:-3] + "_total" if field.endswith("_ok")
                     else field + "_total")
        if field not in receipt or total_key not in receipt:
            return False, "unbound", {"reason": "unknown_field",
                                      "field": field}
        hit = (receipt[field] == n and receipt[total_key] == m_)
        return hit, "bound", {"field": field, "claimed": [n, m_],
                              "actual": [receipt[field], receipt[total_key]]}
    if kind == "mismatch":
        n = int(clause["n"])
        if "mismatch_count" not in receipt:
            return False, "unbound", {"reason": "unknown_field",
                                      "field": "mismatch_count"}
        actual = receipt["mismatch_count"]
        return (actual == n), "bound", {"field": "mismatch_count",
                                        "claimed": n, "actual": actual}
    if kind == "survivor":
        n = int(clause["n"])
        if "survivor_count" not in receipt:
            return False, "unbound", {"reason": "unknown_field",
                                      "field": "survivor_count"}
        actual = receipt["survivor_count"]
        return (actual == n), "bound", {"field": "survivor_count",
                                        "claimed": n, "actual": actual}
    if kind == "atoms":
        token = clause["n"].lower()
        n = int(token) if token.isdigit() else NUM_WORDS.get(token)
        if n is None:
            return False, "unbound", {"reason": "bad_literal",
                                      "clause": clause["clause"]}
        atoms = receipt.get("atoms")
        if not isinstance(atoms, list):
            return False, "defect", {"reason": "no_atoms", "claimed": n}
        return (len(atoms) == n), "bound", {"field": "len(atoms)",
                                            "claimed": n,
                                            "actual": len(atoms)}
    if kind == "pristine":
        n = int(clause["n"])
        pristine = receipt.get("pristine")
        if not isinstance(pristine, dict):
            return False, "defect", {"reason": "no_pristine", "claimed": n}
        actual = pristine.get("cases")
        return (actual == n), "bound", {"field": "pristine.cases",
                                        "claimed": n, "actual": actual}
    if kind == "validate":
        validate = receipt.get("validate")
        if not isinstance(validate, dict):
            return False, "defect", {"reason": "no_validate"}
        defects = validate.get("defects")
        if not isinstance(defects, list):
            return False, "defect", {"reason": "no_validate"}
        return (not defects), "bound", {"field": "validate.defects",
                                        "claimed": [],
                                        "actual": defects}
    raise Unevaluable(f"unknown clause kind {kind!r}")


# --------------------------------------------------------------------------
# record surface
# --------------------------------------------------------------------------

def section(text: str, heading: str) -> str:
    if heading not in text:
        return ""
    tail = text.split(heading, 1)[1]
    return tail.split("\n## ", 1)[0]


def table_rows(block: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in block.splitlines():
        if not line.startswith("|"):
            continue
        if re.match(r"^\|[\s|:-]+\|?\s*$", line):
            continue
        body = line.strip()
        if body.startswith("|"):
            body = body[1:]
        if body.endswith("|"):
            body = body[:-1]
        rows.append([cell.strip() for cell in body.split(" | ")])
    return rows


def capability_rows(scorecard: str) -> list[dict]:
    """`## Capabilities` data rows: name, evidence cell, first-working round."""
    out: list[dict] = []
    block = section(scorecard, CAPABILITIES_HEADING)
    for lineno, line in enumerate(block.splitlines(), start=1):
        if not line.startswith("|") or re.match(r"^\|[\s|:-]+\|?\s*$", line):
            continue
        body = line.strip().strip("|")
        cells = [cell.strip() for cell in body.split(" | ")]
        if len(cells) < 4 or cells[0].lower() == "capability":
            continue
        numerals = ROUND_NUM_RE.findall(cells[3])
        if not numerals:
            continue
        out.append({"name": cells[0].strip("`").strip(),
                    "evidence": cells[2], "first_round": int(numerals[0]),
                    "line": lineno})
    return out


def province_bullets(province: str) -> list[dict]:
    """`- **Core — ...` bullets with their continuation lines."""
    out: list[dict] = []
    current = None
    for lineno, line in enumerate(province.splitlines(), start=1):
        if line.startswith("- "):
            current = {"line": lineno, "text": line} if \
                line.startswith(PROVINCE_BULLET) else None
            if current is not None:
                out.append(current)
            continue
        if line.startswith("## "):
            current = None
            continue
        if current is not None:
            current["text"] += "\n" + line
    return out


def nearest_path(cell: str, group_start: int) -> str | None:
    """The JSON path immediately preceding the group, else the first one."""
    before = cell[:group_start]
    paths = BACKTICK_PATH_RE.findall(before) or JSON_ONLY_RE.findall(before)
    if paths:
        return paths[-1]
    after = BACKTICK_PATH_RE.findall(cell) or JSON_ONLY_RE.findall(cell)
    return after[0] if after else None


def bind_cell(cell: str, resolver: Resolver, label: str) -> dict:
    """Score every annotation group in one evidence cell."""
    result = {"label": label, "groups": 0, "bound": 0, "unbound": 0,
              "prose": 0, "defects": [], "clauses": []}
    for match in GROUP_RE.finditer(cell):
        group = match.group(1)
        clauses = [parse_clause(c) for c in split_clauses(group)]
        parsed = [c for c in clauses if c is not None]
        result["groups"] += 1
        if not parsed:
            result["prose"] += 1
            continue
        path = nearest_path(cell, match.start())
        receipt = resolver.receipt(path) if path else None
        if path is None:
            for clause in parsed:
                result["unbound"] += 1
                result["clauses"].append({"clause": clause["clause"],
                                          "status": "unbound",
                                          "reason": "no_json_receipt"})
            result["defects"].append(
                {"label": label, "group": group, "reason": "no_json_receipt"})
            continue
        if receipt is None:
            result["defects"].append(
                {"label": label, "group": group, "reason": "absent_receipt",
                 "path": path})
            continue
        for clause in parsed:
            ok, status, detail = bind(clause, receipt)
            row = {"clause": clause["clause"], "status": status,
                   "qualifier": clause["qualifier"], "path": path}
            row.update(detail)
            if status == "bound":
                result["bound"] += 1
                if not ok:
                    row["status"] = "defect"
                    result["defects"].append(
                        {"label": label, "group": group, "path": path,
                         "reason": "value_mismatch", **detail})
            else:
                result["unbound"] += 1
            result["clauses"].append(row)
    return result


def audit(root: str, rev: str) -> dict:
    scorecard = show(root, rev, SCORECARD)
    province = show(root, rev, PROVINCE)
    if scorecard is None:
        raise Unevaluable(f"{SCORECARD} absent at {rev}")
    resolver = Resolver(root, rev)
    rows = capability_rows(scorecard)
    cells: list[dict] = []
    in_scope = [r for r in rows if r["first_round"] >= SCOPE_MIN_ROUND]
    for row in in_scope:
        cells.append(bind_cell(row["evidence"],
                               resolver,
                               f"{CAPABILITIES_HEADING} row {row['name']!r} "
                               f"(first-working round {row['first_round']})"))
    for bullet in (province_bullets(province) if province else []):
        cells.append(bind_cell(bullet["text"], resolver,
                               f"{PROVINCE} line {bullet['line']}"))
    defects = [d for cell in cells for d in cell["defects"]]
    bound = sum(cell["bound"] for cell in cells)
    unbound = sum(cell["unbound"] for cell in cells)
    groups = sum(cell["groups"] for cell in cells)
    receipt = {
        "schema": "kaidoku-r77-verdict-bind-v1",
        "rev": rev,
        "root": os.path.abspath(root),
        "predicate": PREDICATE,
        "scope": {"scorercard_heading": CAPABILITIES_HEADING,
                  "min_first_working_round": SCOPE_MIN_ROUND,
                  "province_bullet": PROVINCE_BULLET.strip()},
        "population": {"capability_rows": len(rows),
                       "in_scope_rows": len(in_scope),
                       "groups": groups, "bound_clauses": bound,
                       "unbound_clauses": unbound},
        "cells": cells,
        "defects": defects,
        "mismatch_count": len(defects),
        "instrument": {"path": "tools/round-77/verdict-bind.py",
                       "sha256": sha256_bytes(
                           pathlib.Path(__file__).read_bytes())},
    }
    receipt["ok"] = not defects and bound > 0
    receipt["validate"] = {"defects": [], "bound_clauses": bound}
    receipt["validate"]["defects"] = receipt_defects(receipt)
    receipt["exit"] = 0 if (receipt["ok"]
                            and not receipt["validate"]["defects"]) else 1
    return receipt


# --------------------------------------------------------------------------
# receipt validation
# --------------------------------------------------------------------------

def receipt_defects(receipt: dict) -> list[str]:
    defects: list[str] = []
    cells = receipt.get("cells")
    if not isinstance(cells, list) or not cells:
        return ["cells absent or empty"]
    defects_list = receipt.get("defects")
    if not isinstance(defects_list, list):
        defects.append("defects absent")
        defects_list = []
    recomputed = [d for cell in cells if isinstance(cell, dict)
                  for d in cell.get("defects", [])]
    if len(recomputed) != len(defects_list):
        defects.append("defects row count disagrees with the cell rows")
    bound = sum(cell.get("bound", 0) for cell in cells if isinstance(cell, dict))
    population = receipt.get("population") or {}
    if population.get("bound_clauses") != bound:
        defects.append("population.bound_clauses disagrees with the cell rows")
    if receipt.get("mismatch_count") != len(defects_list):
        defects.append("mismatch_count disagrees with the defects rows")
    if receipt.get("ok") is not (len(defects_list) == 0 and bound > 0):
        defects.append("ok disagrees with defects/bound")
    if not isinstance(receipt.get("validate"), dict):
        defects.append("validate block absent")
    return defects


def validate(path: str) -> int:
    try:
        with open(path, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"validate": path, "defects": [f"unreadable: {exc}"]}))
        return 1
    defects = receipt_defects(receipt)
    print(json.dumps({"validate": path, "defects": defects}, indent=1))
    return 0 if not defects else 1


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------

def make_receipt(**kw) -> dict:
    base = {"atoms": [{"id": "D24_capability_rows", "ok": True}],
            "mismatch_count": 0, "exit": 0, "validate": {"defects": []},
            "pristine": {"cases": 25, "failures": []}, "survivor_count": 0,
            "arms_ok": 3, "arms_total": 3}
    base.update(kw)
    return base


def cell_case(cell: str, receipt: dict | None) -> dict:
    class R:
        def receipt(self, path):
            return receipt
    return bind_cell(cell, R(), "selftest")


def selftest() -> int:
    cases: dict[str, bool] = {}
    good = make_receipt()
    bad = make_receipt(atoms=[{"id": "D24_capability_rows", "ok": False}],
                       mismatch_count=1, exit=1)
    # red: the round-76 false annotation, both clauses false
    cell = "`.ufo/waves/round-76/l1/scores/c1-at-landing.json` (D24 true, mismatch_count 0)"
    out = cell_case(cell, bad)
    cases["red-false-annotation"] = (
        len(out["defects"]) == 2
        and {d["field"] for d in out["defects"]} == {"D24", "mismatch_count"})
    # green: the legitimate look-alike - the same cell against a matching receipt
    out = cell_case(cell, good)
    cases["green-same-cell-true"] = out["defects"] == [] and out["bound"] == 2
    # green: pointer only, no verdict
    out = cell_case("`.ufo/waves/round-76/l1/scores/c1-at-landing.json`", good)
    cases["green-pointer-only"] = out["defects"] == [] and out["groups"] == 0
    # green: prose annotation, no parsed clause
    out = cell_case("`.ufo/waves/round-76/l1/scores/c1-at-landing.json` "
                    "(the round-39 Core row naming the handler)", good)
    cases["green-prose"] = out["defects"] == [] and out["prose"] == 1
    # red: type mismatch - true is not 1
    out = cell_case("`.ufo/x.json` (mismatch_count true)",
                    make_receipt(mismatch_count=1))
    cases["red-type-mismatch"] = [d["reason"] for d in out["defects"]] == \
        ["value_mismatch"]
    # red: unknown field is unbound, never a guessed pass
    out = cell_case("`.ufo/x.json` (survivor 1)", good)
    cases["unbound-unknown-field"] = (out["unbound"] == 1
                                      and out["defects"] == [])
    # red: absent receipt
    out = cell_case("`.ufo/x.json` (mismatch_count 0)", None)
    cases["red-absent-receipt"] = [d["reason"] for d in out["defects"]] == \
        ["absent_receipt"]
    # red: bound clause but no JSON pointer
    out = cell_case("(mismatch_count 0)", good)
    cases["red-no-json-pointer"] = [d["reason"] for d in out["defects"]] == \
        ["no_json_receipt"]
    # word atoms: nine binds, eight fails
    nine = make_receipt(atoms=[{"id": f"A{i}", "ok": True} for i in range(9)])
    out = cell_case("`.ufo/x.json` (0 survivors, validate defect-free, "
                    "nine atoms, pristine 25)", nine)
    cases["green-vocabulary"] = out["defects"] == [] and out["bound"] == 4
    out = cell_case("`.ufo/x.json` (nine atoms)", make_receipt())
    cases["red-atom-count"] = [d["field"] for d in out["defects"]] == ["len(atoms)"]
    # of-form: total disagrees
    out = cell_case("`.ufo/x.json` (arms_ok 3 of 3)",
                    make_receipt(arms_total=2))
    cases["red-of-total"] = [d["field"] for d in out["defects"]] == ["arms_ok"]
    # validate defect-free fails on a defective validate block
    out = cell_case("`.ufo/x.json` (validate defect-free)",
                    make_receipt(validate={"defects": ["x"]}))
    cases["red-validate"] = [d["field"] for d in out["defects"]] == \
        ["validate.defects"]
    # scope floor: a row at first-working round 72 is out of scope
    sc = (f"{CAPABILITIES_HEADING}\n\n| Capability | What it can now do | "
          "Evidence pointer | First-working round |\n|---|---|---|---|\n"
          "| `old` | eight words of description here for the row | "
          "`.ufo/x.json` (mismatch_count 0) | 72 |\n")
    rows = capability_rows(sc)
    cases["scope-floor"] = ([r["first_round"] for r in rows] == [72]
                            and rows[0]["first_round"] < SCOPE_MIN_ROUND)
    # qualifier stripping: `r73: 0 survivors` binds
    out = cell_case("`.ufo/x.json` (r73: 0 survivors)", good)
    cases["qualifier-strip"] = out["defects"] == [] and out["bound"] == 1
    # receipt validation catches a self-contradicting receipt
    receipt = audit_for_selftest()
    cases["receipt-red"] = receipt_defects(dict(receipt, mismatch_count=9)) != []
    failures = [name for name, ok in cases.items() if not ok]
    print(json.dumps({"selftest": "tools/round-77/verdict-bind.py",
                      "cases": len(cases), "case_names": sorted(cases),
                      "failures": failures}, indent=1, sort_keys=True))
    return 0 if not failures else 1


def audit_for_selftest() -> dict:
    """A structurally valid receipt used only to score receipt_defects."""
    return {"cells": [{"bound": 2, "defects": []}], "defects": [],
            "mismatch_count": 0, "ok": True, "validate": {"defects": []},
            "population": {"bound_clauses": 2}}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--json-out")
    ap.add_argument("--validate")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.validate:
        return validate(args.validate)
    if not args.rev:
        print(json.dumps({"unevaluable": "--rev is required"}))
        return 2
    try:
        receipt = audit(args.root, args.rev)
    except Unevaluable as exc:
        print(json.dumps({"unevaluable": str(exc)}))
        return 2
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(json.dumps({k: receipt[k] for k in
                      ("rev", "population", "mismatch_count", "ok", "exit",
                       "validate")}, indent=1, sort_keys=True))
    return 0 if receipt["ok"] and not receipt["validate"]["defects"] else 1


if __name__ == "__main__":
    sys.exit(main())


# --- control mutation: no-binding (parse_clause returns None) ---
def parse_clause(clause):  # noqa: F811 - deliberate control override
    return None
