<!-- DRAFT for parent integration only. Proposed destination: corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md. Proposed coverage-map token: `2026-10-19-arc3-r10-rust-evidence-id-domain`, appended to the Rust binary row in corpus/README.md. No corpus or map edit was made by this seat. -->

# Draft — `inspect_rust_binary` Evidence-ID formula in REA 6.7.0

source: `.ufo/waves/arc3-loop1-round10/claims/c1/EX-4/evidence/{probe-base1.json,probe-base2.json,probe-copyA.json,probe-copyB.json,id-recompute.json,recompute-ids.mjs,identity.txt,command-A-before.json,rederive-commands.txt}`; REA package-source identity and input hash are recorded in `identity.txt`.

recheck: from the lane root, use the cached REA 6.7.0 command shown in `evidence/rederive-commands.txt`; then run `node .ufo/waves/arc3-loop1-round10/claims/c1/EX-4/evidence/recompute-ids.mjs`. The latter recomputes each recorded envelope's semantic projection ID, mutates only excluded display fields, and substitutes only the path-bearing fields to test the copied-path result. The `rustc` inspection is read-only; it does not execute the target.

## Result

The C1 Unknown is the `ev_` Evidence-ID derivation for a second verb family, `inspect_rust_binary` (the frozen candidate is named at `.ufo/waves/arc3-loop1-round10/claims-frozen.md:18-25`; the prior EVM-specific draft limits its finding to `inspect-evm-interface` and says other verbs are outside its claim at `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:9,26`). This draft closes the formula for this operation on the host's cached `rea-agents@6.7.0`; it does not claim that every REA operation or package release has the same domain.

The installed package source root is `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents` (package version and file hashes: `evidence/identity.txt`). Its `dist/domain/evidence.js:159-183` defines `computeEvidenceId` as `ev_` plus the SHA-256 digest of `semanticProjection(evidence)`. The projection omits the Evidence ID itself and subject display fields (`name`, `local_path`); it includes subject digest, format and architecture plus provider, analysis profile, predicate, operation, parameters, raw and normalized results, confidence, authority, environment, limitations, relationship coverage, locations and evidence links. `dist/domain/canonicalDigest.js:8-25,60-76` hashes compact canonical JSON with sorted object keys. These sources are pinned by their captured SHA-256 values in `evidence/identity.txt`.

`inspect_rust_binary` is path-sensitive on this measured class because `dist/application/rust/RustBinaryService.js:55-80` builds path-bearing semantic fields: `parameters.path`, `normalized_result.artifact.path`, and an `artifact-path` location. The same `/usr/bin/rustc` bytes at two different paths produced distinct Evidence IDs; changing only `subject.name` and `subject.local_path` leaves the recomputed ID unchanged, while substituting those three semantic path fields alone reproduces copyA's reported ID. No formula is inferred from path correlation alone: all four IDs were recomputed against the complete returned Evidence envelopes.

## First-hand observations

- `VERIFIED` — two `inspect-rust-binary /usr/bin/rustc --format json --full-output` calls reported the same `ev_96443401784f756a931b32301b2dc0225f66682b0bc2bb8e389267410d7cf256` ID. Both envelopes are retained in `evidence/probe-base1.json` and `probe-base2.json`.
- `VERIFIED` — `/usr/bin/rustc`, copyA and copyB each hash to `c916a85b7d4f52d9650399eebd15c672377933e6c2d8e98215757ab0b9b37136`; each is 5,240 bytes in the returned report. The copied-path IDs differ: `ev_33365d113896f2f8241b0bcebed2961c16209b00d9ea7b24db1457d1427090e9` and `ev_e9515fabeb467b13bd129c34f1b149b8ccfe2ec86f6e754830806f93de8c8de2` (`evidence/probe-copyA.json`, `probe-copyB.json`). `sha256sum` and `file /usr/bin/rustc` were run first-hand; full identities are in `evidence/identity.txt`.
- `REPRODUCED` — independent canonical projection recomputation matches all four reported IDs; changing only display subject fields keeps the base ID, and replacing only the three path-bearing semantic fields yields the exact copyA ID (`evidence/id-recompute.json`; implementation: `evidence/recompute-ids.mjs`).
- `VERIFIED` — the probe is a successful static RESULT, not a claim about runtime execution. The report has `auditable_metadata:null` and `rustc_commit:null`; its own limitation says absence of `.dep-v0` does not establish absence of dependencies (`evidence/probe-base1.json`).
- `VERIFIED` — source-derived Command A at frozen HEAD `5694506a862c32d2f7aac44935778bce4b6184f2` returned `knowledge_files:88`, `mapped:88`, `missing:[]`, `dangling:[]` (`SCORECARD.md:88-124`; exact JSON: `evidence/command-A-before.json`). This artifact is a draft and does not change the count.
- `UNVERIFIABLE` — post-integration `89/89` Command A result: this seat may write only its wave artifact; the corpus entry and Rust-row token remain proposed, not landed.

## Scope and limitations

The observed calls use one ELF at one byte identity, a repeat at the same path and two same-byte copies at distinct paths, through `inspect_rust_binary` in REA 6.7.0. They establish that this operation's emitted IDs match the package's semantic Evidence hash and that semantic path-bearing fields make this case path-sensitive. They do not establish the ID behavior of other REA operations, 6.5.0/6.4.0 or later releases, alternate artifact formats, failure records, or all Evidence field variations. The target was not executed, no network was accessed, and the copied files plus all scratch remained under `/var/tmp`.

The proposed corpus file and coverage token have not been landed. On integration, append the token to the Rust binary coverage row (`corpus/README.md:63`) and rerun Command A at the landing revision to verify `knowledge_files:89`, `mapped:89`, `missing:[]`, `dangling:[]`.
