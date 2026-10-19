<!-- C1 corpus-entry draft for parent integration only. Proposed destination: corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md. Proposed token: `2026-10-19-arc3-r12-go-evidence-id-domain`, appended to the Go binary row in corpus/README.md. No corpus or map edit was made by this seat. -->

# Draft — `inspect_go_binary` Evidence-ID derivation and path-sensitive identity in REA 6.7.0

source: `.ufo/waves/arc3-loop1-round12/claims/c1/EX-2/evidence/{base1.json,base2.json,copy-a.json,copy-b.json,identity.txt,probe-calls.txt,recompute-ids.py,recompute-ids.txt,command-A-before.txt}`; target/package and source-file hashes are recorded in `identity.txt`.

verified-at: 2026-10-19

recheck: use the existing REA 6.7.0 cache path and `/usr/bin/docker` only after confirming its SHA-256 matches `identity.txt`; make two byte-identical copies under distinct `/var/tmp` directories (same basename), set `TMPDIR` to a directory under `/var/tmp`, run the four exact calls recorded in `evidence/probe-calls.txt`, then run `python3 .ufo/waves/arc3-loop1-round12/claims/c1/EX-2/evidence/recompute-ids.py`. Do not use `/tmp` for scratch.

## Result

This is the frozen C1 candidate “a fourth verb family's `ev_` id domain” (`.ufo/waves/arc3-loop1-round12/claims-frozen.md:18-25`). On the host's cached `rea-agents@6.7.0`, `inspect_go_binary` emits an ID equal to `ev_` plus SHA-256 of its canonical semantic Evidence projection, and this measured operation is path-sensitive. The conclusion is bounded to this operation, package version, one ELF byte identity, and the call shape tested. It does not state a universal REA ID rule.

## First-hand observations and re-derivation

The target was `/usr/bin/docker`, 29,327,600 bytes, SHA-256 `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9`; `file` identified it as ELF64 x86-64 (`evidence/identity.txt`). Two same-path calls returned `ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd`. Their `data` objects compare equal; the full JSON envelope files differ only in non-Evidence `meta.duration` (34ms and 36ms). Two same-basename copies have the same measured size and SHA-256 yet returned distinct IDs: copy-a `ev_b9b1f94c1518763423cfbaba4479ffc25641927e4908db0802b9f4851731fef0`, copy-b `ev_62417bbb12d061fd5d25e90aac7b7ce8995df2e6987dd0c5a9a9d9b33e9490f3` (`evidence/probe-calls.txt`; full envelopes are retained).

The independent script in `evidence/recompute-ids.py` rebuilt the projection and compact canonical JSON in Python, SHA-256 hashed the UTF-8 bytes, and matched all four reported IDs (`evidence/recompute-ids.txt`). It also replaced only these path-bearing projection fields in the base record — `parameters.path`, `normalized_result.artifact.path`, and `locations[0].path` — with copy-a/copy-b values; each recomputed ID exactly matched the corresponding returned copy ID. After normalizing those three values to one sentinel, the projections are equal across the three file paths. Mutating only the top-level subject display fields `name` and `local_path` leaves the recomputed base ID unchanged.

The package source supports that narrow mechanism: `dist/domain/evidence.js:159-183` projects subject digest/format/architecture, then includes `parameters`, `normalized_result`, and `locations`, while excluding the subject's display `name`/`local_path`; it defines `ev_` + canonical SHA-256. `dist/domain/canonicalDigest.js:8-25,60-76` emits canonical JSON with sorted object keys and hashes it with SHA-256. `dist/application/go/GoBinaryService.js:54-76` constructs Evidence with the caller path in parameters, the provider's artifact result, and an `artifact-path` location. The source package version and file hashes are pinned in `evidence/identity.txt`; the observed field-level changes and independent recomputation, not source inspection alone, establish the measured result.

The fresh CLI RESULT reports embedded Go version `go1.26.5-X:nodwarf5` and module path `github.com/docker/cli/cmd/docker`. Those are observed embedded metadata, not proof of compiler identity, dependencies, source identity, or runtime behavior. The binary was not executed (`base1.json`).

## Verdicts and bounds

- **REPRODUCED** — same-path `inspect_go_binary` calls returned the same ID and equal Evidence data; outer `meta.duration` is not part of the Evidence record.
- **VERIFIED** — two byte-identical, same-basename copies at different paths returned different IDs. The three measured path fields in the semantic projection account for the observed delta; the top-level subject display path does not.
- **VERIFIED** — independent canonical projection recomputation matched all four full Evidence records and controlled path-field substitutions reproduced both copy IDs.
- **UNVERIFIABLE / still open** — whether another operation whose semantic projection carries no path-bearing fields remains path-stable; no such operation was tested. Other REA verb families, package versions, artifact formats, error envelopes, and alternate request/environment combinations are also untested.
- **VERIFIED baseline, post-integration UNVERIFIABLE** — Command A at work revision `5ee13b3` and recorded HEAD `0436f4940283072db08e73c0117195847c50d31d` independently returned 90 knowledge files, 90 mapped, `missing:[]`, `dangling:[]`, 16 citation-resolved rules / 16 rule blocks (`evidence/command-A-before.txt`; recipe `SCORECARD.md:88-124`). This draft does not edit the corpus or map. The expected 91/91 result must be re-measured by the integrator after both the knowledge file and map token land together.

The prior EVM, Rust, and `inspect_artifact` drafts explicitly bound their results to their own verb families (`corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:9,26`; `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:11,28`; `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:19,23`). Those entries identify the remaining coverage need; this draft's Go results are independently probed here. Proposed map destination is the Go binary row (`corpus/README.md:62`).

## Scope and limitations

Four successful static CLI calls with REA 6.7.0 used one 29,327,600-byte ELF: two calls at `/usr/bin/docker` and two same-byte copies at different absolute paths. This establishes behavior only for `inspect_go_binary` on that input and request shape. It does not characterize other Go binaries, PE/Mach-O inputs, other tool versions, failure records, path aliases, relative-path forms, or every Evidence field combination. No target execution, network request, compiler-authenticity assertion, or dependency-absence claim is made. This remains a draft until the proposed knowledge entry and map token are co-landed and Command A is rerun.
