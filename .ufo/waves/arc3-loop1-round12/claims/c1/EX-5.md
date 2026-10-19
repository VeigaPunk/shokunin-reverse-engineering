<!-- DRAFT for parent integration only. Proposed destination: corpus/knowledge/2026-10-19-arc3-r12-inspect-go-binary-evidence-id-domain.md. Proposed coverage-map token: `2026-10-19-arc3-r12-inspect-go-binary-evidence-id-domain`, appended to the Evidence model row in corpus/README.md. This seat did not modify corpus/ or its map. -->

# Draft — `inspect_go_binary` Evidence-ID domain in REA 6.7.0

source: `.ufo/waves/arc3-loop1-round12/claims/c1/EX-5/evidence/{base-1.json,base-2.json,copy-same-name.json,copy-other-name.json,recompute-ids.mjs,recompute-ids-output.json,calls.txt,input-hashes.txt,input-sizes.txt,identity.txt,source-hashes.txt,command-A-head.json}`.

verified-at: 2026-10-19

recheck: from the lane root, recreate byte-identical copies of `/usr/bin/docker` at `/var/tmp/kaidoku-arc3-r12-ex5/same-name/docker` and `/var/tmp/kaidoku-arc3-r12-ex5/other-name/docker-copy`; check `sha256sum`/`stat` against `evidence/input-hashes.txt` and `evidence/input-sizes.txt`; run the four invocations in `evidence/calls.txt` with `TMPDIR=/var/tmp/kaidoku-arc3-r12-ex5`; then run `node .ufo/waves/arc3-loop1-round12/claims/c1/EX-5/evidence/recompute-ids.mjs`. The recheck uses the host's cached `rea-agents@6.7.0` and disk-backed scratch under `/var/tmp`; no target execution is performed.

## Unknown closed

This draft addresses the frozen C1 candidate for a fourth `ev_` verb family (`.ufo/waves/arc3-loop1-round12/claims-frozen.md:18-25`): the emitted Evidence-ID formula and path behavior of `inspect_go_binary`. The observed identity is operation-specific; this does not characterize every REA verb or package release.

## Result

For the captured `inspect_go_binary` result, the ID is `ev_` plus the SHA-256 digest of the canonical JSON semantic projection defined by the cached package's `dist/domain/evidence.js:159-183`. That projection keeps only `subject.digest`, `subject.format`, and `subject.architecture` from the subject, then includes the semantic Evidence fields (`provider`, `analysis_profile`, `predicate_type`, `operation`, `parameters`, raw and normalized results, confidence, authority, environment, limitations, relationship coverage, locations, and evidence links). `dist/domain/canonicalDigest.js:8-25,58-76` supplies the SHA-256 and canonical object-key ordering. Package version and pinned source-file hashes are recorded in `evidence/identity.txt` and `evidence/source-hashes.txt`.

`inspect_go_binary` is path-sensitive for the measured byte identity and call shape: its service supplies the selected path in `parameters.path` and an `artifact-path` location (`dist/application/go/GoBinaryService.js:54-77`), while the provider returns it as `normalized_result.artifact.path` (`dist/go/GoBinaryProvider.js:157-165`). Those fields are all in the semantic projection. Display-only subject `name` and `local_path` are excluded; path strings retained in semantic fields are not.

## First-hand checks

- `VERIFIED` — cached package manifest says `rea-agents` version `6.7.0` (`evidence/identity.txt`; `package.json:4`). SHA-256 identities for the manifest and the four inspected implementation files are in `evidence/source-hashes.txt`.
- `REPRODUCED` — two calls on `/usr/bin/docker` returned `ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd` both times. Full `ok:true` envelopes: `evidence/base-1.json` and `evidence/base-2.json`.
- `REPRODUCED` — `/usr/bin/docker` and two copies at distinct paths all measured SHA-256 `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9` and size `29,327,600` bytes (`evidence/input-hashes.txt`, `evidence/input-sizes.txt`). The same-basename copy returned `ev_951d9ab14d1a8ff67912061beca2c7a2ebdd964cf80b2671678391053d43b62f`; the differently named copy returned `ev_5cc62fc711609ea88b059abcbfb415e08d7591fcda5b9540178ed8732674b09b` (`evidence/copy-same-name.json`, `evidence/copy-other-name.json`). Same bytes and same basename at a different path are sufficient to show this measured result is path-sensitive.
- `REPRODUCED` — independent recomputation matched all four reported IDs. Mutating only the base result's display-subject fields preserved the ID; replacing only the three path-bearing semantic fields (`parameters.path`, `normalized_result.artifact.path`, and the `artifact-path` location) reproduced each copied-path ID. Exact output: `evidence/recompute-ids-output.json`; recomputation implementation: `evidence/recompute-ids.mjs`.
- `VERIFIED` — the CLI describes this operation as inspecting embedded Go build information “without target execution” (`dist/cli/goCommands.js:8-18`); provider implementation reads and parses the selected stable artifact (`dist/go/GoBinaryProvider.js:122-179`). No target execution is claimed here.
- `VERIFIED` — source-derived Command A at frozen `HEAD` `0436f4940283072db08e73c0117195847c50d31d` returned `knowledge_files:90`, `mapped:90`, `missing:[]`, `dangling:[]`, `citation_resolved_rules:16`, and `rule_blocks:16`. Exact JSON: `evidence/command-A-head.json`; recipe: `SCORECARD.md:88-124`.
- `UNVERIFIABLE` — post-integration `91/91` Command A result. This is a draft only; the corpus entry and matching map token were not landed by this seat. Parent integration must co-land both and rerun Command A against the resulting revision.

## Scope and limits

The live result covers REA 6.7.0, one ELF byte identity (`/usr/bin/docker`), two same-path calls, and two byte-identical copies at distinct paths. The copied-path result is path-sensitive for `inspect_go_binary`; it does not establish a universal `ev_` rule, behavior of other operations, other versions, error envelopes, or MCP-session Evidence. The other frozen C1 candidate about a verb with no path-bearing semantic fields remains open: this operation is specifically not such a case. Embedded Go build metadata is observed file content, not proof of compiler identity or runtime behavior; the envelope also states that dependency coverage is unknown where no main-module record was decoded.

Current Command A evidence is a frozen-HEAD baseline only; the proposed new knowledge filename and map token are not yet in the corpus. Proposed token location: `corpus/README.md:41`.
