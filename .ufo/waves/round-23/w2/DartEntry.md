# DartEntry: source review of the R23 Dart knowledge entry

- Candidate: `2838351450ff1ee4baa620c962a1153450d53311`; baseline `aa1450b82f9ede35aada63efe8a34e01c6e02f72`
- Subject: `corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md` (blob `7d24fb83a4`, sha256 `22711853c6a9ee31ce31669db17e8c8bef95892ba9c6831321704c2bd0178351`)
- Seat: KaidokuR23.DartEntry, leaf source review. No REA command, no `describe-dart.py`, no `count-c1.py`, no `preflight_dart_carrier.py`, no APK parse, no device, remote or process access.

## Method

- Candidate bytes came only from `git show <rev>:<path>`, copied byte-for-byte into the ignored `.ufo/waves/round-23/runtime/DartEntry/cand.*` (29 files). Blob ids came from `git rev-parse`; sha256 was computed on the copies.
- Baseline comparison used `git rev-parse B:path` against `R:path`.
- JSON was read with Python. Text was read with line-numbered `read` and `grep` on the copies.
- Line numbers below refer to the candidate blob.

## Verdict by requested item

| Item | Result |
|---|---|
| Four-symbol table | Values match the committed envelope exactly. Column labels "Dynamic symbol" and "File offset" need a base and citation (F9). |
| Section magic and length | Values match. The magic constant is not recorded. The producer's "Dart 2.14 FullAOT" attribution of kind 3 is unrecorded and conflicts with other committed version labels (F3). |
| Instruction false magic is not a data failure | Conclusion is supported by committed producer text. The "Not a data header" label is layout inference filed under an Observation label (F5). |
| Lower bounds | Partly supported. Scope is narrower than the producer's text, the cap flag it names is absent from the record, and saturation values are unrecorded (F6, F7). |
| Unchanged R22 refusal | PASS. All six R22 artifacts are byte-identical at B and R. Refusal content matches the entry text. |
| Overall | Needs repair before admission. F1 (recheck overclaim) and F2 ("first successful" overclaim) are the material defects. The rest are wording or scope repairs. |

## Findings

### F1 · High · The recheck is described as recomputing values it only copies · observed

- Entry lines 44–46 say the table, source count, hash and lower-bound values "are recomputed from the committed envelope by the `recheck:` command."
- `describe-dart.py` (blob `37d0c66a75`, sha256 `145b09bb734692a371ee6b4971de8a2270547826be840f92d435b40f86a5234f`) prints `libapp` (sections, magic_valid, kind, header_length, snapshot hash and sources) verbatim. It also prints `string_pool.coverage`, `package_uri_count_at_least`, `dart_uri_count_at_least` and `limitations` verbatim.
- Its only computed items are the envelope sha256 and four equality booleans: `stdout_byte_equal`, `argv_target_matches_subject`, `subject_digest_matches_fetch`, `command_matches`.
- No branch compares section offsets, sizes, magic, kind, header length, snapshot hash, source count or any lower bound against APK bytes. Its exit 2 covers only read errors.
- It omits `class_like_token_count_at_least` (4000) and `printable_run_count` (50666), although the entry names token projections among its lower bounds.
- Entry line 3 uses the placeholder `--rev <MEASURED-COMMIT>`, so the recheck is not runnable verbatim.
- Rule violated: QUALITY #21 (`corpus/QUALITY.md` line 31) says a validator's exit 0 "is described only by the fields it recomputes"; a copy must not be described as a recomputation. QUALITY #2 (falsifiable) is nominal, because the recheck cannot falsify the table.
- Repair: say the values are copied from the committed envelope, name the four booleans and the envelope sha256 as the only recomputed items, and name a concrete measured commit. Any real recomputation is a separate change.

### F2 · Medium · "First successful `inspect-dart-aot`" is contradicted by committed successful probes · observed

