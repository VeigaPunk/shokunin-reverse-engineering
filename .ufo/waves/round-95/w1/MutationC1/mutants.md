# MutationC1 — mutate-run-revert of the round-95 instruments

Lane: kaidoku, round 95, attempt 1. Declaration commit `4bda1d1dd3788973f10e61212b70df18b3b14ea0`
(base `b5331db1fb0ce0bf93695ce1730cf831effef6a9`). Each mutant lives in its own fresh
`git clone --shared` of the lane, checked out at 4bda1d1d; the lane was never edited. Scratch was
removed after receipts were copied here.

## Baseline (unmutated clone at 4bda1d1d)

Pins precheck: `sha256sum -c .ufo/waves/round-95/pins.sha256` in the clone → 26 `OK`, exit 0.

| check | command (clone = `$C`, scratch = `$S`) | exit |
|---|---|---|
| (i)   | `python3 -I -B tools/round-95/stop-boundary-repair-battery-v5.py --selftest --work $S/work/X/n1` | 0 (6 cases, 0 failures) |
| (ii)  | `python3 -I -B tools/round-95/c1-agreement-v2.py --selftest $S/work/X/n2` | 0 (5 cases, 0 failures) |
| (iii) | `cd $C && python3 -I -B tools/round-95/c1-forgery-refusal.py --selftest $S/work/X/n3` | 0 (3 cases, 0 failures) |
| (iv)  | `python3 -I -B tools/round-95/c1-forgery-refusal.py --root $C --fixtures $C/.ufo/waves/round-95/forgery --old-prefix forge --old-counter tools/round-94/c1-receipt-agreement.py --honest-dir $S/honest --honest-prefix honest --world-rev b5331db1fb0ce0bf93695ce1730cf831effef6a9 --instrument-rev 4bda1d1dd3788973f10e61212b70df18b3b14ea0 --expect "repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2" --json-out $S/work/X/iv-forgery.json` | 0 (`forgeries refused 4 of 4; before admits True; honest accepted True`) |

`$S/honest` holds copies of `.ufo/waves/round-95/l1/scores/honest-pos.{json,stdout,rc}`.

## Mutants (exactly one hunk each; `git diff` per clone in `mutant-diffs/`)

Kill rule (frozen): killed when any of (i)-(iv) exits differently from the baseline.
Columns (i)-(iv) are exit codes of the mutated clone; baseline is 0 for all four.

| id | file | mutation | (i) | (ii) | (iii) | (iv) | frozen kill rule | which check killed it / supplementary detector |
|---|---|---|---|---|---|---|---|---|
| M1 | v5 `write_receipt` | mkstemp block → `tmp = path + ".tmp"`, `os.open(tmp, O_WRONLY\|O_CREAT\|O_TRUNC)` | **1** | 0 | 0 | 0 | KILLED | (i): `selftest planted-tmp-symlink-ignored: FAIL` (write follows planted symlink into victim) |
| M2 | v5 `write_receipt` | `os.fsync(fh.fileno())` deleted | 0 | 0 | 0 | 0 | **SURVIVED** | none of (i)-(iv). Supplementary D-fsync: `os.fsync` calls 1 → **0** (killed by an fsync-count probe) |
| M3 | v5 `main` | `selfverify = {"ok": True, "reasons": []}` inserted after `verify_receipt` | 0 | 0 | 0 | 0 | **SURVIVED** | none of (i)-(iv). Supplementary D-main (faked verdict, public `main()`): short-rev exit 1 → **0**; rewrite exit 1 → **0**; notrecomp exit 1 → **0** |
| M4 | v5 `main` | fail-closed `code = 1` replaced by `pass` (the only way to delete it and keep the `if` syntactically valid) | 0 | 0 | 0 | 0 | **SURVIVED** | none of (i)-(iv). Supplementary D-main: short-rev prints `selfverify reason: revision-not-bound` but exits **0** (baseline 1) |
| M5 | v5 `verify_receipt` | label-not-frozen branch deleted (`if rec.get("met_target") ...` + append) | **1** | 0 | 0 | 0 | KILLED | (i): `selftest verify-catches-not-frozen: FAIL` |
| M6 | v5 `verify_receipt` | revision-not-bound `elif` + append deleted | 0 | 0 | 0 | 0 | **SURVIVED** | none of (i)-(iv) (no revision case in the v5 selftest). Supplementary D-main short-rev: exit **0** (baseline 1) |
| M7 | v2 `row` | pins-not-bound `if` + append deleted (lines 164-166) | 0 | **1** | **1** | **1** | KILLED | (ii): `fabricated-pins-refused: FAIL`; (iii): `mini-forgeries-refused: FAIL`; (iv): `forgeries refused 3 of 4`, exit 1 |
| M8 | v2 `row` | label-not-recomputed append (line 141) replaced by `pass` | 0 | **1** | **1** | **1** | KILLED | (ii): `not-recomputed-refused: FAIL`; (iii): FAIL; (iv): `refused 3 of 4`, exit 1 |
| M9 | v2 `row` | label-not-frozen append (line 143) replaced by `pass` | 0 | **1** | **1** | **1** | KILLED | (ii): `rewrite-refused: FAIL`; (iii): FAIL; (iv): `refused 3 of 4`, exit 1 |
| M10 | `symlink-probe.py` | receipt fields hard-coded `"verdict": "hardened"`, `"met": True` (exit line untouched) | 0 | 0 | 0 | 0 | **SURVIVED** | none of (i)-(iv): the probe is not run by any of them. Probe negative control (v4 writer, baseline rc 1) still exits 1, so exit code is unchanged; the receipt says `verdict hardened, met True, victim_intact False`. Killed only by a receipt-content check (see below) |

