# ExecC2 — independent R73-C2 calibration review

## Result and scope

Axes: byte-level accuracy, routed-defect coverage, false-green resistance.

Independently extracted committed inputs at base `05bf065684e52d72ea25aad95f7acb71fcd7874c` and declaration `da6c17c1eb8dec0b780e276c7f1cb8d9b4fa4d4b`. All selected target inputs are identical between those revisions. The instrument returns six mismatches at **both**, rc 1, stderr empty. This reproduces its predicates, not seven faithful defect checks: **D7 is already green despite the routed cross-document disagreement remaining uncorrected.** No landing revision was evaluated; zero mismatches at landing is not established by this assignment.

Method: `git show REV:PATH`, JSON field extraction, exact numbered text, SHA256 over original blob bytes; no audit-module imports or verdict reuse in deriving facts. Only after independent extraction, ran the explicitly assigned audit at each revision. The executed working-tree instrument equals the declaration blob, SHA256 `8f22d62037171ffef15bc9c4b2438285e350f15637bcbae6b7d6dafa5f40139d`.

## Routed facts, independent derivation, and comparison

Section 6 of the declaration's `corpus/lessons/round-72-verifier-spotcheck.md`, lines 117–123, supplies seven defects. Exact sentences are retained in `independent-comparison.json`. That spotcheck is absent at base; it defines the later review population, not a base-time document.

1. **D1 — target hash.** The record's digest must describe the measured probe, or explicitly correct the old mistaken digest. Independent SHA256: `d8297e8:tools/round-72/seam-probe.py` = `39a2193ebc23eedd16e78a2239e881286e8d4589c01cb5ebdb0c3ac11b60a94b`; `e67f3a1:tools/round-72/seam-probe.py` = `602b305d79222222c1f17c51cc10365246ecfc184cdd4afd8f773a0f5fd5f0e2`. The round-72 C2 receipt records the latter and rev `e67f3a1b1f79bcd5ce56dd4f64edb4ed18f903ff`, while SCORECARD line 5659 says `target sha ` followed by backticked `39a2193e…`. No correction block. Defect remains; audit false at both, agrees.

2. **D2 — pin.** A matching-pin claim needs an actual expected digest, or must say unpinned. The round-72 receipt has exactly `target_pin: {"defect": null, "expect": null, "matched": true}`. No round-73 C2 landing receipt exists in either snapshot. Defect remains; audit false at both. **Evidence mismatch in scope:** its returned `receipt: null`, `target_pin: {}`, `target_sha256: null` describe missing round-73 evidence, not the existing round-72 null pin. The supplied-pin requirement also rejects the routed defect's permitted honest “unpinned” correction.

3. **D3 — disclosures.** An exact-disclosures assertion requires the actual gate block and round-72 ledger row, or withdrawal of the assertion. The round-72 gate keys are `audited, claim, clean, flagged, freezes, required_clean, required_failed, rev, summary`: no `disclosures`. No round-72/round-73 ledger rows and no round-73 gate receipt exist. Defect remains; audit false at both. It additionally requires a round-73 ledger row and gate rather than allowing a prose correction; those requirements are not the routed defect's sole repair path.

4. **D4 — lying-run rc.** A claimed exit code must be recorded; otherwise describe only the rejection verdict. The round-72 lying receipt records `rc: null`, `met: false`, `clauses.receipt_capsule: false`; failures include exactly `receipt_capsule: canary` (plus digest/count/keys/children failures). SCORECARD line 5660 still says `exits 1`. Defect remains; audit false at both. Its false result additionally depends on absent round-73 receipt/`rc`, and does not allow the routed alternative of citing only the recorded verdict.

5. **D5 — provenance position.** Bind all three provenance fields to the entry opening, or explicitly permit a named provenance section with a strengthened criterion and supporting lesson. The round-72 entry has `source:`, `verified-at:`, `recheck:` at lines 66, 67, 68; none in lines 1–12. Its existing heading is `## Provenance and recheck`, not the instrument's required `## Provenance (round 73 correction)`. No round-73 entry exists. Defect remains; audit false at both. Requiring a new round-73 entry is extra; neither a first-12-line cutoff nor the exact correction heading is named by the routed defect.

6. **D6 — lowest-axis rationale.** Withdraw the unsupported stagnation-waiver rationale; coverage satisfies tied-lowest without a waiver. SCORECARD lines 5653–5654 still state `the stagnation nudge` / `applies (every owned axis 10.0, saturation 10.0, window 10), so the lowest-axis obligation is waived.` No round-73 section or `lowest-axis:` label exists. Defect remains; audit false at both. **Evidence scope differs:** `claims_waiver: false` refers only to absent round-73 text; it does not negate the extant round-72 waiver sentence. Literal label presence is not numerical lowest-axis re-derivation.

