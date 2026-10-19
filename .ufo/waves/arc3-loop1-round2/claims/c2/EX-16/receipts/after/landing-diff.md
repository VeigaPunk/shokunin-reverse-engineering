# EX-16 landing diff — .ufo/gates/c1-census-v10.py (arc3-loop1-round2 r9: H1+H3 fail-closures)

before sha256: 6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b (490 lines)
after  sha256: d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5 (610 lines)
SCOPE table: byte-identical (scope-diff.py rows before=20 after=20, ADDED/REMOVED/CHANGED 0, CREEP FLAGS [])

```diff
--- /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round2/claims/c2/EX-16/tools/census-before.py	2026-10-19 09:03:57.243568428 -0300
+++ /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/c1-census-v10.py	2026-10-19 09:18:14.791363447 -0300
@@ -42,9 +42,59 @@
   past the declared bound must be locus-free in this instrument's unit — no
   `rea-agents@x.y.z`, no bare `6.x.y`, no `~`- or `/`-absolute `path:line` —
   or the bound must be re-keyed in the same commit as a DATED row whose marker
-  line carries that section's own date/round token."""
+  line carries that section's own date/round token.
+
+ARC3-LOOP1-ROUND2 r9 — H1+H3 FAIL-CLOSURES (2026-10-19, EX-16, C2's real-path
+write; instrument sha256 before this edit 6f1d19ff…). Two round-1 latent holes
+close as declared FAIL classes, merged from the round-1 patch texts RV-11/H1
+(proposed-missing-file-guard) and CR-5/H3 (proposed-g2-positive-floor). Scope
+bounds are UNCHANGED (creep audit: scope-diff.py 0 flags).
+
+   - UNREADABLE (H1 class). A scoped file that cannot be read was absorbed as
+     `lines=0 loci=0`; with all its declared rows CURRENT no marker assertion
+     fired and the run read PASS exit 0. Re-measured before (claims/c2/EX-16/
+     receipts/before/): SKILL.md absent -> PASS exit 0; and the same silent
+     class for zero-byte, truncated (rows beyond EOF), is-a-directory and
+     EACCES roots. Now: any scoped file that is unreadable (OSError) OR holds
+     fewer lines than its declared max end is a declared could-not-evaluate
+     class -- reported (`UNREADABLE (could-not-evaluate): [...]`, counts read
+     `lines=None`), carried in --json, and fails the verdict (exit 1) whatever
+     the row classes are. DATED-bearing files keep their existing
+     "marker uncheckable" SCOPE-ERRORs as well.
+   - BLIND-INSTRUMENT (H3 class). `g2_ok`'s old second disjunct was true
+     exactly when the run found nothing, so needles neutered -> loci=0 read
+     PASS exit 0 (re-measured: h3-blind-all / h3-blind-gate). G2 is now a
+     PER-READABLE-FILE positive floor: >= 1 current-ok locus per scoped file
+     the run could read (EX-14's variant B, measured to dominate the global
+     variant A on head/blind/nullskill -- the global floor still swallows a
+     per-file collapse such as a needle-stripped or blanked SKILL.md while
+     the other two files stay loud). Per-ROW floors are refuted by EX-14's
+     occupancy map: 4 DATED rows are zero-locus by design at HEAD. A
+     violating run is declared (`DECLARED FAIL CLASSES:
+     ['BLIND-INSTRUMENT']`) in text and --json, exit 1; the G2 report line
+     carries the per-file substrate so the number is auditable. Unreadable
+     files are exempt from the floor (they are the H1 class and already force
+     FAIL). Residual, named: per-needle PARTIAL blindness (e.g. PIN alone
+     neutered) keeps each file's current-ok count above zero and still reads
+     PASS -- a token floor is not a coverage floor (EX-14 §5); only the
+     external locus/assertion-count + scope-diff audit sees it, and that
+     audit remains the certificate for any instrument touch.
+   - Still named, NOT closed here (no silent widening): H2 same-line inline-
+     marker excusal; t5 DATED-shelter for historical-looking non-live values;
+     H4 self-certification (covered externally, see above).
+   - Still named, NOT closed here (no silent widening): H2 same-line inline-
+     marker excusal; t5 DATED-shelter for historical-looking non-live values;
+     H4 self-certification (covered externally, see above).
+
+  Post-edit identity is recorded in the landing receipt (claims/c2/EX-16/
+  receipts/after/after-sha256.txt + landing-diff.md), NOT inline: an artifact
+  that records its own byte-identity must re-derive it after every revision,
+  so a hash written into the file it hashes would be stale by construction
+  (the queue-drain rule-#14 discipline)."""
 #!/usr/bin/env python3
-"""C1 stale-statement census instrument v9 (E22, arc2-loop1-round2) — FINAL.
+"""C1 census instrument v10-r9 (arc3-loop1-round2: H1+H3 fail-closures; the
+v9-era structure and claim text below are retained as the instrument's history,
+not as a current self-description — see the r9 provenance block at the top).
 
 Claim under test (C1): after the round's commit, every current-surface
 version/pin statement in PROVINCE.md / SKILL.md / SCORECARD.md states a
@@ -116,11 +166,37 @@
                                            range -- the stale-row class EX-28
                                            found at HEAD, PROVINCE.md 45-62
                                            naming :40; now a SCOPE-ERROR)
+  G19 unreadable/undeclarable scoped file (r9, H1): an absent/zero-byte/
+                                           truncated/EACCES/directory scoped
+                                           file was absorbed as lines=0 loci=0
+                                           and, when its rows were all
+                                           CURRENT, read PASS exit 0; now a
+                                           declared UNREADABLE fail class
+                                           (rows beyond the declared max end
+                                           count as truncated too)
+  G20 positive floor, not vacuous         (r9, H3): G2's second disjunct was
+                                           true exactly when the run found
+                                           nothing, so a blind instrument read
+                                           PASS.  The floor is PER READABLE
+                                           FILE OVER CURRENT-OK DETECTIONS.
+                                           The unit is load-bearing knowledge:
+                                           refuted at HEAD are (a) per-SCOPE-
+                                           row floors (4 DATED rows are
+                                           zero-locus by design, EX-14's map)
+                                           and (b) per-file BLOCK floors
+                                           (SKILL.md has 0 current-ok blocks
+                                           but 3 current-ok dets; CR-2's
+                                           false-FAIL episode, CR-3's unit
+                                           table).  Do not re-key the unit
+                                           without re-running the HEAD
+                                           invariance check.)
 
 Verdict: PASS iff stale == 0 AND ambiguous == 0 AND undeclared == 0
-AND unresolved == 0 AND scope_errors == 0 AND g11 == [] AND G2 holds.
+AND unresolved == 0 AND scope_errors == 0 AND g11 == [] AND G2 holds
+(>= 1 current-ok DETECTION per readable scoped file, r9 floor) AND no
+unevaluable scoped file.
 Exit 0 PASS, 1 FAIL, 2 anchor failure.
-Usage: python3 c1-census-v9.py [--root DIR] [--json] [--quiet]
+Usage: python3 c1-census-v10.py [--root DIR] [--json] [--quiet]
 """
 import argparse, json, os, re, sys
 
@@ -435,12 +511,21 @@
     if not all(live.values()):
         print("ANCHOR-FAIL: %r" % live)
         return 2
-    out, counts, filelines = {}, {}, {}
+    out, counts, filelines, unreadable = {}, {}, {}, []
     for f in files:
+        max_end = max((s[2] for s in SCOPE if s[0] == f), default=0)
         try:
             lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()
-        except OSError:
-            counts[f] = {"lines": 0, "loci": 0}
+        except OSError as ex:
+            unreadable.append("%s: %s" % (f, type(ex).__name__))
+            counts[f] = {"lines": None, "loci": None}
+            filelines[f] = None
+            continue
+        if len(lines) < max_end:
+            # G19: declared rows past EOF are unevaluable, never a silent zero.
+            unreadable.append("%s: %d lines < declared max %d (rows beyond EOF)"
+                              % (f, len(lines), max_end))
+            counts[f] = {"lines": None, "loci": None}
             filelines[f] = None
             continue
         filelines[f] = lines
@@ -450,21 +535,52 @@
     undecl = out.get("UNDECLARED", [])
     unres = out.get("UNRESOLVED", [])
     g11, g7 = out.get("g11", []), out.get("g7", [])
-    g2_ok = len(out.get("current-ok", [])) > 0 or (not stale and not unatt and not undecl and not unres)
+    # G20 (r9, H3): the old second disjunct was true exactly when the run found
+    # nothing, so a blind instrument read PASS.  The floor is PER READABLE FILE
+    # over current-ok DETECTIONS (EX-14's variant B, measured to dominate the
+    # global variant A on head/blind/nullskill): every scoped file the run
+    # could read must contribute >= 1 current-ok assertion, so a per-file
+    # collapse (needles stripped, content blanked) is declared even when other
+    # files stay loud.  Dets are counted, not blocks: SKILL.md's only
+    # locus-bearing block is mixed (current-ok + historical) and carries block
+    # disposition "info", so a block-count floor false-FAILs the ordinary run
+    # (measured; EX-14's §6 snippet as written reproduces that false FAIL).
+    # Unreadable files are exempt here -- they are the H1 class and already
+    # force FAIL via `unreadable`.  Per-ROW floors are refuted by EX-14's map
+    # (4 DATED rows are zero-locus by design at HEAD).
+    n_loci = sum((c["loci"] or 0) for c in counts.values())
+    n_current_ok = sum(1 for recs in out.values() if isinstance(recs, list)
+                       for rec in recs if isinstance(rec, dict)
+                       for d in rec["asserts"] if d["disp"] == "current-ok")
+    floor = {f: 0 for f in files}
+    for recs in out.values():
+        if not isinstance(recs, list):
+            continue
+        for rec in recs:
+            if not isinstance(rec, dict):
+                continue
+            for d in rec["asserts"]:
+                if d["disp"] == "current-ok":
+                    floor[rec["file"]] += 1
+    h3_ok = all(floor[f] > 0 for f in files if filelines[f] is not None)
+    g2_ok = h3_ok
+    declared = (["UNREADABLE"] if unreadable else []) + ([] if g2_ok else ["BLIND-INSTRUMENT"])
     ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \
-         and (not g11) and g2_ok
+         and (not g11) and g2_ok and (not unreadable)
     verdict = "PASS" if ok else "FAIL"
     if args.json:
         print(json.dumps({"live": live, "counts": counts, "verdict": verdict,
                           "stale": stale, "ambiguous": unatt, "undeclared": undecl,
                           "unresolved": unres, "scope_errors": scope_errors,
-                          "g11": g11, "g7": g7, "g2_ok": g2_ok,
+                          "unreadable": unreadable, "declared_fail_classes": declared,
+                          "g2_ok": g2_ok, "g2_floor": "1/readable-file", "current_ok_per_file": floor,
+                          "g11": g11, "g7": g7,
                           "historical": out.get("historical", []),
                           "current_ok": out.get("current-ok", [])}, indent=1))
         return 0 if verdict == "PASS" else 1
     print("live anchors (re-derived): %r" % live)
     for f, c in counts.items():
-        print("%-14s lines=%-4d loci=%s" % (f, c["lines"], c["loci"]))
+        print("%-14s lines=%-4s loci=%s" % (f, c["lines"], c["loci"]))
     if not args.quiet:
         for k in ("STALE", "AMBIGUOUS", "UNDECLARED", "UNRESOLVED",
                   "historical", "current-ok", "info"):
@@ -478,9 +594,13 @@
                     print("      :%d [%s] %s=%s -> %s (%s)" %
                           (d["line"], d["kind"], d["client"], d["value"], d["disp"], d["why"]))
     print("\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)
-    print("G2 positive-assertion guard: %s" % ("ok" if g2_ok else "SUSPECT"))
+    print("UNREADABLE (could-not-evaluate): %r" % unreadable)
+    print("G2 positive-assertion guard: %s (current-ok loci per file: %s; total loci=%d; floor=1/file)"
+          % ("ok" if g2_ok else "SUSPECT",
+             ", ".join("%s=%d" % (f, floor[f]) for f in files), n_loci))
     print("G7 configured!=held warnings: %r" % g7)
     print("G11 current-ok without receipt language: %r" % g11)
+    print("DECLARED FAIL CLASSES: %r" % declared)
     print("VERDICT: %s  (stale=%d ambiguous=%d undeclared=%d unresolved=%d)"
           % (verdict, len(stale), len(unatt), len(undecl), len(unres)))
     return 0 if verdict == "PASS" else 1
```
