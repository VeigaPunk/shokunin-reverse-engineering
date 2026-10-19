# Proposed patch text — c1 corpus delta from EX-13 (prologue/dispatch-shape finding)

Status: **proposal only, not applied.** For the c1 landing seats (the round's corpus
knowledge entry is the chain's real target; this seat is not its designated writer).
All claims below are measured in `prologue-delta.md` + `evidence/` (same seat dir).

## Patch A — observation block to add to the round-3 c1 knowledge entry

```
- **Observation (dispatch-shape classes — this round's delta):** all 26 on-host solc
  0.8.37 runtimes (default evmVersion `osaka`; optimizer off and
  `--optimize --optimize-runs 200` arms) carry the r1-recorded PUSH0 prologue
  `5f3560e01c` exactly once; `60003560e01c` and `60043560e01c` occur zero times.
  Preamble offset class: nonpayable-only carriers anchor at pc 25 (CALLVALUE guard),
  payable receive/fallback carriers at pc 13 (`6080604052 60043610 61007e 57` +
  anchor; the <4 target 0x7e splits receive vs fallback). Dispatcher topology class:
  linear-EQ chains for K <= 6 selectors; GT-pivot sorted binary search for K >= 7
  (`80 63 <pivot> 11 61 <dest> 57` before the EQ legs; the pivot selector appears
  both as GT and EQ leg; measured pivot counts 1/1/3/7 at K=8/9/17/33) — identical
  optimizer-off and optimizer-on, and in both preamble classes. The optimizer changes
  runtime size (~44-51% shrink), destination PCs, and adds `4e487b71` Panic
  constants; it does not change prologue class, anchor offset, or topology class.
- **Observation (extractor on the new shapes):** 16 inspect-evm-interface legs
  (rea-agents 6.4.0 x 12 carriers; 6.7.0 x 4) all K/K, zero missing, zero extra —
  including pivot dispatchers (K=8/9/17/33) and optimizer-enabled bytes; decoded
  `bytecode.sha256` equals the compiled runtime sha256; every reported
  `bytecodeOffset` is a JUMPDEST and equals the EQ-leg destination for that
  selector; zero false positives (non-dispatch PUSH4 immediates `16ee4b79`,
  `4e487b71`, `ffffffff` were not reported). Source:
  `.ufo/waves/arc3-loop1-round3/claims/c1/EX-13/prologue-delta.md`.
- **Observation (size band):** sw32-off (3,040 B runtime, 33 selectors) probed K/K —
  above r1's ~1.8-1.9 KB band.
```

## Patch A — Unknowns narrowing (use in the new entry; do not edit the r1 entry in place)

```
- **Unknowns:** Vyper and other solc versions; optimizer-enabled dispatch shapes
  beyond the smoke compile — DISCHARGED for solc 0.8.37 / evmVersion `osaka` by the
  dispatch-shape observations above; dispatcher prologues other than
  `5f3560e01c`/`60003560e01c` — still open (the legacy class did not re-materialize at
  osaka; only synthetic controls exist in-tree); the `ev_` id domain for this verb
  family; whether 6.7.0's CBOR metadata decode generalizes; behavior at carrier sizes
  above the probed ~1.8-1.9 KB runtime class — partially exercised (3,040 B, §size
  band above); deployment/chain identity (never claimed by the tool).
```

## Patch A — sources line additions

```
sources: ... ; `.ufo/waves/arc3-loop1-round3/claims/c1/EX-13/prologue-delta.md` +
`.../claims/c1/EX-13/evidence/{summary,fine-summary,sweep-summary,prologues,compare}.json`
+ `.../claims/c1/EX-13/evidence/probes/` (16 envelopes, manifest sha256-pinned).
```

## Rationale and limits (for the landing seat)

- The threshold K<=6 / K>=7 is a **measurement** over 8 carriers per side (two
  preamble classes, both optimizer settings), not a source-cited compiler mechanism —
  phrase it as measured, as drafted.
- Carriers are this round's, compiled on-host with the receipted r1 solc prefix;
  rv2-off reproduces r1's recorded runtime (`c1081a56…`) and hex (`d7f73058…`) bytes
  exactly, so the delta sits on an r1-validated pipeline.
- Cross-seat corroboration worth citing in the entry if desired: EX-04's VaultB
  (K=11) shows the same EQ+GT binary search and K/K; VZ-1's `rv2tokenopt` probe
  decodes to `ed6c8a76…` == this seat's rv2-on200 runtime sha.