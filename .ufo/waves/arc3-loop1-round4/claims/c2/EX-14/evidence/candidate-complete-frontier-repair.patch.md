# EX-14 — complete line-neutral Frontier repair candidate (4 stale rows → 0)

Seat EX-14 · chain c2 · executor · wave `arc3-loop1-round4` · 2026-10-19.
**Patch text only** — the real `PROVINCE.md` was never written by this seat; every
measurement below ran on a `/var/tmp` scratch copy.

Base: `PROVINCE.md` sha256
`d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` (162 lines,
HEAD `015e1bab`).

## Why this patch exists

The chain's own staleness census (seat VZ-2,
`claims/c2/VZ-2/evidence/province-staleness-census.py`, run by this seat) reads
`SUMMARY: total=24 stale=4 adjudicated=1 current=19` — `STALE: F1b, F5b, X1, R2`.
The frozen C2 claim requires the stale count to reach **0**, and the census gate
(`.ufo/gates/c1-census-v10.py`) to read PASS on the repaired tree. This patch
does both, and holds the line count at 162 so the DATED row `119-131` keeps its
marker line.

## Constraints this patch satisfies (each measured by this seat)

1. **Line-neutral** — 162 → 162. A line-count change shifts the marker line of
   DATED row `("PROVINCE.md", 119, 131)`: measured `SCOPE-ERRORS:
   ["PROVINCE.md:119 marker 'verified 2026-10-13' absent from ''"]`, FAIL exit 1.
2. **Needle-free** — PROVINCE 72–118 (Frontier/Adjacent) is **UNDECLARED** in the
   census scope table; any version token there reads `undeclared=1`, FAIL. Every
   added line here parses `pin=[] ver=[] ptr=[]` under the census's own regexes.
3. **Evidence-grounded** — each repair cites the admitted corpus entry that
   falsifies the old text (paths named in §"Evidence" below).

## Evidence for each repair

| row | old claim | falsified by (admitted corpus state) |
|---|---|---|
| F1b | "Reserve: 91MB Godot ARM64 template" | `corpus/README.md:175` ("`>90MB PE scale — CLOSED, not frontier`"); `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` (91.6MB held, mitigated) |
| F5b | "real solc/vyper-compiled bytecode untested" | `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` (real solc-0.8.37 K/K); `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md` (optimizer on/off) |
| X1 | "`compare-application-versions` still probe-refused since r2" | `corpus/knowledge/2026-10-14-r12-02-queue-b-ledger.md` (L203 drained: `ev_7a8d0ec4…` JS + `ev_b5fc998f…` managed success legs) |
| R2 | "Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` …" | `corpus/README.md:175`; `2026-10-18-arc2-r7-pe-wall.md` (validated analyzer-disable recipe); r8's no-disable control OOM-killed at 9G |

## Patch

`PROVINCE.md`

```diff
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -82,2 +82,2 @@
 - **PE subtypes** — x86-64 AND ARM64 both held (r3-08: cli-arm64.exe, 136
-  procedures via Ghidra). Reserve: 91MB Godot ARM64 template, ARM64X hybrids.
+  procedures via Ghidra). ARM64X hybrids untested; the 91MB scale wall is closed (arc2-r7).
@@ -91,3 +91,3 @@
 - **EVM bytecode (extended)** — selectors held on synthetic dispatcher
-  (Core, r3-07); real solc/vyper-compiled bytecode untested; selectors stay
-  bare hashes (no signature DB → no name resolution).
+  (Core, r3-07), real solc-0.8.37 carriers (Core, arc3-r1/r3) and Vyper 0.4.3
+  (r4) held; selectors stay bare hashes (no signature DB → no name resolution).
@@ -139,6 +139,6 @@
 - **>90 MB PE scale wall** — 91.6 MB Godot ARM64 PE hits REA's ~900s internal
-  session deadline (`provider_timeout`, GhidraClient.js:607), still progressing
-  at kill (r4-12) [r5-audit C1: r4-12 cite added]. Not OOM (RSS ~2.36GB vs
-  -Xmx2G headroom exists). Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` to
-  ~3.6Ms + `GHIDRA_HEADLESS_MAXMEM=6-8G` on an idle host, or bisect with a
-  2-5MB PE.
+  session deadline (`provider_timeout`, GhidraClient.js:607) at kill (r4-12)
+  [r5-audit C1: r4-12 cite added]; not OOM (RSS ~2.36GB vs -Xmx2G headroom).
+  Held since via the validated analyzer-disable recipe (arc2-r7, mitigated);
+  the no-disable control OOM-killed at 9G (arc2-r8), so this is closed, not
+  frontier — no natural hold at this cap, rerun id-stability unknown.
@@ -157,4 +157,4 @@
 - **Cross-version residuals** — `compare-application-versions` is no longer
-  probe-refused since r2; multi-version pacman pairs beyond expac unexercised
-  [r5-audit C1: merged from the pruned Frontier bullet — its
-  `compare_javascript_export_shapes` item is now held (Core, r4-09)].
+  refused since r2: r12-02 drained the row with two success legs; multi-version
+  pacman pairs beyond expac unexercised [r5-audit C1: merged from the pruned
+  Frontier bullet — its `compare_javascript_export_shapes` item is held now].
```

## Open dependency (named, not hidden)

The `Vyper 0.4.3 (r4)` clause cites a leg that is **measured in the wave tree but
whose corpus entry is not yet admitted**: `corpus/knowledge/` is at 83 files and
`corpus/README.md:38` lists only the r1/r3 EVM entries; SC-1 has staged the entry
as patch text (`claims/c1/records-drafts/knowledge-entry-draft.md`, stem
`2026-10-19-arc3-r4-evm-vyper-leg`). If the parent lands this repair **without**
C1's entry in the same commit, that clause asserts what the corpus cannot back
and should be dropped back to the solc-only form
(`real solc-0.8.37 carriers (Core, arc3-r1/r3) held`). Landing both in one commit
is the intended coupling.
