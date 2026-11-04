#!/usr/bin/env python3
"""record-audit.py - round-74 instrument (R74-C2 calibration).

Counts mismatches between the lane's own record and the repo state it claims to
describe.  The atom population is the previous round's NON-AUTHOR spot-check
(`corpus/lessons/round-73-verifier-spotcheck.md`, section "Routed defects"), an
outside document: each atom re-derives one routed defect (or one of the round-73
planned items) from committed bytes at a measured revision, so a repaired record
and an unrepaired one cannot score the same.

The round-73 atoms (D1-D7) are retained byte-for-byte in meaning; round 74 adds
D7b and D8-D15 for the round-73 spot-check's routed defects 1-8 and the planned
items (b) and (d).  Every atom is a predicate over `git show <rev>:<path>` bytes
plus the receipts those bytes cite; nothing is re-run and nothing is trusted as
stated.

Atom classes:
  record_vs_receipt   a value the record states vs the receipt it names
  receipt_absolute    a value inside a committed receipt, checked against the
                      blob/revision that receipt itself names
  record_presence     a required block or field in the record
  record_text         a declared correction sentence

The frozen atom table is `ATOMS` below; a post-freeze addition is a new round's
atom, never an edit of these.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys

SPOTCHECK = "corpus/lessons/round-73-verifier-spotcheck.md"
SCORECARD = "SCORECARD.md"
SOURCES = "corpus/SOURCES.md"
README = "corpus/README.md"
FREEZES = "corpus/claim-freezes-v2.tsv"
KNOWLEDGE_R72 = "corpus/knowledge/2026-11-04-r72-checker-env-capsule.md"
KNOWLEDGE_R73 = "corpus/knowledge/2026-11-04-r73-kernel-witness-record.md"
RECEIPT_C2_BASE = ".ufo/waves/round-72/l1/scores/c2-at-landing.json"
RECEIPT_C1_BASE = ".ufo/waves/round-72/l1/pre/c1-at-base.json"
RECEIPT_C3_LYING_BASE = ".ufo/waves/round-72/l1/scores/c3-lying-check.json"
GATE_BASE = ".ufo/waves/round-72/l1/scores/gate-at-record.json"
R73_C2 = ".ufo/waves/round-73/l1/scores/c3-at-landing.json"  # the mutation receipt carries the pin
R73_C3_LYING = ".ufo/waves/round-73/l1/scores/c3-lying-check.json"
R73_GATE = ".ufo/waves/round-73/l1/scores/gate-at-record.json"
R74_PRE = ".ufo/waves/round-74/pre/c1-base-arm.json"
R74_CLAIMS = ".ufo/waves/round-74/claims.json"
PROMUT = "tools/round-74/probe-mutation.py"
ROUND72_HEADING = "## 2026-11-04 — round 72:"
ROUND73_HEADING = "## 2026-11-04 — round 73:"
ROUND74_HEADING = "## 2026-11-04 — round 74:"
CORRECTION_MARK = "**Correction (round 73"
SELECTION_MARK = "**Before-arm selection (round 74 correction)**"
CAPS_HEADING = "## Capabilities"
SEARCH_HEADING = "## Search log"
R73_REJECTED_PAGES = ("proc.5.html", "proc_cmdline.5.html", "proc_pid.5.html",
                      "index.html#_section_5")
R73_ENTRY = "corpus/knowledge/2026-11-04-r73-kernel-witness-record.md"
PATH_TOKEN = r"[A-Za-z0-9_./-]+\.(?:json|md|py|sh|txt|tsv)"


class Unevaluable(Exception):
    """Exit-2 class: the audit cannot score, so it claims nothing."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(root: str, *argv: str) -> bytes:
    proc = subprocess.run(["git", "-C", root, *argv], capture_output=True)
    if proc.returncode != 0:
        raise Unevaluable(f"git {' '.join(argv)} failed rc={proc.returncode}: "
                          f"{proc.stderr.decode('utf-8', 'replace')[-300:]}")
    return proc.stdout


