# PATCH — census SCOPE disposition (EX-29, chain c3, arc3-loop1-round1)

**Target (EX-28's write, not this seat's):** `.ufo/gates/c1-census-v10.py`
**Target identity at analysis time:** 433 lines, sha256
`36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48`
**Cause and analysis:** `claims/c3/EX-29/dispositions.md` (§2c rows 3 and 20;
§3 flags F1-F4).
**This file is patch text. It has not been applied by this seat.**

## Why this exact shape (two constraints, both measured)

1. **Line-safe, not just line-neutral.** r5 seat reports cite census line numbers
   (`arc2-loop1-round5/E6.md:7` `:67-70,370-429`; `E5.md:56,90` `:97-108,202-215,
   391-399`; `CR4.md:66,72` `:74-83,124-135,218-234,370-386`; `R6.md:13`
   `:5-10,74-80,124-134,218-234,376-399`; `C4.md:107` `:85-108`). Those are dated
   records (r3: adjudicated, not edited) and the lane's precedent is that landings
   must not move landed citations (r8's re-key changed 3 lines in place, net 0:
   `git show 6bc4c29 -- .ufo/gates/c1-census-v10.py`; CR7's +18-line shift attack
   refused, `SCORECARD.md:755`). Therefore: the two retired rows are **replaced
   in place** and the disposition text is **appended at EOF** — no existing line
   number moves.
2. **The retirements are loss-free and verdict-neutral, measured.** See
   `sim-outputs.txt` SIM-A1 (rows 3+20 removed → `PASS 0/0/0/0`, `SCOPE-ERRORS: []`)
   and `patched-run.txt` (this exact patched file run at the repo root →
   `PASS 0/0/0/0`, exit 0). The tripwire survives the retirement: the same patched
   file against a fixture with a stale claim planted at `:856` → `FAIL
   undeclared=1`, exit 1 (recorded in `patched-run.txt` §2).

## Patch

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@ -86,7 +86,7 @@
 SCOPE = [
     ("PROVINCE.md", 8, 13, "CURRENT", None, None),
     ("PROVINCE.md", 15, 26, "CURRENT", None, None),
-    ("PROVINCE.md", 40, 43, "DATED", 40, r"verified on this host 2026-10-13"),
+    # RETIRED (EX-29, 2026-10-19): PROVINCE.md 40-43 — zero loci/literals; cause in the v10 disposition block at EOF.
     ("PROVINCE.md", 44, 44, "CURRENT", None, None),
     ("PROVINCE.md", 45, 62, "DATED", 40, r"verified on this host 2026-10-13"),
     ("PROVINCE.md", 64, 71, "CURRENT", None, None),
@@ -104,7 +104,7 @@
     ("SCORECARD.md", 636, 702, "DATED", 636, r"2026-10-18"),
 
     ("SCORECARD.md", 703, 768, "DATED", 704, r"arc2-loop1-round2"),
-    ("SCORECARD.md", 769, 855, "DATED", 769, r"arc2-loop1-round3"),
+    # RETIRED (EX-29, 2026-10-19): SCORECARD.md 769-855 — zero loci/literals; cause in the v10 disposition block at EOF.
 ]
 
 PIN = re.compile(r"rea-agents@(\d+\.\d+\.\d+)", re.I)
@@ -431,3 +431,21 @@
 
 if __name__ == "__main__":
     sys.exit(main())
