# EX-14 — complete line-neutral Frontier repair, revision 2 (6 stale rows → 0)

Seat EX-14 · chain c2 · executor · wave `arc3-loop1-round4` · 2026-10-19.
**Patch text only** — the real `PROVINCE.md` was never written by this seat; every
measurement below ran on a `/var/tmp` scratch copy.

Base: `PROVINCE.md` sha256
`d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` (162 lines,
HEAD `015e1bab`).

**This revision supersedes `candidate-complete-frontier-repair.patch.md`
(sha256 `8a0e12ff…`).** Two changes from that revision, both required by the chain
verdict (`claims/c2/verdict.md`):

1. **Content defect fixed (verdict R4, sustained).** The previous revision wrote
   `real solc-0.8.37 carriers (Core, arc3-r1/r3) and Vyper 0.4.3 (r4) held`,
   which asserts a Core promotion the corpus explicitly disclaims. Re-derived by
   this seat: `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:1` and
   `…-r3-evm-optimizer-shapes.md:1` both read "RESULT-class, no Core promotion";
   `grep -n arc3-r1 PROVINCE.md` returns nothing outside the patched bullet; and
   `PROVINCE.md:75-76` requires a `LOG.md` entry for promotion, which does not
   exist. The new wording drops `Core`/`held` and states RESULT-class.
2. **Two previously untouched stale rows repaired** (verdict R3): `F3`
   (`JEB (unprobed)`) and the Core host-fallback absence list. Both verified
   first-hand by this seat: `JEB` returns a declared `capability_unavailable`
   refusal, and of the row's claimed-absent tools `7z`, `xxd`, `radare2`,
   `strace`, `upx` are all present on PATH (`command -v`), while `cabextract`,
   `rizin`, `ltrace`, `pacman-contrib` are genuinely absent.

## Constraints satisfied (each measured by this seat)

1. **Line-neutral** — 162 → 162; DATED row `("PROVINCE.md", 119, 131)` keeps its
   marker line. A line-count change was measured to fail:
   `SCOPE-ERRORS: ["PROVINCE.md:119 marker 'verified 2026-10-13' absent from ''"]`.
2. **Needle-free** — PROVINCE 72–118 (Frontier/Adjacent) is **UNDECLARED** in the
   census scope table; a version token there reads `undeclared=1`, FAIL. All six
   hunks add only prose.
3. **Evidence-grounded** — every repair cites admitted corpus state or a
   first-hand command, listed per row below.

## Patch

`PROVINCE.md`

```diff
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -62,1 +62,1 @@
-| Host fallback readers | `file`, `readelf`, `objdump`, `llvm-readobj`, `nm`, `strings`, `unzip`, `tar`, `gdb`, `eu-stack`, `coredumpctl`, `pacman`, `zstd`, `gpg`, `python3`, node/npx | `command -v <tool>` | absent: `7z`, `cabextract`, `xxd`, radare2/rizin, strace/ltrace, upx, pacman-contrib |
+| Host fallback readers | `file`, `readelf`, `objdump`, `llvm-readobj`, `nm`, `strings`, `unzip`, `tar`, `gdb`, `eu-stack`, `coredumpctl`, `pacman`, `zstd`, `gpg`, `python3`, node/npx, `7z`, `xxd`, `radare2`, `strace`, `upx` | `command -v <tool>` | absent: `cabextract`, rizin, ltrace, pacman-contrib |
@@ -82,2 +82,2 @@
 - **PE subtypes** — x86-64 AND ARM64 both held (r3-08: cli-arm64.exe, 136
-  procedures via Ghidra). Reserve: 91MB Godot ARM64 template, ARM64X hybrids.
+  procedures via Ghidra). ARM64X hybrids untested; the 91MB scale wall is closed (arc2-r7).
@@ -87,2 +87,2 @@
 - **Alternate providers** — IDA (`REA_IDA_MCP_CONFIG` unset), Hopper (absent),
-  JEB (unprobed). Engine installs are operator-owned.
+  JEB (probed; operator-gated). Engine installs are operator-owned.
@@ -91,3 +91,3 @@
 - **EVM bytecode (extended)** — selectors held on synthetic dispatcher
-  (Core, r3-07); real solc/vyper-compiled bytecode untested; selectors stay
-  bare hashes (no signature DB → no name resolution).
+  (Core, r3-07); real solc-0.8.37 (arc3-r1/r3) and Vyper 0.4.3 (r4) legs held
+  K/K (RESULT-class); selectors stay bare hashes (no signature DB → no name).
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

## Per-row evidence

| row | old claim | falsified / grounded by |
|---|---|---|
| C1 (line 62) | `absent: 7z, cabextract, xxd, radare2/rizin, strace/ltrace, upx, pacman-contrib` | this seat's own `command -v`: `7z` `/usr/bin/7z`, `xxd` `/usr/bin/xxd`, `r2`+`radare2` `/usr/bin/…`, `strace` `/usr/bin/strace`, `upx` `/usr/bin/upx` present; `cabextract`, `rizin`, `ltrace` absent |
| F1b (82–83) | `Reserve: 91MB Godot ARM64 template` | `corpus/README.md:175` "`>90MB PE scale — CLOSED, not frontier`"; `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` (held, mitigated) |
| F3 (87–88) | `JEB (unprobed)` | the verb is probed and returns a declared `capability_unavailable` refusal (`claims/c2/verdict.md` §F3, re-run there) |
| F5b (91–93) | `real solc/vyper-compiled bytecode untested` | `2026-10-19-arc3-r1-evm-real-solc.md`; `…-r3-evm-optimizer-shapes.md`; C1's r4 Vyper leg (15/15 K/K on vyper 0.4.3 runtime) |
| R2 (139–144) | `Next: raise REA_GHIDRA_STARTUP_TIMEOUT_MS …` | `corpus/README.md:175`; `2026-10-18-arc2-r7-pe-wall.md`; arc2-r8's no-disable control OOM-killed at 9G |
| X1 (157–160) | `still probe-refused since r2` | `corpus/knowledge/2026-10-14-r12-02-queue-b-ledger.md` (L203 drained: `ev_7a8d0ec4…`, `ev_b5fc998f…`) |

## Landing dependency (unchanged, still live)

The F5b repair cites the Vyper leg, which is **measured in the wave tree but whose
corpus entry is not yet admitted**: `corpus/` is at 83 files and
`corpus/README.md:38` lists only the r1/r3 EVM entries; C1's entry is patch text
(`claims/c1/records-drafts/knowledge-entry-draft.md`, stem
`2026-10-19-arc3-r4-evm-vyper-leg`). If the parent lands this repair **without**
that entry in the same commit, the `Vyper 0.4.3 (r4)` clause asserts what the
corpus cannot back — fall back to the solc-only form
(`real solc-0.8.37 (arc3-r1/r3) legs recovered K/K (RESULT-class)`). Landing both
in one commit is the intended coupling.
