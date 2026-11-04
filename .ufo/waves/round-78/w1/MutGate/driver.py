#!/usr/bin/env python3
"""MutGate mutation driver v2 — targets the CURRENT lane instrument (961d5a23),
after the external advance past the first snapshot (a86f6d4d).

Same eight single-point mutations; every run re-taken: selftest + battery at
the pinned rev, detector diff against the v2 pristine baseline.
"""
import hashlib
import json
import pathlib
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = sys.argv[1] if len(sys.argv) > 1 else \
    "c9d986eb1531c43a5b95fd0bf327d048c201e6b5"
SCRATCH = pathlib.Path("/fast/scratch/hyaku/kaidoku-r78/MutGate")
PRISTINE = SCRATCH / "pristine-v2" / "attack-gate.py"
MUTDIR = SCRATCH / "mut-v2"
OUT = SCRATCH / "out-v2"
WORK = SCRATCH / "work-v2"

src = PRISTINE.read_text()
PRISTINE_SHA = hashlib.sha256(PRISTINE.read_bytes()).hexdigest()

MUTANTS = [
    ("m01-auth-findings-noop",
     '    """A receipt is admitted only when its own instrument pin re-derives."""\n'
     '    out: list[dict] = []',
     '    """A receipt is admitted only when its own instrument pin re-derives."""\n'
     '    return []\n    out: list[dict] = []',
     "receipt-unauth",
     "(a) auth_findings returns [] unconditionally (early return before the body)"),
    ("m02-qualified-atom-re-dead",
     'QUALIFIED_ATOM_RE = re.compile(r"^[A-Z][0-9][0-9A-Za-z_]*:")',
     'QUALIFIED_ATOM_RE = re.compile(r"(?!)")',
     "qualified-atom",
     "(b) QUALIFIED_ATOM_RE matches nothing (never-matching negative lookahead)"),
    ("m03-near-miss-re-dead",
     '    r"^(?:mismatch|survivor|atom|pristine|validate|match|matches)\\s+\\S+$")',
     '    r"(?!)")',
     "near-miss-field",
     "(c) NEAR_MISS_RE matches nothing (never-matching negative lookahead)"),
    ("m04-negation-re-dead",
     'NEGATION_RE = re.compile(r"\\b(not|no|none|never|neither)\\b", re.IGNORECASE)',
     'NEGATION_RE = re.compile(r"(?!)")',
     "negated-verdict",
     "(d) NEGATION_RE matches nothing (never-matching negative lookahead)"),
    ("m05-defect-as-bound-pass",
     '                return False, "defect", {"reason": "no_atoms", "field": field}',
     '                return True, "bound", {"reason": "no_atoms", "field": field}',
     "dropped-defect",
     "(e) bind_clause atom-branch defect (no_atoms) returned as (True, 'bound')"),
    ("m06-clean-run-accepts-fail",
     '        elif filing["exit"] != 0 or not filing["passed"]:',
     '        elif False:',
     "unclean-clone-run",
     "(f) judge_receipt_fixture clean_run no longer rejects a failed retained run"),
    ("m07-filing-rev-no-ancestor",
     '        if not is_hex(filing["rev"], 40) or not is_ancestor(root, filing["rev"], rev):',
     '        if not is_hex(filing["rev"], 40):',
     "stale-filing-rev",
     "(g) filing_rev drops the is_ancestor check (keeps only the 40-hex shape)"),
    ("m08-validate-no-refusal-guard",
     '        if fixture.get("refused") and not fixture.get("reasons"):\n'
     '            defects.append(f"{fixture.get(\'id\')}: refused without a reason")',
     '        # mutant m08: the refused-without-reason guard is skipped',
     None,
     "(h) validate_receipt skips the refused-without-reason guard"),
]


def run(argv):
    return subprocess.run(argv, capture_output=True, text=True, cwd=str(SCRATCH))


def selftest(path):
    proc = run([sys.executable, "-I", "-B", str(path), "--selftest"])
    failing, total = [], 0
    for line in proc.stdout.splitlines():
        try:
            d = json.loads(line)
        except Exception:
            continue
        if isinstance(d, dict) and "case" in d:
            total += 1
            if d.get("pass") is False:
                failing.append(d["case"])
    return proc.returncode, failing, total, proc.stderr[-300:]


def battery(path, mid):
    out = OUT / f"{mid}-battery.json"
    proc = run([sys.executable, "-I", "-B", str(path), "--root", LANE,
                "--rev", REV, "--work", str(WORK / mid), "--battery",
                "--json-out", str(out)])
    try:
        return proc.returncode, json.loads(out.read_text()), proc.stderr[-300:]
    except Exception as exc:
        return proc.returncode, None, f"{exc}: {proc.stderr[-300:]}"


