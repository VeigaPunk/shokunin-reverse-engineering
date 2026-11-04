#!/usr/bin/env python3
"""ExecC2: run both frozen readers over the six self-cut forgeries + honest control."""
import json
import os
import subprocess
import sys

SCRATCH = os.path.dirname(os.path.abspath(__file__))
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FIRST_CUT_REV = "4737a542ae3b1b910d8fe43efbd572bc578b07c6"
LYING = os.path.join(SCRATCH, "lying")
FINDINGS = ("/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
            "/.ufo/waves/round-71/w1/ExecC2")
FIRST_CUT_READER = os.path.join(SCRATCH, "first-cut-packed-elf.py")
SUPERSEDED_READER = os.path.join(SCRATCH, "superseded-packed-elf.py")

DECLARED = {
    "L1_unpacked-counts": ["unpacked_counts"],
    "L2_packed-sha": ["packed_sha256"],
    "L3_section-list": ["section_count", "upx_list_rc"],
    "L4_runs-argv": ["runs.pack.argv"],
    "L5_refusal": ["refusal"],
    "L6_format": ["format"],
}


def run_reader(reader: str, receipt: str) -> dict:
    proc = subprocess.run(
        [sys.executable, "-I", "-B", reader, "--check-receipt", receipt,
         "--root", ROOT, "--rev", FIRST_CUT_REV],
        capture_output=True, text=True)
    parsed = None
    try:
        start = proc.stdout.index("{")
        parsed = json.loads(proc.stdout[start:])
    except (ValueError, json.JSONDecodeError):
        pass
    return {"rc": proc.returncode, "met": (parsed or {}).get("met"),
            "failing": (parsed or {}).get("failing"),
            "stderr_tail": proc.stderr[-300:] if proc.returncode == 2 else ""}


def main() -> int:
    rows = []
    for shape, clauses in DECLARED.items():
        receipt = os.path.join(LYING, f"{shape}.json")
        fc = run_reader(FIRST_CUT_READER, receipt)
        sp = run_reader(SUPERSEDED_READER, receipt)
        flat = " | ".join(str(f) for f in (sp.get("failing") or []))
        found = {c: (c in flat) for c in clauses}
        ok = fc["rc"] == 0 and sp["rc"] == 1 and all(found.values())
        rows.append({"shape": shape, "receipt": receipt,
                     "declared_clauses": clauses,
                     "first_cut_rc": fc["rc"], "first_cut_met": fc["met"],
                     "superseded_rc": sp["rc"],
                     "superseded_failing": (sp.get("failing") or [])[:8],
                     "clause_found": found, "row_ok": ok})
        print(f"{shape}: fc_rc={fc['rc']} sp_rc={sp['rc']} clauses={found} ok={ok}")
        if not ok:
            print("  fc failing:", (fc.get("failing") or [])[:4])
            print("  sp failing:", (sp.get("failing") or [])[:6])
    honest = os.path.join(LYING, "honest-relabel.json")
    fc = run_reader(FIRST_CUT_READER, honest)
    sp = run_reader(SUPERSEDED_READER, honest)
    control = {"honest_first_cut_rc": fc["rc"], "honest_first_cut_met": fc["met"],
               "honest_first_cut_failing": (fc.get("failing") or [])[:6],
               "honest_superseded_rc": sp["rc"], "honest_superseded_met": sp["met"],
               "honest_superseded_failing": (sp.get("failing") or [])[:6]}
    print("honest control:", json.dumps(control, sort_keys=True))
    out = {"schema": "kaidoku-r71-w1-execc2-lying-v1", "first_cut_rev": FIRST_CUT_REV,
           "rows": rows, "honest_control": control,
           "all_ok": all(r["row_ok"] for r in rows)}
    os.makedirs(FINDINGS, exist_ok=True)
    with open(os.path.join(FINDINGS, "lying-rederive.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("all_ok =", out["all_ok"])
    return 0 if out["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
