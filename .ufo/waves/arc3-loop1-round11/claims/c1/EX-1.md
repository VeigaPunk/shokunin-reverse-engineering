<!-- DRAFT corpus entry for parent integration. Proposed destination: corpus/knowledge/2026-10-19-arc3-r11-go-evidence-id-domain.md. Proposed coverage token: `2026-10-19-arc3-r11-go-evidence-id-domain`, appended to the Go-binary row in `corpus/README.md`'s Coverage map (current row at :62). The corpus file and map token must co-land. This seat changed neither tracked file. -->

# `inspect_go_binary` Evidence-ID domain in REA 6.7.0 — semantic hash, path-sensitive through request fields

verified-at: 2026-10-19

source: `.ufo/waves/arc3-loop1-round11/claims/c1/EX-1/evidence/` (`target-identity.txt`; `probe-{base1,base2,copy}.json`; `recompute-ids.mjs`; `id-recomputation.json`; `rea-source-identity.txt`). Package source paths and SHA-256 identities are captured in `rea-source-identity.txt`.

recheck: from this repository root, use the pinned cached CLI path recorded here and set `TMPDIR` to a disk-backed directory under `/var/tmp`:

```sh
REA=/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs
SCRATCH=/var/tmp/kaidoku-arc3-r11-ex1
mkdir -p "$SCRATCH"
cp /usr/bin/docker "$SCRATCH/docker-copy"
TMPDIR="$SCRATCH" node "$REA" inspect-go-binary /usr/bin/docker --format json --full-output
TMPDIR="$SCRATCH" node "$REA" inspect-go-binary /usr/bin/docker --format json --full-output
TMPDIR="$SCRATCH" node "$REA" inspect-go-binary "$SCRATCH/docker-copy" --format json --full-output
node .ufo/waves/arc3-loop1-round11/claims/c1/EX-1/evidence/recompute-ids.mjs
```

The exact full envelopes are retained in `EX-1/evidence/probe-{base1,base2,copy}.json`; the re-computation is a separate implementation of the package's projection and canonical hash. This is a bounded characterization of `inspect_go_binary`, not a universal REA Evidence-ID rule.

## Finding and first-hand results

The frozen C1 candidate is the `ev_` ID domain for a third verb family (`.ufo/waves/arc3-loop1-round11/claims-frozen.md:19-20`). This draft exercises that candidate with `inspect_go_binary` on the live local ELF `/usr/bin/docker`, SHA-256 `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9`, 29,327,600 bytes. A copy at `/var/tmp/kaidoku-arc3-r11-ex1/docker-copy` has the same size and digest (`EX-1/evidence/target-identity.txt:1-4`). The calls inspected the bytes; they did not execute Docker.

- **REPRODUCED — same-path repeat.** Two fresh calls to `inspect-go-binary /usr/bin/docker --format json --full-output` returned `ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd` (`EX-1/evidence/probe-base1.json:1`, `EX-1/evidence/probe-base2.json:1`). Their semantic projections compare equal (`EX-1/evidence/id-recomputation.json:20`), and the separate recomputation matches both reported IDs (`EX-1/evidence/id-recomputation.json:4-12`).
- **VERIFIED — path affects the ID for this operation.** The byte-identical copy returned `ev_fe7068208c1c6430e235b71a4aa52a42796ab4b6f391e533a62228aaa21d7385` (`EX-1/evidence/probe-copy.json:1`), also matched by recomputation (`EX-1/evidence/id-recomputation.json:14-18`). The copies have identical SHA-256 and size; the result, source and package output otherwise describe the same Go metadata.
- **REPRODUCED — which fields carry the path.** Installed REA 6.7.0 source constructs the record for `inspect_go_binary` with the selected path in `parameters` and artifact-path `locations` (`dist/application/go/GoBinaryService.js:54-77`; source digest in `EX-1/evidence/rea-source-identity.txt:4`). These `dist/...` paths are relative to the installed package root captured in that identity file. `dist/domain/evidence.js:159-183` defines the hashed semantic projection: it includes `subject.digest`/format/architecture, provider, operation, parameters, raw and normalized results, confidence, authority, environment, limitations, relationship coverage, locations, and evidence links; it excludes display-only `subject.name` and `subject.local_path`. The projection retains `parameters.path`, `normalized_result.artifact.path`, and `locations[0].path`. `dist/domain/canonicalDigest.js:8-25,27-76` hashes canonical JSON with SHA-256 and sorted object keys (the package file hashes are in `EX-1/evidence/rea-source-identity.txt:5-6`).
- **REPRODUCED — field controls.** Changing only the display subject name/path on the base record recomputes to the base ID; substituting only the three semantic path fields recomputes to the copy ID (`EX-1/evidence/id-recomputation.json:21-28`). The implementation and its checks are retained in `EX-1/evidence/recompute-ids.mjs` and exit successfully. Thus this operation's ID is `ev_` + SHA-256 of the package's canonical semantic Evidence projection; its path sensitivity here comes from semantic path fields, not the display subject fields.
- **VERIFIED — observed result scope.** The returned record identifies provider `go-build-info` v1 and reports inline build metadata `go1.26.5-X:nodwarf5`, module path `github.com/docker/cli/cmd/docker`, and `complete:true` (`EX-1/evidence/probe-base1.json:1`). These are file-content observations only; the record does not authenticate compiler identity, dependency authenticity, or runtime behavior. The report also says dependency coverage is unknown because no main-module record was decoded. The reader implementation describes a stable in-process inspection without subprocesses, temporary files, or a Go installation (`dist/go/GoBinaryProvider.js:122-173`).

## Command A coverage baseline and disposition

I reran the SCORECARD recipe (`SCORECARD.md:88-124`) against the two named source commits. At the prior round's work commit `9c1d1fef5595b55d65764626249f164e6816473a`, exact output:

```json
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":89,"mapped":89,"missing":[],"revision":"9c1d1fef5595b55d65764626249f164e6816473a","rule_blocks":16}
```

At the current recorded HEAD `e746ca79e2dbb3cb41436d612f448e81d2c6e585`, exact output:

```json
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":89,"mapped":89,"missing":[],"revision":"e746ca79e2dbb3cb41436d612f448e81d2c6e585","rule_blocks":16}
```

**UNVERIFIABLE — post-integration count.** This seat is limited to its own wave artifact directory, so the proposed corpus entry and Go-row token remain drafts. The `89 → 90`, `mapped:90`, `missing:[]`, `dangling:[]` result is an integration expectation, not a measured result. Parent integration must co-land the proposed file and token, then rerun Command A at the resulting work commit before claiming C1 closure.

## Scope and limitations

The evidence covers one successful static `inspect_go_binary` operation in cached REA 6.7.0 on one ELF, repeated at the same path and once at a byte-identical alternate path. It establishes this operation's observed ID formula and path sensitivity for these calls, not failure records, other fields/shapes, other REA versions, or other verb families. The reported Go metadata is not execution evidence, compiler authentication, dependency completeness, or proof of runtime behavior. No network or target execution was used. The named corpus entry and coverage-map token are not landed.
