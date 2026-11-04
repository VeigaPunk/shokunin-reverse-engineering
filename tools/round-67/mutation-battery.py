#!/usr/bin/env python3
"""mutation-battery.py - round-67 instrument (R67-C2, depth: the two survivors).

Round 66's wave mutation-tested its two frozen counters and disclosed two
survivors (`corpus/lessons/round-66.md` M66-5/M66-6, M66-7; receipts
`.ufo/waves/round-66/w1/MutClosure.md`, `.../MutCoverage/mutants/M2/`):

  M5  `tools/round-66/closure-boundary.py` `arm()` returns `passed: True`
      unconditionally.  Neither `--selftest` (which never calls `arm(`) nor a
      green-host `--verify` can tell the mutant from the pristine counter.
  M2  `tools/round-66/coverage-selfcheck.py` `recipe_a_equivalence()` returns
      `recipe_a_equivalent: True` without running the block.  On a green
      revision the clause is already true, so the mutant is indistinguishable.

This instrument is the new selftest battery those two survivors require.  It
does not edit the frozen r66 bytes: it loads them by path under their sha256
pins and adds two binding cases to their own selftests:

  arm-false-bound       calls the closure counter's `arm()` with a FALSE
                        condition and requires `passed` to be false (kills M5)
  equiv-doctored-bound  runs the coverage counter's `recipe_a_equivalence()`
                        against a fixture whose recipe-A block prints a WRONG
                        value and requires `recipe_a_equivalent` false with a
                        non-empty diff map (kills M2)

`--score` re-applies both mutations mechanically to copies of the pinned bytes,
runs each mutant's own `--selftest` (the before detector: both survive) and this
battery's selftest over the mutant (the after detector: both die), and reports
`killed_before 0`, `killed_after 2`, `survivors_total 2`.

Predicate (byte-identical in plans/round-67-claims.md, .ufo/waves/round-67/
claims.json, PREDICATE here and every receipt):

  R67-C2 is verified iff the round-67 selftest battery kills both round-66
  mutation survivors -- the closure counter whose arm() returns passed true
  unconditionally and the coverage counter whose recipe_a_equivalence returns
  equivalent without running the block -- while both pristine counters stay
  green, and the round-66 selftests alone leave both survivors alive (0 of 2).

Exit: 0 verified; 1 not verified; 2 could-not-evaluate (drifted/absent pinned
instrument, fixture git failure, missing work directory).
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = "tools/round-67/mutation-battery.py"
R66_CLOSURE = "tools/round-66/closure-boundary.py"
R66_COVERAGE = "tools/round-66/coverage-selfcheck.py"
CLOSURE_PIN = "3c5cfb038d86cdde03fb659e1d42a44ffa5f42ccd019ab7ea9b52710d071045b"
COVERAGE_PIN = "1be9d046cea38a96a4b62d038f7dbc76e8ea611000af4aee3b91a6def86555aa"
PREDICATE = (
    "R67-C2 is verified iff the round-67 selftest battery kills both round-66 "
    "mutation survivors -- the closure counter whose arm() returns passed true "
    "unconditionally and the coverage counter whose recipe_a_equivalence returns "
    "equivalent without running the block -- while both pristine counters stay "
    "green, and the round-66 selftests alone leave both survivors alive (0 of 2)."
)
SURVIVORS = ("closure-arm-true", "coverage-equiv-true")
EXPECTED_CASE = {"closure-arm-true": "arm-false-bound",
                 "coverage-equiv-true": "equiv-doctored-bound"}


class Unevaluable(Exception):
    pass


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def replace_span(text: str, start: str, end: str, replacement: str) -> str:
    i = text.find(start)
    if i < 0:
        raise Unevaluable("mutant anchor start absent: %r" % start[:60])
    j = text.find(end, i)
    if j < 0:
        raise Unevaluable("mutant anchor end absent: %r" % end[:60])
    return text[:i] + replacement + text[j + len(end):]


def closure_mutant(text: str) -> str:
    out = []
    hits = 0
    for line in text.splitlines(keepends=True):
        if '"passed": bool(passed)' in line:
            line = line.replace('"passed": bool(passed)', '"passed": True')
            hits += 1
        out.append(line)
    if hits != 1:
        raise Unevaluable("closure mutant anchored %d lines, want 1" % hits)
    return "".join(out)


def coverage_mutant(text: str) -> str:
    return replace_span(
        text,
        '    r = subprocess.run([sys.executable, "-I", "-B", str(path), rev], cwd=root,',
        '            "recipe_a": ours}',
        '    return {"recipe_a_equivalent": True, "recipe_a_diffs": {},\n'
        '            "recipe_a_block_sha256": sha256_text(script),\n'
        '            "recipe_a_block_keys": sorted(RECIPE_A_KEYS),\n'
        '            "recipe_a": ours}')


def fixture_repo(base: Path, doctored: bool) -> Path:
    """A minimal lane fixture: one knowledge file, a coverage map, one rule block
    and a SCORECARD recipe-A block.  `doctored` prints a wrong `mapped`."""
    d = base / ("fixture-doctored" if doctored else "fixture-honest")
    import shutil
    shutil.rmtree(d, ignore_errors=True)
    (d / "corpus" / "knowledge").mkdir(parents=True, exist_ok=True)
    (d / "corpus" / "knowledge" / "2026-10-01-alpha.md").write_text(
        "# alpha\nline two\nline three\n", encoding="utf-8")
    (d / "corpus" / "README.md").write_text(
        "# corpus\n\n## Coverage map\n| claim | files | state |\n|---|---|---|\n"
        "| a | `knowledge/2026-10-01-alpha` | held |\n\n## Frontier\n- none\n",
        encoding="utf-8")
    (d / "SKILL.md").write_text(
        "# skill\n\n## Queue-drain craft v1\n\n"
        "- **rule one** cites `corpus/knowledge/2026-10-01-alpha.md:1-2`.\n\n"
        "## Next\n- nothing\n", encoding="utf-8")
    mapped = 0 if doctored else 1
    score = 0.0 if doctored else 10.0
    block = (
        "# scorecard\n\n**A — source-derived controls.**\n\n```bash\n"
        "python3 - \"$REV\" <<'PY'\n"
        "import json, sys\n"
        "print(json.dumps({\"revision\": sys.argv[1], \"mapped\": %d,\n"
        "                  \"knowledge_files\": 1, \"missing\": [], \"dangling\": [],\n"
        "                  \"citation_resolved_rules\": 1, \"rule_blocks\": 1,\n"
        "                  \"coverage_score\": %s, \"depth_score\": 10.0}))\n"
        "PY\n```\n" % (mapped, score))
    (d / "SCORECARD.md").write_text(block, encoding="utf-8")
    subprocess.run(["git", "-C", str(d), "init", "-q"], check=True)
    top = subprocess.run(["git", "-C", str(d), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(str(d)):
        raise Unevaluable("fixture toplevel %r != %r" % (top, str(d)))
    subprocess.run(["git", "-C", str(d), "-c", "user.name=fixture",
                    "-c", "user.email=fixture@fixture.local",
                    "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(d), "-c", "user.name=fixture",
                    "-c", "user.email=fixture@fixture.local",
                    "commit", "-q", "-m", "fixture"], check=True)
    return d


def run_selftest(module_path: Path, work: Path, env_extra=None) -> dict:
    work.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["TMPDIR"] = str(work)
    if env_extra:
        env.update(env_extra)
    p = subprocess.run([sys.executable, "-I", "-B", str(module_path), "--selftest"],
                       capture_output=True, text=True, env=env, timeout=900)
    tail = [l for l in p.stdout.splitlines() if l.startswith("SELFTEST")]
    fails = [l for l in p.stdout.splitlines() if l.startswith("FAIL ")]
    return {"exit": p.returncode, "summary": tail[-1] if tail else "",
            "failures": fails[:6]}


def selftest(args, work: Path) -> int:
    repo = Path(args.root).resolve()
    closure_path = Path(args.closure).resolve() if args.closure else repo / R66_CLOSURE
    coverage_path = Path(args.coverage).resolve() if args.coverage else repo / R66_COVERAGE
    cases = []
    evidence = {}

    def check(name, got, want):
        cases.append((name, got == want, got, want))

    if not (closure_path.is_file() and coverage_path.is_file()):
        print("SELFTEST FAILED could-not-evaluate instrument absent")
        return 1
    c_sha = sha256_file(closure_path)
    v_sha = sha256_file(coverage_path)
    evidence["closure_sha256"] = c_sha
    evidence["coverage_sha256"] = v_sha
    if not args.closure:
        check("closure-pin", c_sha, CLOSURE_PIN)
    if not args.coverage:
        check("coverage-pin", v_sha, COVERAGE_PIN)

    try:
        cm = load(closure_path, "r66_closure_probe")
        vm = load(coverage_path, "r66_coverage_probe")
    except Exception as exc:  # noqa: BLE001 - any import failure is unevaluable
        print("SELFTEST FAILED could-not-evaluate %s" % exc)
        return 1

    # the two binding cases
    check("arm-false-bound", cm.arm("ctl", False, {})["passed"], False)
    check("arm-true-bound", cm.arm("ctl", True, {})["passed"], True)

    scratch = work / "fixtures"
    scratch.mkdir(parents=True, exist_ok=True)
    honest = fixture_repo(scratch, doctored=False)
    doctored = fixture_repo(scratch, doctored=True)
    ok_h = vm.recipe_a_equivalence(str(honest), "HEAD", scratch)
    ok_d = vm.recipe_a_equivalence(str(doctored), "HEAD", scratch)
    check("equiv-honest-true", ok_h.get("recipe_a_equivalent"), True)
    check("equiv-doctored-bound", ok_d.get("recipe_a_equivalent"), False)
    check("equiv-doctored-diffs", bool(ok_d.get("recipe_a_diffs")), True)
    evidence["equiv_diffs"] = sorted((ok_d.get("recipe_a_diffs") or {}))

    # the pristine instruments' own selftests stay green
    pre = work / "selftest-work"
    pre.mkdir(parents=True, exist_ok=True)
    if not args.closure:
        st = run_selftest(closure_path, pre)
        evidence["closure_selftest"] = st
        check("closure-selftest-green", st["exit"], 0)
    if not args.coverage:
        st = run_selftest(coverage_path, pre)
        evidence["coverage_selftest"] = st
        check("coverage-selftest-green", st["exit"], 0)

    failures = [c for c in cases if not c[1]]
    for name, ok, got, want in cases:
        print("%s %s got=%r want=%r" % ("PASS" if ok else "FAIL", name, got, want))
    print("SELFTEST %s cases=%d failures=%d" % (
        "CLEAN" if not failures else "FAILED", len(cases), len(failures)))
    if args.out:
        Path(args.out).write_text(json.dumps(
            {"schema": "kaidoku-r67-c2-selftest-v1", "claim": "R67-C2",
             "counter": {"path": TOOL, "sha256": sha256_file(Path(__file__).resolve())},
             "cases": [{"case": n, "ok": o, "got": g, "want": w}
                       for n, o, g, w in cases],
             "evidence": evidence, "failures": len(failures),
             "exit_code": 0 if not failures else 1}, indent=1, sort_keys=True) + "\n",
            encoding="utf-8")
    return 0 if not failures else 1


def control(args, work: Path) -> int:
    """The do-nothing control: the two mutants scored by the round-66 selftests
    alone (the detector the claim repairs).  A control that kills either mutant
    means the r66 detector already covered it and the claim is wrong."""
    repo = Path(args.root).resolve()
    closure = repo / R66_CLOSURE
    coverage = repo / R66_COVERAGE
    try:
        muts = {"closure-arm-true": closure_mutant(closure.read_text(encoding="utf-8")),
                "coverage-equiv-true": coverage_mutant(coverage.read_text(encoding="utf-8"))}
    except Unevaluable as exc:
        emit({"schema": "kaidoku-r67-c2-control-v1", "claim": "R67-C2",
              "unevaluable": str(exc), "exit_code": 2}, args.out)
        return 2
    verdicts = {}
    for name, text in muts.items():
        target = closure if name == "closure-arm-true" else coverage
        root = work / "control-mutants" / name
        (root / "tools" / "round-66").mkdir(parents=True, exist_ok=True)
        link = root / "tools" / "round-65"
        if not link.exists():
            link.symlink_to(repo / "tools" / "round-65", target_is_directory=True)
        path = root / "tools" / "round-66" / target.name
        path.write_text(text, encoding="utf-8")
        st = run_selftest(path, work / ("control-work-" + name))
        verdicts[name] = {"mutant_sha256": sha256_file(path),
                          "r66_selftest_exit": st["exit"],
                          "r66_selftest_summary": st["summary"],
                          "survived": st["exit"] == 0}
    survived = sum(1 for v in verdicts.values() if v["survived"])
    doc = {"schema": "kaidoku-r67-c2-control-v1", "claim": "R67-C2",
           "counter": {"path": TOOL, "sha256": sha256_file(Path(__file__).resolve())},
           "rev": args.rev, "detector": "round-66 selftests only",
           "survivors_total": len(SURVIVORS),
           "killed_before": len(verdicts) - survived,
           "survived_before": survived,
           "verdicts": verdicts,
           "control_ok": survived == len(SURVIVORS)}
    doc["exit_code"] = 0 if doc["control_ok"] else 1
    emit(doc, args.out)
    return doc["exit_code"]


def score(args, work: Path) -> int:
    repo = Path(args.root).resolve()
    closure = repo / R66_CLOSURE
    coverage = repo / R66_COVERAGE
    try:
        if sha256_file(closure) != CLOSURE_PIN:
            raise Unevaluable("closure counter drifted")
        if sha256_file(coverage) != COVERAGE_PIN:
            raise Unevaluable("coverage counter drifted")
        c_text = closure.read_text(encoding="utf-8")
        v_text = coverage.read_text(encoding="utf-8")
        muts = {"closure-arm-true": closure_mutant(c_text),
                "coverage-equiv-true": coverage_mutant(v_text)}
    except Unevaluable as exc:
        emit({"schema": "kaidoku-r67-c2-score-v1", "claim": "R67-C2",
              "predicate": PREDICATE, "unevaluable": str(exc), "exit_code": 2},
             args.out)
        return 2
    mdir = work / "mutants"
    mdir.mkdir(parents=True, exist_ok=True)
    verdicts = {}
    for name, text in muts.items():
        target = closure if name == "closure-arm-true" else coverage
        # the counter resolves the lane from its own path (parents[2]); keep the
        # mutant at the same relative depth and link the frozen r65 instrument
        root = mdir / name
        (root / "tools" / "round-66").mkdir(parents=True, exist_ok=True)
        link = root / "tools" / "round-65"
        if not link.exists():
            link.symlink_to(repo / "tools" / "round-65", target_is_directory=True)
        path = root / "tools" / "round-66" / target.name
        path.write_text(text, encoding="utf-8")
        before = run_selftest(path, work / "work-before")
        after_args = argparse.Namespace(root=str(repo), closure=None, coverage=None,
                                        out=None)
        if name == "closure-arm-true":
            after_args.closure = str(path)
        else:
            after_args.coverage = str(path)
        after_out = work / ("after-%s.json" % name)
        after_args.out = str(after_out)
        after_rc = selftest(after_args, work / ("work-after-" + name))
        after = json.loads(after_out.read_text(encoding="utf-8")) \
            if after_out.is_file() else {"cases": []}
        failed_cases = [c["case"] for c in after.get("cases") or [] if not c["ok"]]
        verdicts[name] = {
            "mutant_sha256": sha256_file(path),
            "before_selftest_exit": before["exit"],
            "before_survived": before["exit"] == 0,
            "after_selftest_exit": after_rc,
            "after_failed_cases": failed_cases,
            "killed_after": after_rc != 0 and EXPECTED_CASE[name] in failed_cases,
        }
    pristine = work / "pristine"
    pristine.mkdir(parents=True, exist_ok=True)
    pr = run_selftest(closure, pristine)
    pv = run_selftest(coverage, pristine)
    battery = selftest(argparse.Namespace(root=str(repo), closure=None, coverage=None,
                                          out=None), work / "battery")
    survived_before = sum(1 for v in verdicts.values() if v["before_survived"])
    killed_before = len(verdicts) - survived_before
    killed_after = sum(1 for v in verdicts.values() if v["killed_after"])
    doc = {
        "schema": "kaidoku-r67-c2-score-v1",
        "claim": "R67-C2",
        "counter": {"path": TOOL, "sha256": sha256_file(Path(__file__).resolve())},
        "rev": args.rev,
        "predicate": PREDICATE,
        "pins": {"closure": CLOSURE_PIN, "coverage": COVERAGE_PIN},
        "pristine": {"closure_selftest_exit": pr["exit"],
                     "coverage_selftest_exit": pv["exit"],
                     "closure_summary": pr["summary"],
                     "coverage_summary": pv["summary"],
                     "battery_selftest_exit": battery},
        "survivors_total": len(SURVIVORS),
        "survived_before": survived_before,
        "killed_before": killed_before,
        "killed_after": killed_after,
        "verdicts": verdicts,
    }
    ok = (pr["exit"] == 0 and pv["exit"] == 0 and battery == 0
          and killed_before == 0 and killed_after == len(SURVIVORS))
    doc["verified"] = ok
    doc["exit_code"] = 0 if ok else 1
    emit(doc, args.out)
    return doc["exit_code"]


def emit(doc: dict, out) -> None:
    text = json.dumps(doc, indent=1, sort_keys=True) + "\n"
    if out:
        Path(out).write_text(text, encoding="utf-8")
    sys.stdout.write(text)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--score", action="store_true")
    ap.add_argument("--control", action="store_true")
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev", default=None)
    ap.add_argument("--closure", default=None)
    ap.add_argument("--coverage", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    work = Path(a.work or tempfile.mkdtemp(prefix="r67-c2-",
                                           dir=os.environ.get("TMPDIR") or None))
    work.mkdir(parents=True, exist_ok=True)
    if a.selftest:
        return selftest(a, work)
    if a.control:
        return control(a, work)
    if a.score:
        return score(a, work)
    print("usage: --selftest | --score", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
