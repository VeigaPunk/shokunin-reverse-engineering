# Round 68 — declared claims (frozen; no amendments after this file's container commit)

Base `fcbe200f6739c38939e0dabf3f251de2cc6bd727`. Two claims on distinct axes, causally separable:
each is scored by its own instrument and neither reads the other's result. Both are capability
acquisitions in the AXES sense: the instrument runs, its output verifies, and its row enters the
SCORECARD capabilities table in the same round.

## R68-C1 — calibration: the instrument registry is conformant over its own regime

**Type.** Capability acquisition (a conformance census over the lane's instrument inventory) plus the
self-assessment repair the round-67 outside closure routed (its defect 2).

**Falsifiable before → after.** At the base the lane's own registry (`SKILL.md`, the
`<!-- instrument-registry v2 -->` table) is the self-assessment of which instruments exist; the
plans name instruments the table does not carry, and nothing in the lane compares the two. The
round-67 closure found the pair for the round it had just closed
(`tools/round-67/avm-le-counter.py`, `tools/round-67/mutation-battery.py`), which is 2 mismatches.
After the repair the same census, over the same regime, reports 0.

**Predicate (one sentence, frozen).** R68-C1 is verified iff the frozen registry-conformance census,
run at the measured revision, reports `mismatches 0` with `scope_size 71` and `registry_rows 77`,
while the same census run at the base revision `fcbe200f6739c38939e0dabf3f251de2cc6bd727` reports
`mismatches 2` and names exactly `tools/round-67/avm-le-counter.py` and
`tools/round-67/mutation-battery.py` as unregistered.

**Regime (declared, not inferred from the data).** Scope = every `tools/round-N/<name>.(py|sh|mjs)`
path that `plans/round-N-claims.md` names for its OWN round N, N ≥ 41 (the round the registry begins
at), that exists as a blob at the revision. A plan citing another round's tool cites that round's
regime. Rounds below 41 are reported as `legacy_unregistered` and never counted. Rows whose path is
absent at the revision, duplicate rows, and verdict cells that do not name all three exit codes are
mismatches too — at the base all three sets are empty, which the before-arm records.

**Counting command.**
`python3 -I -B tools/round-68/registry-conformance.py --root <lane> --rev <rev> --json-out <receipt>`
exit 0 = clean, 1 = a named mismatch set, 2 = could-not-evaluate.

**Kill rule.** Any unregistered, duplicate, absent-at-rev or thin row at the measured revision; a
before-arm that does not name the two round-67 instruments; a post-freeze instrument edit; or a run
that needs the predicate changed → not verified, reported, never narrowed.

**Do-nothing control.** `.ufo/waves/round-68/l1/pre/controls-at-base.json` arm `c1-shortcut-self`
(a census whose scope is the registry's own rows) reports 0 mismatches at the base while the defect
exists, and arm `c1-constant-zero` reports 0 without reading anything: both are false greens, which is
why the census reads the plans, not the table, for its scope.

## R68-C2 — coverage: the packed-ELF triage route

**Type.** Capability acquisition (a new owned surface: packing detection, unpacking with byte
identity, and inventory recovery through REA).

**Falsifiable before → after.** At the base the lane has no packed-binary route: `upx` is a name in
PROVINCE's fallback-reader list, REA analyzes the packed bytes it is given and reports the loader stub
(3 procedures on each carrier, below each carrier's declared floor), and an address-level verb on
those bytes is refused. After the route exists, the same two carriers are detected as packed,
unpacked to bytes whose sha256 equals their pins, and recover the original's REA inventory
(167/30/190 and 99/29/103 on procedure/segment/string counts), while the packed stub still refuses the
pinned address.

**Predicate (one sentence, frozen).** R68-C2 is verified iff the frozen packed-ELF counter, run at
the measured revision over its two pinned carriers, reports `carriers_matched 2` of `target 2` and
`control_ok true` with every arm true on both carriers (`detected`, `before_ok`, `identity_ok`,
`recovery_ok`, and `refusal_ok` on the carrier that pins an address), reports the packed bytes of both
carriers at exactly 3 procedures, and reports the non-packed original as neither listed nor
decompressible by the packer.

**Counting command.**
`python3 -I -B tools/round-68/packed-elf.py --root <lane> --rev <rev> --pkg <rea-agents root> --work <scratch> --json-out <receipt>`
exit 0 = met, 1 = not met (every false arm named), 2 = could-not-evaluate.

**Kill rule.** A carrier whose pin drifted; a detection that fires on the unpacked or original bytes;
an unpack that does not restore the pinned bytes; an inventory that does not equal the original's; a
packed-bytes inventory at or above the floor; a refusal arm that does not separate packed from
unpacked; a post-freeze instrument edit; or a run that needs the predicate changed → not verified,
never narrowed.

**Do-nothing control.** `.ufo/waves/round-68/l1/pre/controls-at-base.json` arms `c2-packed-only`
(verdict from the packed arm alone) and `c2-no-identity` (unpack and recovery, identity dropped) are
both not met: no shortcut reaches the target.

## Repairs carried (not claims, recorded with their own evidence)

1. The round-67 entry's stale rule identity (`corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md:33`,
   `b55d5e87…` + a `removed.silent.char-device` row) gets an appended correction block naming the
   superseded sentence, the cited sha, the rule's actual sha (`e66ba022…`) and the silent row's absence
   (QUALITY #65/#100: corrections are appended).
2. The registry rows themselves (the four the census needs: the two round-67 instruments and this
   round's two).
3. The QUALITY #100 companion row for the round-64 findings cell in `corpus/claim-freezes-corrections.tsv`.
4. The prefile gate's own output committed as a receipt, and the superseded `corpus/claim-freezes.tsv`
   retired with a named erratum.
5. This round's C2 kill rule says *undisclosed* post-freeze edit; every receipt names the revision that
   bears the instrument (`instrument.rev`) beside the measured revision.
6. The round-67 report's prompt-hash erratum (`b8507c60` is the round-66 prompt; `754f9074` is r67's)
   lands in this round's report, never as a rewrite of the filed bytes.

## Frontier step

One new `corpus/SOURCES.md` row, opened this round, grounds the packed route's identity rule; the
knowledge entry `corpus/knowledge/2026-11-03-r68-packed-elf-route.md` cites it. The census is run at
round start and round end; one mistake is mined into `corpus/lessons/round-68.md`.

## Assimilation

`merge/kaidoku/` holds no staged theme that fits a registry census or a packed route (the `.jsc`
theme was adopted in round 64); `considerthese/` is absent (`ls considerthese` exit 2). Recorded as
`Assimilation: none` in the report's Sources & frontier section.
