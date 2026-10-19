# EX-7 — C1 corpus-entry draft: pathless `analyze_function` Evidence IDs

**Proposed corpus destination:** `corpus/knowledge/2026-10-19-arc3-r12-analyze-function-id-domain.md`  
**Proposed coverage-map token:** `2026-10-19-arc3-r12-analyze-function-id-domain` in the Evidence model row (`corpus/README.md:41`).  
**State:** draft only. No corpus, coverage-map, or tracked file was edited.

## Proposed corpus entry

source: `.ufo/waves/arc3-loop1-round12/claims/c1/EX-7/evidence/{calls.txt,function-base-1.json,function-base-2.json,function-copy.json,input-file.txt,input-sha256.txt,recompute-ids.mjs,recompute-output.json,source-and-input-sha256.txt,command-a-0436f49.json,command-a-5ee13b3.json}`. REA package source identities are recorded in `source-and-input-sha256.txt`.

verified-at: 2026-10-19

recheck: run the three exact calls in `evidence/calls.txt` with `TMPDIR=/var/tmp/kaidoku-ex7-r12`, recreating the byte-identical copy under `/var/tmp/kaidoku-ex7-r12/copy/`; then run the recorded `recompute-ids.mjs` command. This uses the existing cached `rea-agents@6.7.0`; it does not execute the target. Re-run source-derived Command A as specified at `SCORECARD.md:88-124` for the integration revision after the corpus entry and map token are landed.

## Pathless projection result (bounded to one operation and call shape)

I measured `analyze_function` on `/usr/lib/libjq.so.1.0.4`, procedure `jq_next`, through REA 6.7.0. The input is an ELF64 x86-64 shared object with SHA-256 `7e8bccc6df37a55fb90703c9069b3770f5cdc502e96959c866d2f30fbf5e8b6b`; a byte-identical copy with the same basename was analyzed at `/var/tmp/kaidoku-ex7-r12/copy/libjq.so.1.0.4` (`evidence/input-file.txt`, `input-sha256.txt`). All three successful CLI calls used the exact command shape in `evidence/calls.txt` and returned `ev_15ef9534ada2b94641eece558130ab0e1bddc2129170843fba9b8f96c1047be5` (`function-base-1.json`, `function-base-2.json`, `function-copy.json`). The subject's `local_path` changes between the original and copy; subject digest, REA provider Ghidra 12.1.4, analysis-profile digest `769518a8e9b57f953dd241adbb63672f0f486bb3d66359b9deef7c5e088ca7aa`, and the exact semantic projection are equal (`recompute-output.json`). Each call exited 0; stdout sizes were 6,212,425; 6,212,425; and 6,212,446 bytes, with empty stderr (`calls.txt`).

The package implementation constructs `analyze_function` Evidence with `parameters` and the validated dossier (`FunctionAnalysisEvidence.js:19-33`); this CLI passes only `{procedure:"jq_next"}` as the operation parameters (`coreBinaryCommands.js:218-245`). On the returned records, the normalized dossier has no `path`/`filename` keys and `locations` is empty. The independently recomputed semantic projections are exactly equal across the three calls; the checker found no path/filename fields anywhere in those projections. The actual alternate-path observation therefore shows path stability for this exact operation, target byte identity, procedure, provider, and release—not a universal property of `ev_` IDs.

REA 6.7.0 source defines the hashed semantic projection at `dist/domain/evidence.js:159-183`: it retains subject digest, format and architecture but drops subject `name` and `local_path`, then includes provider, analysis profile, predicate type, operation, parameters, raw and normalized results, confidence, authority, environment, limitations, relationship coverage, locations and evidence links. `dist/domain/canonicalDigest.js:8-25,60-76` streams SHA-256 over compact canonical JSON with sorted object keys. The independent script applied that projection to each complete returned Evidence envelope and called the package's digest implementation; all three recomputed IDs match the emitted IDs, and a display-only subject name/path mutation preserves the ID (`recompute-ids.mjs`, `recompute-output.json`). Package/source SHA-256 identities are recorded in `source-and-input-sha256.txt`.

## Seat verdicts and coverage measurement

- **VERIFIED — same-path repeat:** both `/usr/lib/libjq.so.1.0.4` calls returned the same Evidence ID; full fresh envelopes are `evidence/function-base-1.json` and `function-base-2.json`.
- **VERIFIED — alternate-path behavior:** the same-byte, same-basename copy at a distinct path returned that same ID; hashes and exact paths are in `evidence/input-sha256.txt` and `recompute-output.json`.
- **REPRODUCED — ID formula for this projection:** all three IDs independently recompute, the semantic projection equality checks pass, and the measured projection contains no path/filename fields (`evidence/recompute-output.json`).
- **VERIFIED — Command A baseline:** I re-ran the `SCORECARD.md:88-124` recipe against immutable Git objects. At `0436f49`, exact output is `{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":90,"mapped":90,"missing":[],"revision":"0436f49","rule_blocks":16}`; at `5ee13b3`, exact output is `{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":90,"mapped":90,"missing":[],"revision":"5ee13b3","rule_blocks":16}` (`evidence/command-a-0436f49.json`, `command-a-5ee13b3.json`).
- **UNVERIFIABLE — post-integration 91/91:** this seat is authorized to deliver a draft only and did not land the corpus file or map token; Command A after integration must be measured by the integrator. The measured pre-integration count remains 90 files, 90 mapped, `missing:[]`, `dangling:[]`.

## Limits

Only `analyze_function` in REA 6.7.0 / Ghidra 12.1.4, `/usr/lib/libjq.so.1.0.4` at one byte identity, `jq_next`, two calls at the original path, and one same-byte copy at a different path were tested. This does not establish behavior for other verbs, parameters, inputs, providers, formats, failures, package versions, or MCP evidence. The calls were static analyses; the ELF was not executed. The bounded named Unknown is the frozen residual in `.ufo/waves/arc3-loop1-round12/claims-frozen.md:21-23`.
