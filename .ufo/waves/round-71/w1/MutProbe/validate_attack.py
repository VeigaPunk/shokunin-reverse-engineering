"""MutProbe-2 validate-layer attacks on the FROZEN seam-probe.py and
forged-receipts.py (scratch copies, sha-verified) plus bind_producer probes.

Seam receipts: ten-true-arms/empty-observations, arms_passed contradiction,
failed-list contradiction, filler-observation false-green, fabricated/duplicate
arm ids, broken JSON.
Battery receipts: lying rc pair (0,0), five lying rows, genuine block missing,
base shapes with clause_found False (false-green probe), lying rows with
clause_found False (asymmetry evidence), rc pair (0,0) on a base shape.
"""
import importlib.util
import json
import os
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
SEAM = os.path.join(S, "seam-probe.py")
FRG = os.path.join(S, "forged-receipts.py")
RCPT = os.path.join(S, "receipts")
os.makedirs(RCPT, exist_ok=True)
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "b827a8b5d54f2885ec9be7786389f356c59226ce"
R71_PACKED_SHA = "5cf95aaa0892c4e4f1b82edb60590b57e6667467ed607b15989bb867e7d8efe0"
R70_LANDING = "7c155617bb42dadf1725b88a06fe3f235c364f0a"
R70_LANDING_SHA = "417b116803fbf78b44220d4a2caeb30d1261030353bc1b1c81d22c3b0146048a"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_cli(tool, path):
    proc = subprocess.run([sys.executable, "-I", "-B", tool, "--validate", path],
                          capture_output=True, text=True)
    payload = None
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        pass
    return {"exit": proc.returncode, "payload": payload,
            "stderr_tail": proc.stderr.strip()[-200:]}


def write(name, obj):
    path = os.path.join(RCPT, name)
    with open(path, "w") as fh:
        if isinstance(obj, str):
            fh.write(obj)
        else:
            json.dump(obj, fh)
    return path


results = {"seam": [], "battery": [], "bind_producer": []}

# ---- seam-probe --validate ----
IDS = ["A%d" % i for i in range(1, 11)]


def seam_receipt(ids, flags, passed=None, failed=None, obs=None):
    o = {"x": 1} if obs is None else obs
    arms = [{"id": i, "ok": f, "observed": dict(o)} for i, f in zip(ids, flags)]
    if passed is None:
        passed = sum(1 for f in flags if f)
    if failed is None:
        failed = [i for i, f in zip(ids, flags) if not f]
    return {"arms": arms, "arms_passed": passed, "target": len(ids), "failed": failed}


SEAM_CASES = {
    "V1_ten-true-empty-observations": seam_receipt(IDS, [True] * 10, obs={}),
    "V2_arms-passed-contradicts": seam_receipt(IDS, [True] * 10, passed=8),
    "V3_failed-contradicts": seam_receipt(IDS, [True] * 9 + [False], failed=[]),
    "V4_filler-observations": seam_receipt(IDS, [True] * 10, obs={"x": 1}),
    "V5_fabricated-arm-id": seam_receipt(IDS[:9] + ["X1_fabricated"], [True] * 10),
    "V6_duplicate-arm-ids": seam_receipt(["A1"] * 10, [True] * 10),
    "V7_broken-json": "{not json",
    "V8_empty-arms": seam_receipt([], []),
}
for name, rec in SEAM_CASES.items():
    path = write("seam-%s.json" % name, rec)
    out = run_cli(SEAM, path)
    results["seam"].append({"case": name, **out})

# ---- forged-receipts --validate ----
SHAPES = [("F%d_%s" % (i, n), c) for i, (n, c) in enumerate([
    ("wrong-rev", "rev"), ("wrong-instrument", "instrument.sha256"),
    ("relabelled-source", "source"), ("ratio-underived", "before_ceiling_ratio"),
    ("inflated-orig", "orig_procedures"), ("before-over-limit", "packed"),
    ("rows-vs-matched", "carrier rows"), ("dropped-arm", "arm identity_ok missing"),
    ("unknown-carrier", "unknown carrier id"), ("absent-instrument", "instrument absent")], 1)]


def shape_row(shape, clause, clause_found=True, base_rc=0, landing_rc=1):
    return {"shape": shape, "declared_clause": clause, "receipt": "/nonread",
            "base_rc": base_rc, "base_met": True, "landing_rc": landing_rc,
            "landing_failing": [clause] if clause_found else [],
            "clause_found": clause_found}


def lying_row(shape, clause, fc=0, sp=1, clause_found=True):
    return {"shape": shape, "declared_clause": clause, "receipt": "/nonread",
            "first_cut_rc": fc, "first_cut_met": True, "superseded_rc": sp,
            "superseded_failing": [clause] if clause_found else [],
            "clause_found": clause_found}


LYING = [("L1_unpacked-counts", "unpacked_counts"),
         ("L2_packed-sha", "packed_sha256"),
         ("L3_section-list", "section_count"),
         ("L4_runs-argv", "runs.pack.argv"),
         ("L5_refusal", "refusal"),
         ("L6_format", "format")]

valid_shapes = [shape_row(s, c) for s, c in SHAPES]
genuine = {"checker_rc": 0, "met": True, "probe_rc": 0, "probe_arms_passed": 6,
           "probe_target": 6}

BATTERY_CASES = {
    "B1_lying-rc-pair-0-0": {
        "shapes": valid_shapes,
        "lying_shapes": [lying_row(s, c, fc=0, sp=0) for s, c in LYING],
        "genuine": genuine},
    "B2_five-lying-rows": {
        "shapes": valid_shapes,
        "lying_shapes": [lying_row(s, c) for s, c in LYING[:5]],
        "genuine": genuine},
    "B3_genuine-block-missing": {"shapes": valid_shapes},
    "B4_base-shapes-clause-not-found": {
        "shapes": [shape_row(s, c, clause_found=False) for s, c in SHAPES],
        "genuine": genuine},
    "B5_lying-clause-not-found": {
        "shapes": valid_shapes,
        "lying_shapes": [lying_row(s, c, clause_found=False) for s, c in LYING],
        "genuine": genuine},
    "B6_base-shape-rc-0-0": {
        "shapes": [shape_row(s, c, base_rc=0, landing_rc=0, clause_found=False)
                   for s, c in SHAPES],
        "genuine": genuine},
}
for name, rec in BATTERY_CASES.items():
    path = write("battery-%s.json" % name, rec)
    out = run_cli(FRG, path)
    results["battery"].append({"case": name, **out})

# ---- bind_producer probes (module-level, no subprocess) ----
seam = load(SEAM, "seam_mod_bp")
blob_path = write("bp-blob-marker.txt", "marker")  # placeholder, not used by bind
genuine_receipt = {"rev": FREEZE,
                   "instrument": {"path": "tools/round-71/packed-elf.py",
                                  "sha256": R71_PACKED_SHA}}
transplanted = {"rev": R70_LANDING,
                "instrument": {"path": "tools/round-70/packed-elf.py",
                               "sha256": R70_LANDING_SHA}}
for label, rec in (("genuine-round71", genuine_receipt),
                   ("transplanted-round70", transplanted)):
    p = write("bp-%s.json" % label, rec)
    _, defects = seam.bind_producer(p, LANE, FREEZE, "tools/round-71/packed-elf.py",
                                    R71_PACKED_SHA)
    results["bind_producer"].append({"case": label, "defects": defects})

with open(os.path.join(S, "validate-results.json"), "w") as fh:
    json.dump(results, fh, indent=1)
print(json.dumps(results, indent=1))
