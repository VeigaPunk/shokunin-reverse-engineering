# Proposed corrections to `claims/c3/EX-42/census.md` — clause-level (NOT applied)

Proposal by seat EX-42 (late join), wave `arc3-loop1-round3`, 2026-10-19.
Artifact under proposal: `.ufo/waves/arc3-loop1-round3/claims/c3/EX-42/census.md`,
sha256 `6a0da39b2d84977f98bbf6f44d6f8869fb48c6be8e74303f87ee69d28aecbaec` (22,972 B)
at proposal time. This file is a **proposal only**: the landed census was deliberately not
rewritten by this seat, so its byte identity stays stable for the parent's cross-references.
Both corrections are clause-level; neither changes the acceptance result (§5) or the ledger's
row counts.

## E1 — §4.4 row 5 cause clause is falsified by the repo (measured)

Replace the row-5 cause text:

> **gitignored install prefix** (`node_modules/` wave-.gitignore): no committed git object to grade;
> provenance is the receipted install-receipt anchor

with:

> **gitignored install content**: the prefix directory itself is a committed tree object
> (`package.json` + `package-lock.json` tracked), but the installed compiler bytes live under the
> wave-.gitignore'd `node_modules/`, so there is no gradeable *content* object; provenance is the
> receipted install-receipt anchor (`kbarc3-ev-install-receipt`). Note: the trailing-slash directory
> token is outside the enumerator's extension/slug net (0 hits in `enumeration.tsv`) — this ledger
> row is a manual addition.

Measurement (re-derived at HEAD `c07af80`):
`git cat-file -e HEAD:.ufo/waves/arc3-loop1-round1/tools/solc-prefix/` → exit 0 (tree);
`git ls-tree -r HEAD -- .ufo/waves/arc3-loop1-round1/tools/` → the two files above;
`grep -c solc-prefix enumeration.tsv` → 0.

## E2 — cause-class count label does not match the table (measured: 7, not 5)

§0 point 2: "12 NO-ENTRY rows in five named cause classes (§4.4)" → "…in seven named cause
classes (§4.4)".
§4.4 heading: "NO-ENTRY ledger — 12 rows, five cause classes, none convenient" → "…12 rows,
seven named cause classes, none convenient".

The §4.4 table's distinct bolded labels, in order of first appearance:
1. field/key name (rows 1-2; row 12 is the same class, restated as a duplicate)
2. dirty-worktree-state record (row 3)
3. operator-mutable class (row 4)
4. gitignored install prefix (row 5)
5. line reworded, no arc3-introduced citation (rows 6-7)
6. record-class path mentions, no stated number (rows 8-10)
7. suffix token in prose (row 11)

Row count re-derives exactly (rows 1-2, 3, 4, 5, 6-7, 8-10, 11, 12 = 12); every row carries a
named cause. Bookkeeping label only — no acceptance effect.

## Not proposed

- §5.3's self-reported inaccurate exempt clause ("no stated number means no drift class") is
  already flagged in the census itself; this seat re-derived the falsification (15 anchor-kind
  entries in the landed table carry no line number) and adds nothing further.
- §5.4's gap (LOG.md:1442) and residual R2 (README r3 token) are table-side fixes owned by
  EX-41 / the parent's landing decision, not census-text edits.
