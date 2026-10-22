# ReviewTallySlice4 — R28-C1 tally rows 142-187 (46 rows)

Seat: KaidokuR28a2.ReviewTallySlice4, 2026-10-22. Lane read-only; no lane files other than this
report were touched. No installs were needed (python3 only).

## Scope and method

Slice: heldout.tsv data rows 142-187 in file order. Boundary pinned by raw read
(`read corpus/evidence/round-28/c1/heldout.tsv:raw:141-145`, exit 0, 18:2xZ): line 142 =
`c27fc305 f1() h49` (data row 141), line 143 = `9942ec6f f2() h50` (data row 142 = slice start),
line 188 = `db1d0fd5 alpha() h61` (data row 187 = slice end). 46 rows, carriers h50-h61.

Primary rule `openchain_sole_unfiltered_args_consistent`: the sole openchain candidate with
`filtered=false` whose keccak matches the selector and whose parameter list equals the envelope's
`inferred_arguments` (same rule code as the counter: `_label` and `_load_candidates` exec'd from
tools/round-25/a2/resolve-selectors.py). Verdict per row: named_right (output == abi_signature),
named_wrong (output != abi_signature), no_name (no sole candidate).

For each row I recomputed the verdict independently from the three evidence files — envelope
`normalized_result.functions` inferred_arguments, `db/openchain-<sel>.json`, and the carrier ABI
signature from heldout.tsv — then compared against the tally row (keyed by selector+carrier) and
also against the tally's `inferred_arguments` and `recovered_by_rea` fields.

Producing command (`python3 /fast/scratch/.../check_slice4.py`, exit 0, 2026-10-22T18:26:17Z):
final line `AGREE 46  DISAGREE 0  total 46` [observation].

## Result: verdict holds — 46 agree, 0 disagree

- 26 named_right, 20 no_name, 0 named_wrong. Every recomputed verdict equals the tally row's
  primary-rule verdict, and the name text matches exactly (including the 14 rows where the rule
  names nothing and tally stores null). [observation]
- Field agreement on all 46 rows: tally `inferred_arguments` equals the envelope value (including
  `""` for zero-arg functions and the misreads, e.g. `72b91e61` inferred `uint256` vs ABI
  `seen(address)`), and `recovered_by_rea` is true on all 46 (no h09-style refusal in this slice).
  [observation]
- Aggregate cross-check (`python3 -c` over tally.json, exit 0, 18:2xZ): recomputing the counts
  from all 187 tally rows gives `named 137 right 137 wrong 0 no_name 50`, equal to the frozen
  observed counter output at a2673116; the slice's 26 named_right are exactly the rows of carriers
  h50-h61, which occur only in this slice. [observation]

## Hand-checked evidence rows (read as raw bytes, sha256 below)

1. `f2fde38b` h59 (named_right): openchain response lists two candidates, both `filtered:false` —
   `transferOwnership(address)` (consistent: params `address` == envelope `address`) and
   `_SIMONdotBLACK_(int8[],uint256,address,bytes8,int96)` (args-mismatch). Sole unfiltered
   args-consistent candidate equals the ABI signature. [observation]
2. `0ff5ce72` h56 (no_name): envelope h56 records `0x0ff5ce72` inferred `uint256`; the only
   candidate `set_paused(bool)` is unfiltered but args-mismatch, so no name. [observation]
3. `53f49708` h60 (no_name): response body is `{"ok":true,"result":{"function":{"0x53f49708":null},"event":{}}}`
   — zero candidates. [observation]
4. `7425570b` h57 (no_name): zero openchain candidates; envelope inferred
   `bytes,bytes,uint256,uint256,uint256` vs ABI `tag(string,bytes,uint256[2],bool)` — even a
   hypothetical candidate would have been args-mismatched. [observation]

## Verdict

Holds. The committed tally rows 142-187 reproduce exactly from the committed envelopes and
openchain responses under the round-25 primary rule; no disagreement found.

## Residual risk and verification gaps

- Keccak labeling uses the resolver's standard-library Keccak (the same module the counter exec's;
  its selftest 9/9 is asserted in the knowledge entry, not re-run by this seat). [inference: low risk]
- Responses were read as committed snapshot bytes; no live re-fetch and no per-file manifest
  sha256 sweep (that check belongs to the counter/ExecRecountC1 seats). [observation]
- Hand depth was 4 rows; the other 42 were verified by the script only. [observation]

## Artifacts (scratch, outside the lane)

- /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ReviewTallySlice4/check_slice4.py
  sha256 b80518d3208cfd814dedcc7236e09e8f99043d872f43a21cdd4d6a35fd256fcf
- /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ReviewTallySlice4/slice4_detail.json (per-row labels)
  sha256 e29c56587ba1bf911e46073ffb108f38635f24bcf587033e36a36ca68fdec2cb

Files read (access 2026-10-22): corpus/evidence/round-28/c1/{heldout.tsv
423654f9d71feb417725a1e5a290b1e028ee53ad628141281a8c08391dab6cef, tally.json
655d8d648ecd46fa8ae71aca4fba7f57ba0fabc7dbd122e55bd4b6d0f1d148a5, envelopes/h01,h50-h61.json,
db/openchain-<46 selectors>.json incl. f2fde38b c4974fc80331638545fa6f4068cb9108c9ff330f2a9cf0e66a24821457265f15,
0ff5ce72 656388cb11e8821cf55ce317e0191e0d34c6f947252a24ea3497efdd73f4d68b, 53f49708
1b677d08d80d9771e2be1e0c027ed361d4f8358148611f0a6bcb019d42255e13},
tools/round-28/c1-heldout-naming.py, tools/round-25/a2/resolve-selectors.py,
corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md.
