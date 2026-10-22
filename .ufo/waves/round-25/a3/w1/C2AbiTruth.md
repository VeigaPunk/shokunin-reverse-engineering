# R25 a3 wave 1 — C2AbiTruth (KaidokuR25a3.C2AbiTruth)

Seat `/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2AbiTruth/`. Target: the provenance of the ground truth the C2 claim rests on — the six carriers' compiler ABI files in `corpus/evidence/round-25/a2/c2/carriers.tsv`. Method: recompile each pinned source with the recorded compiler (solc 0.8.37 from the lane's own prefix; Vyper 0.4.3), recompute every selector from the source-level signatures with an independent Keccak-256, and compare against the carrier ABI, the in-tree compiler output and the REA envelopes. Read-only on the lane: no lane file edited, no Git index or jj state touched. Times UTC 2026-10-22.

## 1. Per-carrier verdict on the ground truth's provenance

| carrier | ABI file (lane-relative) | ABI sha256 | verdict |
|---|---|---|---|
| rv2token | `.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.abi.json` | `e9a58020…c6a9d` | **compiler output** |
| kdxtoken | `.ufo/waves/arc3-loop1-round1/claims/c1/EX-05/kdx-abi.json` | `40ad881e…0c2019` | **compiler output** |
| vaultb-opt200 | `.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/out/VaultB.opt200.abi.json` | `6dae6710…88cf3f` | **compiler output** |
| carrierb | `.ufo/waves/arc3-loop1-round3/claims/c1/EX-05/out/CarrierB.abi.json` | `8a11dd93…18a8f63` | **compiler output** |
| stewardtoken | `.ufo/waves/arc3-loop1-round4/claims/c1/EX-03/abi.json` | `a935feb1…7948591` | **compiler output** |
| carrierv | `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/abi.json` | `c7902147…c17550b` | **compiler output** |

"Compiler output" rests on four independent legs per carrier. (a) **Fresh compile**: the pinned source recompiled with the recorded compiler reproduces the ABI (JSON-equal all six; byte-equal kdxtoken, vaultb-opt200, stewardtoken, carrierv). (b) **In-tree compiler output** carries the same ABI — `RV-2/solc-out.json`; `EX-04/solc-out.cleaned.json`; `EX-10/out/VaultB.nopt.abi.json`; `EX-05/out/CarrierB.metadata.json` `output.abi`. (c) **Source coupling**: mutating the source changes the ABI, so the file is not a free-floating hand-written list. (d) The carrier file is a *deterministic re-serialization of the compiler output* (§3), so its byte shape is accounted for without hand-authoring.

## 2. Runtime hex sha256 vs each envelope's subject digest — holds, 6 of 6

Command `final.sh` §A (exit 0, 2026-10-22T11:13:14Z). Each envelope's `subject.digest.sha256` equals the sha256 of the carrier runtime hex **file bytes** exactly:

```
rv2token      d7f73058e2d9fb2563bf96b2f26902f233530de027a7943185e15bfdc4e1048f  match=True
kdxtoken      69a15782678dccdd4d43b2f0af566c2f030fe9dee4de4ef8365bc4b6d1b29ad6  match=True
vaultb-opt200 9a1fbfaba9e3a89c1ce8bc12291c305500beef48a73ee270e6116cd5febb1d88  match=True
carrierb      247e09f3650aab9010b72b21c68af874b08dbc8d16bab54032d0c4a0017149cd  match=True
stewardtoken  cf13c82fb5b0bc73c7c27f1b2217997edda028c6f13b5ee577b9de09ae10b1eb  match=True
carrierv      e0b1021c68f8de8c3f049f4242769548b6f8271a00986f2ab20f049f8748a192  match=True
```

The digest covers the hex-text file, not the decoded bytes; the decoded-byte digests (`c1081a56…` rv2token, `9c40940e…` kdxtoken, `b24a0115…` vaultb-opt200, `b9c70178…` carrierb, `1846469b…` stewardtoken, `57d6fd0a…` carrierv) each equal a fresh compile of the pinned source. File shape: `EX-03/runtime.hex` carries a `0x` prefix and trailing newline; kdxtoken and carrierb end with a newline; the rest are bare hex. The digest follows the file bytes, so prefixes do not break the match.

