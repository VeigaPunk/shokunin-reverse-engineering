#!/usr/bin/env python3
"""record-audit.py - round-75 instrument (R75-C2 calibration).

Counts mismatches between the lane's own record and the repo state it claims to
describe.  The atom population is the previous round's NON-AUTHOR spot-check
(`corpus/lessons/round-74-verifier-spotcheck.md`, section "Routed defects"), an
outside document: each atom re-derives one routed defect's repair from committed
bytes at a measured revision.

Round 74's audit met four of these defects with cosmetic passes: a used-by cell
that *negated* the path it named, a search-log line carrying the tokens without
the counts, an erratum that reversed the two values, and a rejected row with an
empty reason/flip.  The round-74 wave demonstrated all four.  This version
gives those atoms exact grammars (parsed cells, required fields, typed counts,
bound receipts) and carries the four red fixtures in its own selftest, so a
cosmetic pass can be shown to fail before any record is scored.

Atoms (round-74 spot-check routed defects 1-8; defect 8 is a cosmetic report
rounding and is recorded as not atomised, by reason):

  D16  the C2 landing receipt carries its `--validate` verdict and a committed
       validation receipt names it (routed defect 1)
  D17  S275's used-by old->new change is re-logged in the round-75 lesson,
       naming the round-74 wave file that held it (routed defect 2)
  D18  the canary-field mutant's declared case is its SOLE detector and the
       landing battery has zero survivors (routed defect 3)
  D19  the three critic survivors are in the extended patch set and killed by
       their declared cases (routed defect 4a)
  D20  the strengthened D9-D12 grammars each reject their red fixture, and the
       selftest receipt records those names (routed defect 4b)
  D21  the base receipt binds its runner, and the freeze container pins exactly
       the plan's instruments, each pin equal to the blob at the freeze
       (routed defect 5)
  D22  the four SentinelScope code items carry passing selftest arms in the
       round-75 instruments (routed defect 6)
  D23  the search log states the row-`opened` convention and the round-75 Gate
       table follows it (routed defect 7)

Exit: 0 every atom true; 1 mismatches, each named; 2 could-not-evaluate.
`--validate <receipt>` checks a receipt's structural honesty; the written
receipt carries its own `validate` block.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

SCORECARD = "SCORECARD.md"
SOURCES = "corpus/SOURCES.md"
FREEZES = "corpus/claim-freezes-v2.tsv"
LESSON75 = "corpus/lessons/round-75.md"
ENTRY75 = "corpus/knowledge/2026-11-04-r75-a12-case-independence.md"
CLAIMS75 = ".ufo/waves/round-75/claims.json"
PLAN75 = "plans/round-75-claims.md"
C1_LANDING = ".ufo/waves/round-75/l1/scores/c1-at-landing.json"
C1_BASE = ".ufo/waves/round-75/pre/c1-base-arm.json"
C2_LANDING = ".ufo/waves/round-75/l1/scores/c2-at-landing.json"
C2_VALIDATE = ".ufo/waves/round-75/l1/scores/c2-validate-at-landing.json"
AUDIT_SELFTEST = ".ufo/waves/round-75/l1/scores/audit-selftest.json"
BATTERY_SELFTEST = ".ufo/waves/round-75/l1/scores/battery-selftest.json"
PROBE_SELFTEST = ".ufo/waves/round-75/l1/scores/probe-selftest.json"
FREEZE_SELFTEST = ".ufo/waves/round-75/l1/scores/freeze-pins-selftest.json"
ROUND75_HEADING = "## 2026-11-04 — round 75:"
SEARCH_HEADING = "## Search log"
REGISTRY_HEADING = "## Registry"
SCORECARD_ROUND74 = "## 2026-11-04 — round 74:"

PATH_RE = re.compile(r"^(?:corpus/knowledge|corpus/lessons)/[A-Za-z0-9._-]+\.md$")
R75_ROW = re.compile(r"(?m)^\|\s*S[0-9]{3,}\s*\|")
TOOL_PATH = re.compile(r"(?<![A-Za-z0-9_./-])(tools/round-75/[A-Za-z0-9._-]+\.py)"
                       r"(?![A-Za-z0-9_-])")


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


def show_bytes(root: str, rev: str, path: str) -> bytes | None:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def show_json(root: str, rev: str, path: str) -> dict | None:
    text = show(root, rev, path)
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def section(text: str, heading: str) -> str:
    """The body of a `## ...` section, up to the next `## ` heading."""
    if heading not in text:
        return ""
    return text.split(heading, 1)[1].split("\n## ", 1)[0]


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def table_rows(body: str) -> list[list[str]]:
    rows = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = split_row(stripped)
        if all(set(cell) <= set("-: ") for cell in cells):
            continue
        rows.append(cells)
    return rows


def row_by_id(body: str, sid: str) -> list[str] | None:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith(f"| {sid} |") or stripped.startswith(f"|{sid}|"):
            return split_row(stripped)
    return None


def census_rows(text: str) -> int:
    return len(re.findall(r"(?m)^\|[ \t]*S[0-9]{3,}[ \t]*\|", text))


# --------------------------------------------------------------------------
# exact grammars (routed defect 4b: the cosmetic passes)
# --------------------------------------------------------------------------

def parse_used_by(cell: str) -> tuple[list[str], list[str]]:
    """D9': a used-by cell is a comma-separated list of exact corpus paths.

    A negated token (`not <path>`) does not affirm the citation; a token that
    is not a repo-relative `corpus/knowledge/` or `corpus/lessons/` markdown
    path does not name a cited file.
    """
    defects: list[str] = []
    tokens = [tok.strip() for tok in (cell or "").split(",") if tok.strip()]
    if not tokens or tokens == ["—"]:
        return [], ["empty used-by cell"]
    kept = []
    for tok in tokens:
        if tok == "—":
            continue
        low = tok.lower()
        if low.startswith(("not ", "no ", "never ")):
            defects.append(f"negated path token: {tok}")
            continue
        if not PATH_RE.match(tok):
            defects.append(f"token is not an exact corpus path: {tok}")
            continue
        kept.append(tok)
    if not kept:
        defects.append("no affirmative path token")
    return kept, defects


def parse_search_note(body: str, label: str) -> tuple[str | None, list[str]]:
    """D10': one note for `label` with the required fields and integer counts."""
    notes = [ln for ln in body.splitlines() if label in ln]
    if len(notes) != 1:
        return None, [f"{len(notes)} search notes name {label}"]
    note = notes[0]
    defects = []
    for field in ("Question:", "Where searched:", "Identified", "screened",
                  "included", "excluded", "Stop:"):
        if field not in note:
            defects.append(f"missing field: {field}")
    counts = dict(re.findall(
        r"(Identified|screened|included|excluded)\s+(\d+)", note))
    for field in ("Identified", "screened", "included", "excluded"):
        if field not in counts:
            defects.append(f"missing integer count: {field}")
    return note, defects


