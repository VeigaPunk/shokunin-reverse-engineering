# CriticMisKeyed — round 29, wave 1

Seat `KaidokuR29.CriticMisKeyed` (critic). What I attacked: the "mis-keyed canonical list" finding in
`corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md` (Rule bullet 3, Test "Cases" bullet 2,
What this means bullet 2, Limits bullet 4, Use), plus where it is repeated (`corpus/README.md:80`,
`:176`, `corpus/lessons/round-29.md:36-38`). Lane read at tip `18be864a528873b2b70d8c94e31f880290249e90`.
Read-only. No lane writes other than this report, no git or jj writes, no REA, no 4byte.directory
or openchain requests.

## Overall verdict

- **"6 of 31 kept signatures do not hash to their key": holds** (observation, two independent
  keccak implementations agree).
- **Outside the frozen claim, and labelled so: holds in part.** The Limits section and the lesson
  label it. It fails in two places. The Rule section presents it as a consequence of the code.
  `corpus/README.md:80` puts it in the "held narrowly" verdict cell with no label.
- **"Hides the true name", for each of the 6: holds for 4, holds with weaker evidence for 1
  (`0x8abf6077`), and fails for 1 (`0x0d0f30c6`).** `0x0d0f30c6` stores no candidate, so nothing is
  hidden there.
- **Additional defect:** the entry says carrier **n08** holds `factory()`. It is **n06**
  (`UniV2Pair`). n08 is `UniV2Factory`, which has no `factory()`.

## Evidence

### E1. Keccak check (both implementations)

Command (2026-10-22T20:22:26Z):
`python3 -I -B /fast/scratch/hyaku/kaidoku-r29/seats/w1/CriticMisKeyed/keyhash.py`, exit 0.

The script hashes each kept signature and each returned candidate with OpenSSL 3.6.5
`openssl dgst -keccak-256` and with the lane's `selector_of` (`tools/round-25/a2/resolve-selectors.py:86`).
It aborts if the two disagree. They never disagreed. Self-test:
`transfer(address,uint256)=a9059cbb token1()=d21220a7 ok`.

Excerpt:

```
list_sha256 5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2
keys 36 kept_signatures 31
KEPT 0x0d0f30c6 MISKEYED keccak4(token1())=0xd21220a7
KEPT 0x1a686502 MISKEYED keccak4(uniswapV3SwapCallback(int256,int256,bytes))=0xfa461e33
KEPT 0x89035730 MISKEYED keccak4(flash(address,uint256,uint256,bytes))=0x490e6cbc
KEPT 0xc45a0155 MISKEYED keccak4(mint(address,int24,int24,uint128,bytes))=0x3c8a7d8d
KEPT 0xfc6f7865 MISKEYED keccak4(uniswapV3MintCallback(uint256,uint256,bytes))=0xd3487997
KEPT 0x8abf6077 MISKEYED keccak4(proxyOwner())=0x025313a2
miskeyed 6 of 31 0x0d0f30c6,0x1a686502,0x89035730,0xc45a0155,0xfc6f7865,0x8abf6077
CAND 0x0d0f30c6 <none> result=None
CAND 0x1a686502 liquidity() keccak4=0x1a686502 filtered=True verified=True
CAND 0x89035730 parameters() keccak4=0x89035730 filtered=True verified=True
CAND 0x8abf6077 impl() keccak4=0x8abf6077 filtered=True verified=True
CAND 0xc45a0155 factory() keccak4=0xc45a0155 filtered=True verified=True
CAND 0xc45a0155 transfer_attention_tg_invmru_ec11fa8(uint256,bool) keccak4=0xc45a0155 filtered=True verified=False
CAND 0xfc6f7865 collect((uint256,address,uint128,uint128)) keccak4=0xfc6f7865 filtered=True verified=True
candidate_entries 252 candidate_hash_mismatches 0
```

