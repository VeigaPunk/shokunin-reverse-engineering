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

`filterResponse` (`handlers.ts:39-66` at both `0966a3bc` and `189cd726`) looks up each selector's
entry in `canonical-signatures.json` (`:44-45`) and sets, for every candidate under a listed key,
`filtered = name !== expectedCanonical.signature` (`:47-48`). Every other candidate keeps
`filtered: false`. Two consequences follow from the code:

- A key with no `signature` (the 5 `system:magic` keys such as `0x60806040`, the usual start of
  creation code) makes the comparison `name !== undefined`, so every candidate under it is
  filtered. The round-28 entry predicted this from the code (its `:24`) with no fetched data for
  it; this round tests it.
- When the kept signature is not among the stored candidates, every candidate under that key is
  filtered, and a `filter=true` request returns nothing for it.

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

How much each branch tests (wave-1 critic `CriticHeldOutC2`): only `mismatches` can falsify the
rule; `predicted_true >= 1` is computed from names and the list, never from the observed flag, so
it is a coverage guard, not a test. Of the 53 canonical-set entries, 37 under 15 keys whose kept
signature was among the returned candidates test the name-versus-kept-signature comparison (22
predicted true, 15 false); 16 under 7 keys (2 `system:magic`, 5 mis-keyed, below) are filtered
because the key is listed at all. The 199 c1 entries test only the "false outside the list"
branch, which round 28 had already checked; they also rule out the rivals in the Separation
section.

Cases the rule predicted that round 28 had not seen:
- `0x60806040` (`system:magic`): 6 candidates, all spam-like names, all `filtered: true`;
  `0x60a06040`: 4 of 4.
- 5 keys whose kept signature is for another selector (next section): every returned candidate
  was filtered, as predicted.

## Mis-keyed list entries (post-fetch reading of the pinned list, not counted)

After the fetch the L1 hashed every kept signature of the pinned list (first 4 bytes of
keccak-256, the round-25 resolver's `selector_of`; receipt
`.ufo/waves/round-29/after/canonical-keyhash.txt`; re-derived with OpenSSL and pycryptodome by
wave-1 seats `CriticMisKeyed` and `ExecCanonicalHash`). **6 of the 31 kept signatures do not hash to
their own key**:

| key | kept signature (hashes to) | stored candidates (all `filtered: true`) | is the true name hidden? |
|---|---|---|---|
| `0x0d0f30c6` | `token1()` (`0xd21220a7`) | none | no candidate is stored, so nothing is hidden |
| `0x1a686502` | `uniswapV3SwapCallback(int256,int256,bytes)` (`0xfa461e33`) | `liquidity()` | yes: `liquidity()` is declared in Uniswap v3-core `IUniswapV3PoolState` (seat `CriticMisKeyed`) |
| `0x89035730` | `flash(address,uint256,uint256,bytes)` (`0x490e6cbc`) | `parameters()` | yes: `IUniswapV3PoolDeployer` (same seat) |
| `0xc45a0155` | `mint(address,int24,int24,uint128,bytes)` (`0x3c8a7d8d`) | `factory()` and one spam-like name | yes: `factory()`, which R29-C1 carrier n06 (`UniV2Pair`) holds under this selector |
| `0xfc6f7865` | `uniswapV3MintCallback(uint256,uint256,bytes)` (`0xd3487997`) | `collect((uint256,address,uint128,uint128))` | yes: v3-periphery `INonfungiblePositionManager` (same seat) |
| `0x8abf6077` | `proxyOwner()` (`0x025313a2`) | `impl()` | inference only: `impl()` is the only stored preimage; no declaring source was opened |

All 252 candidates fetched here hash to their own selector, so under a mis-keyed key no candidate
can equal the kept string. A side effect (seat `CriticMisKeyed`): `token1()`'s real selector
`0xd21220a7` is not a canonical key, so its three spam-like candidates stay unfiltered beside
`token1()` (R29-C1 lookup `corpus/evidence/round-29/c1/db/openchain-d21220a7.json`).

## What this means

- The round-25 naming rules' filter step is inert for any selector outside the 36 keys: the
  rule predicts `false` there, and all 199 c1 entries here are `false`.
- For a canonical key, `filtered` is not a spam score: it means "differs from the one string
  Sourcify stored". If the deployed list equals the pinned one, a rule that drops filtered
  candidates can never return `factory()` for `0xc45a0155`, or `liquidity()`, `parameters()`,
  `collect(...)` for the other mis-keyed keys. Before trusting a canonical key, check that its
  kept signature hashes to it.

## Separation (what a different service would have shown)

A service that set `filtered` from `hasVerifiedContract`, or marked every non-first candidate,
would have shown mismatches on the c1 set, where the rule predicts `false` for all 199 entries
and several selectors have spam collisions (for example `0x7ecebe00` has 3 candidates). A service
applying a list whose kept signature differs on one of the 15 keys whose kept signature was
returned would have shown mismatches there; on the 4 keys with no candidate and the 7 keys where
every candidate is filtered, a different kept string that matches no candidate gives the same
flags. A list equal to the pinned one on these keys but different on the other 10 is not
separated by this test.

## Limits

- The deployed revision behind `api.openchain.xyz` is assumed; master and staging carry the same
  code and list on 2026-10-22 (S087).
- One fetch instant; says nothing about result order or `hasVerifiedContract`.
- The 26 canonical keys are all of the unanswered ones, not a sample; the c1 set is R29-C1's
  selectors, which share that claim's freeze.
- The counter counts files under `corpus/evidence/round-29/c2/db/`; it cannot tell its own fetch
  from a copy of R29-C1's lookups of the same URLs, whose bodies are byte-identical (seat
  `CriticSeparability`). The two fetches ran as separate processes; their stdout logs are
  `.ufo/waves/round-29/after/c2-fetch.log` and `c1-lookups.log`.
- The mis-keyed count is a post-fetch reading by the L1, not a counter output.

## Use

Treat `filtered: true` as "this selector has a Sourcify-chosen canonical string and this candidate
is not it". For a selector outside the 36-key list the flag carries no information. For
`system:magic` keys every candidate is filtered. For `0x1a686502`, `0x89035730`, `0x8abf6077`,
`0xc45a0155` and `0xfc6f7865` the kept string belongs to another selector, so a filtered candidate
there may still be the true name.
