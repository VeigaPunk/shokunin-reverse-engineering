# R28-C1 tally slice 2 review (data rows 48-94)

Seat: KaidokuR28a2.ReviewTallySlice2. Date 2026-10-22. Lane tip a2673116.

## Scope and method

Heldout data rows 48-94 inclusive (47 rows), i.e. heldout.tsv lines 49-95,
selectors ba3ae68e (h06) through b5c9d046 (h16), carriers h06 h07 h08 h09 h10
h11 h13 h14 h15 h16. For each row I recomputed the primary rule
`openchain_sole_unfiltered_args_consistent` verdict directly from the committed
evidence: the carrier envelope's `normalized_result.functions`
(selector -> inferred_arguments), the openchain response
`db/openchain-<selector>.json`, and the truth signature in heldout.tsv; then I
compared it to the row stored at the same position in tally.json `rows`.

Rule as implemented by tools/round-28/c1-heldout-naming.py (lines 135-150,
247-293): a row that was not recovered by REA yields no name; otherwise take
openchain candidates with `filtered` exactly false, keep those whose label is
`consistent` (keccak of the candidate equals the selector and the candidate's
parameter list equals inferred_arguments with spaces removed); exactly one such
candidate gives the name, `right` when it equals the abi_signature else `wrong`;
zero or more than one gives `no_name`. My script reuses the round-25 resolver's
own keccak and params_of (exec of tools/round-25/a2/resolve-selectors.py, the
same mechanism the counter uses) and re-derives labels independently.

## Producing commands

- `python3 /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ReviewTallySlice2/verify-slice.py`
  exit 0 at 2026-10-22T18:35:54Z. Output:
  `{"slice":[48,94],"rows":47,"agree":47,"disagree":0,"order_ok":true,"field_mismatches":[],"verdict_histogram":{"right":37,"no_name":10}}`
- `cat db/openchain-<sel>.json` for all ten no_name selectors at 18:44Z,
  excerpts below.
- `node -e keccak256` cross-check via npm js-sha3 0.13.0 at ~18:40Z, exit 0;
  all ten sampled signatures reproduce the committed selectors (excerpt:
  `burn(uint256) 42966c68` and `collate_propagate_storage(bytes16) 42966c68`).
- `grep -P '^h09' runs.tsv` at ~18:40Z: `h09 2026-10-22T17:17:34Z 1 npx -y
  rea-agents@6.5.0 ...` confirms the h09 refusal row.

## Result

47 agree, 0 disagree. Tally row order matches heldout.tsv order one to one for
the slice, and stored recovered_by_rea / inferred_arguments fields match the
envelopes for every row.

Verdict histogram for the slice: right 37, no_name 10, wrong 0.

The ten no_name rows, with cause (all observations, each matches the stored row):

- Rows 61 (b44030ab view7 h07), 65 (f5315a02 thrice h08), 68 (37bdeecc h11),
  69 (3f9cdbf7 h11), 79 (07bf89ab computeTxHash h15), 87 (a8c162fb execute h15):
  openchain returned `{"0x<sel>":null}` (file body
  `{"ok":true,"result":{"function":{"0x<sel>":null},"event":{}}}`), so zero
  unfiltered candidates, correct no_name.
- Row 66 (395c1d44 useIt h09): h09's REA run exited 1 (unlinked library
  placeholder, runs.tsv exit column 1; envelope is an error record with no
  normalized_result), so the row is not recovered and the counter emits no name
  by rule, regardless of what openchain says (openchain also returned null).
  Correct no_name.
- Rows 84 (59bf77df h15), 85 (797af627 h15), 88 (d9caa3d2 h15): the sole
  unfiltered openchain candidate equals the abi_signature
  (`confirmationCount(bytes32)`, `confirm(bytes32)`, `submit(bytes32)`), but the
  h15 envelope infers `uint256` for these selectors while the candidates take
  `bytes32`, so the args gate marks them `args-mismatch` and the rule yields
  no_name. The tally rows record inferred_arguments `uint256`; I confirmed that
  string is what the h15 envelope carries. This is a faithful, conservative
  application of the primary rule (REA argument inference mistyped bytes32 as
  uint256 on three h15 getters); it counts against the rule's recall but the
  stored verdicts are what the rule produces. Not a defect in the tally.

Notable checks that held:

- Row 67 (42966c68 h10): openchain lists two unfiltered candidates,
  `burn(uint256)` and `collate_propagate_storage(bytes16)`. js-sha3 confirms
  both hash to 42966c68 — a genuine keccak collision in the dataset. The
  primary rule keeps only the args-consistent `burn(uint256)` and calls it
  right; the fourbyte_first wrong_name entry for this selector in tally.json is
  a different rule's output and is outside my verdict scope but consistent with
  the data.
- Rows 48-54 (h06 f09..f13 family) and 89-94 (h16): each openchain response
  holds exactly one unfiltered candidate equal to truth; all stored right.

## Residual risk / gaps

- I verified the primary rule verdict only; the four other rule_outputs columns
  in each row were not re-derived (their names sit outside this slice's
  assignment). Observed none inconsistent, but not systematically checked.
- `no_name` correctness for absent-candidate rows rests on the recorded null
  response body; I did not refetch openchain (no lookup budget spent; 0
  requests).
- h15 uint256-vs-bytes32 typing: whether REA's inferred_arguments are wrong or
  merely coarse is a claim-level question, not a tally defect.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ReviewTallySlice2/)

- verify-slice.py  sha256 b21933f0cc315a8fed83bd546cc74faad5ba6c29427c5da9b31f241d195d51a6  the verifier
- recheck.json     sha256 d4deb92fdd456d58394b2a419355c167874cc0e8262047719172457ed164795d  per-row detail (candidates, labels, stored vs recomputed)
- package.json / node_modules  npm js-sha3 0.13.0, independent keccak check

## Tooling installs

- npm package js-sha3 0.13.0 into the scratch dir above (channel: npm install,
  local project install), reason: independent keccak-256 spot check. No pacman
  transactions (host-wide pause honored).

## Verdict

Slice 48-94 of tally.json holds: 47 rows reviewed, 47 verdicts agree with the
evidence, 0 disagreements.
