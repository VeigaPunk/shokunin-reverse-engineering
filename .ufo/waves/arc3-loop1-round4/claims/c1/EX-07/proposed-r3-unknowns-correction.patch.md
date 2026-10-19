# Proposed patch text — arc3-r3 EVM entry, Unknowns line (c1, round 4, seat EX-07)

Target file: `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md`
Line: the single `- **Unknowns:**` line (file path only — no line number, per rule #11).
Line-neutral: the replacement text is a same-line substitution; the file's line
count is unchanged (37 lines before and after).

## Why

The r3 Unknowns line reads:

> …; whether 6.7.0-specific envelope deltas (e.g. `relationship_coverage` present
> only there, `EX-07/legA-compare.txt`) generalize; deployment/chain identity …

Measured this round (seat EX-07, first-hand, 66 envelopes): `relationship_coverage`
is **absent at 6.4.0 and present at both 6.5.0 and 6.7.0** (value `null`), with the
`limitations` array at 6 vs 7 entries (the extra line being the terminal-CBOR-metadata
caveat). This holds on six carrier families — three r3 solc carriers re-probed
(VaultB opt200, VaultB nopt, Rv2TokenOpt) and three r4 Vyper carriers (EX-02 Smoke,
EX-04 CarrierV, EX-03 Steward), hex and raw, in-place and scratch-copy. The
6.5.0→6.7.0 envelopes are byte-identical apart from `evidence_id` (0 diff lines on a
key-sorted comparison); the whole delta sits at the 6.4.0→6.5.0 boundary (36 diff
lines on the solc carriers, 12 on the Vyper carriers — the difference being the
solc-only `raw_result.metadata` CBOR decode, which the Vyper carriers do not carry).

So the delta is **not** 6.7.0-specific: it is "≥6.5.0" and, in the envelope as
emitted, it is a single release boundary at 6.5.0. The r3 entry's own reference
(`EX-07/legA-compare.txt`) only compared 6.4.0 vs 6.7.0 and so could not see it.

## Proposed replacement (same line, line-neutral)

old (substring, unique in the file):

```
whether 6.7.0-specific envelope deltas (e.g. `relationship_coverage` present only there, `EX-07/legA-compare.txt`) generalize;
```

new (substring):

```
whether the 6.5.0+ envelope deltas (e.g. `relationship_coverage`, present at 6.5.0 and 6.7.0 but absent at 6.4.0 — re-measured r4 on six carrier families, `.ufo/waves/arc3-loop1-round4/claims/c1/EX-07/compare-legs.out`) generalize;
```

## Evidence

- `.ufo/waves/arc3-loop1-round4/claims/c1/EX-07/compare-legs.out` §6 (envelope key
  delta by pin, all six families) and §1 (per-leg table).
- r3's own 6.5.0 captures agree: `.ufo/waves/arc3-loop1-round3/claims/c1/EX-07/optB-hex-6.5.0.json`,
  `legA-hex-6.5.0.json`, `legC-hex-6.5.0.json` all carry the key; the 6.4.0 legs of
  the same files do not (`analysis.py:42` in that seat reads the same key).
- Byte-identity of my 6.4.0/6.7.0 solc hex envelopes against r3's stored captures:
  `05f76b33…` (opt200 6.4.0), `8336351f…` (opt200 6.7.0), `aad4d0e1…` (nopt 6.4.0),
  `aa1f928d…` (nopt 6.7.0) — `sha256sum` in `legs/MANIFEST.sha256`.

## Note for the reviewer (not part of the patch)

This is a wording correction of an Unknown, not a defect claim about the tool: the
Unknown asked whether the delta generalizes, and the answer measured this round is
"yes, across families, but the boundary is 6.5.0, not 6.7.0". Applying it does not
change the entry's RESULT-class scope or any Observation line.

## Patch simulation (run first-hand at the work tree, before proposing)

- target file line count: **37**; `old` occurs **1** time (unique);
- after substitution: **37** lines — line-neutral confirmed;
- target file identity at simulation time: `bf39c584…` (37 lines), i.e. the entry as
  it stands at HEAD `015e1bab…`. If the parent lands other edits to this entry
  first, re-run the simulation before applying — the `old` substring is a single
  line, so a conflicting revision would show as `old occurs: 0`.
