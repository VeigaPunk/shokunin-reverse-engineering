# REA province boundary — R21 C1/C2

## Axes

- **R21-C1 — calibration** (one of the tied-lowest finite proxies): bind the cited evidence ID to the requested operation in the same successful record; reject refusals and ambiguous/malformed inputs.
- **R21-C2 — depth**: distinguish a valid, bounded silent observation from absent or malformed extractor output, while retaining the specified kind/index/null semantics.

## Evidence and boundary

- `PROVINCE.md:40-71` assigns Kaidoku's Core the REA MCP/CLI/provider and evidence-surface map. The cross-lane registry is specifically per-client registration, provider availability, environment keys, and on-host artifact inventory (`:64-67`); it is live state and MUST NOT rebase a sibling's frozen receipt/history or stand for that sibling's runtime capability (`:67-71`). This is REA-local tool/surface ownership, not blanket ownership of every lane's evidence ledger.
- The current R21 contract is likewise narrow: `claims.json:8-12` separates C1 and C2 and says C1 is local evidence binding, not authentication; `fixture-contract.json:5-17,19-42` freezes 12 C1 and 20 C2 cases, prohibits loading the other claim's successor, and leaves 19 R20 results as retrospective regression only.
- The candidate cross-pattern is supported by current R21 proposals: `w1/C1OperationRecord.md:9-29` and `w1/C1CompareWitness.md:7-28` identify file-wide / nested-input co-occurrence as insufficient for record identity; `w1/C2NakedSilence.md:7-20` distinguishes naked `null` from a bounded silence envelope; `w1/C2Kinds.md:5-27` preserves kind/index equality. `w1/ConnProposal.md:12-26` correctly treats those as distinct predicates, with a round-qualified per-case ledger rather than one shared validator or aggregate green result.
- The source registry's S049/S050 (`corpus/SOURCES.md:55-56`) grounds duplicate-member and decoder ambiguity policy, while expressly disclaiming Evidence authentication and schema authority. It is not a province-ownership registry.
- The prior verifier explicitly leaves the broad REA/revenger adjacency unresolved (`corpus/lessons/round-20-verifier-spotcheck.md:183`). Revenger's older connector report says Kaidoku owns REA's current tool/surface map but distinguishes that from revenger's domain ledger and historical receipt (`../revenger-shokunin/reports/round-1/connector.md:23-36`). Its local “no overlap” verdict concerns that report's named historical fix; it does not supersede R20's later, broader unresolved-adjacency statement.

## One bounded move

Use a **scope-tagged, round-qualified per-case outcome ledger** when the author integrates C1 and C2: record each frozen case's expected/observed exit and semantic label, plus whether its input is a synthetic fixture, a retained historical observation, or (if any) a fresh REA-local record. For C1 expose the root record's own ID, operation, and refusal/error state; for C2 expose envelope validity, `first_failure`, and the `last_line` bound. Keep the two claim runners and authorities separate. This synthesizes the record-binding and bounded-observation proposals while making provenance visible: a local REA contract check is not a claim that REA authenticates Evidence, and neither it nor R20's records decide revenger's domain-ledger authority. It improves calibration by making false attribution observable and improves depth by retaining the distinction between observed silence and no observation; it requires no province transfer or common predicate.

### Concrete acceptance condition

1. Report all **12** frozen R21-C1 IDs separately: the three positives exit 0, the seven record/operation/refusal negatives exit 1, and the malformed/ambiguous cases exit 2; no positive is rejected and no negative is accepted. The isolated C1 positive/decoy control also works without the R20 C3 receipt. C1 does not load C2 successor code.
2. Report all **20** frozen R21-C2 IDs separately: three valid matches exit 0, four well-formed mismatches exit 1, and thirteen absent/malformed/unusable observations exit 2. Bounded silence remains a valid observation; naked/missing/unbounded output does not. C2 uses baseline C1 behavior and does not load C1 successor code.
3. Keep the **19** R20 exact-artifact matches labelled `R20-C3/depth — retrospective`, outside both R21 denominators and not as fresh forecasts. Mark synthetic inputs synthetic; make no Evidence-authentication, runtime, security, or province-adjudication claim. Do not edit `PROVINCE.md` or revenger's files as part of this move.

## Conflict and checks

**Blocking conflict:** any report or integration that turns revenger's older, fix-specific “no overlap” wording into a global no-overlap ruling, or changes historical receipt/producer identity to match Kaidoku's live REA map, conflicts with the R20 unresolved-adjacency ruling and the explicit frozen-history boundary. This blocks a province ownership change, not the bounded R21 C1/C2 test/reporting move. No direct conflict was found between Kaidoku's REA-local surface ownership and the cited revenger report's lane-local ledger ownership; broader adjacency remains unadjudicated.

Parent checks (not run here): run the frozen claim-specific C1 and C2 batteries and inspect per-case IDs/exits against `fixture-contract.json:5-42`; separately test the C1 isolated control with the historical C3 receipt absent and confirm C2 uses baseline C1 behavior. Confirm all 19 R20 authorities remain unchanged and outside the R21 denominators. No tests, validators, builds, providers, REA producers, carriers, or installs were run for this report.

Report: `.ufo/waves/round-21/w1/ConnProvince.md`
