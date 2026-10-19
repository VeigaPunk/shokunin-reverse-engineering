# Proposed patch text (NOT applied) — de-duplicate the r9 header bullet

Seat EX-15 (fixtures, chain c2), 2026-10-19. Target: `.ufo/gates/c1-census-v10.py`
(EX-16's write; this seat did not touch it). Measured at the live revisions
sha256 `a4c16763…` and (still present) `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`
(601 lines):

```
$ grep -n "Still named, NOT closed here" .ufo/gates/c1-census-v10.py
82:   - Still named, NOT closed here (no silent widening): H2 same-line inline-
85:   - Still named, NOT closed here (no silent widening): H2 same-line inline-
$ sed -n '82,87p' .ufo/gates/c1-census-v10.py
   - Still named, NOT closed here (no silent widening): H2 same-line inline-
     marker excusal; t5 DATED-shelter for historical-looking non-live values;
     H4 self-certification (covered externally, see above).
   - Still named, NOT closed here (no silent widening): H2 same-line inline-
     marker excusal; t5 DATED-shelter for historical-looking non-live values;
     H4 self-certification (covered externally, see above).
```

The three-line bullet appears twice verbatim (duplicated during one of the r9
revisions). Cosmetic only — no behavioural effect, no locus/scope effect (the
prose carries no gate token in this instrument's unit; verified by the census's
own PASS 0/0/0/0 at HEAD).

Minimal change: delete one copy (the second occurrence, `:85-87`), keeping the
first. After the edit, re-derive the instrument identity per the C1 rule-#14
discipline and re-run:

```
python3 .ufo/gates/c1-census-v10.py --root .        # expect PASS 0/0/0/0 exit 0
python3 .ufo/waves/arc3-loop1-round1/claims/c3/CR-5/tools/scope-diff.py \
        <before-copy> .ufo/gates/c1-census-v10.py   # expect 0 flags, table identical
```

EX-16 owns the target; this is patch text only.
