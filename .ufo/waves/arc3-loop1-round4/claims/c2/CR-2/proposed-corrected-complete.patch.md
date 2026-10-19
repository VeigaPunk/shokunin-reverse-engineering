# CR-2 corrected complete repair (EX-14 v2 hunks 1-5 + corrected hunk 6)

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
-- **Cross-version residuals** — `compare-application-versions` still
-  probe-refused since r2; multi-version pacman pairs beyond expac unexercised
-  [r5-audit C1: merged from the pruned Frontier bullet — its
-  `compare_javascript_export_shapes` item is now held (Core, r4-09)].
+- **Cross-version residuals** — `compare-application-versions` is no longer
+  probe-refused since r2 (r12-02 drained the row with two success legs); multi-version
+  pacman pairs beyond expac unexercised [r5-audit C1: merged from the pruned
+  Frontier bullet — its `compare_javascript_export_shapes` item is held now].
```
