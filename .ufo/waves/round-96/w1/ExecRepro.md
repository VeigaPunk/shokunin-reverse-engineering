# ExecRepro — independent non-author reproduction of R96-C1 at the working revision

Seat: ExecRepro (executor, leaf). Scratch: `/fast/scratch/hyaku/kaidoku-r96/ExecRepro`.
Clone: `git clone --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/clone`.
Clone HEAD = `3baac2ef4b9b2830d299125b8184ca06d9e6584d` (the disclosed supersession commit on
top of declaration `e4d1f7de9deae83e6d5f78d2d7f0157196002af0`) — verified with
`git -C $S/clone rev-parse HEAD`, exit 0. Axes: calibration (R96-C1). Godspeed: coverage,
depth, calibration, freshness at 10.0 on finite proxies; this seat verifies C1 only.

Tooling: python3 (host), upx 5.2.0 at `/usr/bin/upx`, `/usr/bin/printf` sha256
`b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7` (matches S321 claim).
No tools installed or upgraded (none needed).

## (a) v6 selftest — exit 0

```
cd $S/clone && python3 -I -B tools/round-96/stop-boundary-repair-battery-v6.py --selftest --work $S/v6-st
exit=0
SELFTEST cases=13 failures=0
```
All 13 cases `ok`: bytes-encoded, label-recomputes, planted-tmp-symlink-ignored,
unknown-type-raises-clean, verify-catches-not-recomputed, verify-catches-not-frozen,
verify-catches-wrong-revision, verify-catches-met-lying,
verify-catches-unlabelled-counts, verify-catches-head-mismatch,
verify-catches-counter-pin, verify-honest-accepted, usage-refuses-no-json-out.

## (b) kill-rule selftest — exit 0

```
cd $S/clone && python3 -I -B tools/round-96/kill-rule-v2.py --selftest --work $S/kr-st
exit=0
SELFTEST cases=4 failures=0
```
Cases: apply-once, double-find-refused, lying-probe-inconsistent, truthful-negative-consistent.

## (c) Full frozen kill rule — exit 0, frozen label met

```
cd $S/clone && timeout 1200 python3 -I -B tools/round-96/kill-rule-v2.py \
  --root $S/clone --work $S/kr-repro \
  --mutants .ufo/waves/round-96/mutants.json \
  --fixtures .ufo/waves/round-96/forgery --prefix forge \
  --expect 'repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2' \
  --json-out $S/kr-repro.json
exit=0
```
Finished in ~4 s wall (the round-94 writer leg under K-probe uses the identity repair
control, so no upx battery ran end-to-end inside this command).

Receipt `kr-repro.json`:

- `label`: `mutants killed 10 of 10; forgeries refused 10 of 10; negctl refused 3 of 3;
  probe consistent 1 of 1; honest accepted 1 of 1`
- `met_target`: `true`, `exit`: `0`, `identity_not_killed`: `true`
- `counts`: `{"mutants_killed": 10, "mutants": 10, "forgeries_refused": 10,
  "forgeries": 10, "negctl_refused": 3, "negctl": 3, "probe_consistent": 1,
  "probe": 1, "honest_accepted": 1, "honest": 1}`
- `world_revision`: `3baac2ef4b9b2830d299125b8184ca06d9e6584d`; `decl`: `null`
  (no `--decl` passed — the committed receipt carries the declaration string; see below)
- `counter_sha256` `3b8c7583…` (kill-rule-v2.py), `target_counter_sha256` `7d7d559a…`
  (v6), `probe_sha256` `67b74a4b…`, `mutants_sha256` `aaea35b4…`,
  `agreement_sha256` `ca7d213a…` — all match the clone's committed files.

Honest arm (all `ok: true`): K-selftest-counter (13/0), K-selftest-agreement (5/0),
K-forgeries (10/10 refused, 6 r96 exact + 4 r95 refusal-only), K-agreement (4/4
exact + honest triple accepted), K-dmain (pos exit 0; shortrev/rewrite/notrecomp
exit 1; nojson exit 2), K-fsync (fsync_calls 1), K-probe (probe_rc 1,
verdict `followed-symlink`, met false, victim_intact false, receipt_valid true —
the r94 v4 writer is the unhardened target, so the negative result is the
consistent one), r95-battery-regression (exit 0).

K-forgeries rows (honest): `forge-counter-pin` → `["counter-pin-not-bound"]` exact,
`forge-head-mismatch` → `["head-not-bound"]` exact,
`forge-met-lying` → `["met-not-recomputed"]` exact,
`forge-repair-pin` → `["repair-pin-not-bound"]` exact,
`forge-unlabelled` → `["counts-missing-key:fresh_scored"]` exact,
`forge-verdict-pin` → `["verdict-pin-not-bound"]` exact; the four r95 fixtures
(F1/F2/F3/pos) refused non-exactly with combined reasons (label-not-recomputed /
head-not-bound / pin reasons).

Mutants (killed / killing check):

| name | kind | killed | killing |
|---|---|---|---|
| M0 | identity | false | — |
| M1 | counter (fixed temp name) | true | K-selftest (13 cases, 1 failure) |
| M2 | counter (fsync removed) | true | K-fsync (0 calls) |
| M3 | counter (forced self-verify) | true | K-dmain (shortrev/rewrite/notrecomp all exit 0) |
| M4 | counter (fail-closed removed) | true | K-dmain (same trio exit 0) |
| M5 | counter (label-not-frozen removed) | true | K-dmain (rewrite) + K-selftest |
| M6 | counter (revision binding removed) | true | K-selftest (wrong-revision case) |
| M7 | agreement (pins removed) | true | K-agreement (F3 accepted) + K-selftest |
| M8 | agreement (label-not-recomputed removed) | true | K-agreement (F1 accepted) + K-selftest |
| M9 | agreement (label-not-frozen removed) | true | K-agreement (pos accepted) + K-selftest |
| M10 | probe (verdict hard-coded `hardened`, met true) | true | K-probe (verdict hardened with victim_intact false) |

