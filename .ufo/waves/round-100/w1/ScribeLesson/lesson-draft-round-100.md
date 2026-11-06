# Draft — `corpus/lessons/round-100.md` `## Mistakes` (seat ScribeLesson, round 100)

Draft only: this file lives in the wave directory, not in `corpus/`. The lane integrator copies
what it accepts. Every number below was run by this seat; the receipts are in this directory.

## Mistakes

Each row: class · evidence pointer · captured-by · fix (and whether the fix is shown able to fail).

- **M100-a · a regex that reads a date's day number as a case count, and a flag's argument as a
  claim (own, this round, caught before the freeze).** The C2 counter's first draft took the first
  `(\d+)\s+cases` / `cases[=: ]+(\d+)` match in a registry cell, so `green 2026-10-28 cases=12
  failures=0` was read as **28** cases and `--min-pristine-cases 38` was read as a **38**-case
  claim. The frozen bytes fix it with negative lookbehind in both patterns
  (`tools/round-100/registry-selftest-truth.py:60-61`:
  `(?<![\w./-])(\d+)(?:/\d+)?\s+(?:selftest\s+)?cases\b|(?<![\w-])cases[=: ]+(\d+)` and
  `(?<![\w-])cases["'=: ]+(\d+)|(?<![\w./-])(\d+)/\d+ cases\b|(?<![\w./-])(\d+) cases\b`), and the
  frozen selftest pins both (`claim-date-not-count` want 12, `claim-flag-not-count` want `None`;
  `.ufo/waves/round-100/pre/c2-selftest.txt` lines 7-8, both PASS). The same class exists on the
  observed side: `showcases=4` and `run 2026-10-28 cases=4` were read as counts 4 and 28
  (`obs-not-showcase`, `obs-date-not-count`; frozen receipt lines 11 and 16). Captured-by: the
  counter's own `--selftest` before the freeze (the two pinning cases are in the frozen bytes, so
  the defect was never in a committed revision). Fix: the lookbehind, with each of the four
  lookbehinds independently pinned by one selftest case. **Shown able to fail:** yes, per-lookbehind.
  Removing only the number-guard from `CLAIM_RE` → `FAIL claim-date-not-count got=28 want=12`,
  `SELFTEST cases=22 failures=1`, exit 1 (`claim-re-naive-selftest.txt`); removing only the
  `cases`-guard from `CLAIM_RE` → `FAIL claim-flag-not-count got=38 want=None`, failures=1, exit 1;
  removing the `cases`-guard from `OBS_RE` → `FAIL obs-not-showcase got=4 want=None`; removing the
  number-guard from `OBS_RE` → `FAIL obs-date-not-count got=28 want=4`. End-to-end: running the
  whole counter with the unguarded `CLAIM_RE` at `cbd224ef` gives
  `agree 92 of 93; mismatches 1` exit 1, the false mismatch being the live row
  `tools/round-46/gate.py` (claimed 28 vs counted 12) —
  `.ufo/waves/round-100/w1/ScribeLesson/c2-naive-claim-re-at-a2.json`. The defective pre-freeze
  draft itself is **not** recoverable from the lane (all three pre-freeze sibling commits
  `93a35286d`, `d34d53748`, `e6e9f724c` carry the frozen counter bytes, sha256
  `496a4979ecd6be4e50db21fdca3fec8bc5f427aad85014acf06bc7be6fa6e1f4`), so the defect is shown
  only by mutation, not by a committed artefact.

- **M100-b · seven registry rows stated a self-test case count the tool does not print (round-99
  lesson named limit 1, L1/L6; own, this round).** The round-99 counter checked that a row exists
  and carries a pinned sha256 (presence and shape), not that the prose is true; the counts were
  hand-written and drifted. The seven (stated→printed at base `6371c886`): `tools/round-46/attest.py`
  15→18, `tools/round-47/record.py` 9→10, `tools/round-71/packed-elf.py` 31→32,
  `tools/round-71/seam-probe.py` 7→9, `tools/round-76/record-audit.py` 17→18,
  `tools/round-76/plan-command.py` 3→7, `tools/round-89/upx-field-value-repair.py` 16→22.
  Provenance (`git log -L` / `git blame`, read-only; `registry-row-provenance.txt`): the rounds
  that wrote the rows are **46** (`47b5e265`), **47** (`e856beb5`), **71** (`c46ea96b`, both rows),
  **76** (`821d9eb6`, both rows) and **89** (`5a46542a`). The seven are not one defect but three:
  (i) **two rows were never true** — at the commit that wrote them, `tools/round-71/packed-elf.py`
  printed `"cases": 32` and `tools/round-71/seam-probe.py` printed `"cases": 9`, and neither tool
  changed afterwards (`git log c46ea96b..6371c886 -- <path>` is empty); the row said 31 and 7.
  (ii) **four rows were true when written and the tool was edited under them** — `round-47/record.py`
  printed `cases=9` at `e856beb5` and 10 after four same-round edits (`62e33f7dd`…`07d2894ea`);
  `round-76/record-audit.py` printed 17 at `821d9eb6` and 18 after `a89089306`/`98407fadb`;
  `round-76/plan-command.py` printed 3 then 7; `round-89/upx-field-value-repair.py` printed
  `SELFTEST cases=16` at `5a46542a` and 22 after `7edab6ae5`/`bc0e0c20c`.
  (iii) **one row's cell held two counts** — `tools/round-46/attest.py` read
  `15 cases at the 3182047 and 50862e4a bytes, 16 from the F3 repair at 65678df0 onward`; the tool
  printed 16 at that commit (`332f48849` then took it to 18), but the first-match rule takes the
  stale 15. Captured-by: the round-100 counter `tools/round-100/registry-selftest-truth.py`, which
  runs each row's documented self-test at the measured revision and compares the printed count
  (base control: `agree 86 of 93; mismatches 7`, exit 1 — re-derived here, `c2-base-repro.json`).
  Fix: the seven rows corrected to the printed counts at `cbd224ef` (A2), and the counter as the
  standing check. **Shown able to fail:** yes — the counter at base is red (mismatches 7, exit 1,
  the seven named), and the three forgery controls each stay red: F-drop `claimed 86 of 93;
  mismatches 7` exit 1, F-tool `agree 87 of 93; mismatches 7` exit 1 (a tool edited to print the
  stale 16 is refused by the pin atom), F-dup `claimed 86 of 93; mismatches 7` exit 1
  (`.ufo/waves/round-100/pre/c2-forgery-controls.txt`). At A2 the same command is
  `rows 93; claimed 93 of 93; green 93 of 93; counted 93 of 93; agree 93 of 93; mismatches 0`,
  exit 0 (`c2-a2-repro.json`). Named limit to carry: the counter binds the row to the count the
  tool prints *at the measured revision*; it cannot see a row that will drift again, and class
  (i)/(iii) would have been caught by any counter that ran the row's own tool once.

