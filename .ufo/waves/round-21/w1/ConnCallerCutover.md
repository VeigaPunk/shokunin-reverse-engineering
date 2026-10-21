# R21 successor caller cutover — scoped findings

## Axes

- **R21-C1 / calibration:** the successor control is relevant because it removes a C3 receipt from the evidence path for the C1 correction.
- **R21-C2 / depth:** keep its distinct observation-comparison predicate, implementation and frozen denominator unchanged. No successor-validator migration is needed for C2.

## Caller and registry evidence

- R21 `claims.json:8` requires both record-bound C1 evidence and a routed positive control independent of the C3 receipt; it says the isolated validator control must work without the C3 forecasting delta. The frozen contract (`fixture-contract.json:5-17,41-42`) fixes 12 C1 cases and says the old R20 authorities remain historical.
- The R20 verifier explicitly records the debt and requested separation (`corpus/lessons/round-20-verifier-spotcheck.md:130-138,177`): R20's aggregate D6d check used `.ufo/waves/round-20/runs/t1246-addr2line/receipt.json` as its positive control; R20 C3 separately used the original validator authority. The 19 R20 outcomes and receipt records are historical, not a migration target.
- R20 caller split is intentional and must not be flattened: `.ufo/waves/round-20/tools/routed-r19.py:50-52,937-962` defines both the original and v2 validator paths; `_s_d6d` invokes v2 on a decoy plus the R20 C3 receipt. `.ufo/waves/round-20/measure.py:32,48-50` instead selects the original R17 `receipt-validate.py` for C3. These are retained R20 behavior/provenance, not live R21 callers to rewrite.
- The current R21 successor reference is `.ufo/waves/round-21/tools/isolated-control.py:18-55`: it loads `.ufo/waves/round-17/tools/receipt-validate-v2.py`, synthesizes inert positive/decoy receipt metadata, runs the validator on those two temp receipts, and returns a v2 file digest. The helper's source contains no C3 receipt path. It does not report the sibling `pins.py` digest, although v2 loads `pins.py` alongside itself (`round-17/tools/receipt-validate-v2.py:41-43,68`).
- **Blocking integration gap:** `.ufo/waves/round-21/battery.py:61-107` dispatches only `tools/verb-coverage.py` for C1 and `tools/compare-first-failure.py` for C2. It never calls `isolated-control.py`. Its frozen input manifest (`fixtures/expected.json:1-6`) hashes only the fixture contract and battery cases, not this control. Thus a green claim-specific battery alone does not exercise or register the R20-SEP cutover; the only R21 source-level caller of validator-v2 is currently this otherwise-orphaned helper.
- Attribution needs path/hash, not the validator's JSON `tool` field: `receipt-validate-v2.py:720-725` reports `"tool":"receipt-validate.py"`, the same label as the predecessor at `receipt-validate.py:719-724`. The helper's `authority_sha256` disambiguates the validator bytes, but not its `pins.py` dependency.
- `corpus/SOURCES.md:55-56` registers the RFC 8259 and Python JSON-decoder semantics relevant to the C1 predicate; it is not a validator/call-site registry and contains no successor-validator row. Do not recast the local helper as an external source or rewrite those rows. If the current R21 control needs a registry/provenance pointer, put it in the round-local C1 evidence/report record and name the exact helper, v2 path, revision and authority digests.

## One bounded move

Wire the existing `isolated-control.py` result into the **R21 C1 acceptance/reporting path only**, and record the exact `receipt-validate-v2.py` and sibling `pins.py` authority digests. Keep its two controls supplementary to (not part of) the 12 frozen C1 denominator. Do not route through the R20 carrier receipt. Leave the R20 caller, R20 C3 measurement, original R17 validator, frozen forecasts/logs, and historical receipts untouched; do not import C1 successor code into C2.

### Acceptance condition

At the intended R21 revision, the C1 path reports every frozen C1 case ID with its frozen exit (3 accepted positives, 7 rejected/refusal negatives, 2 unevaluable malformed/ambiguous cases) **and separately** reports the isolated positive (`exit 0`) and decoy (`exit 1`, `analyze_step_unauthenticated`) outcomes. The isolated control passes when invoked from a minimal fixture root containing the v2 validator and required `pins.py` but no `.ufo/waves/round-20/runs/t1246-addr2line/receipt.json`; its report binds both tool and pins digests. C1 must not load C2 code. Separately retain all 20 C2 frozen outcomes and the 19 R20 matches as retrospective only; no historical receipt/prediction/log/comparator bytes change.

## Risks and checks for parent (not run here)

- A bare C1 battery run currently misses the isolated control; wiring or explicitly joining its result is required before the R20-SEP acceptance can be claimed. Keep the 12-case denominator fixed; show the two successor controls as supplementary rows.
- Do not infer v2 identity from output `tool` label. Bind by path, intended revision and SHA-256 for both v2 and adjacent `pins.py`; otherwise the loaded validator and dependency are not fully attributed.
- After integration, run the frozen C1 and C2 battery commands from the lane root and inspect all per-case IDs/exits against `fixture-contract.json:5-42`. Separately exercise the C1 isolated control against a minimal tree lacking the historical C3 receipt. Confirm no R20 receipt, frozen prediction/log/comparator or original-validator blob was rewritten; keep that check independent of fresh REA/carrier activity. No external URLs were opened; no tests, builds, validators, providers, carriers, or installations were run here.

Report: `.ufo/waves/round-21/w1/ConnCallerCutover.md`
