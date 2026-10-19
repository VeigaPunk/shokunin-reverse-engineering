# PROVINCE.md repair — Frontier bullet "EVM bytecode (extended)": real solc bytecode is no longer untested

Authored by SEAT EX-13 (chain c2, executor), wave `arc3-loop1-round4`, 2026-10-19.
**Patch text only** — seats never write `PROVINCE.md`; the parent applies.

## Stale item (census-checked, falsified) — the C2 claim's own named debt

`PROVINCE.md` Frontier bullet `EVM bytecode (extended)`, current bytes:

> (Core, r3-07); real solc/vyper-compiled bytecode untested; selectors stay
> bare hashes (no signature DB → no name resolution).

`real solc/vyper-compiled bytecode untested` is falsified for the **solc** half
by admitted corpus state:

- `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` (admitted) — title:
  "inspect-evm-interface on real solc bytecode — selectors recovered K/K on
  on-host 0.8.37 compiles (5/5, 6/6, 11/11)"; carriers compiled on this host
  with solc `0.8.37+commit.f401782d`.
- `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md` (admitted) —
  optimizer-enabled and non-ERC-20 dispatch shapes, 13/13, 11/11, 8/8, 5/5.
- `corpus/README.md` (EVM row) — "held — EVMole selectors recovered from a
  synthetic dispatcher (r3-07) **and from real solc-0.8.37-compiled runtime
  carriers (arc3-r1)**; positional encoding quirk".

The **vyper** half is *not* repaired here, deliberately: at write time
`corpus/knowledge/` holds 83 files and no vyper entry has landed, so
`vyper-compiled bytecode untested` remains true **against admitted corpus
state**. (C1's vyper leg has succeeded in the wave tree — `CarrierV.vy`,
vyper `0.4.3+commit.bff19ea2`, 15/15 selectors — but the entry is still staged
as patch text at `claims/c1/records-drafts/knowledge-entry-draft.md`. A repair
must track the admitted state, not the wave tree; this patch is re-keyed when
that entry lands.)

## Change (same-line replacement, line count held at 3)

`PROVINCE.md`

```diff
# file: PROVINCE.md
-- **EVM bytecode (extended)** — selectors held on synthetic dispatcher
-  (Core, r3-07); real solc/vyper-compiled bytecode untested; selectors stay
-  bare hashes (no signature DB → no name resolution).
+- **EVM bytecode (extended)** — selectors held on synthetic dispatcher
+  (Core, r3-07) and real solc-0.8.37 carriers (RESULT-class, arc3-r1); vyper
+  bytecode untested; selectors stay bare hashes (no signature DB → no name resolution).
```

## Census conformance

- Line-neutral: 3 → 3 lines; `PROVINCE.md` stays at 162 lines (DATED marker at
  line 119 does not shift).
- Needle-free: `solc-0.8.37` is not a census needle (the instrument's bare-version
  regex requires a leading `6.`), and the replacement introduces no
  `rea-agents@x.y.z` and no `~`/`/`-absolute `path:line`. EX-14 measured that
  writing `rea-agents@6.5.0` into this exact line reads `FAIL (undeclared=1)` —
  this patch introduces no such token, and the census parses the block
  `gated=False, needles=[]`.
- The trailing clause (`selectors stay bare hashes …`) is preserved verbatim —
  it is still true and is not part of the debt.

## Overlap note (avoid double-landing)

`claims/c2/EX-14/evidence/demo-frontier-repair.patch.md` (sha256
`507b00610686f6a215901eefdaf93223bb592001205433f2579e2373b62add51`) is a
**demonstration** patch whose wording for this same bullet is identical to the
replacement above. EX-14's own report states it is "**not** proposed for
landing". Land **one** of the two: applying both is a no-op second apply that
fails closed (`search text not found verbatim`) under either applier.
