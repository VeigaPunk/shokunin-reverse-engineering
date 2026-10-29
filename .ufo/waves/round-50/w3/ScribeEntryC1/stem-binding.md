# Stem binding — where the C1 entry file must be written, and what the frozen counter checks

Author: seat `ScribeEntryC1`, round 50 attempt 2, wave 3 (build). Read-only seat; nothing here was
applied to the lane. All statements below are [observation] of committed bytes at lane HEAD
`6f4aba635fc47b5823ed42afe9c8b5dc3e28127f` (receipt `receipts.tsv`, rows 1-8).

## The three stems in the tree

| stem / path | where it appears | state |
|---|---|---|
| `2026-10-28-r50-avm-le-squashfs-core` | `tools/round-50/c1-counter.py:377-378` (`ENTRY`, `STEM`) | **authoritative** — the frozen counter reads it |
| `2026-10-28-r50-le-avm-members-core` | `.ufo/waves/round-50/l1/land_c1.py:11-12` (`STEM`, `ENTRY`), `.ufo/waves/round-50/l1/land_sources.py:11-12` (`STEM`, `ENTRY`) | stale — attempt-1 landing scripts, not yet corrected |
| `2026-10-29-r50-le-avm-hsqs-core` | named in the **first draft** of `plans/round-50-attempt2-claims.md`; this seat's task text repeated it | corrected away by commit `6f4aba63` ("attempt-2 claims corrected — entry stem pinned to the frozen counter constants") before any data |

`git show 6f4aba63 -- plans/round-50-attempt2-claims.md` shows the correction; the current file
(lines 106-110) pins `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` and says so
explicitly ("the counter, not this file, is the rule").

## What the frozen counter binds (the reason the stem is not free)

`tools/round-50/c1-counter.py` (sha256 `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813`):

| counter line | binding | what the landing must contain |
|---|---|---|
| 377-378 | `ENTRY` / `STEM` | the entry file at `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` |
| 2447-2449 | `province_core_row` | a row in `PROVINCE.md` `## Round-50 additions to Core` whose **first cell** contains `squashfs_v4_le` (word-bounded, `HANDLER_RE` :426), whose text (with `ENTRY` removed) contains `AVM marker` (`AVM_MARKER_RE` :427, case-insensitive `AVM[ _-]marker`), and which contains the `ENTRY` path string |
| 2451-2453 | `frontier_note` | one `PROVINCE.md` line containing `Round-50 frontier note` (`FRONTIER_MARK` :380), the `STEM`, and an `LE AVM` / `AVM LE` token (`LE_AVM_RE` :428, searched with the stem removed) |
| 2457-2458 | `entry_present` | the entry file exists at `ENTRY` at the measured revision |
| 2459-2477 | `sourced` | the entry's `source:` lines name SOURCES rows whose `opened` cell is `2026-10-28` or `2026-10-29` (`OPENED_DATES` :393) and whose `used-by` cell contains the `ENTRY` path or the `STEM` |
| 2480-2482 | `coverage_map_row` | a row of `corpus/README.md` `## Coverage map` containing the `STEM` (the round-49 coverage-map row is at `corpus/README.md:105`, the last row of that section, so a row inserted after it is inside the section) |

`BINDINGS` (:432-434) = `province_core_section`, `province_core_row`, `frontier_note`,
`entry_present`, `sourced`, `coverage_map_row`, `carriers_spec_ok`, `gap_rule_ok`,
`frozen_tables_valid` — all nine must be true for `met_target`.

## The two stale landing scripts (action for the L1)

`.ufo/waves/round-50/l1/land_c1.py` and `.ufo/waves/round-50/l1/land_sources.py` still carry the
attempt-1 stem `2026-10-28-r50-le-avm-members-core`:

* `land_c1.py` writes the entry, the `PROVINCE.md` Core row (whose text embeds `ENTRY`), the
  frontier note (which embeds `STEM`), the `corpus/README.md` coverage-map row and the knowledge
  index row — all with the old stem. With the old stem every one of the counter's documentation
  bindings above is red.
* `land_sources.py` builds the S243 / S244 / S245 / S249 rows with `used-by` = the old stem, and
  then **drops** them on purpose: `S = {k: S[k] for k in ('S246', 'S247', 'S248')}` with the comment
  "honest stop: C1 rows S243-S245/S249 are not landed (no entry cites them)". That filter must be
  removed for the attempt-2 landing (the entry now cites all four) and the `used-by` cell must name
  the counter's stem.

Both scripts are the L1's own wave files, not the lane's `tools/`, `plans/` or `corpus/`; this seat
did not modify them.

## The draft

`.ufo/waves/round-50/w3/ScribeEntryC1/entry-draft.md` — 87 lines, body text only (it names no stem
of its own), six `<FILLED AT LANDING>` placeholders for `carriers_matched`, published file counts,
gaps, `MaliciousSymlinkRemoved` counts and evidence ids, and every claim tagged
`[observation]` / `[inference]` / `[unknown]` (QUALITY 5) with a "What was NOT examined" section
(QUALITY 7). It is paste-ready under the stem above.
