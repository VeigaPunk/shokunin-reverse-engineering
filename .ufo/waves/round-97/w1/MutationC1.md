# MutationC1 - round-97 instrument mutants (scratch clones only)

Seat: MutationC1 (mutation-tester), leaf. Lane: kaidoku-shokunin, landing L = 867ed98d85f45a18265441c1760386ef353b3d43.
Lane tree untouched: sha256 of tools/round-97/kill-rule-v3.py (4017299196653d30...) and stop-boundary-repair-battery-v7.py (2cd984f3a949...) identical before and after (checked with `sha256sum | diff`).
Mutant list: `.ufo/waves/round-97/w1/MutationC1/mutants.json`.
Wrap-up: L1 (KaidokuR97) asked for wrap-up; command-A legs for MA, MF, ME were still running and were cancelled (bg_8406). Those legs are marked not measured.

## Table

| mutant | edit (scratch clone) | observed check | killed |
|---|---|---|---|
| M-A | kill-rule-v3.py write_receipt: CUT dir-fsync block (l.110-114) | rule `--selftest` exit 0 (cases=8 failures=0); command A not measured (cancelled) | no (selftest); cmd A not measured |
| M-B | kill-rule-v3.py blob_sha256: `return None` first | command A exit 1: `bytes 0 of 5; dirtyrefuse 0 of 1; honest accepted 0 of 1`, met False; rule `--selftest` exit 0 | **yes** (K-bytes) |
| M-C | kill-rule-v3.py main: `classes_match = True or all(...)` | command A exit 0, exact frozen label `mutants killed 21 of 21 ... ownrec 1 of 1`; rule `--selftest` exit 0 | **no** |
| M-D | kill-rule-v3.py verify_own_receipt: `return {"ok": True, ...}` first | rule `--selftest` exit 1: `selftest ownrec-lying-refused: FAIL`; command A exit 0 (ownrec still 1 of 1) | **yes** (own selftest only) |
| M-E | v7 count_problems: CUT counts-extra loop (l.152-154) | v7 `--selftest` exit 1: `selftest verify-catches-counts-extra: FAIL` (cases=23 failures=1); isolated forgery battery 12 of 13 (`forge-counts-extra` accepted, reasons []); cmd A not measured | **yes** (v7 selftest + battery) |
| M-F | kill-rule-v3.py c_bytes: body renamed `_c_bytes_real`, wrapper sets `r["ok"]=True` | probe: v7 forced to admit dirty lie -> pristine `ok false`, mutant `ok true` (bound 5 of 5 in both); rule `--selftest` exit 0; cmd A not measured | **no** (blind dirty leg, shown by probe) |

## Commands and exit codes (all run in scratch clones, cwd = tree root unless noted)

- Pristine clone, baseline: `python3 -I -B tools/round-97/stop-boundary-repair-battery-v7.py --selftest --work <S>/work-base-st` -> exit 0, `SELFTEST cases=23 failures=0`.
- Pristine clone: `python3 -I -B tools/round-97/kill-rule-v3.py --selftest --work <S>/work-base-st/kr` -> exit 0, `SELFTEST cases=8 failures=0`.
- Pristine frozen command A, cwd = clone root, `--root . --decl e859a88d... --json-out <S>/run2/base/receipt.json`: exit 0, label `mutants killed 21 of 21; forgeries refused 17 of 17; negctl refused 3 of 3; probe consistent 1 of 1; honest accepted 1 of 1; wlink 2 of 2; durability 2 of 2; bytes 5 of 5; dirtyrefuse 1 of 1; ownrec 1 of 1`, met True. Matches the frozen label.
- Pristine forgery battery (`forgery_battery.py`, frozen `c_verify_forgeries`): `forgeries refused 13 of 13 ok=True`, exit 0.
- Mutant selftests (`--selftest --work <S>/x/<M>/st`): MA exit 0; MB exit 0; MC exit 0; MD exit 1 (ownrec-lying-refused FAIL); MF exit 0; ME (v7) exit 1 (verify-catches-counts-extra FAIL).
- Command A, mutant trees, cwd = mutant root: MB exit 1 (bytes 0 of 5, met False); MC exit 0 (label exact); MD exit 0 (label exact). MA, MF, ME: not finished at wrap-up, cancelled.
- M-E isolated battery: `forgery_battery.py <mut-ME> <rule> <clone>` (pins from pristine clone): `forgeries refused 12 of 13 ok=False`, exit 1. Same battery with mutant's own pins: `refused 1 of 13`, the other 12 fail on `byte-pin-not-bound:counter` (confounded by the byte pin, so the isolated run is the one cited above).
- M-F probe: `mf_probe.py <rule> <tree> <work>`: pristine `{"ok": false, "bound": 5, "total": 8, "v7_refused": false, "v6_admitted": false}`; mutant `{"ok": true, ...}`, exit 0 both.

## Findings

1. **M-C survives.** `classes_match` is only read through a rule that never sees a class mismatch: all 21 real mutants have `observed_class == declared_class` (semantic 20, crash 1), so forcing the value True changes no label. Coverage gap: no mutant exercises a class mismatch.
2. **M-F blind spot.** The K-bytes dirty-clone leg (`dirtyrefuse`) can be made to report green with the v7 admitting the byte lie; the probe shows `ok true` where the frozen code gives `ok false`. Command A cannot see the failure because `dirty_ok` is read from `ok`. Coverage gap: no check asserts that `c_bytes` itself fails when v7 admits the lie.
3. **M-A not observed by command A (selftest only).** Nothing in the frozen check set exercises the rule's own `write_receipt` directory fsync; K-durability checks the v7 writer only. Command-A leg not measured (cancelled), so the survival is by inspection plus the selftest exit 0 only.
4. **K-cwd is not a non-root probe (side observation).** `run()` has no cwd argument; the `cwdprobe` directory only receives `--json-out`, and the r95 battery is called with the relative `--fixtures .ufo/waves/round-95/forgery`. Command A run from a non-root cwd (`$S`) gave exit 1 with `K-cwd False`, `r95-battery-regression False`, `honest accepted 0 of 1` and `mutants killed 20 of 21` (FileNotFoundError on the relative fixture path). The same command from the root gives exit 0 and the exact label. So the check only proves "run from root", not "green from a non-root cwd" as its label says.
5. **M-r1 cwd-sensitive (side observation).** Under the non-root-cwd run, mutant M-r1 (receipt-required refusal disabled) had `failed_checks []`; under the root-cwd run it is killed by `K-selftest`. The kill is therefore sensitive to the invocation cwd, not only to the rule.

## Killed / survived summary

- Killed (measured): M-B (command A, K-bytes), M-D (rule selftest), M-E (v7 selftest and forgery battery).
- Survived (measured): M-C (command A exit 0, exact label).
- Not measured (cmd A cancelled): M-A (selftest exit 0 only), M-F (probe shows blind spot; cmd A not run).

## Tooling

No tool installed or upgraded. Only python3 -I, git (read and clone operations in scratch), sha256sum were used. No pacman, sysctl or host change. Scratch removed at exit.
