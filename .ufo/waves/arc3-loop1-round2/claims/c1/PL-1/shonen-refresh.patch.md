# Proposed SHONEN.md change — craft-section range + rule count (PATCH TEXT, NOT APPLIED)

Seat PL-1 (planner, chain c1), wave `arc3-loop1-round2`, 2026-10-19. Target:
`SHONEN.md:6`. Companion to `rule-14.patch.md` — **must land in the same commit**,
otherwise SHONEN keeps a stale self-referential count (`13/13`) after the craft
section grows to 14 rules — the exact defect class rule #14 names. Not applied
by this seat (`SHONEN.md` is barred to seats this round).

## Patch (unified diff)

```diff
@@ -3,7 +3,7 @@
 Promotion to shokunin requires all of:
 
 - [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
-  asserted: `SKILL.md:81-243` (craft section; rules #11-13 added arc2 rounds 4/7/9); 13/13 rule blocks have resolvable citations, not a full semantic audit — `SCORECARD.md`, command A; no identified outside verifier.
+  asserted: `SKILL.md:81-265` (craft section; rules #11-13 added arc2 rounds 4/7/9, rule #14 added arc3-loop1-round2); 14/14 rule blocks have resolvable citations, not a full semantic audit — `SCORECARD.md`, command A; no identified outside verifier.
```

Full diff also at `shonen-refresh.diff`.

## Range arithmetic and needle check (measured)

- The rule #14 insertion adds 24 lines above the craft section's tail, so the
  range's end moves `243 + 22 = 265` (the original range ended one line past the
  `## Config custody` heading; the heading moves `242 → 264`). The refreshed
  range `81-265` preserves that convention and stays inside the file (395 lines).
- The pointer-table entry `shonen-skill-range` extracts the range from
  `SHONEN.md:6` and requires its needle (`A mitigation claim carries its natural
  control`, rule #13's lead) to sit inside the stated range — "this needle fails
  if a later append pushes that rule past the stated end". Measured after the
  refresh: needle hits **1** inside `SKILL.md:81-265`; probe verdict stays
  `reported findings=0 exit=0` (default) and `clean findings=0 exit=0` (`--strict`).
- Recompute both numbers at the wave's HEAD before landing (the insertion anchor
  or a rival craft-section edit can move them); do not copy these values blind.