def parse_rejected_row(row: list[str]) -> list[str]:
    """D11': a rejected row's teaches cell is REJECTED: <reason>; flip: <cond>."""
    defects = []
    if len(row) < 11:
        return ["row does not carry 11 cells"]
    if row[7] != "rejected":
        return [f"status is {row[7]!r}, not rejected"]
    teaches = row[6]
    match = re.match(r"^REJECTED:\s*(.+?)[;\s]*flip:\s*(.+)$", teaches,
                     re.IGNORECASE)
    if not match:
        return ["teaches does not carry REJECTED: <reason>; flip: <condition>"]
    reason, flip = match.group(1).strip(" ;"), match.group(2).strip()
    if len(reason.split()) < 3:
        defects.append("rejection reason is fewer than three words")
    if len(flip.split()) < 3:
        defects.append("flip condition is fewer than three words")
    return defects


def parse_census_erratum(body: str, measured_rows: int) -> list[str]:
    """D12': the erratum names the measured row count and a committed receipt."""
    defects = []
    if "census erratum" not in body:
        return ["round-75 section carries no census erratum"]
    numbers = [int(n) for n in re.findall(r"\b(\d{2,4})\b", body)]
    if measured_rows not in numbers:
        defects.append(f"erratum does not name the measured {measured_rows} rows")
    if "W04" not in body:
        defects.append("erratum does not name the W04 warning count")
    return defects