## 3. Byte-level provenance of each ABI file (no hand-writing)

- **rv2token** — byte-identical to `jq --indent 1 '.contracts["Rv2Token.sol"]["Rv2Token"].abi'` of the in-tree `RV-2/solc-out.json`, trailing newline stripped (`json.dumps(indent=1)` also matches). `RV-2/solc-out.raw` is the compiler stdout behind it (first line: `>>> Cannot retry compilation with SMT because there are no SMT solvers available.`). The byte form differs from solc's own dump; the content is equal.
- **kdxtoken** — byte-identical to a fresh solc 0.8.37 compile of `arc3-loop1-round1/claims/c1/EX-04/KdxToken.sol` (sha256 `c2980385…d3dccba`, pinned in `EX-04/compile-receipt.txt` §2); JSON-equal to `EX-04/solc-out.cleaned.json`.
- **vaultb-opt200** — byte-identical to a fresh solc 0.8.37 compile of `arc3-loop1-round3/claims/c1/EX-10/VaultB.sol` with `optimizer {enabled:true, runs:200}` (the settings in `EX-10/compile.js`); also byte-identical to the in-tree `EX-10/out/VaultB.nopt.abi.json` (the ABI is optimizer-invariant).
- **carrierb** — JSON-equal to the fresh compile and to `EX-05/out/CarrierB.metadata.json` `output.abi`; byte-identical to that compile's ABI plus one trailing newline, exactly what `EX-05/compile.js` writes (`JSON.stringify(c.abi, null, 2) + '\n'`).
- **stewardtoken** — byte-identical to `vyper -f abi EX-03/token.vy` (0.4.3+commit.bff19ea2); `method-identifiers.json` byte-identical to `vyper -f method_identifiers`.
- **carrierv** — byte-identical to `vyper -f abi EX-04/src/CarrierV.vy`; `method-identifiers.json` likewise; the ABI line in `EX-04/out/combined.txt` (`vyper -f bytecode,abi`) is JSON-equal to `out/abi.json`.

**Mutation test** (`mutation.js`, node + lane solc; Vyper copy): editing one signature in each source and recompiling yields a different ABI in every case — rv2token `balanceOf`→`balanceOfOf`; kdxtoken `mint` gains a parameter; vaultb-opt200 `feeOn` gains a parameter; carrierb `note` gains a parameter; stewardtoken `mint` gains a parameter; carrierv `fee_on` gains a parameter. A hand-written ABI not derived from the source would not track it.

## 4. Selectors recomputed from source-level signatures — 6 of 6 clean

`srcscan.py` parses each source for selector-bearing externals (explicit `function` / `@external def`, plus compiler-generated public getters for public state variables and public mappings), canonicalises the signature, Keccak-256s it and compares with the carrier ABI and with the runtime's PUSH4 dispatch constants (`srcscan.json`):

```
rv2token 5 / kdxtoken 6 / vaultb-opt200 13 / carrierb 8 / stewardtoken 22 / carrierv 15 sigs
for all six: src_sig_set==abi_sig_set=True  selector_sets_equal=True  src_selectors_in_runtime_push4=True
```

The ABI function set equals the source-level signature set exactly (nothing missing, nothing extra, either direction) and every one of the 43 distinct selectors appears as a PUSH4 constant in its runtime. The leftover PUSH4 constants are not function selectors: `vaultb-opt200` carries `4e487b71` (Panic), `30cd7471`/`1309a563`/`1dc930eb` (custom errors) and `3c3332b9` (a `PUSH4`+`SHL` data constant); `rv2token` carries `16ee4b79`. Keccak cross-check: the lane's `tools/round-25/a2/resolve-selectors.py` `selector_of` and pycryptodome agree on all 43 signatures (0 disagreements); that resolver's `selftest` passes 9/9 including the SHA3-256 negative control. The a2 saved lookups cover exactly each carrier's ABI selector set (`db_covers_abi_selectors=True`, zero extras), 138 responses = 2 per row × 69 rows, every `db/manifest.json` sha256 re-checked equal.

