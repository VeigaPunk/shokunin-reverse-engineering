# Advisory patch text — census header disposition line (EX-26 → EX-28)

Status: **proposal only, NOT applied**. The write target
`.ufo/gates/c1-census-v10.py` belongs to seat EX-28 (c3) alone; this file is
EX-26's evidence-backed suggestion. Apply, adapt, or discard.

Measured BEFORE at HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`
(`claims/c3/EX-26/census-at-HEAD.txt`, 91 lines, exit 0, sha256
`3b677b8ee47eccb217616eba641fc0b66f72e53634a5ae51a92f8b04e2a22418`):

    VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)

so the E22 debt (`SCORECARD.md:850-852`) is dispositioned as resolved at HEAD
by measurement — no scope row is undeclared or stale, and the undeclared tail
(SCORECARD 856-1336, PROVINCE 132-162, SKILL 21-371) carries no gated locus.

## Hunk 1 — disposition line in the instrument header

Target: `.ufo/gates/c1-census-v10.py`, line 1 (the v10 provenance line).

```diff
-"""C1 census v10 — v9 (sha256 213fe679…) re-keyed per arc2-loop1-round4 Z1 section 4d."""
+"""C1 census v10 — v9 (sha256 213fe679…) re-keyed per arc2-loop1-round4 Z1 section 4d.
+
+E22 disposition (arc3-loop1-round1, EX-26 measurement): run at HEAD e845c2b
+→ PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0), exit 0; verbatim
+verdict at .ufo/waves/arc3-loop1-round1/claims/c3/EX-26/census-at-HEAD.txt.
+No scope row undeclared/stale at HEAD; re-key NOT required. The undeclared
+tail (SCORECARD 856-1336, PROVINCE 132-162, SKILL 21-371) carries no gated
+locus — verified by classify() probe and raw grep (EX-26 report §4.1).
+Residual design property, stated not fixed: SCOPE has no row for the grown
+tail, so a future version/pin statement there trips UNDECLARED (the L1
+intent holds — fail loud, never silent)."""
```

Notes for EX-28:
- If the round's records commit lands further SCORECARD growth, re-run and
  restate the verdict with the new line counts before sealing this header.
- If a scope-row addition is preferred over a header note, the only defensible
  form at HEAD is a row covering SCORECARD 856–1336 as DATED with marker
  `## arc2-loop1-round4` (line 857 is the round-4 header; 856 is blank) —
  but it is not required: the range is currently locus-free.