GRAMMAR_CASES = {
    "d9-negated-path-red": lambda: parse_used_by(
        "not corpus/knowledge/x.md")[1] != [],
    "d9-exact-path-accepts": lambda: parse_used_by(
        "corpus/knowledge/x.md, corpus/lessons/round-1.md")[1] == [],
    "d9-token-grammar-red": lambda: parse_used_by("x.md")[1] != [],
    "d10-token-only-red": lambda: parse_search_note(
        "round 75 Question: Where searched: Identified screened included "
        "excluded Stop:", "round 75")[1] != [],
    "d10-counts-required-red": lambda: parse_search_note(
        "round 75 Question: Where searched: Identified 3, screened 3, "
        "included 1, excluded 2 Stop: x", "round 75")[1] == [],
    "d11-empty-flip-red": lambda: parse_rejected_row(
        ["S001", "src", "docs", "A", "scope", "anchor",
         "REJECTED: a real reason here", "rejected", "2026-11-04",
         "90d", "—"]) != [],
    "d11-complete-accepts": lambda: parse_rejected_row(
        ["S001", "src", "docs", "A", "scope", "anchor",
         "REJECTED: a real reason here; flip: when the page carries it",
         "rejected", "2026-11-04", "90d", "—"]) == [],
    "d12-reversed-values-red": lambda: parse_census_erratum(
        "census erratum: W04 lines 24 and 23 rows", 25) != [],
    "d12-bound-values-accepts": lambda: parse_census_erratum(
        "census erratum: 25 rows, W04 lines 23", 25) == [],
}


def grammar_cases() -> dict[str, bool]:
    return {name: bool(fn()) for name, fn in GRAMMAR_CASES.items()}


# --------------------------------------------------------------------------
# atoms
# --------------------------------------------------------------------------

def atom_validate_embedded(root: str, rev: str) -> dict:
    """D16 (routed defect 1): the landing receipt carries its own validation."""
    receipt = show_json(root, rev, C2_LANDING)
    val = show_json(root, rev, C2_VALIDATE)
    block = (receipt or {}).get("validate")
    ok = (bool(receipt) and isinstance(block, dict)
          and block.get("defects") == []
          and block.get("atoms") == len(ATOMS)
          and bool(val) and val.get("validate") == C2_LANDING
          and val.get("defects") == [])
    return {"id": "D16_validate_embedded", "ok": bool(ok),
            "detail": "the C2 landing receipt carries a defect-free validate "
                      "block and a committed validation receipt names it",
            "evidence": {"receipt_present": bool(receipt),
                         "receipt_validate": block,
                         "validate_receipt_present": bool(val),
                         "validate_names": (val or {}).get("validate"),
                         "validate_defects": (val or {}).get("defects")}}


def atom_s275_relog(root: str, rev: str) -> dict:
    """D17 (routed defect 2): S275's used-by old->new is logged in the lesson."""
    lesson = show(root, rev, LESSON75) or ""
    old = ("corpus/knowledge/2026-11-04-r72-checker-env-capsule.md, "
           ".ufo/waves/round-72/w1/ScoutSource.md")
    new = old + ", corpus/knowledge/2026-11-04-r73-kernel-witness-record.md"
    hits = [ln for ln in lesson.splitlines() if "S275" in ln]
    ok = any("used-by" in ln and old in ln and new in ln
             and ".ufo/waves/round-74/w1/ScribeRows.md" in ln for ln in hits)
    return {"id": "D17_s275_used_by_relog", "ok": bool(ok),
            "detail": "the round-75 lesson re-logs S275's used-by old and new "
                      "values and names the round-74 wave file holding the old",
            "evidence": {"s275_lines": len(hits), "lesson_present": bool(lesson)}}


