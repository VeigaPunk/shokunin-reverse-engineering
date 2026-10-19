<!-- DRAFT for parent integration only. Proposed destination: corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md. Proposed coverage-map token: `2026-10-19-arc3-r12-go-evidence-id-domain`, appended to the Evidence model row in corpus/README.md. No corpus or map edit was made by this seat. -->

# Draft — `inspect_go_binary` Evidence-ID formula in REA 6.7.0; path-sensitive through semantic path fields

source: `.ufo/waves/arc3-loop1-round12/claims/c1/CR-4/evidence/{base-1.json,base-2.json,copy-a.json,copy-b.json,identity.txt,calls.txt,recompute-ids.py,recompute-results.txt,package-source-hashes.txt,command-a-5ee13b358d0a1112d31808b9bae3d8ddd1b46875.json,command-a-0436f4940283072db08e73c0117195847c50d31d.json,command-a-context.txt}`; the exact cached package source identities and hashes are in `package-source-hashes.txt`.

verified-at: 2026-10-19

recheck: use the four exact `inspect-go-binary` CLI calls in `evidence/calls.txt` with `TMPDIR=/var/tmp/kaidoku-cr4-r12`; recreate the two copies from `/usr/bin/docker` first. Full envelopes are retained in `evidence/{base-1.json,base-2.json,copy-a.json,copy-b.json}`. Run `python3 .ufo/waves/arc3-loop1-round12/claims/c1/CR-4/evidence/recompute-ids.py .ufo/waves/arc3-loop1-round12/claims/c1/CR-4/evidence` to independently recompute the IDs and controlled projection mutations. Do not execute the inspected image.

## Result

This closes one additional operation-specific `ev_` Evidence-ID Unknown selected under the frozen C1 “fourth verb family” candidate (`.ufo/waves/arc3-loop1-round12/claims-frozen.md:18-24`): the formula for `inspect_go_binary` on the host’s cached `rea-agents@6.7.0`. It does not establish a universal rule for other REA operations, releases, or inputs.

For these calls, the reported ID is `ev_` plus the lowercase SHA-256 of the canonical JSON semantic projection. The inspected package’s `dist/domain/evidence.js:159-183` defines that projection: it retains `subject.digest`, `subject.format`, and `subject.architecture`, then provider, analysis profile, predicate, operation, parameters, raw and normalized results, confidence, authority, environment, limitations, relationship coverage, locations, and evidence links. It excludes the ID itself and the subject display fields `name` and `local_path`. `dist/domain/canonicalDigest.js:8-25,60-76` emits compact JSON, sorts object keys, and hashes it with SHA-256.

For `inspect_go_binary`, `dist/application/go/GoBinaryService.js:54-77` puts the selected path in `parameters.path`, `normalized_result.artifact.path`, and an `artifact-path` location. Consequently, those semantic fields make the ID path-sensitive in this controlled same-byte sample; the subject’s display path alone does not.

## First-hand observations and verdicts

- `VERIFIED` — four successful `inspect-go-binary` calls used the pinned cached REA 6.7.0 CLI (`evidence/calls.txt`; package version and source hashes: `evidence/package-source-hashes.txt`). The inspected `/usr/bin/docker` and both copies are byte-identical: SHA-256 `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9`, size 29,327,600 bytes (`evidence/identity.txt:1-6`).
- `VERIFIED` — two calls on `/usr/bin/docker` returned the same ID, `ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd`; see complete envelopes `evidence/base-1.json` and `evidence/base-2.json`, and compact evidence at `evidence/recompute-results.txt:1-2`.
- `VERIFIED` — the same bytes and basename `docker` at `/var/tmp/kaidoku-cr4-r12/copy-a/docker` returned `ev_01c99c5db77c3546a879e7cf570f9d8b0f79950f174b48b2b9d1b87d0c08ff6d`. Same bytes with a different basename at `/var/tmp/kaidoku-cr4-r12/copy-b/docker-copy` returned `ev_4a5922f1f6de19f0d2156e6c22239ae5ff35a6fbf52fd0040dddbdc4dc969e67`. Full envelopes: `evidence/copy-a.json`, `evidence/copy-b.json`; hashes and sizes: `evidence/identity.txt:1-6`.
- `REPRODUCED` — the independent `evidence/recompute-ids.py` matches all four full-envelope IDs (`evidence/recompute-results.txt:1-4`). The base-to-copy-A semantic projection differs only at `locations[0].path`, `normalized_result.artifact.path`, and `parameters.path` (`recompute-results.txt:5`). Changing only the subject’s `name` and `local_path` leaves the base ID unchanged (`:6`); substituting only those three semantic path fields with copy A’s path reproduces copy A’s exact ID (`:7`). This supports the path-field explanation for this sample, not a universal property of all projections.
- `VERIFIED` — the result reports Go version `go1.26.5-X:nodwarf5` and module `github.com/docker/cli/cmd/docker` for this artifact (raw envelopes, e.g. `evidence/base-1.json`). `dist/go/GoBinaryProvider.js:122,139-173` documents and implements stable in-process file inspection; this probe does not execute Docker or establish runtime behavior.
- `VERIFIED` — Command A, re-run from immutable source revisions because no R12 `result.json` exists, returned 90 knowledge files, 90 mapped, `missing:[]`, and `dangling:[]` at both the work revision `5ee13b358d0a1112d31808b9bae3d8ddd1b46875` and records revision `0436f4940283072db08e73c0117195847c50d31d`; raw outputs are `evidence/command-a-5ee13b358d0a1112d31808b9bae3d8ddd1b46875.json` and `evidence/command-a-0436f4940283072db08e73c0117195847c50d31d.json`.
- `UNVERIFIABLE` — post-integration Command A. This seat is restricted to its round artifact directory, so neither the proposed corpus entry nor the map token is landed. Adding exactly one knowledge file and its token predicts 91/91 with no missing or dangling map entries, but that after-state must be measured by the integrating seat.

## Scope and limitations

Only REA 6.7.0, `inspect_go_binary`, one ELF byte identity, two same-path calls, and two copied paths were measured. The tests establish same-path repeat stability and path sensitivity for the three semantic path fields in this result. They do not establish behavior for other formats, operations, REA releases, missing metadata, failures, or all Evidence field variations. The analyzer reads the selected file; the target was not executed and no network access was used. Go build metadata is an observed artifact record, not compiler authenticity, dependency authenticity, or runtime evidence.

## Proposed map change

Append `2026-10-19-arc3-r12-go-evidence-id-domain` to the Evidence model row in `corpus/README.md` (the row that indexes the existing operation-specific `ev_` formula entries). Keep this as a proposed token until the corpus entry is integrated and Command A is re-run at the landing revision.
