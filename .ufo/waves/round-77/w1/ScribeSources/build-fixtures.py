#!/usr/bin/env python3
"""Rebuild the two scratch census lanes used by ScribeSources (round 77).

Run from the lane root with a scratch dir as argv[1]:

    python3 -B .ufo/waves/round-77/w1/ScribeSources/build-fixtures.py /fast/scratch/hyaku/kaidoku-r77/ScribeSources

It produces, from the *current* `corpus/SOURCES.md` plus `rows-draft.md`:

  <scratch>/fix-r77repl-shokunin   the committed S289-S291 rows replaced by the drafts
  <scratch>/fix-r77app-shokunin    the drafts appended after the committed S289-S291 rows

Each fixture is a fake lane whose top-level entries and `corpus/` children are
symlinks to the real lane (so the census's E11 used-by check resolves) and whose
`corpus/SOURCES.md` is the only real file. Run the census with the fixture lane
directory as the argument, not with `--file`:

    TMPDIR=<scratch> bash ../scripts/sources-census.sh validate --today 2026-11-04 <scratch>/fix-r77repl-shokunin

`--file` into a bare scratch dir resolves used-by paths against that directory and
emits spurious E11 findings; that attempt is not evidence.
"""
import os
import shutil
import sys

LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
DRAFT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rows-draft.md")
MARKER = "\n## Paths\n"


def build(scratch, name, text):
    lane = os.path.join(scratch, "fix-r77%s-shokunin" % name)
    shutil.rmtree(lane, ignore_errors=True)
    os.makedirs(os.path.join(lane, "corpus"))
    for entry in os.listdir(os.path.join(LANE, "corpus")):
        if entry == "SOURCES.md":
            continue
        os.symlink(os.path.realpath(os.path.join(LANE, "corpus", entry)),
                   os.path.join(lane, "corpus", entry))
    for entry in os.listdir(LANE):
        if entry in ("corpus", ".git"):
            continue
        os.symlink(os.path.realpath(os.path.join(LANE, entry)), os.path.join(lane, entry))
    with open(os.path.join(lane, "corpus", "SOURCES.md"), "w", encoding="utf-8") as fh:
        fh.write(text)
    rows = sum(1 for line in text.split("\n") if line.startswith("| S"))
    print("%s rows=%d bytes=%d" % (lane, rows, len(text)))


def main():
    scratch = sys.argv[1]
    os.makedirs(scratch, exist_ok=True)
    with open(os.path.join(LANE, "corpus", "SOURCES.md"), encoding="utf-8") as fh:
        registry = fh.read()
    with open(DRAFT, encoding="utf-8") as fh:
        draft = fh.read()
    pre, post = registry.split(MARKER, 1)
    trimmed = [line for line in pre.split("\n")
               if not line.startswith(("| S289 |", "| S290 |", "| S291 |"))]
    replaced = "\n".join(trimmed).rstrip("\n") + "\n" + draft + MARKER + post
    appended = pre.rstrip("\n") + "\n" + draft + MARKER + post
    build(scratch, "repl", replaced)
    build(scratch, "app", appended)


if __name__ == "__main__":
    main()
