# SC-1 — C2 queue-drain rule #16 draft

**Disposition:** rule text and citations prepared for integration; this seat did not edit `SKILL.md` or claim a landed rule. All write activity for this task is limited to this artifact.

## Re-derived evidence

- **REPRODUCED — Command A at HEAD.** Ran the source-derived control recipe in `SCORECARD.md:88-123` against immutable Git objects at `5694506a862c32d2f7aac44935778bce4b6184f2`:
  ```json
  {"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "5694506a862c32d2f7aac44935778bce4b6184f2", "rule_blocks": 15}
  ```
- **REPRODUCED — Command A at the named work commit.** Re-ran the same recipe at `eb5a2c4af9d910bb7a3d4fced780f4641e341a24`:
  ```json
  {"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "eb5a2c4af9d910bb7a3d4fced780f4641e341a24", "rule_blocks": 15}
  ```
- **VERIFIED — r4 dependency.** The r4 cross-chain record says the correct F5b wording depends on whether C1's Vyper corpus entry lands in the same commit; without it the wording must be narrowed (`.ufo/waves/arc3-loop1-round4/claims/c2/verdict.md:313-335`). The C1 entry records its bounded scope and a same-landing correction (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:30`, `:34-57`). This verifies the dependency, not any prior seat's quantitative probe result.
- **VERIFIED — r8 dependency was declared; UNVERIFIABLE — its final joint landing from the seat record.** The frozen r8 claim requires the live PROVINCE pointer, receipt, and C1 extension to land together (`.ufo/waves/arc3-loop1-round8/claims-frozen.md:39-45`). CR-2 explicitly says it cannot attest the combined landing (`.ufo/waves/arc3-loop1-round8/claims/c2/CR-2.md:3,11,61-63`). Separately, the r8 corpus draft says its entry and map token both need to land before Command A can establish the after-count (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:17`).
- **VERIFIED — proposed corpus citations resolve at HEAD.** The independent `git show HEAD:<path>` line-range check returned:
  ```text
  corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:30-30 lines=63 => RESOLVES
  corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:34-57 lines=63 => RESOLVES
  corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:17-17 lines=17 => RESOLVES
  corpus/knowledge/2026-10-13-ghidra-install.md:71-76 lines=76 => RESOLVES
  ```
  The last citation records a corpus correction and its coupled PROVINCE repair in one commit (`corpus/knowledge/2026-10-13-ghidra-install.md:71-76`).

## Proposed Queue-drain craft rule #16

> - **Dependency-coupled claims close only on one verified landing.** When a queue repair's truth depends on a sibling artifact being present or aligned, name the dependency and its required artifacts in the claim, then land the complete set in one commit. Verify the combined committed tree, including the dependent claim and each required corpus, map, gate, or receipt artifact. Until that check succeeds, leave the dependent item open or narrow its wording to what has actually landed; a promised sibling change is not evidence. The r4 F5b wording depends on the C1 Vyper entry (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:30`; `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:34-57`), while r8 records a draft entry/map pair whose count is not established until both land (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:17`). A cross-file corpus correction and its PROVINCE repair were likewise recorded as one landing (`corpus/knowledge/2026-10-13-ghidra-install.md:71-76`).

## Citation list and primary records

- `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:30,34-57` — bounded C1 result and same-landing correction; pair with the explicit F5b dependency at `.ufo/waves/arc3-loop1-round4/claims/c2/verdict.md:313-335`.
- `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:17` — entry/map pair is still a draft until both land and the measured count is rerun; the receipt/extension requirement is recorded at `.ufo/waves/arc3-loop1-round8/claims-frozen.md:39-45` and `.ufo/waves/arc3-loop1-round8/claims/c2/CR-2.md:3,11,61-63`.
- `corpus/knowledge/2026-10-13-ghidra-install.md:71-76` — independent corpus record of a coupled correction.

## Falsifiable integration check

At the measured before revisions, Command A reports `rule_blocks=15` and `citation_resolved_rules=15`. After integration, rerun Command A on the exact committed revision: the proposal is supported only if `rule_blocks=16` and the new rule's corpus citations resolve. **UNVERIFIABLE as an after-measurement here:** this seat is authorized to submit the draft artifact only, not to edit `SKILL.md` or claim the integration commit.
