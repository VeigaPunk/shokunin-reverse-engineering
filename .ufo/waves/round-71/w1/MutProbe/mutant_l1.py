"""MutProbe-2 mutant probe M-L1: a superseded reader weakened to ignore
unpacked_counts. Replays the frozen battery's L1 arm verbatim
(forge_lying/write_lying_shape come from the frozen forged-receipts.py copy,
sha 50bb190b...) against the first-cut reader (must accept), the pristine
superseded reader 7c155617 (must reject naming the clause), and the mutant
(expected: no longer catches the lie -> the battery's L1 row fails).
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
LANDING_MATERIAL = os.path.join(LANE, ".ufo/waves/round-70/l1/scores/c3-at-landing.json")
FIRST_CUT_REV = "4737a542ae3b1b910d8fe43efbd572bc578b07c6"
FIRST_CUT_TOOL = "tools/round-70/packed-elf.py"
PRISTINE = os.path.join(S, "superseded-reader-7c155617.py")
MUTANT = os.path.join(S, "mutant", "mutant-reader.py")
FIRST_CUT = os.path.join(S, "first-cut-reader-4737a542.py")


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


frg = load(os.path.join(S, "forged-receipts.py"), "frg_mut")


def json_out(text):
    return frg.json_out(text)


def run_reader(reader, shape_path, rev):
    proc = subprocess.run(
        [sys.executable, "-I", "-B", reader, "--check-receipt", shape_path,
         "--root", LANE, "--rev", rev],
        capture_output=True, text=True, timeout=900)
    payload = json_out(proc.stdout) or {}
    return {"rc": proc.returncode, "met": payload.get("met"),
            "failing": (payload.get("failing") or [])[:6]}


first_cut_sha = sha(FIRST_CUT)
with open(LANDING_MATERIAL, encoding="utf-8") as fh:
    lmat = json.load(fh)

shape_dir = os.path.join(S, "mutant", "L1_unpacked-counts")
shape_path = frg.write_lying_shape(shape_dir, "L1_unpacked-counts", lmat,
                                   FIRST_CUT_REV, first_cut_sha)

first_cut_res = run_reader(FIRST_CUT, shape_path, FIRST_CUT_REV)
pristine_res = run_reader(PRISTINE, shape_path, FIRST_CUT_REV)
mutant_res = run_reader(MUTANT, shape_path, FIRST_CUT_REV)


def battery_row_ok(fc, sp):
    """The frozen battery's L1 row acceptance (forged-receipts.py check()):
    first_cut_rc 0 and first_cut_met true; superseded_rc 1 and clause found."""
    fc_ok = fc["rc"] == 0 and fc["met"] is True
    sp_ok = sp["rc"] == 1 and any("unpacked_counts" in str(f) for f in sp["failing"])
    return fc_ok and sp_ok


row_pristine = battery_row_ok(first_cut_res, pristine_res)
row_mutant = battery_row_ok(first_cut_res, mutant_res)

out = {
    "mutant": "M-L1 superseded reader ignores unpacked_counts (clause lines 509-511 removed)",
    "pristine_reader_sha256": sha(PRISTINE),
    "mutant_reader_sha256": sha(MUTANT),
    "first_cut_reader_sha256": first_cut_sha,
    "shape_path": shape_path,
    "first_cut_run": first_cut_res,
    "pristine_superseded_run": pristine_res,
    "mutant_superseded_run": mutant_res,
    "battery_L1_row_with_pristine_reader": row_pristine,
    "battery_L1_row_with_mutant_reader": row_mutant,
    "verdict": ("KILLED - the counter catches the weakened reader: the L1 row "
                "fails under the mutant (superseded_rc %s, clause_found %s)"
                % (mutant_res["rc"],
                   any("unpacked_counts" in str(f) for f in mutant_res["failing"])))
               if (row_pristine and not row_mutant)
               else ("INCONCLUSIVE - baseline row_pristine=%s row_mutant=%s"
                     % (row_pristine, row_mutant)),
}
with open(os.path.join(S, "mutant", "mutant-l1-results.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print(json.dumps(out, indent=1))
