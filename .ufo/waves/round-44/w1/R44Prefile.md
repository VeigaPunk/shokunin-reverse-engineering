# R44Prefile — round-44 pre-file gate (pre-freeze build)

**Verdict: DONE.** `prefile-check.sh` is authored, self-tested (5/5 sandbox cases),
mutation-tested (6/6 mutants caught) and replayed against the lane's real history.
The gate reproduces the round-41 closure D1 defect as **RED** on round 41 and is
**GREEN** on rounds 42 and 43, which filed after their waves settled. The live
round-44 state is **RED** because wave 1 has not settled yet — the correct
answer for a gate that exists to block an early filing.

## 1. What I built

Two files, both under this seat's artifact directory (the L1 installs the first
under `tools/round-44/`):

| artifact | sha256 | role |
|---|---|---|
| `.ufo/waves/round-44/w1/artifacts/R44Prefile/prefile-check.sh` | `2f4582418973bea33b186db0373f2e21e928357c7996420b0fde1f72a7f0bac8` | the gate (POSIX `sh`, stdlib `git`/`grep`/`awk`/`sed` only) |
| `.ufo/waves/round-44/w1/artifacts/R44Prefile/mutants.sh` | `dcfa9b5f4b28eec7cb2d0a8dacad56b45f86f3b1c627dc30f04281139810e420` | the harness that proves the gate can fail |

**Installation for the L1:** copy `prefile-check.sh` to
`tools/round-44/prefile-check.sh` in the lane and run it at pre-file time:

```sh
sh tools/round-44/prefile-check.sh \
    --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --fleet /home/vgpnk/Projects/shokunin \
    --round 44 \
    --json-out .ufo/waves/round-44/l1/prefile-gate.json
```

Exit 0 = GREEN (filing permitted), 1 = RED (a binding condition failed), 2 =
could-not-evaluate (usage error / unusable tree). A 2 never counts toward the
target, per the round contract.

## 2. The three binding conditions

The gate re-runs the lane's pre-file gate machinery in the shape round 41
closure D1 and QUALITY #47 require, and that the round-44 prompt restates as
"File only after WAVE-DONE" (`kaidoku-round-44.md` §6, line 160).

| key | condition | how it is decided |
|---|---|---|
| `waves_settled` / `no_wave_done_ledger` | **(a)** every launched wave has its WAVE-DONE signal | a wave is *launched* when `<lane>/.ufo/waves/round-44/<wave>.ready` exists; its WAVE-DONE signal is the `<wave>-results.json` handoff ledger, which must (i) exist, (ii) be **committed at the measured rev**, (iii) name its own wave id, (iv) agree with the ready file's `wave` field. A missing ledger, an uncommitted ledger, a wave-id mismatch and a missing `.ready.dispatched` marker each produce their own named finding. |
| `report_committed` / `report_filed_before_wave_done` / `report_exists_but_wave_unsettled` | **(b)** the report path `.ufo/reports/round-44/kaidoku.md` exists only after all waves done | the report is located in the fleet repo (and, defensively, in the lane) at its measured rev. When committed, the gate compares the report's **first filing commit time** (`git log --full-history --diff-filter=A --format=%ct`, oldest add) against each wave ledger's **first add commit time**: a report filed before a wave settled is a FAIL. When the report is absent, the gate says so plainly and refuses to bless filing while a wave is still unsettled. |
| `frozen_paths_nonempty` / `frozen_paths_empty` | **(c)** the claims file's frozen-paths list is non-empty | the `## Frozen paths` section of `plans/round-44-claims.md` at the measured rev is extracted and its backticked path-like tokens counted; zero paths is a FAIL. Resolution of each named path at the rev is reported **advisory** (a directory or glob pathspec counts as resolved) — the binding clause is non-emptiness, not resolvability. |

The measured revision defaults to the **lane branch tip** (`refs/heads/main`),
never bare HEAD — the lane's HEAD is detached after the first helper commit
(`kaidoku-round-44.md` §5). `--rev` overrides it. The fleet tip is read the same
way. When the branch tip lags the worktree the gate prints a
`branch_tip_lags_worktree` warning so a stale measurement is never silent.

