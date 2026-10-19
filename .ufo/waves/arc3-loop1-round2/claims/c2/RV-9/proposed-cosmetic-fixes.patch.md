# Proposed patch text (NOT applied) — RV-9 cosmetic fixes to the landed census

Seat RV-9 (reviewer, chain c2), arc3-loop1-round2, 2026-10-19. **Patch TEXT only.**
The reviewer seat may not write `.ufo/gates/`; EX-16 owns that target. Anchored on
the landed bytes sha256 `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`
(610 lines, mtime 2026-10-19 09:15:39 -0300). Both hunks are cosmetic; neither
changes a verdict. If landed, the queue-drain rule-#14 discipline applies: re-derive
the instrument identity, re-run the ordinary verdict, and record the fresh stdout
digest (the second hunk changes the G2 report line, so the current stdout digest
`1db2ec31…` would be superseded — expect a new digest, same verdict `PASS 0/0/0/0`).

## F1 — duplicated docstring paragraph (measured: the identical 3-line paragraph appears twice)

```
$ grep -c "Still named, NOT closed here" .ufo/gates/c1-census-v10.py
2
$ grep -n "Still named, NOT closed here" .ufo/gates/c1-census-v10.py
82:   - Still named, NOT closed here (no silent widening): H2 same-line inline-
85:   - Still named, NOT closed here (no silent widening): H2 same-line inline-
```

The lines 82-84 and 85-87 are byte-identical. Delete one copy (either; the file
content after the deletion is the same).

## F2 — unit label inside the G2 report line (per-file numbers are detections, not loci)

Measured on the ordinary run: the per-file numbers sum to 34 (`PROVINCE.md=17,
SCORECARD.md=14, SKILL.md=3`) while `total loci=17` (`loci` lines: 6/9/2) — the
same printed line uses the word "loci" for two different units.

```diff
--- .ufo/gates/c1-census-v10.py
+++ .ufo/gates/c1-census-v10.py
@@ -598,1 +598,1 @@
-    print("G2 positive-assertion guard: %s (current-ok loci per file: %s; total loci=%d; floor=1/file)"
+    print("G2 positive-assertion guard: %s (current-ok dets per file: %s; total loci=%d; floor=1/file)"
```

Optional companion wording (docstring, same unit confusion at :67):

```diff
-     PER-READABLE-FILE positive floor: >= 1 current-ok locus per scoped file
+     PER-READABLE-FILE positive floor: >= 1 current-ok detection per scoped file
```

If the parent prefers zero output churn at landing, F2 can be deferred to the next
instrument touch: the floor semantics are correct and the numbers are auditable
(the per-file counts are exactly the `-> current-ok` detections in the printed
buckets, verified by counting the report text independently).
