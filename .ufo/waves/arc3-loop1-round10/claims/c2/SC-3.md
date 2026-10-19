# SC-3 — C2 depth claim

Disposition: **rule #16 draft; not integrated into `SKILL.md`.** No shared or tracked source file was changed.

## First-hand re-derivation

Re-ran Command A's source-derived measurement (`SCORECARD.md:88-124`) against immutable HEAD `5694506a862c32d2f7aac44935778bce4b6184f2`. Exact output:

```json
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "5694506a862c32d2f7aac44935778bce4b6184f2", "rule_blocks": 15}
```

I independently checked the candidate dependency examples from Git objects, not by carrying forward earlier seat metrics:

- **r4 F5b/C1 dependency — REPRODUCED.** `git diff-tree --no-commit-id --name-status -r 40de38343398eee72aeebad7429f3bb99ab0a8dd -- PROVINCE.md corpus/README.md corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md` returned `M PROVINCE.md`, `M corpus/README.md`, and `A corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md` in the same commit. The `PROVINCE.md` hunk changes the EVM Frontier clause to name the r4 Vyper carrier, while the new r4 entry records that its scope sentence was contradicted by the same-commit promotion and needed alignment (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:51-56`).
- **r8 receipt/extension/re-anchor dependency — REPRODUCED.** `git diff-tree --no-commit-id --name-status -r 53fcf0caca7255f730fe1a1f17aefd00203a2978 -- .ufo/gates/c1-census-v10.py .ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt PROVINCE.md corpus/README.md corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md` returned, in that commit, `M` for the gate and `PROVINCE.md`, plus `A` for the receipt, coverage-map update, and corpus entry. The gate diff makes pointer collection unconditional; the receipt records the target pointer; `PROVINCE.md` moves the re-anchor from `:3546` to `:4126`. The corpus entry explicitly says the post-landing count requires both entry and map token and a Command A rerun at that revision (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:17`).
- **Citation shape — VERIFIED.** The two corpus references below resolve under Command A's citation pattern and each cited range is within the file. In-memory projection using the same `rule_blocks` split and citation resolver yielded `base rule_blocks=15 citation_resolved_rules=15`; with this proposed block appended, `projection rule_blocks=16 citation_resolved_rules=16`. This is a projection only, not a claim that HEAD contains rule #16.

## Rule #16 draft

- **Same-tree dependencies land as one coupled claim.** Before integration, name each sibling artifact whose presence makes the conclusion true; land the dependent artifacts together and run the claim's check against that exact commit. If a dependency is absent or the evidence/check comes from a different revision, mark the dependent conclusion UNVERIFIABLE/UNEVALUABLE—not PASS—and rerun after repair. A prior receipt or census does not transfer across the landing boundary (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:51-56`; `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:17`).

## Citation list

1. `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:51-56` — same-commit promotion made the entry's flat scope statement false; the entry records the necessary alignment.
2. `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:17` — a landing-dependent count is not established until both the corpus entry and map token land and Command A runs at that revision.

## Verdicts

- Existing `rule_blocks=15` at HEAD: **VERIFIED** by the Command A output above.
- Coupled landing as an earned rule: **REPRODUCED** from the r4 and r8 commit trees and cited corpus lines above.
- Proposed citations: **VERIFIED** against Command A's filename/range resolver; projection is `16/16`.
- Actual integration and post-landing `16/16`: **UNVERIFIABLE** until an integrator lands the rule and reruns Command A on that commit.
