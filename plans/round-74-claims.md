# Round 74 — declared claims (frozen; no amendments after this file's container commit)

Base `04fdc2c4dbedbe5ee50a069af14310068393233e` (the round-73 lane tip: the record, the
report and the round-73 non-author spot-check lesson; the lane tree is clean and pushed).
Two claims on two distinct axes, causally separable — each is scored by its own instrument and
none reads the other's result. Both are capability acquisitions in the AXES sense: the
instrument runs, its output verifies, and its row enters the SCORECARD capabilities table in the
same round.

**Lowest-axis obligation.** The lane's three owned proxies (coverage/depth/calibration) sit at
10.0 behind different proxies and are tied; the stagnation nudge's waiver condition is *not* met
(capability rows entered in rounds 70–73, inside the 10-round window), so no waiver is claimed.
**`lowest-axis: calibration`** — R74-C2 works a tied-lowest axis. The round-73 closure admitted
the same tie and worked coverage; a tie has no unique lowest member.

The round-73 non-author spot-check routed nine defects to this round
(`corpus/lessons/round-73-verifier-spotcheck.md` §6) and the round-73 record's `planned` list
carried items (a)–(e). This round's work is that queue, resolved as follows:

- planned (a) the six A12 selftest survivors + planned (c) the call-site case → **R74-C1**;
- planned (b) the D7 false-green + planned (d) the freeze-pin procedure → **R74-C2**;
- routed defects 1–8 (bookkeeping, the census erratum, the runner field, the trailing newline,
  the standing freeze flag) → **R74-C2**;
- planned (e) standing duties (census, lesson, source rows) → the frontier step, no claim slot.

## R74-C1 — operability: the six A12 selftest survivors die by declared cases

**Type.** Capability acquisition. Round 73's mutation probe (`MutProbe`) reported six A12
selftest survivors on the landed round-73 probe: deleting the genuine-canary conjunct, reading
an unreadable `/proc/<pid>/environ` as an empty environment, keeping only the first kernel
sample, dropping the `canary_present` field, swapping the verdict's two witnesses and skipping
the forged sub-run each left `--selftest` green. This round names the acquisition and wiring
seams those cases need and binds each conjunct to its own case.

**Falsifiable before → after.** At the base the ten defect classes applied to
`tools/round-73/seam-probe.py` score four killed and **six survivors** (`c1_base_world`); the
round-74 probe's selftest has 20 cases and the same ten classes score **zero survivors**, each
killed by its declared case. The call-site case (planned (c)) is `a12-arm-forged-executed`: the
forged sub-run is executed with an injected spawner and witness, and the case requires both
producer launches and the kernel poll to have happened — a mutant that returns the forged dict
as a constant is killed there, not by the seam-body case.

**Predicate (one sentence, frozen).** R74-C1 is verified iff the frozen battery
`tools/round-74/probe-mutation.py`, run at the measured revision as
`python3 -I -B tools/round-74/probe-mutation.py --root . --rev <measured> --tool
tools/round-74/seam-probe.py --patch-set r74probe --work <scratch> --expect-survivors 0
--expect-target-sha256 <the r74 probe's sha256 at <measured>> --json-out <receipt>`, exits 0
with `survivor_count 0`, every mutant `killed` with its `expect_case` in its `failed` list,
`pristine {cases 20, failed [], rc 0}` and `target_pin.matched true` — while the same battery
with `--patch-set r73probe --tool tools/round-73/seam-probe.py --expect-survivors 6` exits 0
reporting exactly the six survivors `a-drop-genuine-canary, b-unreadable-empty,
b-first-sample-only, b-drop-canary-field, c-swap-verdict-inputs, c-skip-forged-subrun`.

**Counting command.** The two battery commands above; `survivor_count` is the counter.

**Kill rule.** A survivor; a mutant killed by a case other than its declared one
(`killed_wrong_case`); a pristine selftest that is not green or shorter than 20 cases; an
unpinned target; a base arm that does not name all six survivors → not verified, reported,
never narrowed.

**Do-nothing control.** `tools/round-74/controls.py` arm `c1_base_world` (the round-73 blob: four
killed, the six survivors) and arm `c1_no_declared_cases` (the round-74 probe with the six case
names renamed, assertions unchanged: the six mutants are `killed_wrong_case` and no kill — a red
selftest alone does not satisfy the claim).

