# ReviewTallySlice1 — R28-C1 tally rows 1-47

Verdict: **holds**. All 47 rows of my slice agree with an independent
recomputation of the primary rule. 0 disagreements.

## Scope

Data rows 1-47 of `corpus/evidence/round-28/c1/heldout.tsv` in file order:
h01 rows 1-8, h02 rows 9-18, h03 rows 19-26, h04 row 27, h05 rows 28-29,
h06 rows 30-47. No h09 rows in this slice, so the REA h09 refusal does not
touch it.

## Method

Independent script (not the counter): for each row it reads the carrier
envelope `corpus/evidence/round-28/c1/envelopes/<carrier>.json`
(`normalized_result.functions`, selector matched without the `0x` prefix),
reads `corpus/evidence/round-28/c1/db/openchain-<sel>.json`, re-checks the
file sha256 against `db/manifest.json`, and recomputes
`openchain_sole_unfiltered_args_consistent` as: exactly one candidate with
`filtered` false, keccak256(name)[:4] equal to the selector, and parameter
list equal to the envelope's `inferred_arguments` (spaces stripped; when
`inferred_arguments` is null the parameter check is skipped). Verdict:
`no_name` when null, else `right`/`wrong` against the heldout
`abi_signature`. Keccak and `params_of` are imported from the lane resolver
`tools/round-25/a2/resolve-selectors.py` with two fixed vectors asserted at
run time (empty-string keccak and `transfer(address,uint256)` -> `a9059cbb`).
Tally rows were matched positionally, cross-checked on selector and carrier.

- Producing command: `python3 -I -B /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ReviewTallySlice1/verify_slice1.py > run1.json`, exit 0, 2026-10-22T18:26:01Z.
- Input pins observed: heldout.tsv sha256 423654f9d71feb417725a1e5a290b1e028ee53ad628141281a8c08391dab6cef (equals the counter pin); tally.json sha256 655d8d648ecd46fa8ae71aca4fba7f57ba0fabc7dbd122e55bd4b6d0f1d148a5.

## Result (observation)

- rule output agree 47/47, disagree 0; verdict agree 47/47.
- Verdicts: named right 33, named wrong 0, no_name 14.
- All 47 openchain files sha256-match their manifest entry (observation).
- Tally row order equals heldout.tsv order for all 47 (selector and carrier
  match at every position) (observation).
- Tally `inferred_arguments` and `recovered_by_rea` equal the envelope for
  all 47 (observation).

## Hand checks from raw bytes (observations)

- Row 12 `6901eb1e` h02, truth `digestOf(bytes32)`, tally no_name: envelope
  h02 says `0x6901eb1e` inferred `'uint256'`; `openchain-6901eb1e.json` body
  `{"ok":true,"result":{"function":{"0x6901eb1e":[{"name":"digestOf(bytes32)","filtered":false,"hasVerifiedContract":true}]}}}`.
  The sole unfiltered candidate is the true name but its parameter list
  `bytes32` differs from the inferred `uint256`, so the rule gives no name.
  Correct per the rule (the documented round-25 failure mode).
- Row 18 `ee02438e` h02, truth `mark(bytes32)`, tally no_name: same shape —
  sole unfiltered candidate `mark(bytes32)`, envelope inferred `'uint256'`,
  rejected on arguments. Correct.
- Row 27 `47c1ab88` h04, truth `blob_fee()`, tally no_name: response body is
  `{"ok":true,"result":{"function":{"0x47c1ab88":null},"event":{}}}` — zero
  candidates; envelope h04 has the single function with inferred `''`.
  no_name correct.
- Row 13 `6e69f38c` h02, truth `scale(uint256,uint256)`, tally right: sole
  unfiltered candidate `scale(uint256,uint256)`, envelope inferred
  `'uint256,uint256'`, name equals truth. Correct.
- Rows 10, 11, 19-26, 29: openchain body null for every selector (no
  candidates), no_name correct for each (script census, sampled raw).

No disagreement found. Nothing to report as a defect in this slice.

## Residual risk and verification gaps

- Keccak and parameter parsing reuse the lane resolver's implementation, so a
  bug there would self-confirm; the two fixed vectors and the round-25
  selftest mitigate but do not eliminate this. [inference]
- I checked only the primary rule column (`openchain_sole_unfiltered_args_
  consistent`); the other four rule columns in `tally.json` rows are inside
  the slice but outside my acceptance. Their wrong_names list is empty and
  my run saw no contradiction, unverified claim otherwise. [observation on
  primary only]
- The envelope and response files were taken as committed bytes; I did not
  re-verify REA run exits or fetch timestamps (counter's scope, and the
  committed runs.tsv shows h09 exit 1 outside this slice).

## Artifacts (outside the lane, /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ReviewTallySlice1/)

- `verify_slice1.py` sha256 c319880d6e46674528666c8f5cb37a274655fb88e5d32211b92c9a6af28c0326
- `run1.json` (full per-row output) sha256 29ececae562b5ad6313030642d427f2b7e8491ed5ba4b23e012c66aadb8f0686

No tools were installed or upgraded (stdlib Python only). No network calls.
Lane untouched except this report file.

Report: .ufo/waves/round-28/a2w/ReviewTallySlice1.md
