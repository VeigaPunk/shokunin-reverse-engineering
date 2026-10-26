DONE — SOURCES candidate for REA 6.5.0's outcome vocabulary opened. The published tarball's integrity equals the registry's, and all 1574 `dist/` files are byte-identical to the installed copy. There are **six** `extraction_gaps` kinds, not three. File:line and located quote are recorded per kind below.

Seat: R39SrcReaGapKinds. Date 2026-10-26. Lane base a2f64e1d. Nothing edited in the lane except this report and `.ufo/waves/round-39/w1/artifacts/R39SrcReaGapKinds/`.

## 1. Integrity (observed)

Commands run in `$S=/fast/scratch/hyaku/kaidoku-r39/R39SrcReaGapKinds`, scratch since removed:
- `curl -sSL -o rea.tgz https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz`
- `openssl dgst -sha512 -binary rea.tgz | base64 -w0` gives `C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==`.
- `npm view rea-agents@6.5.0 dist.integrity dist.shasum` gives `sha512-C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==` and `7ea5e6f669bc18c45dbf5dba653edaa1ada07ab3`.
- `sha1sum rea.tgz` gives `7ea5e6f6…` and equals `dist.shasum`.
- **The sha512 integrity matches.** It also matches what S080 already records.
- Tarball sha256: `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699` (artifact `tarball.sha256`).
- `diff -rq x/package/dist $HOME/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist` printed nothing.
- Per-file sha256 lists (`find . -type f | sort | xargs sha256sum`), both 1574 lines, are `cmp`-identical: artifacts `dist-sha256-published.txt` and `dist-sha256-installed.txt`.
- The installed `package.json` says version 6.5.0.
- Key-file sha256 (artifact `key-files.sha256`):

| file | sha256 |
|---|---|
| `dist/firmware/FirmwarePublication.js` | `bb4f3246bee70a5b32b048e5ef956e649626b6449b1d457454440739a8d51029` |
| `dist/firmware/FirmwareReports.js` | `6885966b78451b3d2761e76543c6fa81688293da9ec7af692fdac211624cba16` |
| `dist/firmware/FirmwareFiles.js` | `f6934b7bd71208d82a5ff076ec720dd304245236de0a85c8de8c6f90ffe3073a` |
| `dist/domain/firmware/firmwareAnalysis.js` | `2cbc1cc4ceaa760a8e47b8883a6b7b85040d640032546864fa9cba4898243aa5` |
| `dist/cli-runtime/cli.js` | `168cd322a29c9baed02d7e44ab5ae9b2634b3f5b872ff5fcfa3bd20b718e2204` |

The unbundled modules above are the readable source. `cli-runtime/cli.js` and `mcp/main-kBXHZ8S5.js` are bundled duplicates of the same code with different line numbers. Both are listed where they matter.

## 2. Gap-kind table

The enum is `domain/firmware/firmwareAnalysis.js:84-91`: `z.enum(["missing-extractor-dependency","unknown-chunk-handler","encrypted-chunk","depth-limited","extractor-failure","unpublished-entry"])`. The bundled copy is `cli-runtime/cutterToolContracts-TZH9EHr5.js:1797-1802`.

Paths are relative to `package/dist/`. "Pub" is `firmware/FirmwarePublication.js`. "Rep" is `firmware/FirmwareReports.js`.