## 5. Scope caveat: kdxtoken's compile record is not in the carrier's own directory

Five carriers keep their compile record in or beside the carrier's directory: `RV-2/` (`Rv2Token.sol`, `solc-input.json`, `solc-out.json`, `sigs.txt`, `expected-selectors.txt`); `EX-10/` (`VaultB.sol`, `compile.js`, `manifest.sha256.txt`); `EX-05/` round 3 (`src/CarrierB.sol`, `compile.js`, `out/CarrierB.report.json`, `manifest.sha256.txt`); `EX-03/` (`token.vy`, `method-identifiers.json`, `compile-receipt.txt`, `MANIFEST.sha256`); `EX-04/` round 4 (`src/CarrierV.vy`, `out/method-identifiers.json`, `out/compile-receipt.txt`, `out/metadata.json`, `out/combined.txt`, `evidence/artifact-manifest.sha256`). For **kdxtoken** the carrier ABI lives in `EX-05/` (round 1), whose only compile script `compile-kdx.js` reads a `/dev/shm` path that no longer exists; the source pin, `solc-input.json`, `solc-out.cleaned.json` and `compile-receipt.txt` live in the **sibling** `EX-04/` directory (plus a byte-identical `KdxToken.sol` copy in `EX-06/evidence/`, same sha256 `c2980385…`). **Observation, not a defect**: the chain is intact (`EX-05/README.md` "Pre-landing reproduction"; `EX-04/compile-receipt.txt` §6 pins all four artifact hashes), but it crosses two seat directories of the same wave, so a reader looking only inside `EX-05/` will not find the source.

## 6. Two traps in the lane's own Vyper `method-identifiers.json` (not used by C2)

Vyper 0.4.3 prints selectors with leading zero nibbles stripped — `stewardtoken`: `approve(address,uint256)`→`0x95ea7b3` (true `0x095ea7b3`), `fee_of(uint256,uint256)`→`0xc751377` (true `0x0c751377`), `name()`→`0x6fdde03` (true `0x06fdde03`); `carrierv`: `fee_of`→`0xc751377`, `is_owner(address)`→`0x776076f` (true `0x0776076f`). Both files also carry a phantom `__default__()`→`0x89402a72`, a correct Keccak of that literal but occurring 0 times in either runtime. The C2 ground truth is the ABI file, not `method-identifiers.json`, so the claim is unaffected — but a recount seeded from `method-identifiers.json` misses those five selectors and gains one false positive per Vyper carrier. The lane already records both traps in `EX-03/compile-receipt.txt` §7.

## Result summary

| attack | verdict |
|---|---|
| carrier ABI file is hand-written rather than a compiler output | **holds** for all six (fresh compile, in-tree compiler output, source-coupling mutation, deterministic re-serialization) |
| carrier runtime hex sha256 vs each envelope's subject digest | **holds** — 6 of 6 equal |
| selectors recomputed from source-level signatures match the ABI and the runtime dispatch | **holds** — 6 of 6, 43 distinct selectors, 0 discrepancies |
| saved a2 lookups cover exactly the ABI selector set | **holds** — 138 responses, 0 extra, all manifest sha256 equal |
| compile record found in the carrier's own directory tree | **fails for kdxtoken only** — chain crosses into sibling `EX-04/`; intact but not local |

