# ExecReproC2 — independent reproduction of R98-C2 (round 98, attempt 1)

Seat: ExecReproC2 (executor, leaf). Date: 2026-11-05. Scratch: /fast/scratch/hyaku/kaidoku-r98/ExecReproC2 (trap-deleted after run).
Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. All commands run in a `--shared` clone; no mutating git anywhere; no host/pacman changes; no tools installed.

## Environment
- Clone: `git clone --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/clone` → exit 0.
- `git -C $S/clone checkout --detach 72346895a35a74af18151b125934fa0c09fe1e3c` → exit 0.
- `git -C $S/clone rev-parse HEAD` → `72346895a35a74af18151b125934fa0c09fe1e3c` (L).
- `git -C $S/clone rev-parse --show-toplevel` → `/fast/scratch/hyaku/kaidoku-r98/ExecReproC2/clone` (asserted before any write).

## Selftests
- `python3 -I -B tools/round-98/stop-boundary-repair-battery-v8.py --selftest --work $S/v8-st` → exit 0, `SELFTEST cases=24 failures=0` (expected 24/0). Includes the new `selftest verify-catches-nine-key-stub: ok`.
- `python3 -I -B tools/round-97/stop-boundary-repair-battery-v7.py --selftest --work $S/v7-st` → exit 0, `SELFTEST cases=23 failures=0` (expected 23/0). v8 adds exactly one case over v7: `verify-catches-nine-key-stub`.

## Frozen C2 command (clone at L, cwd = clone)
- `python3 -I -B tools/round-98/allowlist-check.py --counter tools/round-98/stop-boundary-repair-battery-v8.py --rev 72346895a35a74af18151b125934fa0c09fe1e3c --work $S/c2-v8 --json-out $S/c2-v8-receipt.json` → exit 0, label `legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1 met True`. Wall 4.99 s.
- Control (v7 unchanged): `python3 -I -B tools/round-98/allowlist-check.py --counter tools/round-97/stop-boundary-repair-battery-v7.py --rev 72346895a35a74af18151b125934fa0c09fe1e3c --work $S/c2-v7 --json-out $S/c2-v7-receipt.json` → exit 1, label `legs passed 1 of 4; public 0; real14 0; stub9 0; extra 1 met False`. Wall 4.70 s.

## Comparison with frozen receipts (field-level, from my receipts vs L1/pre files)
- v8 run vs `.ufo/waves/round-98/l1/scores/c2-at-72346895a35a74af18151b125934fa0c09fe1e3c.json`: identical `label`, `met=true`, `exit=0`, `public_rc=0`, `public_stdout` (`selfverify ok=True reasons=0` + frozen label `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2 met True exit 0`), empty `public_stderr`, same `rev`, same `counter`, `counts_source` = my real public receipt (not the `.ufo/waves/round-97/l1/public/v6-public.json` fallback). Only scratch paths differ (expected).
- v7 control vs `.ufo/waves/round-98/pre/c2-v7-control.json`: identical `label`, `met=false`, `exit=1`, `public_rc=1`, `public_stdout` (`selfverify ok=False reasons=5` … `met True exit 1`), `public_stderr` identical five reasons in order: `counts-extra-key:fresh_far`, `:fresh_far_refused`, `:fresh_repaired`, `:refused`, `:silent`. `counts_source` = public receipt (len-14 counts written, selfverify refused) — same as pre receipt. Only scratch paths differ (expected).

## v7 → v8 delta review (unified diff of full files, `git show` blobs at rev L)
Behavioral changes found — all inside the permitted classes:
1. COUNT_KEYS allow-list: nine label keys → fourteen (`+fresh_far, +fresh_far_refused, +fresh_repaired, +refused, +silent`); new constant `NINE_LABEL_KEYS` (the old nine) used only by the new selftest case. No other constant or function body changed.
2. `TOOL` constant: `tools/round-97/stop-boundary-repair-battery-v7.py` → `tools/round-98/stop-boundary-repair-battery-v8.py`.
3. Selftest fixture: the planted `counts` dict gains the five new keys (now the fourteen-key set) — this is what flips `verify-catches-counts-extra` semantics to the honest-14 case.
4. Selftest case added: `verify-catches-nine-key-stub` (expects exactly `counts-missing-key:fresh_far|fresh_far_refused|fresh_repaired|refused|silent`).
5. Docstrings/comments only: module docstring (states "v8 = v7 with one change … Everything below describes v7"), `count_problems` docstring (nine→fourteen wording), inline COUNT_KEYS comment.

Flagged beyond the four named classes, and judged benign: the `--selftest` default scratch path changed `kaidoku-r97/selftest-v7` → `kaidoku-r98/selftest-v8`. It is part of the selftest harness, not the frozen command path (C2 always passes explicit `--work/--expect/--json-out`; `--selftest` is never exercised by the C2 legs). No change to `recompute_label`, `verify_receipt`, receipt I/O, or the VERDICT (v3) import/pinning.

## B → L scope check
`git -C $S/clone diff d0aebc288621b0072ac3eb2a79a62ad26bfa837a 72346895a35a74af18151b125934fa0c09fe1e3c --stat` → 10 files, 1683 insertions, 0 deletions: pre receipts (c1-identity, c1-r87, c2-v7, census-start), `plans/round-98-claims.md`, `tools/round-98/{allowlist-check.py, controls/identity-copy.py, pe-upx-tamper-battery.py, stop-boundary-repair-battery-v8.py, upx-pe-repair.py}`. No pre-existing file modified or deleted — nothing outside round-98 scope.

## Verdict
R98-C2 reproduced independently: frozen command exit 0 with target label; v7 control exit 1 with refusal label; selftests 24/0 and 23/0; v8 delta confined to the allow-list, TOOL constant, selftest fixture/case, docstrings (+ selftest scratch default, benign). No anomaly found.

## Risks / notes
- None blocking. The control's public leg recomputes `met True` yet exits 1 (selfverify refusal on extra keys) — this is v7's designed behavior, unchanged by v8, and matches the pre-frozen receipt byte-for-byte in stdout/stderr.
- Findings: 5 (selftests; frozen C2 pass; control fail; delta confinement; B..L scope).