Observations:
- The other 25 kept signatures hash to their key.
- The list bytes equal the frozen pin (`5572beb5…`, claims.json `loaded_by_counter`) and S085/S087.
- All 252 candidate entries hash to their own selector, which confirms the entry's "all 252 entries
  fetched here do".
- The six response files and `openchain-d21220a7.json` match their manifest sha256 (`sha256sum`,
  2026-10-22T20:24:39Z). Example: `openchain-c45a0155.json` =
  `687a3960aaf74bad3930c75804fbb701223f38accba0c1e893e56818087052da`.

### E2. The comparison really is by key (S087 re-opened)

`curl` https://raw.githubusercontent.com/argotorg/sourcify/0966a3bcf13a46b335dae390a0c95b3b0d980c69/services/4byte/src/api/handlers.ts
(2026-10-22T20:23:10Z): HTTP 200, sha256 `30981efbc7bc1b541954eb75767c8154562f4f77a9bfc1ad22cf19c8996c5a38`
(equal to S087). Quotes:
- `:44` `const expectedCanonical = canonicalSignatures[hash];`
- `:45` `if (expectedCanonical !== undefined && response[type][hash] !== null) {`

Observation: the lookup is keyed by the selector, and an exact string compare follows (`:47-48`).
So a kept signature that hashes elsewhere can never match a candidate whose hash is the key.

Observation: by `:45`, a `null` response skips filtering. That is what `0x0d0f30c6` returned
(`{"0x0d0f30c6": null}`) on a `filter=false` request. No candidate is stored there; none was hidden.

### E3. Primary sources for the true names

`git ls-remote` (2026-10-22T20:23:02Z):
- Uniswap/v3-core `refs/heads/main` = `aab5aa019b5acb312acc01aff7f03a1b09755197`
- Uniswap/v3-periphery `refs/heads/main` = `7c8367c896ec8514198a8c03e5b0668c8b207a79`

Files fetched by `curl` at 2026-10-22T20:23:10Z, all HTTP 200, accessed 2026-10-22:

| URL | sha256 | located quote (line) |
|---|---|---|
| https://raw.githubusercontent.com/Uniswap/v3-core/aab5aa019b5acb312acc01aff7f03a1b09755197/contracts/interfaces/pool/IUniswapV3PoolState.sol | `d8d3937703d08d95f7f867a0f49c2aa73c3f3ef5508a54d431e829295f5175ea` | `function liquidity() external view returns (uint128);` (:48) |
| https://raw.githubusercontent.com/Uniswap/v3-core/aab5aa019b5acb312acc01aff7f03a1b09755197/contracts/interfaces/pool/IUniswapV3PoolImmutables.sol | `ac6332f7e174db7fa3852a6c5ae3da3bd013e72c2ff8fa1cf2ec37f6916e2951` | `function factory() external view returns (address);` (:9) |
| https://raw.githubusercontent.com/Uniswap/v3-core/aab5aa019b5acb312acc01aff7f03a1b09755197/contracts/interfaces/IUniswapV3PoolDeployer.sol | `48908460f444abc497b261e38a38540effecbf5c99d17e60d849f1d0acfb1fe6` | `function parameters()` (:16) |
| https://raw.githubusercontent.com/Uniswap/v3-periphery/7c8367c896ec8514198a8c03e5b0668c8b207a79/contracts/interfaces/INonfungiblePositionManager.sol | `42fceb0c7981931bc7c190e9fcfe65feafe22604eb57ab1cbd61a76288f3c387` | `function collect(CollectParams calldata params) external payable returns (uint256 amount0, uint256 amount1);` (:173) |

For `collect`, the struct `CollectParams` (`:159-163`) has members `uint256 tokenId; address
recipient; uint128 amount0Max; uint128 amount1Max;`. Its canonical form is therefore
`collect((uint256,address,uint128,uint128))`, the candidate openchain returned.

