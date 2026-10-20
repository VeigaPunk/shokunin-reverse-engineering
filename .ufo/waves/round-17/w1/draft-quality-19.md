# Draft: QUALITY.md admission row 19 (R16-PROVENANCE)

Status: author-side draft by DraftQuality19 (advisory). L1 integrates. Not applied to `corpus/QUALITY.md`.

Placement: insert as the new last row of the `## Admission criteria` table, immediately after row 18 (`corpus/QUALITY.md:28`), before the blank line at `corpus/QUALITY.md:29`. Rows 1-18 unchanged. Signals table follows unchanged.

Table header, copied from `corpus/QUALITY.md:9-10`:

| # | criterion | why (lesson) | supersedes |
|---|---|---|---|
| 19 | Any statement that a pin, input, fixture, or producer was unchanged *during*, *across*, or *throughout* a run or execution cites retained pre-run and post-run records (absolute path, sha256, size, mtime_ns, UTC timestamps) and their equality comparison. A boolean such as `pins_unchanged_during_run: true`, a single `executed_at_utc`, or a hash map matched to committed blobs is not such a record. With only those, the admissible wording is "map matches committed source-revision blobs; temporal stability not evidenced". Equal pre/post records support "identical at each recorded instant" only; "throughout" or "stable during" additionally needs a retained continuous change-notification record with its gap bound stated, and is otherwise inadmissible. Corrections are append-only: a stale statement is qualified by a named correction line that cites its path, never rewritten. | `corpus/lessons/round-16-verifier-spotcheck.md:183` (R16-PROVENANCE: `.ufo/waves/round-16/verification.json` retains a 20-entry `producer_and_fixture_sha256` map, one `executed_at_utc`, and `pins_unchanged_during_run:true` with no before/after maps or timestamps; committed r16 statements in `corpus/lessons/round-16.md:154`, `LOG.md:2012` and `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` repeat it); `corpus/lessons/round-17.md` Mistakes row for R16-PROVENANCE (not yet on disk at draft time) | — |

Notes for L1 (not part of the row):
- Row 18 already admits the R16-INVOCATION route (`corpus/lessons/round-16-verifier-spotcheck.md:184`) through its "explicitly names an unexercised variant" clause, so row 19 carries only the R16-PROVENANCE route.
- The `why` cell cites a path that will exist only after the r17 lesson lands; re-verify that path and row wording at integration.
- After integration the admission table has 19 rows and the signals table keeps its six rows.
