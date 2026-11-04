# ReviewerClaim — R83-C1 frozen-claim review

## Recommendation and axes

**Finite verdict: frozen predicate is coherent and calibration-grounded; no blocking defect demonstrated in that exact eight-case predicate. The target is insufficient to establish the entire declared header grammar or general attribution correctness. Candidate success is not assessed here.** Author-side recommendation only; no outside verification, admission, integration, or frontier promotion.

Axes: calibration fit; predicate/fixture identity; real-baseline fidelity; positive/negative discrimination; counter pin enforcement; honest generalization limits. Review used only read-only git operations and bounded attribution probes; no builds, linters, formatters, dispatch, installs, clones, or production changes.

## Findings, by severity

### Medium — eight-case success does not imply the stated grammar

`plans/round-83-claims.md:11` specifies arbitrary IDs of at least three ASCII digits, exactly one source field, first-twelve-line placement, and malformed-header refusal. The frozen cases (`.ufo/waves/round-83/attribution-cases.json:2-9`) do not test duplicate fields, the twelve-line boundary, or any valid queried ID other than S286/S299. This is a limit of the evidence, not a changed predicate or a failure of the literal finite target.

Exact independently exercised exploit: the deliberately inadequate review-only function in `w1/ReviewerClaim/probe.py` returns `sid == 'S286' or (sid == 'S299' and text.startswith(('source: S299 —', 'source: S286, S299 —')))`. Frozen `score` gives it **zero mismatches across all eight cases**. Yet it returns false for valid `source: S300 — primary`, true for duplicated `source: S299 — primary\nsource: S300 — secondary`, and true for S286 with no source header. These are concrete contradictory grammar behaviors; see `w1/ReviewerClaim/receipts/bounded-probe.json`. This control was never substituted for the candidate, written into a target, or committed. A thirteenth-line negative was also exercised and correctly refused by this control; it is not claimed as a successful exploit.

Keep the frozen population unchanged. Limit any success statement to that finite predicate; do not infer full grammar conformance, universal citation correctness, or saturation from eight passing observations.

### Medium — freeze and instrument pins are reported, not independently enforced

`tools/round-83/attribution-audit.py:43-60` resolves the subject revision, but fetches fixtures from caller-provided `args.freeze` and only checks length, unique IDs, and number of real flags. It reports fixture/instrument hashes without comparing them against the claims container's expected pins (`claims.json:14-20`). Therefore an alternate committed fixture set preserving eight unique IDs and two real flags could change expectations while retaining the predicate string; the counter itself would not reject that substitution. This is a static code-path finding, not a claim that an altered-freeze run was performed. No alternate commits or fixtures were created.

For this review the canonical inputs were correct: declaration `de4e58b2c22bf4376dc81bd32dfe0b9ac605e17e`; counter SHA256 `386e7891b4ffedae6f3df12c8c741e81aaa2338dfea3447dc26537f274646521`; fixture SHA256 `2066da67577812070fb93bc004bc8818b7f92b761d79fff29f2713189add441f`. Read-only diff declaration→first-container `af20aff3f72630ab1f86d69db4a423e05f563c30` was empty for plan, counter, and fixtures. Pin/command identity must be checked externally before interpreting a receipt. This report does not repair the frozen counter.

### Low — outer selftest does not independently anchor the legacy revision

`attribution-audit.py:69-78` runs both legacy and candidate targets at `args.rev`; it does not use BASE for the legacy arm and checks only rc1 plus presence of `real-withdrawn`, not the full legacy mismatch set. The proper before command is separately specified at `plans/round-83-claims.md:21`. Candidate selftest success alone cannot replace that canonical BASE measurement. This review ran the canonical BASE command separately.

## Positive checks and observed evidence

