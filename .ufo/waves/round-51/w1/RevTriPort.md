# RevTriPort — R51-C2 port-fidelity review

Verdict: checklist delivered; recommend pre-freeze contract clarification, not admission of a v6 implementation.

## Findings, severity order

1. **High: before-arm preflight contradiction.** `plans/round-51-claims.md:128-135,157-159` requires the same freeze-bearing command at the old base, but `tools/round-50-c3/sqfs-triage-v5.py:1257-1263` rejects that future/nonancestor freeze with exit 2. Amend and freeze distinct, explicitly bound before/after invocation semantics; do not broadly bypass ancestry.
2. **High: a mechanical port can falsely claim the stronger conjunction.** v5 `run` gates success only on pair agreement/coverage (`tools/round-50-c3/sqfs-triage-v5.py:1365,1410`), dispatches selftest separately (`:2285-2295`), and only reports drift (`:1252-1281`). v6 must actually gate audits/census/selftest and refuse frozen drift, not merely print fields.
3. **Medium: 126-member and metric-schema claims need explicit binding.** v5 accepts any nonempty envelope directory (`tools/round-50-c3/sqfs-triage-v5.py:1212-1229,1283-1285`); mismatch/missing fields are lists (`:1355-1359`), not numeric zeroes. Preserve pair/action semantics and bind the exact frozen population; clarify count/list interpretation.

## Deliverables and evidence

- Full MUST-preserve list, all 18 static selftest cases, seven textual mutations plus blanked-cell witness, exact six-part MUST-change list, and source file:line citations: `.ufo/waves/round-51/w1/RevTriPort/checklist.md`.
- Exact git-read argv, exit code, stdout sha256, UTC, static case inventory and 13 outside-census path identities: `.ufo/waves/round-51/w1/RevTriPort/inspection.json`.
- Assignment-base static source inspection: registry 55, frozen census 42, outside 13. This corroborates the declaration at the assignment base, not a runtime score at the older declared measurement base.

## Residual risk / verification gaps

No integrated candidate v6 was reviewed; this seat compares the assigned v5 source against R51-C2 requirements. No scoring, selftest, mutation execution, REA, reader runs or downloads performed. LSP unavailable: `read xd://lsp` returned `No such tool`; literal reads/static AST fallback only, no semantic-reference proof. No tools installed, no scratch created, no scratch cleanup needed, no lane source or git state changed. L1 should run the canonical frozen instrument's before/after arms, identity-bound 126-member scoring, receipt writer, H1 both-column cases, audit/census deletion controls and frozen-byte drift control.

## Self-evaluation

Accuracy 4/5: source and base-object evidence, but no runtime confirmation. Completeness 4/5: every requested checklist axis covered; landed implementation is outside this comparison. Clarity 4/5: long checklist uses explicit V/C/M file aliases. Actionability 5/5: per-item source anchors and discriminating handoff checks. Conciseness 4/5: inventory is intentionally detailed for port auditing. Overall 4.2/5. Highest-impact improvement is L1's canonical before/after/control exercise after the contract is unambiguous. User-agreement self-check: this is a source-grounded BUILD-wave checklist, not a claimed pass.