def atom_canary_sole(root: str, rev: str) -> dict:
    """D18 (routed defect 3): the canary-field case is the sole detector."""
    receipt = show_json(root, rev, C1_LANDING)
    rows = {r.get("name"): r for r in (receipt or {}).get("mutants") or []
            if isinstance(r, dict)}
    row = rows.get("b-drop-canary-field") or {}
    sole = (receipt or {}).get("sole_detector") or {}
    ok = (bool(receipt) and receipt.get("patch_set") == "r75probe"
          and receipt.get("survivor_count") == 0
          and row.get("verdict") == "killed"
          and row.get("failed") == ["a12-kernel-canary-field"]
          and sole.get("b-drop-canary-field") is True)
    return {"id": "D18_canary_sole_detector", "ok": bool(ok),
            "detail": "the landing battery's canary-field mutant is killed by "
                      "exactly its declared case, zero survivors",
            "evidence": {"receipt_present": bool(receipt),
                         "row": row, "sole": sole.get("b-drop-canary-field"),
                         "survivor_count": (receipt or {}).get("survivor_count")}}


def atom_critic_classes(root: str, rev: str) -> dict:
    """D19 (routed defect 4a): the three critic survivors are bound."""
    receipt = show_json(root, rev, C1_LANDING)
    rows = {r.get("name"): r for r in (receipt or {}).get("mutants") or []
            if isinstance(r, dict)}
    expect = {"d-home-under-truthy": "a12-genuine-field-identity",
              "d-name-samples-last-wins": "a12-sample-name-merge",
              "d-lie-clean-superset": "a12-lie-clean-keys-exact"}
    out = {}
    for name, case in expect.items():
        row = rows.get(name) or {}
        out[name] = {"present": bool(row),
                     "verdict": row.get("verdict"),
                     "expect_case": row.get("expect_case"),
                     "failed": row.get("failed"),
                     "ok": (row.get("verdict") == "killed"
                            and row.get("expect_case") == case
                            and case in (row.get("failed") or []))}
    ok = all(row["ok"] for row in out.values())
    return {"id": "D19_critic_classes_bound", "ok": bool(ok),
            "detail": "home-under identity, sample last-wins and the superset "
                      "key test are in the landing patch set, each killed by "
                      "its declared case",
            "evidence": out}


def atom_grammar_reds(root: str, rev: str) -> dict:
    """D20 (routed defect 4b): each strengthened grammar rejects its fixture."""
    cases = grammar_cases()
    receipt = show_json(root, rev, AUDIT_SELFTEST)
    names = set((receipt or {}).get("case_names") or [])
    sources = show(root, rev, SOURCES) or ""
    registry = section(sources, REGISTRY_HEADING)
    s277 = row_by_id(registry, "S277") or []
    used_tokens, used_defects = parse_used_by(s277[10] if len(s277) > 10 else "")
    used_resolve = [p for p in used_tokens if show(root, rev, p) is not None]
    note, note_defects = parse_search_note(section(sources, SEARCH_HEADING),
                                           "round 75")
    s285 = row_by_id(registry, "S285") or []
    rej_defects = parse_rejected_row(s285) if s285 else ["S285 absent"]
    scorecard = show(root, rev, SCORECARD) or ""
    errata_defects = parse_census_erratum(section(scorecard, ROUND75_HEADING),
                                          census_rows(sources))
    live = {"s277_tokens": used_tokens, "s277_defects": used_defects,
            "s277_resolved": used_resolve, "note_defects": note_defects,
            "s285_defects": rej_defects, "erratum_defects": errata_defects}
    live_ok = (bool(used_tokens) and not used_defects
               and used_resolve == used_tokens and note is not None
               and not note_defects and not rej_defects and not errata_defects)
    ok = (all(cases.values())
          and set(GRAMMAR_CASES) <= names
          and (receipt or {}).get("failures") == []
          and live_ok)
    return {"id": "D20_grammar_reds", "ok": bool(ok),
            "detail": "the four strengthened grammars reject their red fixture "
                      "in-process and in a committed selftest receipt, and the "
                      "live S277 used-by cell, round-75 search note, S285 rejected "
                      "row and census erratum all parse clean",
            "evidence": {"cases": cases, "receipt_present": bool(receipt),
                         "receipt_names_grammars": sorted(
                             set(GRAMMAR_CASES) & names),
                         "live": live}}


