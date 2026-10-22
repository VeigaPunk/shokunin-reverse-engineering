# R28-C1 review — tally slice 3 (rows 95-141)

Seat: KaidokuR28a2.ReviewTallySlice3. Lane read-only; no lane file touched except this report.
Run window: 2026-10-22T18:20Z-18:27Z. No network requests, no REA runs, no installs (none needed).

## Scope and interpretation

- Slice: held-out data rows 95-141 inclusive (1-based, after the header row), in the order of
  `corpus/evidence/round-28/c1/heldout.tsv` — 47 rows, carriers h16-h49. First row 95 = ed88c68e
  donate() h16, last row 141 = c27fc305 f1() h49 (observation, results.tsv first/last line).
- Numbering convention (1-based data rows) is an [INFERENCE] from "data rows in order of
  heldout.tsv"; with the header at file line 1 this maps to file lines 96-142. Under the only
  alternative (0-based) the slice would be rows 96-142, one row shifted; the check script is
  parameterized so a re-run under that convention is trivial.
- Checked per row: (a) envelope `normalized_result.functions` inferred arguments for the
  selector, (b) `db/openchain-<sel>.json` candidates, (c) the committed tally row, recomputing
  the primary rule `openchain_sole_unfiltered_args_consistent` and the verdict
  named-right / named-wrong / no_name; plus tally fields abi_signature, recovered_by_rea and
  inferred_arguments against heldout.tsv and the envelope.

## Method

- Script `check_slice3.py` (sha256 2c9f605d817d8e969b216a03ed1343aee8960a3d6a110a27f8a171628d1216c8)
  imports `tools/round-25/a2/resolve-selectors.py` read-only (module import only; no lane write)
  so keccak256, `params_of` and `_label` semantics are byte-identical to the counter
  `tools/round-28/c1-heldout-naming.py` (`rule_outputs`, lines 135-152: unfiltered openchain
  candidates, label "consistent", named only when exactly one).
- Verdict: hold/none — observation below.

## Result

- Command: `TMPDIR=... python3 check_slice3.py`, exit 0, 2026-10-22T18:26:34Z.
  Excerpt: `slice=95-141 rows=47 agree=47 disagree=0` and `computed verdicts: {'right': 41, 'wrong': 0, 'no_name': 6}`.
- Verdict counts across the slice (recomputed from evidence, independent of the tally):
  41 named right, 0 named wrong, 6 no_name (observation).
- 47/47 tally rows agree with the recomputation; 0 disagreements (observation).
- No row in the slice has more than one openchain candidate (`awk -F'\t' '$6>1'` over
  results.tsv: no output, exit 0): 41 rows have exactly 1 unfiltered consistent candidate
  naming the true ABI signature; 6 rows have zero candidates (observation).
- no_name rows, all with 0 candidates in the openchain response (observation, results.tsv):
  113 0cc70726 h25 p0(uint256); 115 c4bf1a8c h25 p4(uint256); 118 8ec3a062 h26 p6(uint256);
  132 5ce2a6a0 h31 timestampProbe(); 136 1011b3d5 h32 local_b(uint256); 137 4c6cac96 h32
  local_a(uint256). Spot evidence: `openchain-0cc70726.json` = `{"ok":true,"result":{"function":{"0x0cc70726":null},"event":{}}}`;
  h31 envelope recovers 5ce2a6a0 with inferred_arguments `""` and the tally row has all five
  rule outputs null with recovered_by_rea true — consistent (observation).

## Keccak validation (rule semantics)

- The sole non-trivial primitive is keccak256. Cross-checked the lane resolver implementation
  against three values known independently: transferOwnership(address) -> f2fde38b, get() ->
  6d4ce63c (script asserts, exit 0) and increment() -> d09de08a (separate run, exit 0,
  2026-10-22T18:27:21Z). All match (observation). No keccak defect found in the slice.

## Artifact sha256

- check_slice3.py 2c9f605d817d8e969b216a03ed1343aee8960a3d6a110a27f8a171628d1216c8
- results.tsv a30b79aded59e45b8470b124f4ab72a83b65e8c86dee1f9fc62e30969d11d8b3
  (per-row table: row, selector, carrier, abi, inferred, candidate counts, computed primary,
  computed verdict, tally verdict, agree flag)
Both under /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ReviewTallySlice3/.

## Lane files read (evidence base)

- corpus/evidence/round-28/c1/heldout.tsv, tally.json, envelopes/<h16,h18,h19,h20,h21,h22,
  h23,h24,h25,h26,h27,h28,h30,h31,h32,h34,h49>.json, db/openchain-<sel>.json for the 47 slice
  selectors, db/manifest.json (structure only).
- tools/round-28/c1-heldout-naming.py, tools/round-25/a2/resolve-selectors.py (rule semantics).

## Verdict

HOLDS — the 47 tally rows 95-141 are faithful to the committed evidence: recomputation from
envelopes + openchain responses reproduces every primary-rule verdict, including the 6
no_name rows caused by empty openchain responses, and no named-wrong case exists in this
slice. This is consistent with the round-level aggregate (primary rule 0 wrong, 50 no_name
overall).

## Residual risk and verification gaps

- Slice only; rows 1-94 and 142-187 were reviewed by sibling seats.
- Slice numbering convention is inferred (see Scope); a 0-based reading shifts the slice by
  one row and was not re-run.
- The 4byte side of each row was not recomputed (out of scope; primary rule is openchain-only),
  so fourbyte_first/fourbyte_sole verdicts in these tally rows are unchecked by this seat.
- Envelope contents were taken as the committed REA output; this seat did not re-run REA on
  the runtime bytecode (not in item scope).