- **Calibration fit:** retained `.ufo/waves/round-82/l1/scores/c2-at-landing.json:137-145` records `entry_cites_row: true`, while `met` remains false and `SOURCED_ROW_UNMET` remains present. Actual committed BASE entry `corpus/knowledge/2026-11-04-r82-conjunction-and-printed-commands.md:1` starts `source: S286 — ...; duplicate S299 withdrawn in-round`. The discrepancy is specifically positive-attribution self-assessment versus lexical presence, not a retroactive round82 success or a newly acquired source.
- **Actual legacy baseline:** BASE `650344bc37ca303fb9487c1174192057af499b9b` contains the exact-ID regex implementation, not the earlier substring proposal: `printed-command.py:257-261` tokenizes every ID anywhere on the first source line. `sourced_arm:273-288` trusts that result for `entry_cites_row`. This explains why an exact S299 in withdrawal commentary produces true even after substring matching was fixed.
- **Measured red controls:** canonical CLI at BASE, canonical FREEZE, actual legacy target exited **1**, with exactly `real-withdrawn`, `commentary-only`, `withdrawn-head` mismatched. Receipt: `w1/ReviewerClaim/receipts/legacy-cli.json`. Independent frozen-function scoring reproduced those three; refuse-everything had exactly `real-primary`, `plain-positive`, `multi-positive` mismatches. Neither reaches target.
- **Two real cases:** `real-primary` and `real-withdrawn` are two queries against the same actual committed entry, not two independent real documents. `score:35` uses the BASE entry bytes for both. The actual entry SHA256 measured `c14b43393b85cc64275f06c00a9195fd03d0e54c4e78c01f897649096b5089ee`; S286 observed true/expected true, S299 observed true/expected false in legacy. No synthetic entry replaced that text.
- **Predicate identity and booleans:** plan line 7, claims line 10, and counter `PREDICATE` agree. `score:38` requires `type(value) is bool`; numeric 0/1 are not accepted as booleans. `run:46` requires eight unique case IDs and two real flags. Errors are rendered UNEVALUABLE/rc2 by `main:91-99` rather than a green measurement.
- **Scope honesty:** plan explicitly disclaims historical migration, source novelty, universal citation parsing, old claim repair, and frontier promotion. There are no runtime routing, resume, or `resume_continuity_v1` changes in the assigned diff; those contracts are not exercised or granted here. No saturation claim is supported or made.

## Residual risk and verification gaps

The candidate file was not present in the lane or wave directory during this review; no candidate green result, AST self-containment, candidate callsites, or candidate CLI behavior is certified. This assignment reviews the frozen plan/counter/data and actual legacy evidence. L1 must separately bind the eventual committed candidate bytes and measure the unchanged command. `load_function:21-30` executes a named AST function with Python builtins and does not sandbox decorators/default expressions or enforce its self-contained-except-re property; do not treat extraction as an execution-security guarantee. Fixture substitution, executable pin enforcement, and the outer legacy-revision limitation above were inspected, not mutation-tested.

Semantic tool unavailable: `read xd://lsp` returned “No such tool”; no semantic server status/references/definition/diagnostics could be obtained. Literal search and explicit AST/function execution were fallbacks, not semantic proof. No tooling was installed or updated. Scratch was used only as an explicit TMPDIR and removed before yielding; receipts and the reproducible bounded probe remain under this seat.

## Self-evaluation

Accuracy 4/5: exact hashes and bounded probe receipts support observations; pin-substitution exploit is static only. Completeness 4/5: all requested frozen-claim axes reviewed; candidate implementation was not available and is explicitly excluded. Clarity 4/5: limitations distinguished from literal-predicate failures; pin details are necessarily dense. Actionability 4/5: L1 can retain frozen target and limit conclusions while verifying committed candidate identity; no counter repair performed. Conciseness 4/5: evidence-rich report retains some overlapping scope cautions. Overall 4.0/5. Highest-impact improvements for downstream review: verify the eventual committed candidate; independently enforce canonical freeze/instrument identity; retain exact finite-scope language. Would the user agree? Expected only as a bounded author-side review, not admission.

## Late candidate addendum

After the initial result, ExecCandidate supplied `.ufo/waves/round-83/w1/ExecCandidate/candidates/source-bind.py`. Read-only AST extraction and bounded function probes measured candidate SHA256 `fa08b06340eb49929ffc34d69ac789c4fde91e83b4714afaff20b020e940ed18`: all eight frozen cases matched with boolean results. The function at lines 37–46 is self-contained except `re`; no candidate CLI or committed candidate revision was exercised. Receipt: `w1/ReviewerClaim/receipts/candidate-function.json`. This supersedes the earlier candidate-unavailable gap only for that exact uncommitted function.

**Medium, grammar-boundary counterexample:** candidate lines 38–39 truncate to twelve lines before checking duplicates. `source: S299 — first\n` followed by eleven blank lines and then `source: S286 — second\n` returns true for S299, despite the plan's unqualified “Duplicated source fields ... are unbound/false.” It is a demonstrated discrepancy under the global-duplicate reading of that sentence, and an ambiguity if the first-twelve-line scope was intended to apply to duplicate detection too. It does not falsify the frozen eight-case predicate. L1 should disclose it rather than assert full grammar conformance or silently reinterpret the frozen target.

ExecCandidate subsequently reported that KaidokuR83 confirmed global duplicate rejection and that the candidate now counts all source fields before enforcing the first-twelve-line position, with a new private late-duplicate selftest. This is peer-reported remediation, not independently verified here. The reviewed SHA and function receipt above apply only to the superseded candidate. The observed defect should not be attributed to later bytes without their own measurement.
