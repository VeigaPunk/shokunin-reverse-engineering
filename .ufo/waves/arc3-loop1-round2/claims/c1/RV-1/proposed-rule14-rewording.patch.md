# RV-1 measured rewording of rule #14 (proposal, NOT applied)
# Rationale: EX-01's text (a) attributes the stale numbers to the entry instead of the patch text's verification block,
# (b) bounds the duty to an artifact's OWN bytes while the measured case is a claim about the bytes it produces, and
# (c) names the recheck line as the churn cause (measured cause: path-style edits; recheck fix landed later).

## candidate text
- **An artifact that records a byte-identity — its own, or of the bytes it produces and lands — must re-derive that identity after every revision; a stale identity voids the verification block, not the work.** The C1 entry's patch text claimed 8,316 B / `f95c5a05…` in its "Verification performed" block while the bytes its hunks produced hashed 8,598 B / `d8d85949…` (`.ufo/waves/arc3-loop1-round1/seats/CR-2.md:86-89`), re-measured at 9,513 B by the convergence seat (`.ufo/waves/arc3-loop1-round1/seats/VZ-1.md:115`). The correction is a fresh measurement of the landed bytes, recorded by the integrator at landing (10,225 B / `dd986f56…` — `SCORECARD.md:1366-1368`; `LOG.md:1411-1412`); the landed entry is the subject whose identity moved (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:7`). Never a revert, never a carried-over number.
## measured on a fresh HEAD tree (rule inserted after line 239)
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "rule_blocks": 14}
rule14 {'bad': [], 'refs': 1, 'rule': 14, 'valid': True}
census v10: VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0) (exit 0)
needle scan: added_lines=2 needle_hits=0
prior-13 byte-identical: True
SKILL.md post-image sha256: cfb87fcce060f3a74d72e8351886e2ab5af0ddd0c89dd35cc5bd289a93ee22c2, 373 lines