## R74-C2 — calibration: the record binds the round-73 routed set, its own pointers and its freeze pins

**Type.** Capability acquisition. The lane's self-assessment is checked against committed bytes
by a frozen atom table derived from an **outside** document — the round-73 non-author spot-check's
routed-defect list — never from the table it audits (QUALITY #111). Round 74 adds nine atoms:
`D7b` (a claim row naming two before arms must append a selection block naming which is the
before-arm and each other receipt's role — the false-green `D7` never noticed), `D8` (the
capabilities table carries three round-73 and two round-74 rows, each with a resolving pointer),
`D9` (S275's `used-by` names the round-73 entry that cites it), `D10` (the search log carries
round-73 and round-74 notes), `D11` (each page opened and rejected in round 73 has a `rejected`
row with reason and flip), `D12` (the census erratum names both the reported 24 W04 lines and
the measured 23), `D13` (`corpus/README.md` is newline-terminated), `D14` (a before receipt
binds its runner path and sha256) and `D15` (every pin in the freeze container equals the blob
at the first commit that added `claims.json` — planned item (d)). `D3` and `D6` extend to the
round-74 record (gate ledger row, lowest-axis declaration).

**Falsifiable before → after.** At base `04fdc2c4` the audit exits 1 with `mismatch_count 11`
naming `D3, D6, D7b, D8, D9, D10, D11, D12, D13, D14, D15`; at the landing revision it exits 0
with `mismatch_count 0` over 16 atoms.

**Predicate (one sentence, frozen).** R74-C2 is verified iff the frozen audit
`tools/round-74/record-audit.py`, run at the measured revision as
`python3 -I -B tools/round-74/record-audit.py --root . --rev <measured> --json-out <receipt>`,
exits 0 with `mismatch_count 0` over its 16 atoms and every atom row `ok true` — while the same
command at base `04fdc2c4` exits 1 with `mismatch_count 11` naming exactly the eleven atoms
above, and the same command's `--validate` returns no defect on the landing receipt.

**Counting command.** The audit command above; `mismatch_count` is the counter.

**Kill rule.** An atom true at the base for a reason its routed defect names (then the atom does
not bind the defect); an atom false at the landing; a `--validate` defect; an atom added,
removed or re-worded after this freeze → not verified, reported.

**Do-nothing control.** `tools/round-74/controls.py` arm `c2_do_nothing` (the audit at base
`04fdc2c4`: every atom added this round is false there) and arm `c2_selftest_reds` (the audit's
parser selftest carries the red arms `selection-two-arms-red` and `used-by-wrong-entry-red`, so
the parsers are shown able to fail).

## Frontier step (inside the claim cap, no extra claim)

- **SOURCES.md.** One row opened this round: man7 `ptrace(2)` (`PTRACE_MODE_READ_FSCREDS`), the
  read-permission gate behind an unreadable `/proc/<pid>/environ`. It grounds C1's
  `a12-proc-environ-unreadable` case: an unreadable environ must be omitted, never read as
  empty. The four pages opened and rejected in round 73 are registered as `rejected` rows
  (routed defect 4).
- **Census.** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` at round
  start (exit 0, 184 rows) and at round end (exit 0).
- **Mistake mined.** Round 73 froze its before-arm as "the same probe against the round-72 route
  reports 11 of 12" — a comparator the instrument could not produce (it reports 8 of 12), and
  its freeze pinned two producer digests that were not the blobs at the freeze. Both are the
  same class: a record value written from a plan rather than from the bytes; captured by the
  freeze-pin procedure (planned item (d)) and by `D7b`'s selection block.
- **Assimilation.** The `merge/kaidoku/` package does not serve these claims →
  `Assimilation: none`. `considerthese/` is absent in this lane (no directory).
- **Sourced claim.** R74-C1 cites S278 through
  `corpus/knowledge/2026-11-04-r74-probe-mutation-closure.md`.

## Waves

One v1 wave `r74-w1`, 15 seats: 5 executor, 3 scribe, 2 reviewer, 1 critic, 1 mutation-tester,
1 sentinel, 1 scout, 1 connector. Attack roles (reviewer/critic/mutation-tester/mutation-tester
class) 4 of 15 = 27%. One connector. The L1 holds the planner seat. No residual call.
