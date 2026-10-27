# R43W2Mistakes — adversarial review of M43 candidates and routed defects

## Axes
- **Coverage:** checked all four M43 candidates as proposed in the committed R43Mistake report, the round-42 / round-41 cited evidence, binding prompt rules, cited QUALITY rows, and frozen-plan C1/C2 receipts.
- **Depth:** independently checked evidence for the actual recurrent failures and current score receipts, rather than treating their summaries as closure.
- **Calibration:** distinguish candidate merit from adoption (no round-43 lesson exists at the measured tip) and partial implementation from passing routed-defect closure.

## Measured revision and scope
Evaluated current lane worktree/tip `5856614ac4bf7f2363bbcd1956644474a82108e5`; frozen claims `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c` is an ancestor. The exact committed C1 score evaluates `77d196c66f4fea00d7d543728b190ebdfaf6d0f0`; C2 scores evaluate `77d196c66f4fea00d7d543728b190ebdfaf6d0f0` and `09ab56b8fdc2efcc3b58b203644537d84dd5ac9e`, not current tip. Full commands, outputs, receipt hashes and source hashes are in `artifacts/R43W2Mistakes/evidence.txt`.

## Findings

1. **Cand-1 (unreceipted gate citation): evidence and capture rule confirmed; this is not a demonstrated R43 fix.** Round-42 report line 65 says pre-file gate GREEN at `af50af81`. Round-42 spot-check §1 D2 records the sweep finding no committed round-42 run output, and the independent committed-text sweep likewise found only selftest strings and the round-41 run. QUALITY 52 directly captures this exact failure class. Evidence pointer is sound. However, the proposed cited-runs extension is only a red-check sketch in R43Mistake; no implementation for round-42 pre-file citations was evidenced at inspection. Keep this as a candidate for a future rule implementation, not a claimed closed fix. Avoid treating R43's committed control receipts as proof that the round-42 citation itself was repaired.

2. **Cand-2 (round below floor / missing falsification wave): evidence and capture confirmed; current dispatch addresses the recurrence, not a completed filing check.** The round-42 ledger count is 43, below the prompt's binding 64-seat floor, and round-42 had no wave 2 (spot-check §1 D1 and §5 R42-V1). Prompt §6 run-10 preserves the run-9 64–128 band. No QUALITY row was found for round size, so the prompt rule is the accurate capture citation. At this inspection, R43 has 32 wave-1 reports and a 32-member wave-2 registry, total 64 dispatched; W2 had not settled. This is evidence of an appropriately-sized falsification dispatch, not evidence of a completed wave or a filing-time enforcement tool. Do not call R42-CL2 discharged by this dispatch alone; completion awaits WAVE-DONE and the round-43 closure record.

3. **Cand-3 (filing before WAVE-DONE): historical evidence is strong, but candidate is substantially duplicate/redundant.** Round-41 spot-check §1 and §5 D1 already record this same failure: report before WAVE-DONE, late work and stray `.err` paths. The prompt's WAVE-DONE rule and QUALITY 47 already capture it. This is a recurrence, not a novel class or implemented new fix; the proposed ledger-aware gate is only a sketch. If adopted, explicitly label it a recurrence of the existing rule and show a distinct implementation/failure prevented. Otherwise omit it as a duplicate, rather than presenting the rule/evidence as newly discovered. No evidence of a newly implemented ledger check was found.

4. **Cand-4 (counter parser brittle to wrapped seat votes): prompt capture is direct, but implementation/evidence is not kaidoku-local.** Prompt §6 explicitly describes mori r55 and the plain-vs-JSON wrapping mismatch. QUALITY 22 is not the direct rule: it concerns reproducible per-seat status, and the candidate correctly calls it adjacent. The pointer to the prompt is adequate, but this candidate has no local reproduced failure or implemented parser/sidecar fix in the inspected R43 artifacts. Do not imply QUALITY 22 independently catches the parsing defect. If retained, state that it is an existing prompt-rule warning and require the proposed red/green implementation before calling it closed.

## Candidate duplication / closure calibration
- Cand-3 repeats an already documented round-41 failure and existing WAVE-DONE/QUALITY 47 bar; it should not be presented as a fresh mistake without explicitly distinguishing the recurrence and a real new fix.
- Cand-1 and cand-2 are distinct failures (unreceipted claim vs undersized round/no falsification); neither is duplicated by M42-1..M42-3. Cand-4 concerns a separate parser interface but its captured-by is the prompt, not QUALITY 22.
- At measured tip, `corpus/lessons/round-43.md` does not exist. Therefore no proposed M43 row is confirmed adopted, and the requirement “each adopted mistake has …” cannot yet be positively certified. R43Mistake calls them candidates; keep that distinction.
- The wave-1 candidate report's `fix` cells are red-check sketches, not implementations. Do not report any of those four candidate fixes as implemented based on this report.

## Routed defects — actual implementation vs score
- **R42-CL1 / M42-2:** generator and counter are present; the committed C1 score at `77d196c6` exits 0 with 78/78 and all bindings true. This supports the specific generator self-observation fix at that measured revision. Current-tip equivalence is not asserted; its measured revision is explicit.
- **R41-CL3 / R42-CL3:** local copies, gate, and 136-check content verifier are present. But both committed C2 aggregate receipts inspected (at `77d196c6` and `09ab56b8`) exit 1 because `sources_numstat_three_additions` is false, even though the gate rows and copy-audit checks are green. Since frozen target requires scorer exit 0, these receipts do **not** establish full P43-C2 closure. This is a concrete unsupported-closure risk; do not promote the green child checks or empty `rows_failed` to a green aggregate.
- **R42-CL2:** 32+32 seats are dispatched (64 total), but W2 is unsettled at the measured inspection. This satisfies the minimum dispatched shape only; not the required falsification-and-settlement closure.

## Smallest safe correction
Keep M43 rows explicitly provisional until the post-wave lesson is present. For adoption, require a concrete implemented fix plus a red/green check per row; drop or label cand-3 as a recurrence unless it adds a distinct implemented control. Preserve cand-4's prompt-only capture and do not misattribute it to QUALITY 22. For routed C2, resolve why the scorer's `sources_numstat_three_additions` binding is false and obtain the frozen scorer's exit 0 before claiming closure; do not alter the frozen predicate. For R42-CL2, wait for WAVE-DONE/settled result and the closure receipt.

## Safety and reproducibility
Read-only inspection; no installations, no scratch directory, no VCS mutation, no reserved-input execution, no whole-repo checks. Existing unrelated/user worktree changes were left untouched. Evidence artifact lists command invocations and return observations, file digests, limits, and all receipt revisions.

Report: `.ufo/waves/round-43/w2/R43W2Mistakes.md`