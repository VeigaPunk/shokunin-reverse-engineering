# R26-C1 cache confound — rea-agents 6.5.0 CLI

Scope: source reading only of the installed 6.5.0 package plus a read-only hash and line-anchor check. No REA call was made. Question: could the C1 base / same-path repeat / byte-identical-copy comparisons be served from a cache, and would a cached answer carry the same evidence id as a fresh one?

Package root: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (version 6.5.0, `package.json:4`, sha256 a5003023…050a6c). Below, `$PKG` is that root.

## Verdict
Observation: on the frozen C1 argv there is no cache between a base run and its repeat, and none between base and the copy. Each `npx` invocation is one CLI process; the source says so at `$PKG/dist/application/DirectAnalysis.js:22` ("every CLI invocation is intentionally isolated and does not retain a target or provider client for a subsequent command"). The only result caches are (a) an in-memory, session-lifetime snapshot cache, (b) caller-supplied snapshot files read only when `--snapshot` is passed, and (c) the Ghidra project and target copy, created inside a fresh `mkdtemp` root per provider start and removed on close. No cache key includes the user path; all keys are content-keyed.
Inference: a same-path repeat can be served from a cache only if the invocation supplies `--snapshot` with an existing file, or if it runs inside one long-lived MCP session. Neither holds for the frozen argv (`verbs_argv` has no `--snapshot`). A path-keyed cache does not exist in the package.

## Cache inventory
| cache | location | key | lifetime | reachable from frozen argv |
|---|---|---|---|---|
| Analysis snapshot, in memory | `$PKG/dist/application/binary/AnalysisSnapshotCache.js:30,162-164` (`Map`, ceiling 10 000) | `analysisQueryId` = sha256 of canonical `{target, binding, operation, parameters}` (`$PKG/dist/domain/analysisSnapshot.js:330-332`); `target` = sha256/kind/format/architecture(/entry_point), explicitly "path-free" (`analysisSnapshot.js:234-248`) | one process / MCP session | no — one operation per CLI process; map starts empty |
| Analysis snapshot file | `$PKG/dist/application/binary/AnalysisSnapshotFiles.js:9`; read at `$PKG/dist/application/DirectAnalysis.js:144,317-320` | same query id, plus an evidence record matched on subject sha256, operation, provider, profile and canonical parameters (`analysisSnapshot.js:271-295`) | caller-controlled file | no — requires `--snapshot` (`$PKG/dist/cli/coreBinaryCommands.js:24-28`); C1 argv omits it |
| Ghidra project | `$PKG/dist/ghidra/GhidraLauncher.js:328,441` | location `<mkdtemp>/project`, name `rea-project`, import of `<mkdtemp>/target-<sha12><ext>` (`$PKG/dist/ghidra/GhidraTargetSnapshot.js:14`), `-readOnly -deleteProject` (`GhidraLauncher.js:380-381`) | one provider start; runtime root removed on close (`$PKG/dist/ghidra/GhidraClient.js:395,600-650`) | it runs, but is empty each run — nothing to reuse |
| Ghidra HOME/cache/config/data | `$PKG/dist/ghidra/GhidraLauncher.js:536-538` | all redirected under the same per-run `<mkdtemp>` root (`ghidraRuntimePaths`, `GhidraLauncher.js:440-451`) | one provider start | fresh and deleted |
| `~/.cache/rea/cutter-bridge` | `$PKG/dist/cutter/CutterBridgeClient.js:176` | Cutter bridge only | host | no — not on the Ghidra or pwntools path |
| npx package cache | `$PKG` itself | package spec `rea-agents@6.5.0` | host | supplies identical code, not answers |
| pwntools layout runtime | `$PKG/dist/native/pwntools/PwntoolsLayoutProvider.js:15` → `$PKG/dist/process/PrivateRuntimeRoot.js:38` | fresh `mkdtemp(…, "rea-elf-layout-")` per call | one call | fresh; no result store |

