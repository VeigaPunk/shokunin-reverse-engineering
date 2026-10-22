# Round 29 W1 — fresh carrier rebuild and screen

## Result

- **[OBSERVATION] Byte identity:** rebuilt carrier outputs match the pinned `HEAD` byte-for-byte: 49/49 generated output files compared, with no differing paths. The carrier files covered are `carriers.tsv`, 16 Solidity sources, and 32 runtime/ABI files.
- **[OBSERVATION] Screen:** the requested hex screen passed 16/16 (`carriers=16 fail=0`, exit 0). Every runtime file was also non-empty and had no `__$` sequence (16/16, exit 0).
- **[OBSERVATION] Verdict — “hex-screened 16/16”: HOLDS.**
- **[INFERENCE]** This demonstrates repeatability with the pinned source and `solcjs 0.8.37+commit.f401782d.Emscripten.clang` on this host; it does not establish cross-version or cross-platform reproducibility.
- **[OBSERVATION] Blockers:** none.

## Retained evidence

All times are UTC on 2026-10-22.

1. **[OBSERVATION] Pinned clone revision**
   - Command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD` (cwd: scratch clone).
   - Output: `18be864a528873b2b70d8c94e31f880290249e90`
   - Exit: 0. Time: `2026-10-22T20:23:18Z`.

2. **[OBSERVATION] Rebuild** (after changing only the clone's `LANE` constant to the clone path)
   - Command: `python3 -I -B tools/round-29/make-carriers.py` (cwd: scratch clone).
   - Exact output: `carriers=16 compiler=0.8.37+commit.f401782d.Emscripten.clang`
   - Exit: 0. Time: `2026-10-22T20:21:30Z`.

3. **[OBSERVATION] Clone status and requested diff stat**
   - Commands: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git status --porcelain` and `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git diff --stat` (cwd: scratch clone).
   - Exact output:
     ```text
      M tools/round-29/make-carriers.py
     tools/round-29/make-carriers.py | 2 +-
     1 file changed, 1 insertion(+), 1 deletion(-)
     ```
   - Both exits: 0. Time: `2026-10-22T20:22:07Z`. The only clone change is the required local `LANE` adjustment.

4. **[OBSERVATION] Tracked carrier diff**
   - Command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git diff --exit-code -- corpus/evidence/round-29/c1` (cwd: scratch clone).
   - Exact output: empty.
   - Exit: 0. Time: `2026-10-22T20:22:35Z`.

5. **[OBSERVATION] Byte-for-byte comparison against committed blobs**
   - Command: `python3 -I -B /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRebuildCarriers/check-carrier-bytes.py /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRebuildCarriers/clone`.
   - Exact output:
     ```text
     carrier_files=49 differing=0
     manifest=/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRebuildCarriers/carrier-sha256.txt
     exit=0
     ```
   - Exit: 0. Time: `2026-10-22T20:22:41Z`. The checker compared each listed worktree file's bytes with `git show HEAD:<path>`; per-file SHA-256 values are retained below.

6. **[OBSERVATION] Hex screen**
   - Command: `python3 -I -B tools/round-28/hex-screen.py --root /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRebuildCarriers/clone corpus/evidence/round-29/c1/carriers.tsv` (cwd: scratch clone).
   - Exact output: `carriers=16 fail=0` then `exit=0`.
   - Exit: 0. Time: `2026-10-22T20:22:07Z`.

7. **[OBSERVATION] Runtime file non-empty / placeholder screen**
   - Command: `python3 -I -B /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRebuildCarriers/check-runtime-files.py /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRebuildCarriers/clone`.
   - Output contained one row per carrier, each with `nonempty=1 placeholder=0`; exact summary: `runtime_files=16 fail=0`, then `exit=0`.
   - Exit: 0. Time: `2026-10-22T20:22:07Z`.

## Scratch artifacts and hashes

The following are SHA-256 of the retained scripts and comparison inventory. The inventory records SHA-256 and `identical=1` for each of the 49 rebuilt output files.

```text
155ca3f3188c6adf1bdb0b6020bb8140fac5173fbcff684c92adbd6d1feeea29  /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRebuildCarriers/check-runtime-files.py
9ec751f553901005398ed97d3751809df39f2fa900a0f9247f85cbf366c70435  /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRebuildCarriers/check-carrier-bytes.py
8054cc638e92e38fb5044a9dbde7fe723b05b64a79d451bc015a1160dff56ff7  /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRebuildCarriers/carrier-sha256.txt
 a200d75b5e7d04699734a9841b2e0b4796288586b03c7676f0121d5d97524388  /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRebuildCarriers/clone/tools/round-29/make-carriers.py
