# C2: independent Keccak-256 labels for every saved candidate and every ABI signature

Seat KaidokuR25a3.C2IndependentKeccak. Round 25 attempt 3, wave 1. Lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin, read-only except this report. Offline only: saved lookups in `corpus/evidence/round-25/a2/c2/*/db/`, the six REA envelopes and the six carrier ABIs. No network request was made.

## Verdict

**Holds.** Every Keccak label in the C2 chain reproduces under an implementation independent of the lane resolver. 344 candidate instances (99 distinct texts) over 37 selectors that have candidates: 0 Keccak mismatches, 0 disagreements with the resolver's per-candidate labels, 0 disagreements with the resolver's five naming-rule outputs or with the committed `tally.json`. 69 of 69 ABI functions hash to a selector in the REA selector set of their carrier; 0 REA functions lack an ABI signature.

## Independent implementation

- **pycryptodome 4.1.0** (`Crypto.Hash.keccak`, `digest_bits=256`), scratch venv via `uv venv` + `uv pip install pycryptodome` (PyPI). Python 3.15.0.
- **@noble/hashes 2.4.0** (`keccak_256`), `npm install --prefix <seat>/npm @noble/hashes` (npm registry). Node v24.21.0.

The lane resolver (`tools/round-25/a2/resolve-selectors.py`) carries its own pure-Python Keccak. Its `keccak256()` returns all 4 state words (32 bytes, full Keccak-256, not a truncation) and is not NIST SHA3-256 (`hashlib.sha3_256(b"transfer(address,uint256)")[:8]` is `4b40e901`, Keccak is `a9059cbb`). Known-answer vectors for `""`, `transfer(address,uint256)`, `balanceOf(address)`, `approve(address,uint256)` and `transferFrom(address,address,uint256)` agree in all three implementations.

## Counts

Per carrier, over all saved responses in `db/` (4byte.directory page 0 and openchain `filter=false`):

| carrier | candidates | keccak match | keccak mismatch | 4byte | openchain | ABI funcs | ABI sel. in REA | REA funcs w/o ABI |
|---|---|---|---|---|---|---|---|---|
| rv2token | 70 | 70 | 0 | 22 | 48 | 5 | 5 | 0 |
| kdxtoken | 74 | 74 | 0 | 24 | 50 | 6 | 6 | 0 |
| vaultb-opt200 | 30 | 30 | 0 | 14 | 16 | 13 | 13 | 0 |
| carrierb | 16 | 16 | 0 | 8 | 8 | 8 | 8 | 0 |
| stewardtoken | 125 | 125 | 0 | 47 | 78 | 22 | 22 | 0 |
| carrierv | 29 | 29 | 0 | 13 | 16 | 15 | 15 | 0 |
| **total** | **344** | **344** | **0** | **128** | **216** | **69** | **69** | **0** |

37 distinct selectors carry candidates; 6 distinct selectors (7 carrier rows) carry none: `3efdef66`, `0c751377`, `e0749a6a`, `875194ac`, `cee38a15`, `d869f754`. 99 distinct candidate texts; no text appears under two different queried selectors.

## Disagreements with the resolver: none. Three comparisons, all zero.

1. Per candidate: 344 candidates against the labels in `corpus/evidence/round-25/a3/c2/analyze/<carrier>.json`. Resolver labels `keccak-mismatch` / `args-mismatch` / `consistent`; I recomputed the Keccak part with pycryptodome and the parameter-list part with my own top-level parameter splitter. 0 disagreements on the Keccak verdict, 0 on the full three-way label.
2. Resolver Keccak versus mine over all 344 candidate texts: 0 disagreements. `selector_of` and `keccak256(text)[:4]` return the same 8 hex characters for every one of the 344 texts and for all 69 ABI canonical signatures.
3. Rule outputs: I re-implemented the five naming rules of `tools/round-25/a3/tally-resolution.py` with pycryptodome and my own parameter splitter. My `per_carrier_rows` and `distinct_selectors` blocks equal the committed `corpus/evidence/round-25/a3/c2/analyze/tally.json` field for field, and my `wrong_names` list (29 entries) is item-identical. Noble cross-check: 344/344 candidate texts and 69/69 ABI signatures agree with pycryptodome; 0 disagreements.

## What the Keccak check can and cannot do here

Observation: 0 Keccak mismatches does not mean 0 wrong names. 224 candidate instances (63 distinct texts) are genuine 4-byte Keccak collisions: the signature differs from the carrier's ABI signature while hashing to the same selector. `approve(address,uint256)` (`095ea7b3`) is also `YmCvE(address[4],bytes[3])` and `__$$$$___$$_$_$$__$_$_$$__$$$$(address,uint256)`; `fee_quote(uint256)` (`6e8efde2`) is also `hasStreamed(address)`. The openchain `filtered=true` junk entries in the saved responses are real preimage collisions, not malformed text, so the Keccak check alone can never remove them. This supports the C2 entry's statement that "the Keccak check alone never removes a wrong name here": the parameter-list and `filtered=false` checks do all the separating work.

