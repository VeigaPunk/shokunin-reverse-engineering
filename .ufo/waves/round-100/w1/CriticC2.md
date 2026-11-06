# CriticC2 — falsify R100-C2 (registry self-test count truth, 7 → 0)

Seat: CriticC2 (critic). Lane: kaidoku-shokunin, L1 KaidokuR100, round 100 attempt 1.
Revision used: A2 = cbd224ef9b9d2271f415d823bdc4d1e70a0d281c (lane `main` not advanced past it by me).
Scratch: /fast/scratch/hyaku/kaidoku-r100/CriticC2 (clone + fixtures; trap-deleted at exit).
Copied evidence: .ufo/waves/round-100/w1/CriticC2/ (receipts/, patches/, attacks.py).

## Verdict line

R100-C2 reaches its frozen label `rows 93; claimed 93 of 93; green 93 of 93; counted 93 of 93; agree 93 of 93; mismatches 0` with exit 0 on 7 of 7 admitted classes, singly and combined. The counter guarantees that the first count-looking token in the self-test column equals the printed count; it does not guarantee the registry's self-assessment is true. Seven named limits are admitted below.

## Commands and results (all run in the scratch clone or fixture clones)

| run | command (abridged) | label | exit |
|---|---|---|---|
| genuine A2 | `python3 -I -B clone/tools/round-100/registry-selftest-truth.py --root <clone> --rev cbd224ef… --work w-base --json-out base.json` | `rows 93; claimed 93 of 93; green 93 of 93; counted 93 of 93; agree 93 of 93; mismatches 0` | 0 (44 s) |
| ctl words-only | same, `--root fx/ctl-words-only --rev 32b5dd71…` | `… agree 92 of 93; mismatches 1` | 1 |
| f1 | `--rev 83b268da…` | full label | 0 |
| f2 | `--rev aecfc412…` | full label | 0 |
| f3 | `--rev c5e64061…` | full label | 0 |
| f4 | `--rev faeee5b1…` | full label | 0 |
| f5 | `--rev 7d873682…` | full label | 0 |
| f6 | `--rev 6d2338fa…` | full label | 0 |
| f7 | `--rev 85a579b2…` | full label | 0 |
| f8 combined | `--rev 87ceb1c3…` | full label | 0 |

Each fixture is a `git clone --shared` of the A2 clone, detached at A2, with one commit that changes only `SKILL.md` (`patches/*.patch`, `*.stat.txt`). Anchors were asserted to occur exactly once. The fixture commit SHAs are scratch identities, not claims (per lesson M99-j).

Control on the forgery mechanism: `ctl-words-only` replaces `10 cases` and `9 cases` in the record.py self-test cell with words only. The counter then records `claimed None` for that row and exits 1 with one mismatch. So a pure words count is caught; the admitted classes below are the ones that keep a digit-form count somewhere the counter reads first.

## Admitted forgeries (named limits)

Each row: the edit, the true value, and the result. All were scored by the frozen counter at the fixture commit with the frozen predicate, and each exits 0.

- **L1 — later wrong count in the same cell (first match wins).** `tools/round-46/attest.py` self-test cell (column 4): appended "a later re-run on 2026-11-05 printed 15 cases". The tool prints `cases=18` (genuine run: `ATTEST_SELFTEST: cases=18 failures=0` is the row's own claim; the counter's `counted` is 18). The cell's first `18 cases` matches; the later `15 cases` is never checked. Result: full label, exit 0 (f1).
  - Already present at A2 (not forged): the same cell carries "this cell said 15 cases at the 3182047 and 50862e4a bytes, 16 from the F3 repair" — labelled history, so not a false claim, but it shows the first-match rule is load-bearing.