def show(root: str, rev: str, path: str) -> str | None:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", "replace")


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
    body = text.split(heading, 1)[1]
    return body.split("\n## ", 1)[0]


def first_lines(text: str, count: int) -> str:
    return "\n".join(text.splitlines()[:count])


def split_row(line: str) -> list[str]:
    """Cells of a pipe-table row (GFM splits on unescaped pipes; the registry
    carries no escaped pipes after round 73's normalization)."""
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def table_rows(body: str) -> list[list[str]]:
    """Data rows of a markdown table body (the separator row excluded)."""
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


def row_for(body: str, prefix: str) -> list[str] | None:
    for line in body.splitlines():
        if line.strip().startswith(prefix):
            return split_row(line.strip())
    return None


def resolves(root: str, rev: str, path: str) -> bool:
    return show(root, rev, path) is not None


# --------------------------------------------------------------------------
# atoms: each takes (root, rev) and returns {id, ok, detail, evidence}
# --------------------------------------------------------------------------

def atom_c2_evidence_hash(root: str, rev: str) -> dict:
    """D1: the round-72 C2 target sha the record states is the receipt's."""
    receipt = show_json(root, rev, RECEIPT_C2_BASE)
    scorecard = show(root, rev, SCORECARD) or ""
    body = section(scorecard, ROUND72_HEADING)
    measured = (receipt or {}).get("target_sha256")
    rrev = (receipt or {}).get("rev")
    blob_ok = None
    if isinstance(measured, str) and isinstance(rrev, str):
        proc = subprocess.run(["git", "-C", root, "show",
                               f"{rrev}:tools/round-72/seam-probe.py"],
                              capture_output=True)
        blob_ok = (proc.returncode == 0
                   and sha256_bytes(proc.stdout) == measured)
    stated = [tok for tok in __import__("re").findall(
        r"target sha `([0-9a-f]{8,64})", body)]
    wrong = [tok for tok in stated
             if isinstance(measured, str) and not measured.startswith(tok)]
    correction = CORRECTION_MARK in body
    tail = body.split(CORRECTION_MARK, 1)[-1] if correction else ""
    named = (all(tok in tail for tok in wrong)
             and isinstance(measured, str) and measured[:8] in tail)
    ok = (bool(receipt) and blob_ok is True
          and (not wrong or (correction and named)))
    return {"id": "D1_c2_evidence_hash", "ok": bool(ok),
            "detail": "the record's C2 target sha re-derives from the receipt's "
                      "own rev, or a round-73 correction names both values",
            "evidence": {"receipt_target_sha256": measured,
                         "receipt_rev": rrev, "blob_matches": blob_ok,
                         "stated_tokens": stated, "wrong_tokens": wrong,
                         "correction_block": correction,
                         "correction_names_wrong": named}}


def atom_c2_pin(root: str, rev: str) -> dict:
    """D2: the mutation battery's target pin is supplied, not vacuous."""
    receipt = show_json(root, rev, R73_C2)
    pin = (receipt or {}).get("target_pin") or {}
    target = (receipt or {}).get("target_sha256")
    ok = (bool(receipt) and isinstance(pin.get("expect"), str)
          and pin.get("expect") == target and pin.get("matched") is True)
    return {"id": "D2_c2_pin_conjunct", "ok": ok,
            "detail": "a landing mutation receipt pins an exact target blob "
                      "(expect == target_sha256, matched true)",
            "evidence": {"receipt": R73_C2 if receipt else None,
                         "target_pin": pin, "target_sha256": target}}


