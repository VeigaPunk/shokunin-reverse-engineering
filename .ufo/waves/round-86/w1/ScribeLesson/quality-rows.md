# ScribeLesson — QUALITY.md rows 150 and 151 (draft for the L1)

Target file: `corpus/QUALITY.md`. Append at the end of the file, after Row 149 (the file's last row).
Style follows the existing appended-row form: a blank line, then

```
- **Row N (<title in the row's own words>).** <the criterion>. Evidence: <citations>. Sharpens <n>.
```

The two rows below are the ones the round-86 evidence supports. They are drafted here only; this
seat does not edit `corpus/QUALITY.md`.

---

- **Row 150 (a correction filed in prose leaves the record wrong where it is re-derived - the supersession row is the correction, and its count is re-derived by command).** A defect routed against a registry cell is corrected **in that cell's own record**, not in the lesson that narrates it: where the registry's own rule provides a supersession row, the correction is that row, its count is re-derived by the command that produces it at the revision the row names, and the prose correction points at the row instead of restating the number. A lesson is where a reader learns *that* a value was wrong; the record is where a reader learns *what the value is*, and only the record is read by the lane's own instruments. Fails when the routed defect is answered in a narrative file while the cell that states the value keeps its old wording, or when the corrected count is asserted in prose without the command that re-derives it from the committed bytes. Round-86 case, judged by this row: the round-85 correction for the S303 row was filed as prose in `corpus/lessons/round-85.md` (Corrections C-R2) while `corpus/SOURCES.md:219` still read "the registry already holds this URL in five scopes (S083/S090/S092/S119/S123)"; eight rows carry the URL and seven precede S303 (S079/S080/S083/S090/S092/S119/S123), and the round-85 commit `01f2d5193` changed no existing SOURCES cell (`git show 01f2d5193 -- corpus/SOURCES.md` shows one added row, no removed line). Evidence: `corpus/lessons/round-86.md` M86-1; `tools/round-86/record-agreement.py` atom `A1-s303-supersede-count`; `.ufo/waves/round-86/w1/ScribeLesson/sweep.txt` and `receipts/c1-at-base-rederived.json` (A1 false at BASE `2cf0b7ff93c698809bed321f7338276a22d6beb9`: "no row whose teaches opens `supersedes S303`"); `corpus/lessons/round-85.md` Corrections C-R2. Sharpens 149.

- **Row 151 (a registry row is a claim about behaviour - its entry command is executed and its declared exit observed, or the row is decoration).** An instrument-registry row that names a tool is a claim about that tool's behaviour, and it is admitted only when its entry command is **executed** and its **declared exit is observed** to match: the row's self-test cell names an argv on the tool's own path, that argv runs with no shell in a bounded child environment, and the exit the tool returns is the exit the row declares. A row that names a command the tool cannot honour, or whose declared exit the tool does not produce, is decoration - it is refused, not re-read. Fails when the row is scored by the presence of its text (the path exists, the exit digits are present, the verdict map's `0=`/`1=`/`2=` tokens appear) without the tool being run, when the executed command is not on the tool's path, or when the declared exit is copied from the row's own text rather than from the run. Round-86 case, judged by this row: the round-85 gate `tools/round-85/predicate-bind.py` was landed and left unregistered, so a reader of the lane's own checklist could not find or run it (`agreed 0/5` at BASE `2cf0b7ff93c698809bed321f7338276a22d6beb9`, every atom false, `.ufo/waves/round-86/pre/c2-at-base.json`); the counter that scores the row re-derives it by running the tool (`tools/round-86/gate-registry.py`, atoms `G2-exit-map-observed`, `G3-self-invocation`), and its weak forms are named in the wave's own attack receipts - a row whose self-test cell is `python3 -c "import sys; sys.exit(0)"` (no tool path) and a row whose verdict cell is prose containing `0=`/`1=`/`2=` both reach 5/5 while declaring nothing about the tool (`.ufo/waves/round-86/w1/ReviewerC2/receipts/Fa3-no-tool-path-python-c.json`, `Fb1-verdict-prose-tokens.json`). Evidence: `corpus/lessons/round-86.md` M86-2 and the round-86 Gate; `tools/round-86/gate-registry.py`; `.ufo/waves/round-86/pre/c2-at-base.json`; `.ufo/waves/round-86/w1/ReviewerC2/attack.md`. Sharpens 149.

---

## Notes for the L1 on these two rows

1. **Row 150's evidence pointer is committed.** `corpus/SOURCES.md:219`, `corpus/lessons/round-85.md`
   Corrections C-R2, `git show 01f2d5193 -- corpus/SOURCES.md`, and the BASE receipt
   `.ufo/waves/round-86/pre/c1-at-base.json` are all committed bytes at the declaration. The
   `sweep.txt` / `receipts/c1-at-base-rederived.json` pair is this seat's re-derivation of the same
   fact, under the wave tree.
2. **Row 150 sharpens 149, and does not rewrite it.** Row 149 says a counted scope is re-derived by
   the command that produces it; row 150 says the re-derivation must land in the *record* the reader
   re-derives, not only in the prose that narrates the correction. Rows 149 and 136 are left as
   written.
3. **Row 151 cites `corpus/lessons/round-86.md` M86-2**, a mistake id this seat's lesson draft
   reserves for the registry-row-is-decoration class; the row's evidence (the 0/5 BASE receipt and
   the reviewer's two false-green receipts) is committed or in the wave tree, and the reviewer's
   receipts are the executor's findings rather than this seat's own, so the L1 should confirm the
   citation resolves once the L1 lands the lesson.
4. **Row 151's criterion is a behaviour criterion, not a shape criterion.** It admits a row only on
   an observed exit, and it names the two shape-tests it refuses to accept in place of an
   observation (`python3 -c` in the self-test cell; verdict-map tokens without an exit map), so that
   the row cannot be satisfied by text that merely mentions the tool.
5. **Both rows cite the round-86 lesson id** (`corpus/lessons/round-86.md` M86-1 and M86-2) and a
   counter/receipt path (`tools/round-86/record-agreement.py` with
   `.ufo/waves/round-86/w1/ScribeLesson/receipts/`; `tools/round-86/gate-registry.py` with
   `.ufo/waves/round-86/pre/c2-at-base.json` and
   `.ufo/waves/round-86/w1/ReviewerC2/receipts/`), as the lane's row style requires.
6. **Next free numbers are 150 and 151**: `corpus/QUALITY.md` ends at Row 149
   (`grep -n '^- \*\*Row ' corpus/QUALITY.md | tail -1` → line 239), and no row 150+ exists.
