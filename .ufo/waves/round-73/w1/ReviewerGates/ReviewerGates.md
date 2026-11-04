# ReviewerGates scoped receipt report

Full severity-ordered findings with exact source lines and proposed fixes: `../ReviewerGates.md` (the required wave seat report).

Evidence: `counterexamples.json`; reproduction: `review-probes.py`.

Observed counterexamples: seven-atom audit accepts wrong-token correction, malformed provenance, absent population and absent round-specific receipt (0 mismatches); partial record and mutation receipts validate (rc 0), including mutation count 99 with no survivor rows; c3_no_case accepts a git acquisition failure (rc 2) without executing the fixture. A12 rejects both empty genuine and empty forged kernel samples. Forged caller-environment inheritance and strict control aggregation are supported by source inspection. Conditional A12 environment-value disclosure is identified without capturing any host values.

Recommendation: address the five high-severity and two medium-severity findings before treating these controls/validators as false-green resistant. No source changes, admission, integration or git writes were performed. No tools installed. Scratch was removed by the completed EXIT trap.

Residual risk: focused synthetic function tests and one real battery acquisition-refusal invocation are not an end-to-end landing measurement. LSP device unavailable; literal references are not semantic proof.

Self-evaluation: accuracy 4/5 (source paths and executed results recorded; no live kernel experiment); completeness 4/5 (all assigned instruments and six arms reviewed, full control execution intentionally not claimed); clarity 4/5 (finding/report split requires one cross-reference); actionability 5/5 (each finding has exact lines, evidence and a proposed fix); conciseness 4/5 (full report retains detail needed to distinguish producer from validator behavior). Overall 4.2/5. Highest-impact improvements for the integrator: repair c3_no_case's experiment routing, enforce receipt censuses, then rerun the canonical end-to-end controls. User-facing result remains a review recommendation, never admission.

Report: .ufo/waves/round-73/w1/ReviewerGates/ReviewerGates.md
