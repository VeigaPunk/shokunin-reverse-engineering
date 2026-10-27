# R43W2C2Pins — independent C2 anchor-digest audit

## Scope and revision

Evaluated committed C2 landing bytes at revision `09ab56b8fdc2efcc3b58b203644537d84dd5ac9e` (tree `ba63deba89c8852fb578ec0fcd9593a9cf0251e5`), whose parent is `681360e6be40ffbc47fb7aadaa5eac0cd39cf22e`. Current lane tip observed: `5856614ac4bf7f2363bbcd1956644474a82108e5`. Freeze: `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`.

## Result

- The committed `anchor-coverage.tsv` enumerates 41 `(SOURCES row,digest)` anchor slots, with 35 carried by copied bytes (including decoded S023 JSON, S035 Go members, and archived S048 members) and 6 structural slots. I did not use the map hash as a content proxy: independently hashed copied files/member streams and fetched npm/Go upstream objects.
- S048's landed deterministic tar is exactly 28 members, 2,324,480 bytes, SHA-256 `dca1b4edb39c8768c18aa1aeb21950f4b513ef1e24e1b9460a2f6f48d15bad92`. Its contents are 27 `dist`-relative files plus package-relative `bridge/ghidra/ReaGhidraBridge.java`. All 24 S048/S066/S070/S079/S083/S090/S092 anchor-cited 6.5.0 member files in this tar hashed identically to the corresponding members of a freshly downloaded 6.5.0 npm tarball (SHA-256 `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699`). The five formerly missing files are present and match: `domain/pcap/pcapAnalysis.js` (`7651b4c5…597c641`), `pcap/PcapProvider.js` (`16a4d813…33ed64d4`), `pcap/PcapNativeBound.js` (`24811182…830838cd2`), `ghidra/GhidraTargetSnapshot.js` (`a27e4107…f03f52b`), and `bridge/ghidra/ReaGhidraBridge.java` (`db16aed4…79c0a105`).
- 6.7.0 tarball freshly fetched SHA-256 `20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90`; all three copied S081 member digests match source tarball bytes.
- S035: each of the three pinned files in both committed version tars matches its row digest; freshly fetched raw Go tag sources for both `go1.25.0` and `go1.24.6` independently match those same six copy members.
- Direct copied bytes also match S001, S002, S003 member archive, S006, S007, S023 (after `gzip -dc`), S040, S056, S066, S083. S003's live host ZIP itself hashes to the row's container pin.
- The six non-byte slots are precisely: S003's `Base-src.zip` container digest (map `source_sha256`; two cited Java members are copied and checked); S081's 6.7.0 tarball digest (verified from fetched source tarball and recorded in its map provenance note, while only three cited members are copied); S082's two values (installed tinyxxd binary digest appears as text in copied `mtree`; package tarball digest appears as `%SHA256SUM%` text in copied `extra.db` member); and S090/S092's shared 6.5.0 tarball digest (verified against fetched upstream tarball and stated in the SOURCES anchors). They are not falsely represented as archived member bytes.
- No mismatch found in this assigned anchor-coverage audit. This does not erase the C2 score stop: committed score `c2-at-09ab56b8.json` exits 1 because `sources_numstat_three_additions` is false (`sources_numstat` is `4\t0\tcorpus/SOURCES.md`); its gate is green and content audit reports 136 checks/0 failures. Thus the inspected committed evidence itself records an honest failed target, independent of the byte-coverage result.

## Commands and outputs

All commands ran read-only against committed lane files, or downloaded only the npm package tarballs and Go source files into `/fast/scratch/hyaku/kaidoku-r43/w2/R43W2C2Pins/`. No REA, unblob, sasquatch, or firmware extraction was run.

