# SC-2 — c2 depth: queue-drain rule #16 draft

**Status:** artifact-only draft for parent integration. No `SKILL.md` edit was made; the frozen write scope permits this artifact only. The baseline and supporting records below were re-derived from `HEAD`, not taken from a prior seat's output.

## Rule draft

Append this as one bullet immediately after queue-drain rule #15:

- **Co-land every truth dependency.** Before repairing a statement whose truth depends on another deliverable, name the dependency in the patch or claim (for example, a corpus entry ↔ its map token, or a receipt/pointer ↔ an instrument extension). Until every side can land together, keep the dependent statement conditional or defer it; a scratch projection is not a landed result. Land the dependency set in one commit, then rerun the named acceptance check against that commit and record the measured revision. In r4, F5b's Vyper wording depended on C1's corpus entry (`.ufo/waves/arc3-loop1-round4/claims/c2/verdict.md:332-335`); in r8, the pointer and receipt were required with C1's `ptr_check` extension (`.ufo/waves/arc3-loop1-round8/claims-frozen.md:39-50`). Corpus precedents: `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:51-57`, `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:5-6`, and `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:17`.

## First-hand re-derivation and verdicts

- **Current baseline — VERIFIED.** Ran Command A from `SCORECARD.md:93-123` against immutable `HEAD` (`python3 - HEAD`). Exact output:

  ```json
  {"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "HEAD", "rule_blocks": 15}
  ```

  `git log -1 --format='%H %s'` returned `5694506a862c32d2f7aac44935778bce4b6184f2 arc3-loop1-round9: records — SCORECARD round section, LOG entry, round report + scope re-key to EOF (measured at work commit eb5a2c4)`.
- **r4 F5b ↔ C1 dependency — VERIFIED.** The r4 c2 verdict states the F5b wording depends on whether C1's corpus entry lands in the same commit (`.ufo/waves/arc3-loop1-round4/claims/c2/verdict.md:332-335`). `git show --format='commit %H%nsubject %s' --stat 40de383 -- PROVINCE.md corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md` returned commit `40de38343398eee72aeebad7429f3bb99ab0a8dd`, subject `arc3-loop1-round4: work — Vyper knowledge entry (arc3-r4), PROVINCE 9-row same-line repair (162 held), ghidra erratum, r3 entry correction`; its changed-file list includes both `PROVINCE.md` and the r4 knowledge entry. The corpus erratum records that the entry's old no-Core-promotion scope sentence was contradicted by the same commit's PROVINCE promotion (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:51-57`).
- **r8 receipt ↔ extension dependency — VERIFIED.** The frozen r8 claim says the pointer update and receipt must land in the same commit as C1's instrument extension (`.ufo/waves/arc3-loop1-round8/claims-frozen.md:39-50`); C2's seat independently records that same-commit condition as unverifiable from an artifact-only seat (`.ufo/waves/arc3-loop1-round8/claims/c2/EX-6.md:5-9`). `git show --format='commit %H%nsubject %s' --stat 53fcf0c -- .ufo/gates/c1-census-v10.py PROVINCE.md .ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt` returned commit `53fcf0caca7255f730fe1a1f17aefd00203a2978`, subject `arc3-loop1-round8: work — ptr_check extension landed on live :4126 anchor (gate + scope re-key + PROVINCE re-anchor + receipt, coupled), Vyper optimizer-forms entry (86->87)`; its changed-file list includes the gate, PROVINCE, and receipt.
- **Draft citation ranges — VERIFIED.** Checked the proposed corpus references against immutable `HEAD` with `git show HEAD:<path>` and line-range bounds. Exact output:

  ```json
  [{"lines": 63, "path": "corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md", "requested": [51, 57], "resolves": true}, {"lines": 17, "path": "corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md", "requested": [5, 6], "resolves": true}, {"lines": 17, "path": "corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md", "requested": [17, 17], "resolves": true}]
  ```
- **Draft parser projection — REPRODUCED (in-memory only).** I inserted the draft bullet into `HEAD`'s queue-drain section in memory and ran Command A's rule-splitting and citation-range logic. Exact output: `{"before": {"citation_resolved_rules": 15, "rule_blocks": 15}, "draft_projection": {"citation_resolved_rules": 16, "rule_blocks": 16}, "projection_only": true, "source_revision": "HEAD"}`. No source file was written by this projection.
- **Rule #16 landing / after-count — UNVERIFIABLE here.** This seat is prohibited from editing `SKILL.md`; no post-integration `rule_blocks=16` measurement is claimed. Parent acceptance check: apply the draft as exactly one new bullet, then rerun Command A at the landing revision and require `rule_blocks=16` and `citation_resolved_rules=16`.

No discrepancy found in the re-derived baseline or the dependency examples. The new rule is a proposed craft improvement, not a claim that the source skill has changed.
