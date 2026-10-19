# PROVINCE.md repair — Round-4 frontier bullet ">90 MB PE scale wall": the wall fell (r7 held, r8 control)

Authored by SEAT EX-13 (chain c2, executor), wave `arc3-loop1-round4`, 2026-10-19.
**Patch text only** — seats never write `PROVINCE.md`; the parent applies.

## Stale item (census-checked, falsified)

`PROVINCE.md` `### Round-4 frontier (post-unlock)` bullet `>90 MB PE scale wall`,
current bytes:

> 91.6 MB Godot ARM64 PE hits REA's ~900s internal session deadline
> (`provider_timeout`, GhidraClient.js:607), still progressing at kill (r4-12)
> [r5-audit C1: r4-12 cite added]. Not OOM (RSS ~2.36GB vs -Xmx2G headroom
> exists). Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` to ~3.6Ms +
> `GHIDRA_HEADLESS_MAXMEM=6-8G` on an idle host, or bisect with a 2-5MB PE.

This is **closed**, not frontier — by the admitted corpus's own words,
`corpus/README.md`:

> `>90MB PE scale — CLOSED, not frontier: r7's validated analyzer-disable recipe produced a mitigated hold; r8's no-disable control OOM-killed at 9G in 4m42.945s. No natural hold at this cap; rerun id-stability remains unknown.`

and `corpus/README.md`'s scale-ladder row (naming `2026-10-18-arc2-r6-pe-midrung`
and `2026-10-18-arc2-r7-pe-wall`):

> wall-fell — r7: the 91.6MB Godot ARM64 PE HELD with three validated analyzers
> disabled; r8: the same-target natural control (no disables; same cap/deadline/
> heap) OOM-killed at 9G, proving the disable necessary.

Evidence: `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` — user service
`arc2-r7-pe`, exit 0, `Result=success`, wall 1424.663 s (vs the 7200 s raised
deadline, unused), 9 segments / **75,218 procedures**, `ev_a4aa9b0d…`,
`analyzer_preset: "ghidra-default+disabled:Call Convention ID,Decompiler
Parameter ID,Decompiler Switch Analysis"`; plus the append-only r8 natural
control (same target, no disables, identical caps → kernel OOM at 9G in
4m42.945s).

The bullet's own "Next:" list is therefore spent — `REA_GHIDRA_STARTUP_TIMEOUT_MS`
was raised and the disable recipe validated. The one genuinely open residual is
rerun id-stability (recorded as such in the r7 entry's erratum and in
`corpus/README.md`).

## Change (same-line replacement, line count held at 6)

`PROVINCE.md`

```diff
# file: PROVINCE.md
-- **>90 MB PE scale wall** — 91.6 MB Godot ARM64 PE hits REA's ~900s internal
-  session deadline (`provider_timeout`, GhidraClient.js:607), still progressing
-  at kill (r4-12) [r5-audit C1: r4-12 cite added]. Not OOM (RSS ~2.36GB vs
-  -Xmx2G headroom exists). Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` to
-  ~3.6Ms + `GHIDRA_HEADLESS_MAXMEM=6-8G` on an idle host, or bisect with a
-  2-5MB PE.
+- **>90 MB PE scale wall — CLOSED** (r7 held: 91.6 MB Godot ARM64 PE, 75,218
+  procedures, exit 0, analyzer-disable recipe validated; r8 same-target
+  no-disable control OOM-killed at 9G in 4m42.945s — no natural hold at this
+  cap). Supersedes the r4-12 `provider_timeout` reading. Residual: rerun
+  id-stability (r7 erratum). Not OOM (RSS ~2.36GB vs -Xmx2G headroom exists).
+  [r5-audit C1: r4-12 cite added].
```

## Census conformance

- Line-neutral: 6 → 6 lines; `PROVINCE.md` stays at 162 lines. This bullet sits
  at 139–144, **below** the DATED row `("PROVINCE.md", 119, 131)` whose marker
  is asserted at line 119 — a line-count change anywhere above 119 would raise
  `SCOPE-ERRORS` (EX-14's arm 8). Holding the count removes that class
  entirely.
- Needle-free: no `rea-agents@x.y.z`, no bare `6.x.y`, no `~`/`/`-absolute
  `path:line`. This block (133–162) is **UNDECLARED** in the census scope, so a
  needle here reads `FAIL (undeclared=1)`. Note `GhidraClient.js:607` is a bare
  `name.js:N` form, not the census's `~`/`/`-absolute pointer regex — but the
  replacement drops it anyway (it is superseded evidence, and the r4-12 cite is
  retained).
- The `[r5-audit C1: r4-12 cite added]` annotation is preserved so the audit
  trail is not lost.

## Note for the parent

This repair *removes* a Frontier bullet by promoting it to a closed state,
while keeping the bullet in place (line-neutral) rather than deleting it —
deleting would shift every line below 144 and is not available to a same-line
patch. If the parent prefers the bullet physically moved into the "Round-4
additions to Core" table, that is a structural edit outside a patch text's
line-neutral contract; flag it as a follow-up rather than folding it here.
