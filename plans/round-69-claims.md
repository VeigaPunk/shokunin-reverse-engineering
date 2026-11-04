# Round 69 — declared claims (frozen; no amendments after this file's container commit)

Base `d7d9a62cc70935304e600ed0dee864fc4f1751f7`. Three claims on three distinct axes, causally
separable: each is scored by its own instrument and none reads another's result. All three are
capability acquisitions in the AXES sense — the instrument runs, its output verifies, and its row
enters the SCORECARD capabilities table in the same round. The stagnation nudge is in play: every
owned axis sits at 10.0 (saturation line 10.0, window 10; `SCORECARD.md`), so the lowest-axis
obligation is waived and this round is a capability/frontier move.

The instrument under test is `tools/round-69/packed-elf.py`, a supersession of the round-68 route
(`tools/round-68/packed-elf.py`, kept byte-identical at its own round). The route's scope is
unchanged: detect a UPX-packed ELF, unpack it with sha256 identity, recover the original's REA
inventory.

## R69-C1 — calibration: the route's five known mutation survivors are killed by its own selftest

**Type.** Capability acquisition (an arm-false selftest that can feed each arm a false input) plus
the repair of the round-68 routed defect M68-6.

**Falsifiable before → after.** At the base the route's gate cannot see the five 2026-11-03 mutants:
the round-68 wave showed each of M1_identity, M2_recovery, M3_detected, M4_before and M5_control
survives `--selftest` green at 13 cases (and survives a real green run too). After the round the same
five patches must each fail the instrument's own selftest, naming the arm-false case that binds the
mutated arm; the base instrument still shows the five survivors, so the before-arm is re-derived by
the same battery over committed bytes.

**Predicate (one sentence, frozen).** R69-C1 is verified iff the frozen mutation battery, run at the
measured revision against `tools/round-69/packed-elf.py` with patch set `r69`, reports
`survivors []` with all five mutants `killed` and each kill's `failed` list naming its declared
arm-false case (`M1_identity`→`arm-pack-identity-false`, `M2_recovery`→`arm-pack-recovery-false`,
`M3_detected`→`arm-pack-detected-false`, `M4_before`→`arm-pack-before-false`,
`M5_control`→`arm-pack-control-false`) and `pristine.cases 20` with `pristine.ok true`, while the
same battery against `tools/round-68/packed-elf.py` at the base revision
`d7d9a62cc70935304e600ed0dee864fc4f1751f7` with patch set `r68` reports exactly the five survivors
`M1_identity`, `M2_recovery`, `M3_detected`, `M4_before`, `M5_control` and `pristine.cases 13`.

**Counting command.**
`python3 -I -B tools/round-69/mutation-check.py --root . --rev <measured> --tool tools/round-69/packed-elf.py --patch-set r69 --work <scratch> --json-out <receipt>` —
exit 0 met (0 survivors, every kill names its case), 1 missed (each survivor named), 2 could-not-evaluate.

**Kill rule.** Any survivor, any kill whose `failed` does not name the declared case (a syntax error
is not a gate), a pristine selftest not green, a patch site that matches zero or several times, a
before-arm that does not show the five survivors, or a post-freeze instrument edit → not verified,
reported, never narrowed.

**Do-nothing control.** `.ufo/waves/round-69/l1/pre/controls-at-base.json` arm `c1-do-nothing`
(the r68 instrument + r68 patch set, scored by this same battery) reports `survivor_count 5`; arm
`c1-constant-battery` (a receipt with no mutant rows claiming zero survivors) is rejected by
`mutation-check --validate`, so the counter cannot be satisfied by an empty receipt.

## R69-C2 — operability: the route's contract is typed, pinned and recorded

**Type.** Capability acquisition (a typed preflight/exit-2 contract and an enforced packer pin) plus
the repair of the round-68 routed defects M68-4, ADV-2 and ADV-3.

**Falsifiable before → after.** At the base the route's promised exit-2 contract is prose: a missing
`node` and an unwritable `--work` escape as Python tracebacks with exit 1 (measured at the base by
the frozen probe, A1/A2), the packer pin is recorded but never enforced (A3/A4 are not even
implementable — the base instrument has no `--upx` seam), and the carrier records name neither
format nor packing mode, nor the pin in the receipt (A5/A6). After the round the same six arms pass
against the new instrument and a receipt it wrote.

**Predicate (one sentence, frozen).** R69-C2 is verified iff the frozen contract probe, run at the
measured revision against `tools/round-69/packed-elf.py` with the measured run's receipt, reports
`arms_passed 6` of `target 6` — `A1_missing_node`, `A2_work_unusable`, `A3_packer_version`,
`A4_packer_sha256`, `A5_carrier_record` and `A6_packer_pin` each true — while the same probe against
`tools/round-68/packed-elf.py` and its own round-68 landing receipt
`.ufo/waves/round-68/l1/scores/c2-at-landing.json` at the base revision reports `arms_passed 0` of 6
naming all six arms.

