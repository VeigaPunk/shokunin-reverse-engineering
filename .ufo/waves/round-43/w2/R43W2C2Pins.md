# R43W2C2Pins — anchor-digest falsification

## Verdict

**No counterexample to C2 anchor digest coverage found in this assigned audit.** On the measured C2 landing revision `09ab56b8fdc2efcc3b58b203644537d84dd5ac9e` (tree `ba63deba89c8852fb578ec0fcd9593a9cf0251e5`), I independently verified the 41 `(row,digest)` anchor slots: 35 are reproduced in committed copy bytes and six are structural source/container or copied-metadata pins. S048's committed archive has 28 members and all 24 unique anchor-cited 6.5.0 files match the freshly fetched upstream package by SHA-256. The five S048 gaps reported against the earlier 23-member pack are present and match.

This does **not** turn the C2 score green. The committed score at the measured revision exits 1: `sources_numstat_three_additions` is false because `corpus/SOURCES.md` changed by `4\t0`, not the frozen required `3\t0`. Score receipt reports gate exit 0, copy audit 136 checks/0 failures, but `checks_ok: false`. For the audited axis, the direct byte evidence supports coverage; the C2 overall claim remains stopped by its own recorded landing predicate. This is an honest stop, not a digest mismatch.

## 41 slots / six structural slots

The 35 byte-reproduced slots are enumerated by the committed C2 anchor coverage receipt, then independently checked here using the committed payloads and upstream sources:

- byte-pinned slots: S023 (decoded gzip payload); S035 (three Go files in each of two tars); S056 (one); S066 (two); S070 (three); S079 (six); S081 (three package members); S083 (three); S090 (four); S092 (nine). S003's one row slot is structural, as below. Total byte slots = 35.
- structural slots, not falsely described as archived member bytes:
  1. **S003** — the pinned Ghidra `Base-src.zip` container digest `f00d29c2…a8d804` is map `source_sha256`; the container itself is above the copy bound. Both cited Java source members are in the copied tar and hash correctly.
  2. **S081** — the 6.7.0 package tarball digest `20958a66…f51f90`; source tarball was freshly fetched and matched; the copy intentionally contains three cited package members, not the whole upstream tarball.
  3. **S082** — installed tinyxxd binary digest `7b1e5d0c…03ae65` appears as text in copied `mtree`; package tarball digest `3f84d7de…607ce` appears as `%SHA256SUM%` text in the copied repository `desc` member.
  4. **S090** and **S092** — each row's digest pin is the same 6.5.0 package tarball container digest `531717a0…18e699`; fresh upstream tarball matched, and their cited package member bytes are separately present in S048.

Thus 35 + 6 = all 41 slots. The six do not collapse into the map hash: I checked the independently pinned container/source object or the metadata bytes carrying each value.

## S048's 28-member archive

Committed path: `corpus/evidence/round-42/local-sources/S048/rea-agents-6.5.0-cited-members.tar`; SHA-256 `dca1b4edb39c8768c18aa1aeb21950f4b513ef1e24e1b9460a2f6f48d15bad92`; size 2,324,480 bytes. `tar -tf` returned 28. Exact member paths:

1. `application/DirectAnalysis.js`
2. `application/binaryDiagnostics/BinaryLayoutService.js`
3. `application/reverse/ReverseEngineeringService.js`
4. `artifacts/readStableArtifact.js`
5. `bridge/ghidra/ReaGhidraBridge.java`
6. `cli-runtime/cli.js`
7. `cli/reverseEngineeringCommands.js`
8. `contracts/reverseEngineeringToolContracts.js`
9. `domain/analysisView/analysisView.js`
10. `domain/analysisView/binaryLayoutView.js`
11. `domain/canonicalDigest.js`
12. `domain/evidence.js`
13. `domain/pcap/pcapAnalysis.js`
14. `domain/reverseEngineering.js`
15. `domain/sqlite/sqliteDatabase.js`
16. `ghidra/GhidraTargetSnapshot.js`
17. `go/GoElfImage.js`
18. `pcap/PcapNativeBound.js`
19. `pcap/PcapProvider.js`
20. `rust/RustAuditableReader.js`
21. `rust/RustBinaryImage.js`
22. `sqlite/SqliteDatabaseFailures.js`
23. `sqlite/SqliteDatabaseInspection.js`
24. `sqlite/SqliteDatabaseLimits.js`
25. `sqlite/SqliteDatabaseProvider.js`
26. `sqlite/SqliteDatabaseSnapshot.js`
27. `sqlite/SqliteDatabaseWorker.js`
28. `sqlite/SqliteDatabaseWorkerExecution.js`

The 24 unique cited member paths across the six 6.5.0 rows S066/S070/S079/S083/S090/S092 were individually streamed from this tar and compared to the fetched upstream tarball; every digest matched. In particular, all five previously missing S048 pack members now occur in the tar: `domain/pcap/pcapAnalysis.js`, `pcap/PcapProvider.js`, `pcap/PcapNativeBound.js`, `ghidra/GhidraTargetSnapshot.js`, and package-root `bridge/ghidra/ReaGhidraBridge.java`.

## Direct evidence and exact paths/hashes