def atom_gate_disclosures(root: str, rev: str) -> dict:
    """D3: the record gate carries a disclosures block and the ledger its rows."""
    base_gate = show_json(root, rev, GATE_BASE)
    gate = show_json(root, rev, R73_GATE)
    ledger = show(root, rev, FREEZES) or ""
    rows = [ln for ln in ledger.splitlines()
            if ln.strip() and not ln.startswith("#")]
    has72 = any("round-72" in ln for ln in rows)
    has73 = any("round-73" in ln for ln in rows)
    has74 = any("round-74" in ln for ln in rows)
    block = (gate or {}).get("disclosures")
    ok = (isinstance(block, dict) and block.get("missing") == []
          and block.get("stray") == [] and has72 and has73 and has74)
    return {"id": "D3_record_gate_disclosures", "ok": bool(ok),
            "detail": "the record gate's disclosures block is empty-missing and "
                      "empty-stray, and the freeze ledger carries rounds 72-74",
            "evidence": {"base_gate_has_disclosures":
                         isinstance((base_gate or {}).get("disclosures"), dict),
                         "r73_gate_present": bool(gate),
                         "r73_disclosures": block,
                         "ledger_round_72": has72, "ledger_round_73": has73,
                         "ledger_round_74": has74}}


def atom_c3_exit_code(root: str, rev: str) -> dict:
    """D4: a receipt the record describes with an exit code records that code."""
    base = show_json(root, rev, RECEIPT_C3_LYING_BASE)
    landing = show_json(root, rev, R73_C3_LYING)
    ok = (bool(landing) and isinstance(landing.get("rc"), int)
          and landing.get("rc") == 1 and landing.get("met") is False)
    return {"id": "D4_c3_exit_code", "ok": bool(ok),
            "detail": "the lying-receipt checker run records rc 1 with met false",
            "evidence": {"base_receipt_rc": (base or {}).get("rc"),
                         "landing_receipt_rc": (landing or {}).get("rc"),
                         "landing_met": (landing or {}).get("met")}}


def atom_provenance_open(root: str, rev: str) -> dict:
    """D5: an entry's provenance trio sits at its open (or in a correction)."""
    r72 = show(root, rev, KNOWLEDGE_R72) or ""
    r73 = show(root, rev, KNOWLEDGE_R73) or ""
    trio = __import__("re").compile(r"(?m)^(source|verified-at|recheck):")
    list_trio = __import__("re").compile(r"(?m)^- `(source|verified-at|recheck):")
    open72 = bool(trio.search(first_lines(r72, 12)))
    corr72 = "## Provenance (round 73 correction)" in r72 and len(
        list_trio.findall(r72.split("## Provenance (round 73 correction)", 1)[1])) == 3
    open73 = bool(trio.search(first_lines(r73, 12))) and len(
        trio.findall(first_lines(r73, 12))) == 3
    ok = (open72 or corr72) and open73
    return {"id": "D5_provenance_trio_open", "ok": bool(ok),
            "detail": "the round-72 entry carries the appended correction trio "
                      "and the round-73 entry opens with its own trio",
            "evidence": {"r72_trio_in_first_12": open72,
                         "r72_correction_trio": corr72,
                         "r73_trio_in_first_12": open73}}


def atom_nudge_rationale(root: str, rev: str) -> dict:
    """D6: the round's rationale names the lowest axis it satisfies."""
    scorecard = show(root, rev, SCORECARD) or ""
    r73 = section(scorecard, ROUND73_HEADING)
    r74 = section(scorecard, ROUND74_HEADING)
    ok = (("lowest-axis:" in r73 and "nudge applies" not in r73
           and "stagnation nudge applies" not in r73)
          and ("lowest-axis:" in r74 and "nudge applies" not in r74))
    return {"id": "D6_nudge_rationale", "ok": bool(ok),
            "detail": "the round-73 and round-74 sections name their lowest "
                      "axis and do not claim the nudge waiver",
            "evidence": {"r73_names_lowest_axis": "lowest-axis:" in r73,
                         "r74_names_lowest_axis": "lowest-axis:" in r74,
                         "claims_waiver": "nudge applies" in (r73 + r74)}}