| kind | condition (what makes REA emit it) | file:line | located quote (≤25 words) |
|---|---|---|---|
| `missing-extractor-dependency` | A producer report of `__typename__ == "ExtractorDependencyNotFoundReport"` with a non-empty `dependencies`. Three emit routes: (a) nested under one chunk, `chunk_missing_dependencies`, which carries handler, range and `provider_id`; (b) a MultiFile stage report; (c) task-wide `missing_dependencies`, with null handler and range. | Pub:161-182 (a), Pub:183-195 (b), Pub:197-205 (c); Rep:75-78 (accepted report shape), Rep:171-188, Rep:195-223, Rep:320-335. Continuation text Pub:13. Bundled cli.js:14065, 14176-14206. | Pub:13 "REA installs nothing. Add the named dependency to your own environment and rerun extract_firmware on the same immutable input with a fresh output_directory" |
| `missing-extractor-dependency` with empty `dependencies: []` | The report was found but named nothing, or named `""`. This gets the distinct "unnamed" continuation. | Rep:180-182 (`length === 0 \|\| includes("")` sets `unnamed`), Rep:193 (`facts.unnamed ? [{ dependencies: [] }]`); Pub:20, Pub:177-179. | Pub:20 "The producer reported a missing extractor dependency without naming it; its identity is unavailable in this evidence." |
| `extractor-failure` (chunk) | A `ChunkReport` whose `extraction_reports` is non-empty (`extraction_failed`) AND `handler !== null` AND `encrypted !== true` AND the same `[input_path, provider_id]` has no dependency row. | Rep:284 (`extractionFailed = detail !== null && detail.extraction_reports.length > 0`), Rep:301; Pub:241 (`dependencyChunkKeys`), Pub:288-293; schema `domain/firmware/firmwareAnalysis.js:78-79`. Continuation text Pub:16. Bundled cli.js:14068, 14271. | Pub:288-293 "chunk.extraction_failed === true && chunk.handler !== null && chunk.encrypted !== true" |
| `extractor-failure` (stage) | (i) A `MultiFileReport` with non-empty `extraction_reports` and no dependency report inside. (ii) A task-level `ExtractorExecutionErrorReport`. Both carry null range. | Rep:310-337 (i, kind chosen at Rep:332-334), Rep:257-267 (ii); Pub:275-285. Bundled cli.js:14260-14270, 14765-14770, 14823. | Rep:257 `item.__typename__ === "ExtractorExecutionErrorReport"` ; Pub:284 "The producer retained this extraction stage's failure in diagnostics." |
| `unpublished-entry` | After extraction, an output-tree entry that is not a regular file. REA publishes only regular files. It records the entry as `unpublished_entries[]` with `kind` `symlink` or `special`, and forces `coverage` to `"partial"`. | Pub:68-75 (non-file pushed to `unpublished`), Pub:103 (`unpublished.length > 0 ? "partial"`), Pub:301-308 (gap row); `firmware/FirmwareFiles.js:175-185` (kind from `lstat`); schema `domain/firmware/firmwareAnalysis.js:137-141`. Bundled cli.js:14070, 14280-14285. | Pub:18 "The entry is retained as metadata; only regular files are published, without executable permission bits." |
| `unknown-chunk-handler` | A chunk whose `handler === null` (an `UnknownChunkReport`, a carved region with no format handler). | Pub:286; Rep:268-309; Pub:14 (continuation); nested variant Pub:31-38. | Pub:286 `chunkGaps("unknown-chunk-handler", (chunk) => chunk.handler === null)` |
| `encrypted-chunk` | A chunk with `encrypted === true`. | Pub:287; Pub:15. | Pub:15 "No static extraction continues past encryption; treat the region as unexamined rather than empty or corrupt." |
| `depth-limited` | A task whose `depth >= maxDepth`. | Rep:229-230; Pub:294-300; Pub:17, Pub:24-28. | Pub:17 "Rerun extract_firmware with a higher max_depth (up to 10) and a fresh output_directory to descend into this path." |

### Fields and sections the assignment named

