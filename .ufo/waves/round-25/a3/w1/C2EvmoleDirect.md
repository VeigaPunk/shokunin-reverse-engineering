# C2 direct EVMole run — REA 6.5.0 bundle vs current release (KaidokuR25a3.C2EvmoleDirect, round 25 attempt 3, wave 1)

Target: which EVMole REA 6.5.0 bundles, what the current EVMole release says about the same
six lane carriers, and whether the Vyper address-argument miss persists. Lane access was
read-only; the only lane file written is this report. Verified 2026-10-22, 10:42:55Z–10:46:22Z.

## Verdict

- REA 6.5.0 bundles **EVMole 0.9.3** (four independent confirmations below).
- Current EVMole release is **0.9.4** (`npm view evmole version`, exit 0, 10:42:55Z), published 2026-10-13.
- **The Vyper address-argument miss does not persist in EVMole 0.9.4**: all 11 address-typed rows on the two Vyper carriers are recovered as `address`, match the compiler ABI, and get the correct state mutability. It **does** persist in every published REA release, because 6.3.0 / 6.4.0 / 6.5.0 / 6.7.0 all pin `evmole@0.9.3` exactly.
- One argument miss persists in 0.9.4 and is not Vyper-specific: `3efdef66` `note(bytes32,uint256)` on carrierb is read as `uint256,uint256` by both versions.

## Which EVMole REA 6.5.0 bundles (observation)

- `corpus/evidence/round-25/a2/c2/rv2token/envelope.json` → `"provider":{"id":"evmole-interface",…,"version":"evmole@0.9.3"}` (read 10:42Z).
- `rea/node_modules/evmole/package.json` from `npm install rea-agents@6.5.0` → `evmole 0.9.3 dist/evmole_node.cjs` (install exit 0, 10:42:5xZ).
- `rea/node_modules/rea-agents/dist/evm/EvmoleRelease.js:5` → `version: "evmole@0.9.3",` (hardcoded provider identity; grep 10:43Z); `licenses/npm-dependencies.txt:2048` → `evmole@0.9.3 | runtime | MIT`.
- `npm view rea-agents@6.3.0|6.4.0|6.5.0|6.7.0 dependencies.evmole` → `0.9.3` for all four (exit 0, 10:45Z). No published REA release carries 0.9.4.

## Current release (observation)

`https://registry.npmjs.org/evmole` (plain HTTP fetch, exit 0, 10:44:08Z): `"0.9.3" time 2026-07-31T06:13:02.262Z`, `"0.9.4" time 2026-10-13T10:36:49.898Z`, `dist-tags {"latest":"0.9.4"}`, repo `github.com/cdump/evmole`. Upstream `https://github.com/cdump/evmole/releases` (API, HTTP 200, 10:44:15Z), release 0.9.4, section "Changes since previous release": "arguments: improve vyper quality" (commit `7b5e0ae`, 2026-08-02, `src/arguments/mod.rs`, +159/−1) and "state_mutability: improve quality on modern vyper contracts" (`1bf0365`, 2026-07-31, `src/state_mutability/mod.rs`, +14/−0). That patch adds calldata-length decoding (`direct_min_calldata_words`, `dense_min_calldata_words`), consistent with Vyper dispatchers that gate on `calldatasize`.

## Method

- 0.9.3 arm: the copy bundled in REA 6.5.0 (`rea/node_modules/.bin/evmole analyze --file <hex> --pretty`). 0.9.4 arm: `npx -y evmole@0.9.4 analyze --file <hex> --pretty`, the `--bytecode 0x…` form, and the JS API (`contractInfo`, scratch npm prefix `js/`); all three agree on selectors, arguments, mutability and bytecode offsets.
- `run.sh` exit 0; `out/run.log`: 12 runs all `exit=0`, utc 10:43:40Z–10:43:42Z; `--bytecode` rerun 6 runs all `exit=0`, utc 10:45:15Z–10:45:16Z; JS API 6 runs, function counts 5/6/13/8/22/15.
- Selector sets are identical for 0.9.3, 0.9.4 and the committed REA envelopes (69 rows).

## Selector sets and changed-row count

| carrier | language | 0.9.3 fns | 0.9.4 fns | REA env fns | ABI fns | 0.9.3=0.9.4=env selectors | rows changed |
|---|---|---|---|---|---|---|---|
| rv2token | solc | 5 | 5 | 5 | 5 | yes | 0 |
| kdxtoken | solc | 6 | 6 | 6 | 6 | yes | 0 |
| vaultb-opt200 | solc opt200 | 13 | 13 | 13 | 13 | yes | 0 |
| carrierb | solc | 8 | 8 | 8 | 8 | yes | 0 |
| stewardtoken | Vyper `EX-03/token.vy` | 22 | 22 | 22 | 22 | yes | 12 |
| carrierv | Vyper `EX-04/src/CarrierV.vy` | 15 | 15 | 15 | 15 | yes | 8 |