def atom_before_pointer(root: str, rev: str) -> dict:
    """D7: each round's before receipt is named once and resolves."""
    scorecard = show(root, rev, SCORECARD) or ""
    r72 = section(scorecard, ROUND72_HEADING)
    r73 = section(scorecard, ROUND73_HEADING)
    named = __import__("re").findall(r"l1/pre/[A-Za-z0-9._-]+\.json", r72 + r73)
    resolved = []
    for path in sorted(set(named)):
        receipt = show_json(root, rev, ".ufo/waves/round-72/" + path)
        if receipt is None:
            receipt = show_json(root, rev, ".ufo/waves/round-73/" + path)
        resolved.append({"path": path, "exists": receipt is not None,
                         "rev": (receipt or {}).get("rev")})
    ok = bool(resolved) and all(r["exists"] and isinstance(r["rev"], str)
                                for r in resolved)
    return {"id": "D7_before_pointer", "ok": bool(ok),
            "detail": "every before receipt a round section names resolves at "
                      "the measured revision and records its rev",
            "evidence": {"named": sorted(set(named)), "rows": resolved}}


def atom_before_selection(root: str, rev: str) -> dict:
    """D7b (round 74): a claim row with two before arms names which one is the
    before-arm and each other receipt's role.

    The round-73 C1 row named both `pre/c1-at-base-r72probe.json` (11 arms) and
    `pre/c1-at-base.json` (8 of 12) without saying which is the claim's
    before-arm -- D7 never noticed, because both resolve.  The repair is an
    appended selection block, never a rewrite of the filed row.
    """
    scorecard = show(root, rev, SCORECARD) or ""
    body = section(scorecard, ROUND73_HEADING)
    claims = {}
    for claim in ("R73-C1", "R73-C2", "R73-C3"):
        row = row_for(body, f"| {claim} |")
        if row is None:
            claims[claim] = {"present": False}
            continue
        paths = sorted(set(__import__("re").findall(
            r"pre/[A-Za-z0-9._-]+\.json", "|".join(row))))
        claims[claim] = {"present": True, "before_paths": paths}
    ambiguous = [c for c, row in claims.items() if len(row.get("before_paths") or []) >= 2]
    block = body.split(SELECTION_MARK, 1)[1] if SELECTION_MARK in body else ""
    named = all(path in block
                for c in ambiguous
                for path in claims[c]["before_paths"])
    ok = (all(row.get("present") for row in claims.values())
          and (not ambiguous or (bool(block) and named)))
    return {"id": "D7b_before_selection", "ok": bool(ok),
            "detail": "a round-73 claim row naming two before receipts has an "
                      "appended selection block naming the before-arm and "
                      "every other receipt's role",
            "evidence": {"claims": claims, "ambiguous": ambiguous,
                         "selection_block": bool(block),
                         "selection_names_all": named}}


def atom_capability_rows(root: str, rev: str) -> dict:
    """D8 (routed defect 1): the capabilities table carries the round-73 and
    round-74 acquisitions, each with a resolving evidence pointer."""
    scorecard = show(root, rev, SCORECARD) or ""
    body = section(scorecard, CAPS_HEADING)
    rows = table_rows(body)
    out = {"total": len(rows), "r73": 0, "r74": 0, "unresolved": []}
    for row in rows:
        if len(row) < 4:
            out["unresolved"].append(row[:1])
            continue
        last = row[-1]
        if "73" in last:
            out["r73"] += 1
        if "74" in last:
            out["r74"] += 1
    caps = [row for row in rows if len(row) >= 4
            and ("73" in row[-1] or "74" in row[-1])]
    for row in caps:
        tokens = __import__("re").findall(PATH_TOKEN, "|".join(row[1:-1]))
        if not any(resolves(root, rev, tok) for tok in tokens):
            out["unresolved"].append(row[0])
    ok = (out["r73"] >= 3 and out["r74"] >= 2 and not out["unresolved"])
    return {"id": "D8_capability_rows", "ok": bool(ok),
            "detail": "three round-73 and two round-74 capability rows are in "
                      "the table and each resolves an evidence pointer",
            "evidence": out}