1. `df -h /fast/scratch/hyaku` → `/dev/nvme1n1p2 804G 205G 599G 26%`; scratch created only under the assigned seat path.
2. `curl -fsSL -o <scratch>/rea-agents-6.5.0.tgz https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz; sha256sum <file>` → `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699`.
3. `tar -tf corpus/evidence/round-42/local-sources/S048/rea-agents-6.5.0-cited-members.tar | wc -l` → `28`; `wc -c <file` → `2324480`; `tar -tvf <file>` listed the 28 paths, including all five additions. `tar -xOf <committed S048 tar> <member> | sha256sum` compared with `sha256sum <scratch>/npm/package/dist/<member>` (package-relative bridge uses `package/bridge/...`) → MATCH for all 24 cited member paths. Full per-member hashes were emitted in the command output during this audit.
4. `curl -fsSL -o <scratch>/rea-agents-6.7.0.tgz https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz; sha256sum <file>` → `20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90`; compared S081 archive streams `dist/domain/evidence.js`, `dist/domain/canonicalDigest.js`, `package.json` against extracted package members → all three MATCH.
5. `tar -xOf` for each `map_swiss.go`, `map_noswiss.go`, `map_select_swiss.go` in each committed S035 archive; hashes respectively `0e2fedbedf244b5fe360a3c6e5ca71502ea6ee7a4043bd83b96a13d1af76c383`, `03db5a82addb4c8cb471aa93b0b75c3eee8ecf39326ee646f398a9b2e25a7291`, `c16b55b87bb7b5873fea4b9468ee60cb24d9b33240c5e58f7ede6584af799718`; then `curl -fsSL` each file from `https://raw.githubusercontent.com/golang/go/{go1.25.0,go1.24.6}/src/internal/abi/` → all six upstream SHA-256 values match the corresponding archive members.
6. `sha256sum` direct copies and `gzip -dc S023/go1.25.0.json.gz | sha256sum`; results match the row/source pins: S001 `056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692`; S002 `18b8828aec6476be03ca92bdb9506c47cc9ef8c1415c37d33e4af2f8c55cf8f9`; S003 copy tar `ba1f1209766abada1a4c4ae6262904f23f13efc0bfc2f99ea9f1a7eab31e6c94`; S006 `a23562a3175409a66e12e5ba47bd19e218cd7868b03bc3210c4ae7e0d296c33e`; S007 `c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4`; S023 compressed copy `ad405f00949215aa32de7314ae7fc3fc60303c599c62841afb943dc9a9cb7e05`, decoded `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252`; S040 `c4d56e038151ce3fa700692fb0701f3651c05add34e6e7cb1d2eef8b9b4f6aaa`; S056 `41963156f6330ecf7b8d8b62e00da6a563ad5312fca82afac38f51c996255dd3`; S066 `fdc1fc13d2468fa0bcaf1e1bf585c80dc9840f059f78a623d7be420f76d30549`; S083 `64c07dae6fe8b79a2015550cd8de208bc41f7b325dddd7262031ef76820c00df`.
7. `sha256sum` S003 host `Base-src.zip` → `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`; copied tar's two cited Java members hash to `2415ceba3ea5250774fff51d43f6b22656a83713372f090701a10e49ad581d95` and `765d25365a8c379c929097a6602df5fa75049f871eb0f610d5376d630d95eb7d`.
8. `gzip -dc S082/mtree` visibly contains `sha256digest=7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65`; `tar -xOf S082/extra-db-tinyxxd-1.3.17-1-desc.tar tinyxxd-1.3.17-1/desc` visibly contains `%SHA256SUM%` = `3f84d7de243de1391f97cfbc90adf01bb5b784fccb249372b67accf4e65607ce`. These are correctly classified as copied metadata values, not copied binary bytes.

## Exact read-path hashes

- `plans/round-43-claims.md` `0326dff974d48df575486256dbd5a0b36593dbc84155d0d40560b64d3c20d83e`
- `corpus/SOURCES.md` `251ec4a72ee3dcf1f0f5e45debc001be2333c0340b661e616ebceaaedb62c68c`
- `corpus/evidence/local-sources.json` `3158cdc982fc07d263198ab0eaeee2adb9ca9d8cf4ebb662ea640c1c0491148e`
- `.ufo/waves/round-43/l1/scores/c2-at-09ab56b8.json` `126b529eb5c3b0d61eaceb5f2e026eb3de9b0a9c2256239eabd86a23eaad9f4e`
- `.ufo/waves/round-43/w1/artifacts/R43C2Land/receipts/anchor-coverage.tsv` `897045990f41c83e36db9048e1ccd7f81f67168e85104a65e5da703d98ccfa59`
- `.ufo/waves/round-43/w1/artifacts/R43C2Land/receipts/reverify.tsv` `011378f982269717c1e3a400b9ed9c85233875a9cbcedffa4f2da74fd86f5286`
- S035 Go 1.25.0 tar `069d0c887b475efa4a4d98acc7803e2f56cdfd4812244457803d2c2a00fc0df3`; Go 1.24.6 tar `8530a509c4d28765b68292bb5c3fda670fb53e8a8700dce90b0a567bf21a11d1`
- S048 tar `dca1b4edb39c8768c18aa1aeb21950f4b513ef1e24e1b9460a2f6f48d15bad92`; S081 tar `11c07d925277ee136d430fe1e329151d39b63192ee866c2e54e64430dc89f42d`
- S082 copied `desc` `a2d70e537e159315625038c38cc2d54830617431db384b2b5caf0d9da8cd5456`; `mtree` `a5e4c9e67d9c608f0b7c8603cd68ebab5d9d97f4cddfbf85c2b4ced0365fea58`; desc-member tar `4c1d650f1528d17c0c9fd3000f5df257923e799e24dddd38c75edbe22e68bb31`.

## Limitations

This audit independently checks digest reproduction and upstream identity for the assigned content surfaces; it is not an independent re-run of all 136 provenance-verifier checks. The score receipt remains the canonical observed C2 stop: source-row numstat is four insertions, not the required three. No tools installed. Scratch cleanup is recorded by the seat report.
