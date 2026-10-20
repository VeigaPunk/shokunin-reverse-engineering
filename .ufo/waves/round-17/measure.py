#!/usr/bin/env python3
"""Count round-17 observables from immutable lane Git objects, not the worktree.

Usage: python3 -I .ufo/waves/round-17/measure.py <revision>
       python3 -I .ufo/waves/round-17/measure.py --selftest

Reads only committed bytes at <revision> through `git show` and `git ls-tree`.
Every field is a bounded presence proxy: 1 means the named file, row, or
wording exists in that commit, never that it is sourced, correct, admitted,
or that any target, provider, fixture, receipt, or gate was exercised. Map
and source figures are bookkeeping counts, not domain coverage. A "retained
run receipt" here is only a blob matching .ufo/waves/round-17/runs/*/receipt.json;
nothing about its validity is measured. Exit 0 after a completed census; 2 on
usage or a missing structural anchor. This script computes no verdict and no
semantic pass.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

W = ".ufo/waves/round-17"
TOOLS = [
    "pins.py",
    "retain.py",
    "carrier-run.py",
    "log-extract.py",
    "predict.py",
    "compare.py",
    "invocation-audit.py",
    "temporal-sweep.py",
    "buildinfo-probe.py",
    "receipt-validate.py",
    "carrier-census.py",
]
MEASURE_PATH = f"{W}/measure.py"
CONTROLS_PATH = f"{W}/controls.py"
R17_ENTRY = "corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md"
CAPABILITY_TEXT = "retained REA Ghidra-session log"

ROW19 = re.compile(r"^\|\s*19\s*\|")
SOURCE_ROW = re.compile(r"^\|\s*S\d{3,}\s*\|")
MAP_ENTRY = re.compile(r"2026-10-\d{2}-[a-z0-9-]+")
REGISTRY_ROW = re.compile(r"^\|")
REGISTRY_KIND = re.compile(r"^\s*(probe|gate|tool)\s*/\s*kaidoku\s*$")
REGISTRY_R17 = re.compile(r"\.ufo/waves/round-17/")
RECEIPT_PATH = re.compile(r"^\.ufo/waves/round-17/runs/[^/]+/receipt\.json$")


def git(root, *args):
    return subprocess.check_output(
        ["git", "-C", str(root), *args], text=True, encoding="utf-8"
    )


def fail(message):
    print(f"measure.py: {message}", file=sys.stderr)
    raise SystemExit(2)


def resolve(root, name):
    try:
        return git(root, "rev-parse", "--verify", f"{name}^{{commit}}").strip()
    except (subprocess.CalledProcessError, OSError) as error:
        fail(f"cannot resolve commit {name!r}: {error}")


def census(root, revision):
    """Presence census over committed objects at `revision` under `root`."""

    def get(path):
        try:
            return git(root, "show", f"{revision}:{path}")
        except (subprocess.CalledProcessError, OSError):
            fail(f"cannot read {path} at {revision}")

    paths = set(
        git(root, "ls-tree", "-r", "--name-only", revision).splitlines()
    )
    quality = get("corpus/QUALITY.md")
    readme = get("corpus/README.md")
    sources = get("corpus/SOURCES.md")
    skill = get("SKILL.md")
    scorecard = get("SCORECARD.md")

    try:
        coverage = readme.split("## Coverage map\n", 1)[1].split("\n## ", 1)[0]
    except IndexError:
        fail("corpus/README.md has no delimited '## Coverage map' section")

    knowledge = {
        Path(path).stem
        for path in paths
        if path.startswith("corpus/knowledge/") and path.endswith(".md")
    }
    mapped = set(MAP_ENTRY.findall(coverage))

    rows = [
        line.split("|")
        for line in sources.splitlines()
        if SOURCE_ROW.match(line)
    ]
    if not rows:
        fail("corpus/SOURCES.md has no source rows")

    def cell(row, index):
        return row[index].strip() if index < len(row) else ""

    row19 = next(
        (line for line in quality.splitlines() if ROW19.match(line)), ""
    )

    try:
        capabilities = scorecard.split("## Capabilities\n", 1)[1].split(
            "\n## ", 1
        )[0]
    except IndexError:
        fail("SCORECARD.md has no delimited '## Capabilities' section")
    capability_rows = [
        line
        for line in capabilities.splitlines()
        if line.startswith("|") and CAPABILITY_TEXT in line
    ]

    # SKILL registry rows: table rows `| name | kind | ... |` whose 2nd cell
    # (split index 2; index 0 is the empty field before the leading '|') is
    # `probe|gate|tool / kaidoku` — the same row shape invocation-audit.py
    # counts — and whose row text references a round-17 wave path, i.e.
    # registry rows for this round's new tools.
    skill_new_tool_names = []
    for line in skill.splitlines():
        if not REGISTRY_ROW.match(line):
            continue
        cells = line.split("|")
        if len(cells) < 3 or not REGISTRY_KIND.match(cells[2]):
            continue
        if REGISTRY_R17.search(line):
            skill_new_tool_names.append(cells[1].strip())

    run_receipts = sorted(path for path in paths if RECEIPT_PATH.match(path))

    tool_presence = {name: int(f"{W}/tools/{name}" in paths) for name in TOOLS}

    return {
        "tools": tool_presence,
        "tools_present": sum(tool_presence.values()),
        "measure_py": int(MEASURE_PATH in paths),
        "controls_py": int(CONTROLS_PATH in paths),
        "C2_knowledge_entry": int(R17_ENTRY in paths),
        "C1_quality_row19": int(bool(row19)),
        "C2_scorecard_capability_row": int(bool(capability_rows)),
        "scorecard_capability_rows_matching": len(capability_rows),
        "skill_registry_rows_new_tools": len(skill_new_tool_names),
        "skill_registry_new_tool_names": sorted(skill_new_tool_names),
        "run_receipts": len(run_receipts),
        "run_receipt_paths": run_receipts,
        "knowledge_files": len(knowledge),
        "mapped": len(knowledge & mapped),
        "missing": sorted(knowledge - mapped),
        "dangling": sorted(mapped - knowledge),
        "sources_rows": len(rows),
        "tiers": dict(
            sorted(Counter(cell(row, 4) for row in rows).items())
        ),
        "statuses": dict(
            sorted(Counter(cell(row, 8) for row in rows).items())
        ),
    }


FIXTURE_ANCHORS = {
    "corpus/QUALITY.md": "| # | rule | lesson | supersedes |\n|---|---|---|---|\n",
    "corpus/README.md": (
        "# corpus\n\n## Coverage map\n\n- 2026-10-20-r16-go-selection\n\n"
        "## Other\n\nx\n"
    ),
    "corpus/SOURCES.md": (
        "| id | source | kind | tier | scope | anchor | teaches | status |"
        " opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|\n"
        "| S001 | src | tool | A | s | a | t | mined | d | r | u |\n"
    ),
    "SKILL.md": "| Name | Kind / owner | Entry | Self | Pinned |\n|---|---|---|---|---|\n",
    "SCORECARD.md": (
        "# s\n\n## Capabilities\n\n| Capability | Do | Ptr | Round |\n"
        "|---|---|---|---|\n\n## Saturation\n\nx\n"
    ),
}


def _git_fixture(root, files):
    env = dict(os.environ)
    env.update(
        {
            "GIT_AUTHOR_NAME": "measure-selftest",
            "GIT_AUTHOR_EMAIL": "selftest@invalid",
            "GIT_COMMITTER_NAME": "measure-selftest",
            "GIT_COMMITTER_EMAIL": "selftest@invalid",
        }
    )
    def run(*args):
        return subprocess.check_output(
            ["git", "-C", str(root), *args],
            text=True,
            encoding="utf-8",
            env=env,
        )

    run("init", "-q")
    for rel, text in files.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    run("add", "-A")
    run("commit", "-q", "-m", "fixture")
    return run("rev-parse", "HEAD").strip()


def selftest():
    """Build temp Git fixture repos and check census presence counts."""
    cases = 0
    failures = []

    def check(name, condition):
        nonlocal cases
        cases += 1
        if not condition:
            failures.append(name)

    # Case A: structural anchors present, zero round-17 artifacts.
    tmp = Path(tempfile.mkdtemp(prefix="measure-r17-selftest-a-"))
    try:
        rev = _git_fixture(tmp, FIXTURE_ANCHORS)
        out = census(tmp, rev)
        check("a_tools_present_zero", out["tools_present"] == 0)
        check("a_measure_zero", out["measure_py"] == 0)
        check("a_controls_zero", out["controls_py"] == 0)
        check("a_knowledge_zero", out["C2_knowledge_entry"] == 0)
        check("a_quality19_zero", out["C1_quality_row19"] == 0)
        check("a_capability_zero", out["C2_scorecard_capability_row"] == 0)
        check("a_registry_zero", out["skill_registry_rows_new_tools"] == 0)
        check("a_receipts_zero", out["run_receipts"] == 0)
        check("a_sources_rows", out["sources_rows"] == 1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # Case B: round-17 artifacts committed -> every presence reads 1.
    tmp = Path(tempfile.mkdtemp(prefix="measure-r17-selftest-b-"))
    try:
        files = dict(FIXTURE_ANCHORS)
        files["corpus/QUALITY.md"] += "| 19 | r17 rule | l | — |\n"
        files["corpus/README.md"] = FIXTURE_ANCHORS["corpus/README.md"].replace(
            "- 2026-10-20-r16-go-selection",
            "- 2026-10-20-r16-go-selection\n- 2026-10-20-r17-go-carrier-diagnostics",
        )
        files["SKILL.md"] += (
            "| r17-carrier-run | tool / kaidoku | `python3 -I "
            ".ufo/waves/round-17/tools/carrier-run.py` | x | y |\n"
        )
        files["SCORECARD.md"] = FIXTURE_ANCHORS["SCORECARD.md"].replace(
            "|---|---|---|---|",
            "|---|---|---|---|\n| retained REA Ghidra-session log capture |"
            " c | p | round-17 |",
        )
        files[f"{W}/tools/pins.py"] = "# pins\n"
        files[f"{W}/tools/retain.py"] = "# retain\n"
        files[MEASURE_PATH] = "# measure\n"
        files[CONTROLS_PATH] = "# controls\n"
        files[R17_ENTRY] = "# r17 diagnostics\n"
        files["corpus/knowledge/2026-10-20-r16-go-selection.md"] = "# r16\n"
        files[f"{W}/runs/shfmt/receipt.json"] = "{}\n"
        files[f"{W}/runs/esbuild/receipt.json"] = "{}\n"
        rev = _git_fixture(tmp, files)
        out = census(tmp, rev)
        check("b_two_tools", out["tools_present"] == 2)
        check("b_tools_pins", out["tools"]["pins.py"] == 1)
        check("b_tools_absent", out["tools"]["compare.py"] == 0)
        check("b_measure_one", out["measure_py"] == 1)
        check("b_controls_one", out["controls_py"] == 1)
        check("b_knowledge_one", out["C2_knowledge_entry"] == 1)
        check("b_quality19_one", out["C1_quality_row19"] == 1)
        check("b_capability_one", out["C2_scorecard_capability_row"] == 1)
        check("b_registry_one", out["skill_registry_rows_new_tools"] == 1)
        check(
            "b_registry_name",
            out["skill_registry_new_tool_names"] == ["r17-carrier-run"],
        )
        check("b_receipts_two", out["run_receipts"] == 2)
        check("b_mapped", out["mapped"] == 2)
        check("b_missing_empty", out["missing"] == [])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if failures:
        print(f"SELFTEST: FAILED cases={cases} failures={failures}")
        raise SystemExit(1)
    print(f"SELFTEST: CLEAN cases={cases}")


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        selftest()
        return
    if len(sys.argv) != 2:
        fail("usage: python3 -I measure.py <revision>")
    revision = resolve(ROOT, sys.argv[1])
    result = {
        "revision": revision,
        "argv": list(sys.argv),
        "orig_argv": list(getattr(sys, "orig_argv", sys.argv)),
    }
    result.update(census(ROOT, revision))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
