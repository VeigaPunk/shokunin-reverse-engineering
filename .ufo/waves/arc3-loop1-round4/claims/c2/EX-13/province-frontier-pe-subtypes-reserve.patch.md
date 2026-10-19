# PROVINCE.md repair — Frontier bullet "PE subtypes": the 91MB Godot ARM64 template is no longer an un-run reserve

Authored by SEAT EX-13 (chain c2, executor), wave `arc3-loop1-round4`, 2026-10-19.
**Patch text only** — seats never write `PROVINCE.md`; the parent applies.

## Stale item (census-checked, falsified)

`PROVINCE.md` Frontier bullet `PE subtypes`, current bytes:

> Reserve: 91MB Godot ARM64 template, ARM64X hybrids.

The 91.6 MB Godot ARM64 export template is no longer a *reserve* (a not-yet-run
target): it is the subject of the r7 held run — 75,218 procedures with three
validated analyzers disabled — and of r8's natural control. The admitted corpus
says so in its own words, `corpus/README.md` Frontier list:

> `>90MB PE scale — CLOSED, not frontier: r7's validated analyzer-disable recipe produced a mitigated hold; r8's no-disable control OOM-killed at 9G in 4m42.945s.`

Evidence: `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` (admitted; target
`/home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/windows_release_arm64.exe`,
91,662,336 B, `sha256 7a2ccd68…`, 9 segments / 75,218 procedures);
`corpus/README.md` (the `Frontier` section's `>90MB PE scale` line).
Host re-check: the template path still exists, 91,662,336 B (`ls -la`).

The `ARM64X hybrids` reserve is untouched and still correct (`corpus/knowledge/2026-10-13-r3-pe-arm64.md` names it as the un-run reserve).

## Change (same-line replacement, line count held at 2)

`PROVINCE.md`

```diff
# file: PROVINCE.md
-- **PE subtypes** — x86-64 AND ARM64 both held (r3-08: cli-arm64.exe, 136
-  procedures via Ghidra). Reserve: 91MB Godot ARM64 template, ARM64X hybrids.
+- **PE subtypes** — x86-64 AND ARM64 both held (r3-08: cli-arm64.exe, 136
+  procedures via Ghidra); 91MB Godot ARM64 template held mitigated (r7). Reserve: ARM64X hybrids.
```

## Census conformance

- Line-neutral: 2 search lines → 2 replacement lines; `PROVINCE.md` stays at
  162 lines, so the DATED marker at line 119 (`verified 2026-10-13`) does not
  shift (EX-14's arm 8 measured the line-count-change failure mode).
- Needle-free: the replacement introduces no `rea-agents@x.y.z`, no bare
  `6.x.y`, no `~`/`/`-absolute `path:line` — the Frontier section (72–118) is
  **UNDECLARED** in the census scope, and a needle there reads
  `FAIL (undeclared=1)` (EX-14's arm 3).
- Search text is verbatim and unique in `PROVINCE.md` (verified by the
  apply-and-census run recorded in `claims/c2/EX-13/evidence/`).
