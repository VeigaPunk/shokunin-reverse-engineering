<!-- DRAFT for parent integration only. Proposed destination: corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md. Proposed coverage-map token: `2026-10-19-arc3-r12-go-evidence-id-domain`, appended to the Go binary row in corpus/README.md. This seat did not edit corpus/ or the coverage map. -->

# Draft — `inspect_go_binary` Evidence-ID formula and path-sensitive identity in REA 6.7.0

source: `.ufo/waves/arc3-loop1-round12/claims/c1/EX-4/evidence/{identity.txt,calls.txt,probes/{base1,base2,copyA,copyB}.json,recompute-ids.py,recompute-results.json,command-a.py,command-a-head.json,command-a-work.json}`.
verified-at: 2026-10-19
recheck: create two byte-identical copies of `/usr/bin/docker` at the paths recorded in `evidence/calls.txt`, set `TMPDIR` to a directory under `/var/tmp`, and run the four recorded `inspect-go-binary` commands with the cached REA CLI. Then run `python3 .ufo/waves/arc3-loop1-round12/claims/c1/EX-4/evidence/recompute-ids.py`. The copied inputs, full JSON envelopes, output, and package-source hashes are retained with this draft; `/tmp` was not used.

## Result

This draft closes one bounded C1 Unknown: the `ev_` Evidence-ID domain for a fourth verb family, `inspect_go_binary`, in cached `rea-agents@6.7.0`. The inspected file was `/usr/bin/docker`, a 29,327,600-byte ELF; its SHA-256 and the byte-identical copies' hashes are recorded in `evidence/identity.txt`. This does not assert a universal formula for other verbs, releases, artifact identities, or failure envelopes.

The four successful CLI envelopes report these IDs:

- `VERIFIED` — two calls on `/usr/bin/docker` returned `ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd`.
- `VERIFIED` — copies at different paths but with the same basename and the same SHA-256 returned `ev_0e2a7da842265a964fa0f9976decaaddc4fbb123e5849dc41dff3aa6f7a9475a` and `ev_0997c5ff17aa581e8f5f09feb71659fef753e44a57fe602f08a27aab0c6ad1e2`.
- `REPRODUCED` — the independent Python recomputation exactly matches all four returned IDs; its eight checks pass in `evidence/recompute-results.json`. Masking the three changed path fields makes all four semantic projections equal. Changing only `subject.name` and `subject.local_path` preserves the base ID, while changing only the three path-bearing semantic fields reproduces copy A's ID.

## Derived identity rule

The pinned REA package source defines an `ev_` ID as SHA-256 over compact canonical JSON for a semantic Evidence projection. In `dist/domain/evidence.js:159-183`, the projection includes `subject` reduced to `{digest, format, architecture}` and the fields `provider`, `analysis_profile`, `predicate_type`, `operation`, `parameters`, `raw_result`, `normalized_result`, `confidence`, `authority`, `environment`, `limitations`, `relationship_coverage`, `locations`, and `evidence_links`; it excludes the ID and subject display-only `name`/`local_path`. `dist/domain/canonicalDigest.js:8-25,62-76` implements canonical JSON hashing with sorted object keys and SHA-256. Package and source digests are in `evidence/identity.txt`.

For this verb, `dist/application/go/GoBinaryService.js:54-76` passes the selected path through `parameters: input.data`, the inspected report as `result`, and an `artifact-path` location. The report's artifact path is constructed in `dist/go/GoBinaryProvider.js:157-165`. Therefore `parameters.path`, `normalized_result.artifact.path`, and `locations[0].path` are in the semantic projection and changed between probes; these three substitutions alone reproduce the observed copy A ID. This is a measured path-sensitive case, not a claim that all Go inspections or all Evidence IDs are path-sensitive.

The inspections are static. No target execution, network access, or native analysis session is claimed. The metadata is observed file content, not proof of compiler identity, dependency authenticity, or runtime behavior.

## Coverage measurement and limits

`REPRODUCED` — I ran the Command A calculation from `SCORECARD.md:88-124` against immutable Git objects at source revisions `0436f4940283072db08e73c0117195847c50d31d` and `5ee13b358d0a1112d31808b9bae3d8ddd1b46875`. Both fresh outputs report `knowledge_files:90`, `mapped:90`, `missing:[]`, and `dangling:[]` (`evidence/command-a-head.json` and `command-a-work.json`). The script is retained at `evidence/command-a.py`.

`UNVERIFIABLE` — the post-integration `91/91` result. This deliverable is a draft and does not change `corpus/knowledge/` or `corpus/README.md`; the proposed entry and map token must be integrated together and Command A rerun at that revision. No claim of a landed corpus count is made.

Only one byte identity, one Go operation, one cached REA release, one same-path repeat, and two alternate paths were tested. Other Go binaries, package versions, error outcomes, all Evidence field variations, and other verb families remain untested. The returned `module.main` is null, so its own limitations leave dependency coverage unknown; an empty dependencies list does not prove there are no dependencies.
