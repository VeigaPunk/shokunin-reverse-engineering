# Proposed patch text (NOT applied) — SCORECARD:908 parenthetical wording

Seat RV-11 (reviewer, chain c3). Target: `SCORECARD.md:908` (inside the DATED
row `:769-855`, round-4 section — parent-owned; this seat writes no SCORECARD).

Current text (`SCORECARD.md:908`):

> | freshness (fleet) — C3 | census verdict FAIL(undeclared=2, unreproducible at HEAD) → v10 PASS 0/0/0/0 at the work tree (fixed-bound re-key; laundering path refused) + lessons:82 discharged (content-anchored erratum) | improved |

Measured against the recovered v9 (`213fe679…`) at HEAD `e845c2b`:

```
$ python3 scratch/c1-census-v9-recovered.py --root . --quiet
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=2 unresolved=0)     exit=1
SCOPE-ERRORS: ["SCORECARD.md:635 marker '2026-10-18' absent from ''"]
```

The `undeclared=2` reading **is** mechanically reproducible at HEAD (and at every
tree tested: 766/854/1336 lines). What is unreproducible at HEAD is the 701-line
`PASS` (v9@HEAD ≠ PASS) — the reading that is offset-bound, per round-3's own
`C1.md` §2.8 observation (i). As written, the parenthetical attaches
"unreproducible" to the FAIL, which the measurement does not support.

Suggested wording (append-only correction or a parent rewrite at integration):

```diff
- | freshness (fleet) — C3 | census verdict FAIL(undeclared=2, unreproducible at HEAD) → v10 PASS 0/0/0/0 at the work tree (fixed-bound re-key; laundering path refused) + lessons:82 discharged (content-anchored erratum) | improved |
+ | freshness (fleet) — C3 | census verdict FAIL(undeclared=2 at the 766-line card; the 701-line PASS is offset-bound and unreproducible at HEAD) → v10 PASS 0/0/0/0 at the work tree (fixed-bound re-key; laundering path refused) + lessons:82 discharged (content-anchored erratum) | improved |
```

Evidence for the parenthetical: `claims/c3/RV-11/e22-reproduction.md` §1-§2
(matrix + exits); recovery proof for v9 in the same artifact.
