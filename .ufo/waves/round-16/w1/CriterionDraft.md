# CriterionDraft report — kaidoku round 16, w1 (QUALITY #18)

Artifact: `.ufo/waves/round-16/w1/CriterionDraft.candidate.md` (draft row #18 plus grounding notes). `corpus/QUALITY.md` and all other existing docs were read only. Nothing executed: no gate, selftest, probe, measure script, or recount was run. Claims below are read from committed bytes and retained argv records.

## Findings

1. **Routed defect 1 (argv vs guidance) is real but narrower than stated.** `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:3` recheck omits `-I` and uses a relative script path. In `.ufo/waves/round-15/verification.json`, 7 of 10 `python3` argv entries use `-I` with an absolute path. The 3 without `-I` are `measure-before`, `measure-after`, `citation-strict`. `final-recheck.json` also runs `measure.py` and the citation probe without `-I`. The closure's "retained execution uses `python3 -I`" describes only the inventory and quote-fidelity runs. Row #18 therefore requires per-invocation argv.
2. **Routed defect 2 (registry discoverability) is confirmed.** `SKILL.md:450` (quote-fidelity row, pinned-values cell) names only `.ufo/waves/round-14/fixtures/expected.json`. The supplemental baseline `.ufo/waves/round-15/boundary-fixtures/expected.json` is pinned in `.ufo/waves/round-15/measurement-pins.json:4` and checked by `no-harm-controls.json:27`. Its frozen run is the argv labelled `boundary-frozen` in `verification.json`. The row needs the path and pin location; no gate change.
3. **Routed defect 3 (producing command) is confirmed, with a sharper gap.** `.ufo/waves/round-15/no-harm-controls.json` has no command field. `row16_unchanged`, `append_only`, `pins_match` have no producing command in any committed file; the closure describes them as reproduced from Git objects (`corpus/lessons/round-15-verifier-spotcheck.md:139-142`) without a snippet. Craft counts have a snippet only in the closure lesson (`:143`, and recount block `:97-115`). Round-14 `command-a-control.json:2` stored a prose command, which #18 excludes as an argv.
4. **Existing criteria do not cover this.** #6 requires a reproducing call for REA-drawn claims; #13 requires the verify command for minified-file counts to reproduce itself. Neither requires registry pin completeness or per-value producing commands. #18 extends them; it supersedes neither.
5. **Round-16 lesson is not yet on disk.** `corpus/lessons/` contains round-15 and earlier only. Row #18 cites `.ufo/waves/round-16/claims.json` C2 and marks the round-16 lesson path as pending. L1 should re-check the citation once the lesson lands.

## Scope and calibration

- #17 is unchanged; #18 is a new row, appended after 17 by L1.
- Routed defect 4 (SHONEN wording) is outside QUALITY and was not drafted.
- The append-only correction for the round-15 `recheck:` line and the registry row amendment are integration work for L1 or the lesson drafter; this report does not apply them.
- Confidence: high that the argv inventory above is what `verification.json` records (read from parsed JSON via `jq`, not re-run). Medium on the wording's ability to hold for future rounds: it depends on L1 applying the append-only route.
- `-I` effect on output was not tested. The draft treats it only as part of the recorded invocation.

## Limits

- No execution: argv records are claims about past runs, not reproduced now.
- sha256 values quoted from pin files were not recomputed.
- The recheck line in knowledge entries was not run.

## Tool installs/updates

None. Read-only `jq` and `grep` on committed artifacts; no package changes.
