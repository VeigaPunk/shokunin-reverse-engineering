# RecomputeIds — round 26, wave 1

Seat `KaidokuR26.RecomputeIds`; lane base `a0639d8e61e486e2a716ff94cddd89a73200a02c`. Scope: how rea-agents 6.5.0 mints `.data.evidence_id` for the eight R26-C1 verbs, a standard-library recompute
instrument, and the per-envelope recompute result. Only this report file was written in the lane; no REA call was made by this seat (all envelopes came from the four Run\* seats) and no tool was
installed or upgraded. "Package root" below is `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/` (`package.json` `"version": "6.5.0"`); package paths are relative to it.

## 1. The minting function

**The minting function** is `computeEvidenceId` at `dist/domain/evidence.js:182`, file sha256 `f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff`: `const computeEvidenceId = (evidence)
=> \`ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}\`;`

**The hashed projection** is `semanticProjection` at `dist/domain/evidence.js:156-180` (same file): `subject` reduced to `digest`, `format`, `architecture`; plus `provider`, `analysis_profile`,
`predicate_type`, `operation`, `parameters`, `raw_result`, `normalized_result`, `confidence`, `authority`, `environment`, `limitations`, `relationship_coverage` (only when not `null`), `locations`,
`evidence_links`. **The digest** is `digestCanonicalValue` at `dist/domain/canonicalDigest.js:8-25` (encoder `emitCanonical` `:27-88`), file sha256
`f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9` — SHA-256 over RFC 8785-style canonical JSON (object keys by UTF-16 code unit, arrays in order, `JSON.stringify` escapes). **The
caller** is `createEvidence` at `dist/domain/evidence.js:234-241`; `normalizeEvidenceObservation` builds the record at `:256-315`; `authenticatedEvidenceSchema` at `:133-140` re-verifies a stored id
against `computeEvidenceId`. **The subject's `name` and `local_path` are excluded** (`evidence.js:157-162`) — the structural reason most verbs are path-insensitive. **The shipped runtime bundle**
carries byte-identical logic at `dist/cli-runtime/reconstructionObligationLedgerSchemas-Bao0xMr-.js:536` and `:557`, sha256 `81d775c4db3329718f6acb98e7933ed580ce9b8ee5befdb50060115f879899f5`; that is
the chunk `dist/cli-runtime/cli.js` loads.

Call sites deciding what enters the projection per verb. `dist/application/DirectAnalysis.js:280-296` — generic binary verb path, `createEvidence(subject ?? openedTarget, provider, { operation: tool,
parameters: input.arguments, result, rawResult, limitations, locations })`; the argument object never holds the file path, the path is consumed separately. `dist/application/DirectAnalysis.js:252-259`
+ `dist/application/WorkflowEvidence.js:26-31` — composed-workflow path for `analyze`/`inspect`, forwards `parameters` unchanged. `dist/application/FunctionAnalysisEvidence.js:20-26` — `function`,
`parameters: arguments_`, `result: dossier.value`. `dist/application/binaryDiagnostics/BinaryLayoutService.js:54-68` — `inspect-binary-layout`, `parameters: input.data` (:61), `result: value` (:62,
carries `artifact.path`), `locations: [{ kind: "artifact-path", path: value.artifact.path }]` (:67). **The only one of the eight that puts the path into `parameters`, `normalized_result` and
`locations`.** CLI wiring (the argument object that becomes `parameters`): analyze `dist/cli/coreBinaryCommands.js:88` → `binary_overview`; inspect `:98` → `binary_overview`; decompile `:130` →
`procedure_pseudo_code`; xrefs `:182` → `xrefs`; function `:241` → `analyze_function`; instructions `:270` → `read_function_instructions`; read-bytes `dist/cli/coreNativeCommands.js:63` →
`read_bytes`; inspect-binary-layout `dist/cli/binaryDiagnosticsCommands.js:34`.

## 2. Per-verb path-bearing fields in the hashed projection

"Path-bearing" = a field inside the projection whose value is the artifact path. The subject's own `local_path` is outside the projection and is not listed.

| Verb | Path-bearing fields in the projection (file:line) | Predicted | Observed |
| --- | --- | --- | --- |
| analyze | none (`parameters` is `{}`; `subject.local_path` excluded, `evidence.js:157-162`) | content-keyed | content-keyed |
| inspect | none (same, `coreBinaryCommands.js:98`) | content-keyed | content-keyed |
| decompile | none (`parameters` = only `procedure`, `coreBinaryCommands.js:130-133`) | content-keyed | content-keyed |
| xrefs | none (`parameters` = only `address`, `coreBinaryCommands.js:182-184`) | content-keyed | content-keyed |
| function | none (`parameters` = only `procedure`, `FunctionAnalysisEvidence.js:22`) | content-keyed | content-keyed |
| instructions | none (`parameters` = only `procedure`, `coreBinaryCommands.js:270-272`) | content-keyed | content-keyed |
| read-bytes | none (`parameters` = `address`,`length`, `coreNativeCommands.js:63`) | content-keyed | content-keyed |
| inspect-binary-layout | `/parameters/path` (`BinaryLayoutService.js:61`); `/normalized_result/artifact/path` (`:62`); `/locations/0/path` (`:67`) | **path-sensitive** | **path-sensitive** |

