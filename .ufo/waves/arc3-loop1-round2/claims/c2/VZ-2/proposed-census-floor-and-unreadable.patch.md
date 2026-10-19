# FALLBACK patch text (NOT APPLIED) — census H1 absent-file guard + H3 positive floor

Seat VZ-2 (C2 convergence), arc3-loop1-round2, 2026-10-19. **Convergence seat; may
not write `.ufo/gates/`.** Only EX-16 (designated implementer) or the parent may
apply this. Substitute for the round-1 c3 patch texts
(`arc3-loop1-round1/claims/c3/RV-11/proposed-missing-file-guard.patch.md` — H1;
`arc3-loop1-round1/claims/c3/CR-5/proposed-g2-positive-floor.patch.md` — H3),
rebased onto the current revision: `.ufo/gates/c1-census-v10.py`, HEAD `14b1682`,
blob `8fee9422…`, sha256 `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b`,
490 lines (post-E22-disposition). Before-state repro of both holes:
`../before/t1-absent-skill.out`, `../before/t5-blind-instrument.out` (PASS exit 0 each).

## Hunk 1 — H1: absent/unreadable scoped file becomes a declared FAIL class

```diff
@@ -438,10 +438,12 @@
     out, counts, filelines = {}, {}, {}
+    unreadable = []
     for f in files:
         try:
             lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()
-        except OSError:
+        except OSError as ex:
+            unreadable.append("%s: %s" % (f, type(ex).__name__))
             counts[f] = {"lines": 0, "loci": 0}
             filelines[f] = None
             continue
```

```diff
@@ -453,8 +455,8 @@
-    g2_ok = len(out.get("current-ok", [])) > 0 or (not stale and not unatt and not undecl and not unres)
+    g2_ok = len(out.get("current-ok", [])) > 0
     ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \
-         and (not g11) and g2_ok
+         and (not g11) and g2_ok and (not unreadable)
@@ -457,7 +459,7 @@
     if args.json:
         print(json.dumps({"live": live, "counts": counts, "verdict": verdict,
+                          "unreadable": unreadable,
                           "stale": stale, "ambiguous": unatt, "undeclared": undecl,
@@ -480,6 +482,7 @@
     print("\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)
-    print("G2 positive-assertion guard: %s" % ("ok" if g2_ok else "SUSPECT"))
+    if unreadable:
+        print("UNREADABLE (could-not-evaluate): %r" % unreadable)
+    print("G2 positive-assertion guard: %s (current-ok loci=%d, total loci=%d)" %
+          ("ok" if g2_ok else "SUSPECT", len(out.get("current-ok", [])),
+           sum(c["loci"] for c in counts.values())))
```

Hunk 1 in one statement: `g2_ok` loses its vacuous second disjunct (true exactly
when the run finds nothing — the blind-instrument pass, H3), and an unreadable
scoped file is reported and FAILs (H1). Both edits are additive to the report;
the `VERDICT: …` line format is unchanged, so ordinary runs at HEAD still read
`PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)` and the SCOPE table is
untouched (creep audit must show 0 flags).

Expected after-state (VZ-2 battery, runnable by the applier): t0 PASS 0/0/0/0
(counts unchanged); t1 FAIL with `UNREADABLE (could-not-evaluate): ['SKILL.md:
FileNotFoundError']`; t5 blind FAIL (`G2 … SUSPECT`, current-ok loci=0);
t3/t4 unchanged FAIL; t6/t7/t8 unchanged (residuals outside this claim).

## Optional hardening (separate decision; not part of the frozen claim)

An **emptied** scoped file (present, 0 bytes / gate-token-free) still reads
silent PASS (`../before/t2-empty-skill.out`). A floor faithful to
"zero loci in a non-empty scope" at run level does not catch it. If the parent
wants the per-file form: FAIL when a present scoped file whose every declared
row fits within its length yields 0 loci. Deliberately not included above —
scope-bounded change, and the frozen claim names only absent-file + total floor.

## Header note for the applier

The instrument's header (G-history block, lines 73-118) lists the repaired defect
classes G1-G18; a G-history entry for this revision (absent-file class + floor
de-vacuumed) should be added in the same commit, per the round-1 lesson that an
artifact recording its own identity must re-derive it after every revision.
