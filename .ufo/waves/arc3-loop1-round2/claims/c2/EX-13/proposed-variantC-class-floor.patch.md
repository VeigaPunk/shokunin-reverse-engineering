# Proposed patch text (NOT APPLIED) — variant C: class-restricted per-file floor

Seat EX-13 (executor, chain c2), arc3-loop1-round2, 2026-10-19. **Patch text only** —
EX-16 owns the real target (`.ufo/gates/c1-census-v10.py`); this seat wrote no target.

- Base (before-state): `df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43`
  (R4, the live revision at 09:11:50–09:15:02), pinned as `tools/census-landed-r4.py`.
- After-state of this proposal: `tools/census-r4-variantC.py` (full file, for review);
  diff below is exactly `diff -u` between the two, only the two hunks shown.
- Motivation/measurements: [`r4-recheck.md`](r4-recheck.md) — residual F4.

## Diff

```diff
@@ -553,7 +553,21 @@
             for d in rec["asserts"]:
                 if d["disp"] == "current-ok":
                     floor[rec["file"]] += 1
-    h3_ok = all(floor[f] > 0 for f in files if filelines[f] is not None)
+    # variant C (EX-13): additionally, every readable file with declared CURRENT rows
+    # must contribute >= 1 current-ok assertion whose own scope is CURRENT.
+    files_with_current = {s[0] for s in SCOPE if s[3] == "CURRENT"}
+    cur_floor = {f: 0 for f in files}
+    for recs in out.values():
+        if not isinstance(recs, list):
+            continue
+        for rec in recs:
+            if not isinstance(rec, dict):
+                continue
+            for d in rec["asserts"]:
+                if d["disp"] == "current-ok" and d["scope"] == "CURRENT":
+                    cur_floor[rec["file"]] += 1
+    h3_ok = all(floor[f] > 0 for f in files if filelines[f] is not None) and \
+        all(cur_floor[f] > 0 for f in files_with_current if filelines[f] is not None)
     g2_ok = h3_ok
     declared = (["UNREADABLE"] if unreadable else []) + ([] if g2_ok else ["BLIND-INSTRUMENT"])
     ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \
@@ -586,9 +600,10 @@
                           (d["line"], d["kind"], d["client"], d["value"], d["disp"], d["why"]))
     print("\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)
     print("UNREADABLE (could-not-evaluate): %r" % unreadable)
-    print("G2 positive-assertion guard: %s (current-ok loci per file: %s; total loci=%d; floor=1/file)"
+    print("G2 positive-assertion guard: %s (current-ok per file: %s; CURRENT-class per file: %s; total loci=%d; floor=1/file+CURRENT)"
           % ("ok" if g2_ok else "SUSPECT",
-             ", ".join("%s=%d" % (f, floor[f]) for f in files), n_loci))
+             ", ".join("%s=%d" % (f, floor[f]) for f in files),
+             ", ".join("%s=%d" % (f, cur_floor[f]) for f in files), n_loci))
     print("G7 configured!=held warnings: %r" % g7)
     print("G11 current-ok without receipt language: %r" % g11)
     print("DECLARED FAIL CLASSES: %r" % declared)
```

Semantics: a readable file that declares CURRENT rows must expose at least one
`current-ok` assertion whose *own* scope is CURRENT. Det counts include assertions that
sit inside `info` (mixed) blocks — that is where SCORECARD.md's CURRENT-class dets live,
so a block-disposition filter would false-FAIL the ordinary run.

## Measured (receipts in `receipts-r4/`; not asserted)

| root | R4 | variant C |
|---|---|---|
| ordinary HEAD | PASS, per-file 17/14/3 | PASS, CURRENT-class 15/4/3 |
| F1 all CURRENT rows blanked | FAIL (`SKILL.md=0`) | FAIL (0/0/0) |
| F2 all declared rows blanked | FAIL (`SKILL.md=0`) | FAIL (0/0/0) |
| **F4 only SCORECARD.md CURRENT row blanked** | **PASS (residual)** | **FAIL (SCORECARD.md=0)** |
| SKILL.md absent | FAIL `UNREADABLE`, no spurious class | same |
| no scoped files | FAIL `UNREADABLE`, no spurious class | same |

## Caveat (this seat's own refutation attempt)

C's tightest margin at HEAD is SCORECARD.md's 4 CURRENT-class dets, all from the single
declared CURRENT block 56-60; a later legitimate rewrite of that block to needle-free
prose would false-FAIL C. EX-14's map already refutes per-row and per-CURRENT-row floors
(`seats/EX-14.md` rows D/E) — C is per-file, not per-row, but the risk is of the same
kind at smaller scale. Recommended disposition: either land C this round, or keep R4 and
name the residual in the records (receipt `receipts-r4/r4-f4.out`).
