# ExecReproC2 — independent reproduction of R100-C2 (registry self-test count truth)

Seat: ExecReproC2 (executor, leaf). Item: independent reproduction of R100-C2 only (C1 is not this item).
Revisions: B0 = 6371c88633f6ce6692eaeff17e256b80ad21ece0; freeze F = 8e24c29a37ca81a0bd1ff5ec73c96a949885322e;
A2 = cbd224ef9b9d2271f415d823bdc4d1e70a0d281c. Lane `HEAD` at run time = cbd224ef (= A2; lane did not advance during the runs).
Lane advanced after the runs to b0a7bb8c (round-100 C1 knowledge; SKILL.md +4 lines, registry rows added). Not re-run against b0a7bb8c; all results above are pinned to A2.
Supporting files: `.ufo/waves/round-100/w1/ExecReproC2/` (receipts, outputs, parser/driver/sweep scripts).

## Verdict
R100-C2 **reproduces**. Frozen counter at A2 and at the lane tip: `rows 93; claimed 93 of 93; green 93 of 93; counted 93 of 93; agree 93 of 93; mismatches 0`, exit 0.
Base control at B0 reproduces: `agree 86 of 93; mismatches 7`, exit 1. The seven mismatched rows are exactly the seven corrected rows.
The tools themselves already printed the corrected counts at B0; the defect was prose only. My independent runs of the seven tools give the same printed counts at B0 and A2.
Five findings (section 6) concern rows outside the frozen 93 and the wording of the registry; none changes the C2 label.

## 1. Frozen command (exit, label)
| # | command (cwd = clone of the stated rev, counter bytes from freeze) | exit | label |
|---|---|---|---|
| 1 | `python3 -I -B clone-a2/tools/round-100/registry-selftest-truth.py --selftest` | 0 | `SELFTEST cases=22 failures=0` (22 PASS lines) |
| 2 | `python3 -I -B tools/round-100/registry-selftest-truth.py --root clone-a2 --rev cbd224ef… --work W --json-out R` | 0 | `rows 93; claimed 93 of 93; green 93 of 93; counted 93 of 93; agree 93 of 93; mismatches 0`, `met True` |
| 3 | same, `--root clone-tip --rev HEAD` (HEAD = cbd224ef) | 0 | identical label |
| 4 | same, `--root clone-b0 --rev 6371c886…` | 1 | `… agree 86 of 93; mismatches 7`, `met False` |

Notes on row 4 and row 1:
- The counter script is added at the freeze commit, so it is absent from the B0 tree. `--selftest` at B0 could not run (`can't open file … clone-b0/tools/round-100/…`, rc 2). For the B0 control I ran the freeze-era counter from the A2 clone against `--root clone-b0`.
- Counter identity: sha256 of the counter in my A2 clone = `496a4979ecd6be4e…`, equal to the L1 receipt `counter_sha256`. `git diff --stat F A2 -- tools/round-100/registry-selftest-truth.py` is empty (unchanged since freeze).
- My A2 label equals the L1 receipt `c2-at-cbd224ef….json` label exactly (`label` compare: True).
- My B0 label equals the stored base control `.ufo/waves/round-100/pre/c2-do-nothing-at-base.json` label exactly (compare: True; exit 1 both).
- The seven rows at B0 that the counter flags: attest 15→18, record 9→10, packed-elf 31→32, seam-probe 7→9, record-audit 17→18, plan-command 3→7, upx-field-value-repair 16→22 (same set as the seven corrected rows).

## 2. The seven corrected rows, run by my own invocations (not the counter)
Each tool's documented argv from its SKILL.md registry cell, run in a clone; `rc` and the printed count copied from its stdout.

| row | tool | documented argv (abbrev) | A2 rc / printed | B0 rc / printed | prose before | corrected to |
|---|---|---|---|---|---|---|
| L39 | tools/round-46/attest.py | `--selftest --root . --freeze HEAD --rev HEAD` | 0 / `cases=18 failures=0` | 0 / `cases=18` | 15 | 18 |
| L45 | tools/round-47/record.py | `--selftest --root . --rev <R>` | 0 / `cases=10 failures=0` | 0 / `cases=10` | 9 | 10 |
| L94 | tools/round-71/packed-elf.py | `--selftest` | 0 / `"cases": 32` | 0 / `"cases": 32` | 31 | 32 |
| L95 | tools/round-71/seam-probe.py | `--selftest` | 0 / `"cases": 9` | 0 / `"cases": 9` | 7 | 9 |
| L126 | tools/round-76/record-audit.py | `--selftest` | 0 / `"cases": 18` | 0 / `"cases": 18` | 17 | 18 |
| L127 | tools/round-76/plan-command.py | `--root . --rev <R> --work W --selftest` | 0 / `"cases": 7` | 0 / `"cases": 7` | 3 | 7 |
| L170 | tools/round-89/upx-field-value-repair.py | `--selftest` | 0 / `SELFTEST cases=22 failures=0` | 0 / `SELFTEST cases=22` | 16 | 22 |

