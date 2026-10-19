# Advisory patch text — RV-10 (fixed-bound rationale + optional bound guard)

Status: **proposal only, NOT applied.** The write target
`.ufo/gates/c1-census-v10.py` belongs to seat EX-28 (c3) alone. These hunks
compose with EX-26's `proposed-census-header-disposition.patch.md` and SC-6's
`e22-disposition.draft.md` §6 (both touch the header only; these touch the
SCOPE list and `assert_markers`).

Measured basis (this seat, 2026-10-19; full commands and outputs in
`fixtures.md` + `evidence/`): the r4 refusal of the open-ended bound is live
in the landed form — the same synthetic stale append reads `UNDECLARED` (FAIL,
rc 1) under the fixed bound and `historical (dated scope)` (PASS, rc 0) under
both the `900` overshoot and the `10**9` open variants (fixtures A-E); a
run-time guard makes the relaxation itself a scope error (G1-G4b).

## Hunk 1 — restore the fixed-bound rationale at the rows (documentation)

Z1 §4d's rationale comment (`.ufo/waves/arc2-loop1-round4/Z1.md:145-150`) was
not landed; the rows landed bare and only the line-1 provenance cites Z1.
Restore it (wording adapted to the post-r8 line numbers; cite the
re-measurement):

```diff
     ("SCORECARD.md", 703, 768, "DATED", 704, r"arc2-loop1-round2"),
     ("SCORECARD.md", 769, 855, "DATED", 769, r"arc2-loop1-round3"),
+    # fixed-bound by design (Z1 section 4d; refused the open-ended form): an
+    # out-of-range append must read UNDECLARED and be re-keyed deliberately,
+    # never absorbed silently. The open-ended tail was measured to launder a
+    # stale append (R3 section 2.7 rows 10/11; Z1 section 5.5; re-measured
+    # 2026-10-19 arc3-loop1-round1 RV-10: fixed -> FAIL undeclared=1,
+    # 900/10**9 -> PASS 0/0/0/0 with the locus read as historical).
 ]
```

## Hunk 2 — optional mechanical guard (the relaxation itself fails loud)

Adds 5 lines at the top of `assert_markers` (a pre-loop over **all** SCOPE
rows, so CURRENT rows are covered too — an open-ended CURRENT bound would
otherwise absorb loci into the stale/current-ok checks instead of UNDECLARED).
It converts the open-ended/overshooting relaxation from "PASS that launders"
into a scope error **statically** — no laundered locus needed.

```diff
 def assert_markers(filelines):
     """G15: every declared DATED range must carry its marker text."""
     errs = []
+    for (f, s, e, cls, ml, mr) in SCOPE:
+        lines = filelines.get(f)
+        if lines and e > len(lines):
+            errs.append("%s: declared end %d beyond EOF (%d lines) -- open/overshooting bound"
+                        % (f, e, len(lines)))
     for (f, s, e, cls, ml, mr) in SCOPE:
         if cls != "DATED" or ml is None:
             continue
```

Measured (this seat, variants in `evidence/variants.diff`):

| instrument | tree | result |
|---|---|---|
| landed + guard @HEAD | clean HEAD | PASS rc 0, scope-errors `[]` (inert; output byte-identical to the census's own HEAD capture, sha256 `3b677b8e…` — the same digest five seats captured) |
| landed + guard @r4 | clean r4 | PASS rc 0, scope-errors `[]` (inert) |
| guard + `10**9` open | clean HEAD | FAIL rc 1 — `SCORECARD.md: declared end 1000000000 beyond EOF (1336 lines)` |
| guard + `900` overshoot | clean r4 | FAIL rc 1 — `declared end 900 beyond EOF (854 lines)` |

Trade-off stated: the guard makes "bound at EOF" a hard invariant. That is the
r4 intent, but it also means any future deliberate bound that must exceed the
current EOF (none is wanted; bounds are meant to be re-keyed to EOF) or any
scoped file shrinking below a declared end becomes a scope error. Both are
fail-loud directions. If EX-28/parent prefers no code change this round,
Hunk 1 alone carries the rationale; the guard can wait for the next
instrument touch. EX-26's and SC-6's header stanzas remain compatible either
way.
