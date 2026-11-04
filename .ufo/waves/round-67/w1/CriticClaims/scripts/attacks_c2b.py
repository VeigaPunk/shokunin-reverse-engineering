#!/usr/bin/env python3
"""Attack C (corrected shape) and the D correction demo."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
S = Path("/fast/scratch/hyaku/kaidoku-r67/CriticClaims")
OUT = S / "o"
CLOSURE = REPO / "tools/round-66/closure-boundary.py"
COVERAGE = REPO / "tools/round-66/coverage-selfcheck.py"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_battery(tag, closure=None, coverage=None):
    out = OUT / ("battery-%s.json" % tag)
    args = [sys.executable, "-I", "-B",
            str(REPO / "tools/round-67/mutation-battery.py"),
            "--selftest", "--root", str(REPO), "--out", str(out),
            "--work", str(OUT / ("bw-" + tag))]
    if closure:
        args += ["--closure", str(closure)]
    if coverage:
        args += ["--coverage", str(coverage)]
    env = {"PATH": "/usr/bin:/bin:/home/vgpnk/.local/bin",
           "HOME": "/home/vgpnk", "TMPDIR": str(OUT / ("bt-" + tag))}
    p = subprocess.run(args, capture_output=True, text=True, env=env, timeout=900)
    doc = json.loads(out.read_text()) if out.is_file() else {"cases": []}
    return {"rc": p.returncode,
            "summary": (p.stdout.splitlines() or [""])[-1],
            "failed_cases": [c["case"] for c in doc.get("cases") or [] if not c["ok"]],
            "cases": {c["case"]: {"ok": c["ok"], "got": c["got"], "want": c["want"]}
                      for c in doc.get("cases") or []}}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    bat = load(REPO / "tools/round-67/mutation-battery.py", "bat")
    doc = {"battery_sha256": bat.sha256_file(
        REPO / "tools/round-67/mutation-battery.py")}

    # C: a mutant failing the OTHER arm bound (an unrelated case for the
    # always-True survivor whose EXPECTED_CASE is arm-false-bound).
    text = CLOSURE.read_text()
    needle = '"passed": bool(passed)'
    assert text.count(needle) == 1
    mdir = OUT / "mutants" / "arm-always-false" / "tools" / "round-66"
    mdir.mkdir(parents=True, exist_ok=True)
    mpath = mdir / "closure-boundary.py"
    mpath.write_text(text.replace(needle, '"passed": False'))
    c = run_battery("arm-false", closure=mpath)
    expected = bat.EXPECTED_CASE["closure-arm-true"]
    doc["C"] = {
        "attack": "C false-kill: an unrelated failing case",
        "clause_attacked": "kills both survivors (killed_after definition)",
        "mutant": 'arm() returns "passed": False for every input',
        "battery_rc": c["rc"], "summary": c["summary"],
        "failed_cases": c["failed_cases"],
        "cases": c["cases"],
        "expected_case": expected,
        "killed_after_by_shipped_formula": bool(
            c["rc"] != 0 and expected in c["failed_cases"]),
        "verdict": ("no false kill: rc=1 and the mutant is NOT reported killed, "
                    "because the failing case is arm-true-bound, not the named "
                    "EXPECTED_CASE. Two different mutants, two different cases."),
        "limit": ("the same guard means the battery's kill verdict is one-case "
                  "wide per survivor; a mutant that breaks the other bound is "
                  "invisible to the verdict"),
    }

    # D correction: a no-run mutant keyed on text COMMON to both fixtures is
    # killed, which is the detector the current text-doctored fixture lacks.
    cov = COVERAGE.read_text()
    start = '    path = scratch / "recipe-a-verbatim.py"'
    end = '            "recipe_a": ours}'
    common = '''    if '"mapped"' in script:
        return {"recipe_a_equivalent": True, "recipe_a_diffs": {},
                "recipe_a_block_sha256": sha256_text(script),
                "recipe_a_block_keys": sorted(RECIPE_A_KEYS),
                "recipe_a": ours}
    return {"recipe_a_equivalent": False, "recipe_a_diffs": {"x": {}},
            "recipe_a_block_sha256": sha256_text(script),
            "recipe_a_block_keys": sorted(RECIPE_A_KEYS),
            "recipe_a": ours}'''
    cdir = OUT / "mutants" / "textguess-common" / "tools" / "round-66"
    cdir.mkdir(parents=True, exist_ok=True)
    cfile = cdir / "coverage-selfcheck.py"
    cfile.write_text(bat.replace_span(cov, start, end, common))
    d = run_battery("textguess-common", coverage=cfile)
    exp2 = bat.EXPECTED_CASE["coverage-equiv-true"]
    doc["D_correction"] = {
        "purpose": ("a no-run mutant keyed on text shared by both fixtures "
                    "returns one answer for both and is killed: the battery "
                    "separates 'inspects the text' from 'runs the block' only "
                    "when the two fixtures' block text is identical"),
        "mutant": "returns equivalent iff '\"mapped\"' appears in the block text",
        "battery_rc": d["rc"], "summary": d["summary"],
        "failed_cases": d["failed_cases"],
        "killed_by": bool(d["rc"] != 0 and exp2 in d["failed_cases"]),
        "implication": ("the shipped doctored fixture differs from the honest "
                        "one only in the block TEXT ('\"mapped\": 0' vs 1, "
                        "coverage_score 0.0 vs 10.0), so a text-reading mutant "
                        "can reproduce both answers without executing"),
    }
    (OUT / "attack-C2-corrected.json").write_text(
        json.dumps(doc, indent=1, sort_keys=True) + "\n")
    print(json.dumps(doc, indent=1, sort_keys=True)[:4000])


if __name__ == "__main__":
    sys.exit(main())