Scan basis (`surface-scan.py` over unbundled `dist/**/*.js`): 4 `XDG_CACHE_HOME` rows (only Ghidra's per-run redirect is a provider path), 1 `homedir()` row (Cutter bridge), 15 `mkdtemp` calls (all fresh temp roots, none a stable cache directory).

## What the evidence id hashes
Observation: `computeEvidenceId` is `"ev_" + sha256(canonicalJson(semanticProjection))` (`$PKG/dist/domain/evidence.js:156-182`, `$PKG/dist/domain/canonicalDigest.js:8`). The projection includes subject digest/format/architecture but not subject name or `local_path`; it includes parameters, raw_result, normalized_result, limitations, locations, profile and provider. The displayed path is deliberately outside the id; parameters and result content are inside it. The executed bundle carries the same code (`$PKG/dist/cli-runtime/reconstructionObligationLedgerSchemas-Bao0xMr-.js:536-557`).
Cached versus fresh id:
- In-memory replay: `lookup` returns the stored execution with an appended limitation "Loaded from a local REA analysis snapshot; this call did not re-run the provider." (`AnalysisSnapshotCache.js:183-186`). That string is hashed, so the replay's id differs from the fresh id; in a persistent session a cached repeat would look unstable, not equal.
- File snapshot replay: `snapshotEvidenceForQuery` returns the stored, authenticated evidence record (`analysisSnapshot.js:281-294`), so the id equals the original fresh id. Target matching ignores the path (`analysisSnapshot.js:255-261`), so a snapshot taken on `/usr/bin/jq` would also answer the alt copy if operation and parameters matched.

## Per-verb inference (frozen `verbs_argv`)
Hashed parameters come from the CLI registration: `binary_overview {}` (analyze and inspect), `procedure_pseudo_code {procedure}` (decompile), `xrefs {address}`, `read_bytes {address,length}` (`$PKG/dist/cli/coreNativeCommands.js:63`), `analyze_function {procedure}`, `read_function_instructions {procedure}`, `inspect_binary_layout {path}` (`$PKG/dist/application/binaryDiagnostics/BinaryLayoutService.js:61`).
| verb | cache consulted | base vs repeat | base vs copy |
|---|---|---|---|
| analyze | none; fresh Ghidra client | ids equal iff Ghidra output is deterministic across processes; no cache in between | same expectation; parameters are `{}` and the target identity is path-free, so the copy hashes identically if the provider output does |
| inspect | same operation and `{}` parameters as analyze | as analyze; analyze and inspect should therefore share an evidence id for one carrier | as analyze |
| decompile | none | deterministic decompiler text gives equal ids | same; the provider sees only `<mkdtemp>/target-<sha12>.bin`, never the user path |
| xrefs | none | as decompile | as decompile |
| read-bytes | none | exact 64 bytes at one address are expected to repeat | same |
| function | none | dossier ordering could vary; any difference is provider nondeterminism | as function |
| instructions | none | deterministic listing text expected | same |
| inspect-binary-layout | none; fresh pwntools subprocess | equal iff the decoder repeats; the path is identical in both runs anyway | id must differ: `{path}` is hashed and the result embeds `artifact.path` (`PwntoolsLayoutProvider.js:18`), forcing a path-sensitive verdict |

## Which verdicts could be caching artifacts
- Content-keyed, any verb: only if `--snapshot` had been passed with a snapshot holding a base entry (file replay returns the stored id, and target matching ignores the path). Not the case: no C1 argv contains `--snapshot`, and the pre-freeze probe did not create one.
- Unstable, any verb: not from caching on the frozen argv. It would be the signature of an in-memory replay inside a persistent session (extra limitation hashed), or genuine run-to-run provider variation. C1 uses one-shot CLI processes, so only the latter applies.
- Path-sensitive, `inspect-binary-layout`: an artifact of the verb's own contract, not of caching and not proof of a path-sensitive reader. The absolute path is an input parameter and is echoed in `normalized_result.artifact.path`, so the id must differ even for byte-identical files.
- For the seven Ghidra-backed verbs a path-sensitive verdict cannot come from path hashing (path is excluded from subject identity and parameters) and cannot come from the provider distinguishing paths (it receives the content-derived snapshot copy). A differing copy id would indicate run-to-run nondeterminism or an input difference, not path sensitivity, and needs a second repeat to diagnose.

## Evidence
All commands read-only; exit codes and UTC times as observed. Artifacts live under `/fast/scratch/hyaku/kaidoku-r26/seats/CacheConfound/` with these sha256 values:
```
6beb4464bc9520c47317d66ede0ebb94ae3867eb6509f55b5bdd61813fa9ee09  cite-check.py
eec3d84991c3f95c5bc4c5707a02f5a7242f83dbe2c362e43e20b31755b7d4f2  citations.json
7f9355835187317cb251545194c56aca87e1bbd7cb701fe21f34aaf595b78e3d  surface-scan.py
07ec45a277eecb3f245e8990c92a2b352583e736403e8469620ed00ef3abab59  surface.json
a1250b54d047876a6aaffa486a4daf47d65d9d3c4bab35ee25aed91cbba83ddc  sources.sha256
7d987b996b3df6d517acc02c435d6a05b753d50a7e464f9eea930188c0f9cc40  runs.txt
```
- 2026-10-22T12:19:23Z: created the seat directory (exit 0).
- 2026-10-22T12:19:40Z: first `cite-check.py` run, exit 1, 48 citations, 1 failure — an off-by-one anchor (`canonicalDigest.js:9`; the declaration is line 8). Anchor corrected; no package file was changed.
- 2026-10-22T12:19:55Z: corrected run, exit 0, `RESULT citations=51 failures=0`.
- 2026-10-22T12:20:11Z: `surface-scan.py`, exit 0; counts above.
- 2026-10-22T12:20:46Z: `sha256sum -c sources.sha256`, exit 0, 24 files OK.
- 2026-10-22T12:21:04Z: final `cite-check.py`, exit 0, `54 0` from `citations.json`.
Tool installs or upgrades: none.

## Confidence and unknowns
Observation: all 54 cited file:line anchors contain the quoted text; the package is 6.5.0.
Inference (high): no path-keyed or content-keyed result cache is on the frozen C1 path; cached-answer id equality can arise only through a `--snapshot` file, which is absent.
Unknown: whether Ghidra's analysis is deterministic across fresh projects on this host — not tested here, and not a cache question. Unknown: whether the C1 runner accidentally inherits a `--snapshot` option or an MCP session; the frozen argv says no, and I did not observe a run. Unknown: npx was not executed, so the resolver's install choice per call is inferred from the fixed installed root, not observed.