def atom_s275_used_by(root: str, rev: str) -> dict:
    """D9 (routed defect 2): S275's used-by cell names the entry that cites it."""
    sources = show(root, rev, SOURCES) or ""
    body = section(sources, "## Registry")
    row = row_for(body, "| S275 |")
    used = row[-1] if row and len(row) >= 11 else None
    ok = bool(used) and R73_ENTRY in used
    return {"id": "D9_s275_used_by", "ok": bool(ok),
            "detail": "the S275 row's used-by cell lists the round-73 entry "
                      "that cites it",
            "evidence": {"row_present": row is not None,
                         "used_by": used, "expects": R73_ENTRY}}


def atom_search_log(root: str, rev: str) -> dict:
    """D10 (routed defect 3): the bounded search of rounds 73 and 74 is logged."""
    sources = show(root, rev, SOURCES) or ""
    body = section(sources, SEARCH_HEADING)
    has73 = "round 73" in body and "Identified" in body
    has74 = "round 74" in body and "Identified" in body
    ok = has73 and has74
    return {"id": "D10_search_log", "ok": bool(ok),
            "detail": "the search log carries a round-73 and a round-74 note "
                      "with the identified/screened/included counts",
            "evidence": {"round_73_note": has73, "round_74_note": has74}}


def atom_rejected_rows(root: str, rev: str) -> dict:
    """D11 (routed defect 4): the pages opened and rejected in round 73 are
    registered as rejected rows (reason + flip), not dropped."""
    sources = show(root, rev, SOURCES) or ""
    body = section(sources, "## Registry")
    rows = table_rows(body)
    rejected = []
    for row in rows:
        if len(row) < 11:
            continue
        if row[7] != "rejected":
            continue
        rejected.append(row)
    hits = {}
    for page in R73_REJECTED_PAGES:
        hits[page] = sum(1 for row in rejected if page in row[1])
    ok = all(count >= 1 for count in hits.values())
    return {"id": "D11_rejected_rows", "ok": bool(ok),
            "detail": "each round-73 opened-and-rejected page has a rejected "
                      "registry row with a reason and a flip condition",
            "evidence": {"rejected_rows": len(rejected), "per_page": hits}}


def atom_census_erratum(root: str, rev: str) -> dict:
    """D12 (routed defect 5): the census-arithmetic erratum names both values."""
    scorecard = show(root, rev, SCORECARD) or ""
    body = section(scorecard, ROUND74_HEADING)
    ok = ("census erratum" in body and "W04" in body
          and "24" in body and "23" in body)
    return {"id": "D12_census_erratum", "ok": bool(ok),
            "detail": "the round-74 record carries a census erratum naming the "
                      "reported 24 W04 lines and the measured 23",
            "evidence": {"round_74_section": bool(body),
                         "erratum": "census erratum" in body}}


def atom_readme_newline(root: str, rev: str) -> dict:
    """D13 (routed defect 7): the index file is newline-terminated."""
    text = show(root, rev, README)
    ok = text is not None and text.endswith("\n")
    return {"id": "D13_readme_newline", "ok": bool(ok),
            "detail": "corpus/README.md ends with a newline at the measured "
                      "revision",
            "evidence": {"present": text is not None,
                         "last_chars": repr((text or "")[-4:])}}


