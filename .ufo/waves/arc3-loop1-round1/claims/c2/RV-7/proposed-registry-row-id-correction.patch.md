# RV-7 — registry-row finding-id correction (patch text, NOT applied)

Seat RV-7, chain c2, wave `arc3-loop1-round1`, 2026-10-19. Reviewer artifact.
**No repo file was written by this seat beyond this artifact and its seat
report.** `SKILL.md` is parent-integrated; this is patch text only.

## The defect

The landed probe (`.ufo/gates/citation-drift/citation-drift-probe.py`, sha256
`e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a`) emits
exactly three guard finding ids:

| id | landed site |
|---|---|
| `pointer_table_unpinned` | `citation-drift-probe.py:297` (+ CNE set `:82`) |
| `pointer_table_tampered` | `citation-drift-probe.py:306` (+ CNE set `:81`) |
| `pointer_table_unreadable` | `citation-drift-probe.py:292,303,312` (+ CNE set `:81`) |

`table_tampered` appears once in the landed probe, at `:444`, as the **selftest
case name** (`if case == "table_tampered":`) — never as a finding id.

Three c2 patch-text artifacts still declare the finding id `table_tampered`:

- `claims/c2/SC-4/scratch/registry-row.diff:8` — row text: "a digest-mismatched
  table → exit 2, finding \`table_tampered\`"
- `claims/c2/SC-4/scratch/patchtest/SKILL.md` — the applied copy of that text
- `claims/c2/RV-6/patchtest/registry-row.diff` — RV-6's private copy of the same
  text (RV-6.md §4 attack 8 already flagged this as a MISMATCH to reconcile)
- `claims/c2/EX-21/selfinvocation.patch.md:61,100,112,144` — EX-21 chose this id
  deliberately ("v1 → v2 changes: finding id `pointer_table_tampered` →
  `table_tampered`"), diverging from PL-2's design and from the landed code

Applying any of them would make `SKILL.md:371` document a finding id the
instrument never emits — a citation-class defect inside the registry row that
documents the citation gate.

**Correct text already exists:** `claims/c2/EX-20/registry-row.patch.md` (v2)
uses `pointer_table_tampered` / `pointer_table_unpinned` /
`pointer_table_unreadable` and matches the landed code. Integrate EX-20's v2,
not SC-4's diff and not EX-21's row.

## Minimal correction for SC-4's diff (if that text is preferred)

One token, in the diff's `+` row line (line 8 of
`claims/c2/SC-4/scratch/registry-row.diff`):

```diff
-...a digest-mismatched table → exit 2, finding `table_tampered`, an absent table → exit 2, finding `pointer_table_unreadable`)...
+...a digest-mismatched table → exit 2, finding `pointer_table_tampered`, an absent table → exit 2, finding `pointer_table_unreadable`)...
```

## Also verify before applying any row

The landed guard is **fail-closed** on an unpinned baseline, so the row's
unpinned clause is true as written (`pointer_table_unpinned`, exit 2) — measured
by RV-7 on the landed artifact (`verify-extra-post.log`, X2/X3) and consistent
with EX-20 v2 and PL-2. A row that omits the unpinned clause understates the
landed behaviour; a row that names it under a different id is wrong.

Evidence for every claim above is in this seat's `verify-post.log`,
`verify-extra-post.log`, `named-checks-landed.log`, and `reproduce-midlanding.py`.
