# CriticC1 — adversarial attack on R96-C1 (kill-rule gate coverage and unbound-field bindings)

Seat: CriticC1 (critic). Lane kaidoku, round 96, attempt 1. Clone: `git clone --shared` of the lane, checked out at lane HEAD `3baac2ef4b9b2830d299125b8184ca06d9e6584d` (`git -C <clone> rev-parse --show-toplevel` = clone). Full attack table with mechanisms, commands and per-row verdicts: `.ufo/waves/round-96/w1/CriticC1/attack.md`. Receipts and fixtures: `.ufo/waves/round-96/w1/CriticC1/`.

## Verdict

R96-C1 is reproduced at lane HEAD (frozen command 1 rc 0, label met; honest v6 public run rc 0 with selfverify ok; v6 probe leg rc 0, victim intact). The claim as worded is **falsified in part**: the v6 bindings do not bind every field the receipt claims, and the kill rule does not assert the head/measured-tree binding it is cited for. Five concrete survivors or acceptances, one misnamed kill route, and one landed receipt whose revision does not name the bytes it pins.

## Findings (counterexamples)

1. **Unbound fields accepted** (verify_receipt and agreement both ACCEPT; `attack.md` A2, A3, A9, A11, A12):
   - extra or unbound counts keys (`forged_extra`, `silent`): the verifier binds only the nine `COUNT_KEYS`;
   - `repair_cmd` swapped while `repair_sha256` still matches the upx pin: `repair_cmd` is recorded, never bound;
   - `public_met` / `public_label` lying: unbound;
   - `imported_r92_battery_sha256` / `imported_v2_sha256` zeroed: v6 has zero references to `imported_*`. The round-96 plan lists these pins among the M95-g unbound fields; the v6 binding list does not cover them.
2. **met_target type not checked** (A5, A6): `"true"` and `null` with the frozen label and pins are ACCEPTED by `verify_receipt` (its checks are `is True` / `is False` only). The c1-agreement-v2 instrument refuses them (`stdout-disagree`, `predicted-mismatch`), but the kill rule never runs agreement on round-96 fixtures.
3. **head binds the commit, not the measured bytes** (A10, A14): `head` is compared only with `revision`, which is compared only with the caller's `rev_full`. The verifier has no ground truth. Kill-rule K-forgeries passes `rev_full = receipt["revision"]`, so the head/revision pair is accepted whatever its value. The landed honest receipt `.ufo/waves/round-96/l1/scores/honest-pos.json` records `head = revision = e4d1f7` but `counter_sha256 = 7d7d559…`; `git show e4d1f7:tools/round-96/stop-boundary-repair-battery-v6.py` sha256 is `a9ba5d46…`. Its counter pin equals the bytes committed at 3baac2ef. [INFERENCE] the landed run measured an uncommitted working tree (the v6 supersession fix) while `head` recorded the declaration commit. The c1-agreement-v2 check at the receipt's own revision refuses it (`pins-not-bound`, rc 1). The landed honest evidence does not survive its own agreement check at its named revision.
4. **Kill rule does not test the head binding** (K3): mutant M11 (`receipt["head"] = resolve_rev(root, args.rev)`) is **not killed** by K-selftest, K-dmain, K-fsync or K-forgeries. The frozen 10-mutant table never runs `--rev ≠ HEAD`. Direct scenario (fake verdict, `--rev e4d1f7`): honest counter exit **1** (`selfverify reason: head-not-bound`); M11 exit **0** with `head = revision = e4d1f7` while HEAD = 3baac2ef (`attacks/results/rev-old-scenario.json`). The honest counter is correct; the frozen rule does not assert it.
5. **Bool clause not killed** (K4): removing the `isinstance(v, bool)` clause from `count_problems` (M12) is not killed. No bool fixture exists in the round-96 forgery set. Attack A1 is refused by v6 with the correct reason `counts-type:repaired`, but agreement names the same forgery `label-not-recomputed` (misnamed: `%d` coerces True to 1).
6. **Probe consistency is self-referential and tested only on the unhardened writer** (K7, K8): P1 (victim_intact and receipt_valid forced true) survives K-probe, as the plan declares. New: P2 (a probe that always reports `followed-symlink`) also survives K-probe. K-probe's honest leg uses the default writer `tools/round-94/stop-boundary-repair-battery-v4.py` (unhardened), so the consistency predicate is satisfied by a probe that never detects a hardened writer. The v6 discrimination (command 3) is outside the frozen label. Command 3 itself reproduces: `victim_intact true`, `verdict hardened`, rc 0.
7. **K-forgeries cannot test revision binding** (K9): `c_verify_forgeries` derives `rev_full` from each fixture's own `revision`, so `revision-not-bound` can never fire in that battery. The "forgeries refused 10 of 10" is a self-consistency result, not a world-binding result.
8. **Misnamed kill route** (K5): mutants.json declares M6's kill via `K-dmain shortrev`. Observed: M6 fails only K-selftest; the shortrev receipt is also refused by `head-not-bound`. The mutant is still killed.
9. **Reason misnamed or coarse**: A4 (`head-39hex` → two reasons in the HEAD world; agreement has no head check at all), A8 (`receipt-missing-counts-or-label` conflates missing counts and missing label, skipping the frozen-label check), A10 (agreement at the OLD revision reports `pins-not-bound` for a head fault).
10. **Named limits confirmed**: A7 — `--expect ""` disables the met-lying check in `verify_receipt`; no green exit is reachable through main with an empty expect (v3 sets `met = label == args.expect and …`, so `exit 1`; code read, path not executed). K2 — build_copy's count-based placement cannot tell a dead-text (docstring) mutant from a real survivor; M13 in a docstring is applied and `killed=False`; no false kill follows. K10 — agreement raises a bare `KeyError` on any `--names` outside pos/F1/F2/F3.

