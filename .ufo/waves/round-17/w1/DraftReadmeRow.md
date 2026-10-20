# Round 17 w1 — DraftReadmeRow report (author-side advisory, leaf seat)

Scope: exact `corpus/README.md` coverage-map row for the r17 Go token that keeps citation-drift pins fixed, plus any `## Frontier` change. Draft: `.ufo/waves/round-17/w1/draft-readme.md`. No repo file edited; `corpus/README.md` untouched (clean at HEAD `b563c79`).

## Result

- Coverage map: add the r17 token **in place on line 35** (Go row, cell 1), with cell 2/3 clauses appended. No line is added; no pinned line moves. Drafted as S1–S3 in `draft-readme.md`.
- Frontier: one bullet **appended after line 181** (new line 182). Lines 170–181 are not edited.
- Gate: apply only in the landing commit that adds `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` (README rule `corpus/README.md:8-9`). Placeholders `<R17-VERDICT>` and `<R17-RECEIPT>` are filled from the landed entry only.
- No Knowledge-table row for r17 (precedent: r14–r16 Go entries have none).

## Evidence (observations)

- Pinned README lines in `.ufo/gates/citation-drift/pointer-table.json`:
  - `corpus/README.md:22` — `readme22-r7range` / `r8range` (file key :170, :182).
  - `corpus/README.md:175` — `readme175-sc1217` / `-r7range` / `-r8e2` (file key :208, :219, :231).
  - `SCORECARD.md:69` cites `corpus/README.md:180` (`held, not frontier`), pattern at pointer-table.json:57 (`sc69-readme-177`).
  - `SCORECARD.md:72` cites `corpus/README.md:138` (`4 nits: 2 fixes applied at integration`), pattern at :68 (`sc72-readme-nitrow`).
  - `readme38-arc3r1-token` (:407) is an anchor with the line deliberately unpinned; `corpus/README.md:38` in `exempt` is a round-record pin (not graded).
- Pointer-table digest `7994eec7e764e8c3195dd79efb850b63d437aa610e6a9d96ed24484bb53789d1` matches `expected.json` `pointer_table.sha256`.
- Baseline probe run (read-only, Git objects, no writes): `python3 -I .ufo/gates/citation-drift/citation-drift-probe.py --root <repo> --rev HEAD` → `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`.
- Precedent for this exact failure: `corpus/lessons/round-12.md:20` (row 9): a row inserted above `## Frontier` produced 5 `citation_dead` (including `sc69-readme-177` and `readme175-*`), and the SCORECARD cite could not be rewritten (append-only).
- Line 35 (`corpus/README.md:35`) is the Go row; cell 1 = tokens, cell 2 = summary, cell 3 = sources. Multi-token rows are the convention (e.g., line 63, line 35 itself).
- Go source tokens present in corpus: `2026-10-20-r14-go-version-diagnosis.md`, `2026-10-20-r15-go-snapshot-inventory.md`, `2026-10-20-r16-go-selection-preview.md` (all in `corpus/knowledge/`). The r17 file is absent (`ls corpus/knowledge | grep r17` → none).
- The r17 filename is fixed by `.ufo/waves/round-17/contract.md:117` (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`).

## Simulation (in-memory, no writes; not the real probe)

Replicated the README-citing pins in Python against three candidate texts:

| candidate | r22 cite | r175 cite | sc69 → :180 | sc72 → :138 | r1-evm anchor | verdict |
|---|---|---|---|---|---|---|
| HEAD | PASS | PASS | PASS | PASS | PASS | — |
| A: in-place token on line 35 | PASS | PASS | PASS | PASS | PASS | **adopt** |
| B: A + frontier bullet after 181 | PASS | PASS | PASS | PASS | PASS | **adopt** |
| C: new coverage row after 35 | PASS | FAIL | FAIL | FAIL | PASS | reject |

Caveat: this replicates the `extracted`/`anchor` checks for the README-citing entries only; it is not the gate. L1 must run the real probe at the landing revision (draft step 2).

## Inferences (not observed)

- The real probe will report `findings=0` for candidate B, because the only pinned citing and target lines it reads (22, 138, 175, 180) keep their text and no pin references README lines ≥182. Inference from the table above plus the absence of a README pin ≥182 in the pointer table; not run.
- The Frontier bullet's "no retained Ghidra analyzer log for a Go carrier" rests on `.ufo/waves/round-17/claims.json` C2 ("one observed-not-cited log line (r4-10, log deleted)"). That claim is L1-authored; I did not verify the deletion independently.

## Frontier decision

- Add one bullet now-or-at-landing (drafted for landing with Edit 1). It names the open Go bootstrap gap, which is true before and after r17. It does not depend on r17 results, so it cannot overstate them.
- Do not alter bullet :175 (pinned) or :180 (pinned by SCORECARD:69 "held, not frontier"). Do not alter the existing r5-02/r9-02/r11-01 residue text in :180.

## Limits

- r17 results are unknown to me; S2/S3 clauses must be copied from the landed entry and receipt, not drafted.
- Simulation was in-memory Python; no citation-drift run at a new revision (not possible without writing Git objects, which the contract forbids for this seat).
- Only README-citing pins were replicated; other graded entries (SKILL/SCORECARD/LOG/knowledge) do not touch README except SCORECARD:69 and :72 (both replicated).

## Tools / installs

None. Reads and checks used `sha256sum`, `ls`, `grep`, `git diff --stat`, python3 stdlib, and the committed probe in read-only mode. No `pacman`, `uv`, `npm`, or REA invocation.

## Files

- Draft: `.ufo/waves/round-17/w1/draft-readme.md`
- Report: `.ufo/waves/round-17/w1/DraftReadmeRow.md`
- Repo files changed: none.