## Files changed

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-25/a3/w1/C2AbiTruth.md` (new). No lane corpus, tool, SCORECARD, SOURCES, Git index or jj state touched; nothing else written inside the lane.

## Artifacts (seat dir `/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2AbiTruth/`, full sha256)

- Scripts: `hashcheck.py` `28763c353399ebbfca06ae2c92686c1479f97593f1b537a2a9d5f4babd739d4c`, `selrecompute.py` `83519c788c95eb865d7d352656f43fc8e225cf06de3511ca84efbb9ef6964180`, `srcscan.py` `9d7e7d80a09e5cb275ecf52ef3007fae14ab6f9a8d273988c26943df0e483686`, `provenance.py` `5d7da54e958be6d5ef2da6e747c8edfbb5b3b5c8879020058e0d8287d282185c`, `metatrailer.py` `d4da7f277cc4fa03b96fdb28839e8d3aee88120e5c6be19e74cd742e5ac741c2`, `abi_vs_envelope.py` `3f48615a49a028b1244c419d907ba7bd782589bed7f650ac4a1663dad8d472ab`, `recompile.js` `fe6d521f0d1a220329a15dcc09edf35402f24f6c24240c49f330ef2f677d07db`, `mutation.js` `237f95fc6e42e09fc8447d8f464dc6e9efa32331aeb41800332dc3e244999413`, `final.sh` `154d40d8407a9013f15cb1975b6adf37f41758518d9dbfada03bf81a5c7569a7`.
- Results: `hashcheck.json` `4068daacb77abcd1f99dcc5643ae9eee3e9f63f175f154c0d11cb2dcfbc3d941`, `selectors.json` `6478bfce9051dbdde345943169eef3152bead8db92314680b00d56b91756f878`, `srcscan.json` `1ab7dd48faf32de0f424fbdbbdb6b78a840028f10e16eb9c78e525092a6febe1`, `provenance.json` `031a543a56440dfc3a4dd9318945280e6b465fc899e01ecd9f1fb616f88688c8`, `metatrailer.json` `3598934b274fc6ec711f16505d424c91f8726da553ff26fe834682a78285f2ef`, `final.out` `c060c018c3356a0deb88f86049fb87d3dd806ce98a6140c630218e535118dfd2`.
- Recompiled ABI: `recompiled/rv2token.abi.nonl.json` `4261652cd23e8b7cbd94ff996f5a19b82c72969208b2315f4f6516fa2199e957`, `recompiled/kdxtoken.abi.nonl.json` `40ad881eff2a8cbd267fba51a21c1057f82653f51e823698c84daa12e40c2019`, `recompiled/vaultb-opt200.abi.nonl.json` `6dae6710e6bfa77a99d87e27fe46a9912c97a6ad91d6c343c18e104ef688cf3f`, `recompiled/vaultb-nopt.abi.nonl.json` `6dae6710e6bfa77a99d87e27fe46a9912c97a6ad91d6c343c18e104ef688cf3f`, `recompiled/carrierb.abi.nonl.json` `cdc31cc16d01d51e61bebcbe46cd887838548c87e151ba56693ac8d76f15d0c9`, `vyper/stewardtoken.abi.json` `a935feb15bed491268e30a9a206b6c511b82737c64325a50bfb774f637948591`, `vyper/carrierv.abi.json` `c7902147808d31861bb8cf82837554c4700e675f85ef3b6010d82639cc17550b`.
- Recompiled runtime: `recompiled/rv2token.runtime.hex` `8495d7db40940573eae28439b794de3624d00887aa9acd67541b90d8124633d7`, `recompiled/kdxtoken.runtime.hex` `69a15782678dccdd4d43b2f0af566c2f030fe9dee4de4ef8365bc4b6d1b29ad6`, `recompiled/vaultb-opt200.runtime.hex` `ab6d09011f4065d1104d82e2029a7f9c58851625ba64399e7ecd8938049b4972`, `recompiled/vaultb-nopt.runtime.hex` `7817d9fc6004957cfec097cdf2e31bdb2dbb8d6f79f4ab48132c182632e938b7`, `recompiled/carrierb.runtime.hex` `247e09f3650aab9010b72b21c68af874b08dbc8d16bab54032d0c4a0017149cd`, `vyper/stewardtoken.runtime.hex` `cf13c82fb5b0bc73c7c27f1b2217997edda028c6f13b5ee577b9de09ae10b1eb`, `vyper/carrierv.runtime.hex` `1cb9eb945650eb8ae88a59fc09d5b3d34c37fbdb48dce586f645a08cb9fd72dd`; `vyper/stewardtoken.method-identifiers.json` `c6a5f987093858de03d9532fc65eb9f7ea0a1684825e0d334af9d2b4de0a6e11`, `vyper/carrierv.method-identifiers.json` `0d5cab2f3e3dde97f1d6f17ffd4a40dc2c9dbd5716cba98d7ca191632d52beb3`.
- Mutation outputs: `mutated/rv2token.mutated.abi.json` `c661689e72a588160bfeb22fd894928aba5ac2a2bac4d66b711a8a861f42080c`, `mutated/kdxtoken.mutated.abi.json` `e3ce4ad188afe3e2b54e7bb374d3886a0a23fff44f218bb418e875e7453be7df`, `mutated/vaultb-opt200.mutated.abi.json` `14058020d153762364236fce799189b55fd840b0b2753e47bd61327c64bbc3a8`, `mutated/carrierb.mutated.abi.json` `18de9d3d6c44c1778c47c1d1fc64b60133f283a1866253b947a11e016792f9f8`, `vmut/stewardtoken.mutated.abi.json` `9ac58666e79debb156520ff5bc784fe30cd867e6c2829a7bb40921054e6997d9`, `vmut/carrierv.mutated.abi.json` `70d1eb3cc3ffd583f9bb5f1004d6e5c398b51d79708e932d847732240eba2213`.
- Resolver replay: `an_rv2token.json` `76edb9ecbaacbc680d636afc7e5a2afb18717047595421863d7696bf736cc2b1`, `an_kdxtoken.json` `233f1260115766dde6818a88eb102a8e427badfc10c783b0079693d46aff2f8b`, `an_vaultb-opt200.json` `7be57d1a9c0985437ee1bfdc47d897de31598a4689c1984134904d7e569ad040`, `an_carrierb.json` `6b5b13288b232d5b4a564769785e4b90243e1611215e715865bb8fb317b059cc`, `an_stewardtoken.json` `8874ecbefe24b50368319e36ae96030c7e0a5b3dc6a89800e12966d24b202e63`, `an_carrierv.json` `bbcf5f83ed0773acef528e0c34b9cf20b9d1a46ca7c5681f9bd6395c0c9bb187` — all 69 rows' `abi_signature` values equal my independently recomputed source-level signatures, 0 mismatches.

## Tooling

`uv` 0.13.0 (pre-existing). Seat-local venv `.venv` via `uv venv`; `uv pip install pycryptodome` (4.1.0) then `uv pip install "vyper==0.4.3"`, which pulled vyper 0.4.3 and pinned `pycryptodome 3.24.1` (the vyper-compatible pin, matching the lane's own `arc3-loop1-round4/tools/vyper-venv`); that 4.1.0→3.24.1 change is inside the seat venv only, no system package touched. Compiler: the lane's own `arc3-loop1-round1/tools/solc-prefix/node_modules/solc` (0.8.37+commit.f401782d), read-only reuse; no solc installed by this seat; Vyper 0.4.3 from PyPI via `uv pip`. No pacman transaction (host-wide pacman paused), no MCP device, no REA invocation (envelopes read as files), no web request.

## Risks, limits, blockers

- The recompiles used each seat's recorded toolchain and settings. Where a receipt and a script disagreed — vaultb-opt200's `EX-05/recompiled/opt200/VaultB.report.json` names a *different* source (`arc3-loop1-round3/claims/c1/EX-04/carrierB.sol`, sha256 `14566042…`) — I followed the carrier's own directory (`EX-10/`). The `EX-05/recompiled/` copy is a different contract under the same output names; do not use it as the vaultb-opt200 ground truth.
- "Compiler output" is established by reproduction with the recorded compiler on this host and by content/byte equality with the lane's own compiler artifacts. It does not prove the source is the author's original intent; it proves ABI, runtime and source are mutually consistent.
- The Keccak used is pycryptodome 3.24.1; it agrees with the lane's pure-Python implementation on all 43 signatures, and both match the published selectors, so a keccak defect is excluded.
- No blockers.
