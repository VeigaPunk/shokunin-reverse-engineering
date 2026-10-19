# frontier-repair-B — PROVINCE.md Frontier bullets F5b (EVM) and X1 (cross-version) (2 hunks, line-neutral)

Authored by SEAT EX-11 (chain c2, executor), wave `arc3-loop1-round4`. **Patch text
only** — the parent applies it; seats never write PROVINCE.

Measured against revision `015e1bab914713568f339fd53999bc180459cc40` at write time:
`PROVINCE.md` sha256 `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad`,
162 lines. Line-neutral, needle-free. This file carries the **named debt** of the
frozen claim (`claims-frozen.md:44-46`).

## Evidence for each repair

- **F5b (lines 91-93)** — both halves now stale. solc: the r1 entry
  (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`) recovered K/K on real
  0.8.37 compiles; the r3 entry
  (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md`) extended it to
  optimizer on/off and non-ERC-20 shapes. vyper: this wave's C1 EX-04 compiled a
  real Vyper carrier with vyper 0.4.3 — 15/15 selectors K/K, sealed
  `ev_405e2a2a…`, decoded runtime sha256 `57d6fd0a…`, 6.7.0 re-run `ev_470be5f5…`,
  raw leg `ev_83a6f336…` (`claims/c1/EX-04/evidence/probe/`; planted set K=15
  recorded pre-compile/pre-probe, two independent derivations agreeing,
  `claims/c1/EX-04/evidence/planted-K.json`). The "bare hashes / no signature DB"
  clause stays true and is kept.
- **X1 (lines 157-160)** — "still probe-refused since r2" is stale:
  `corpus/knowledge/2026-10-14-r12-02-queue-b-ledger.md:213` records the success
  path exercised (JS-graph class, obsidian 1.12.7->1.13.7, 10 changed / 208
  unknown over 218 items). Its runtime-reconciliation input class is the residual
  and is kept as open. "multi-version pacman pairs beyond expac unexercised" is
  stale: `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:15` exercised
  cached pacman pairs `1password-cli` 2.34.1->2.40.0 and `qpdf` 12.3.2->12.4.1.

## Hunks

### Hunk 1

Target file: `PROVINCE.md`

```diff
# file: PROVINCE.md
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -91,3 +91,3 @@
-- **EVM bytecode (extended)** — selectors held on synthetic dispatcher
-  (Core, r3-07); real solc/vyper-compiled bytecode untested; selectors stay
-  bare hashes (no signature DB → no name resolution).
+- **EVM bytecode (extended)** — selectors held on synthetic dispatcher
+  (Core, r3-07); real solc/vyper-compiled bytecode tested (arc3-r1/r3; r4
+  vyper 0.4.3); selectors stay bare hashes (no signature DB → no name resolution).
```

### Hunk 2

Target file: `PROVINCE.md`

```diff
# file: PROVINCE.md
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -157,4 +157,4 @@
-- **Cross-version residuals** — `compare-application-versions` still
-  probe-refused since r2; multi-version pacman pairs beyond expac unexercised
-  [r5-audit C1: merged from the pruned Frontier bullet — its
-  `compare_javascript_export_shapes` item is now held (Core, r4-09)].
+- **Cross-version residuals** — `compare-application-versions` exercised
+  (r12-02: JS-graph diff 10 changed / 208 unknown); its runtime-reconciliation
+  input class open; multi-version pacman pairs exercised (r4-10: op, qpdf);
+  `compare_javascript_export_shapes` held (Core, r4-09) [r5-audit C1].
```

## Note on what this patch does NOT claim

The r12-02 ledger names one residual sub-class — the runtime-reconciliation input
class (a held `reconcile_javascript_runtime` Evidence composed as input), untested.
The repair keeps that residual and drops only the refuted "still probe-refused" /
"unexercised" wordings. The r5-audit merge provenance is kept as a trailing tag.
