# R28-C2 review: the 59 predicted_true entries (seat KaidokuR28a2.ReviewPredictedTrue)

Date 2026-10-22. Scope: the candidate entries in corpus/evidence/round-28/c2/db/
with `filtered=true`, and canonical-key entries with `filtered=false`, each checked
against corpus/evidence/round-28/c2/canonical-signatures.json (pin
5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2, verified).
Rule under test: filtered=true exactly when the selector is a canonical key and
the candidate name differs from the canonical signature string (comparison is the
full signature string, same operationalization as the counter's `pred`).

## Verdict

HOLDS. Both lists verify with zero exceptions at two revisions
(a267311678309fd17772407e8afa122ec3219289 and lane tip
9db24c9e10287d44d9f780d782ab608f3c84ff5a); the lists are byte-identical.

## Counts (acceptance)

- List 1, filtered=true candidates: 59 of 59 confirmed (selector is a canonical
  key AND name differs from the canonical signature). Matches counter
  predicted_true=59.
- List 2, canonical-key entries with filtered=false: 10 of 10 confirmed (name
  equals the canonical signature). Full list below.
- Exceptions: 0. No filtered=true entry with a non-canonical selector or an
  equal name; no canonical filtered=false entry with a differing name; no
  non-boolean `filtered` value. Across all 246 entries the biconditional
  (filtered=true iff canonical key and name differs) holds exactly.

## Method and evidence

1. Independent script (no counter code reused) read selectors.tsv (230 rows,
   pin ad1b50982922ed69... verified), the pinned canonical file (36 keys), and
   each of the 230 db/openchain-*.json files, trusting a file only after its
   tree sha256 matched the manifest.json committed at the reviewed revision.
   Command: `./check-predicted-true.py a2673116...`; exit 0;
   excerpt `responses_ok=230/230 entries=246` / `list1_filtered_true=59` /
   `list2_canonical_filtered_false=10` / `non_boolean_filtered=0 exceptions=0`;
   2026-10-22T18:25:51Z. Observation.
2. Same script at tip 9db24c9e...: exit 0, identical counts and identical list
   lines (diff empty, `LISTS_IDENTICAL`); 2026-10-22T18:26:12Z. Observation.
3. Counter reproduction, read-only git show: `python3
   tools/round-28/c2-filtered-flag.py --root LANE --rev a2673116... --base
   935c3660...`; exit 1; excerpt `responses_complete=230/230 entries=246
   mismatches=0 predicted_true=59 entry_ok=0` plus `FAIL entry absent`
   (the knowledge entry/SOURCES/Gate landing is the known entry_ok=0 gap, not in
   this item's scope); 2026-10-22T18:26:34Z. Observation.
4. Lane working tree had 7 dirty paths at review time (other seats' drafts);
   immaterial here because every db byte was checked against committed manifest
   sha256 and the canonical file against its pin. Observation.

## List 2 in full (canonical key, filtered=false, name equals canonical)

0x06fdde03 name() · 0x095ea7b3 approve(address,uint256) · 0x18160ddd
totalSupply() · 0x23b872dd transferFrom(address,address,uint256) · 0x313ce567
decimals() · 0x70a08231 balanceOf(address) · 0x8da5cb5b owner() · 0x95d89b41
symbol() · 0xa9059cbb transfer(address,uint256) · 0xdd62ed3e
allowance(address,address) — all src=standard:erc20 except 0x8da5cb5b
(standard:ownable).

List 1 (59 lines) is in artifact out-head.txt (grep '^TRUE '); exemplars:
0x06fdde03 has four candidates — three junk names such as
`__$$____$_$___$_$_$_$_$__$$___()` and `message_hour(uint256,int8,uint16,bytes32)`
(filtered=true, differ from canonical `name()`) plus the true `name()`
(filtered=false, equal). This placeholder-style name parallels the C1 h09
unlinked-library placeholder pattern; it is genuine openchain data and the rule
classifies it correctly. Observation.

## Findings by severity

- Blocking: none.
- Major: none.
- Minor: none in scope. Note only: canonical-signatures.json holds 36 keys and
  69 canonical-key candidate entries appear across the 230 responses (59 true +
  10 false), so several canonical selectors carry multiple junk candidates; this
  is data shape, not a rule defect.

## Residual risk and verification gaps

- I did not diff the pinned canonical-signatures.json against upstream sourcify
  commit 189cd726f7ed8fb3d2f503402d5c133e0f50e1fd; that identity belongs to the
  S084/S085 source rows (L1). Inference: if the pin is faithful, the claim's
  upstream premise stands; I verified only the pinned copy.
- No openchain/4byte refetch was made (out of this item's scope; network quota
  unused). Unknown: whether openchain would return the same candidates today.
- Conclusion "rule holds on this dataset" is observation; generalization beyond
  the 230 fetched selectors is inference.

## Artifacts (under /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ReviewPredictedTrue/)

- check-predicted-true.py (verification script) sha256
  34d1f2e2f981c954b107877ee5ae5194e21cdee90e9735655c9a8f67818af054
- out-a2673116.txt (full lists at dispatch rev) sha256
  839237fcf05c00af2f247b71351abc3a5ce974e80b3083fabecce6772fc2bece
- out-head.txt (full lists at tip) sha256
  ec1a06eef090ac5dff0dd12f8e334c833d85b6866bef981352f20aaff4b796a7
- counter-a2673116.txt (counter reproduction) sha256
  a018cb84dd9217a22fe6e3554deadbf10ae0b55b71ef1df3cbb92fde22a64476

No tools were installed or upgraded (existing python3 sufficed). The lane was
touched only by this report file; no refs, index or jj state were modified.