- Entry line 7: "Coverage-map ground: first successful `inspect-dart-aot`."
- Committed connector outputs (`evidence/c1/connect-dart-symbols/`) include two successful runs captured at `2026-10-21T14:42:37Z`:
  - `inspect-dart-aot-saber-1330203.envelope.json` (blob `2168e9698e`, sha256 `7ee2c3c0b9254e1f1c96a78b43fdf7023f4d206eab74543df30fe7d2a2ab84c1`), `ok:true`, exit 0, libapp coverage complete.
  - `inspect-dart-aot-saber-1340303.envelope.json` (blob `43d2f03601`, sha256 `22d1acd01c8dcb71d0bc63bf516e23114e25ef1615b790cf621b9631ebb7c69d`), `ok:true`, exit 0, coverage complete. APK sha256 is `ac68a976b1bfb8456bc062b9fd80a4a2098717a227d59ff771cda825b36b8b8d`, a second build.
- L1's run was captured at `14:47:19.045031Z`. The connector's 1330203 record has the same APK digest, and its normalized_result, libapp, string_pool and limitations equal L1's. Only `target.path` and the path-derived evidence_id differ (`ev_dcdab9d0…` against `ev_d2ff19d7…`).
- Entry lines 30–31 call the connector outputs "speculative/probe" outputs. They do not state that those outputs succeeded or share the digest. The connector README (`cand.cd_readme`, blob `0d91c3ff05`) calls 1340303 a "corroborating run, exit 0".
- The LOG (line 2636) and the lessons row (line 52) say only the L1 run is admitted.
- Repair: "first admitted, L1-produced successful inspect-dart-aot." Disclose the two earlier successful connector runs with their digests, as probe receipts, not failures.

### F3 · Medium · The producer's completeness conditions and version attribution are not recorded; committed version labels conflict and remain unresolved · observed, unknown

- Envelope limitation 3 (`evidence/c1/inspect-dart-legacy-saber.envelope.json`, blob `f75bdc238a`, sha256 `7768198e07329ce23d239c39deeaf34b8f2664457aaa7a955f3b328445d4c508`) says: "complete decoding supports kind 3 (the Dart 2.14 FullAOT layout), a valid hash and a declared length that fits its symbol, including the four magic bytes; other kind values remain observed with partial coverage."
- Entry line 35 says only "scoped to the reader's section/header contract."
- On the committed values, all conditions hold: kind 3 on both data rows, header_length 16842 ≤ 18384 and 6058354 ≤ 7153168, one snapshot-hash candidate, two sources. The entry should enumerate them.
- Three unreconciled version assertions exist in committed bytes:
  - (a) The producer's "Dart 2.14 FullAOT layout" comment (limitation 3).
  - (b) The connector's carrier matrix (`cand.cd_carriers`, blob `6e6a46e17a`, sha256 `652f05a626078250f617f7f4f3b5d64ca56d286b8654137757a5009ba983f2c6`), `carriers[1].libflutter.dart_version_string` = "3.11.4 (stable)…", from libflutter.so bytes that are not retained. Unverifiable here.
  - (c) REA identify on the same APK (`cd_idenv1330`, blob `9932ec575d`, sha256 `3d56fe45b4a3d0428091128229e41c6a9fbc686180b3a1ac66fe0c24c56b9626`): `libflutter.dart_version: null`, `dart_version_capped: false`.
- Entry lines 54–55 ("No SDK version is inferred from a bare snapshot hash") are true but silent on (a)–(c). Record the version as unknown. Do not let "legacy" carry a version reading.

### F4 · Medium-low · The "legacy-layout" label is undefined in the entry and defined only by an unadmitted author-side boundary · observed

