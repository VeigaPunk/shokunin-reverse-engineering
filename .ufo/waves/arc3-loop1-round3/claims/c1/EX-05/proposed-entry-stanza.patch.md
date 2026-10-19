# PROPOSED entry stanzas — C1 arc3-round3 coverage (seat EX-05)

**Status: PROPOSAL, not landed.** Seat EX-05 (chain c1, executor) wrote no corpus
file, no LOG/SCORECARD/SHONEN text, and no README change this round (freeze rule:
patch text only). This file is the seat's proposed *content* for the C1 landing
(a new corpus knowledge entry, e.g. `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md`,
plus the matching line-neutral map token) — the implementer/reviewer owns the
final text, the citation form, and the entry's own identity. Every number below
was measured by this seat on its own pinned bytes; the implementing seat must
re-derive (rule #14) rather than copy.

Suggested entry title:

> `inspect-evm-interface` on optimizer-enabled and non-ERC-20 solc 0.8.37 carriers —
> K/K with zero extras; the dispatch topology is selector-count driven, not optimizer driven

Proposed observations (each one line, RESULT-class, evidence pointers only):

- **Carrier B, non-ERC-20 shape, optimizer on (`{enabled:true, runs:200}`):** `CarrierB`
  (payable `receive` + payable `fallback`, mixed view/pure/payable/nonpayable
  surface, internal-library arithmetic inlined) compiled on-host with the receipted
  r1 solc prefix; source `claims/c1/EX-05/src/CarrierB.sol` sha256 `289bc599…44b984f`,
  creation 1560 B `6794c3a2…3de6fdc0`, runtime 1469 B `b9c70178…4ebd7940`
  (`claims/c1/EX-05/out/`, report + input JSON in the same dir).
- **Observation (RESULT — K/K, both probe pins):** `rea-agents@6.4.0` hex and raw legs
  and `6.7.0` hex leg each report 8 functions, all `dispatch:"abi"`, set-equal to the
  planted set `3efdef66, 410673e5, 51f91066, 6ea056a9, 8da5cb5b, ca1d209d, d5d44d80,
  e7ee6ad6` (K = 8, derived from the compiler ABI; independent keccak oracle agreed);
  zero missing / zero extra; decoded `bytecode.sha256 b9c70178…` = the runtime bytes
  (`claims/c1/EX-05/probe/probe-runtime-hex-6.4.0.json` + `…hex-6.7.0.json` +
  `…raw-6.4.0.json`; the planted table was written 9.9 s before the first envelope).
- **Observation (zero-extras stress leg):** an attack variant whose source declares
  and uses two custom errors (`claims/c1/EX-05/src/attack/CarrierBErr.sol`) still reads
  8/8 with zero extras — `ev_bdc1db67…` — even though the optimized runtime embeds
  `245aecd3` (`NotOwner(address)`) directly and `1182d3d5` = `2305a7aa >> 1`, the latter
  being the halved form the compiler emits for the 2-arg error `2305a7aa`
  (`(0x1182d3d5 << 225) == (0x2305a7aa << 224)` = the ABI selector word; the
  unoptimized build of the same source carries the plain `2305a7aa` and lacks
  `1182d3d5`). The extractor is not a naive PUSH4-constant sweep.
- **Observation (dispatch topology — the round's delta vs r1):** every carrier probed
  here carries the `5f3560e01c` shift idiom and the `60043610` calldatasize guard; the
  legacy `60003560e01c` idiom appears in none — the r1 prologue lexicon is unchanged,
  so the freeze's "prologue class differs" branch does not fire. What changes is the
  dispatch topology: ≤ 6 selectors → linear `EQ` chain, ≥ 7 selectors → one `GT` root
  comparison over sorted selectors with `EQ` leaves (measured over N = 4…12 in BOTH
  optimizer modes; `claims/c1/EX-05/shape-boundary.txt`). r1's 11-selector attack
  carrier (optimizer OFF) already shows the GT-root topology, so the topology is
  **selector-count driven, not optimizer driven**; the optimizer's measured effect on
  these carriers is code size and jump-destination width (PUSH1 dests vs PUSH2 dests).
- **Observation (cross-seat re-derivation):** EX-04's carrier B (`VaultB`, 11 selectors)
  re-compiled by this seat with the seat's own driver reproduces EX-04's pins exactly —
  opt200 runtime 1850 B `aaf85cea…cf239412`, creation 2237 B `8466da5f…f22ee975`;
  noopt runtime 3872 B `679678e9…7d83d005`, creation 5276 B `45a6d3d7…4d4904f9`
  (`claims/c1/EX-05/recompiled/{opt200,noopt}/`). Two independently built compile
  drivers, one source, byte-identical output.
- **Route caveat (for every compile receipt in this round):** the standard-JSON unit
  name changes the embedded metadata CID and therefore the creation/runtime sha256 at
  the tail only (code region byte-identical; demonstrated by controlled experiment,
  `claims/c1/EX-05/route-parity.txt`). Receipts should state the unit name they used.

Proposed map token (line-neutral, implementer's form): a new token for this entry,
e.g. `2026-10-19-arc3-r3-evm-optimizer-shapes`, with the SCORECARD state cell
refreshed in the same commit — the existing r1 entry's stanza and the prior 82
knowledge files must stay byte-identical (the claim's "prior 82" clause).

Not proposed: any widening of the probe's table (C3's artifact), any census scope
change, or any availability→holding promotion — this stays RESULT-class, scoped to
solc-0.8.37-compiled on-host carriers under the pins named here.