#!/usr/bin/env python3
"""Count round-16 observables from immutable lane Git objects, not the worktree.

Usage: python3 -I .ufo/waves/round-16/measure.py <revision>

Reads only committed bytes at <revision> through `git show` and `git ls-tree`.
Every C1/C2 field is a bounded presence proxy: 1 means the named file or
wording exists in that commit, never that it is sourced, correct, admitted, or
that any target, provider, fixture, or gate was exercised. Map and source
figures are bookkeeping counts, not domain coverage. Exit 0 after a completed
census; 2 on usage or a missing structural anchor. This script computes no
verdict and no semantic pass.
"""
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

C1_TOOL = ".ufo/waves/round-16/selection.py"
C1_FIXTURES = ".ufo/waves/round-16/selection-fixtures.json"
C1_SELFCHECK = ".ufo/waves/round-16/selfcheck.py"
C2_CONTROLS = ".ufo/waves/round-16/controls.py"
R15_ENTRY = "corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md"
SUPPLEMENT_BASELINE = ".ufo/waves/round-15/boundary-fixtures/expected.json"
HISTORICAL_DATE = "2026-10-15"
ROW18 = re.compile(r"^\|\s*18\s*\|")
QUOTE_ROW = re.compile(r"^\|\s*quote-fidelity\s*\|")
INSTRUCTIONS_BOX = re.compile(r"^- \[~\] Instructions executable by an agent")
SOURCE_ROW = re.compile(r"^\|\s*S\d{3,}\s*\|")
MAP_ENTRY = re.compile(r"2026-10-\d{2}-[a-z0-9-]+")
R16_ENTRY_STEM = re.compile(r"^2026-10-\d{2}-r16-.*selection")
CORRECTION_HEADING = re.compile(r"(?m)^## Round-16 correction[^\n]*$")
ABS_R15_SCRIPT = re.compile(
    r"/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*/\.ufo/waves/round-15/"
    r"snapshot-inventory\.py"
)
ISOLATION_FLAG = re.compile(r"(?:^|[\s`])(?:python3?\s+)?-I(?:[\s`]|$)")


def git(*args):
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], text=True, encoding="utf-8"
    )


def fail(message):
    print(f"measure.py: {message}", file=sys.stderr)
    raise SystemExit(2)


def main():
    if len(sys.argv) != 2:
        fail("usage: python3 -I measure.py <revision>")
    try:
        revision = git(
            "rev-parse", "--verify", f"{sys.argv[1]}^{{commit}}"
        ).strip()
    except (subprocess.CalledProcessError, OSError) as error:
        fail(f"cannot resolve commit {sys.argv[1]!r}: {error}")

    def get(path):
        try:
            return git("show", f"{revision}:{path}")
        except (subprocess.CalledProcessError, OSError):
            fail(f"cannot read {path} at {revision}")

    paths = set(git("ls-tree", "-r", "--name-only", revision).splitlines())
    quality = get("corpus/QUALITY.md")
    readme = get("corpus/README.md")
    sources = get("corpus/SOURCES.md")
    skill = get("SKILL.md")
    shonen = get("SHONEN.md")
    r15_entry = get(R15_ENTRY)

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

    row18 = next((line for line in quality.splitlines() if ROW18.match(line)), "")
    quote_row = next(
        (line for line in skill.splitlines() if QUOTE_ROW.match(line)), ""
    )

    # The named r15 correction appends a `## Round-16 correction …` section to
    # the r15 knowledge entry (append-only convention, cf. round-14 lesson
    # `Round-15 correction — virtual-dispatch advisory`,
    # corpus/lessons/round-14.md:144). Anchoring on the exact heading avoids
    # the older `Named correction:` reference at R15_ENTRY:39 consuming the
    # appended section or unrelated `-I`/absolute-path text producing a hit.
    # Presence additionally requires the recorded isolation flag `-I` and an
    # absolute (rooted) path to the round-15 probe script.
    heading = CORRECTION_HEADING.search(r15_entry)
    correction_section = r15_entry[heading.start():] if heading else ""
    correction_ok = bool(
        correction_section
        and ISOLATION_FLAG.search(correction_section)
        and ABS_R15_SCRIPT.search(correction_section)
    )

    shonen_instructions_line = ""
    for index, line in enumerate(shonen.splitlines()):
        if INSTRUCTIONS_BOX.match(line):
            following = shonen.splitlines()[index + 1 : index + 2]
            shonen_instructions_line = following[0] if following else ""
            break

    r16_entries = sorted(
        stem for stem in knowledge if R16_ENTRY_STEM.match(stem)
    )

    result = {
        "revision": revision,
        "C1_round16_knowledge_entry": int(bool(r16_entries)),
        "C1_round16_knowledge_entry_files": r16_entries,
        "C1_selection_probe": int(C1_TOOL in paths),
        "C1_selection_fixtures": int(C1_FIXTURES in paths),
        "C1_selection_selfcheck": int(C1_SELFCHECK in paths),
        "C2_quality_row18": int(bool(row18)),
        "C2_supplement_baseline_in_quote_fidelity_row": int(
            bool(quote_row) and SUPPLEMENT_BASELINE in quote_row
        ),
        "C2_named_r15_correction_isolated_absolute_recheck": int(
            correction_ok
        ),
        "C2_shonen_line_names_historical_round": int(
            bool(shonen_instructions_line)
            and HISTORICAL_DATE in shonen_instructions_line
            and "this round" not in shonen_instructions_line.lower()
        ),
        "C2_shonen_line_still_says_this_round": int(
            "this round" in shonen_instructions_line.lower()
        ),
        "C2_controls_script": int(C2_CONTROLS in paths),
        "knowledge_files": len(knowledge),
        "mapped": len(knowledge & mapped),
        "missing": sorted(knowledge - mapped),
        "dangling": sorted(mapped - knowledge),
        "sources_rows": len(rows),
        "tiers": dict(sorted(Counter(cell(row, 4) for row in rows).items())),
        "statuses": dict(sorted(Counter(cell(row, 8) for row in rows).items())),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