Prediction and observation agree for all eight. Method: base-vs-copy projections compared field by field; for the seven content-keyed verbs the whole projection is equal between the `/usr/bin/jq` run
and the `/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq` run, only `subject.local_path` (outside the projection) differing, while `inspect-binary-layout` differs exactly in the three fields listed.
Caveat observed but not claimed: `analyze`/`inspect` `normalized_result.document` is `target-e815667571d0.bin`, derived from the content digest not the path (`dist/ghidra/GhidraTargetSnapshot.js:14`).

## 3. The recompute instrument

`/fast/scratch/hyaku/kaidoku-r26/seats/RecomputeIds/recompute-ids.py`, sha256 `89afa3756a9b101c8ef6c5274f7ed68dc3533a306812906780949941fd60208b`. Standard library only (`hashlib`, `json`, `gzip`,
`argparse`, `os`, `sys`, `math`). It reimplements `semanticProjection` (`evidence.js:156-180`), `computeEvidenceId` (`:182`) and the canonical-JSON encoder (`canonicalDigest.js:27-88`), then prints
`MATCH`/`MISMATCH` per envelope plus the path-bearing fields found in the projection. Exit 0 iff all match, 1 on any mismatch, 2 on input error. Usage `recompute-ids.py ENVELOPE...` or `--dir DIR`
(scans `*.json`, `*.json.gz`).

Validation on the L1 probe `/fast/scratch/hyaku/kaidoku-r26/l1/probe-ibl.json` (envelope sha256 `689680863a6e3dbd8c5a442aee52042a4601fd37e0555aa6db66d3a8ab3b195a`, matching `claims.json`
`pre_freeze_probe.envelope_sha256`); command `python3 -I -B recompute-ids.py /fast/scratch/hyaku/kaidoku-r26/l1/probe-ibl.json`, exit 0, run 2026-10-22T12:21Z. Output `MATCH`; operation
`inspect_binary_layout`; stored and recomputed id both `ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd`; path-bearing fields in the projection: `/parameters/path = /usr/bin/jq`,
`/normalized_result/artifact/path = /usr/bin/jq`, `/normalized_result/linkage/interpreters/0/display = /lib64/ld-linux-x86-64.so.2`, `/locations/0/path = /usr/bin/jq`.

Two independent cross-checks: (1) `crosscheck.mjs` hashes the same projection with the package's own `dist/domain/canonicalDigest.js` — 25 of 25 match; (2) `probe/dist/cli-runtime/bundle-check.mjs`
re-mints every envelope through the **shipped runtime bundle's own `createEvidence()`** (`probe/dist/cli-runtime/bundle-probe.mjs` — a copy of `reconstructionObligationLedgerSchemas-Bao0xMr-.js` with
`init_canonicalDigest(); init_evidence();` appended, because the bundle's exports are lazily initialised; the installed package was not modified) — 25 of 25 match.

Negative control (three mutated copies of the probe; instrument exit code 1 on the set): `neg-localpath.json` (`subject.local_path` → `/tmp/other/jq`, sha256
`47bed6d3240ff9eadd1a8a1f3f8a0df2ead3eba7708f2edb221b22b9761b976c`) → MATCH as expected, that field being outside the projection; `neg-parameters.json` (`parameters.path` changed, sha256
`7343b1d18d09a1142360dcdd6aee5fdf0a96333c49b5828b46714f11f0292ce5`) → MISMATCH (`ev_b1f2e1b9…`); `neg-resultpath.json` (`normalized_result.artifact.path` changed, sha256
`7c784d628d899e7ac3352151f0f53f4d46b70be642b7b05cb5a20ae580725ecc`) → MISMATCH (`ev_3f4f3f81…`).

## 4. Recompute results per envelope

Command run 2026-10-22T12:21:52Z, exit 0 (full output `recompute-all.txt`): `python3 -I -B recompute-ids.py --dir …/RunAnalyzeInspect/envelopes --dir …/RunDecompileFunction/envelopes --dir
…/RunReadBytesLayout/envelopes --dir …/RunXrefsInstructions/envelopes`.

**Result: 24 match of 24 total** (8 verbs × 3 runs; the complete C1 table population as of 2026-10-22T12:21Z). With the L1 probe: **25 of 25**.

| Verb | Operation | base id | repeat id | copy id | Recompute | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| analyze | binary_overview | `ev_14f9d92f…3d328` | same | same | 3/3 match | content-keyed |
| inspect | binary_overview | `ev_14f9d92f…3d328` | same | same | 3/3 match | content-keyed |
| decompile | procedure_pseudo_code | `ev_03d78618…14df` | same | same | 3/3 match | content-keyed |
| function | analyze_function | `ev_b2b7e9e4…88b5` | same | same | 3/3 match | content-keyed |
| instructions | read_function_instructions | `ev_b20a0f25…25f8b` | same | same | 3/3 match | content-keyed |
| read-bytes | read_bytes | `ev_99b0c6e1…7500c` | same | same | 3/3 match | content-keyed |
| xrefs | xrefs | `ev_d591ef8c…b27c` | same | same | 3/3 match | content-keyed |
| inspect-binary-layout | inspect_binary_layout | `ev_294a449c…a71bd` | same | `ev_52da4b3d…cd161` | 3/3 match | **path-sensitive** |