- **M100-c · a rejection that was never registered, and a search-log note that was never written
  (round-99 closure defect 1; own, carried).** `corpus/lessons/round-99.md` `## Gate` records the
  S326 admission and the S324 re-read and **no rejection**, and the round-99 ScoutSources sweep
  (GitHub issue API: `"invalid overlay size"` 0 hits; `"overlay size"` 2 hits; `overlay truncated`
  0 hits; `doc/upx-doc.txt` at v5.2.0 contains no `invalid`) never reached `corpus/SOURCES.md`
  `## Search log`; the drafted rejection exists only as
  `.ufo/waves/round-99/w1/ScoutSources/draft-s327-candidate-rejection.md` (tracked in the lane).
  Measured at `b0a7bb8ca`: the round-99 lesson `## Gate` table has 4 lines (header, separator,
  S326, S324) and 0 occurrences of a rejection, and `corpus/SOURCES.md` `## Search log` contains
  **no** round-99 or round-100 note (`grep -cE "round 99|round 100"` → 0), the newest note being
  round 76. Captured-by: the round-99 closure (`corpus/lessons/round-99-verifier-spotcheck.md` §5
  defect 1). Fix: append the rejection to the round-100 lesson `## Gate` and a round-99/100
  search-log note to `corpus/SOURCES.md`. **Shown able to fail:** not by any committed gate — the
  search-log atoms bind rounds 73/74/75 only (`tools/round-74/record-audit.py:372-379` D10,
  `tools/round-76/record-audit.py:655-666` D23); no instrument mentions rounds 99 or 100. A
  D10-shaped probe of the same shape (`scratch/probe/searchlog_probe.py`) returns `absent` rc=1 for
  `round 99` and `round 100` on the current corpus and `present` rc=0 on a copy with the note
  appended, so the fix is verifiable but only by a probe, not by a committed counter.

- **M100-d · a census warning claimed as pre-existing when the round added one (round-99 closure
  defect 2; own, carried).** The round-99 report §Sources says the end census has "only the W04
  warnings that were already there", and the round-99 lesson census line states only row counts
  (230→231) with no warning figure. Measured: round-99 `pre/census-start.txt` has **32** W04 lines,
  `l1/census-end.txt` has **33**; the diff is exactly one added line,
  `kaidoku W04 S326 duplicate url raw.githubusercontent.com/upx/upx/v5.2.0/src/packer.cpp across
  scopes` — the same URL as S310, a new scope. So the report's claim is false. Captured-by: the
  round-99 closure (§5 defect 2). Fix: record the correction and state whether the S326/S310 scope
  split is deliberate — it is: S310's scope is the header-arithmetic sanity gate and explicitly
  excludes the checksum comparison (S308), S326's scope is the overlay check; two tier-A mined
  rows on one file with distinct scopes is the corpus convention (the round-18 S033/S032 precedent),
  so the W04 is expected and the *figure* is the defect. **Shown able to fail:** partially — the
  QUALITY-187 sweep `sweep-w04.sh` compares a stated "N W04" against the receipt's line count and
  does fail when a number is written (`DISAGREE: report 33 != receipt 34` rc=1; `agree: report 34
  == receipt 34` rc=0), but on the round-99 report and on the round-99 lesson it exits 2
  `nothing checked`: neither states a number, so a qualitative claim like "only the warnings that
  were already there" is invisible to it. The lesson's own census line must carry the count.
  **The same shape recurs this round and is open:** the round-100 census start has 33 W04 lines and
  the current census has **34** — the added line is
  `kaidoku W04 S327 duplicate url raw.githubusercontent.com/upx/upx/v5.2.0/src/packhead.cpp across
  scopes`, the same URL as S308 (`census-now.txt` vs `.ufo/waves/round-100/pre/census-start.txt`).
  A round-100 census claim of "the same warnings as before" would repeat M100-d; the round-100
  end-census figure is 34.