All seven agree with the corrected prose. Outputs: `seven/` and `selftest` copies in the supporting directory.

## 3. Whole-registry sweep at A2 (own parser, `parse_registry.py`)
- SKILL.md `<!-- instrument-registry v2 -->` block: 186 rows, 0 duplicate paths, every row's tool file exists at A2.
- 50 rows have no stated case count and a self-test cell mentioning `--selftest`/`selftest`. Of these, 26 name a runnable `--selftest`-style argv; 24 say `none`/`no --selftest`/`bad-argument probe only`.
- I ran the first 25 of the 26 (registry order, lines 11–184), each from its own cell argv, `python3 -I -B`, clone A2, scratch `runs/rowNN/`, 300 s timeout. Row 186 (`tools/round-97/kill-rule-v3.py`) was the 26th and is not run.

| line | tool | rc | printed count | prose count | notes |
|---|---|---|---|---|---|
| 11 | round-41/gen-squashfs.py | 0 | 71 | 71 checks | match |
| 12 | round-41/heldout-gen-v3.py | 0 | 12 checks | 12 checks | match |
| 16 | round-41/sqfs-list.py | 0 | 16/16 | — | |
| 21 | round-42/c2-counter.py | 0 | 79 | — | |
| 23 | round-42/heldout-gen-v4.py | 0 | 17 checks | 17 checks | match |
| 27 | round-42/sqfs3-oracle.py | 0 (fresh `--work`) | none (`0 failure(s)`) | 0 failures | **second run in the same `--work` → rc 1 `FileExistsError`** (finding F5) |
| 29 | round-43/c1-counter.py | 0 | 91 | — | one run timed out at 300 s under host load; clean rerun rc 0 `cases=91` |
| 31 | round-43/heldout-gen-v4r43.py `--selftest-tuple` | 0 | 17/17 | 17 of 17 | match |
| 35 | round-44/c2-counter.py | 0 | arms 24, ok true | 24 arms | match |
| 42 | round-46/registry.py `--selftest --root . --freeze 0 --rev 0` (literal) | 0 | 12 | — | literal `0` placeholders accepted |
| 47 | round-48/record2.py | 0 | none (parser blocks only) | parser cases only | no count printed |
| 49 | round-49/c1-controls.py | 0 | 11 | — | |
| 50 | round-49/c1-oracle.py | 0 | 24 | — | |
| 60 | round-50-c3/sqfs-triage-v5.py | 0 | 18 | count "in freeze receipt" | |
| 61 | round-51/census3.py | 0 | 20 | — | |
| 64 | round-53/r53-record.py (`python -X utf8 -I -B`) | 0 | 32 | — | |
| 104 | round-72/capsule-audit.py | 0 | 13 | "exercises it" | pinned row file differs (F2) |
| 141 | round-81/strictness-battery.py | 0 | 11 | "eleven cases" | match |
| 142 | round-82/conjunction-gate.py `--cli-selftest` | 0 | 2 cases, 0 failures | — | |
| 143 | round-82/printed-command.py `--cli-selftest` | **1** | 2 cases, 1 failure (`printed-green`, `SCRIPT_PIN_MISMATCH`) | — | **red at A2 and at B0** (F4) |
| 144 | round-82/cli-fixtures.py `--selftest` | **1** | 4 cases, 1 failure (`printed-green`) | — | **red at A2 and at B0** (F4) |
| 145 | round-83/attribution-audit.py | 0 | 2 | — | |
| 146 | round-83/source-bind.py | 0 | 10 case lines | "six isolated cases, twice each" | **prose ≠ printed** (F3) |
| 155 | round-90/control-cheat-repack.py `--selftest` | **2** | argparse: `--in, --out are required` | `--selftest` alone | **prose ≠ argparse** (F1) |
| 184 | round-97/depth-blocks-v4.py | 0 | 8 | — | |

Counts are as printed by each tool. "—" means the cell states no count and the tool printed one anyway.