Read-only by construction: only `git rev-parse`, `cat-file -e`, `show`, `log`,
`ls-tree` and `status`-free reads are used; `GIT_OPTIONAL_LOCKS=0` is exported;
no temp file is left behind (the findings file is removed by an `EXIT` trap).

## 3. The gate can fail — selftest and mutants

**Selftest** (`sh prefile-check.sh --selftest`, sandbox fixtures built under
`$TMPDIR`, `git init -b main` + identity, fixtures removed afterwards):
5 cases, 5 pass, 0 fail, exit 0.

```
SELFTEST PASS green-wave-settled-no-report               expect=0 got=0
SELFTEST PASS red-wave-never-settled                     expect=1 got=1
SELFTEST PASS red-report-filed-before-wave-done          expect=1 got=1
SELFTEST PASS red-empty-frozen-paths                     expect=1 got=1
SELFTEST PASS red-unusable-lane-root                     expect=2 got=2
SELFTEST cases=5 pass=5 fail=0
```

The `red-report-filed-before-wave-done` fixture is the D1 shape end to end: the
fleet repo commits the report at 12:15 and the lane commits the wave ledger at
12:30; the gate exits 1 and names `report_filed_before_wave_done`.

**Mutants** (`sh mutants.sh ./prefile-check.sh <lane> <fleet>`): six one-line
semantic mutations, **6 caught, 0 survived**, exit 0. The harness compares both
the exit code *and* the set of `FAIL` keys per case, so a mutant that downgrades
one binding finding (e.g. `FAIL` → `WARN`) is caught even when the verdict is
unchanged.

```
BASE selftest_overall=0  replay_41=1  replay_42=0  replay_43=0  replay_44=1  replay_nowavedir=1
MUTANT m1_no_order_check            CAUGHT   selftest_overall:0->1 replay_41:1->0 replay_41_failkeys:report_filed_before_wave_done,->
MUTANT m2_ledger_fail_to_warn       CAUGHT   replay_44_failkeys:no_wave_done_ledger,waves_settled,->waves_settled,
MUTANT m3_frozen_fail_to_warn       CAUGHT   selftest_overall:0->1
MUTANT m4_force_exit_zero           CAUGHT   selftest_overall:0->1 replay_41:1->0 replay_44:1->0 replay_nowavedir:1->0
MUTANT m5_wave_dir_ignored          CAUGHT   replay_nowavedir_failkeys:wave_dir_missing,->no_launched_wave,
MUTANT m6_report_presence_ignored   CAUGHT   selftest_overall:0->1 replay_41:1->0 replay_41_failkeys:report_filed_before_wave_done,->
MUTANTS caught=6 survived=0
```

## 4. Real-history replay — the D1 defect reproduces

This is the load-bearing evidence: the gate is run against the **committed lane
and fleet history** of the rounds that already closed.

| round | report first filed (ct) | wave ledgers settled (ct) | gate | exit |
|---|---|---|---|---|
| 41 | `1793050181` (18:29:41) | w1 `1793049032`, w2 `1793051068` (18:44:28) | **RED** — `report_filed_before_wave_done` | **1** |
| 42 | `1793056701` (20:18:21) | w1 `1793056243` (20:10:43) | GREEN | 0 |
| 43 | `1793103308` (09:15:08) | w1 `1793096214`, w2 `1793102919` | GREEN | 0 |
| 44 (live) | not filed | w1 not settled | **RED** — `no_wave_done_ledger`, `waves_settled` | **1** |

Round 41 is exactly the round-41 closure D1 defect: the report was committed at
18:29:41, wave 2's WAVE-DONE ledger landed at 18:44:28, and the report was
amended at 18:44:45 (`00171131 "round-41: kaidoku report amended after wave-2
WAVE-DONE"`). The gate detects the *first* filing, not the amendment, which is
the honest reading of "the report path exists only after all waves done".

Round 41's own report also names the defect in its text, so the replay is
corroborated by the round's own account of it.

