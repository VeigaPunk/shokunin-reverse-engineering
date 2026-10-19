# EX-1 — C1 coverage: `analyze_function` Evidence-ID Unknown

## Deliverable

Corpus-entry draft: `claims/c1/EX-1/corpus-entry-draft.md`. Evidence bundle: `claims/c1/EX-1/evidence/`. Proposed destination is `corpus/knowledge/2026-10-19-arc3-r12-analyze-function-evidence-id-domain.md`; proposed map token is `2026-10-19-arc3-r12-analyze-function-evidence-id-domain` on the Evidence model row at `corpus/README.md:41`. Per the wave's write fence, no corpus, README, SKILL, gate, LOG, PROVINCE, or other tracked file was edited.

## Re-derived findings and verdicts

- **VERIFIED — package formula and projection:** `rea-agents@6.7.0` source at `dist/domain/evidence.js:159-183` projects `subject` to `{digest, format, architecture}`, then hashes its other semantic fields; `dist/domain/canonicalDigest.js:8-25,27-83` supplies SHA-256 over compact canonical JSON. Package source identities: `claims/c1/EX-1/evidence/source-hashes.txt`; source excerpts: `evidence/source-contract.txt`.
- **REPRODUCED — path stability for this `analyze_function` case:** two calls to the primary fixture and one to an identical alternate-path copy all returned `ev_69e0476bafd383f7160bc68db2c0d932b242afe9c84a842be5b400967b4d1499`. An independent recomputation matched all three in the initial run and the fresh end-to-end rerun; projections were byte-identical, path-key and exact target-path-string scans returned `[]`, and display-path-only mutation preserved the ID. Initial audit: `evidence/recompute-path-audit.txt`; rerun script, envelopes, and audit: `evidence/recheck.sh`, `evidence/rerun/`, and `evidence/recompute-rerun-path-audit.txt`; exact calls/exits: `evidence/calls.txt`.
- **VERIFIED — measured baseline:** Command A at HEAD `0436f4940283072db08e73c0117195847c50d31d` returned `knowledge_files=90`, `mapped=90`, `missing=[]`, `dangling=[]`, `rule_blocks=16`, `citation_resolved_rules=16`; exact initial and repeated JSON: `evidence/command-A-before.txt` and `evidence/command-A-recheck.txt`, with revision in `evidence/revision.txt`.
- **UNVERIFIABLE — post-integration map count:** `91/91` is the projected count if the parent lands both the corpus entry and token, not a measurement by this seat. This artifact does not modify the shared corpus/map, so command A remains 90/90 at the measured HEAD.

## Measurement details

The target is a GCC-compiled synthetic x86-64 ELF, not an application claim: its source and binary copies are retained at `evidence/fixtures/`; both measured copies hash to `31b145a39175770833faf3b01fb6320060a9f4f9329218f9e711e0df93c28c64`. The CLI source `dist/cli/coreBinaryCommands.js:218-245` passes only `{procedure:"probe_target"}` as `analyze_function` parameters; application composition is at `dist/application/FunctionAnalysisEvidence.js:8-33`. The target was statically analyzed and never executed. Scratch and Ghidra TMPDIR were under `/var/tmp`, not `/tmp`.

The independent check is `python3 claims/c1/EX-1/evidence/recompute.py` for the saved original envelopes, or pass the `evidence/rerun/` directory to verify fresh calls; both runs audit path-key fields and exact target-path strings. The corpus draft contains the bounded result, recheck recipe, source/version scope, and explicit no-universal-claim limitation.
