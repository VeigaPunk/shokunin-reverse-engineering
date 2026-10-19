# EX-32 (late join) — optional strengthening of the re-anchor (patch text)

**Proposal only, not applied.** The table is EX-41's (C3's) real-path target.
This is a **superseding variant** of the §2 re-anchor in
`pointer-table-reanchor.patch.md` — the parent/EX-41 should apply **one or the
other**, never both. Both are measured; neither is required by the frozen claim.

## 1. Why (measured, evidence/late-row-discrimination.txt)

The §2 form, `precedence CONTENT-DRIFT > (UNEVALUABLE > )?ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH`,
accepts a row whose precedence chain is followed by junk:

| row variant | §2 form | this form |
|---|---|---|
| round-2 row (real, pre-landing) | pass | pass |
| revised row (real, post-landing) | pass | pass |
| wrong: UNEVALUABLE after ABSENT | REDDENS | REDDENS |
| wrong: UNEVALUABLE last | **pass** | REDDENS |
| wrong: reversed chain | REDDENS | REDDENS |
| wrong: `UNEVALUBLE` typo | REDDENS | REDDENS |

The laxity is **inherited, not introduced**: the round-2 needle
(`… METADATA-DRIFT > MATCH`) also accepts `… > MATCH > UNEVALUABLE;`, because a
substring match has no anchor at the tail. So the §2 re-anchor is not a
regression — it merely carries forward a pre-existing looseness. This variant
closes it.

## 2. The patch

Replace the §2 `must_match` with:

```
precedence CONTENT-DRIFT > (UNEVALUABLE > )?ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH(;|\||$)
```

The `(;|\||$)` tail anchor matches how the registry row actually terminates its
clause (`… > MATCH;`) while still accepting a `|`-delimited cell end or a line
end, so it does not over-fit the current wording.

## 3. Status

Not applied, not re-pinned, no digest claimed — the §2 patch's digests
(`a810bd17…` table, `e33f0e2d…` expected) **do not apply** to this variant; a
different table digest would result. This is offered as a design note for the
parent's ruling: if the strengthening is wanted, it should be built and
re-pinned by EX-41 in the same commit, exactly as §2 prescribes. If not, §2
stands as measured.