Observation: REA's `inferred_arguments` disagrees with the ABI parameter list on 12 of 69 rows, always inferring `uint256` where the ABI says `address` (`approve`, `transfer`, `transferFrom`, `balanceOf`, `allowance`, `mint`, `is_steward`, `set_steward`, `note(bytes32,uint256)`, `is_owner`, `balances`, `balance_of`). The lane's rule comparisons use REA's list, so on those rows the parameter check can reject the true name. REA-side inference quality, not a Keccak finding.

## Limits

Six lane-compiled carriers, 43 distinct selectors (37 with candidates), one saved snapshot (2026-10-22T08:28Z-08:30Z); nothing here measures deployed or obfuscated contracts. One 4byte page per selector and no non-empty openchain `event` map, so no candidate was reachable through an unread channel. The manifest sha256 of all 138 saved responses matches the six `db/manifest.json` files, and each response file name's selector equals the selector in its manifest URL, so "the queried selector" is the one the fetch asked for. Collision counting uses the carrier ABI as ground truth.

## Commands and evidence (all exit 0, UTC 2026-10-22)

1. `10:49:29Z` `bash <seat>/run_all.sh` (exit 0): `indep_keccak.py`, `node crosscheck_noble.js noble_input.json` (`records 344, noble_agrees 344, noble_disagrees 0`), `node crosscheck_noble.js noble_abi_input.json` (`records 69, noble_agrees 69, noble_disagrees 0`), `resolver_cmp.py`, `abi_truth_rules.py`, `summary_counts.py`, and the lane's `python3 -I -B tools/round-25/a2/resolve-selectors.py selftest` (`ok: true`, 9/9) — all exit 0.
2. `10:50:40Z` `.venv/bin/python reproduce_tally.py` (exit 0): `per_carrier_rows_identical: true`, `distinct_selectors_identical: true`, `wrong_names_identical: true` (`mine_count 29`, `lane_count 29`).
3. `10:49:29Z` `resolver_cmp.py` excerpt: `"resolver_keccak_vs_independent_over_candidates": {"compared": 344, "disagreements": 0, "examples": []}`; per carrier `"identical_selector_to_signature_map": true` for all six ABIs; `"sha256_mismatches": []` for all six manifests.
4. `10:58:01Z` full re-run of `run_all.sh` (exit 0, `run_all_final.log`) plus `reproduce_tally.py` (exit 0): byte-identical outputs, so every JSON artifact above is reproducible.

## Artifacts (seat dir, the L1 integrates)

Seat dir `/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2IndependentKeccak/`, file and sha256:

```
indep_keccak.py efe55542aaa44285337930b7f0d15afafa877a95042f4cdabe56142694baef8e
indep_keccak.json 5be0ff2588ac7453e04ca34137facabb39d96b8ee078bb71b9c8dc423b80c6d4
indep_keccak_candidates.json 2ac6e8ccc59762bfc03bfa9fa37fff844fef2c08545a9cead038566bdf7f6743
crosscheck_noble.js 9ba9e74d7b9e0d29334ad02b70bf66980ba5ac9e336ac156fa3d859cc870aef7
noble_input.json 044902df31f36bb6b25b900a96bb617f4ec7943e4b4f22a2c02bb6acb9de4f2b
noble_abi_input.json 9360a3586544aa9ffc900fbd484a99837e3a8dfada38c708a9f2b99facda6ebc
resolver_cmp.py 6e428f6b86c5f367edc9e96e88d13212b36a65ed33e2cd7b3a3ca4a3239653b8
resolver_cmp.json 1fc4b872a4da9227929477dbfb3c2a944dcc9f7a4b6fa4472ab96b452ff82fd1
abi_truth_rules.py 5716b80d970f58a026af48c400f82ac8d7e253c63d62262ac7be64d4dbb15e89
abi_truth_rules.json 68ff993a43a0b73b47bd14e03fa9a18fc59da32dc24fd2809a32ff944693e224
reproduce_tally.py 6594ce84cf9e5df432b992e92ae81ef5595cf876277e03c9edf9d58c41a8be4e
tally_reproduction.json dc5908fda18b0a4b4e7e83c3a742cc8fe9a4e5a748b4534bfe623e94e02c9c17
summary_counts.py 113af4ae47ae570413bfb838802dffcee68f52837cfd43fa6fdfe41ba6d8d34d
summary_counts.json 92ad9ffe3a00b8f9fe70d732525507da117d56da89eef98fa40e729af721fc52
keccak_truncation.py 8ed2d9520fb3e7beb643e59d5aa2247fbb96f5e2ed4fa2a98b2dbaa34ce98f30
run_all.sh fe482e937fd293f35d4ef488ebf1790b06fdfe548808614955083b78068208d6
run_all.log 7ff862e425e052042dd0407fd21762241f33f7ffb98d4f3dff40cdf12f9a53c6
run_all_final.log 7108a40aa4fe537ec1a763b95b2b36da75ab43ee0585b137ddfd6c4478b8e842
```

Tooling installed this seat: pycryptodome 4.1.0 (PyPI, `uv pip install` into a scratch venv) and @noble/hashes 2.4.0 (npm registry, `npm install --prefix` into the seat dir), both for an independent Keccak-256 and a cross-validation. No system package changed; no host service restarted; no pacman transaction.

Report: .ufo/waves/round-25/a3/w1/C2IndependentKeccak.md