The list itself tags all five Uniswap keys `"source": "protocol:uniswap"`
(`canonical-signatures.json`).

### E4. No preimage found for `0x0d0f30c6`

Command (2026-10-22T20:22Z, rerun with output saved at 20:24Z):
`python3 -I -B .../CriticMisKeyed/guess.py`, exit 0. Output: `tried 89`, no `HIT`.

What it tried: 89 Uniswap V2/V3 core and periphery signatures and common proxy or pool getters,
hashed offline. Result: unknown. The lane holds no preimage; openchain stores none (E2).

### E5. Which carrier holds `factory()`

Commands at 2026-10-22T20:23:36Z, over `corpus/evidence/round-29/c1/`: `grep` the carrier sources
and check `factory` in each `compiled/*.abi.json`.

Excerpts:
- `src/UniV2Pair.sol:17:    function factory() external { v_uint256 = block.number; }`
- `compiled/UniV2Pair.abi.json True`; every other ABI, including `compiled/UniV2Factory.abi.json`, is `False`.
- `carriers.tsv` rows: `n06 …/UniV2Pair.runtime.hex`, `n08 …/UniV2Factory.runtime.hex`.

Observation: the entry's "the function R29-C1 carrier n08 holds under that selector" (`:60`) is
wrong. It is n06.

Inference: a lane-compiled stub is weak naming evidence anyway, because the lane typed the name
itself from a published list. The Uniswap V3 source in E3 is the primary evidence.

### E6. The other side of the mis-keying (observation in committed data)

`corpus/evidence/round-29/c2/db/openchain-d21220a7.json` (sha256 `367199c2…2276`, manifest equal)
is the response for token1()'s real selector. It holds `token1()` plus
`detectabilityAntiauthoritarianism()`, `join_tg_invmru_haha_a906df4(bool,bool)` and
`watch_tg_invmru_6092201(bool,address,uint256)`. All four are `"filtered":false`.

Inference: because `token1()` was filed under the wrong key, Sourcify does not filter the spam at
the selector it presumably meant to protect. The entry does not state this. Of the six intended
selectors, only `0xd21220a7` is in the lane data; the other five are unknown.

## Verdict per key

All six are mis-keyed (E1).

**`0x0d0f30c6`** (keeps `token1()`, which is `0xd21220a7`)
- Mis-keyed: holds.
- Hides the true name: **fails.** openchain stores no candidate (`null`, E2), so nothing is hidden.
- True name: unknown. No stored candidate, and the 89 offline guesses found no preimage (E4).

**`0x1a686502`** (keeps `uniswapV3SwapCallback(int256,int256,bytes)`, which is `0xfa461e33`)
- Mis-keyed: holds.
- Hides the true name: **holds.**
- True name: `liquidity()`. It hashes to the key, it is the sole candidate, openchain marks it
  `hasVerifiedContract: true`, and v3-core `IUniswapV3PoolState.sol:48` declares it.
- Label: observation (hash, response); inference that it is the intended function.

**`0x89035730`** (keeps `flash(address,uint256,uint256,bytes)`, which is `0x490e6cbc`)
- Mis-keyed: holds.
- Hides the true name: **holds.**
- True name: `parameters()`. It hashes to the key, it is the sole candidate, `hasVerifiedContract:
  true`, and v3-core `IUniswapV3PoolDeployer.sol:16` declares it.
- Label: observation plus inference, as above.

**`0xc45a0155`** (keeps `mint(address,int24,int24,uint128,bytes)`, which is `0x3c8a7d8d`)
- Mis-keyed: holds.
- Hides the true name: **holds.** The second candidate,
  `transfer_attention_tg_invmru_ec11fa8(uint256,bool)`, also hashes to the key and is filtered too.
  Here the filter hides the real name and the spam alike.
