#!/usr/bin/env python3
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[7]
ARTIFACT = pathlib.Path(__file__).resolve().parent
SOURCE_GATE = REPO / ".ufo/gates/c1-census-v10.py"
PATCH = ARTIFACT / "g21-frontier-coverage.patch"
DOCS = ("PROVINCE.md", "SKILL.md", "SCORECARD.md")


def copy_inputs(destination):
    destination.mkdir(parents=True)
    for name in DOCS:
        shutil.copy2(REPO / name, destination / name)


def run_gate(name, gate, root):
    command = [sys.executable, str(gate), "--root", str(root), "--json"]
    result = subprocess.run(command, cwd=REPO, text=True, capture_output=True)
    try:
        parsed = json.loads(result.stdout)
    except json.JSONDecodeError:
        parsed = None
    return {
        "command": command,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "parsed": parsed,
    }


scratch = pathlib.Path(tempfile.mkdtemp(prefix="kaidoku-rv1-g21-", dir="/var/tmp"))
original = {}
for name in ("source-baseline", "source-seeded", "candidate-baseline", "candidate-seeded"):
    root = scratch / name
    copy_inputs(root)
    original[name] = root

seed_line = len((original["source-seeded"] / "PROVINCE.md").read_text().splitlines()) + 1
with (original["source-seeded"] / "PROVINCE.md").open("a", encoding="utf-8") as stream:
    stream.write("- **RV-1 synthetic unregistered frontier** — seeded G21 boundary fault.\n")

patch_root = scratch / "candidate-instrument"
(patch_root / ".ufo/gates").mkdir(parents=True)
candidate_gate = patch_root / ".ufo/gates/c1-census-v10.py"
shutil.copy2(SOURCE_GATE, candidate_gate)
patch_result = subprocess.run(
    ["patch", "--batch", "-p1", "-i", str(PATCH)],
    cwd=patch_root,
    text=True,
    capture_output=True,
)
if patch_result.returncode != 0:
    raise SystemExit("scratch patch failed: " + patch_result.stdout + patch_result.stderr)

for name in ("candidate-baseline", "candidate-seeded"):
    shutil.copy2(original["source-baseline"] / "PROVINCE.md", original[name] / "PROVINCE.md")
if seed_line:
    with (original["candidate-seeded"] / "PROVINCE.md").open("a", encoding="utf-8") as stream:
        stream.write("- **RV-1 synthetic unregistered frontier** — seeded G21 boundary fault.\n")

results = {
    "scratch_root": str(scratch),
    "seeded_bullet_line": seed_line,
    "patch_command": ["patch", "--batch", "-p1", "-i", str(PATCH)],
    "patch_stdout": patch_result.stdout,
    "patch_stderr": patch_result.stderr,
    "cases": {
        "source_baseline": run_gate("source_baseline", SOURCE_GATE, original["source-baseline"]),
        "source_seeded": run_gate("source_seeded", SOURCE_GATE, original["source-seeded"]),
        "candidate_baseline": run_gate("candidate_baseline", candidate_gate, original["candidate-baseline"]),
        "candidate_seeded": run_gate("candidate_seeded", candidate_gate, original["candidate-seeded"]),
    },
}

checks = {
    "source_baseline_passes": results["cases"]["source_baseline"]["exit_code"] == 0
        and results["cases"]["source_baseline"]["parsed"]["verdict"] == "PASS",
    "source_seeded_passes_silently": results["cases"]["source_seeded"]["exit_code"] == 0
        and results["cases"]["source_seeded"]["parsed"]["verdict"] == "PASS"
        and results["cases"]["source_seeded"]["parsed"]["frontier_errors"] == [],
    "candidate_baseline_passes": results["cases"]["candidate_baseline"]["exit_code"] == 0
        and results["cases"]["candidate_baseline"]["parsed"]["verdict"] == "PASS",
    "candidate_seeded_flags_unregistered_bullet": results["cases"]["candidate_seeded"]["exit_code"] == 1
        and results["cases"]["candidate_seeded"]["parsed"]["verdict"] == "FAIL"
        and results["cases"]["candidate_seeded"]["parsed"]["frontier_errors"]
        == ["PROVINCE.md:%d unregistered Frontier bullet (FRONTIER-UNEVALUABLE)" % seed_line]
        and "FRONTIER-UNEVALUABLE"
        in results["cases"]["candidate_seeded"]["parsed"]["declared_fail_classes"],
}
results["checks"] = checks
(ARTIFACT / "g21-seeded-measurement.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)
summary = {
    "scratch_root": str(scratch),
    "seeded_bullet_line": seed_line,
    "checks": checks,
    "cases": {
        name: {
            "exit_code": case["exit_code"],
            "verdict": case["parsed"]["verdict"] if case["parsed"] else None,
            "frontier_errors": case["parsed"]["frontier_errors"] if case["parsed"] else None,
            "declared_fail_classes": case["parsed"]["declared_fail_classes"] if case["parsed"] else None,
        }
        for name, case in results["cases"].items()
    },
}
print(json.dumps(summary, indent=2, ensure_ascii=False))
if not all(checks.values()):
    raise SystemExit(1)