- The label appears in the entry file name, in file paths on entry lines 15, 26 and 28 (`inspect-dart-legacy-saber`, `legacy-saber-download`), in the S061 title (`sources` line 67), in README index rows (`cand.readme` lines 72 and 159), and in LOG line 2607.
- The only definition is connector-authored: `carriers.json` `boundary.legacy_layout` ("Dart <= 3.12 …") and `boundary.inference` (line 305), which dates the boundary from dart-lang/sdk commit `d36adbacaf` (cited in the connector run record's `sources`). No SOURCES row admits that commit or any Dart-version boundary.
- Repair: define the label as REA-6.5.0-relative (the four expected symbol names plus kind-3 headers), or remove it from titles and index rows. Do not import the connector's version boundary.

### F5 · Medium-low · "Not a data header" is layout inference filed under an Observation label; citation and magic constant missing · observed

- Entry line 33 opens with "**Observation:**" and introduces the table (lines 37–42). Rows 39–40 say "Not a data header." The envelope records only `magic_valid:false`, `kind:null`, `header_length:null`. "Not a data header" is not an envelope field.
- Supporting producer text exists but is not cited: limitation 3 says "Snapshot hash sources are the headers at the start of the VM and isolate data symbols." The connector preflight (`cand.cd_preflight` line 88) also parses headers only for `…Data` symbols.
- QUALITY #5 (`corpus/QUALITY.md` line 15) says "layout-derived claims are inference, never 'observed behavior'." Relabel the classification as inference and cite limitation 3.
- Entry lines 53–54 ("not silently reclassified") are accurate: the table relabels explicitly. The coverage-complete result is unaffected. libapp coverage is complete with two magic_valid:false instruction rows, and no limitation makes instruction magic a failure criterion.
- The entry does not record the expected magic. The connector preflight uses `0xDCDCF5F5` read little-endian (`cand.cd_preflight` line 42). That constant is author-side and unsourced.

### F6 · Medium · The lower-bound statement is narrower than the producer's, cites a cap flag absent from the record, and omits the saturation values · observed

- Entry lines 50–51: "package URI and token projections are capped lower bounds."
- Producer limitations:
  - 6: "string-pool counts are lower bounds: collection stops at twice each projection bound, and any value beyond that is counted only through the capped flag."
  - 7: "String-pool collection or printable-run capacity was exceeded; counts are lower bounds and overflowed runs are omitted."
  - 8: "package_uris reports 500 of at least 1000 distinct URIs."
  - 9: "class_like_tokens reports 2000 of at least 4000 distinct tokens."
- Observed values: `package_uri_count_at_least` = 1000 (list length 500); `class_like_token_count_at_least` = 4000 (list length 2000); `dart_uri_count_at_least` = 215 (list length 215); `printable_run_count` = 50666 (no bound field).
- For packages and tokens, the "at least" value is exactly twice the listed length. These are collection stop points, not estimates.
- The string "capped" appears once in the envelope, inside limitation 6. No `capped` field exists in `string_pool` or anywhere in `data`. The cap condition the producer names is not recorded.
- Printable-run overflow (limitation 7) covers `printable_run_count`, which the entry omits.
- Repair: state the four bound values and that they are stop points. State that printable_run_count is a lower bound with overflow. State that the cap flag named by limitation 6 is absent from the envelope.

### F7 · Low · Six of 500 listed package URIs are not canonical package URIs · observed

- Entries in `normalized_result.string_pool.package_uris` that fail fullmatch against `package:[a-z0-9_]+/[A-Za-z0-9_./-]+\.dart`:
  - `package:abstract_sync/src/sync_file.dart#`
  - `package:background_downloader/src/chunk.dart]`
  - `package:flutter/src/foundation/isolates.dart*`
  - `package:flutter/src/material/app_bar.dartx`
  - `package:flutter/src/material/divider.dart ` (trailing space)
  - `package:flutter/src/widgets/router.dart<`
- Inference: the roughly 500 unlisted entries of the "at least 1000" may include similar byte-run artifacts. Repair: call these "package-like byte-pattern runs" (limitation 4).

### F8 · Low · Missing spaces between labels and numbers in exact-value text · observed

- Entry line 18: `size41263437 bytes`. Entry line 41: `kind3, declared length16842`. Entry line 42: `kind3, declared length6058354`.
- Same pattern elsewhere in the new round text:
  - `sources` line 64: `sigrok-cli0.7.2`, `opened2026-10-21`.
  - `sources` line 65: `and625kHz at9600baud`, `opened2026-10-21`.
  - `sources` line 66: `sigrok0.7.2`.
  - `sources` line 67: `REA6.5.0`, `opened2026-10-21`.
  - LOG line 2639: `SHA25649d2f597…`.
  - Lessons lines 51–52: `Keep102`, `distinguish13`.
- The same pattern is in unchanged R22 text (`entry22` blob `41b69636af`): `size16778120`, `size13051424`. Do not edit frozen R22 text. Repair new R23 text.
- Verified with regex `(size|length|kind|at|and)[0-9]{2,}` on the copies.

### F9 · Low · Table column bases are unspecified · observed, inferred

- Entry line 37 labels the offsets "File offset," but the envelope field is `offset` with no stated base. The largest section end (7298944 + 10038688 = 17337632) is below `libapp.bytes` (17367984). That is consistent with offsets inside `lib/x86_64/libapp.so` (inferred). The connector preflight computes file offsets inside the libapp bytes (`cand.cd_preflight` lines 81–90). Name the base.
- Entry line 37 "Dynamic symbol" matches limitation 2 ("located through the ELF dynamic symbol table").

### F10 · Low · The zoneless `verified-at` is not stated as unchecked · observed

- Entry line 2: `verified-at: 2026-10-21, round23`. QUALITY #23 (`corpus/QUALITY.md` line 33): "Zoneless timestamps are not checked and are stated as unchecked."
- Checked by reading, not run: the zoned evidence timestamps (L1 run `14:47:19.045031Z`, L1 download `14:47:18.289487Z`, connector fetch `14:43:18Z`, carriers `14:45:00Z`, connector runs `14:42:37Z`) all precede the committer time of `2b40aec` (`11:56:57-03:00` = `14:56:57Z`). No future-dating observed. The `evidence-timestamps.py --strict` check still needs its own run.

### F11 · Low · The admitted L1 run record keeps no resolved tool identity · observed

- `run23` keys: `argv, captured_at, cwd, env_overrides, exit, stderr, stdout`. The argv pins `rea-agents@6.5.0` through `npx -y`.
- The connector record `cd_run1330` keeps `resolved_tool` {version 6.5.0, package_path under `~/.npm/_npx/…`, node v24.21.0, npx 11.19.0}. L1's record does not.
- QUALITY #18 (line 28) is met for argv, stdout, stderr and exit. The resolved package identity for the admitted run is unknown.

## Passed checks (observed in committed bytes)

- Table values: names, offsets, sizes, magic_valid, kind and header_length match `normalized_result.libapp.sections` in the envelope exactly (entry lines 39–42).
- Digests and IDs: libapp sha256 `f82ab4111807552af82ada747c5cccfe49474ecfcce49d5e0c3c701feeab38a8` (entry line 34). APK sha256 `a7b1f5c8c077aafc8903eb8246d9b6f5fc8ebb4829dc5cb32bd2cdd8ba3ea618` (entry line 19; matches the fetch receipt and the envelope subject). Bytes 41263437. Evidence id `ev_d2ff19d7100f34b52e4b2bc52ee115e48428624f7da57814e5f184b4bd4c7491` (entry line 29). ABI x86_64. Snapshot hash `78da37fed6bf1489361a312568249f3f`, `snapshot_hash_sources` 2, one candidate (entry line 44).
- Run: argv `npx -y rea-agents@6.5.0 inspect-dart-aot <abs apk> --format json --full-output`. `argv[4]` equals `subject.local_path`. Exit 0. Empty stderr. The envelope bytes equal run stdout (87293 bytes, byte-equal).
- Fetch receipt `legacy-saber-download.json`: status 200, size 41263437, sha256 as above, "signature_verification: not performed; digest identity only." Matches entry lines 13–22.
- Ranges: all four symbol ranges lie inside libapp bytes. Each data header_length is ≤ its symbol size.
- Independent connector records (not admitted) show the same header_length values (16842, 6058354), kind 3 and snapshot hash (`cand.cd_carriers` lines 177–186).
- R22 unchanged at B and R (all SAME): `env22` (blob `36698856e8`, sha256 `2b13cb8fad6d21fdd9633e8fc28d5e06326c6fe0e119462d54f77966e3c5c145`), `run22` (blob `aeac0341a7`, sha256 `d1eaa23f96ec4a9695af4f373051da8ad3e87fc3dff3bbee083eed5eaf2eb34a`), `idenv22` (blob `02d21d4f31`, sha256 `143af76e3969c6a79f591115a55b0fd581dfab13a10db5c72fda0b8306f9904b`), `idrun22` (blob `2371c116ac`, sha256 `6b2c24d9599542b812f1facac864f8767d07b11a27f14f4d244a3459cca6068f`), `dl22` (blob `05951a5192`, sha256 `f635c723cdeaf01051cdf4efa8db5b41aa7e1bee1d74662c7f1303d255800edb`), `entry22` (blob `41b69636af`, sha256 `417482ef5f275afdd96f1c7d09dcde08b47556fd8116494712d3541c614c7dd8`).
- R22 refusal content (`env22`): code `unsupported_target`. Names all four symbols absent from the dynamic symbol table. `run22` argv targets `/tmp/kd22probe/saber.apk`, exit 1. This matches `entry22` and the R23 entry's lines 7–9.
- Counting linkage (read, not run): the first line is `source: S061 …` (`count-c1.py` line 102). The S061 row is status mined, date 2026-10-21, and its used-by column includes the entry path (`sources` line 67; `count-c1.py` lines 105–107).
- README index rows are present (`cand.readme` lines 72 and 159).
- The connector README digest table (`cand.cd_readme` lines 13–21) matches committed blobs for all nine listed files (sha256 recomputed on the copies).
- Runtime copies are ignored: `.ufo/waves/round-23/.gitignore` line 1 is `/runtime/`, and `git check-ignore` matched the copy path.

## Produced files and hashes

- `.ufo/waves/round-23/w2/DartEntry.md` (this report). Its sha256 cannot be embedded in itself; it is reported in the seat's final message.
- `.ufo/waves/round-23/runtime/DartEntry/cand.*` (29 byte copies of candidate blobs via `git show`, ignored). Key sha256 values:

| Copy | Blob (R) | sha256 |
|---|---|---|
| entry23 | 7d24fb83a4 | 22711853c6a9ee31ce31669db17e8c8bef95892ba9c6831321704c2bd0178351 |
| env23 | f75bdc238a | 7768198e07329ce23d239c39deeaf34b8f2664457aaa7a955f3b328445d4c508 |
| run23 | 448820b214 | 588460380006a5c1044ba8fb9b8b0136446a2cab5c40e8f2f911978328e82fa6 |
| dl23 | a94a698185 | 2e6c00305dfbaf09001c421df6e4cf0730dcce3bfb7a5aa5acc358873da40496 |
| desc23 | 37d0c66a75 | 145b09bb734692a371ee6b4971de8a2270547826be840f92d435b40f86a5234f |
| count23 | 0f966a5001 | f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2 |
| cd_env1330 | 2168e9698e | 7ee2c3c0b9254e1f1c96a78b43fdf7023f4d206eab74543df30fe7d2a2ab84c1 |
| cd_run1330 | ddb4dbcdab | 4b263db8e6060a659f1cf81aab3df025b4014afecdd59258464d57351fe7938d |
| cd_env1340 | 43d2f03601 | 22d1acd01c8dcb71d0bc63bf516e23114e25ef1615b790cf621b9631ebb7c69d |
| cd_run1340 | df066d1a69 | 34f4ab462e0df49d6f9ff476e619f6bf2e01da750824771da5c8e1e8f78b3db3 |
| cd_idenv1330 | 9932ec575d | 3d56fe45b4a3d0428091128229e41c6a9fbc686180b3a1ac66fe0c24c56b9626 |
| cd_idrun1330 | 48344aa1c6 | 9660b55cc8ed0046f67adace0e75636777c2696e5b111f5b918f9fe196b8cd60 |
| cd_carriers | 6e6a46e17a | 652f05a626078250f617f7f4f3b5d64ca56d286b8654137757a5009ba983f2c6 |
| cd_fetch | c01e93e86e | 6beac67b0f6361accc59729c969965b9b8f0f777f5beaca7dd1ed65b11566f2d |
| cd_readme | 0d91c3ff05 | 83de3786f38854a74e3bfaabf8457a68036ddba2b8cc385d27ddb63ab162b05c |
| cd_preflight | (content) | 08d0c4605c41f6b091d5b5d09172c5254eaf3bbffa8bf8bcf5f5c7b4b105514c |
| sources | daf5ce02b0 | 736857e1fb46cb81ee8bc29b79e595567a400994a83c330f0ccc47f394eb3525 |
| readme | b5863fc2e3 | 795466e5be2ac7341014a30a1a793a1aea17cdbb1f0d3451abc305085a62b57c |
| quality | 4af8644e04 | ba6a20b3632f9f1a6f1e5ad50d9637bffa7933dfb9440d3faac9422b293b2c73 |
| lessons23 | 96ffed835e | 8327a21fbae3c976af820e10063d973f1862a945a041d4b02a90906700a70723 |
| log23 | 9966bfb7d5 | 249553811d364458ddf3964446b97c181cb557db203423ff0b40f9d0032163ef |
| scorecard23 | 7f2adb4e1d | e3c85af02e045fc5a4c07881ac54c49b3cf24056816c49f46ed777484c36aa15 |
| env22 | 36698856e8 | 2b13cb8fad6d21fdd9633e8fc28d5e06326c6fe0e119462d54f77966e3c5c145 |
| run22 | aeac0341a7 | d1eaa23f96ec4a9695af4f373051da8ad3e87fc3dff3bbee083eed5eaf2eb34a |
| idenv22 | 02d21d4f31 | 143af76e3969c6a79f591115a55b0fd581dfab13a10db5c72fda0b8306f9904b |
| idrun22 | 2371c116ac | 6b2c24d9599542b812f1facac864f8767d07b11a27f14f4d244a3459cca6068f |
| dl22 | 05951a5192 | f635c723cdeaf01051cdf4efa8db5b41aa7e1bee1d74662c7f1303d255800edb |
| entry22 | 41b69636af | 417482ef5f275afdd96f1c7d09dcde08b47556fd8116494712d3541c614c7dd8 |

## Installs or none

None. No package, tool or runtime was installed or updated. No pacman, npm or npx invocation. git was used read-only. python3 was used only to parse JSON copies.

## Open risks

- **O1 (unknown, unverified).** REA identify reports `dart_version: null, dart_version_capped: false` for the R22 engine (`idenv22`, blob `02d21d4f31`) and the 1330203 engine (`cd_idenv1330`, blob `9932ec575d`). The connector's byte scans report "3.13.2" (R22 engine, `carriers[0]`, offset 2035994) and "3.11.4" (1330203 engine, `carriers[1]`, offset 2007997). libflutter.so is not retained, so the conflict cannot be resolved from committed bytes. The R22 entry says "The lack of a labeled Dart version string does not establish absence of Dart." Resolution needs retained bytes, not a run from this seat.
- **O2 (observed).** The R22 identify limitation (last item of `idenv22` limitations) says: "libapp.so carries 1 snapshot section(s) … so the library is truncated or nonstandard." The connector classifies the R22 carrier as new-layout (`carriers[0]`: kind 2, new symbol names only). That points to a layout change rather than truncation. The R22 entry does not preserve this limitation. R22 text is frozen; L1 decides the wording.
- **O3 (inferred, outside this item).** `count-c1.py` line 111 treats every 64-hex token in the R23 entry as a candidate evidence id. The entry contains the APK and libapp SHA-256 digests (lines 19 and 34) as well as `ev_d2ff19d7…`. The binder must reject non-evidence digests. The binder was not read here.
- **O4 (observed).** Connector files under `evidence/c1/connect-dart-symbols/` sit inside the counter's evidence root but are cited by no `source:` entry, so the new-entry scan (`count-c1.py` lines 98–124) should not reach them. The Run seat should confirm by running the counter once.
- **O5 (observed).** The scope deviation is disclosed in LOG lines 2634–2636 and lessons row 52 ("ConnectDartSymbols created production-tree carrier/probe files before the explicit L1 stop"). The entry says only "after the connector's scope deviation" (line 2). Naming the deviation (the 1340303 fetch and runs, and `/tmp` scratch paths) would make the provenance checkable.
- **O6 (unknown).** The "Dart 2.14 FullAOT layout" meaning of kind 3 is producer-asserted. No admitted SOURCES row covers Dart snapshot format.

## Verification gaps

- No REA command, `describe-dart.py`, `count-c1.py`, preflight script or APK parse was run. All conclusions come from committed bytes (`git show`) and JSON reads.
- Not checked: the count binder (`bind_cli`), `evidence-timestamps.py --strict`, LOG and SCORECARD arithmetic, and lessons beyond the rows cited.
- No outside admission. Ownership and authentication are not claimed.
