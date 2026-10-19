# Proposed patch (NOT APPLIED) — census G2 positive-assertion guard is vacuous

Seat CR-5 (critic, c3), arc3-loop1-round1, 2026-10-19. **This is patch TEXT
only.** The critic seat may not write `.ufo/gates/`; EX-28 owns that target.
Target: `.ufo/gates/c1-census-v10.py` (before-state sha256
`36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48`).

## Finding (measured, receipt attached)

With all three needle regexes neutered (`PIN`/`VER`/`PTR` replaced with
never-matching patterns), the census reports `loci=0` on all three files and
still prints `G2 positive-assertion guard: ok` → `VERDICT: PASS (stale=0
ambiguous=0 undeclared=0 unresolved=0)`, exit 0. Receipt:
`claims/c3/CR-5/receipts/census-blind-at-head.out`; fixture
`claims/c3/CR-5/tools/census-blind.py`.

Cause — `main()`:

```python
g2_ok = len(out.get("current-ok", [])) > 0 or (not stale and not unatt and not undecl and not unres)
```

The second disjunct is true exactly when the run finds nothing at all, so the
"positive-assertion guard" passes when there are no assertions — the blind
instrument cannot be distinguished from the clean one. Every historical run
measured this wave had a large positive floor (current-ok dets: 29 at
`b21c0da`, 31 at `679af5d`, 35 at `e87e507`/`6bc4c29`; 10 loci at HEAD
`e845c2b`), so requiring the floor breaks no observed run.

## Proposed diff (context, not applied)

```diff
@@ def main():
-    g2_ok = len(out.get("current-ok", [])) > 0 or (not stale and not unatt and not undecl and not unres)
+    g2_ok = len(out.get("current-ok", [])) > 0
@@ print G2 line
-    print("G2 positive-assertion guard: %s" % ("ok" if g2_ok else "SUSPECT"))
+    print("G2 positive-assertion guard: %s (current-ok loci=%d, total loci=%d)" %
+          ("ok" if g2_ok else "SUSPECT", len(out.get("current-ok", [])),
+           sum(c["loci"] for c in counts.values())))
```

Optional stronger form (calibration decision, parent/EX-28's call): also fail
when total loci == 0 while anchors are live, e.g.
`and sum(c["loci"] for c in counts.values()) > 0` — redundant with the above
but self-documenting in the verdict line.

## Why it matters for this round's claim

The c3 claim's after-state is a PASS produced by this instrument. The census
cannot detect its own widening (receipt
`claims/c3/CR-5/receipts/census-widened-at-head.out`) and cannot detect its
own blindness (receipt above). Any edit that narrows detection (regex or
`REA_GATE` changes) or widens scope will read PASS unless the diff and the
locus counts are audited externally. Recommendation: audit EX-28's diff with
`claims/c3/CR-5/tools/scope-diff.py` and re-check locus-count invariance
(HEAD before: PROVINCE 6 / SCORECARD 9 / SKILL 2; current-ok loci 10).