Seven verbs are content-keyed; `inspect-binary-layout` is path-sensitive (copy id `ev_52da4b3d…` differs from base `ev_294a449c…`). `analyze` and `inspect` yield the same id because both route to
`binary_overview` with empty `parameters` (`coreBinaryCommands.js:88` and `:98`) — the same observation, not a collision.

## 5. Artifacts and sources

Artifacts, all under `/fast/scratch/hyaku/kaidoku-r26/seats/RecomputeIds/`: `recompute-ids.py` `89afa3756a9b101c8ef6c5274f7ed68dc3533a306812906780949941fd60208b`; `crosscheck.mjs`
`f892eccd2aad2d369720b7d7482f5f5788fc688c74d38f4bd48ca162b9498bd5`; `recompute-all.txt` `8c47b6120ea998596639bcd217bfc04fe68def968affa9ba98ea180db725e145`; `recompute-probe.txt`
`7a1c32172a7d882d9832733c0a1a7b190780581a3a79c111c2673f68a7505495`; `recompute-negative.txt` `e9b4855d8555cc223e4c023cdfca36654ddd8ae75070968d2e20d7aa7b9dfbc8`; `neg-localpath.json`
`47bed6d3240ff9eadd1a8a1f3f8a0df2ead3eba7708f2edb221b22b9761b976c`; `neg-parameters.json` `7343b1d18d09a1142360dcdd6aee5fdf0a96333c49b5828b46714f11f0292ce5`; `neg-resultpath.json`
`7c784d628d899e7ac3352151f0f53f4d46b70be642b7b05cb5a20ae580725ecc`; `probe/dist/cli-runtime/bundle-probe.mjs` `33bd46204d78dd1388c9b9433a4b22bb822cb53c62ac581c1c1411c9d682ad43`;
`probe/dist/cli-runtime/bundle-check.mjs` `839db5c61ae915f12b6add922dc8829523130e7a0d29496817d0afe45f276618`; `probe/dist/cli-runtime/bundle-remint-all.jsonl`
`6b2405d3c7a9e2996322237c4e67ce686a4640a1ac4439a85aa0cf82ddf0506f`. `probe/dist/` also holds an unmodified copy of the installed `dist/` tree plus a `node_modules` symlink so the bundle's relative
imports resolve.

Sources, all opened by ordinary file read on 2026-10-22; path relative to the package root unless stated; sha256 of the bytes read; quote with its line:

- `dist/domain/evidence.js` (133-182) sha256 `f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff` — 182: "computeEvidenceId = (evidence) => `ev_${digestCanonicalValue(semanticProjection(evidence), \"Evidence\")}`".
- `dist/domain/canonicalDigest.js` (8-88) sha256 `f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9` — 8: "export const digestCanonicalValue = (value, context = \"Comparison\") => {".
- `dist/application/binaryDiagnostics/BinaryLayoutService.js` (54-68) sha256 see §1 — 61: "parameters: input.data," ; 67: "locations: [{ kind: \"artifact-path\", path: value.artifact.path }]".
- `dist/application/DirectAnalysis.js` (252-296) sha256 see §1 — 282: "parameters: input.arguments,".
- `dist/cli-runtime/reconstructionObligationLedgerSchemas-Bao0xMr-.js` (536-557) sha256 `81d775c4db3329718f6acb98e7933ed580ce9b8ee5befdb50060115f879899f5` — 557: "computeEvidenceId = (evidence) => `ev_${digestCanonicalValue(semanticProjection(evidence), \"Evidence\")}`".
- `/fast/scratch/hyaku/kaidoku-r26/l1/probe-ibl.json` sha256 `689680863a6e3dbd8c5a442aee52042a4601fd37e0555aa6db66d3a8ab3b195a` — `.data.evidence_id`: "ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd".
- `kaidoku-shokunin/.ufo/waves/round-26/claims.json` (repo file, read-only) — `pre_freeze_probe.evidence_id`: "ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd".

## 6. Risks, limits, blockers

- The instrument reproduces the 6.5.0 minting rule as shipped in this npx cache; it is pinned to that package root. Another `rea-agents` version may project different fields and the instrument would have to be re-derived.
- Each verb's verdict depends on `parameters` not carrying the path. That is a property of these eight CLI verbs at this pin, not a general guarantee for rea-agents.
- `inspect-binary-layout` is path-sensitive only because its service places the path in `parameters`, `normalized_result.artifact.path` and `locations`; dropping one of the three would change the verdict without the file bytes changing.
- No blocker. Nothing in the lane was modified except this report; no REA call was made; no tool was installed.
