# PATCH PROPOSAL (not applied) — PL-1 rule #14 v5: make the verdict citation resolvable

Seat RV-2 (reviewer, chain c1), 2026-10-19 wave `arc3-loop1-round2`.
Target: `claims/c1/PL-1/rule-14-block.txt` (planner's v5 block), one path token.
Only relevant if the integrator lands the v5 text instead of EX-01's payload.

## Why — measured

My rule-citation audit (`rule-citation-audit.py --block ...`, HEAD `14b1682b…`)
resolves every citation token in the v5 block against repo-root paths:

```
T1/T2/T3/EX05/EX01 blocks: dead = 0
PL1-v5: citations 6, resolved 5, dead 1
  DEAD  claims/c1/verdict.md (file_absent_at_rev)
```

`git cat-file -e HEAD:claims/c1/verdict.md` → absent. The intended target exists
at `.ufo/waves/arc3-loop1-round1/claims/c1/verdict.md`; the block's own prose
qualifies it ("the same tree's"), but a citation that does not resolve from the
repo root is exactly the class this review exists to catch — a reader who greps
the literal token finds nothing.

## Proposed change

```diff
--- a/claims/c1/PL-1/rule-14-block.txt
+++ b/claims/c1/PL-1/rule-14-block.txt
@@
-  `.ufo/waves/arc3-loop1-round1/claims/c1/CR-2/entry-file-identity.txt`; the
-  same tree's `claims/c1/verdict.md` §E7/D9 re-applied both revisions
-  independently). None of the three was a lie when written — that is the
+  `.ufo/waves/arc3-loop1-round1/claims/c1/CR-2/entry-file-identity.txt`; the
+  same tree's `.ufo/waves/arc3-loop1-round1/claims/c1/verdict.md` §E7/D9
+  re-applied both revisions
+  independently). None of the three was a lie when written — that is the
```

## Verification after the fix (scratch, already run)

`rule-citation-audit.py --root . --rev HEAD --block /var/tmp/rv2/blocks/PL1-v5-fixed.md`:

```
revision 14b1682b1128d2e41085ebc79c9addeb8786d420 | rules 2 | citations 6 | resolved 6 | dead 0 | form_flags 0
```

The block's other
five citations already resolve, and its form is the conforming one: it cites
`SCORECARD.md`/`LOG.md` by section key ("by section key, never a bare line
number — rule #11 form"), so this fix would make the v5 text conform on both of
this seat's checks at once.