def atom_binding_and_pins(root: str, rev: str) -> dict:
    """D21 (routed defect 5): runner binding and an exact, pinned tool set."""
    base = show_json(root, rev, C1_BASE)
    runner = (base or {}).get("runner") or {}
    runner_blob = show_bytes(root, rev, "tools/round-75/probe-mutation.py")
    runner_ok = (runner.get("path") == "tools/round-75/probe-mutation.py"
                 and runner_blob is not None
                 and runner.get("sha256") == sha256_bytes(runner_blob))
    claims = show_json(root, rev, CLAIMS75)
    plan = show(root, rev, PLAN75) or ""
    named = sorted(set(TOOL_PATH.findall(plan)))
    pins = (claims or {}).get("instruments") or {}
    freeze_rev = None
    if claims:
        proc = subprocess.run(["git", "-C", root, "log", rev, "--diff-filter=A",
                               "--format=%H", "--", CLAIMS75],
                              capture_output=True, text=True)
        commits = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
        freeze_rev = commits[-1] if commits else None
    rows = {}
    if isinstance(freeze_rev, str):
        for path, digest in pins.items():
            blob = show_bytes(root, freeze_rev, path)
            rows[path] = {"pinned": digest,
                          "blob": sha256_bytes(blob) if blob else None,
                          "matched": blob is not None
                          and sha256_bytes(blob) == digest}
    ledger = show(root, rev, FREEZES) or ""
    ledger_rows = [ln for ln in ledger.splitlines() if ln.strip()]
    debt = any(ln.startswith("round-73\tFLAGGED\tINSTRUMENT_PIN_MISMATCH")
               for ln in ledger_rows)
    own_row = any(ln.startswith("round-75\tCLEAN\t-") for ln in ledger_rows)
    ok = (runner_ok and bool(named) and sorted(pins) == named
          and all(row["matched"] for row in rows.values())
          and len(rows) == len(pins) and debt and own_row)
    return {"id": "D21_binding_and_pins", "ok": bool(ok),
            "detail": "the base receipt binds the round-75 runner, the freeze "
                      "pins exactly the plan's round-75 instruments each equal "
                      "to the blob at the freeze, and the ledger restates the "
                      "round-73 standing pin debt beside the round-75 row",
            "evidence": {"runner_ok": runner_ok, "plan_tools": named,
                         "pinned": sorted(pins), "freeze_rev": freeze_rev,
                         "pins_match": {k: v["matched"] for k, v in rows.items()},
                         "ledger_round73_debt": debt,
                         "ledger_round75_row": own_row}}


def atom_security_arms(root: str, rev: str) -> dict:
    """D22 (routed defect 6): the four SentinelScope items carry green arms."""
    probe = show_json(root, rev, PROBE_SELFTEST)
    battery = show_json(root, rev, BATTERY_SELFTEST)
    freeze = show_json(root, rev, FREEZE_SELFTEST)
    landing = show_json(root, rev, C1_LANDING)
    probe_names = set((probe or {}).get("case_names") or [])
    battery_names = set((battery or {}).get("case_names") or [])
    freeze_names = set((freeze or {}).get("case_names") or [])
    pin = ((landing or {}).get("target_pin") or {})
    ok = ({"a11-shim-sidecar", "a12-shim-values-redacted"} <= probe_names
          and {"pin-mismatch-refused", "pin-unpinned-ok"} <= battery_names
          and {"containment-absolute-refused",
               "containment-traversal-refused"} <= freeze_names
          and (probe or {}).get("failures") == []
          and (battery or {}).get("failures") == []
          and (freeze or {}).get("failures") == []
          and pin.get("pinned_before_exec") is True)
    return {"id": "D22_security_arms", "ok": bool(ok),
            "detail": "shim-value redaction, the sidecar shim source, the "
                      "pin-before-execution and the freeze-pin containment "
                      "arms are green in committed selftest receipts",
            "evidence": {"probe_names": sorted(probe_names),
                         "battery_names": sorted(battery_names),
                         "freeze_names": sorted(freeze_names),
                         "pinned_before_exec": pin.get("pinned_before_exec")}}