- True name: `factory()`. It hashes to the key, it is the only candidate with
  `hasVerifiedContract: true` (the other is `false`, with the `tg_invmru` spam pattern also seen at
  `0xd21220a7`), and v3-core `IUniswapV3PoolImmutables.sol:9` declares it.
- The carrier is **n06**, not n08 (E5).

**`0xfc6f7865`** (keeps `uniswapV3MintCallback(uint256,uint256,bytes)`, which is `0xd3487997`)
- Mis-keyed: holds.
- Hides the true name: **holds.**
- True name: `collect((uint256,address,uint128,uint128))`. It hashes to the key, it is the sole
  candidate, `hasVerifiedContract: true`, and v3-periphery `INonfungiblePositionManager.sol:159-173`
  declares it.

**`0x8abf6077`** (keeps `proxyOwner()`, which is `0x025313a2`)
- Mis-keyed: holds.
- Hides the true name: **holds, with weaker evidence.**
- True name: `impl()` is the only stored preimage, it hashes to the key, and it has
  `hasVerifiedContract: true`. No primary source declaring it was opened.
- Label: "true name" here is an inference from the sole verified preimage.

## Scope and labelling

The frozen claim (`.ufo/waves/round-29/claims.json`, R29-C2 `statement`) covers only "filtered is
true exactly when … the name differs from that key's signature". Its predictions do not depend on
whether a kept signature hashes to its key. So the mis-keyed count lies outside the claim. It is a
post-fetch reading of a pinned input.