**Counting command.**
`python3 -I -B tools/round-69/contract-probe.py --root . --rev <measured> --tool tools/round-69/packed-elf.py --pkg <REA 6.5.0 root> --work <scratch> --receipt <measured run receipt> --json-out <receipt>` —
exit 0 met, 1 each failed arm named with its observation, 2 could-not-evaluate.

**Kill rule.** Any arm false; a receipt whose carrier pins/formats/modes do not equal the probe's own
derivation from the pinned source bytes; a receipt whose packer pin is not enforced and equal to the
host packer; a before-arm that does not show 0 of 6 with all six named; or a post-freeze instrument
edit → not verified, reported.

**Do-nothing control.** `controls-at-base.json` arm `c2-do-nothing` (base instrument + base receipt,
this same probe) reports `arms_passed 0`; arm `c2-constant-probe` (a receipt with no arm rows
claiming 6 passed) is rejected by `contract-probe --validate`.

## R69-C3 — coverage: the packed shared-object class enters Core on a pinned carrier

**Type.** Capability acquisition (a new carrier class in the route) — Frontier ground moved to Core.

**Falsifiable before → after.** At the base the route owns two executable carriers
(`/usr/bin/jq`, `/usr/bin/xxd`); PROVINCE's round-68 frontier note names "packed libraries and static
binaries" as still Frontier, and the base instrument's `CARRIERS` carries no shared object. After the
round a third pinned carrier of kind `shared-object` (`/usr/lib/libz.so.1.3.2`, sha256
`6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9`) is measured through the same
route: detected, unpacked byte-identically, and its REA inventory recovered (184/29/199 original vs
98/6/136 packed vs 184/29/199 recovered on procedure/segment/string).

**Predicate (one sentence, frozen).** R69-C3 is verified iff the frozen receipt checker, run at the
measured revision over the instrument's three-carrier receipt, reports `met true` with `target 3`,
`carriers_matched 3`, `control_ok true`, `failing []`, every carrier's `before_ceiling_ratio` at or
below `0.75`, and one carrier of `kind` `shared-object` (`libz`), while the same checker over the
round-68 receipt `.ufo/waves/round-68/l1/scores/c2-at-landing.json` reports `target 2` and no
shared-object carrier.

**Counting command.**
`python3 -I -B tools/round-69/packed-elf.py --check-receipt <three-carrier receipt>` — exit 0 met,
1 each failing clause named, 2 unreadable.

**Kill rule.** A carrier arm false, a ceiling ratio above 0.75 (a ceiling looser than three quarters
of the original inventory is not evidence that the packed bytes are the stub), no shared-object
carrier, a `target` other than 3, or a post-freeze instrument edit → not verified, reported.

**Do-nothing control.** `controls-at-base.json` arm `c3-do-nothing` (`--check-receipt` on the round-68
receipt) reports `target 2 != 3` and no shared-object carrier; arm `c3-loose-ceiling` (a synthetic
receipt with one ratio at 0.9) is rejected, so the ceiling relation is load-bearing; arm
`c3-synthetic-met` proves the checker can pass a receipt inside the bounds.

## Repairs carried (not claims)

The round-68 non-author closure routed six conformance defects; all six are closed or answered this
round under the round's LOG entry, never as claim input: R68-V1 (the round-68 knowledge entry's
line-start provenance trio, as an appended correction block), R68-V2 (the knowledge-index row moved
below its table delimiter), R68-V3 (a committed prefile PASS receipt at the ticket tree), R68-V4
(`tools/round-29/prefile-check.sh` prose and its unreachable `${got:-absent}` branch, plus an appended
LOG correction — never a rewrite of the filed line), R68-V5 (the S269 word-count: a superseding row
carrying the correct count and the reason), R68-V6 (a report erratum naming the single
advisory-corrected registry row).

## Frontier step (§2b)

`corpus/SOURCES.md` gains only rows opened this round (the lesson `## Gate` carries URL, access date
and a ≤25-word located quote). R69-C2's packer-pin arm rests on the UPX 5.2.0 documentation row
opened this round for the pin/`--version` surface (a new row: the round-68 S269 row covers byte
identity, not packer identity); at least one claim names it. One mistake is mined into
`corpus/lessons/round-69.md` `## Mistakes` (candidate: the round-68 landing's `format`/`mode` record
gap, M68-4, captured by none until the closure routed it). No `considerthese/` directory exists in
this lane; `Assimilation: none` this round (the `merge/kaidoku/` package themes do not serve these
three claims; the frozen claims may not be widened).
