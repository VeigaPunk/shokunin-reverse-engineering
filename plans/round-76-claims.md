# Round 76 — declared claims (frozen; no amendments after this file's container commit)

Base `5303a662d43aac52b0667f2776cce49dfc004fcf` (the round-75 lane tip: the record, the report
and the round-75 non-author spot-check lesson; the lane tree is clean and pushed).
Two claims on two distinct axes, causally separable — each is scored by its own instrument and
neither reads the other's result. Both are capability acquisitions in the AXES sense: the
instrument runs, its output verifies, and its row enters the SCORECARD capabilities table in the
same round.

**Lowest-axis obligation.** The lane's three owned proxies (coverage/depth/calibration) sit at
10.0 behind different proxies and are tied; the stagnation nudge's waiver condition is *not* met
(capability rows entered in rounds 72–75, inside the 10-round window), so no waiver is claimed.
**`lowest-axis: calibration`** — R76-C1 works a tied-lowest axis.

The round-75 non-author spot-check (`corpus/lessons/round-75-verifier-spotcheck.md` §6) routed
eight defects to this round. This round's work is that queue, resolved as follows:

- routed defects 1 (two capability rows missing from the table) and 2 (the round-75 audit's atom
  set dropped the round-74 D8 capability-rows atom) → **R76-C1**;
- routed defect 4 (the printed R75-C1 counter command is not executable as written) → **R76-C2**;
- routed defects 3, 5, 6, 7 and 8 (two uncited round-75 commits, loose receipt-revision prose, the
  `LOG.md` "defects 1-8" sentence, the freeze-ledger disclosure sentence, the missing receipt
  exit code) are record corrections, carried **unclaimed** in the round's report and lesson; each
  is closed by an appended correction, never by rewriting filed bytes.

## R76-C1 — calibration: the capability rows become a checked claim

**Type.** Capability acquisition. The round-75 record says "**Capabilities rows appended** in the
table above (`## Capabilities`): `A12 case-independence closure` and `exact-grammar record audit`"
— and neither row exists in the table; the round-75 audit had no atom reading the table, because
its atom set was the ROUND-74 routed set and dropped the round-74 D8 capability-rows atom. So a
self-assessment sentence about the repertoire was written, contradicted by the card, and no
instrument could see the contradiction.

**Falsifiable before → after.** At base `5303a662` the round-76 audit exits 1 with
`mismatch_count 1` naming `D24_capability_rows`, whose evidence names exactly the two absent rows
(`A12 case-independence closure`, `exact-grammar record audit`); at the landing revision it exits
0 with `mismatch_count 0` over nine atoms `D16`–`D24`, every row `ok true`, and a defect-free
`validate` block.

**Predicate (one sentence, frozen).** R76-C1 is verified iff
`python3 -I -B tools/round-76/record-audit.py --root . --rev <measured> --json-out <receipt>`
exits 0 with `mismatch_count 0` over nine atoms `D16`–`D24`, every atom row `ok true`,
`validate {defects [], atoms 9}`, and atom `D24_capability_rows` true with its evidence naming the
round-75 claim line and the two rows; while the same command at base `5303a662` exits 1 with
`mismatch_count 1` naming exactly `D24_capability_rows` and defects naming those two rows, and the
selftest carries one red fixture per D24 failure shape (absent row, empty evidence cell, absent
evidence path, round mismatch, stub description, no claim line).

**Counting command.** `mismatch_count` is the counter; the machine block below is the command the
gate executes.

<!-- counting-command: C1 -->
```sh
python3 -I -B tools/round-76/record-audit.py --root . --rev $REV --json-out $OUT
```
<!-- /counting-command -->

**Kill rule.** An atom true at base for a reason its routed defect names; an atom false at the
landing; a `validate` defect; a D24 red fixture that passes; a claim line whose names are parsed
from a rewritten grammar after this freeze; an evidence pointer that does not resolve at the
measured revision → not verified, reported, never narrowed.

**Do-nothing control.** The round-75 audit (`tools/round-75/record-audit.py`) at base `5303a662`
reports `mismatch_count 0` over its eight atoms while both rows are absent: the prior state's
green record is exactly the defect. D24's six red fixtures show the new grammar can fail.

## R76-C2 — operability: the printed counting command executes as printed

**Type.** Capability acquisition. A plan or report's counting command is a runnable artifact
(AXES: "commands that exist, scripts that run"). Round 75 printed its R75-C1 counter as
`--expect-target-sha256 1fc1c8fc…` with no `--work`: pasted as printed it exits 2 at the
instrument's own preflight (`{"unevaluable": "missing required arguments: work"}`), so the number
it prints is not reproducible from the record by the reader it was printed for.

