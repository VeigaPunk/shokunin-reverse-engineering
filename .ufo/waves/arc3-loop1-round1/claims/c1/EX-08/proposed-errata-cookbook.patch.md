# Proposed changes — EX-08 (arc3-loop1-round1, chain c1) — PATCH TEXT, NOT APPLIED

Seat: EX-08 (control probes). Nothing was written to any repo target; this file
is a proposal for the parent to integrate (or reject) at record time.

## Proposal 1 — corpus errata line for `corpus/knowledge/2026-10-13-r3-evm-interface.md`

Append to the existing `## Errata (round 4)` section (or add `## Errata (arc3-loop1-round1)`):

```markdown
## Errata (arc3-loop1-round1)

- **Dispatcher prologue must load calldata at offset 0.** EVMole labels the SHR
  result as the selector only when the loaded word's low 4 bytes equal its
  synthetic calldata selector `aabbccdd` (`cdump/evmole` @ `go/v0.9.3`,
  `src/selectors/mod.rs:145-156` + `src/selectors/calldata.rs`
  `SYNTHETIC_SELECTOR`), which holds only for `CALLDATALOAD` at offset 0
  (`60003560e01c`, or solc 0.8.x's `5f3560e01c`). A plausible-but-wrong
  `60043560e01c` (offset 4) prologue returns `functions: []` with exit 0 — no
  refusal, shape-identical to "no dispatch exists". Control carriers:
  `.ufo/waves/arc3-loop1-round1/claims/c1/EX-08/variants2/{off0,off4,push0}.hex`
  (off0/push0 → 3/3 selectors, off4 → 0).
- **Carrier bytes remain unrecoverable (re-confirmed).** A bounded structural
  search over 1,580,544 candidate 81-byte assemblies found no sha256 match to the
  recorded `3e2fd6ca…fe67`; r4 audit-A's elision verdict stands. A same-shape
  81-byte rebuild (`60003560e01c` prologue, JUMPDEST targets 62/68/74) reproduces
  the recorded outcome exactly: 3/3 selectors at the recorded offsets,
  `dispatch:"abi"`, zero false positives, hex ≡ raw, identical on rea-agents
  6.4.0 and 6.7.0 (evmole@0.9.3).
```

## Proposal 2 — cookbook line for the lane's command cookbook / `PROVINCE.md:54` row

```markdown
| EVM interface | `rea inspect-evm-interface <file> <raw|hex>` — encoding POSITIONAL;
EVMole needs the selector prologue to be `PUSH1 00 CALLDATALOAD PUSH1 e0 SHR`
(offset-0 load) or `PUSH0 CALLDATALOAD PUSH1 e0 SHR`; a wrong prologue fails
SILENT (exit 0, `functions: []`); worker needs a writable TMPDIR (system /tmp is
EDQUOT-broken on this host → set `TMPDIR`; unset TMPDIR yields
`execution_failure` "Unknown system error -122") |
```

Both proposals are evidence-backed by the artifacts under
`.ufo/waves/arc3-loop1-round1/claims/c1/EX-08/` (see `probe-matrix.md`).