## (3) Pins — 0 mismatches

```
cd $S/clone && sha256sum -c .ufo/waves/round-96/pins.sha256
exit=0, 60 entries, 0 mismatches (no FAILED / no-such-file lines)
```
Verified against the clone's committed (supersession-regenerated) copy. Spot checks:
kill-rule-v2 `3b8c7583…`, v6 `7d7d559a…`, probe `67b74a4b…`, mutants `aaea35b4…`,
v3 verdict `60026511…`, repair `ce1b1769…`, agreement `ca7d213a…` all match pins.

## Diff vs committed receipts (`l1/scores/`)

- vs `c1-at-decl-worktree.json` (the only committed kill-rule receipt; created by the
  supersession commit, run at the worktree whose HEAD was the declaration
  `e4d1f7de9…`): deep diff is exactly two fields — `world_revision` mine
  `3baac2ef…` vs committed `e4d1f7de…`, and `decl` mine `null` vs committed
  `"e4d1f7de9…"` (I did not pass `--decl`). Label, counts, all mutant killed
  verdicts, all per-check rows and reasons, all sha256 pins are byte-identical;
  `identity_not_killed` true in both. Both exit 0 with the frozen label.
- vs `honest-pos.json` (exit 0, `selfverify ok=True reasons=0`, stdout
  `… met True exit 0`): the public honest run at the declaration revision,
  `head`/`revision` `e4d1f7de…`, counts identical to the frozen battery label.
  I did not re-run the public upx battery (item 2 names only the kill rule, whose
  K-probe leg uses the noop repair); the committed receipt stands as the public-run
  evidence and its pins match my clone's bytes.
- vs `honest-pos-red-head-not-bound.{json,rc,stderr,stdout}`: the pre-fix red
  evidence — `head: null` (old hex-only `resolve_rev` rejected `HEAD`),
  `counter_sha256 a9ba5d46…` (pre-fix v6 bytes), stderr
  `selfverify reason: head-not-bound`, rc `1`, stdout still prints the met-True
  label — the fail-closed gate turning the green verdict into exit 1 before the
  `resolve_rev` fix. Consistent with the disclosed supersession in claims.json.
- Before arm (committed, re-read only): `pre/c1-legacy-rule-at-base.json` — r95 rule
  kills 5 of 10, survivors M2/M3/M4/M6/M10 (killed: M1/M5/M7/M8/M9), exit 1;
  `pre/c1-v5-admits-unbound-at-base.json` — v5 accepts 5 of 6 forgeries,
  `KeyError: 'fresh_scored'` on forge-unlabelled, nojson exit 0 with no receipt;
  `pre/c1-probe-writer-unbound-at-base.json` — r95 probe write follows the planted
  link (victim_intact false), v2 probe leaves it intact (true).

## Lifecycle end-to-end (source read; `file:line` at clone HEAD)

- `load_module` (kill-rule-v2.py:107) loads the counter by path; `main` (v6:344)
  refuses without `--json-out` (exit 2, `receipt-required`) before `v3.score`,
  then writes via `write_receipt` (v6:83: mkstemp + fsync + `os.replace`) and
  `verify_receipt` (v6:142) re-reads, re-binds head/revision/pins, and `main`
  fails closed (`code == 0 and not selfverify["ok"]` → 1, v6:387–388).
- Kill rule honest arm (kill-rule-v2.py:405–448): selftests → forgeries
  (`c_verify_forgeries` :142, in-process `verify_receipt` with `counter_pins`
  :137) → agreement exact (subprocess, `--rev R95_WORLD_REV`) → `c_dmain`
  (:203, faked `v3.score`, 4 scenarios + nojson) → `c_fsync` (:249,
  monkeypatched `os.fsync` count) → `c_probe` (:266, subprocess of probe-v2
  against the r94 writer) → r95 battery regression subprocess. Mutant arm
  `run_mutant` (:320) = `build_copy` (:297, exactly-once find/replace) +
  per-kind checks; `killed = any(not ok)` (:355). `resolve_head` (:114)
  pins the world revision to the clone HEAD.
- Known limits (claims-named, observed not altered): K-probe checks only the
  probe receipt's internal consistency (`verdict == "hardened"` iff
  `victim_intact and receipt_valid`, plus `met`); a probe lying consistently
  about a manipulated victim is not caught. K-dmain fakes `v3.score` in
  process; the real battery path is exercised only by the committed honest-pos
  receipt and the probe legs. fsync counting is Python-level, not `strace`.
  The forgery `exact` flag: r96 six require the single intended reason;
  r95 four require refusal only (their reasons now include `head-not-bound`/
  pin reasons because the r95 fixtures are verified against v6 pins and the
  current HEAD — expected, not a silent weakening; K-agreement still checks
  the r95 four exactly with the r95 agreement instrument).

No discrepancies from the frozen claim were found. No lane files were edited;
scratch clone work dirs and all tool output were under `$S` (removed after
receipts were copied to the seat dir).

Receipts in seat dir: `ExecRepro-kr-repro.json` (=== `$S/kr-repro.json`,
sha256 `6389be60…`), `ExecRepro-kr.out`, `ExecRepro-v6-selftest.out`,
`ExecRepro-kr-selftest.out`, `ExecRepro-pins.out`.