| item | what it is | file:line | located quote |
|---|---|---|---|
| `dependencies` field | A string array on each gap row. It is empty for every kind except `missing-extractor-dependency`, where it holds the executable names the producer reported. | `domain/firmware/firmwareAnalysis.js:100-101`; Pub:39-46 (`emptyGap.dependencies: []`); Rep:171-194 | firmwareAnalysis.js:100 "Extractor executables named by the producer; empty when it named none." |
| `unpublished_entries` | `{relative_path, kind: "symlink"\|"special", link_target}[]`. It is filled from output entries that are not regular files. | schema firmwareAnalysis.js:137-141; Pub:99-105; FirmwareFiles.js:175-185. Bundled cli.js:14139 | firmwareAnalysis.js:139 `kind: z.enum(["symlink", "special"])` |
| `diagnostics` | `z.array(jsonValueSchema)`. Two inputs: (1) any report on a task whose `__typename__` is outside the `known` set, as `{input_path, report}`; (2) each chunk or MultiFile `extraction_reports` item, wrapped by `extractionDiagnostic` as `{input_path, stage?, missing_dependencies?, report}`. | schema firmwareAnalysis.js:151; Rep:65-74 (`known`), Rep:109-119, Rep:253-255, Rep:287, Rep:317; Pub:109 | Rep:254-255 "if (!known.has(item.__typename__)) diagnostics.push(jsonValueSchema.parse({ input_path: path, report: item }));" |
| `coverage` | `"partial"` if `depths.length>0` OR `diagnostics.length>0` OR any chunk has `handler===null` or `encrypted===true`. Publication forces `"partial"` when `unpublished.length>0`. | Rep:419-423; Pub:103 | Rep:419-421 "depths.length > 0 \|\| diagnostics.length > 0 \|\| chunks.some((c) => c.handler === null \|\| c.encrypted === true)" |
| `report.__typename__` / `command` | These two come from **unblob, not REA**. REA copies unblob's JSON report verbatim into `diagnostics[].report`. `__typename__` comes from `Report.__typename__`. `command` is a field of `ExtractCommandFailedReport`, created when the extractor exits non-zero. `stdout` and `stderr` are base64. A missing binary raises `FileNotFoundError`, which becomes `ExtractorDependencyNotFoundReport(dependencies=self.get_dependencies())`. | unblob 26.6.4 `report.py:34-39` (Report/`__typename__`), `report.py:91-103` (`command: str`, `stdout`, `stderr`, `exit_code`, base64 serializer), `report.py:118-122`, `report.py:125-130` (`ExtractorTimedOut`), `report.py:133-138` (`MaliciousSymlinkRemoved`); `extractors/command.py:59-68`, `:69-77`, `:78-84`, `:101-102` | command.py:60-65 `error_report = ExtractCommandFailedReport(command=command, stdout=res.stdout, stderr=res.stderr, exit_code=res.returncode,)` |

## 3. Mappings this fixes (for the C2 triage table)

All checked against the lines above and the R38 receipts.

1. **Observed live outcomes** on `corpus/evidence/round-38/c1/K1..K4/{before,after}.json`, read with a python3 one-liner over `normalized_result`:

| carrier | run | `coverage` | `extraction_gaps` | `unpublished_entries` | `diagnostics` | `files` |
|---|---|---|---|---|---|---|
| K1-K4 | before (sasquatch-v4be unreachable) | partial | `missing-extractor-dependency` `$input` `squashfs_v4_be` deps `['sasquatch-v4be']` | none | `ExtractorDependencyNotFoundReport` | 0 |
| K1 | after | partial | none | none | `MaliciousSymlinkRemoved` | 5 |
| K2 | after | partial | `unpublished-entry` for `$output/firmware.bin_extract/var/lib/run-link` | `run-link` (`symlink`) | none | 3 |
| K3 | after | complete | none | none | none | 4 |
| K4 | after | complete | none | none | none | 4 |

2. **A "partial" coverage does not imply a gap row.** In K1-after, `MaliciousSymlinkRemoved` is not in the `known` set (Rep:65-74). It lands in `diagnostics` (Rep:254-255), which flips `coverage` to partial (Rep:419-421). No gap kind is derived from it. Only `unpublished-entry` and the dependency/failure kinds come from the gap builder.

3. **Why `unpublished-entry` instead of the symlink being removed (K2 vs K1).** unblob's `fix_symlink` (`extractor.py:50-92`) does two things:
   - It unlinks loops, empty targets and traversal-escaping links, and emits `MaliciousSymlinkRemoved` only for loops and escapes (`extractor.py:58-65`, `:81-87`).
   - It rewrites in-tree links to relative form (`extractor.py:88-91`). Those survive and then become REA `unpublished-entry` rows (K2).

4. **The dependency row suppresses the failure row for the same chunk.** `dependencyChunkKeys` (Pub:241) excludes chunks that already have a dependency row from the generic `extractor-failure` emission (Pub:293). A missing `sasquatch-v4be` therefore yields one `missing-extractor-dependency` row, not two.

5. **`dependencies` names the executable actually invoked, not the handler's full set.**
   - `Command.get_dependencies()` returns `[self._executable]` (`command.py:101-102`).
   - `SquashFSExtractor.extract` builds `Command(executable, …)` with the v4BE executable for BE v4 (`handlers/filesystem/squashfs.py:39-41`, `:65`), while the extractor's own `get_dependencies` lists `sasquatch` and `sasquatch-v4be` (`:68-69`).
   - The K1-K4 receipts show `['sasquatch-v4be']` only. [INFERENCE] a missing plain `sasquatch` would name `sasquatch`. The other half of that conclusion was not executed here.