7. **D7 — before pointer.** Report and SCORECARD must select the same C1 before receipt and measured revision. SCORECARD line 5658 names `l1/pre/c1-at-base.json`, rev `6316c1053f927a1a1cdc3e0960b70acab5f56381`, 9/11. `l1/scores/c1-at-base-final.json` also exists, rev `e67f3a1b1f79bcd5ce56dd4f64edb4ed18f903ff`, 9/11. The committed spotcheck item 7 explicitly says the report selects that second receipt. Neither selected lane input changes between base and declaration. **Audit true at both is a semantic disagreement/false green**, not proof of repair: it checks only resolving SCORECARD `l1/pre/*.json` pointers and string revisions, never the report or `l1/scores/` pointer or agreement. It also deduplicates names, so its docstring's “named once” is not enforced.

Audit D7 additionally resolves C2 pre receipt rev `b827a8b5d54f2885ec9be7786389f356c59226ce` and C3 pre receipt rev `6316c1053f927a1a1cdc3e0960b70acab5f56381`; their existence is independently retained. Instrument booleans in D1–D7 order: `[false,false,false,false,false,false,true]` at both revisions. No numerical/predicate-reproduction disagreements; the disagreement is correspondence to the routed repair obligation.

## False-green and off-target-failure review

These are source-derived logical counterexamples, **not executed mutations**:

- **D1:** deleting every `target sha` match makes `wrong=[]` and permits green with no correction. A correction tail merely repeating the old token passes without stating the correct value. It never checks the report correction.
- **D2:** any JSON receipt with equal arbitrary string `expect`/`target_sha256` and `matched:true` passes; no actual target digest/revision binding or record correction is checked. A legitimately “unpinned” textual correction still fails.
- **D3:** synthetic `disclosures:{missing:[],stray:[]}` plus ledger lines merely containing round substrings passes without validating exact findings or gate revision. A legitimate withdrawal of the assertion still fails; round-73 row is an extra obligation.
- **D4:** JSON `rc:true` is accepted because Python bool is an int and `True == 1`; no real integer exit code is required. An unrelated rejection lacking the canary also passes. Honest verdict-only wording still fails if rc absent.
- **D5:** one opening field suffices for round 72; three duplicate `source:` fields satisfy round 73 because identities are not distinguished. A named correction with three duplicate list fields also counts. Criterion/lesson changes are not inspected. New-entry presence and exact heading/cutoff can cause failures outside the routed defect.
- **D6:** arbitrary `lowest-axis:` text passes without naming/deriving a real lowest axis, and checking only the round-73 section does not ensure the prior rationale is corrected. Equivalent honest wording without that exact label fails.
- **D7:** observed false green already at base/declaration. It checks extra C2/C3 pointers while omitting the report comparison that is the actual defect; round identity is weakened by trying round-72 resolution first for each deduplicated relative path.

Therefore “six mismatches at base” is numerically reproduced, but must not be presented as evidence that exactly six routed defects remain or that all seven atoms faithfully re-derive their named defects.

## Evidence and limits

All receipts below are under this report's directory:

- `committed-evidence.json`: exact selected committed text with line numbers, JSON fields, whole-input byte lengths/digests, independently computed probe hashes, both revisions.
- `independent-comparison.json`: seven own-word mechanical facts, per-revision conclusions, exact routed sentences, semantic disagreement.
- `base-audit.json`, `declaration-audit.json`: requested instrument outputs.
- `audit-execution.json`: argv, cwd, rc, stderr, rows and executed instrument hash.

Report-side source bytes are fleet-owned, outside the pinned lane snapshots: no external report was read or modified. The report pointer discrepancy is grounded in the declaration's committed non-author spotcheck, not claimed as a fresh direct report inspection. No landing evaluation, mutations, packer invocation, builds, linters, formatters or tests were run. No tool installed; no credentials/environment values read or retained. Scratch `/fast/scratch/hyaku/kaidoku-r73/ExecC2` was deleted in `finally` after copying receipts. No implementation changed. LSP tools are not mounted in this seat; no symbol refactor was performed.

Parent action: treat D7 as uncalibrated against its named defect; compare actual report and SCORECARD selected before receipt/rev when deciding repair. Evaluate any eventual landing independently rather than treating declaration as landing.

Self-evaluation: accuracy 4 (report-side bytes unavailable within scope; attribution explicit), completeness 4 (all seven facts and both revisions covered, landing intentionally unevaluated), clarity 4 (predicate truth separated from repair truth), actionability 4 (specific weak predicates identified; no code changes authorized), conciseness 4 (exact-byte details retained separately). Overall 4.0. Improvements: bind D7 to both documents; distinguish missing next-round evidence from original-defect failure; evaluate a supplied landing. These are advisory, not scope-expanded edits.

Report: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-73/w1/ExecC2/Report.md
