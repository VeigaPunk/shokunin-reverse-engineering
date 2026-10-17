# CB2 — append-only attacker (both lanes' errata)

## CLAIM
Both lanes' errata converge on substance but carry five landing hazards: heading forms, a rewrite instruction, a mislabeled count, a line-shifting README edit, and newline-fragile PROVINCE mechanics.

## METHOD
Read-only at cfc84c2 (`git show`). Primary sources: the seven targets, SCORECARD.md (:16-17, :92-123), LOG.md:385-405, SKILL.md; then all Lane A and ~20 mid-flight Lane B reports. Receipts: hex recompute (0x1c01dc8=29,367,752 B; 0x505b000=84,258,816 B); X1 matcher repro; PROVINCE byte-2961 check. No probes/MCP/network; only this file written.

## FINDINGS
1. **Headings.** Firmware's errata norm is top-level (`## Errata (round 6, …)`, r4u-01:114); R7.md:17 lands `### Erratum` (nests under it); G2.md:10/V2.md:15 are headingless. r9-02 has no `###` (all `##`, :3-:352): V5.md:12/D5.md:11 `### Erratum` nests under `## Census note` (:352); G5.md:10 headingless. Standardize top-level `## Errata (luna-round-5, 2026-10-16, append-only)` (D1/G1/VB1 form); "round 5"/"round 5 audit" (V1.md:13; D2.md:11) collides with fleet-round naming (no "luna-round" errata label exists yet).
2. **Rewrite/label.** V7.md:10 instructs "replace 'exactly two'" — an in-place-edit instruction; existing :99-104 only supersedes; must not land. P0.md:16 says "four variance classes/seven values"; r12-01:99-101 says "two classes across FOUR sites … 7 values" — don't propagate P0's wording.
3. **README shift.** D4.md:8 deletes :163 "with no replacement line" — the only line-count-changing edit; :164-173 shift up, re-pointing LOG.md:685 (`README.md:169`) and corpus/lessons/2026-10-15-round-1.md:37 (`:164`); these cites are baseline-relative by convention (SCORECARD.md:16-17) and LOG.md is append-only. Same-line retirement (CB11 agrees) or a recorded shift is required. SCORECARD.md:68-72's :128/:160 already mispoint to :131/:163; :23's `README.md:11-60` stops short of the r14-02 row at :61.
4. **PROVINCE.** SCORECARD.md:45 (`PROVINCE.md:68-73,144-153`), :79 (`:107-109`), SHONEN.md:12 (`:88-109`) cite ≥ :34. F3's byte-2961 point is the blank line before `## Core`; an added newline makes 155 lines 156 and breaks all three. Land same-line in the :28-33 paragraph (DB3.md:8). :26's self-cite `HEAD:PROVINCE.md:19-26` stays valid.
5. **r9-02 text.** V5/D5/G5 embed bare self-line cites (:7-8, :215-216, :326-335) — correct at HEAD and append-stable, but unmatched by landed errata in these files; V5/D5 fail X1's predicate (needs "does not establish"; VB5.md:11). X1's SIZES matcher cannot pass comma-grouped decimals (repro `False`); fix the matcher, not the style (:41/:49).

## THREATS
Drafts, not landed; pins valid only at cfc84c2; no live verification; Lane B mid-flight.

## VERDICT
FINDING: heading levels/labels, V7's "replace" and P0's count wording, the README:163 shift, the newline-fragile PROVINCE insert, and r9-02's guard-failing wording.
