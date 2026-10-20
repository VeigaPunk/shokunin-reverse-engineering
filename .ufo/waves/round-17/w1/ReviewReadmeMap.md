# ReviewReadmeMap — r17 token placement in `corpus/README.md` (coverage map + Frontier)

Axes: calibration (a reproducible placement matrix from the committed gate) and depth (the line-shift hazard class plus its SCORECARD coupling).

**Verdict:** place `2026-10-20-r17-go-carrier-diagnostics` as an **in-place append to the existing Go-lineage coverage-map row at `corpus/README.md:35`** (first-cell token list; optional same-line clauses in cells 2/3). Do **not** add any row to `corpus/README.md`, do not split `:35`, do not put the token in `## Frontier`. This is the only zero-shift placement of the token that measured clean.

## Pinned lines (`.ufo/gates/citation-drift/pointer-table.json`, HEAD `b563c79`)

| pinned surface | pointer-table id(s) | needle that must survive |
|---|---|---|
| `corpus/README.md:22` | `readme22-r7range`, `readme22-r8range` | cited r7-entry range must hold `75,218 procedures`; cited r8 range must hold `kernel-OOM-killed at the 9G cap in 4m42.945s` |
| `corpus/README.md:138` | `sc72-readme-nitrow` (`SCORECARD.md:72` states `corpus/README.md:138`) | `4 nits: 2 fixes applied at integration` |
| `corpus/README.md:175` | `readme175-sc1217`, `readme175-r7range`, `readme175-r8e2` | `SCORECARD.md:1216` pointer, r7 range, `.ufo/waves/arc2-loop1-round8/E2.md` range |
| `corpus/README.md:180` | `sc69-readme-177` (`SCORECARD.md:69` states `corpus/README.md:180`) | `held, not frontier` |
| `corpus/README.md` (file-level, no `pin_line`) | `readme38-arc3r1-token` | token `2026-10-19-arc3-r1-evm-real-solc` must still appear somewhere |

Probe semantics (OBSERVATION, `.ufo/gates/citation-drift/citation-drift-probe.py:180,191,212-250`): `extracted` entries read the stated number out of the citing line, then verify the target line; a line insert therefore renumbers the target while the stated number stays, which is exactly the `citation_dead` class. `sc69-readme-177`'s id names an old README line; its `line` field is `SCORECARD.md:69` — do not read the id as a README pin.

Other README structure anchors: row rule `corpus/README.md:8-9` ("A row is written when its file exists, never before"); coverage map heading `:11`, table rows `:13-68` (blank `:69`); Knowledge table data rows `:74-153`; `## Lessons` `:155`; `## Frontier` `:170-181`; `## Known gaps` `:183-190`. Line `:35` is 1,196 chars, three cells, no internal pipes.

## Measured placement matrix

Method (OBSERVATION, instrument reuse, no writes): imported the committed `citation-drift-probe.py`, substituted only the `corpus/README.md` text in memory, resolved **all 60 `entries` + 5 `quoted`** at HEAD; the worktree was never written (`git status` clean apart from untracked `.ufo/waves/round-17/`). Baseline at HEAD = **0 findings**; table sha256 matches the `expected.json` pin (`7994eec7…`). The matrix is a semantics replay of the committed gate, not an execution of the r17 `measure.py` (not yet written).

| candidate move | findings |
|---|---|
| **A. in-place append on `:35`** (token + cell clauses; line count unchanged) | **0** |
| B. Knowledge-table row inserted after `:153` | **4** `citation_dead`: `sc69-readme-177`, `readme175-sc1217`, `readme175-r7range`, `readme175-r8e2` |
| C. standalone coverage-map row before `## Knowledge` (after `:68`) | **5** `citation_dead`: the four above + `sc72-readme-nitrow` |
| D. split `:35` into two physical lines | **5** `citation_dead`: same set as C |
| E. Frontier bullet appended after `:181` | 0 |
| F. Known-gaps bullet appended at EOF (after `:190`) | 0 |
| G. in-place reword of `:175` preserving the needles | 0 |

A full draft of A (token + state-cell clause + method-cell clause) simulates to 0 findings, line length 1,505, line count 190 unchanged, and coverage-map mapped tokens **94 → 95**.

## Why `:35` is the host