## 4. Prose vs argparse (flags and exit codes)
Static sweep (`sweep_flags.py`, regex over `add_argument`): 27 rows flagged. Each was checked by hand:
- **Real mismatch:** row 155 (F1).
- **Real mismatch of target:** row 104 (F2).
- **Real mismatch of count:** row 146 (F3).
- Prose negations, correct as written (`none` / `no --selftest`): rows 7, 15, 20, 28, 51, 52, 53, 79, 176, 179, 180, 181, 182, 185, 188, 189, 191, 193–196.
- False positives: row 6 (`--tools` registered via `ap.add_argument(k)` loop); row 61 (`--selftest` in a `mutex` loop, runs and prints 20); row 112 (`--check-receipt` lives in `tools/round-73/packed-elf.py` line 1384, the cell says so); row 30 and row 32 (`--help` is argparse built-in).
- Exit codes checked against bad-argument probes (my runs, in clone A2): row 7 `c1-run.sh` no-args and `--bogus` rc 2; row 19 `c1-run.sh` no-args rc 2; row 20 `c2-controls.py` no-args and `--bogus` rc 2; row 30 `c2-score-r43.py` `--help` rc 0 and `--bogus` rc 2; row 32 `verify-copies-r43.py` `--help` rc 0 and no-args rc 2. All match the cells.
- Row 41 (gate.py): its cell says `registry.py --selftest` needs `--root --freeze --rev`. Confirmed: bare `registry.py --selftest` rc 2 (`the following arguments are required: --root, --freeze, --rev`); with them rc 0 `cases=12 failures=0`.

## 5. Independent verdict for C2
Reproduced. Frozen label at A2 and tip equals the L1 receipt; base control at B0 equals the stored control; the seven corrected rows print the corrected counts at both revisions.
I did not find any seven-row prose mismatch remaining at A2.

## 6. Findings (outside the frozen 93; none changes the C2 label)
- **F1 (row 155, `tools/round-90/control-cheat-repack.py`).** Cell: `python3 -I -B tools/round-90/control-cheat-repack.py --selftest`. Argparse requires `--in` and `--out` (`ap.add_argument("--in", required=True)`, `--out`), so the documented invocation exits 2 before the self-test runs. The row's self-test is not runnable as written.
- **F2 (row 104, `tools/round-72/capsule_audit.py`).** The pinned row path is the library module (blob c309b3c…), which has no `--selftest` argparse entry. The cell runs `tools/round-72/capsule-audit.py` (a different blob 36900c2…, rc 0, `"cases": 13`). The cell says that script "exercises it"; the pin and self-test target are not the same file.
- **F3 (row 146, `tools/round-83/source-bind.py`).** Cell says `six isolated cases, twice each`. Self-test printed 10 case lines (`selftest …: ok rc=[…]`), two invocations each. Could be 6 CLI cases plus 4 helper cases; not verified from source (`[INFERENCE]`).
- **F4 (rows 143 and 144, round-82 `printed-command.py` and `cli-fixtures.py`).** Both documented self-tests exit 1 at A2 and at B0 (2 cases / 1 failure and 4 cases / 1 failure, both on the `printed-green` arm: `SCRIPT_PIN_MISMATCH`). The cells state no exit code, so this is a silent red, not a prose mismatch. Not in the frozen 93, so not scored.
- **F5 (row 27, `tools/round-42/sqfs3-oracle.py`).** Not idempotent: a second `--selftest` in the same `--work` tree exits 1 with `FileExistsError: apple.txt`. The cell does not say `--work` must be fresh.

## 7. Limits and environment
- Ran the frozen command at B0, A2 and tip (counter from the freeze commit; sha256 pinned and equal to L1). I did not re-derive the frozen 93-row population independently; only the seven corrected rows and the 25 no-count rows were run by my own driver.
- Row 29 timed out once (300 s) under concurrent host load; clean rerun passed. Counted as environment noise.
- Row 186 not run (25-row cap).
- Static flag sweep is regex-based; loop-registered flags are false positives (see section 4).
- Row 41 (gate.py) is scored by the frozen counter through `registry.py` argv (the frozen population's `_pop` entry for gate.py). Noted, not disputed.
- No tools installed or upgraded. Python 3.14.8 (`/usr/bin/python3`), `python` present (`/usr/bin/python`). No pacman use.
- Lane: read-only git only (`log`, `rev-parse`, `diff --stat`, `ls-tree`). No lane file edited outside this report and its supporting directory. Clones and runs were under `/fast/scratch/hyaku/kaidoku-r100/ExecReproC2/` and removed at the end.
- Other peers' scratch and receipts were not read.

## Files (supporting dir `.ufo/waves/round-100/w1/ExecReproC2/`)
- `c2-frozen-{a2,tip,b0}.txt`, `c2-{a2,b0}.json`, `c2-selftest-a2.txt`: frozen command outputs.
- `rows.json`, `sweep-a2.json`: parser and static sweep output.
- `parse_registry.py`, `run_selftests.py`, `sweep_flags.py`: my scripts (not the counter).
- `selftests-25-first-run.json`, `selftests-25-second-run.txt`, `selftest-stdout/row*.{stdout,stderr}.txt`, `*.rc`: 25-row runs.
- `clean-reruns/`: rows 27 and 29 rerun from clean scratch; B0 runs of rows 143 and 144.
- `seven/`, `bogus-argv-probes/`, `registry-46-literal-args`: corrected-row and probe outputs.

verdict: R100-C2 reproduces at A2/tip (`mismatches 0`, exit 0) and its B0 control (`mismatches 7`, exit 1) matches; 5 non-scored findings (F1-F5).
