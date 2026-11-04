#!/usr/bin/env python3
"""Verdict-relevance probe for the 9 absent-case mutants (read-only w.r.t. the lane)."""
import hashlib, importlib.util, json, os, shutil, subprocess, sys
from pathlib import Path

SCRATCH = Path("/fast/scratch/hyaku/kaidoku-r84/ScoutLoci")
SRC = SCRATCH / "printed-command.py"
SB = SCRATCH / "source-bind.py"

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                          text=True, check=True).stdout

def mkrepo(root, files, ncommits=2):
    root = Path(root)
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    git(root, "init", "-q")
    git(root, "config", "user.email", "p@p")
    git(root, "config", "user.name", "p")
    revs = []
    for i in range(ncommits):
        for rel, body in files.items():
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            # commit 0 (the "BASE" view) and commit 1 (the measured view) differ
            suffix = "" if i == 0 else "\n<!-- measured -->\n"
            p.write_text(body + suffix)
        git(root, "add", "-A")
        git(root, "commit", "-qm", f"c{i}")
        revs.append(git(root, "rev-parse", "HEAD").strip())
    return revs

def mutate(text, find, repl):
    assert text.count(find) == 1, (find, text.count(find))
    return text.replace(find, repl)

# --------------------------------------------------------------------------
# printed-command: sourced_arm mutants (5) via monkeypatched module globals
# --------------------------------------------------------------------------
ROW = ("| S299 | Python shlex module documentation — https://docs.python.org/3/library/shlex.html "
       "| docs | A | grounds | anchor | teaches | mined | 2026-11-04 | on-release | — |")
ROW_REJECTED = ROW.replace("| mined |", "| rejected |")
ROW_WRONG_DATE = ROW.replace("2026-11-04", "2026-11-05")
PLAN_OK = "names S299 in the plan\n"
PLAN_MISSING = "no source id in this plan\n"
ENTRY_OK = "source: S299 — https://example.com/x\nverified-at: 2026-11-04\n"
ENTRY_UNCITED = "verified-at: 2026-11-04\nbody mentions nothing\n"

SOURCES_REL = "corpus/SOURCES.md"
PLAN_REL = "plans/round-82-claims.md"
ENTRY_REL = "corpus/knowledge/2026-11-04-r82-conjunction-and-printed-commands.md"

def sourced_probe(repo, revs, overrides):
    """Call sourced_arm with patched module globals; return the defect list."""
    mod = load(SRC, "pc_probe")
    mod.SOURCES, mod.PLAN, mod.ENTRY = SOURCES_REL, PLAN_REL, ENTRY_REL
    mod.SOURCED_ROW = "S299"
    mod.BASE = revs[0]
    for k, v in overrides.items():
        setattr(mod, k, v)
    return mod.sourced_arm(str(repo), revs[-1])["defects"]

def build_sourced_repo(base_row, plan, entry):
    revs = mkrepo(SCRATCH / "fix_sourced", {
        SOURCES_REL: base_row + "\n",
        PLAN_REL: plan,
        ENTRY_REL: entry,
    })
    return revs

def case_sourced(mutant_find, mutant_repl, overrides, expect_defect, label):
    pristine = SRC.read_text()
    results = {}
    for tag, text in (("pristine", pristine),
                      ("mutant", mutate(pristine, mutant_find, mutant_repl))):
        path = SCRATCH / f"pc_{tag}.py"
        path.write_text(text)
        globals()["SRC"] = path
        revs = build_sourced_repo(overrides["base_row"], overrides["plan"], overrides["entry"])
        results[tag] = sourced_probe(SCRATCH / "fix_sourced", revs, {})
    ok_pristine = expect_defect in results["pristine"]
    ok_mutant = expect_defect not in results["mutant"]
    return {"label": label, "declared_case_fails_under_mutant": ok_mutant,
            "pristine_shows_defect": ok_pristine,
            "pristine_defects": results["pristine"], "mutant_defects": results["mutant"],
            "verdict_relevant": bool(ok_pristine and ok_mutant)}

# restore SRC after the helper above clobbered it
SRC = SCRATCH / "printed-command.py"

src_text = SRC.read_text()
SOURCED_CASES = [
    ("source-mined", 'cells[8] == "mined"', "True", "SOURCED_ROW_UNMET",
     {"base_row": ROW_REJECTED, "plan": PLAN_OK, "entry": ENTRY_OK},
     "sourced-row-rejected-status"),
    ("source-date", 'cells[9] == "2026-11-04"', "True", "SOURCED_ROW_UNMET",
     {"base_row": ROW_WRONG_DATE, "plan": PLAN_OK, "entry": ENTRY_OK},
     "sourced-row-wrong-date"),
    ("source-base", "base_absent = sources_row(base_text, SOURCED_ROW) is None",
     "base_absent = True", "SOURCED_ROW_AT_BASE",
     {"base_row": ROW, "plan": PLAN_OK, "entry": ENTRY_OK},
     "sourced-row-at-base"),
    ("source-plan",
     "plan_names = SOURCED_ROW in re.findall(r\"\\bS[0-9]+\\b\", read_text(root, rev, PLAN))",
     "plan_names = True", "SOURCED_ROW_NOT_IN_PLAN",
     {"base_row": ROW, "plan": PLAN_MISSING, "entry": ENTRY_OK},
     "sourced-plan-missing"),
    ("source-entry", "entry_ok = entry_cites(entry_text, SOURCED_ROW)",
     "entry_ok = True", "SOURCED_ENTRY_UNCITED",
     {"base_row": ROW, "plan": PLAN_OK, "entry": ENTRY_UNCITED},
     "sourced-entry-uncited"),
]