- It is the Go-lineage row: `2026-10-13-r4-10-real-version-pair`, `2026-10-20-r14-go-version-diagnosis`, `2026-10-20-r15-go-snapshot-inventory`, `2026-10-20-r16-go-selection-preview` (`corpus/README.md:35`). r17 is the observation leg of the same r14→r16 source-model chain; appending at the end preserves chronology.
- The move is already settled twice: `corpus/lessons/round-16.md:97` — "The token/command now extend the existing Go row at line 35, keeping subsequent pinned line numbers stable and the new knowledge token mapped"; `LOG.md:1985-1988` records the same integration correction. The r14/r15/r16 commits made only in-place, line-count-neutral edits: r14 changed `:35` and `:140` (the r4-10 Knowledge row's source cell), r15 and r16 changed only `:35` (`git show 3e99fbd|856d193|27b8fc1 -- corpus/README.md`).
- The failure mode is a committed lesson: `corpus/lessons/round-12.md:20` — a standalone README row above `## Frontier` at `4072ebb` produced 5 `citation_dead`, and the fix was to remove the row, because `SCORECARD.md:69`'s stated `corpus/README.md:180` cannot be rewritten.
- Mapping instrument (OBSERVATION, `.ufo/waves/round-16/measure.py:34,80,89`; r17 contract `.ufo/waves/round-17/contract.md:119`): tokens are collected only inside the delimited `## Coverage map` section. HEAD census = **94 knowledge files / 94 mapped, `missing:[]`, `dangling:[]`**. Adding the r17 file plus a token on `:35` simulates to 95/95, still empty both ways. A Knowledge-table-only token would be invisible to that measure and would shift lines anyway.
- The Knowledge table is a **subset**, not a completeness rule: 15 of 94 knowledge files have no Knowledge-table row today — including `2026-10-20-r15-go-snapshot-inventory`, `2026-10-20-r16-go-selection-preview`, `2026-10-20-r14-go-version-diagnosis` (the r14 token rides on `:35` and its citation sits in the source cell of `:140`, but it has no Knowledge row), `2026-10-18-arc2-r7-pe-wall`, and the arc3 EVM/id entries. So r17 owes no Knowledge row; adding one is pure line-shift risk (row B).

## Frontier specifically

There is no Go bullet in `## Frontier` (`:170-181`), and no r17 token belongs there: the frontier list carries no per-entry index and the pointer table has no frontier pin for it. If L1 decides the out-of-range bootstrap result opens a frontier line, the **only** pin-safe insertion is after `:181` (after "Blocked-on-operator", before `## Known gaps` at `:183`) — measured 0. Any earlier insertion shifts `:175`/`:180` and reddens four to five entries. Prefer no Frontier change: the r17 claim is a depth/capability move, and `corpus/README.md:35`'s clustered ledger already records the Go lineage.

## Coupled hazards for L1 integration

- **Capability row placement (SCORECARD).** The C2 capability ("retained REA Ghidra-session log capture") must be added as an append-only EOF section, per the r13/r14 precedent — `SCORECARD.md:2131` and `:2136` ("This is an append-only capability record; the earlier line-addressed summary table is unchanged"), `:2203`. Inserting into the `## Capabilities` table (`SCORECARD.md:615-625`) would shift `:1216` and redden `readme175-sc1217`. Appending at EOF also leaves `SCORECARD.md:69`/`:72` untouched.
- **Same-commit ordering.** The token and the entry file must land in one commit: the measure grades a revision, so token-first reads `dangling` and file-first reads `missing`. This also satisfies the row rule at `corpus/README.md:8-9`.
- **No README Lessons row.** r14/r15/r16 added none; a lessons-index row would be an insertion above `## Frontier` (the round-12 defect). The round's lesson lives in `corpus/lessons/round-17.md` (contract) and needs no README row.

## Calibration notes

- `SCORECARD.md:1216`'s "pre-fall wall text (R2 — next README-touching round)" is **historical, not an open r17 obligation**: it was discharged at arc2-loop1-round9 by same-line rewords (`SCORECARD.md:1230-1236`: "Same-line rewords, zero shift; stale-wall-state rows 2 → 0"), and `README:175` was re-pointed `:1217`→`:1216` at round 10 (`LOG.md:1371`). Do not re-open it as an r17 claim.
- Draft clause for `:35` (write only after `W/runs/*/receipt.json` exists): cell 2 `; r17 retains REA analyze-session Ghidra analyzer logs for pinned Go carriers and grades source-model predictions field by field against observed diagnostics`; cell 3 `; r17 retained analyze-session log copies plus prediction/observation comparison in `.ufo/waves/round-17/runs/``. Keep cells pipe-free; measured clean at 1,505 chars.
- Pilot cross-check (OBSERVATION, `.ufo/waves/round-17/pilot/shfmt-log/ghidra.log`): `Untested Go version [1.27.0]`, `Missing Go bootstrap type info`, `GolangSymbolAnalyzer`/`GolangStringAnalyzer` errors. An observed-diagnostics clause is defensible, but the final wording must cite the retained receipt runs, not the pilot (pilot README states pre/post pins were not recorded).

## Residual risk / verification gaps

- The r17 `measure.py` is unwritten; the 94→95 and `missing`/`dangling` figures reproduce the committed probe plus r16 measure semantics (INFERENCE for the future instrument; OBSERVATION for the committed ones).
- The gate itself was replayed function-by-function from the committed module, not invoked end-to-end via its CLI; the CLI adds only the table-digest preflight (digest verified equal) and reporting.
- `readme38-arc3r1-token` is line-free, so no pin constrains `:38`'s line number; the only file-level obligation is that the EVM token survives, which the `:35` edit does not touch.