def atom_runner_binding(root: str, rev: str) -> dict:
    """D14 (routed defect 6): a before receipt binds the runner that made it."""
    receipt = show_json(root, rev, R74_PRE)
    runner = (receipt or {}).get("runner") or {}
    blob = show(root, rev, PROMUT)
    ok = (bool(receipt) and runner.get("path") == PROMUT
          and isinstance(runner.get("sha256"), str)
          and blob is not None and sha256_bytes(blob.encode()) == runner["sha256"])
    return {"id": "D14_runner_binding", "ok": bool(ok),
            "detail": "the round-74 base-arm receipt names its runner and the "
                      "runner's sha256 is the blob at the measured revision",
            "evidence": {"receipt": R74_PRE if receipt else None,
                         "runner": runner}}


def atom_freeze_pins(root: str, rev: str) -> dict:
    """D15 (planned item d): the freeze's pins are the blobs at the freeze."""
    claims = show_json(root, rev, R74_CLAIMS)
    if not claims:
        return {"id": "D15_freeze_pins", "ok": False,
                "detail": "the round-74 freeze container is present and every "
                          "producer pin equals the blob at its own freeze rev",
                "evidence": {"claims_present": False}}
    proc = subprocess.run(["git", "-C", root, "log", rev, "--diff-filter=A",
                           "--format=%H", "--", R74_CLAIMS],
                          capture_output=True, text=True)
    freeze_rev = None
    if proc.returncode == 0:
        commits = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
        freeze_rev = commits[-1] if commits else None
    rows = {}
    if isinstance(freeze_rev, str):
        for block in ("instruments", "loaded_by_counter"):
            for path, digest in (claims.get(block) or {}).items():
                blob = show(root, freeze_rev, path)
                rows[f"{block}:{path}"] = {
                    "pinned": digest,
                    "blob": sha256_bytes(blob.encode()) if blob is not None else None,
                    "matched": blob is not None
                    and sha256_bytes(blob.encode()) == digest}
    ok = bool(rows) and all(row["matched"] for row in rows.values())
    return {"id": "D15_freeze_pins", "ok": bool(ok),
            "detail": "the round-74 freeze container names its freeze revision "
                      "and every producer pin equals the blob at that revision",
            "evidence": {"freeze_rev": freeze_rev,
                         "rows": {k: v["matched"] for k, v in rows.items()}}}


ATOMS = [atom_c2_evidence_hash, atom_c2_pin, atom_gate_disclosures,
         atom_c3_exit_code, atom_provenance_open, atom_nudge_rationale,
         atom_before_pointer, atom_before_selection, atom_capability_rows,
         atom_s275_used_by, atom_search_log, atom_rejected_rows,
         atom_census_erratum, atom_readme_newline, atom_runner_binding,
         atom_freeze_pins]


def audit(root: str, rev: str) -> dict:
    spotcheck = show(root, rev, SPOTCHECK)
    atoms = []
    for fn in ATOMS:
        atoms.append(fn(root, rev))
    mismatches = [a["id"] for a in atoms if not a["ok"]]
    return {"schema": "kaidoku-r74-record-audit-v2", "rev": rev,
            "root": os.path.abspath(root),
            "population": {"document": SPOTCHECK,
                           "present": spotcheck is not None,
                           "atoms": len(atoms)},
            "atoms": atoms, "mismatches": mismatches,
            "mismatch_count": len(mismatches),
            "ok": not mismatches}


def validate(path: str) -> int:
    """QUALITY #114 in the record direction: a receipt is scoreable only when
    its own rows agree with its verdict fields."""
    try:
        with open(path, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"defects": [f"receipt unreadable: {exc}"]}))
        return 1
    defects = []
    atoms = receipt.get("atoms")
    if not isinstance(atoms, list) or not atoms:
        defects.append("atoms absent or empty")
        atoms = []
    for row in atoms:
        if not isinstance(row, dict) or not isinstance(row.get("ok"), bool):
            defects.append(f"{row.get('id') if isinstance(row, dict) else row}: "
                           f"no boolean verdict")
        if isinstance(row, dict) and not row.get("detail"):
            defects.append(f"{row.get('id')}: no detail")
    derived = sorted(a["id"] for a in atoms
                     if isinstance(a, dict) and a.get("ok") is False)
    if sorted(receipt.get("mismatches") or []) != derived:
        defects.append("mismatches disagree with the atom rows")
    if receipt.get("mismatch_count") != len(derived):
        defects.append("mismatch_count disagrees with the atom rows")
    if receipt.get("ok") is not (not derived):
        defects.append("ok disagrees with the atom rows")
    print(json.dumps({"validate": path, "defects": defects}, indent=1))
    return 0 if not defects else 1