def atom_opened_convention(root: str, rev: str) -> dict:
    """D23 (routed defect 7): the row-opened convention is stated and followed."""
    sources = show(root, rev, SOURCES) or ""
    log = section(sources, SEARCH_HEADING)
    stated = ("Convention:" in log and "first opened" in log
              and "round" in log.lower())
    lesson = show(root, rev, LESSON75) or ""
    gate = section(lesson, "## Gate")
    followed = False
    for row in table_rows(gate):
        if len(row) >= 3 and row[0].startswith("S2") and "round 74" in " ".join(row):
            followed = True
    ok = stated and followed
    return {"id": "D23_opened_convention", "ok": bool(ok),
            "detail": "the search log states the row-opened convention and a "
                      "round-75 Gate row names a retrospective opening round",
            "evidence": {"stated": stated, "followed": followed}}


ATOMS = [atom_validate_embedded, atom_s275_relog, atom_canary_sole,
         atom_critic_classes, atom_grammar_reds, atom_binding_and_pins,
         atom_security_arms, atom_opened_convention]


# --------------------------------------------------------------------------
# receipt validation
# --------------------------------------------------------------------------

def receipt_defects(receipt: dict) -> list[str]:
    defects = []
    atoms = receipt.get("atoms")
    if not isinstance(atoms, list) or not atoms:
        return ["atoms absent or empty"]
    ids = [row.get("id") for row in atoms if isinstance(row, dict)]
    if len(ids) != len(ATOMS):
        defects.append("atom count disagrees with the frozen table")
    if len(set(ids)) != len(ids):
        defects.append("duplicate atom ids")
    if receipt.get("mismatch_count") != sum(
            1 for row in atoms if not row.get("ok")):
        defects.append("mismatch_count disagrees with the atom rows")
    if receipt.get("ok") is not (receipt.get("mismatch_count") == 0):
        defects.append("ok disagrees with mismatch_count")
    if not isinstance(receipt.get("validate"), dict):
        defects.append("validate block absent")
    return defects


def audit(root: str, rev: str) -> dict:
    rows = []
    for fn in ATOMS:
        rows.append(fn(root, rev))
    mismatches = [row["id"] for row in rows if not row["ok"]]
    receipt = {"schema": "kaidoku-r75-record-audit-v1", "rev": rev,
               "root": os.path.abspath(root), "atoms": rows,
               "mismatch_count": len(mismatches), "mismatches": mismatches,
               "ok": not mismatches}
    receipt["validate"] = {"defects": [], "atoms": len(rows)}
    receipt["validate"]["defects"] = receipt_defects(receipt)
    return receipt


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


def selftest() -> int:
    cases = grammar_cases()
    cases["receipt-defects-red"] = receipt_defects(
        {"atoms": [{"id": "x", "ok": False}], "mismatch_count": 0,
         "ok": True, "validate": {}}) != []
    print(json.dumps({"selftest": "tools/round-75/record-audit.py",
                      "cases": len(cases), "case_names": sorted(cases),
                      "failures": [k for k, v in cases.items() if not v]},
                     indent=1, sort_keys=True))
    return 0 if all(cases.values()) else 1


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
    print(text)
    return 0 if receipt["ok"] and not receipt["validate"]["defects"] else 1


if __name__ == "__main__":
    sys.exit(main())