## Diff table — changed rows 0.9.3 → 0.9.4, with compiler-ABI truth

| carrier | selector | 0.9.3 args / mut | 0.9.4 args / mut | ABI args (signature) |
|---|---|---|---|---|
| stewardtoken | 095ea7b3 | uint256,uint256 / payable | address,uint256 / nonpayable | address,uint256 (approve) |
| stewardtoken | 23b872dd | uint256,uint256,uint256 / payable | address,address,uint256 / nonpayable | address,address,uint256 (transferFrom) |
| stewardtoken | 40c10f19 | uint256,uint256 / payable | address,uint256 / nonpayable | address,uint256 (mint) |
| stewardtoken | 70a08231 | uint256 / payable | address / view | address (balanceOf) |
| stewardtoken | 875194ac | uint256 / payable | address / view | address (is_steward) |
| stewardtoken | a9059cbb | uint256,uint256 / payable | address,uint256 / nonpayable | address,uint256 (transfer) |
| stewardtoken | cee38a15 | uint256 / payable | address / nonpayable | address (set_steward) |
| stewardtoken | dd62ed3e | uint256,uint256 / payable | address,address / view | address,address (allowance) |
| stewardtoken | 0c751377 | uint256,uint256 / payable | uint256,uint256 / view | uint256,uint256 (fee_of) |
| stewardtoken | 1aa02d59 | uint256 / payable | uint256 / nonpayable | uint256 (set_fee) |
| stewardtoken | d869f754 | uint256 / payable | uint256 / view | uint256 (preview_fee) |
| stewardtoken | db006a75 | uint256 / payable | uint256 / nonpayable | uint256 (redeem) |
| carrierv | 0776076f | uint256 / payable | address / view | address (is_owner) |
| carrierv | 27e235e3 | uint256 / payable | address / view | address (balances) |
| carrierv | b144adfb | uint256 / payable | address / view | address (balance_of) |
| carrierv | 0c751377 | uint256,uint256 / payable | uint256,uint256 / view | uint256,uint256 (fee_of) |
| carrierv | 1aa02d59 | uint256 / payable | uint256 / nonpayable | uint256 (set_fee) |
| carrierv | 2e1a7d4d | uint256 / payable | uint256 / nonpayable | uint256 (withdraw) |
| carrierv | 6e8efde2 | uint256 / payable | uint256 / view | uint256 (fee_quote) |
| carrierv | e0749a6a | uint256 / payable | uint256 / view | uint256 (fee_on) |

Every 0.9.4 value equals the compiler ABI; every 0.9.3 `address` was `uint256`. Argument
rows matching the ABI (0.9.3 → 0.9.4): rv2token 5/5 → 5/5, kdxtoken 6/6 → 6/6,
vaultb-opt200 13/13 → 13/13, carrierb 7/8 → 7/8 (unchanged miss `3efdef66`),
stewardtoken 14/22 → **22/22**, carrierv 12/15 → **15/15**.

## Does the Vyper address-argument miss persist?

- **EVMole 0.9.4: no.** All 11 address-typed rows on the two Vyper carriers are `address` and match the ABI; mutability also becomes correct (0.9.3 said `payable` on every Vyper row, 0.9.4 says view/nonpayable).
- **REA: yes.** The pin is `evmole@0.9.3`, so the committed envelopes are exactly 0.9.3 output and cannot change without a different tool or a REA release that bumps the pin.
- So the C2 entry's error pattern ("Wrong REA arguments pick the wrong name … REA inferred `uint256,uint256` for `0xa9059cbb`") is a property of the REA 6.5.0 pin, not of EVMole today; it is version-bound and should be labelled as such.

## Downstream effect on the C2 naming rules (offline over the saved lookups)

Recomputed with the lane's own resolver (`tools/round-25/a2/resolve-selectors.py analyze`, read-only, over the committed saved lookups and compiler ABIs), once with the committed envelopes (0.9.3) and once with scratch envelopes carrying 0.9.4 arguments/mutability. The 0.9.3 arm reproduces the committed `corpus/evidence/round-25/a3/c2/analyze/tally.json` exactly (69 rows; 59/33/26/10, 48/47/1/21, 62/61/1/7, 55/54/1/14, 49/49/0/20), so the harness is validated against the published numbers.

| naming rule | 0.9.3 named/right/wrong/no-name | 0.9.4 named/right/wrong/no-name |
|---|---|---|
| first 4byte.directory result | 59/33/26/10 | 59/33/26/10 |
| only 4byte candidate matching REA args | 48/47/1/21 | **54/54/0/15** |
| first openchain result (filter=false) | 62/61/1/7 | 62/61/1/7 |
| only openchain candidate with filtered=false | 55/54/1/14 | 55/54/1/14 |
| only filtered=false openchain candidate matching REA args | 49/49/0/20 | **57/57/0/12** |

