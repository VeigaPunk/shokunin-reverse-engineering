# SC-4 — C2 depth: rule #16 draft

**Disposition:** Draft only. No change was made to `SKILL.md`; this artifact proposes one queue-drain rule and its citation list for parent integration.

## Re-derivations and per-item verdicts

- **Current `rule_blocks` — VERIFIED at HEAD.** I ran Command A from `SCORECARD.md:93-123` against the immutable Git object selected by `git rev-parse HEAD` (`5694506a862c32d2f7aac44935778bce4b6184f2`). Exact stdout:
  ```json
  {"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "5694506a862c32d2f7aac44935778bce4b6184f2", "rule_blocks": 15}
  ```
- **R4 F5b↔C1 dependency — REPRODUCED as a dependency; not evidence of a combined landing.** The candidate Frontier repair says its Vyper claim must be dropped back to the solc-only form unless C1's knowledge entry lands in the same commit (`.ufo/waves/arc3-loop1-round4/claims/c2/EX-14/evidence/candidate-complete-frontier-repair.patch.md:80-90`). The corresponding corpus entry scopes the Vyper result and its remaining Unknowns (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28-30`).
- **R8 receipt↔extension — REPRODUCED as a requirement; UNVERIFIABLE as a completed combined landing.** The frozen R8 claim requires the pointer update and receipt in the same commit as C1's instrument extension (`.ufo/waves/arc3-loop1-round8/claims-frozen.md:37-45`); the R8 C2 artifact explicitly says the co-landing was not established (`.ufo/waves/arc3-loop1-round8/claims/c2/EX-5.md:73-76`). Separately, the R8 corpus draft says its post-landing count is not established until both entry and map token land and Command A reruns (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:5-17`).
- **Draft parser/citation check — REPRODUCED in memory, not landed.** Applying Command A's bullet and corpus-citation patterns to the current immutable SKILL/corpus text plus the exact draft below gives `baseline_rule_blocks=15`, `draft_rule_blocks=16`, `draft_citation_resolved_rules=16`, `unresolved_rule_indexes=[]`. The two corpus citation ranges in the proposed rule resolve at HEAD. This is not a post-landing Command A result.

## Proposed rule text

Append as one new bullet after the current Queue-drain craft rules; do not treat this draft as a source edit:

- **Declare and co-land truth-dependent repairs.** Before landing a repair, name every sibling artifact, receipt, or index that its claim presupposes. Land the dependency set in one commit, then re-run the relevant checks against that exact revision. If a member cannot land, narrow or remove the dependent assertion and record the remaining claim as `UNVERIFIABLE`; a scratch pass or proposed patch is not landing evidence. This is earned by the Frontier Vyper clause whose truth required the C1 corpus entry (`.ufo/waves/arc3-loop1-round4/claims/c2/EX-14/evidence/candidate-complete-frontier-repair.patch.md:80-90`; `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28-30`), by the R8 entry/map pair whose post-landing count was left pending (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:5-17`), and by the pointer receipt that had to co-land with the instrument extension (`.ufo/waves/arc3-loop1-round8/claims-frozen.md:37-45`).

## Citation list

- `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28-30` — scope and Unknown boundary for the C1 evidence that the Frontier assertion relies on.
- `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:5-17` — entry/map token are drafts; the post-landing count requires both plus a rerun.
- `.ufo/waves/arc3-loop1-round4/claims/c2/EX-14/evidence/candidate-complete-frontier-repair.patch.md:80-90` — explicit dependency, same-commit condition, and safe fallback for the R4 Frontier clause.
- `.ufo/waves/arc3-loop1-round8/claims-frozen.md:37-45` — the receipt and pointer re-anchor are prerequisites coupled to the instrument extension.
- `.ufo/waves/arc3-loop1-round8/claims/c2/EX-5.md:73-76` — co-landing remains unverified in that artifact; no completion is claimed here.

**Landing boundary:** The 16-block result above is a candidate-only in-memory check. Parent integration must append the reviewed bullet and rerun Command A against the actual landing revision before reporting `rule_blocks=16` as landed.