st_exit, st_failed, st_total, st_err = selftest(PRISTINE)
b_exit, b_receipt, b_err = battery(PRISTINE, "pristine-v2")
results = []
baseline = {
    "pristine_sha256": PRISTINE_SHA,
    "selftest_exit": st_exit,
    "selftest_cases": st_total,
    "selftest_failed_cases": st_failed,
    "battery_exit": b_exit,
    "battery": None,
}
if b_receipt is not None:
    baseline["battery"] = {
        "fixtures_total": b_receipt["fixtures_total"],
        "base_accepted": b_receipt["base_accepted"],
        "refused": b_receipt["refused"],
        "ok": b_receipt["ok"],
        "genuine": {"mismatch_count": b_receipt["genuine"]["mismatch_count"],
                    "defects": b_receipt["genuine"]["defects"][:6],
                    "population_floor": b_receipt["genuine"].get("population_floor")},
        "validate": b_receipt["validate"],
        "per_fixture": [
            {"id": f["id"], "refused": f["refused"],
             "rules": sorted({x.get("rule") for x in f["reasons"]}),
             "base_accepted": (f.get("base") or {}).get("accepted")}
            for f in b_receipt["fixtures"]],
    }

for mid, old, new, declared, edit in MUTANTS:
    count = src.count(old)
    if count != 1:
        results.append({"id": mid, "verdict": "driver-error",
                        "error": f"old-string count {count} != 1"})
        continue
    mpath = MUTDIR / f"{mid}.py"
    mpath.write_text(src.replace(old, new, 1))
    msha = hashlib.sha256(mpath.read_bytes()).hexdigest()

    st_exit_m, st_failed_m, st_total_m, st_err_m = selftest(mpath)
    b_exit_m, receipt, b_err_m = battery(mpath, mid)

    entry = {
        "id": mid,
        "task_label": edit.split(" ")[0],
        "edit": edit,
        "declared_detector": f"fixture:{declared}" if declared else None,
        "mutant_sha256": msha,
        "selftest_exit": st_exit_m,
        "selftest_cases": st_total_m,
        "selftest_failed_cases": st_failed_m,
        "battery_exit": b_exit_m,
        "battery_stderr_tail": b_err_m,
    }
    if receipt is None:
        entry["verdict"] = "inconclusive"
        entry["note"] = "battery produced no receipt"
        results.append(entry)
        continue

    lost, wrong = [], []
    for f in receipt["fixtures"]:
        if not f["refused"]:
            lost.append(f["id"])
        else:
            rules = {x.get("rule") for x in f["reasons"]}
            if f["rule"] not in rules:
                wrong.append({"id": f["id"], "fired": sorted(rules)})
    base_fail = [f["id"] for f in receipt["fixtures"]
                 if not (f.get("base") or {}).get("accepted")]
    gen_mm = receipt["genuine"]["mismatch_count"]
    gen_def = receipt["genuine"]["defects"]
    floor = receipt["genuine"].get("population_floor")
    val_def = receipt["validate"]["defects"]

    detectors = []
    detectors += [f"fixture:{i}" for i in lost]
    detectors += [f"fixture:{w['id']}:wrong-rule" for w in wrong]
    if gen_mm or gen_def:
        detectors.append("genuine-scan")
    if val_def:
        detectors.append("validate")
    detectors += [f"selftest:{c}" for c in st_failed_m]

    entry.update({
        "base_arm_failures": base_fail,
        "fixtures_lost_refusal": lost,
        "fixtures_wrong_rule": wrong,
        "genuine_mismatch_count": gen_mm,
        "genuine_defects": gen_def[:6],
        "population_floor": floor,
        "validate_defects": val_def[:6],
        "detectors_failed": detectors,
        "killed_by": detectors[0] if detectors else None,
        "killed": bool(detectors),
        "sole": detectors == ([f"fixture:{declared}"] if declared else []),
        "survivor": not detectors,
        "verdict": ("inconclusive" if base_fail else
                    ("survivor" if not detectors else "killed")),
    })
    results.append(entry)

summary = {
    "schema": "kaidoku-r78-mutgate-v2",
    "target": "tools/round-78/attack-gate.py",
    "target_sha256": PRISTINE_SHA,
    "measured_rev": REV,
    "baseline": baseline,
    "mutants": results,
    "survivors": [r["id"] for r in results if r.get("survivor")],
    "inconclusive": [r["id"] for r in results if r.get("verdict") == "inconclusive"],
}
(OUT / "mutation-receipt-v2.json").write_text(
    json.dumps(summary, indent=1, sort_keys=True) + "\n")
print(json.dumps({k: v for k, v in baseline.items() if k != "battery"}, sort_keys=True))
if baseline["battery"]:
    print("BASELINE", json.dumps({k: baseline["battery"][k] for k in
                                  ("fixtures_total", "base_accepted", "refused",
                                   "ok", "genuine", "validate")}, sort_keys=True))
for r in results:
    print(json.dumps({k: r.get(k) for k in
                      ("id", "verdict", "killed_by", "sole", "survivor",
                       "detectors_failed", "base_arm_failures")},
                     sort_keys=True))
print("SURVIVORS", summary["survivors"])
print("INCONCLUSIVE", summary["inconclusive"])
