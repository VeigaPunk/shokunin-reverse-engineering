# Patch text (NOT applied) — floor-unit specification + one optional hardening

Seat CR-3 (critic, chain c2), arc3-loop1-round2, 2026-10-19. This seat is **not**
the implementer; EX-16 owns `.ufo/gates/c1-census-v10.py`. Nothing here is
applied. Target bytes: `.ufo/gates/c1-census-v10.py` sha256
`df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43`, 601 lines.

## 1. What this patch is for

The H3 floor is now per-file over current-ok **detections** and reads PASS at
HEAD (`receipts/live3-head.out`). That predicate is HEAD-safe and was reached
only after two refuted granularities, one of which was on disk:

| unit | HEAD run | evidence |
|---|---|---|
| SCOPE row, any class | FAIL — 4 DATED rows are zero-locus by design | `receipts/v-row-head.out` |
| per-file, **blocks** | FAIL — `SKILL.md=0` (its current-ok dets sit in a block disposed `info`) | `receipts/live2-head.out` (revision `c95a5cf3…`, 12:10Z) |
| SCOPE row, CURRENT only | PASS | `receipts/v-class-head.out` |
| per-file, any loci | PASS | `receipts/v-file-head.out` |
| per-file, detections (landed) | PASS | `receipts/live3-head.out` |
| corpus, blocks or dets | PASS at HEAD, but blind to a per-file collapse | `receipts/v-global-gut.out` |

So the floor's unit is now load-bearing knowledge, not an implementation detail:
a future editor who "simplifies" the det loop back to a block count, or who
extends the floor to rows, re-introduces a permanent false FAIL on an ordinary
HEAD run — the exact defect class this round exists to close, inverted.

## 2. Text-only change (no behaviour change): name the unit at the floor

```diff
@@ docstring, G20 stanza (after ":180", beside the other G-lines)
   G20 positive floor, not vacuous         (r9, H3): G2's second disjunct was
                                           true exactly when the run found
-                                          nothing, so the floor is per readable
-                                          scoped file (BLIND-INSTRUMENT;
-                                          per-row floors refuted by EX-14's
-                                          map)
+                                          nothing.  The floor is PER READABLE
+                                          FILE OVER CURRENT-OK DETECTIONS.
+                                          Unit is load-bearing: refuted at HEAD
+                                          are (a) per-SCOPE-row floors (4 DATED
+                                          rows are zero-locus by design) and
+                                          (b) per-file BLOCK floors (SKILL.md
+                                          has 0 current-ok blocks, 3 current-ok
+                                          dets).  Do not re-key the unit without
+                                          re-running the HEAD invariance check.
```

## 3. Optional hardening (one behaviour change, measured)

One latent permanent-false-positive path remains: a scoped file whose declared
rows are **all DATED** (a pure record file) can never contribute a current-ok
detection, so the landed floor would FAIL it forever. Measured on a scratch
fixture (`SKILL.md` needle-free with its two rows re-keyed DATED, gate copy):
landed floor → `DECLARED ['BLIND-INSTRUMENT']`, exit 1; refined floor → PASS.
At HEAD the refinement is invisible (all three scoped files carry CURRENT rows;
17/14/3), and it does not weaken detection: the stripped-SKILL fixture still
FAILs (`receipts/live-refined-gut.out`).

```diff
@@ .ufo/gates/c1-census-v10.py:546-556 (landed df9ffdf9…)
     floor = {f: 0 for f in files}
     for recs in out.values():
         if not isinstance(recs, list):
             continue
         for rec in recs:
             if not isinstance(rec, dict):
                 continue
             for d in rec["asserts"]:
                 if d["disp"] == "current-ok":
                     floor[rec["file"]] += 1
-    h3_ok = all(floor[f] > 0 for f in files if filelines[f] is not None)
+    # Only files that declare a CURRENT row owe a live statement; a pure record
+    # file (all-DATED rows) is legitimately zero current-ok and must not FAIL.
+    current_row_files = {r[0] for r in SCOPE if r[3] == "CURRENT"}
+    h3_ok = all(floor[f] > 0 for f in files
+                if filelines[f] is not None and f in current_row_files)
```

Cost: one set comprehension; the G2 report line already prints the per-file
substrate. If the parent prefers to keep the landed predicate byte-stable, the
path in §3 belongs in the named-residual list instead — it is latent (no scoped
file is a pure record at HEAD), not live, and nothing in this round's claim
depends on it.

## 4. Not proposed (refused)

- **Re-keying the four zero-locus rows.** They are zero by measurement, and the
  rows are load-bearing coverage: a pin planted inside row 769-855 dates as
  `historical` (measured: `receipts/v-none-inj.out`, block 780-781). Dropping
  or narrowing them would turn a future locus there into `UNDECLARED` → the r4
  laundering path.
- **Widening `REA_GATE` to give rows 417-466 / 467-502 a locus.** That is a
  scope-vocabulary change (G4 class) whose blast radius is the whole census; it
  is the widening move the round's rules refuse.
