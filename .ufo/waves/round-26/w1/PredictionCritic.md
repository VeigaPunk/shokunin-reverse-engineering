# PredictionCritic - blind verdict predictions for the R26-C1 table

Seat: KaidokuR26.PredictionCritic (critic, leaf). Attacks: the R26-C1 eight-verb verdict table, by predicting each verdict from rea-agents@6.5.0 source before seeing run outputs.
Source root (read-only): /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/ (package.json version 6.5.0). Paths below are relative to it.
Predictions sealed in this draft at 2026-10-22T12:16:14Z, before any file under seats/Run*/ was opened (only the seat directory names were listed).

## Mechanism (observation, source read)

- The id is `ev_` plus a canonical digest of `semanticProjection(evidence)`: dist/domain/evidence.js:182 and :250-253.
- The projection keeps only subject digest, format and architecture, and drops subject name and local_path: dist/domain/evidence.js:156-163. It does hash parameters, raw_result, normalized_result, environment, limitations, relationship_coverage, locations and evidence_links: :164-179.
- So a verb is path-sensitive only if the caller path reaches one of those hashed fields, and repeat-unstable only if a time, random or per-run value does.
- The executed CLI is dist/cli-runtime/cli.js (scripts/rea.mjs runtimeFiles). The same projection is in the bundle at dist/cli-runtime/reconstructionObligationLedgerSchemas-Bao0xMr-.js:536-557, and the layout evidence at cli.js:7786-7800.

## Seven Ghidra-backed verbs (observation, source read)

- CLI argv to operation and params: analyze and inspect go to binary_overview with `{}` (dist/cli/coreBinaryCommands.js:88 and :98). decompile goes to procedure_pseudo_code `{procedure}` (:130-136). xrefs goes to xrefs `{address}` (:182-184). function goes to analyze_function `{procedure}` (:241-243). instructions goes to read_function_instructions `{procedure}` (:270-272). read-bytes goes to read_bytes `{address, length}` (dist/cli/coreNativeCommands.js:63). No params carry the path.
- The provider is Ghidra: Hopper, Ghidra and IDA are the candidates (dist/composition/binary.js:17-20). The host has GHIDRA_INSTALL_DIR set and no IDA. All seven ops are bridge methods (bridge/ghidra/ReaGhidraBridge.java:431-455).
- Ghidra never sees the caller path. It imports a byte copy named `target-<first 12 hex of sha256><extension>` inside a per-run private runtime root (dist/ghidra/GhidraTargetSnapshot.js:13-14, dist/ghidra/GhidraClient.js:418-441). The program name is therefore content-derived. The bridge contains no getExecutablePath, absolute-path or wall-clock call (grep returned no matches). Its only clock use is a nanoTime deadline at :317-321.
- The evidence fields are built at dist/application/DirectAnalysis.js:280-296 (generic ops), dist/application/FunctionAnalysisEvidence.js:20-33 (function) and dist/application/WorkflowEvidence.js:26-43 (binary_overview, where rawResult is null). raw_result is the raw bridge reply (dist/ghidra/GhidraProviderClient.js:457 and :584). Limitations are static strings (:438-449). Locations are addresses or file offsets only (dist/ghidra/GhidraFunctionValues.js:345-362).
- The per-run `run_id` exists only in the ping handshake, sessionInfo (ReaGhidraBridge.java:419-421 and :501). No hashed result of these seven ops includes the handshake. binary_overview hashes document, image_base, segments, procedure_count and string_count (dist/application/EnhancedTools.js:444-462). The document is currentProgram.getName() (ReaGhidraBridge.java:1975), which is `target-e815667571d0`.
- Provider identity is fixed: ghidra with version null (dist/ghidra/GhidraProviderCapabilities.js:6-10), and rea-workflow version "1" (dist/application/InvestigationProviders.js:3-7).

## inspect-binary-layout (observation, source read)

- The CLI passes `{ path: resolve(args.path) }` (dist/cli/binaryDiagnosticsCommands.js:35).
- The caller path enters three hashed fields: `parameters: input.data` (dist/application/binaryDiagnostics/BinaryLayoutService.js:61), `normalized_result.artifact.path` (:62, set at dist/native/pwntools/PwntoolsLayoutProvider.js:17-21), and `locations: [{kind: "artifact-path", path}]` (:67).
- The pwntools payload itself is path-free, because the decoder reads a snapshot inside a per-run root (dist/native/pwntools/PwntoolsDecoder.js:139-147).
- The hashed result also includes `diagnostics.stdout`, `diagnostics.stderr` and `truncated` (dist/domain/native/binaryLayout.js:162-166, PwntoolsLayoutProvider.js:22). The bridge imports pwnlib.elf with log_level "warning" and a per-run PWNLIB_CACHE_DIR (bridge/pwntools/layout_impl.py:127-131, decoder_runtime.py:28-29), and it does not `import pwn`, so the pwntools update check is not triggered. The expected stderr is empty or constant.

## Predictions (sealed before any run output was read)