Tally under the frozen kill rule: **5 killed** (M1, M5, M7, M8, M9), **5 survived** (M2, M3, M4, M6, M10).

## Survivors and the check that kills each

The supplementary detectors are not frozen counters; they are my own in-process/CLI probes, run
only to show which check would kill each survivor. None is written into the lane.

- **M2 (fsync removed).** Killed by an fsync-count check on `write_receipt` (D-fsync: 1 call on baseline, 0 on M2). Not observable by any functional selftest; durability needs an instrumented check.
- **M3 (self-verify forced ok).** Killed by a `main()`-level negative control: a met-True verdict whose receipt cannot verify (short `--rev`, rewritten label, or label that does not recompute) must exit 1. D-main gives baseline 1/1/1 and M3 0/0/0. The frozen (i)-(iv) never call `main()`, and the honest run is genuinely green, so it cannot discriminate.
- **M4 (fail-closed removed).** Same `main()`-level negative control. M4 still prints `selfverify reason: revision-not-bound` on stderr but exits 0 (baseline exit 1).
- **M6 (revision binding removed).** Killed by a revision case in the v5 selftest (wrong `revision` must give exactly `["revision-not-bound"]`). The frozen v5 selftest has no such case (only `verify-catches-not-recomputed` and `verify-catches-not-frozen`). D-main short-rev: baseline 1, M6 0.
- **M10 (probe hard-coded).** Killed by a receipt-content check on the probe's v4 negative control: a probe whose receipt says `verdict hardened` while `victim_intact` is `false` is self-contradictory. Baseline v4 receipt: `followed-symlink`, `met False`, `victim_intact False`; M10 v4 receipt: `hardened`, `met True`, `victim_intact False`, exit 1 (identical to baseline). Note that the probe's exit code cannot catch this, and the probe is not in (i)-(iv).

## Probe and detector results (supplementary, from saved receipts)

| run | result |
|---|---|
| baseline probe v4 (`followed-symlink`, expected) | rc 1; `verdict followed-symlink victim_intact False met False receipt_valid True` |
| baseline probe v5 (`hardened`, expected) | rc 0; `verdict hardened victim_intact True met True receipt_valid True` |
| M10 probe v4 | rc 1; `verdict hardened victim_intact False met True` (contradicts victim_intact) |
| M10 probe v5 | rc 0; identical to baseline v5 (the mutant does not change the v5 outcome) |
| D-main baseline | pos 0; shortrev 1 (`revision-not-bound`); rewrite 1 (`label-not-frozen`); notrecomp 1 (`label-not-recomputed`) |
| D-fsync baseline | fsync_calls 1, receipt written |

Probe commands: `python3 -I -B tools/round-95/symlink-probe.py --root $C --writer <v4 or v5> --repair-cmd .ufo/waves/round-93/controls/identity_noop.py --work $W --rev 4bda1d1d... --expect "<label>" --json-out $W/probe.json` (run from the clone).

## Notes and named limits

- Mutants M4 and M8/M9 use `pass` in place of the deleted statement. This is the smallest edit that keeps the surrounding `if`/`elif` syntactically valid; the behaviour is identical to deleting the append/assignment.
- Killed mutants show the four-check exit codes as recorded; `rc` files and full stdout/stderr are under `receipts/<X>/logs/`.
- M10's frozen-rule verdict is "survived" because the rule only compares exit codes of (i)-(iv); this is a real coverage gap of the frozen C1 kill rule, not a measurement error.

## Files written by this seat

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/MutationC1/mutants.md` (this file)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/MutationC1/mutant-diffs/M1.diff` … `M10.diff` (10 files, one hunk each)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/MutationC1/receipts/run4.sh`, `receipts/d-main.py`, `receipts/d-fsync.py` (the exact driver scripts used)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/MutationC1/receipts/{base,M1..M10}/logs/{i,ii,iii,iv}.{out,err,rc}` (four-check outputs)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/MutationC1/receipts/{base,M1..M10}/det/detectors.txt` and `det/fsync-probe.json` (supplementary detectors)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/MutationC1/receipts/{base,M10}/probe-v4/{probe.json,stdout.txt,rc}` and `probe-v5/…` (probe receipts)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/MutationC1/receipts/base/{junk,after}.{out,err}`, `c2-junk.json`, `c2-after.json`, `d2.out`, `d3.out`, `iv-forgery.json` (C2 base reproduction and baseline forgery receipt)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/MutationC1.md` (scoped findings report; the Report: trailer path)

No tools were installed or upgraded. No lane file was modified, and no git mutation was run in the lane.
