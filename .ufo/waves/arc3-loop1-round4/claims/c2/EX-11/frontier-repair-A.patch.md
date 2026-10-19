# frontier-repair-A — PROVINCE.md Frontier bullets F1b / F2 / F3 (3 hunks, line-neutral)

Authored by SEAT EX-11 (chain c2, executor), wave `arc3-loop1-round4`. **Patch text
only** — the parent applies it; seats never write PROVINCE.

Measured against revision `015e1bab914713568f339fd53999bc180459cc40` at write time:
`PROVINCE.md` sha256 `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad`,
162 lines. All hunks are line-neutral (162 -> 162) and introduce no census needle
(`rea-agents@x.y.z`, bare `6.x.y`, `~`/`/`-absolute `path:line`) — the Frontier
region is UNDECLARED in the census scope table, so a needle there would read FAIL
undeclared. Each `-` line below is a byte-exact copy of the current file line, so
the chain's appliers land the hunks by content, not by line number.

## Evidence for each repair

- **F1b (lines 82-83)** — the 91MB Godot ARM64 template is no longer a reserve:
  arc2 r7 held the exact target (sha256 `7a2ccd68…`) at 75,218 procedures
  (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md`); `corpus/README.md:175`
  already reads "CLOSED, not frontier". Only ARM64X hybrids remain unexercised.
- **F2 (lines 84-86)** — "all 3 organic cores exceed the cap (waybar 434MB)" is
  falsified live this wave: `core.chrome_crashpad…1857` decompresses to
  17,608,704 B (< the 33,554,432 B cap) and `inspect-recorded-crash` returns RC=0
  with sealed `ev_cde93acb…` (`evidence/crash-probe-crashpad-under-cap.json`).
  The waybar core has decayed out of the store (`ls /var/lib/systemd/coredump |
  grep -c waybar` -> 0). The oversize refusal class still holds and is re-measured
  (`evidence/oversize-refusal-33554432.json`). The "no cap-raising knob" half is
  confirmed by `inspect-recorded-crash --schema` (only `path` + `debuggerContext`)
  and kept.
- **F3 (lines 87-88)** — "JEB (unprobed)" is stale: the r2 provider matrix
  records the live refusal probe
  (`corpus/knowledge/2026-10-13-r2-provider-capability-matrix.md:99`), and
  r12-02's L201 re-verified the gap. Re-checked live this wave: `:8425` closed,
  `REA_JEB_MCP_URL` unset.

## Hunks

### Hunk 1

Target file: `PROVINCE.md`

```diff
# file: PROVINCE.md
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -82,2 +82,2 @@
-- **PE subtypes** — x86-64 AND ARM64 both held (r3-08: cli-arm64.exe, 136
-  procedures via Ghidra). Reserve: 91MB Godot ARM64 template, ARM64X hybrids.
+- **PE subtypes** — x86-64 AND ARM64 both held (r3-08: cli-arm64.exe, 136
+  procedures via Ghidra). 91MB Godot ARM64 template held (arc2-r7); ARM64X reserve.
```

### Hunk 2

Target file: `PROVINCE.md`

```diff
# file: PROVINCE.md
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -84,3 +84,3 @@
-- **Recorded crashes >32 MiB** — mechanism held (Core); all 3 organic cores
-  exceed the cap (waybar 434MB). Needs a cap-raising knob or partial-core
-  intake — neither exists. Retention decays oldest-first.
+- **Recorded crashes >32 MiB** — mechanism held (Core); an organic core
+  under the cap inspects (arc3-r4, 17.6MB); oversize refused typed. Needs
+  a cap knob or partial-core intake — neither exists; retention decays oldest-first.
```

### Hunk 3

Target file: `PROVINCE.md`

```diff
# file: PROVINCE.md
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -87,2 +87,2 @@
-- **Alternate providers** — IDA (`REA_IDA_MCP_CONFIG` unset), Hopper (absent),
-  JEB (unprobed). Engine installs are operator-owned.
+- **Alternate providers** — IDA (`REA_IDA_MCP_CONFIG` unset), Hopper (absent),
+  JEB (refusal-probed, absent). Engine installs are operator-owned.
```

## Why these three, and why not the rest

The census (`frontier-census.md`, this directory) classifies every Frontier
bullet. These are the repairs whose stale half is a **false statement about the
world** that the corpus already contradicts. F5b and X1 are in
`frontier-repair-B.patch.md`; the >90 MB PE wall is in
`frontier-repair-C.patch.md`, so each patch carries one class of change and can be
accepted or rejected on its own. The remaining bullets measured current and are
not touched: a repair without a contradicting measurement is churn.