**Live round-44 state** (`receipts/replay-r44.out`): RED, exit 1, because wave
`r44-w1` has no results ledger yet — the wave is still running. This is the
gate doing its job: an L1 that filed the round-44 report right now would be
filing before wave 1 settled, which is the defect class this gate exists to
catch.

**Read-only proof** — a full run over the live lane and fleet leaves the
repositories untouched:

```
lane HEAD  before=1e9c4a430a46d5fde5f9cd1294fb04400199fe1b after=1e9c4a430a46d5fde5f9cd1294fb04400199fe1b
fleet HEAD before=c5f6ce9d4666575f03ff8b9f395fff2b12fe69d0 after=c5f6ce9d4666575f03ff8b9f395fff2b12fe69d0
status sha before=2c0c3bc165b555d54cb4407b7b5e97f5bc7d6d0b5f0665d4ffe6e5d84f9d1eb2  after=2c0c3bc165b555d54cb4407b7b5e97f5bc7d6d0b5f0665d4ffe6e5d84f9d1eb2
index  sha before=24da81b09f1352ec8bffb33261142d5b591c55f8aac275a8408d9cf324f80bba after=24da81b09f1352ec8bffb33261142d5b591c55f8aac275a8408d9cf324f80bba
```

## 5. Receipts

Every receipt below carries seat name, command, exit code, stdout sha256 and
wall time (round contract, QUALITY §failure-honesty). They are under
`.ufo/waves/round-44/w1/artifacts/R44Prefile/receipts/`.

| receipt | exit | stdout sha256 (12) | wall (s) |
|---|---|---|---|
| `selftest` | 0 | `ef7ccc454d45` | 0.312 |
| `replay-r41` | **1** | `2d695ed9c9dd` | 0.092 |
| `replay-r42` | 0 | `45fd42e14938` | 0.080 |
| `replay-r43` | 0 | `3e394c54b315` | 0.133 |
| `replay-r44` | **1** | `39ca26cf62b1` | 0.099 |
| `replay-r44-json` | **1** | `57ccc4f2a229` | 0.126 |
| `mutants` | 0 | `65dada929dea` | 8.020 |

The two exit-1 receipts are honest captures of a gate doing its job, not
failures of this seat's work.

## 6. Disclosed limits

- **The gate sees committed bytes only.** A wave whose results ledger exists in
  the worktree but is not yet committed at the measured rev is a FAIL
  (`results_not_committed` / `results_not_at_branch_tip`), never a pass. This is
  deliberate: the WAVE-DONE handoff must be durable before a report cites it.
- **Ordering is decided by commit timestamps** (committer date, `%ct`) across two
  repositories — the report lives on the fleet repo and the wave ledgers on the
  lane, so a single repository's ancestry cannot decide it. Timestamps are
  therefore the honest available signal; the round-41 replay shows it separates
  the defective filing from the two correct ones. A same-second tie is treated
  as *not* a violation (the report is not before the wave).
- **The gate does not verify the report's content.** It checks *when* the report
  appeared relative to the waves, not what it says. Content conformance stays
  with QUALITY #47 and the L1's own filing review.
- **The `frozen_paths_resolution` finding is advisory.** A frozen path that does
  not resolve at the measured rev is reported, not failed — the binding clause
  the seat was given is *non-emptiness*. A future round may want resolution
  bound to the freeze as a hard clause; that would need its own claim.
- **The gate's own path is not self-frozen.** It is an artifact under the wave
  directory; the L1 installs it under `tools/round-44/`, which the round-44
  claims file already lists as a frozen path (`tools/round-44/` DIRECTORY
  pathspec). Installing it is therefore a freeze-relevant act and belongs
  before the freeze commit, not after it.

## 7. Scope

I authored exactly two files plus their receipts, and this report. I did not
touch `plans/round-44-claims.md`, `tools/round-44/`, any claim text, any
counter, any evidence file, or any fleet-root tracked file. I did not run the
after-side C1 data procedure (`tools/round-44/c1-run.sh` does not exist yet and
was never invoked). No package was installed: the gate uses only `git`, `grep`,
`awk`, `sed` and POSIX shell already present (git 2.56.0, GNU coreutils), so
the pacman guard is not engaged.
