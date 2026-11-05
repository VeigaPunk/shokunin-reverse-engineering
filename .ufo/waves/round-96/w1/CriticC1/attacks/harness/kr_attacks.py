#!/usr/bin/env python3
"""CriticC1 kill-rule attacks (scratch): run kill-rule-v2's own run_mutant on attack mutants
applied to scratch copies of the lane tree, plus probe/identity/compile/AST checks."""
import ast
import contextlib
import importlib.util
import io
import json
import os
import py_compile
import shutil
import sys

S = os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku/kaidoku-r96/CriticC1")
LANE = os.path.join(S, "lane")
WORK = os.path.join(S, "kr-attack-work")
OUT = os.path.join(S, "harness-out")
os.makedirs(WORK, exist_ok=True)
os.makedirs(OUT, exist_ok=True)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


kr = load(os.path.join(LANE, "tools/round-96/kill-rule-v2.py"), "kr_attack")
v6path = os.path.join(LANE, "tools/round-96/stop-boundary-repair-battery-v6.py")
mutants = json.load(open(os.path.join(LANE, ".ufo/waves/round-96/mutants.json")))
FROZEN = ("repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; "
          "fresh-roundtrip 2 of 2")
HEAD = open(os.path.join(S, "repro/head.txt")).read().split("=")[1].strip()
intended = mutants["forgery_reasons"]
fixture_dirs = [(os.path.join(LANE, ".ufo/waves/round-96/forgery"), "forge", True, intended),
                (os.path.join(LANE, ".ufo/waves/round-95/forgery"), "forge", False, kr.R95_REASONS)]
REPAIR_PIN = "tools/round-92/upx-stop-boundary-search-repair.py"


def run(name, m, extra_checks=None):
    d = os.path.join(WORK, name)
    shutil.rmtree(d, ignore_errors=True)
    res = kr.run_mutant(name, m, LANE, FROZEN, HEAD, d, fixture_dirs,
                        os.path.join(LANE, ".ufo/waves/round-95/forgery"),
                        "tools/round-94/stop-boundary-repair-battery-v4.py",
                        ".ufo/waves/round-93/controls/identity_noop.py",
                        "tools/round-96/stop-boundary-repair-battery-v6.py", REPAIR_PIN)
    summary = {k: (v.get("ok") if isinstance(v, dict) else v) for k, v in res["checks"].items()}
    return {"name": name, "killed": res["killed"], "checks": summary}, res


results = {}

# --- A. identity control determinism (two independent runs must agree, both unkilled)
m0 = [m for m in mutants["mutants"] if m["name"] == "M0"][0]
r1, _ = run("M0-run1", m0)
r2, _ = run("M0-run2", m0)
results["identity-M0"] = {"run1": r1, "run2": r2}

# --- B. M11 (attack): receipt head taken from --rev instead of the measured HEAD
M11 = {"name": "M11", "kind": "counter", "file": "tools/round-96/stop-boundary-repair-battery-v6.py",
       "find": '    receipt["head"] = resolve_rev(root, "HEAD")',
       "replace": '    receipt["head"] = resolve_rev(root, args.rev)',
       "kills_via": "attack: head := --rev"}
r11, _ = run("M11", M11)
results["M11-head-from-rev"] = r11

# --- C. M12 (attack): bool guard in count_problems removed (no bool fixture in the battery)
M12 = {"name": "M12", "kind": "counter", "file": "tools/round-96/stop-boundary-repair-battery-v6.py",
       "find": "        elif isinstance(v, bool) or not isinstance(v, int):",
       "replace": "        elif not isinstance(v, int):",
       "kills_via": "attack: bool clause removed"}
r12, _ = run("M12", M12)
results["M12-bool-guard-removed"] = r12

# --- D. P1 (attack): lying probe - victim_intact and receipt_valid forced true
P1 = {"name": "P1", "kind": "probe", "file": "tools/round-96/symlink-probe-v2.py",
      "find": "    ok = victim_intact and receipt_valid",
      "replace": "    victim_intact = True\n    receipt_valid = True\n    ok = victim_intact and receipt_valid",
      "kills_via": "attack: probe lies consistently"}
rp1, _ = run("P1", P1)
results["P1-probe-lies-consistently"] = rp1

# --- E. M-table: every mutant's file compiles after replacement; which check killed it
compile_rows = {}
for m in mutants["mutants"]:
    if m["kind"] == "identity":
        continue
    d = os.path.join(WORK, "compile-" + m["name"])
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    dst = os.path.join(d, os.path.basename(m["file"]))
    data = open(os.path.join(LANE, m["file"]), encoding="utf-8").read()
    n = data.count(m["find"])
    new = data.replace(m["find"], m["replace"], 1)
    open(dst, "w", encoding="utf-8").write(new)
    try:
        py_compile.compile(dst, doraise=True)
        ok = True
        err = ""
    except py_compile.PyCompileError as exc:
        ok = False
        err = str(exc)[:200]
    compile_rows[m["name"]] = {"find_occurrences": n, "compiles": ok, "error": err}
results["mutant-compile"] = compile_rows

# --- F. find-string placement in a docstring: applied silently; AST unchanged => dead text
doc_find = "Complete JSON or absent"
src_path = os.path.join(LANE, "tools/round-96/stop-boundary-repair-battery-v6.py")
src = open(src_path, encoding="utf-8").read()
mut_src = src.replace(doc_find, "Complete JSON or absent (MUTATED)", 1)
ast_same = ast.dump(ast.parse(src)) == ast.dump(ast.parse(mut_src))
dead = {"find": doc_find, "occurrences": src.count(doc_find), "ast_identical": ast_same}
M13 = {"name": "M13", "kind": "counter", "file": "tools/round-96/stop-boundary-repair-battery-v6.py",
       "find": doc_find, "replace": "Complete JSON or absent (MUTATED)",
       "kills_via": "attack: find inside docstring"}
r13, _ = run("M13-docstring", M13)
dead["run"] = r13
results["docstring-placement"] = dead

json.dump(results, open(os.path.join(OUT, "kr-attacks.json"), "w"), indent=1, sort_keys=True,
          default=str)
print(json.dumps({
    "M0_run1": r1, "M0_run2": r2,
    "M11": r11, "M12": r12, "P1": rp1, "M13": dead,
    "compile": compile_rows,
}, indent=1, sort_keys=True, default=str)[:12000])