6. **AVM-marker case.** A BE v4 image with `bytes_used == mkfs_time` (`squashfs.py:47-50`) is run without `-be`. The probe `.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/rea-k1-avm.json` shows the resulting outcome:
   - `extractor-failure`, handler `squashfs_v4_be`, `dependencies: []`.
   - Diagnostic `ExtractCommandFailedReport` with `command` `sasquatch-v4be -no-exit-code -f -d … ` and `exit_code` 1.
   - Base64 stderr decodes to "SquashFS version [1024.0] / inode count [184549376] suggests a SquashFS image of a different endianess…" (decoded text from the probe `summary.json`).
   - Coverage partial, 0 files.

7. **Probable dead branch.** The REA branch at Rep:257 keys on `ExtractorExecutionErrorReport`, a name that does not appear in unblob 26.6.4.
   - `grep -rn ExtractorExecutionError` over the installed unblob package returned zero hits. The only hit anywhere was `firmware/FirmwareReports.js:257`.
   - It is also absent from `BUILTIN_REPORT_TYPES` (`report.py:340-360`).
   - [INFERENCE] The task-level stage `extractor-failure` row is unreachable with unblob 26.6.4. An unblob extractor failure reaches REA as chunk-level `extraction_failed`, as in the AVM probe. This was not tested with a crafted report.

8. **Extractor timeouts.** A timeout (`ExtractorTimedOut`, `command.py:78-84`) is not a dependency report, so it would surface as chunk `extractor-failure` with `dependencies: []`. [INFERENCE] not exercised here.

## 4. Draft SOURCES row (11 columns)

Next free id in the lane `SOURCES.md` is S118 (last row S117). L1 renumbers if needed.

```
| S118 | rea-agents 6.5.0 package tarball, firmware outcome code — https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz (members `package/dist/firmware/FirmwarePublication.js`, `firmware/FirmwareReports.js`, `firmware/FirmwareFiles.js`, `domain/firmware/firmwareAnalysis.js`), file-for-file identical to the installed copy `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/`; with unblob 26.6.4 `report.py` and `extractors/command.py` for the producer-side `command` field | code | A | The `extract_firmware` outcome vocabulary of REA 6.5.0 only: the six `extraction_gaps` kinds, their emit conditions, and the `dependencies`, `unpublished_entries`, and `diagnostics` fields; not the unblob extractors, not other REA versions, not any image | tarball `dist.integrity` `sha512-C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==` (matches `npm view rea-agents@6.5.0 dist.integrity`), tarball sha256 `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699`; all 1574 `dist/` files sha256-identical to the installed copy; `firmwareAnalysis.js:84-91` kind enum; `FirmwarePublication.js:13-18` continuations, `:161-205` dependency rows, `:286-308` unknown/encrypted/failure/depth/unpublished rows; `FirmwareReports.js:253-255,419-423` diagnostics and coverage; unblob `report.py:91-98` `command: str`; quote `FirmwarePublication.js:18` "The entry is retained as metadata; only regular files are published, without executable permission bits." | Read an REA `extract_firmware` outcome by gap kind and field before attributing it to the image: a dependency row is an environment gap, `extractor-failure` carries unblob's `command`/`exit_code` in `diagnostics[].report`, `unpublished-entry` is a symlink or special entry REA does not publish, and `partial` coverage can arise from diagnostics alone | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md |
```

Related rows already present: S080 holds the same integrity and S079 the identical-copy claim for other members. The S118 scope is the firmware outcome code, so it is not a duplicate. Neither `extraction_gaps` nor `FirmwarePublication` appears in any current `SOURCES.md` row.

## 5. Gaps and limits

- Nothing was run through REA this wave. All conclusions come from source reading plus the R38 receipts and the R38 AVM probe envelopes.
- The `ExtractorTimedOut` and `ExtractorExecutionErrorReport` mappings (items 7-8) are source-only [INFERENCE].
- Quote word counts were checked by eye against the ≤25-word limit.
- Installed unblob is 26.6.4: `unblob-26.6.4.dist-info` under `lib/python3.13/site-packages/`. sha256 for the four unblob files cited is in artifact `unblob-26.6.4-files.sha256`.
- No tools installed or updated. Scratch removed (see below).

Artifacts (`.ufo/waves/round-39/w1/artifacts/R39SrcReaGapKinds/`): `tarball.sha256`, `dist-sha256-published.txt`, `dist-sha256-installed.txt`, `key-files.sha256`, `unblob-26.6.4-files.sha256`.
