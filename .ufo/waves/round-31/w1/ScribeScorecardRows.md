# Round-31 SCORECARD rows — scribe report

## Findings

1. **Observed — recipe A at `c369242fee9f559f895e3f7956b1242076c7b1be`.** I copied the Python block from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md:92-123` to `/fast/scratch/hyaku/kaidoku-r31/seats/w1/scribe-scorecard-rows/recipe-a.py` and ran it from the lane repository. The status-capturing invocation was:

   ```text
   timeout 300 python3 /fast/scratch/hyaku/kaidoku-r31/seats/w1/scribe-scorecard-rows/recipe-a.py c369242fee9f559f895e3f7956b1242076c7b1be | tee /fast/scratch/hyaku/kaidoku-r31/seats/w1/scribe-scorecard-rows/recipe-a.json; rc=${PIPESTATUS[0]}; printf 'EXIT_CODE=%s\n' "$rc"; exit "$rc"
   ```

   **Full stdout:**

   ```json
   {"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 116, "mapped": 116, "missing": [], "revision": "c369242fee9f559f895e3f7956b1242076c7b1be", "rule_blocks": 17}
   EXIT_CODE=0
   ```

   **Exit code:** 0. **UTC output-capture time:** the output file mtime was `2026-10-23 01:10:20.927783766 -0300` (`2026-10-23T04:10:20.927783766Z`); this timestamps the captured output, not the process start. The first invocation printed the same JSON without an explicit status line; this second invocation captured the raw JSON and explicit status. The recipe used read-only `git ls-tree` / `git show` against the requested revision.

2. **Drafts — not applied to SCORECARD.md.** The proposed replacement cells and round-31 lowest-axis line are recorded verbatim in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/scribe-scorecard-rows/scorecard-cell-drafts.md`:

   - Coverage score: `9.72 → 10.0`.
   - Coverage observable/limitation: `116/116 knowledge files mapped at `c369242fee9f559f895e3f7956b1242076c7b1be` (round 31); index integrity only, **not** fraction of the REA domain held. History: 78/78 at `3395b6d` (luna-round-7; the row kept that revision until round 26), 107/107 at `7ef837a473ae65d924b9ea34e7748f722a6cd7d5`, 108/108 after the round-25 EVM selector-naming entry`.
   - Depth score: `10 → 10`.
   - Depth observable/limitation: `17/17 queue-drain rule blocks have resolvable file/range citations at `c369242fee9f559f895e3f7956b1242076c7b1be` (round 31). History: 9/9 at `638fb211` (luna-round-3); rule blocks grew from 9 to 17 in eight commits from `58116aa1` to `4072ebb3` (2026-10-18 and 2026-10-19), and the row kept 9/9 until round 25 added a recount at `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76`. **not** semantic correctness, generality, or fresh execution — the r3 semantic contradiction removal is measured by the contradiction census, not this proxy`.
   - Round-31 section line: `Lowest-axis basis: coverage, depth and calibration are tied at 10; none is retired, so either claim satisfies the rule.` This lowest-axis statement is drafted from the assignment-provided basis; recipe A did not measure calibration or retirement status.

## Gates and scope

- Recipe A was the only measurement run; it completed with exit 0. No tests, recipe B, REA invocation, or external-source fetch was run. No tool was installed or updated.
- The recipe's counts establish the coverage-map and citation-resolved-rule proxies only. The draft retains the existing limits: map integrity is not the fraction of the REA domain held; depth citations do not establish semantic correctness, generality, or fresh execution.
- No lane file other than this assigned report was written. `SCORECARD.md` remains unchanged; only the specifically requested draft text is supplied. The existing Evidence/counting-command column and all other scorecard content were not changed.

## Touched surfaces and artifacts

- Report written: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/w1/ScribeScorecardRows.md`.
- Scratch artifacts (all under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/scribe-scorecard-rows/`):
  - `recipe-a.py` — copied recipe; SHA-256 `236dde1da2d78b5ee2f4827fb884901857385fe1f40bbb09bbb4b4ab4f6e9b01`.
  - `recipe-a.json` — captured stdout; SHA-256 `7c1abf92407609bf34bb1b261e1a6954273b978f92ea68fbf3b8179ced79932d`.
  - `scorecard-cell-drafts.md` — drafted cells and section line; SHA-256 `f2745a13cca1ee4aaa42074b79190e55442e8ff90c191a7684c6c4fdee4fb09f`.

Report: .ufo/waves/round-31/w1/ScribeScorecardRows.md
