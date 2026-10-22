source: S087 Sourcify 4byte service filterResponse code and canonical list on the staging head `0966a3bc` (byte-identical to S084/S085 at master `189cd726`)
verified-at: 2026-10-22, round 29 (R29-C2); 178 openchain `filter=false` responses fetched 2026-10-22T20:03:21Z–20:06:17Z, every one HTTP 200 on its first try, after the claim froze at lane commit dbd87cfa; manifest with sha256 per response in `corpus/evidence/round-29/c2/db/manifest.json`
recheck: python3 -I -B tools/round-29/c2-filtered-unseen.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV> (offline over committed bytes; expected `responses_complete=178/178 entries=252 mismatches=0 predicted_true=38 predicted_false=214 entry_ok=1`, exit 0)

# openchain's `filtered` flag, predicted from code on 178 selectors the lane had never fetched: mismatches 0 of 252 entries

The round-28 entry (`corpus/knowledge/2026-10-22-r28-openchain-filtered-flag.md`) read the rule
from Sourcify's code and checked it on 230 selectors, but 168 of them had already been answered in
the lane before that freeze, and all of its predicted-true entries came from selectors a pre-freeze
probe had scored (mistake M28-4). Its agreement was a re-observation. This round repeats the test
on selectors with no openchain response anywhere in the lane at the base, frozen before any fetch.

## Rule (code, S087; unchanged from S084)

`filterResponse` (`handlers.ts:39-66` at both `0966a3bc` and `189cd726`) sets, for every
candidate under a selector that is a key of `canonical-signatures.json`,
`filtered = name !== expectedCanonical.signature` (`:47-48`). Every other candidate keeps
`filtered: false`. Three consequences the round-28 entry did not state:

- A key with no `signature` (the 5 `system:magic` keys such as `0x60806040`, the usual start of
  creation code) makes the comparison `name !== undefined`, so every candidate under it is
  filtered.
- When the kept signature is not among the stored candidates, every candidate under that key is
  filtered, and a `filter=true` request returns nothing for it.
- **6 of the 31 kept signatures do not hash to their own key** (first 4 bytes of keccak-256 of
  the signature, computed with the round-25 resolver's `selector_of` over the S087 bytes):
  `0x0d0f30c6` keeps `token1()` (which is `0xd21220a7`), `0x1a686502` keeps
  `uniswapV3SwapCallback(int256,int256,bytes)` (`0xfa461e33`), `0x89035730` keeps
  `flash(address,uint256,uint256,bytes)` (`0x490e6cbc`), `0xc45a0155` keeps
  `mint(address,int24,int24,uint128,bytes)` (`0x3c8a7d8d`), `0xfc6f7865` keeps
  `uniswapV3MintCallback(uint256,uint256,bytes)` (`0xd3487997`) and `0x8abf6077` keeps
  `proxyOwner()` (`0x025313a2`). Every stored candidate hashes to its selector (all 252 entries
  fetched here do), so under these 6 keys no candidate can equal the kept signature and every
  candidate, including the true name, is filtered.

## Test (R29-C2, frozen at dbd87cfa, fetched once after)

Test set (`corpus/evidence/round-29/c2/selectors.tsv`, 178 selectors):
- `canonical` (26): the canonical keys with no openchain response in the lane at the base
  (`tools/round-29/preseen.py --kind flag` → `overlap=0`, exit 0; the other 10 keys were answered in
  rounds 25 and 28 and were left out).
- `c1` (152): the R29-C1 held-out selectors, none a canonical key.

| set | selectors | entries | predicted filtered | observed filtered | mismatches |
|---|---|---|---|---|---|
| canonical | 26 | 53 | 38 | 38 | 0 |
| c1 | 152 | 199 | 0 | 0 | 0 |
| all | 178 | 252 | 38 | 38 | **0** |

Counter output: **mismatches 0 of 252 entries**, `predicted_true=38`, `predicted_false=214`. Both
branches hold unseen data. 4 canonical keys returned no candidate (`0x0d0f30c6`, `0x60c06040`,
`0x60e06040`, `0x61010060`).

Cases the rule predicted that round 28 had not seen:
- `0x60806040` (`system:magic`): 6 candidates, all spam-like names, all `filtered: true`;
  `0x60a06040`: 4 of 4.
- The mis-keyed entries: 5 of the 6 returned candidates and every one was filtered, as predicted:
  `0x1a686502` (only candidate `liquidity()`), `0x89035730` (`parameters()`), `0x8abf6077`
  (`impl()`), `0xfc6f7865` (`collect((uint256,address,uint128,uint128))`), and `0xc45a0155`
  (2 candidates, one of them `factory()`, the function R29-C1 carrier n08 holds under that
  selector). `0x0d0f30c6` returned no candidate.

## What this means

- The round-25 naming rules' filter step is inert for any selector outside the 36 keys (R29-C1:
  0 of 199 entries filtered on its 152 rows).
- For a canonical key, `filtered` is not a spam score: it means "differs from the one string
  Sourcify stored". For the 6 mis-keyed entries that string belongs to another selector, so the
  flag hides every stored name, the true one included: a rule that drops filtered candidates can
  never return `factory()` for `0xc45a0155`. Before trusting a canonical key, check that its kept
  signature hashes to it.

## Separation (what a different service would have shown)

A service that set `filtered` from `hasVerifiedContract`, or marked every non-first candidate,
would have shown mismatches on the c1 set, where the rule predicts `false` for all 199 entries
and several selectors have spam collisions (for example `0x7ecebe00` has 3 candidates). A service
applying a list whose kept signature differs on any of the 26 keys would have shown mismatches
there. A list equal to the pinned one on these 26 keys but different on the other 10 is not
separated by this test.

## Limits

- The deployed revision behind `api.openchain.xyz` is assumed; master and staging carry the same
  code and list on 2026-10-22 (S087).
- One fetch instant; says nothing about result order or `hasVerifiedContract`.
- The 26 canonical keys are all of the unanswered ones, not a sample; the c1 set is R29-C1's
  selectors, which share that claim's freeze. C2 counts only its own fetch.
- The mis-keyed count (6 of 31) is computed by the L1 over the pinned list; it is not a counter
  output and was found after the fetch.

## Use

Treat `filtered: true` as "this selector has a Sourcify-chosen canonical string and this candidate
is not it". For a selector outside the 36-key list the flag carries no information. For
`system:magic` keys every candidate is filtered. For `0x0d0f30c6`, `0x1a686502`, `0x89035730`,
`0x8abf6077`, `0xc45a0155` and `0xfc6f7865` the kept string is for another selector, so a filtered
candidate there may still be the true name.