Where it is labelled:
- **Labelled:** entry Limits `:89-90` ("computed by the L1 over the pinned list; it is not a counter
  output and was found after the fetch").
- **Labelled:** `corpus/lessons/round-29.md:36-38` ("Gate note (after the fetch, by the L1) … not a
  counter output").
- **Not labelled:** entry Rule section `:24-34`. It sits under "Rule (code, S087…)" as one of "three
  consequences", bolded. It is a property of the list's data, not a consequence of the code.
- **Not labelled:** `corpus/README.md:80`. The index row's "held narrowly" cell carries "6 of the
  31 kept canonical signatures do not hash to their key" next to the counted results, with no
  post-hoc mark. A reader would take it as part of what was held.
- **No receipt:** nothing in `.ufo/waves/round-29/after/` or the lane computes the 6-of-31 count
  (`git grep` for `fa461e33`, `025313a2`: no file outside the c1/c2 data). The entry's provenance,
  "computed with the round-25 resolver's `selector_of`", has no command or output behind it.

## Wording the entry should use

1. **Move the third Rule bullet** out of "Rule (code…)" into its own section, for example
   "## Reading of the pinned list (after the fetch; not counted)":

   > Over the pinned list (sha256 `5572beb5…`), 6 of the 31 kept signatures do not hash to their
   > key (first 4 bytes of keccak-256; L1 reading after the fetch, receipt `<path>`; not a counter
   > output and not part of R29-C2): `0x0d0f30c6` keeps `token1()` (`0xd21220a7`), `0x1a686502`
   > keeps `uniswapV3SwapCallback(int256,int256,bytes)` (`0xfa461e33`), `0x89035730` keeps
   > `flash(address,uint256,uint256,bytes)` (`0x490e6cbc`), `0xc45a0155` keeps
   > `mint(address,int24,int24,uint128,bytes)` (`0x3c8a7d8d`), `0xfc6f7865` keeps
   > `uniswapV3MintCallback(uint256,uint256,bytes)` (`0xd3487997`), `0x8abf6077` keeps
   > `proxyOwner()` (`0x025313a2`). Every candidate fetched here hashes to its selector, so under
   > these keys no candidate can equal the kept string, and the rule filters every stored candidate.
   > At this fetch that was 6 entries under 5 keys; `0x0d0f30c6` stores none.

2. **Replace "every candidate, including the true name, is filtered"** with:

   > Under 4 of these keys the filtered candidate is the function the list's `source` tag names:
   > `liquidity()`, `factory()` and `parameters()` (Uniswap v3-core interfaces) and
   > `collect((uint256,address,uint128,uint128))` (v3-periphery), each hashing to its key and
   > marked `hasVerifiedContract: true`. Under `0x8abf6077` the only candidate, `impl()`, is filtered.
   > It is the sole verified preimage, but no source declaring it was opened. `0x0d0f30c6` stores no
   > candidate, so nothing is hidden there; its preimage is unknown.

3. **Fix `:60`:** change "the function R29-C1 carrier n08 holds under that selector" to "the function
   R29-C1 carrier n06 (`UniV2Pair`) holds under that selector". Better still, cite the Uniswap V3
   interface as the evidence and the carrier only as a cross-check.

4. **Make "can never return `factory()`" (`:70`) conditional:** "while the deployed list matches the
   pinned one, a rule that drops filtered candidates cannot return `factory()` for `0xc45a0155`"
   (inference).

5. **Use section (`:96-97`):** change "the kept string is for another selector" to "the kept string
   hashes to another selector". Name only the five keys with stored candidates as places where a
   filtered candidate may be the true name. Add: "and at the selector a kept string really hashes to
   (seen at `0xd21220a7`), spam candidates stay unfiltered."

6. **`corpus/README.md:80`:** move the mis-keyed clause out of the "held narrowly" cell, or prefix it
   "(post-fetch list reading, not counted)".

7. **Receipt:** commit a receipt for the 6-of-31 computation. `keyhash.out` below can serve; it uses
   two implementations and cross-checks them.

Impacted axes:
- R29-C2 depth: provenance and labelling only. The counted result
  (`mismatches=0` of 252) is unaffected by any finding here.
- Entry accuracy: the n08/n06 mix-up and the `0x0d0f30c6` overstatement.

The defects are fixable wording problems, not a tradeoff the judge must reject. Inference: none of
them changes the R29-C2 counter result.

## Artifacts (`/fast/scratch/hyaku/kaidoku-r29/seats/w1/CriticMisKeyed/`)

| file | sha256 |
|---|---|
| keyhash.py | `5a6b5dea25c9224f6f4112566cd98cc7f7159db3a8103072113c18929f9a459c` |
| keyhash.out | `e500487c23067441b84f435894e1c2245e3769d5106467369c191df6c7b08627` |
| guess.py | `355560ea757b7f8e0f13c622f1722b5bfc46dc8d286f9065b99c37643bc0a978` |
| guess.out | `36ff94ae74601e5635f3019e75aa29e18df2cc76fb025638a5de57c641332a8c` |
| src/IUniswapV3PoolState.sol | `d8d3937703d08d95f7f867a0f49c2aa73c3f3ef5508a54d431e829295f5175ea` |
| src/IUniswapV3PoolImmutables.sol | `ac6332f7e174db7fa3852a6c5ae3da3bd013e72c2ff8fa1cf2ec37f6916e2951` |
| src/IUniswapV3PoolDeployer.sol | `48908460f444abc497b261e38a38540effecbf5c99d17e60d849f1d0acfb1fe6` |
| src/INonfungiblePositionManager.sol | `42fceb0c7981931bc7c190e9fcfe65feafe22604eb57ab1cbd61a76288f3c387` |
| src/handlers.ts | `30981efbc7bc1b541954eb75767c8154562f4f77a9bfc1ad22cf19c8996c5a38` |

## Tooling and process notes

- Installs: none. I used the host's OpenSSL 3.6.5 KECCAK-256 and the lane's pure-Python keccak.
- `skill://godspeed` could not be resolved from this harness; no `godspeed/SKILL.md` exists on the
  host filesystem (`find / -xdev -path '*/godspeed/SKILL.md'`: no output). I proceeded under the
  assignment contract.
- Network: only `git ls-remote` of three public repositories and `curl` of five raw files. No
  4byte.directory or openchain requests.