**Falsifiable before → after.** At base the battery exits 1 with `arms_ok 0` of 3 (no plan block,
no fixtures, no gate at `5303a662`); at the landing revision it exits 0 with `arms_ok 3` of 3:
`plan-c1` executes the plan's own `counting-command: C1` block verbatim and reads
`mismatch_count 0`; `r75-printed` refuses the round-75 printed command with
`PLACEHOLDER_UNBOUND` and executes nothing; `r75-argv` executes the same command with the digest
bound and reports `EXECUTION_FAILED` with the instrument's `missing required arguments: work` at
rc 2.

**Predicate (one sentence, frozen).** R76-C2 is verified iff
`python3 -I -B tools/round-76/plan-command.py --root . --rev <measured> --work <scratch>
--battery --json-out <receipt>` exits 0 with `arms_ok 3`, `arms_total 3`, `ok true`, each arm
carrying its expected observation (`plan-c1`: executed, rc 0, `mismatch_count 0`; `r75-printed`:
`PLACEHOLDER_UNBOUND` with `executed false`; `r75-argv`: executed, rc 2, stderr carrying
`missing required arguments: work`), while the same command at base `5303a662` exits 1 with
`arms_ok 0`, and the gate's three do-nothing controls each fail in their named way.

**Counting command.** `arms_ok` is the counter; the machine block below is the command the gate
executes (the battery re-runs the C1 block as its green arm).

<!-- counting-command: C2 -->
```sh
python3 -I -B tools/round-76/plan-command.py --root . --rev $REV --work $WORK --battery --json-out $OUT
```
<!-- /counting-command -->

**Kill rule.** An arm met for a reason other than its expected observation; a block executed
without its static grammar passing; a fixture arm that runs instead of refusing; a plan block
whose placeholder set is not exactly `$REV`/`$WORK`/`$OUT`/`$ROOT`; a command executed with a
shell, with a script outside `tools/round-76/`, or with `$WORK`/`$OUT` outside the work root →
not verified, reported.

**Do-nothing control.** `--control prose-plan` (the plan block replaced by the round-75 printed
command: `PLACEHOLDER_UNBOUND`, nothing executed), `--control missing-required-arg` (a runnable
argv with its required `--root` removed: `EXECUTION_FAILED` rc 2) and `--control ellipsis-rev`
(`$REV` replaced by an abbreviated hash: `PLACEHOLDER_UNBOUND`). All three are selftest cases.

## Instruments

Committed at the declaration, before any claim data, and pinned by sha256 in
`.ufo/waves/round-76/claims.json`:

- `tools/round-76/record-audit.py` — the round-75 audit plus D24 and its six red fixtures;
- `tools/round-76/plan-command.py` — the block extractor, static grammar, no-shell executor,
  four-key child environment, counter reader, battery, three controls and selftest.

Loaded by the counters (not themselves counted): `tools/round-75/record-audit.py` (the do-nothing
control for C1) and `tools/round-75/probe-mutation.py` (the fixture command C2 refuses).

## Frontier step (inside the claim cap, no extra claim)

- **SOURCES.md.** Two pages opened this round on **2026-11-04**: `shlex.split` (admitted, docs/A)
  — the shell-like tokenizer the gate uses so no shell ever runs a plan's bytes — and
  `argparse` `error()`/exit status (admitted, docs/A) — the documented status 2 the before-arm
  observes. One rejection: `sh(1)` (rejected: the claim's whole point is the shell the gate
  refuses to invoke; the consumer search is recorded in the lesson Gate).
- **Census.** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` at round
  start: exit 0, 191 rows, 24 W04 warnings (`.ufo/waves/round-76/l1/census-start.txt`).
- **Mistake mined.** The class: *a self-assessment sentence written before its artifact existed,
  and a printed command never executed by its author*. Captured by D24 and the plan-command gate,
  each shown able to fail before data.
- **Assimilation.** `merge/kaidoku/` does not serve these claims → `Assimilation: none`.
  `considerthese/` is absent in this lane (no directory).
- **Sourced claim.** R76-C2 cites S286/S287 through
  `corpus/knowledge/2026-11-04-r76-plan-command-executability.md`.

## Waves

One v1 wave `r76-w1`, 14 seats: 4 executor, 2 scribe, 2 reviewer, 1 critic, 1 mutation-tester,
1 sentinel, 1 scout, 1 connector, 1 labrat. Attack roles (reviewer/critic/mutation-tester/labrat)
5 of 14 = 36%. One connector. The L1 holds the planner seat. No residual call.
