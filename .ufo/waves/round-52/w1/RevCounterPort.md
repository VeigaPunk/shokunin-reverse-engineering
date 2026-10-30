# RevCounterPort — settled

Verdict: checklist delivered; v2 conformance is not adjudicated by this source-only assignment.

Deliverable: `.ufo/waves/round-52/w1/RevCounterPort/checklist.md` — preservation matrix, all nine original bindings with exact documentation markers, mandatory R52 deltas, 205 static named inventory rows plus dynamically generated probe expansions and separate real-REA suite requirements. Axes: semantic preservation, explicit deltas, fail-closed controls, traceable evidence.

## Findings / integration hazards (severity ordered)

1. **High — a literal port of the real-REA selftest cannot produce its intended green.** `tools/round-50/c1-counter.py:4737-4743` constructs a carrier spec without `projection`, while `:882-886` requires explicit `plus-extractor`; `:4822-4826` requires no false binding. Preserve its intended green/fabrication-red coverage, but carry the mandatory projection into the v2 fixture. Static finding; not executed.
2. **High — new landing obligations exceed the inherited binding list.** `tools/round-50/c1-counter.py:2475-2478` proves merely one matching opened source row; the nine bindings at `:432-434` do not check every named citation, fresh receipt reference, SCORECARD head or LOG entry demanded by `plans/round-52-claims.md:162-176`. Keeping these nine unchanged is not proof of every R52 landing obligation. Checklist separates preserved predicates from added derivations.
3. **Medium — retry exhaustion needs explicit frozen interpretation.** v1 `:2397-2402` maps exhausted provider_timeout to exit 2; R52 claims `:107-114` introduce eligible ENOENT retries and persisting failure/other-error red semantics. Preserve falsifiability and freeze the exact exhaustion outcome; never let a recovered attempt erase attempt diagnostics. Also `re_scored_pins` is a frozen allow-list, not a fourth boolean law clause.

## Residual risks and verification gaps

- LSP unavailable: `read xd://lsp` returned “No such tool”; no semantic references/definitions/diagnostics claimed. Direct source inspection and static AST inventory only.
- No v2 draft was assessed, no runtime invoked, no counter imported/executed, no tests/REA/downloads/probes run. No test result is labeled passed.
- V1 source SHA256 observed by static AST extraction: `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813`; extraction timestamp UTC `2026-10-30T10:48:54.007860+00:00`. The inventory is source-derived, not a runtime count.
- Same-identity rerouting, saturation and resume-continuity contracts are outside this counter-port checklist; no claims about those runtimes.
- Only assigned seat directory/report written. No scratch created, no installations/updates, no repo mutation or fixture commits.

## Self-evaluation

Accuracy 4/5: line-grounded source facts, no runtime evidence; LSP unavailable. Completeness 4/5: all requested behavior groups and static case inventory included, actual v2 verification intentionally reserved for L1. Clarity 4/5: preservation/deltas/inventory split, but inventory necessarily long. Actionability 5/5: explicit checkboxes, source lines and expected outcomes. Conciseness 4/5: substantial inventory required by assignment. Overall 4.2/5; primary improvement is L1 matching landed v2 bytes against the checklist. The user can distinguish required acceptance from observed verification.