| verb | base vs copy | base vs repeat | predicted verdict |
|---|---|---|---|
| analyze | equal | equal | content-keyed |
| inspect | equal | equal | content-keyed |
| decompile | equal | equal | content-keyed |
| xrefs | equal | equal | content-keyed |
| read-bytes | equal | equal | content-keyed |
| function | equal | equal | content-keyed |
| instructions | equal | equal | content-keyed |
| inspect-binary-layout | differ | equal | path-sensitive |

- P-extra (inference): the analyze and inspect ids are byte-equal to each other, because both hash operation binary_overview with params `{}` and the same result.
- P-extra (inference): every inspect-binary-layout envelope contains its run path in .data.parameters.path, .data.normalized_result.artifact.path and .data.locations[0].path. No Ghidra-verb envelope has the caller path inside a hashed field; it appears only in .data.subject.local_path and .data.subject.name, which are not hashed.
- Conditional (unknown): if an address verb fails at 0x103fa0 (for example "not_found" from Ghidra, or analysis_incomplete at ReaGhidraBridge.java:423-427), that envelope has ok false and the derived verdict is no-id. Source cannot settle whether 0x103fa0 is a function start in jq.
- Residual repeat risks (inference, not seen in source): nondeterministic Ghidra auto-analysis or decompiler output across runs; a pwnlib warning that names the per-run snapshot path in stderr.

## Weakness in the falsifier design (inference)

- The copy run cannot detect basename or extension sensitivity. Both carriers are named `jq` with no extension, and both the Ghidra program name (GhidraTargetSnapshot.js:13-14 uses the source extension) and subject.name derive from the name. A "content-keyed" verdict means directory-insensitive at this name, not name-insensitive.
- Smallest safe correction: a disclosed limit line in the table entry, or a fourth run with a differently named copy such as alt/jq.bin. The fourth run is optional and out of the frozen rules.

## Comparison with run outputs (observation)

- Command: `python3 -I -B /fast/scratch/hyaku/kaidoku-r26/seats/PredictionCritic/compare.py`, run 2026-10-22T12:17:08Z, exit 0. Output: compare.out.
- Inputs: 24 envelopes under seats/RunAnalyzeInspect, RunDecompileFunction, RunReadBytesLayout and RunXrefsInstructions /envelopes/, as present at 12:16:46Z. The verdict is derived by the claims.json `derived_verdict` rule. Every envelope had ok true and the carrier sha256 (no NOTE lines).
- Excerpt: `inspect-binary-layout predicted=path-sensitive derived=path-sensitive AGREE`, `hashed_diff base-vs-copy=['.locations[0].path', '.normalized_result.artifact.path', '.parameters.path']`, `disagreements=0`.

| verb | derived | base = repeat id | copy id | agrees |
|---|---|---|---|---|
| analyze | content-keyed | ev_14f9d92f...b3d328 | same | yes |
| inspect | content-keyed | ev_14f9d92f...b3d328 | same | yes |
| decompile | content-keyed | ev_03d78618...6014df | same | yes |
| xrefs | content-keyed | ev_d591ef8c...96b27c | same | yes |
| read-bytes | content-keyed | ev_99b0c6e1...47500c | same | yes |
| function | content-keyed | ev_b2b7e9e4...0488b5 | same | yes |
| instructions | content-keyed | ev_b20a0f25...125f8b | same | yes |
| inspect-binary-layout | path-sensitive | ev_294a449c...a71bd | ev_52da4b3d...cd161 | yes |

- Disagreements: none. 8 of 8 verdicts match.
- P-extra analyze equals inspect: holds for base, repeat and copy (`P-extra analyze==inspect base=True repeat=True copy=True`).
- P-extra path placement: holds. For inspect-binary-layout, the hashed differences between base and copy are exactly the three predicted fields. For the seven Ghidra verbs, the caller path appears in no hashed field (`path_in_hashed=[]`), only in the unhashed subject.local_path.
- Hashed projections are identical leaf for leaf between base and repeat for all 8 verbs. The layout diagnostics are empty in all three runs (stdout "", stderr "", truncated false; read at 12:17:14Z), so the stderr repeat risk did not occur.
- The layout base id equals the L1 pre-freeze probe id in claims.json (ev_294a449c...a71bd, probe at 11:59:16Z), which is one more same-path repeat (observation).

## Verdict

- Attack target: the R26-C1 table verdicts. Result: holds. Source predicts all 8 verdicts and the run envelopes match with 0 disagreements.
- Remaining defect, a tradeoff rather than a fixable bug: "content-keyed" is shown for directory changes only, because both carriers have the basename jq. Impacted axis: depth, through the knowledge entry wording. Smallest safe correction: the entry states "directory-insensitive at an identical basename; basename and extension sensitivity not tested", citing GhidraTargetSnapshot.js:13-14.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r26/seats/PredictionCritic/)

- source-sha256.txt (sha256 of 20 cited package files): b27af8f5736901dea73837b2659cd0cd81d29636b3dca61e93b0a5ab07062f9a
- compare.py: bf59ae24f63c252e0d3bcff45a9222f11b7c3ee293b9752ab894849be6947275
- compare.out: 1f58fd40cd7c1187e4068da2bc68c73c832941e0f11d818d8308bec83e866ada
- No REA call was made by this seat, no tool was installed, and no lane file other than this report was written. Sources were local package files only; no web source was opened.
