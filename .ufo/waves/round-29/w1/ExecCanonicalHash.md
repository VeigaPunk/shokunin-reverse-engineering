# R29 canonical signature hash audit

## Findings

**Observation — verdict: holds.** At revision `18be864a528873b2b70d8c94e31f880290249e90`, 6 of the 31 signature-bearing entries in `canonical-signatures.json` do not Keccak-256 hash to their own key. There are 5 `system:magic` entries (36 entries total). Each computed selector below is the first four bytes of Keccak-256 over the UTF-8 signature.

| Key | Signature | Computed selector |
|---|---|---|
| `0x0d0f30c6` | `token1()` | `0xd21220a7` |
| `0x1a686502` | `uniswapV3SwapCallback(int256,int256,bytes)` | `0xfa461e33` |
| `0x89035730` | `flash(address,uint256,uint256,bytes)` | `0x490e6cbc` |
| `0xc45a0155` | `mint(address,int24,int24,uint128,bytes)` | `0x3c8a7d8d` |
| `0xfc6f7865` | `uniswapV3MintCallback(uint256,uint256,bytes)` | `0xd3487997` |
| `0x8abf6077` | `proxyOwner()` | `0x025313a2` |

**Observation:** All 252 candidate names across the 178 C2 response files hash to their respective selectors; no candidate-name mismatches or malformed candidate names were found.

## Evidence

Producing command: `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecCanonicalHash/venv/bin/python /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecCanonicalHash/audit.py | tee /fast/scratch/hyaku-r29/seats/w1/ExecCanonicalHash/audit-output.json` (run with `set -o pipefail`; script exit captured as `COMMAND_EXIT`). The script reads each input using read-only `git show REV:path` at the pinned revision and hashes with `Crypto.Hash.keccak` (Keccak-256).

Exact output excerpt:

```json
{
  "candidate_mismatch_count": 0,
  "candidate_mismatches": [],
  "candidate_names_hashed": 252,
  "canonical_entry_count": 36,
  "magic_keys": 5,
  "malformed_candidates": [],
  "pycryptodome_version": "4.1.0",
  "responses_read": 178,
  "revision": "18be864a528873b2b70d8c94e31f880290249e90",
  "selectors_count": 178,
  "signature_bearing_keys": 31,
  "signature_mismatch_count": 6,
  "signature_mismatches": [
    {"computed_selector": "0xd21220a7", "key": "0x0d0f30c6", "signature": "token1()"},
    {"computed_selector": "0xfa461e33", "key": "0x1a686502", "signature": "uniswapV3SwapCallback(int256,int256,bytes)"},
    {"computed_selector": "0x490e6cbc", "key": "0x89035730", "signature": "flash(address,uint256,uint256,bytes)"},
    {"computed_selector": "0x3c8a7d8d", "key": "0xc45a0155", "signature": "mint(address,int24,int24,uint128,bytes)"},
    {"computed_selector": "0xd3487997", "key": "0xfc6f7865", "signature": "uniswapV3MintCallback(uint256,uint256,bytes)"},
    {"computed_selector": "0x025313a2", "key": "0x8abf6077", "signature": "proxyOwner()"}
  ],
  "utc": "2026-10-22T20:21:47Z"
}
COMMAND_EXIT=0
```

Input hashes emitted by the same run: `canonical-signatures.json` SHA-256 `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2`; `selectors.tsv` SHA-256 `3a93f7837accb9acd66874707922317d9a8e0f8afb0c9cd87ee79f3d9fa15b5d`; response bundle (path + NUL + bytes, selectors.tsv order) SHA-256 `ba12ecc112e0a717ad75666c7d24fa3a18e2667b340ce654bf634e5a0aba0bed`.

## Tooling and retained artifacts

- Installed `pycryptodome==4.1.0` from PyPI using `uv pip` in a task-local venv, for an independent Keccak-256 implementation. The available `uv` was version `0.13.0`; no other tool installs/updates.
- Script `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecCanonicalHash/audit.py` — SHA-256 `c295495b0eeb77ae87c6f2e9fe7cb9e96b9b039383c6e03bd86863e2d1d34310`.
- Raw output `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecCanonicalHash/audit-output.json` — SHA-256 `089d5e7d8b5f15aac5e972542311c17d7132451376672a5f02afb34d7332f84e`.

No 4byte.directory/OpenChain network lookups, external sources, or REA runs. Risks/blockers: none identified.
