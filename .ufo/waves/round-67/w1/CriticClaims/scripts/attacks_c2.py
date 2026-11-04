#!/usr/bin/env python3
"""Critic attacks C and D on R67-C2.  Uses the shipped battery (selftest with
--closure/--coverage over hand-built mutants) and the shipped r66 counters."""
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
S = Path("/fast/scratch/hyaku/kaidoku-r67/CriticClaims")
OUT = S / "o"
CLOSURE = REPO / "tools/round-66/closure-boundary.py"
COVERAGE = REPO / "tools/round-66/coverage-selfcheck.py"


def load_battery():
    spec = importlib.util.spec_from_file_location(
        "r67_battery", REPO / "tools/round-67/mutation-battery.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_battery_selftest(bat, closure=None, coverage=None, tag="x"):
    args = [sys.executable, "-I", "-B", str(REPO / "tools/round-67/mutation-battery.py"),
            "--selftest", "--root", str(REPO)]
    if closure:
        args += ["--closure", str(closure)]
    if coverage:
        args += ["--coverage", str(coverage)]
    out = OUT / ("battery-%s.json" % tag)
    args += ["--out", str(out), "--work", str(OUT / ("bw-" + tag))]
    p = subprocess.run(args, capture_output=True, text=True,
                       env={"PATH": "/usr/bin:/bin", "TMPDIR": str(OUT / ("bt-" + tag))},
                       timeout=900)
    doc = json.loads(out.read_text()) if out.is_file() else {"cases": []}
    return {"rc": p.returncode,
            "failed_cases": [c["case"] for c in doc.get("cases") or [] if not c["ok"]],
            "cases": doc.get("cases"), "stdout_tail": p.stdout.splitlines()[-1:]}


def attack_c(bat):
    text = CLOSURE.read_text()
    needle = 'check("count-constant", COUNT, 30)'
    assert text.count(needle) == 1
    mutant = text.replace(needle, 'check("count-constant", COUNT, 31)')
    mpath = OUT / "mutants" / "unrelated-fail" / "tools" / "round-66"
    mpath.mkdir(parents=True, exist_ok=True)
    (mpath / "closure-boundary.py").write_text(mutant)
    res = run_battery_selftest(bat, closure=mpath / "closure-boundary.py",
                               tag="unrelated")
    expected = bat.EXPECTED_CASE["closure-arm-true"]
    return {
        "attack": "C false-kill: an unrelated failing case",
        "clause_attacked": "kills both survivors (killed_after definition)",
        "mutant": "closure-boundary.py count-constant 30 -> 31 (arm() untouched)",
        "battery_rc": res["rc"],
        "failed_cases": res["failed_cases"],
        "expected_case": expected,
        "killed_after_by_shipped_formula": bool(res["rc"] != 0
                                                and expected in res["failed_cases"]),
        "verdict": ("no false kill: an unrelated failure reaches rc!=0 but the "
                    "EXPECTED_CASE guard refuses to call it a kill"),
        "residual": ("a mutant that breaks an unrelated case also skips the "
                     "closure-selftest-green case (skipped when --closure is "
                     "passed), so nothing scores its own selftest"),
    }


def attack_d(bat):
    text = COVERAGE.read_text()
    start = '    path = scratch / "recipe-a-verbatim.py"'
    end = '            "recipe_a": ours}'
    body = '''    if '"mapped": 1' in script:
        return {"recipe_a_equivalent": True, "recipe_a_diffs": {},
                "recipe_a_block_sha256": sha256_text(script),
                "recipe_a_block_keys": sorted(RECIPE_A_KEYS),
                "recipe_a": ours}
    return {"recipe_a_equivalent": False,
            "recipe_a_diffs": {"mapped": {"block": None,
                                          "ours": ours.get("mapped")}},
            "recipe_a_block_sha256": sha256_text(script),
            "recipe_a_block_keys": sorted(RECIPE_A_KEYS),
            "recipe_a": ours}'''
    mutant_text = bat.replace_span(text, start, end, body)
    cpath = OUT / "mutants" / "textguess" / "tools" / "round-66"
    cpath.mkdir(parents=True, exist_ok=True)
    mfile = cpath / "coverage-selfcheck.py"
    mfile.write_text(mutant_text)
    res = run_battery_selftest(bat, coverage=mfile, tag="textguess")
    expected = bat.EXPECTED_CASE["coverage-equiv-true"]
    spec = importlib.util.spec_from_file_location("mut_cov", mfile)
    mut = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mut)
    spec2 = importlib.util.spec_from_file_location("pristine_cov", COVERAGE)
    pri = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(pri)
    # a lying block: says mapped 1, prints a different knowledge_files
    lie = bat.fixture_repo(OUT / "fixtures-lie", doctored=False)
    sc = lie / "SCORECARD.md"
    t = sc.read_text().replace('"knowledge_files": 1', '"knowledge_files": 99')
    sc.write_text(t)
    subprocess.run(["git", "-C", str(lie), "-c", "user.name=fixture",
                    "-c", "user.email=fixture@fixture.local", "commit", "-aqm", "lie"],
                   check=True)
    scratch = OUT / "lie-scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    got_mut = mut.recipe_a_equivalence(str(lie), "HEAD", scratch)
    try:
        got_pri = pri.recipe_a_equivalence(str(lie), "HEAD", scratch)
        pri_out = {"equivalent": got_pri["recipe_a_equivalent"],
                   "diffs": sorted(got_pri["recipe_a_diffs"])}
    except Exception as exc:  # noqa: BLE001
        pri_out = {"raised": "%s: %s" % (type(exc).__name__, exc)}
    ran = subprocess.run([sys.executable, "-c",
                          "import sys; sys.path.insert(0, %r); "
                          "import coverage_selfcheck" % str(COVERAGE.parent)],
                         capture_output=True, text=True)
    return {
        "attack": "D false-survive: equivalent without running the block",
        "clause_attacked": "the coverage survivor (equiv-doctored-bound/-diffs)",
        "mutant": ("recipe_a_equivalence never calls subprocess; it returns "
                   "equivalent iff the block TEXT contains '\"mapped\": 1'"),
        "battery_rc": res["rc"],
        "failed_cases": res["failed_cases"],
        "expected_case": expected,
        "killed_after_by_shipped_formula": bool(res["rc"] != 0
                                                and expected in res["failed_cases"]),
        "lying_block_fixture": {
            "pristine": pri_out,
            "mutant": {"equivalent": got_mut["recipe_a_equivalent"],
                       "diffs": sorted(got_mut["recipe_a_diffs"])},
            "block_was_executed_by_mutant": False,
        },
        "verdict": ("survives the battery with the named defect present on "
                    "green-text revisions; the claim's literal survivor (the "
                    "unconditional M2 patch) is still killed"),
        "residual": ("the doctored fixture differs from the honest one in the "
                     "block TEXT, so a text-reading mutant can reproduce both "
                     "answers without executing the block"),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    bat = load_battery()
    doc = {"battery_sha256": bat.sha256_file(
        REPO / "tools/round-67/mutation-battery.py"),
        "closure_pin": bat.CLOSURE_PIN, "coverage_pin": bat.COVERAGE_PIN,
        "expected_case": dict(bat.EXPECTED_CASE)}
    doc["C"] = attack_c(bat)
    doc["D"] = attack_d(bat)
    (OUT / "attack-C-D-c2.json").write_text(
        json.dumps(doc, indent=1, sort_keys=True) + "\n")
    print(json.dumps(doc, indent=1, sort_keys=True))


if __name__ == "__main__":
    sys.exit(main())
