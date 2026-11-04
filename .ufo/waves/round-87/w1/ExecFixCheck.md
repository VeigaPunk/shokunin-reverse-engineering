# ExecFixCheck — round 87, mistake-fix check for V86-2 (S305 written with no opened document)

Candidate: `.ufo/waves/round-87/w1/ExecFixCheck/candidate/tools/round-87/registry-opened-check.py`
sha256 `c579d111a06c25fa3940fd2393db011a0ae1dd963f3257b86e1e71c9062fe670`. Not integrated at the production path; that is the L1's step.

## Behavior
- Reads `corpus/SOURCES.md` at `--base` and `--rev` with `git show REV:corpus/SOURCES.md`. Scores rows (`^ {0,3}\| S[0-9]{3,} \|`) that are new at `--rev`, or whose line text matches no `--base` row with the same id.
- Splits each row on unescaped pipes (GFM `\|` stays inside the cell). Flags per row:
  - `cells:N`: the row does not have 11 cells. The other checks are skipped for that row.
  - `opened`: cell 9 has no valid ISO date. Uses `datetime.date` validation, so `2026-13-40` is flagged.
  - `no-document`: cell 6 (anchor) **or cell 2 (source)** says no document was opened (`no document opened`, `not/never opened`, `unopened`, …).
  - `no-locator`: cell 2 has no URL, DOI, absolute or `~/` path, or relative path ending in a file extension. `S079/S080` id lists do not count as paths.
- Exit codes: 0 = clean; 1 = flagged (ids and flags in JSON on stdout); 2 = could not evaluate (`git show` failed or the table header is missing).

## Evidence (receipts in this dir)
- `selftest.txt`: `python3 <candidate> --selftest` ran 14 cases with `failures: 0` and rc 0. One case is the literal S305 row text.
- `r86-red.json`: `--root <lane> --base 2cf0b7ff93c698809bed321f7338276a22d6beb9 --rev 4cc03025e6d4f6f1e00b5e402fcc0180e6e730bc` gave **rc 1**. It scored S255 (re-open edit, clean) and S305, and flagged `S305: [no-document, no-locator]`.
- `base-clean.json`: `--base 99f8b6a8… --rev 99f8b6a8…` gave **rc 0**, with nothing scored.
- I also ran `--rev deadbeef` and got rc 2 (`invalid object name`). That output was not kept; it was scratch only.
- Calibration: every row at BASE 99f8b6a8 was scored against an empty table. 210 rows were scored and 2 were flagged: S305 (`no-document`, `no-locator`) and S115 (`no-locator`). S115's source cell is "7-Zip 26.04 BE v4 refusal — own-work (committed tool output)", which has no path. So on the existing registry the check gives 1 extra flag beyond S305. It is a real gap in that row's locator, not a parser error. Under normal diff mode S115 is never scored, because it is unchanged.

## Findings
- **The `opened` cell alone cannot fail on S305.** S305's opened cell is `2026-11-04` and its anchor cell begins "Opened 2026-11-04". The phrase "no document opened" is in its **source** cell, not the anchor cell. A check built only to the letter of the spec (opened date + anchor phrase) passes S305 on the date and anchor checks; only the source-cell locator check catches it. So the no-document phrase check covers both the source and anchor cells. This is a deliberate widening of the spec, and the selftest pins it.
- Limits: the check reads text only. It does not fetch URLs, check that paths exist, or match anchor quotes against documents. A row that names a locator it never opened still passes.

## Tooling
Nothing was installed or upgraded. Scratch `/fast/scratch/hyaku/kaidoku-r87/ExecFixCheck/` was removed with `rm -rf` (the trap did not fire because the shell was persistent), and `ls` confirmed it is gone. No VCS mutation.