Eight rows change output, all on the two Vyper carriers, all from "no name" (or the wrong `workMyDirefulOwner(uint256,uint256)`) to the correct ABI name: `095ea7b3`, `23b872dd`, `70a08231`, `a9059cbb`, `dd62ed3e` (stewardtoken) and `0776076f`, `27e235e3`, `b144adfb` (carrierv). Remaining wrong names are database-side and version-independent: the 4byte.directory junk first-results and the `6e8efde2` collision (`hasStreamed(address)` vs the ABI `fee_quote(uint256)`).

## Risks, gaps, could-not-evaluate

- The 0.9.4 arm is a direct EVMole run, not a REA run: the R25-C2 claim's own envelopes stay 0.9.3 output, and no REA release exercises 0.9.4.
- Only the six lane carriers were measured (69 rows, 43 distinct selectors); no accuracy claim is made for deployed or obfuscated contracts.
- `3efdef66 note(bytes32,uint256)` is still `uint256,uint256` under 0.9.4; that row is solc, not Vyper, and I did not investigate the upstream cause.
- The upstream release text was read from the GitHub API JSON, not a rendered page; I read the file list and the first patch hunk of `src/arguments/mod.rs`, not the full diff.
- Two of the six carriers are Vyper (`EX-03/token.vy`, `EX-04/src/CarrierV.vy`); the C2 entry's "one Vyper token" understates this — Vyper exposure is 37 of the 69 rows.
- Scratch envelopes (`out/env094/*.json`) are copies of lane envelopes with inferred arguments substituted; they are not lane evidence and carry no evidence id.

## Tools and seat artifacts

No system package was installed or upgraded (pacman untouched). npm installs were confined to scratch prefixes: `rea-agents@6.5.0` (bundled EVMole 0.9.3 + REA provider identity) and `evmole@0.9.4` (JS API arm); `npx -y evmole@0.9.4` for the CLI arm. Node v24.21.0. Root: `/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2EvmoleDirect/`.

- `run.sh` 357640d1ff312f26417814ca1964d511d18b8cce7908ffd9c30376238b8f27ec; `compare.py` 7487826d1c961216264cce5948bfdaae930219df1dd35ae1b2fa64d319401925; `compare_js_cli.py` c023b13b2326f40f7dcf8f9b85b1c76e4526f4baeb60c902ebda515f18f8424c; `tally094.py` 3c78c06b77b7b33ad2caf32749efbcf4b135b6ee04ad74ae53b6f3f26ed9c739; `js/check.mjs` 6ad7e939398b0ea2293923975c1783bab1096291a18a539edb0ab55515ebfe0e.
- `out/run.log` 590d2252a2fddaabe0551b60e5eefcc17635d00ebf04eb066772a9e0b34b018d; `out/compare.txt` 994ae3e13a320e093bcbcbf87ef5b836837258d04085ad52a60ac4973a8f41ad; `out/tally-compare.txt` bada6253dd04ccda21f0a6c8eb7dcce7f089359d2efa1dfa691ccbf6fbb0178d; `out/tally-compare.json` ffd1105c95cd921bd1bce7fde24267e6ac04c127e7134c209c0aa41b6585d61c.
- `out/npm-evmole.json` 2f42c1cbff9800aaeaad270551ea10cca24f89f838c36bcc0a700b6a0997d384; `out/gh-releases.json` 7e45a34e2bb0e96d90bb68812261c8fb9ebd187f6aa6cb1be622cfc14917907f; `out/gh-release-0.9.4.md` 430ce9328945a606db51640f24b29db41e3004b3e239cfa6a94f327559415218; `out/commit-7b5e0ae….json` 1a4d0c9365d6c8eb4f3fd98199eb754f4841034954fb104ef05f73314f794567; `out/commit-1bf0365….json` e30a434ccabe508e13b22455f0e5fb1452ef503762426256a49613e177d9c74e.
- Per-carrier raw outputs `out/<carrier>.v093.json`, `out/<carrier>.v094.json`, `out/<carrier>.v094.bytecode.json`, `out/<carrier>.js094.json` and scratch envelopes `out/env094/<carrier>.json`: per-file sha256 in `out/artifact-sha256.txt`.
- `pkg/evmole-0.9.3.tgz` 58373518479be41098e70ccc87f713cc13a3560e0ab56f49c1d9a79e58b3352c, `pkg/evmole-0.9.4.tgz` ee147e32a1c5b9135ffe037eade03869aa8925cf5b959c134a38f988e1f52711 (`dist/evmole_bg.wasm` sha256 542b24e2… for 0.9.3 vs a868af01… for 0.9.4).
