# RevTriPort — port-fidelity review

Verdict: checklist delivered; freeze-text decisions required before claiming a green v6 port. This is a static recommendation, not an admission.

## Findings by severity

1. **Medium: before-arm freeze contradiction.** `plans/round-52-claims.md:203-210` requires the future freeze to be an ancestor yet requires the same command to score the earlier claims draft with exit 1. Canonical ancestor rejection in `tools/round-50-c3/sqfs-triage-v5.py:1257-1263` instead makes that invocation exit 2. Specify the before-table mode/freeze separately without disabling production ancestry gating.
2. **Medium: new registry rows require a revision-appropriate census.** Claims `190-195,233-234` inherit census3 while adding v6 (and C1 adds other rows, `175-176`). `tools/round-51/census3.py:102-115` correctly flags new registry paths missing from the old census. Explicitly freeze an exact expanded inventory/extension and retain historical before equality.
3. **Low: counting-bullet fidelity needs a claim amendment.** C2 counting bullet `plans/round-52-claims.md:230-232` lacks explicit before SHA and 1->0 audit sizes. Original guard isolates and binds the bullet itself (`sqfs-triage-v5.py:2183-2217`); retarget it to C2 rather than searching the entire document or retaining old R50 literals.

## Deliverable

`.ufo/waves/round-52/w1/RevTriPort/checklist.md`: file:line MUST-preserve inventory (H1, receipt readback, instrument hash, counting guard, 18 selftest responsibilities, 126-envelope pair semantics, exits) and exact MUST-change inventory (new row, evaluator precedence, independent audit, census3 clause, drift gate, registry).

## Residual risk and verification gaps

The old run logic records instrument/tool drift but does not gate it (`sqfs-triage-v5.py:1252-1281,1365,1410`); v6 must replace that behavior. Merely matching v6 table/evaluator pairs cannot prove executability. Corpus size 126 is a claim population, not enforced by v5 enumeration. These are integration checklist items, not assertions that an unreviewed v6 draft contains defects.

LSP unavailable: `read xd://lsp` returned “No such tool”; no semantic references/definition/diagnostics available. Source read/grep only. No scores, controls, selftests, REA invocations, downloads, installs, fixture repos, or scratch were run/created; no runtime receipt exists and none is claimed passed. All changes are the requested seat checklist/report/status only. No resume path or same-identity runtime rerouting surface exists in this assigned static port review; no saturation claim made.

Self-evaluation: accuracy 4/5 (source-grounded, no runtime evidence); completeness 4/5 (requested inventory covered, future draft not supplied); clarity 4/5 (long checklist uses explicit aliases); actionability 4/5 (concrete acceptance gates, integration still required); conciseness 4/5 (detailed 18-case inventory retained for fidelity). Overall 4.0/5. Most useful next check is L1's frozen before-arm invocation after resolving ancestry, then exact 126-pair comparison and census/drift controls. User agreement expected because limitations are explicit.
