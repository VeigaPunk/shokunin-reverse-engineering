# Proposed patch text (NOT applied) — dedupe the duplicated "Still named" stanza

Seat RV-8 (reviewer, chain c2), arc3-loop1-round2, 2026-10-19. **Patch text
only** — EX-16 owns `.ufo/gates/c1-census-v10.py`; this seat wrote nothing to
the target.

Target state: the paragraph is duplicated in every late digest — verified at
`df9ffdf9…` (601 L, 12:12:15Z), `a4c16763…` (603 L, EX-16 "r9 final"
12:16:31Z), and the digest at RV-8's close `d0772ce8…`
`d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`
(610 L; still moving at close). The `:82-87` layout is identical in all three;
re-check the anchor lines after any further landing (rule #14).

## Finding (measured)

The paragraph is duplicated verbatim at `:82-84` and `:85-87`:

```
$ grep -c "Still named, NOT closed here" .ufo/gates/c1-census-v10.py
2
$ sed -n '82,84p' .ufo/gates/c1-census-v10.py > /var/tmp/rv8-kai/dup1.txt
$ sed -n '85,87p' .ufo/gates/c1-census-v10.py > /var/tmp/rv8-kai/dup2.txt
$ diff /var/tmp/rv8-kai/dup1.txt /var/tmp/rv8-kai/dup2.txt   # DUP-IDENTICAL, exit 0
```

Likely cause: two overlapping landings each carried the same paragraph. Note
for the parent: EX-23's `header.patch.md` Hunk D replaces ONE occurrence
(anchored at 82fb807e `:74-76`, where the copy was single); applying it naively
to the final target rewrites one copy and leaves the other.

## Proposed diff (context, not applied)

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@ -82,9 +82,6 @@
    - Still named, NOT closed here (no silent widening): H2 same-line inline-
      marker excusal; t5 DATED-shelter for historical-looking non-live values;
      H4 self-certification (covered externally, see above).
-   - Still named, NOT closed here (no silent widening): H2 same-line inline-
-     marker excusal; t5 DATED-shelter for historical-looking non-live values;
-     H4 self-certification (covered externally, see above).
 
   Post-edit identity is recorded in the landing receipt (claims/c2/EX-16/
```

Post-fix check (the reader's side):

```
$ grep -c "Still named, NOT closed here" .ufo/gates/c1-census-v10.py    # expect 1
$ python3 .ufo/gates/c1-census-v10.py --root . --quiet                   # expect PASS, exit 0
```