+
+# ---- v10 disposition (arc3-loop1-round1 EX-29, 2026-10-19; HEAD e845c2b) ----
+# Every SCOPE row's bound was re-audited against content at HEAD: all rows were
+# content-tight, so no re-key was required; the E22 drift finding is discharged
+# by measurement (PASS 0/0/0/0 at HEAD; receipts in the wave seat dir
+# .ufo/waves/arc3-loop1-round1/claims/c3/EX-29/). Two rows were RETIRED with
+# cause (zero loci, zero version literals, no marker duty) and replaced in place
+# by the comments above, so no landed line citation moves:
+#   PROVINCE.md 40-43 and SCORECARD.md 769-855 -> now UNDECLARED, fail-closed.
+# Two zero-locus rows were RETAINED because they are the only classification
+# path for dated-record literals the gate cannot see (SCORECARD.md 417-466
+# :463; 467-502 :467,:471,:496,:500).
+# Widening a DATED bound to cover a new append, or declaring the pin-free
+# regions (SCORECARD.md 856-1336, PROVINCE.md 132-162, SKILL.md 21-371), stays
+# REFUSED: measured to launder a stale append as historical (R3 section 5,
+# CR3 section 2.5; EX-29 sims B2/B3). The pin-free append discipline (E15
+# section 3.4) is what keeps the short bound safe. Bound-drift detection (slide
+# absorption, EX-29 sim C2) is a named next-round candidate, not landed here.
```

The exact diff as generated against a patched copy is also stored verbatim at
`patch-diff.txt` (it differs only in the `+++` header path, which pointed at the
seat's temporary verification copy).

## Pre-registered expectations (measured by this seat on the patched copy)

| run | command | expected | measured |
|---|---|---|---|
| post-apply, repo root | `python3 .ufo/gates/c1-census-v10.py` | `PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, `SCOPE-ERRORS: []`, exit 0 | same (`patched-run.txt`) |
| planted stale append at `:856` | `python3 <patched> --root <fixture>` | `FAIL undeclared=1`, exit 1 | same (`patched-run.txt`) |

## Steps for EX-28

1. Apply the patch (the two in-place replacements and the EOF block). Do not add
   or remove any other line — see constraint 1.
2. Run `python3 .ufo/gates/c1-census-v10.py` at the records commit; confirm
   `PASS 0/0/0/0` and `SCOPE-ERRORS: []`.
3. Keep the round's own SCORECARD records append **version-token-free** (it
   lands at `:856+`, outside every declared row): a version literal there fails
   `undeclared=1` — measured (SIM-B1) and already recorded at
   `SCORECARD.md:1069`. If the append must cite a version, declare that block
   narrowly and re-key to its measured end in the same commit.

## Peer variants to reconcile (same chain, all patch text, none applied)

- **Header stanza (the claim's "stated in the instrument's own header")**: SC-6
  `claims/c3/SC-6/e22-disposition.draft.md` §6 P1 and SC-7
  `claims/c3/records-drafts/census-header-draft.md` §2 both expand line 1 into a
  ~15-line docstring. That satisfies the header requirement but inserts net +14
  to +16 lines, moving every citation below it (SCOPE 86→~100; r5's `:97-108`
  →~111-122). No probe risk: `pointer-table.json` pins no census line (0
  matches). If that form lands, take the SCOPE half of this patch only and drop
  this seat's EOF block.
- **Fixed-bound guard comment**: RV-10
  `claims/c3/RV-10/proposed-fixed-bound-guard.patch.md` restores Z1 §4d's
  fixed-bound comment that the r4 rows landed without. Independent of this
  patch; both can land.
- **Missing-file guard**: RV-11 `claims/c3/RV-11/proposed-missing-file-guard.patch.md`;
  **G2 positive floor**: CR-5 `claims/c3/CR-5/proposed-g2-positive-floor.patch.md`.
  Neither interacts with the SCOPE table.
- **Retire-branch divergence**: SC-6 and SC-7 both conclude "none retired". This
  patch's two retirements are the loss-free discharge of the debt's "or retire"
  branch under EX-29's per-row criterion (`dispositions.md` §1-§2c) and are
  measured verdict-neutral; they are **not required** for the claim's PASS. The
  parent adjudicates.

## If the parent prefers a zero-diff landing

The retirements are the recommended, measured-neutral form, but they are not
required for the C3 claim: no row is stale at HEAD, so the claim's antecedent
("if any scope row is undeclared/stale") is already false and the census already
reports `PASS 0/0/0/0`. In that variant the disposition text in §2c and §3 of
`dispositions.md` is still the record of the E22 adjudication; only the two
retirements and the EOF block are dropped.