- **L2 — count in words, digits elsewhere in the cell.** `tools/round-47/record.py`: "10 cases" → "fifteen cases" (true 10); the cell keeps `` `RECORD_SELFTEST: cases=10 failures=0` ``. `CLAIM_RE` skips "fifteen cases" (no digits) and takes `cases=10`. Result: full label, exit 0 (f2).
- **L3 — documented command and exit text are not checked.** `tools/round-47/record.py` self-test cell: documented command changed to `python3 -I -B tools/round-47/record.py --run-battery --rev <R>` and "exit 0" → "exit 2". Verified in the clone: that command exits 2 (`argparse: error: the following arguments are required: --root`, rc 2), and the genuine `--selftest --root . --rev HEAD` exits 0 with JSON `"failures": 0`. The counter runs its own frozen argv, never the row text. Result: full label, exit 0 (f3).
- **L4 — verdict-map and write-scope columns are not read.** `tools/round-47/record.py`: verdict map "0=met; 1=not met" → "0=not met; 1=met" (false: genuine run exits 0 when met); write scope "writes only the --json-out receipt" → "writes SCORECARD.md in place" (false: `tools/round-47/record.py` only reads `SCORECARD.md` at `--rev` via `gate.show`, its only write is the `--json-out` receipt; checked by grep of `open(`/`write_receipt`). Result: full label, exit 0 (f4).
- **L5 — count stated in the purpose column.** `tools/round-76/plan-command.py` purpose cell (column 1, not parsed for 7-cell rows): added "`--selftest` prints 4 cases" (true 7; the cell's column-4 "7 cases" is untouched, so the checked count still agrees). Result: full label, exit 0 (f5).
- **L6 — prose outside the registry markers.** `SKILL.md` after `<!-- /instrument-registry -->`: "Note: tools/round-47/record.py runs 12 cases." (true 10). The counter reads only text between the markers. Result: full label, exit 0 (f6).
- **L7 — a second row with a mangled key is invisible.** Inserted `` | `tools/round-47/record.py` (copy) | gate - copy | 0=met | `… --selftest` 3 cases | … `` before the real row. The key becomes `tools/round-47/record.py` (copy) (stripping `` ` `` only at the ends), so `rows` is not duplicated and the stale row is never read. Result: full label, exit 0 (f7).
- **Combined (f8):** all of f1–f7 applied to one commit (9 edits), with f3 applied before f2 so the anchors do not collide. Result: `rows 93; claimed 93 of 93; green 93 of 93; counted 93 of 93; agree 93 of 93; mismatches 0`, exit 0.

Not run (out of seat scope, not claimed): a tool edit that prints a stale count (pinned by sha, the lane's F-tool control covers it); the `--json-out` path; the `selftest()` of the counter itself.

## Observations at A2 (not forged; read from the unmodified lane bytes)

- Population rows are not uniform. `tools/round-69/packed-elf.py` has 8 cells (its owner is cell 7; the header says 7 columns); `tools/round-88/upx-chain-repair.py`, `tools/round-89/depth-blocks-v2.py`, `tools/round-89/upx-field-value-repair.py` have 2 cells. For short rows the counter joins cells 1..n and parses the purpose text. The counter's row atom accepts these shapes; the round-71 census grammar would name them, but C2 does not call it.
- Two rows with a count in column 1 or 4 besides the stated one: `tools/round-69/packed-elf.py` purpose "20 selftest cases" (agrees), `tools/round-92/upx-stop-boundary-search-repair.py` cells 3 and 4 both "6 cases" (agree).
- The `tools/round-46/attest.py` and `tools/round-47/record.py` cells contain labelled historical counts (`15 cases`, `9 cases`) after the true count; they are not false claims, but a later edit that removes the label would make them false without changing the label.

## Smallest safe correction (for the judge; not a re-freeze)

1. Collect every count-bearing token from all cells of a population row (not just cell 4), and require all of them to equal the counted value, or to be explicitly labelled history.
2. Reject word-form counts ("fifteen cases", "nine cases") in any count-bearing cell.
3. Compare the documented command text (`python3 -I -B tools/<path> ...`) to the frozen argv and require the stated exit text to be 0 when green.
4. Require exactly seven cells per population row and a backticked key with no trailing text; count cell-1 and cell-2 prose the same as cell 4.
5. Scan SKILL.md outside the markers for any `tools/round-N/x.py` followed by a count phrase, or check the whole file rather than the registry block.

## Limits of this seat

- I did not run the tool-pin control, the F-tool/F-dup controls, or C1. Only the C2 counter was exercised.
- I did not verify the self-test count of every one of the 93 rows beyond the frozen run; the genuine A2 receipt (`receipts/c2-a2-genuine.json`) is the evidence for them.
- No tools were installed or upgraded. No lane, MANIFEST, .ufo/state or fleet file was written; the only lane writes are this report and `.ufo/waves/round-100/w1/CriticC2/`.