## No effect (checked)

- K1 identity control: M0 run twice in fresh work dirs; both runs unkilled, all four checks ok both times. `c_selftest` rmtree's its own run dir before each call; M0 runs no probe, agreement or upx. No flake observed.
- K6 collateral kills: all ten declared mutant files `py_compile` after replacement; each find string occurs exactly once in code. Per-mutant kill attribution: M1 K-selftest; M2 K-fsync; M3 K-dmain; M4 K-dmain; M5 K-dmain+K-selftest; M6 K-selftest; M7/M8/M9 K-agreement+K-selftest; M10 K-probe.
- No false refusal of the genuine honest receipt (A15, accepted by verify and agreement).

## Reproductions (exit codes)

| Command (clone, scratch `HYAKU_SCRATCH`) | rc | Receipt |
|---|---|---|
| `python3 -I -B tools/round-96/kill-rule-v2.py --root . --work <scratch> --mutants .ufo/waves/round-96/mutants.json --fixtures .ufo/waves/round-96/forgery --prefix forge --expect '<FROZEN>' --json-out <scratch>/repro/c1-kill-rule-at-head.json` | 0 | `attacks/repro/c1-kill-rule-at-head.{json,stdout,stderr,rc}`: `mutants killed 10 of 10; forgeries refused 10 of 10; negctl refused 3 of 3; probe consistent 1 of 1; honest accepted 1 of 1`, `identity_not_killed true` |
| `python3 -I -B tools/round-96/stop-boundary-repair-battery-v6.py --root . --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py --work <scratch> --rev 3baac2ef… --expect '<FROZEN>' --json-out attacks/base/honest-at-head.json` | 0 | `attacks/base/honest-at-head.json`; `repro/honest-at-head.{stdout,stderr,rc}`: `selfverify ok=True reasons=0`, `met True exit 0` |
| `python3 -I -B tools/round-96/symlink-probe-v2.py --root . --writer tools/round-96/stop-boundary-repair-battery-v6.py --repair-cmd .ufo/waves/round-93/controls/identity_noop.py --work <scratch> --rev 3baac2ef… --expect '<FROZEN>' --json-out repro/c1-symlink-v6-at-head.json` | 0 | `repro/c1-symlink-v6-at-head.{json,stdout,stderr}`: `victim_intact true`, `verdict hardened` |
| `python3 -I -B attacks/harness/attack_harness.py` (in-process verify + agreement over 16 fixtures) | 0 | `attacks/results/inprocess.json`, `attacks/results/agreement.json` (agreement run per attack dir with `--names pos`; first attempt with other names crashed, see K10) |
| `python3 -I -B attacks/harness/kr_attacks.py` (M0 twice, M11, M12, P1, M13, compile, placement) | 0 | `attacks/results/kr-attacks.{json,stdout,stderr}` |
| `python3 -I -B attacks/harness/kr_attacks2.py` (P2, per-mutant kill attribution) | 0 | `attacks/results/kr-attacks2.{stdout,stderr}` |
| `python3 -I -B attacks/harness/rev_old.py` (`--rev e4d1f7` honest vs M11) | 0 | `attacks/results/rev-old-scenario.json` (`honest exit 1 head-not-bound`; `M11 exit 0`) |

Harness drivers copied to `.ufo/waves/round-96/w1/CriticC1/attacks/harness/`: `attack_harness.py`, `kr_attacks.py`, `kr_attacks2.py`, `rev_old.py`.

## Files written (lane, all under my SEAT)

- `.ufo/waves/round-96/w1/CriticC1.md` (this report)
- `.ufo/waves/round-96/w1/CriticC1/attack.md`
- `.ufo/waves/round-96/w1/CriticC1/attacks/fixtures/atk-*.json` (16 receipt fixtures)
- `.ufo/waves/round-96/w1/CriticC1/attacks/agreement/<attack>/atk-pos.{json,stdout,rc}` (15 agreement triples; shortrev is in-process only)
- `.ufo/waves/round-96/w1/CriticC1/attacks/base/honest-at-head.json`
- `.ufo/waves/round-96/w1/CriticC1/attacks/harness/*.py` (4 drivers)
- `.ufo/waves/round-96/w1/CriticC1/attacks/results/*` (inprocess, agreement, kr-attacks, kr-attacks2, rev-old-scenario)
- `.ufo/waves/round-96/w1/CriticC1/repro/*` (kill-rule, honest v6, probe v6 receipts and streams)

Scratch `/fast/scratch/hyaku/kaidoku-r96/CriticC1/` (clone, work dirs, copies) removed after the receipts were copied into the SEAT.

## Host and tool changes

None. No tools installed or upgraded. No sysctls, no pacman, no writes outside SEAT and scratch. No lane file edited, committed, staged or deleted. No git mutation (clone is `--shared` and read-only use only; the only git commands were `rev-parse`, `show`, `cat-file`, `status`, `clone`, `checkout` in the clone).

## Named needs (for the main agent)

- R96-C1's bindings should cover: every counts key the receipt carries (or an explicit allow-list), `met_target` as a bool, `repair_cmd`, `public_met`/`public_label`, `imported_r92_battery_sha256`/`imported_v2_sha256`; `head` should be compared to `git rev-parse HEAD` of the measured tree and the pins to `git show <revision>:<path>` (or the receipt should record a clean-tree flag).
- The kill rule needs: a `--rev ≠ HEAD` scenario (kills M11), a bool fixture (kills M12), a probe leg on the hardened v6 writer (kills P2), and a revision check that does not take `rev_full` from the receipt (K9).
- The landed honest receipt `l1/scores/honest-pos.json` should be re-measured at a clean tree (its counter pin is not the bytes at its revision).