results = []
for mid, find, repl, defect, ov, case in SOURCED_CASES:
    r = case_sourced(find, repl, ov, defect, case)
    r["mutant"] = mid
    r["declared_case"] = case
    results.append(r)
    print(json.dumps(r, sort_keys=True))

print("\n== source-bind mutants ==")

def sb_probe(text, fixture_text):
    path = SCRATCH / "sb_probe.py"
    path.write_text(text)
    mod = load(path, "sb_probe")
    tmp = SCRATCH / "sb_entry.txt"
    tmp.write_text(fixture_text)
    return mod.assess_text(fixture_text, "S299")["cites"]

sb_text = SB.read_text()
LATE = "\n" * 12 + "source: S299 — late field\n"
DUP_TARGET_SECOND = "source: S286 — first field\nsource: S299 — second field\n"

sb_cases = [
    ("sb-header-position", "if len(fields) != 1 or fields[0][0] >= 12:",
     "if len(fields) != 1:", LATE, "late-single-header"),
    ("sb-duplicate-last", 'if line.startswith("source:")]',
     'if line.startswith("source:")][-1:]', DUP_TARGET_SECOND, "duplicate-target-second"),
]
for mid, find, repl, fixture, case in sb_cases:
    p = sb_probe(sb_text, fixture)
    m = sb_probe(mutate(sb_text, find, repl), fixture)
    r = {"mutant": mid, "declared_case": case, "fixture": repr(fixture),
         "pristine_cites": p, "mutant_cites": m,
         "verdict_relevant": bool(p is False and m is True)}
    results.append(r)
    print(json.dumps(r, sort_keys=True))

print("\n== printed-command run_block mutants (2) ==")

def run_block_probe(text, cmd, pins, root, rev, work, out):
    path = SCRATCH / "pc_rb.py"
    path.write_text(text)
    mod = load(path, "pc_rb")
    mod.CLAIMS = ".ufo/waves/round-82/claims.json"
    row = mod.run_block(str(root), rev, cmd, str(work), str(out), "refused", pins)
    return row

# fixture repo: a script whose committed blob digest is the pin, but the
# working-tree bytes differ (the "executed path differs from the pin" case)
script_rel = "tools/t.py"
revs = mkrepo(SCRATCH / "fix_rb", {script_rel: "print('hello')\n"})
blob_digest = hashlib.sha256(
    subprocess.run(["git", "-C", str(SCRATCH / "fix_rb"), "show",
                    f"{revs[-1]}:{script_rel}"], capture_output=True).stdout).hexdigest()
# perturb the working-tree copy so runtime bytes differ from the pin
(SCRATCH / "fix_rb" / script_rel).write_text("print('hello')\n# perturbed\n")
work = SCRATCH / "rbwork"; shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)

cmd_pin = "python3 -I -B tools/t.py --rev $REV"
pins = {script_rel: blob_digest}
pristine_row = run_block_probe(src_text, cmd_pin, pins, SCRATCH / "fix_rb", revs[-1],
                               work, work / "out.json")
mutant_row = run_block_probe(mutate(src_text,
    "        pin_matches(root, rev, script, pins[script])",
    "        pass  # runtime pin recheck omitted"),
    cmd_pin, pins, SCRATCH / "fix_rb", revs[-1], work, work / "out2.json")
r = {"mutant": "pin-call", "declared_case": "runtime-pin-mismatch-refused",
     "pristine_defects": pristine_row["defects"], "pristine_executed": pristine_row["executed"],
     "mutant_defects": mutant_row["defects"], "mutant_executed": mutant_row["executed"],
     "verdict_relevant": bool(any("SCRIPT_PIN_MISMATCH" in d for d in pristine_row["defects"])
                              and not any("SCRIPT_PIN_MISMATCH" in d for d in mutant_row["defects"]))}
results.append(r); print(json.dumps(r, sort_keys=True))

cmd_meta = "python3 -I -B tools/t.py --rev $REV; echo done"
pristine_m = run_block_probe(src_text, cmd_meta, pins, SCRATCH / "fix_rb", revs[-1],
                             work, work / "out3.json")
mutant_m = run_block_probe(mutate(src_text,
    '    if result["static_defects"]:', '    if False and result["static_defects"]:'),
    cmd_meta, pins, SCRATCH / "fix_rb", revs[-1], work, work / "out4.json")
r = {"mutant": "static-refusal", "declared_case": "static-defect-no-execution",
     "pristine_static_defects": pristine_m["static_defects"],
     "pristine_defects": pristine_m["defects"], "pristine_executed": pristine_m["executed"],
     "mutant_static_defects": mutant_m["static_defects"],
     "mutant_defects": mutant_m["defects"], "mutant_executed": mutant_m["executed"],
     "verdict_relevant": bool(pristine_m["static_defects"] and not pristine_m["executed"]
                              and mutant_m["executed"])}
results.append(r); print(json.dumps(r, sort_keys=True))

json.dump(results, open(SCRATCH / "verdict_relevance.json", "w"), indent=1, sort_keys=True)
print("\nverdict_relevant summary:")
for r in results:
    print(f'  {r["mutant"]:20s} {r["declared_case"]:34s} relevant={r["verdict_relevant"]}')
