# frontier-repair-C — PROVINCE.md Round-4 frontier bullet R2: the >90 MB PE scale wall (1 hunk, line-neutral)

Authored by SEAT EX-11 (chain c2, executor), wave `arc3-loop1-round4`. **Patch text
only** — the parent applies it; seats never write PROVINCE.

Measured against revision `015e1bab914713568f339fd53999bc180459cc40` at write time:
`PROVINCE.md` sha256 `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad`,
162 lines. Line-neutral, needle-free.

## The staleness (measured)

The bullet reads as an OPEN wall with a "Next:" plan. Later measurements close it,
and the lane's own README already says so:

- `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` — the wall FALLS at arc2 r7:
  9 segments / 75,218 procedures, sealed `ev_a4aa9b0d…`, 1424.663 s wall, peak
  7.9 G under a 9 G cap, zero decompile workers; the analyzer-disable recipe is
  the mechanism. The target is byte-identical to the one this bullet cites
  (`windows_release_arm64.exe`, sha256 `7a2ccd68…`).
- Same entry, r8 erratum — the identical target with NO disables was
  kernel-OOM-killed at 9 G in 4m42.945s: "no natural hold exists at this cap".
- `corpus/README.md:175` — "`>90MB PE scale — CLOSED, not frontier`".
- `LOG.md:1363` — rerun id-stability closed at arc2 r10 ("id STABLE at 91.6MB").

The bullet's own "Next:" advice is superseded: r7's hold used a 7200 s deadline it
did not need (1424 s used), with the *disable* doing the work. Leaving the advice
in place would send the next seat at a solved wall with a stale lever.

## Hunk

### Hunk 1

Target file: `PROVINCE.md`

```diff
# file: PROVINCE.md
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -139,6 +139,6 @@
-- **>90 MB PE scale wall** — 91.6 MB Godot ARM64 PE hits REA's ~900s internal
-  session deadline (`provider_timeout`, GhidraClient.js:607), still progressing
-  at kill (r4-12) [r5-audit C1: r4-12 cite added]. Not OOM (RSS ~2.36GB vs
-  -Xmx2G headroom exists). Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` to
-  ~3.6Ms + `GHIDRA_HEADLESS_MAXMEM=6-8G` on an idle host, or bisect with a
-  2-5MB PE.
+- **>90 MB PE scale wall** — HELD at arc2 r7: 75,218 procs, 1424s, 9G cap,
+  analyzer-disable recipe (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md`).
+  r8 natural control OOM-killed at 9G in 4m42.945s — disable necessary. The
+  r4-12 deadline kill (`provider_timeout`, GhidraClient.js:607) is superseded;
+  rerun id-stability closed at r10 (byte-identical). Residual: the disable is
+  caller-arranged, not a plain-cap hold.
```

## The residual this repair keeps (honesty note)

r7's run used `analyzer_preset: "ghidra-default+disabled:…"` — a caller-arranged
mitigation, not a plain-cap hold, and the r8 control shows the disable is
*necessary* at 9 G. "REA analyzes 91.6 MB PE unattended" would therefore be an
over-claim; the repaired text says HELD and names the recipe.
