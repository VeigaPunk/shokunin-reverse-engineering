#!/usr/bin/env python3
"""mutapply.py - ExecC1's OWN mutation applier for R69-C1.

Independent of tools/round-69/mutation-check.py: it shares no code with it, does
not import it and does not read its patch tables.  The patch strings below were
derived by reading the frozen blobs at the freeze commit
f15998102f1ce3569e61faa2ac6f286bc414538e; each must match exactly once or the
applier refuses (a zero/several match is a finding, never a silent no-op).

Two families per blob:

  constant  every arm expression replaced by the literal `True` (the seat's
            "patch the expression to a constant" reading: the gate becomes
            blind, which is the strongest kill target a selftest can be asked
            to catch)
  literal   the exact textual mutants declared by the frozen battery's patch
            sets r68/r69, applied by this applier so the battery's own claim
            can be checked without trusting its receipt

Usage:
  mutapply.py --blob <path> --family constant|literal --target r68|r69 \
              --outdir <dir> --json-out <file>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys

# --- r69 (tools/round-69/packed-elf.py), arm expressions inside evaluate_carrier()
R69_CONSTANT = [
    ("M1_identity", "arm-pack-identity-false",
     'identity_ok = model["unpack_rc"] == 0 and model["unpacked_sha256"] == model["pin"]',
     "identity_ok = True"),
    ("M2_recovery", "arm-pack-recovery-false",
     'recovery_ok = bool(model["recovered_counts"]) and model["recovered_counts"] == model["orig_counts"]',
     "recovery_ok = True"),
    ("M3_detected", "arm-pack-detected-false",
     'detected = model["upx_list_rc"] == 0 and model["section_count"] == 0',
     "detected = True"),
    ("M4_before", "arm-pack-before-false",
     'before_ok = model["packed_procedures"] is not None and model["packed_procedures"] <= model["before_max_procedures"]',
     "before_ok = True"),
    ("M5_control", "arm-pack-control-false",
     'control_ok = model["control_list_rc"] != 0 and model["control_decompress_rc"] != 0',
     "control_ok = True"),
]

# frozen battery patch set r69, re-typed by hand from the blob's own lines
R69_LITERAL = [
    ("M1_identity", "arm-pack-identity-false",
     'identity_ok = model["unpack_rc"] == 0 and model["unpacked_sha256"] == model["pin"]',
     "identity_ok = True"),
    ("M2_recovery", "arm-pack-recovery-false",
     'recovery_ok = bool(model["recovered_counts"]) and model["recovered_counts"] == model["orig_counts"]',
     'recovery_ok = bool(model["recovered_counts"])'),
    ("M3_detected", "arm-pack-detected-false",
     'detected = model["upx_list_rc"] == 0 and model["section_count"] == 0',
     'detected = model["upx_list_rc"] == 0'),
    ("M4_before", "arm-pack-before-false",
     'before_ok = model["packed_procedures"] is not None and model["packed_procedures"] <= model["before_max_procedures"]',
     'before_ok = model["packed_procedures"] is not None'),
    ("M5_control", "arm-pack-control-false",
     'control_ok = model["control_list_rc"] != 0 and model["control_decompress_rc"] != 0',
     "control_ok = True"),
]

# --- r68 (tools/round-68/packed-elf.py), arm expressions inside score()
# M5 lives in the fold() call: r68's local `control_ok` at line 277 is dead
# (never read again) - see rederive.md.
R68_CONSTANT = [
    ("M1_identity", None,
     'identity_ok = (unpack["rc"] == 0 and os.path.exists(unpacked)\n'
     '                           and sha256_file(unpacked) == c["sha256"])',
     "identity_ok = True"),
    ("M2_recovery", None,
     'recovery_ok = bool(rec_counts) and rec_counts == orig_counts',
     "recovery_ok = True"),
    ("M3_detected", None,
     'detected = listing["rc"] == 0 and secs == 0',
     "detected = True"),
    ("M4_before", None,
     'before_ok = before_procedures is not None and before_procedures < floor',
     "before_ok = True"),
    ("M5_control", None,
     'fold(carriers, all(c["control"]["list_rc"] != 0 and c["control"]["decompress_rc"] != 0\n'
     '                                     for c in carriers), len(CARRIERS))',
     "fold(carriers, True, len(CARRIERS))"),
]

R68_LITERAL = [
    ("M1_identity", None,
     'and sha256_file(unpacked) == c["sha256"])',
     "and True)"),
    ("M2_recovery", None,
     'and rec_counts == orig_counts',
     'and rec_counts == rec_counts'),
    ("M3_detected", None,
     'detected = listing["rc"] == 0 and secs == 0',
     'detected = listing["rc"] == 0 and True'),
    ("M4_before", None,
     'and before_procedures < floor',
     'and before_procedures == before_procedures'),
    ("M5_control", None,
     'fold(carriers, all(c["control"]["list_rc"] != 0 and c["control"]["decompress_rc"] != 0\n'
     '                                     for c in carriers), len(CARRIERS))',
     "fold(carriers, True, len(CARRIERS))"),
]

# --- r69 gate-strength probes (NOT part of R69-C1; report-only observations)
R69_EXTRA = [
    ("X1_ok_hardwired", "arm-pack-identity-false",
     'return {"arms": arms, "ok": all(arms.values())}',
     'return {"arms": arms, "ok": True}'),
    ("X2_fold_all_matched", "fold-not-met",
     'matched = sum(1 for c in carriers if c["ok"])',
     'matched = len(carriers)'),
    ("X3_sections_zero", "sections-some",
     '    if "There are no sections in this file" in readelf_text:\n        return 0\n'
     '    return len(re.findall(r"(?m)^\\s*\\[\\s*\\d+\\]\\s", readelf_text))',
     '    return 0'),
    ("X4_refusal_dropped", "arm-pack-refusal",
     '    refusal_ok = None\n    if model.get("address"):',
     '    refusal_ok = None\n    if False and model.get("address"):'),
    ("X5_arm_case_deleted", "case-inventory",
     '    ident = evaluate_carrier(_model(unpacked_sha256="bb" * 32))\n'
     '    cases.append(("arm-pack-identity-false",\n'
     '                  ident["arms"]["identity_ok"] is False and ident["ok"] is False))',
     '    ident = evaluate_carrier(_model(unpacked_sha256="bb" * 32))\n'
     '    _ = ident  # case deleted by mutant'),
    ("X6_control_unwired", "arm-pack-control-false",
     '    arms = carrier_arms(detected, before_ok, identity_ok, recovery_ok, refusal_ok, control_ok)',
     '    arms = carrier_arms(detected, before_ok, identity_ok, recovery_ok, refusal_ok, True)'),
]

# --- r68 gate-strength probe (report-only): the local at line 277 is a dead store
R68_EXTRA = [
    ("X7_r68_dead_control_store", None,
     '            control_ok = ctrl_l["rc"] != 0 and ctrl_d["rc"] != 0',
     '            control_ok = True'),
]

TABLES = {
    ("r69", "constant"): R69_CONSTANT,
    ("r69", "literal"): R69_LITERAL,
    ("r68", "constant"): R68_CONSTANT,
    ("r68", "literal"): R68_LITERAL,
    ("r69", "extra"): R69_EXTRA,
    ("r68", "extra"): R68_EXTRA,
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_selftest(path: str) -> dict:
    proc = subprocess.run([sys.executable, "-I", "-B", path, "--selftest"],
                          capture_output=True, text=True, timeout=300)
    payload = None
    for text in (proc.stdout, proc.stderr):
        if not text.strip():
            continue
        try:
            cand = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(cand, dict) and "cases" in cand:
            payload = cand
            break
    return {"rc": proc.returncode,
            "cases": (payload or {}).get("cases"),
            "failed": (payload or {}).get("failed"),
            "ok": (payload or {}).get("ok"),
            "parsed": payload is not None,
            "stderr_tail": proc.stderr[-300:]}


def classify(result: dict, expect_case: str | None) -> str:
    """ExecC1's own verdict rule (spelled out, not inherited)."""
    if result["rc"] == 0 and result["ok"] is True:
        return "survived"
    if result["failed"] is None:
        # no parsed payload: syntax/import error, not a gate hit
        return "unevaluable_no_payload"
    if expect_case is not None and expect_case in result["failed"]:
        return "killed_named"
    return "killed_other_cases"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--blob", required=True)
    ap.add_argument("--family", required=True, choices=["constant", "literal", "extra"])
    ap.add_argument("--target", required=True, choices=["r68", "r69"])
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--json-out", required=True)
    args = ap.parse_args(argv)

    blob = os.path.abspath(args.blob)
    data = open(blob, "rb").read()
    text = data.decode("utf-8")
    os.makedirs(args.outdir, exist_ok=True)
    pristine = os.path.join(args.outdir, "pristine-" + os.path.basename(blob))
    with open(pristine, "wb") as fh:
        fh.write(data)
    base = run_selftest(pristine)

    rows = []
    for mid, expect_case, old, new in TABLES[(args.target, args.family)]:
        hits = text.count(old)
        row = {"id": mid, "expect_case": expect_case,
               "old": old, "new": new, "site_matches": hits}
        if hits != 1:
            row["verdict"] = "patch_site_%d_matches" % hits
            rows.append(row)
            continue
        mutant_text = text.replace(old, new, 1)
        mpath = os.path.join(args.outdir, f"{args.family}-{mid}-{os.path.basename(blob)}")
        with open(mpath, "w", encoding="utf-8") as fh:
            fh.write(mutant_text)
        mbytes = mutant_text.encode("utf-8")
        res = run_selftest(mpath)
        row.update({"path": os.path.basename(mpath),
                    "sha256": sha256_bytes(mbytes),
                    "differs_from_pristine": mbytes != data,
                    "rc": res["rc"], "cases": res["cases"],
                    "failed": res["failed"], "ok": res["ok"],
                    "stderr_tail": res["stderr_tail"],
                    "verdict": classify(res, expect_case)})
        rows.append(row)

    survivors = [r["id"] for r in rows if r.get("verdict") == "survived"]
    killed_named = [r["id"] for r in rows if r.get("verdict") == "killed_named"]
    wrong = [r["id"] for r in rows
             if r.get("verdict") in ("killed_other_cases", "unevaluable_no_payload")
             or str(r.get("verdict", "")).startswith("patch_site_")]
    receipt = {"applier": "ExecC1/mutapply.py", "target": args.target,
               "family": args.family, "blob": blob,
               "blob_sha256": sha256_bytes(data),
               "pristine": base,
               "mutants": rows, "survivors": survivors,
               "killed_named": killed_named, "wrong_or_unevaluable": wrong}
    with open(args.json_out, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps({k: receipt[k] for k in
                      ("target", "family", "blob_sha256", "pristine",
                       "survivors", "killed_named", "wrong_or_unevaluable")},
                     indent=1, sort_keys=True))
    return 0 if not survivors and not wrong else 1


if __name__ == "__main__":
    sys.exit(main())
