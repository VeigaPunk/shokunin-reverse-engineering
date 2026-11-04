# ExecLedger — scoped repairs report

Report: `.ufo/waves/round-69/w1/ExecLedger.md`

Drafts and exact commands: `.ufo/waves/round-69/w1/ExecLedger/repairs.md`, with separate V1/V2/V5 drafts and six retained receipts under `ExecLedger/evidence/`.

## Observations at landing `5ee94c56ce7490938ee38c2e5c10930a1fd1330a`

- **V1:** the entry now has an append-only correction block, with all three provenance fields as backticked list items (count 3). Do not append the duplicate draft.
- **V2:** the row moved, but the landing shortened the delimiter to three cells against a four-cell header. Strict GFM renders no Knowledge table. Exact remaining change at `corpus/README.md:119`: replace `|---|---|---|` with `|---|---|---|---|`. The scratch mirror renders a table after that change. Evidence: `ExecLedger/evidence/table-parse.txt`.
- **V5:** the prescribed `printf`/`wc -w` command prints **10**, with or without the trailing period. The pinned manual re-fetch matched 37,208 bytes and sha256 `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42`. Exact S271 superseding row and lesson notes are drafted, 11 cells with the required `supersedes S269 — ` prefix. The landing instead records a reason not to supersede. Those branches cannot both stand; the L1 must reconcile the entry and lesson if S271 lands. Duplicate-URL correction precedents are retained as evidence against that part of the recorded rationale.

## Boundaries and handoff

Only this report and files under `w1/ExecLedger/` were written; no tracked implementation file, index, commit or push was changed by this seat. Scratch was deleted after retaining receipts. No tools installed. No lane gate/build/test/lint was run; only the explicitly requested scratch measurements and document parsing were exercised. Parent should apply the V2 delimiter repair and run its integrated corpus checks. No missing prerequisite blocks the drafts.
