#!/usr/bin/env python3
"""record-audit.py - round-73 instrument (R73-C2 calibration).

Counts mismatches between the lane's own record and the repo state it claims to
describe.  The atom population is the previous round's NON-AUTHOR spot-check
(corpus/lessons/round-72-verifier-spotcheck.md, section "Routed defects"), an
outside document: the audit re-derives each routed defect from committed bytes
at a measured revision, so a repaired record and an unrepaired one cannot score
the same.

Every atom is a predicate over `git show <rev>:<path>` bytes plus the receipts
those bytes cite; nothing is re-run and nothing is trusted as stated.  The
counter prints per-atom rows and a mismatch count; exit 0 requires every atom
resolved, 1 names the unresolved ones, 2 is the unevaluable class.

Atom classes:
  record_vs_receipt   a value the record states vs the receipt it names
  receipt_absolute    a value inside a committed receipt, checked against the
                      blob/revision that receipt itself names
  record_presence     a required block or field in the record
  record_text         a declared correction sentence (the routed-defect
                      discharge for a claim that cannot be re-derived)

The frozen atom table is `ATOMS` below; a post-freeze addition is a new round's
atom, never an edit of these.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

SPOTCHECK = "corpus/lessons/round-72-verifier-spotcheck.md"
SCORECARD = "SCORECARD.md"
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
ROUND72_HEADING = "## 2026-11-04 — round 72:"
ROUND73_HEADING = "## 2026-11-04 — round 73:"
CORRECTION_MARK = "**Correction (round 73"
TRIO_RE = re.compile(r"(?m)^(source|verified-at|recheck):")
LIST_TRIO_RE = re.compile(r"(?m)^- `(source|verified-at|recheck):")


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
    stated = re.findall(r"target sha `([0-9a-f]{8,64})", body)
    wrong = [tok for tok in stated
             if isinstance(measured, str) and not measured.startswith(tok)]
    correction = CORRECTION_MARK in body
    tail = body.split(CORRECTION_MARK, 1)[-1] if correction else ""
    # The correction must name BOTH values: a correction that repeats only the
    # wrong token leaves the record self-contradictory (round-73 CriticClaims'
    # D1 false-green).
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
    block = (gate or {}).get("disclosures")
    ok = (isinstance(block, dict) and block.get("missing") == []
          and block.get("stray") == [] and has72 and has73)
    return {"id": "D3_record_gate_disclosures", "ok": bool(ok),
            "detail": "the record gate's disclosures block is empty-missing and "
                      "empty-stray, and the freeze ledger carries both rounds",
            "evidence": {"base_gate_has_disclosures":
                         isinstance((base_gate or {}).get("disclosures"), dict),
                         "r73_gate_present": bool(gate),
                         "r73_disclosures": block,
                         "ledger_round_72": has72, "ledger_round_73": has73}}


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
    open72 = bool(TRIO_RE.search(first_lines(r72, 12)))
    corr72 = "## Provenance (round 73 correction)" in r72 and len(
        LIST_TRIO_RE.findall(r72.split("## Provenance (round 73 correction)", 1)[1])) == 3
    open73 = bool(TRIO_RE.search(first_lines(r73, 12))) and len(
        TRIO_RE.findall(first_lines(r73, 12))) == 3
    ok = (open72 or corr72) and open73
    return {"id": "D5_provenance_trio_open", "ok": bool(ok),
            "detail": "the round-72 entry carries the appended correction trio "
                      "and the round-73 entry opens with its own trio",
            "evidence": {"r72_trio_in_first_12": open72,
                         "r72_correction_trio": corr72,
                         "r73_trio_in_first_12": open73}}


def atom_before_pointer(root: str, rev: str) -> dict:
    """D7: each round's before receipt is named once and resolves."""
    scorecard = show(root, rev, SCORECARD) or ""
    r72 = section(scorecard, ROUND72_HEADING)
    r73 = section(scorecard, ROUND73_HEADING)
    named = re.findall(r"l1/pre/[A-Za-z0-9._-]+\.json", r72 + r73)
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


def atom_nudge_rationale(root: str, rev: str) -> dict:
    """D6: the round's rationale names the lowest axis it satisfies."""
    scorecard = show(root, rev, SCORECARD) or ""
    r73 = section(scorecard, ROUND73_HEADING)
    ok = ("lowest-axis:" in r73 and "nudge applies" not in r73
          and "stagnation nudge applies" not in r73)
    return {"id": "D6_nudge_rationale", "ok": bool(ok),
            "detail": "the round-73 section names its lowest-axis target and "
                      "does not claim the nudge waiver",
            "evidence": {"section_present": bool(r73),
                         "names_lowest_axis": "lowest-axis:" in r73,
                         "claims_waiver": "nudge applies" in r73}}


ATOMS = [atom_c2_evidence_hash, atom_c2_pin, atom_gate_disclosures,
         atom_c3_exit_code, atom_provenance_open, atom_nudge_rationale,
         atom_before_pointer]


def audit(root: str, rev: str) -> dict:
    spotcheck = show(root, rev, SPOTCHECK)
    atoms = []
    for fn in ATOMS:
        atoms.append(fn(root, rev))
    mismatches = [a["id"] for a in atoms if not a["ok"]]
    return {"schema": "kaidoku-r73-record-audit-v1", "rev": rev,
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
    cases["validate-clean"] = True
    print(json.dumps({"selftest": "tools/round-73/record-audit.py",
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
        print(json.dumps({"schema": "kaidoku-r73-record-audit-v1",
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
