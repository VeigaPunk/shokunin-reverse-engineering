## CLAIM
Adjudicate XA’s four reported divergences and PB0’s L10 route/class concern.

## METHOD
Read XA, PB0, CB9; the referenced RV2/RV3/RV4, RE1, EX6/EX8/EX10, SC5, PR1 and PS4 reports; and lane-A/B receipts for L4, L6 and L10. No probes or other writes.

## FINDINGS
- **L10 / PB0:** XA’s RV2 attribution is wrong; the canonical lane-A receipt records two `inspect_wasm_artifact` calls, and lane B records the same calls and stdout hash. Both got structured `capability_unavailable` refusals, so the observed class is TYPED-REFUSAL. Under the class-only contract supplied for this adjudication, the detour does not void that class match. Neither `compare_wasm_interfaces` nor the Harmony fallback ran, however. **Carried open:** PS4:8 says L10 predicts RESULT if WASM carriers exist; SC5:8 reports carriers. That conflicts with the supplied L10 TYPED-REFUSAL prediction, so the actual frozen prediction and route-level completion cannot be settled from these records.
- **L6 receipt/provenance:** Resolved for the current receipt: `receipts/leg-6.md` is RV3’s selected-table replay (`ev_e0eb…`, stdout SHA `9a1445…`), not EX6’s separate claimed run (`ev_1570…`). **Carried open:** EX6’s raw capture was only in `/tmp` and is unavailable; its result and the exact replacement chronology cannot be independently verified.
- **L6 hash:** Resolved. XA misattributes the mismatch to EX8 (an L8 report); RE1 recorded a mismatch against an earlier receipt snapshot. The final L6 receipt’s displayed stdout matches its recorded hash (CB9); its later write time explains RE1’s stale finding.
- **L4 target:** Resolved. The canonical receipt targets Signal’s `.node`; RV2’s `/usr/bin/rg` replay is a distinct off-target check, not contradictory L4 evidence.

## THREATS
Prior receipt versions and EX6’s raw capture are unavailable; mtimes do not independently prove chronology. The PS4 versus supplied-contract conflict limits L10 adjudication.

## VERDICT
FINDING: L4 and the current L6 receipt/hash discrepancies resolve; EX6 provenance and L10’s frozen prediction/route remain open.