def selftest() -> int:
    cases = {}
    cases["section-bounds"] = (
        section("a\n## X — y\nbody\n## Z", "## X — y").strip() == "body")
    cases["section-absent"] = section("nothing", "## X") == ""
    cases["first-lines"] = first_lines("1\n2\n3\n4", 2) == "1\n2"
    cases["row-split"] = (split_row("| a | b |  | c |") == ["a", "b", "", "c"])
    table = ("| cap | what | ptr | round 73 |\n|---|---|---|---|\n"
             "| x | y | z | 73 |\n| w | v | u | 72 |\n")
    cases["table-rows"] = (table_rows(table) == [["cap", "what", "ptr", "round 73"],
                                                ["x", "y", "z", "73"],
                                                ["w", "v", "u", "72"]])
    cases["row-for"] = (row_for("| R73-C1 | a |\n| R73-C2 | b |", "| R73-C1 |")
                        == ["R73-C1", "a"])
    two_arm = ("| R73-C1 | x | base `pre/a.json` and `pre/b.json` |\n")
    single = ("| R73-C1 | x | base `pre/a.json` |\n")
    import re as _re
    def selection_ok(body):
        row = row_for(body, "| R73-C1 |")
        paths = sorted(set(_re.findall(r"pre/[A-Za-z0-9._-]+\.json",
                                       "|".join(row or []))))
        block = body.split(SELECTION_MARK, 1)[1] if SELECTION_MARK in body else ""
        return (len(paths) < 2) or (bool(block) and all(p in block for p in paths))
    cases["selection-single-arm"] = selection_ok(single) is True
    cases["selection-two-arms-red"] = selection_ok(two_arm) is False
    cases["selection-two-arms-green"] = selection_ok(
        two_arm + SELECTION_MARK + "\n- before-arm `pre/a.json`; `pre/b.json` is "
        "the route differential\n") is True
    trap = ("| S275 | page | docs | A | scope | anchor | teaches | mined | "
            "2026-11-04 | 90d | corpus/knowledge/other.md |\n")
    cases["used-by-wrong-entry-red"] = (
        "corpus/knowledge/2026-11-04-r73-kernel-witness-record.md"
        not in split_row(trap.strip())[-1])
    right = trap.replace("other.md", "2026-11-04-r73-kernel-witness-record.md")
    cases["used-by-named-entry-green"] = (
        "corpus/knowledge/2026-11-04-r73-kernel-witness-record.md"
        in split_row(right.strip())[-1])
    cases["newline-check"] = (("a\n".endswith("\n") is True)
                              and ("a".endswith("\n") is False))
    print(json.dumps({"selftest": "tools/round-74/record-audit.py",
                      "cases": len(cases),
                      "failures": [k for k, v in cases.items() if not v]},
                     indent=1, sort_keys=True))
    return 0 if all(cases.values()) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    ap.add_argument("--rev")
    ap.add_argument("--json-out")
    ap.add_argument("--validate")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.validate:
        return validate(args.validate)
    if not (args.root and args.rev):
        print("record-audit: --root and --rev are required", file=sys.stderr)
        return 2
    try:
        receipt = audit(args.root, args.rev)
    except Unevaluable as exc:
        print(json.dumps({"schema": "kaidoku-r74-record-audit-v2",
                          "unevaluable": str(exc)}), file=sys.stderr)
        return 2
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
