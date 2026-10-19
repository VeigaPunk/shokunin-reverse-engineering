# CR-1 — C2 coverage claim

## Verdict

**C2: REPRODUCED — bounded closure of one different-verb-family Unknown.** I selected the frozen candidate for an `ev_` identity domain outside `inspect-evm-interface` and independently measured `inspect_sqlite_database` under the cached REA 6.7.0 package. The earlier SQLite entry reports schema inventory behavior and limitations but no Evidence-ID characterization (`corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md:11-14`). The corpus entry here is only a draft; canonical corpus and coverage-map files remain untouched as required.

## First-hand re-derivation

- Built a synthetic SQLite fixture from `evidence/fixture.sql`; independently measured its identity as 8,192 bytes, SHA-256 `b0db23c66fcdf957241e6ff0e62404b411a913c39178de2304dd4bed272cf85c`. The REA invocation was `inspect-sqlite-database <absolute-path> --format json`, with TMPDIR under `/var/tmp`.
- At one path, two complete envelopes were byte-identical and both returned `ev_aeee5a3875b7009b0dbb8f89ad946522c7815a4e8000cc51dc969bcbdfffe8d6`. A byte-identical copy at a second absolute path retained the same database SHA-256 and size but returned `ev_5d18329c9f4f0a29f0c6080008125652c585820b0e37f7bf6ddcd5ac1262d273`.
- Recomputed the IDs independently from the semantic projection for all three envelopes; all matched. The only changed projected values across paths are `/parameters/path`, `/normalized_result/artifact/path`, and `/locations/0/path`. Masking just these three values makes the two path projections byte-identical. The REA subject's `local_path` changes but is not projected; its `name` remains the shared basename.
- Derived the formula directly from the pinned package source: `dist/domain/evidence.js:159-183` projects semantic fields and excludes subject display fields, while `dist/domain/canonicalDigest.js:1-25,27-75` computes SHA-256 over canonical JSON. SQLite call construction is at `dist/application/sqlite/SqliteDatabaseService.js:64-74`; SQLite parameters and locations are built at `dist/domain/sqlite/sqliteDatabase.js:177-185` and `dist/sqlite/SqliteDatabaseProvider.js:239-250`. Package/source hashes are recorded in `evidence/implementation-identity.txt`.
- Reproduction is end-to-end tested by `bash evidence/reproduce.sh`; its fresh three-call run and recomputation both end `result=PASS` in `evidence/reproduction-run.txt`.

## Exact evidence and corpus draft

- Full observed envelopes: `evidence/probes/{a1,a2,b1}.json`.
- Independent formula/path checks: `evidence/recompute.mjs`, `evidence/recompute.txt`, `evidence/canonicalizer-crosscheck.txt`.
- Reproducible fixture and commands: `evidence/fixture/catalog.db`, `evidence/fixture.sql`, `evidence/reproduce.sh`.
- Pinned implementation identity: `evidence/implementation-identity.txt`.
- Proposed corpus entry: `draft-corpus-entry.md`, intended destination `corpus/knowledge/2026-10-19-arc3-r9-sqlite-evidence-id-domain.md`.
- Proposed coverage-map token: `2026-10-19-arc3-r9-sqlite-evidence-id-domain`, to add to the `Evidence model` row at `corpus/README.md:41`.

## Per-item verdicts and boundary

- `inspect_sqlite_database` same-path re-derivation: **REPRODUCED** — two byte-identical complete envelopes; see `evidence/recompute.txt`.
- Different-path, same-byte SQLite identity: **REPRODUCED** — same file digest and size, distinct IDs; only the three path fields above differ in the semantic projection; see `evidence/recompute.txt`.
- `ev_` projection and SHA-256 derivation for this operation/package: **REPRODUCED** — all three hashes match; source references and hashes above.
- Command A pre-integration baseline at immutable HEAD: **VERIFIED** — `evidence/command-a-before.json` reports `knowledge_files=87`, `mapped=87`, `missing=[]`, `dangling=[]`, revision `947091d6b6f52684faf9ca53adf94ff8a0f6b006`.
- Post-integration Command A `87 → 88`: **UNVERIFIABLE in this seat** — the canonical corpus entry and map token must be landed by the integrator; write scope forbids changing either here. The `88` result is a prediction from adding one entry and one token, not an observed result.

Only one synthetic default-inventory SQLite call shape and REA 6.7.0 were tested; this closes no other operation's Evidence-ID domain and does not establish a universal formula. Full draft and retained source observations are in the paths above.