```

Per-file SHA-256 inventory (each `identical=1` against pinned `HEAD`):

```text
94438ede707d98987af7d8a869aa5fdb5ac18872fb9cf57fe621e9593bdc6e9c  corpus/evidence/round-29/c1/carriers.tsv
 d57aeacb2bb53fe15a48177fc0b89e7f7412446497398f6b145ef06b6b5346d4  corpus/evidence/round-29/c1/src/AccessOwnable.sol
 a0b64109b41851d3fe388004b9555580f9ad473144c154330562b364c9c039bb  corpus/evidence/round-29/c1/src/ChainlinkAggregator.sol
 ed3b3e453b1ddd3469a74559d5778ba401d64c47e876dee467fcad04383f3084  corpus/evidence/round-29/c1/src/EnsRegistry.sol
 6c2a1cb1e014e8b538fb8451271ef5eef92386fc49f3481d3c2e1714659e0bc2  corpus/evidence/round-29/c1/src/Erc1155.sol
 e0fe3a356f5d862003f32a61703b7b822dc382294aaf1ae102c296ce6b2a8c6c  corpus/evidence/round-29/c1/src/Erc20Permit.sol
 9a36a645838b060e31d76fe5fc993851bdb14f49b04a2035ac043b0db0c6a002  corpus/evidence/round-29/c1/src/Erc4626.sol
 098c1c43c7169dae7ca8da665b3dc912ba0dc069f96d1ef3999a4a4de178f7cd  corpus/evidence/round-29/c1/src/Erc721Full.sol
 503aa845338d4da2cc5521027da77ef37869cf9f100a9c076269422cf336826a  corpus/evidence/round-29/c1/src/GovernorBravo.sol
 cb7704e2a6bda2de79dfb1af2051ddcfb52f28f43c4e69e51d89e11f1c4c5f08  corpus/evidence/round-29/c1/src/Multicall3Getters.sol
 229850d9d4204be2207fd8ad21309fe65bc01003882bc65232ac98e9348d5d13  corpus/evidence/round-29/c1/src/NftDropAdmin.sol
 fff2cdf63f55fdd0603a6a59993cf19b0a61795d758a46c17033bb7325edf0bd  corpus/evidence/round-29/c1/src/SafeOwners.sol
 5a4f36b600a8239a96b8ac1d227b9de32c8ab9d2a2f87bedc747d1badf8f6469  corpus/evidence/round-29/c1/src/Timelock.sol
 7187b86ec9fdc06978b85b04f8a80030efb22d66f68c1586c426c366632e4765  corpus/evidence/round-29/c1/src/UniV2Factory.sol
 6074d4368b4dcef3d3b40be4d4d5a81208da31ef40e2dbcc5018c5ef14f67352  corpus/evidence/round-29/c1/src/UniV2Pair.sol
 880bdf995f3aeb262ff33eed54270b4fbe0667e09b10819a50a552db3991822b  corpus/evidence/round-29/c1/src/UniV2Router.sol
 2d23ffce03fa9123143da042624fa7edd834b2ea44846d97e4445616144dd551  corpus/evidence/round-29/c1/src/Weth9.sol
 5b3f3f769e43534e9ea7eec797a4c2f53a14d63d0ae55a7ec315b05d9227e66f  corpus/evidence/round-29/c1/compiled/Erc20Permit.runtime.hex
 dd9d607eac9ae180e3238d80675f58d862385d9a8514c4de602801c7892cac25  corpus/evidence/round-29/c1/compiled/Erc20Permit.abi.json
 d7bff45d0a7c68a3bd7a25a567bc8a5d226d2cb86aa0307f0a5aa29d21b1c7ab  corpus/evidence/round-29/c1/compiled/Erc721Full.runtime.hex
 bfc69e3e074310f430a12c22c850cf49234c1bb0d569307cbd62d6c7dbef8ec7  corpus/evidence/round-29/c1/compiled/Erc721Full.abi.json
 3acfbfda8cdf62c6c6c1cdd2109f89f5294054eb0b039aed6cce1ee9abc4df57  corpus/evidence/round-29/c1/compiled/Erc1155.runtime.hex
 16bee02f4e36dd275d46fb2daed58051eb4eec5c4893d53f7628569e70bfc140  corpus/evidence/round-29/c1/compiled/Erc1155.abi.json
 5a37c73afd3a075dba69d53b548283efacdb78b08672a44d9a940be310a6cca0  corpus/evidence/round-29/c1/compiled/Erc4626.runtime.hex
 0260e4e9cb7d872f87d0ede56fd492ac04f8793720aa1f80e67ad18a17d9f085  corpus/evidence/round-29/c1/compiled/Erc4626.abi.json
 ba576c922bf72db3c1ab3cd6d6ee6af6e18196874c974514bfb16e3f59bafca0  corpus/evidence/round-29/c1/compiled/AccessOwnable.runtime.hex
 e91b945ea6e0cda4250741a4e88ee80473d35eb045649cb6a26710af15d499a8  corpus/evidence/round-29/c1/compiled/AccessOwnable.abi.json
 9b16dfa64c6e0579203b569169ee73b5dea8f554b92677bdf21aea6f2ef218db  corpus/evidence/round-29/c1/compiled/UniV2Pair.runtime.hex
 c672c746e25fd0efbd595e663b5670e60257fc0cd4a6be1841fe1183875ccba4  corpus/evidence/round-29/c1/compiled/UniV2Pair.abi.json
 7e7f03b83f619aaa65954149b96c30d63a7a5a0c4589cf817d3aef1e961b7a9f  corpus/evidence/round-29/c1/compiled/UniV2Router.runtime.hex
 bda1d23c632e4984c68efc3706b801dbda8fa397acf499d06e5208527b4bcc66  corpus/evidence/round-29/c1/compiled/UniV2Router.abi.json
 f718813e15032e8a1d04a2a0bd1483003e279318ab9301a268e629c63bc0d91f  corpus/evidence/round-29/c1/compiled/UniV2Factory.runtime.hex
 792a8254426a743d696b95110e8781335031c9c990748e33dbaa172b027da84f  corpus/evidence/round-29/c1/compiled/UniV2Factory.abi.json
 a2dbecf0d45ee1d7b0be2d7966266ac73dfbbbcf6b2abbd3b82036ac907f6071  corpus/evidence/round-29/c1/compiled/Weth9.runtime.hex
 faf6dab28745c571053573cbebcfdbceb37a66325d8777b1ff4fc8d9fa2577e0  corpus/evidence/round-29/c1/compiled/Weth9.abi.json
 9deaf740120a8ab3adbb03229639b85e690dd2d40ef89d5f3bd429786637d39b  corpus/evidence/round-29/c1/compiled/Multicall3Getters.runtime.hex
 eef2dd5a0146126dd5d3333b1cb6404ccc21f764b2a7901d5587c503b603239f  corpus/evidence/round-29/c1/compiled/Multicall3Getters.abi.json
 5c7fe0b05916971b7784c5631e10b720e543215eb259b52d37e64ab2676e0dc9  corpus/evidence/round-29/c1/compiled/ChainlinkAggregator.runtime.hex
 ae7bcfa2d0de104b6d6bfef9321fe07834c10e4e667618425d346fa68aba266e  corpus/evidence/round-29/c1/compiled/ChainlinkAggregator.abi.json
 be2d3f24434c230f90044bef55a8ec09c08b9cf2bd6b1b7dc6a964e7005ac69b  corpus/evidence/round-29/c1/compiled/Timelock.runtime.hex
 d0d259dda645654e4751aa963fb6c42cebd97b89dbda5012705ae7e71a50d457  corpus/evidence/round-29/c1/compiled/Timelock.abi.json
 2f67e4c52dc188b58659888a958f2bb8e8a426966a47f6916ff9dead009cf8b5  corpus/evidence/round-29/c1/compiled/GovernorBravo.runtime.hex
 c0c60be13c6faf44ddbcd02ee74f6bec337f39209f3eab7afde3fe021c1718e8  corpus/evidence/round-29/c1/compiled/GovernorBravo.abi.json
 bb75506440b11908fc051c80f04db4513178fde401bb90f9daf9717ca82c29d0  corpus/evidence/round-29/c1/compiled/SafeOwners.runtime.hex
 ca2298db0884f702b973e452adb0d152a779da2b52ae59877419eb0e6fdcdffc  corpus/evidence/round-29/c1/compiled/SafeOwners.abi.json
 7652be8f1f19eabdb53027fc14688e62800dd1e3dfe9290bcd447da1b2d632e6  corpus/evidence/round-29/c1/compiled/EnsRegistry.runtime.hex
 553894477a1ed8032716b8b86b3eea1043561594ce6316aaa755e048661da869  corpus/evidence/round-29/c1/compiled/EnsRegistry.abi.json
 24cc490f6820e25ca963dabc899ac6f80d7c44f7584e5f7ace151f2c9ed4a8ef  corpus/evidence/round-29/c1/compiled/NftDropAdmin.runtime.hex
 132222c3b65e316a9f357617b0350078c86aa05fec14c842b424373a88e4566a  corpus/evidence/round-29/c1/compiled/NftDropAdmin.abi.json
```