- Measured tree: `09ab56b8fdc2efcc3b58b203644537d84dd5ac9e` → `ba63deba89c8852fb578ec0fcd9593a9cf0251e5`; current tip observed separately: `5856614ac4bf7f2363bbcd1956644474a82108e5`.
- Plan `plans/round-43-claims.md`: `0326dff974d48df575486256dbd5a0b36593dbc84155d0d40560b64d3c20d83e`.
- Table `corpus/SOURCES.md`: `251ec4a72ee3dcf1f0f5e45debc001be2333c0340b661e616ebceaaedb62c68c`.
- Map `corpus/evidence/local-sources.json`: `3158cdc982fc07d263198ab0eaeee2adb9ca9d8cf4ebb662ea640c1c0491148e`.
- C2 score `.ufo/waves/round-43/l1/scores/c2-at-09ab56b8.json`: `126b529eb5c3b0d61eaceb5f2e026eb3de9b0a9c2256239eabd86a23eaad9f4e`.
- Existing anchor table `.ufo/waves/round-43/w1/artifacts/R43C2Land/receipts/anchor-coverage.tsv`: `897045990f41c83e36db9048e1ccd7f81f67168e85104a65e5da703d98ccfa59` (41 slots, 35 covered / 6 structural).
- Existing reverify receipt `.ufo/waves/round-43/w1/artifacts/R43C2Land/receipts/reverify.tsv`: `011378f982269717c1e3a400b9ed9c85233875a9cbcedffa4f2da74fd86f5286` (133 checks, zero failures; used as a cross-check, not as a substitute for my byte comparisons).
- Committed copy hashes: S001 `056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692`; S002 `18b8828aec6476be03ca92bdb9506c47cc9ef8c1415c37d33e4af2f8c55cf8f9`; S003 member tar `ba1f1209766abada1a4c4ae6262904f23f13efc0bfc2f99ea9f1a7eab31e6c94`; S006 `a23562a3175409a66e12e5ba47bd19e218cd7868b03bc3210c4ae7e0d296c33e`; S007 `c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4`; S023 gz `ad405f00949215aa32de7314ae7fc3fc60303c599c62841afb943dc9a9cb7e05` (decoded bytes `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252`); S035 1.25.0 tar `069d0c887b475efa4a4d98acc7803e2f56cdfd4812244457803d2c2a00fc0df3`, 1.24.6 tar `8530a509c4d28765b68292bb5c3fda670fb53e8a8700dce90b0a567bf21a11d1`; S040 `c4d56e038151ce3fa700692fb0701f3651c05add34e6e7cb1d2eef8b9b4f6aaa`; S048 `dca1b4edb39c8768c18aa1aeb21950f4b513ef1e24e1b9460a2f6f48d15bad92`; S056 `41963156f6330ecf7b8d8b62e00da6a563ad5312fca82afac38f51c996255dd3`; S066 `fdc1fc13d2468fa0bcaf1e1bf585c80dc9840f059f78a623d7be420f76d30549`; S081 tar `11c07d925277ee136d430fe1e329151d39b63192ee866c2e54e64430dc89f42d`; S082 `desc` `a2d70e537e159315625038c38cc2d54830617431db384b2b5caf0d9da8cd5456`, `mtree` `a5e4c9e67d9c608f0b7c8603cd68ebab5d9d97f4cddfbf85c2b4ced0365fea58`, repo-desc tar `4c1d650f1528d17c0c9fd3000f5df257923e799e24dddd38c75edbe22e68bb31`; S083 `64c07dae6fe8b79a2015550cd8de208bc41f7b325dddd7262031ef76820c00df`.
- Fetched upstream sources under seat scratch: 6.5.0 npm tar `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699`; 6.7.0 npm tar `20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90`. Go raw tagged sources for both versions each matched the three row values: `map_swiss.go` `0e2fedbedf244b5fe360a3c6e5ca71502ea6ee7a4043bd83b96a13d1af76c383`; `map_noswiss.go` `03db5a82addb4c8cb471aa93b0b75c3eee8ecf39326ee646f398a9b2e25a7291`; `map_select_swiss.go` `c16b55b87bb7b5873fea4b9468ee60cb24d9b33240c5e58f7ede6584af799718`.
- S003 host container at `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` exists and hashes to row/source pin `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`; copied member digests are GoRttiMapper `2415ceba3ea5250774fff51d43f6b22656a83713372f090701a10e49ad581d95` and GoApiSnapshot `765d25365a8c379c929097a6602df5fa75049f871eb0f610d5376d630d95eb7d`.

## Commands, outputs, exit codes, limits

- Read frozen plan first; read current lane tip and committed score, map, table, and C2 audit receipts. `git show -s` confirmed measured revision and tree above.
- Scratch guard: initial `df -h /fast/scratch/hyaku/kaidoku-r43/w2/R43W2C2Pins` returned exit 1 because the seat directory did not yet exist. Then `df -h /fast/scratch/hyaku` returned exit 0 with 599G free (26% used); created only the assigned scratch/artifact directories.
- Downloaded only `rea-agents` npm tarballs and official Go source files into own scratch; all curl/tar/hash/read-only comparison commands exited 0. Results and exact commands are preserved in `artifacts/R43W2C2Pins/anchor-digest-audit.md`.
- No third-party firmware was opened or copied; no REA/unblob/sasquatch runs, package installs, git mutations, whole-repo checks, or subagent dispatch.

## Axes and correction

Impacted axis: **coverage**. This specific attack found no digest-coverage defect; the six structural slots are properly identified as non-byte container/metadata evidence. The overall C2 score is still red for the independently recorded `SOURCES.md` numstat mismatch. Smallest safe correction for this audit: none to the copy bytes or S048 membership. L1 should preserve the honest C2 stop unless its frozen numstat clause is satisfied by the actual landing evidence; do not treat this coverage result as a green score.

Report artifact: `.ufo/waves/round-43/w2/artifacts/R43W2C2Pins/anchor-digest-audit.md`.
