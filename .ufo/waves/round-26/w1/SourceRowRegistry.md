# R26 w1 — Source row S080: npm registry record for rea-agents@6.5.0

Seat: KaidokuR26.SourceRowRegistry. Date: 2026-10-22 (UTC). Lane read-only: no lane file was edited; this report is the only file written in the lane. Scratch artifacts: `/fast/scratch/hyaku/kaidoku-r26/seats/SourceRowRegistry/`.

## Verdict

**holds.** The npm registry's own record for `rea-agents@6.5.0` is the artefact the R26-C1 runs execute: the npx-cached tarball's sha512 and sha1 equal the registry's `dist.integrity` and `dist.shasum`, the npx lock metadata repeats the same digest, and the installed tree is file-for-file byte-identical to that tarball (1650 files, 25 564 765 bytes, 0 content mismatches). Id check: `grep -c 'S079\|S080' corpus/SOURCES.md` → `0`; the registry holds 78 rows, S001–S078, so S079 (seat `KaidokuR26.SourceRowEvidence`, the 6.5.0 code row) and S080 (this seat) are consecutive and both unused at the freeze commit `c27f445e70cedbaf5300b2fd0a53e821d9b659a9`. Base census `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → `ok`, exit 0 (5 pre-existing W04 warnings, none from S080).

## The row (paste-ready, 11 cells, no `|` inside any cell)

| S080 | rea-agents 6.5.0 npm registry record — https://registry.npmjs.org/rea-agents/6.5.0 (tarball https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz; packument https://registry.npmjs.org/rea-agents) | dataset | A | Publish identity and integrity of rea-agents@6.5.0 as served by the npm registry, and the identity of the npx-installed copy the R26-C1 runs use; not the package's runtime behaviour | Version document `dist.integrity` `sha512-C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==`, `dist.shasum` `7ea5e6f669bc18c45dbf5dba653edaa1ada07ab3`; packument `time["6.5.0"]` `2026-10-14T12:56:14.513Z`; attestation `https://registry.npmjs.org/-/npm/v1/attestations/rea-agents@6.5.0`, predicate `https://slsa.dev/provenance/v1`, `resolvedDependencies[0].digest.gitCommit` `3b79af28e80785afce9f5998d8f03289402a1847`; npx lock `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/.package-lock.json` entry `node_modules/rea-agents`; fetched bytes sha256 `52184d3129b17c15a223736c48a3235038f26aa8aaa959f30a4b0931453b5cde` (version document), `bfa6974e131d1bafa18cbfd5d2b590c9ae9ee9965916e0c45014f3e8fce36450` (packument), `af5a2c203702c99a70713075860cdf87ef108383cc74d3e020a235ad2d7bdf0b` (attestation); opened 2026-10-22 | The 6.5.0 tarball behind the R26-C1 runs is the registry's own published artefact: the npx-cached tarball's sha512 and sha1 equal `dist.integrity` and `dist.shasum`, and the installed tree is file-for-file identical to that tarball, so the pin is a named registry record rather than a local directory. | mined | 2026-10-22 | on-release | corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md, corpus/lessons/round-26.md |

## The lesson `## Gate` text (paste-ready)

For `corpus/lessons/round-26.md`, new-rows table (the S079 seat's five columns, so both new rows can sit in one table):

| row | source and access date | sha256 of the bytes read | located quote (at most 25 words) | section |
|---|---|---|---|---|
| S080 | https://registry.npmjs.org/rea-agents/6.5.0, npm registry version document for `rea-agents@6.5.0`; opened 2026-10-22 | 52184d3129b17c15a223736c48a3235038f26aa8aaa959f30a4b0931453b5cde | "integrity": "sha512-C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==" | `dist.integrity` |
| S080 | same version document; opened 2026-10-22 | 52184d3129b17c15a223736c48a3235038f26aa8aaa959f30a4b0931453b5cde | "shasum": "7ea5e6f669bc18c45dbf5dba653edaa1ada07ab3" | `dist.shasum` |
| S080 | https://registry.npmjs.org/rea-agents, npm packument for `rea-agents`; opened 2026-10-22 | bfa6974e131d1bafa18cbfd5d2b590c9ae9ee9965916e0c45014f3e8fce36450 | "6.5.0": "2026-10-14T12:56:14.513Z" | `time["6.5.0"]` |
| S080 | https://registry.npmjs.org/-/npm/v1/attestations/rea-agents@6.5.0, npm attestation bundle; opened 2026-10-22 | af5a2c203702c99a70713075860cdf87ef108383cc74d3e020a235ad2d7bdf0b | "gitCommit": "3b79af28e80785afce9f5998d8f03289402a1847" | SLSA payload `predicate.buildDefinition.resolvedDependencies[0].digest.gitCommit` |

Gate note to accompany the table:

> S080 is a new row; no older row's `status`, `recheck` or `used-by` cell changes. It grounds the published identity of the 6.5.0 pin only; the per-verb Evidence-ID verdicts belong to the round-26 C1 table, its counter and the S079 code row. Search log (contract rule 5): one bounded search — the npm registry version document and packument for `rea-agents` 6.5.0, opened 2026-10-22; identified 1, screened 1, included 1 (S080), excluded 0 (the 6.7.0 record is S037, the 6.5.0 installed code is S079); stop rationale: the pin's identity is fully answered by the registry record plus the cached tarball digest.

## Does the installed package match the registry record?

Yes — four independent checks, all 2026-10-22, exit 0 (script `verify-installed.py`, receipt section 5). (1) The cached tarball `/home/vgpnk/.npm/_cacache/content-v2/sha512/0b/a0/46ec…f8` (5 634 033 B) has sha512 == `dist.integrity` and sha1 `7ea5e6f669bc18c45dbf5dba653edaa1ada07ab3` == `dist.shasum`. (2) The npx lock entry `node_modules/rea-agents` gives version `6.5.0`, resolved `https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz`, integrity == `dist.integrity`. (3) The installed manifest equals the version document in all 19 compared fields (name, version, description, license, repository, homepage, bugs, engines, packageManager, bin, dependencies, optionalDependencies, publishConfig, mcpName, keywords, type, imports, allowScripts, overrides): 0 differences; installed `package.json` sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`. (4) The installed tree equals the cached tarball file for file: 1650 files each, file sets equal, 0 content mismatches, 25 564 765 bytes == `dist.unpackedSize`, 1650 == `dist.fileCount`. npx lock digests: `node_modules/.package-lock.json` `db11c1095adc50bdc3fe50f2174003f5b975d778f322c88d53d0f17953c5f071`, `package-lock.json` `464e94f3e6338e637955a813dbb9117f9b877edbe5e4ad5aced298e6a65bcef8`.

## Findings (labels per the evidence contract)

- observation — the version document publishes `dist.integrity`, `dist.shasum`, `dist.fileCount` 1650, `dist.unpackedSize` 25564765 and tarball `https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz` (`jq -S .dist rea-agents-6.5.0.json`, 2026-10-22T12:12Z); the packument gives `time["6.5.0"]` = `2026-10-14T12:56:14.513Z` and `dist-tags.latest` = `6.7.0`; published with npm 11.16.0 on node 24.18.0. The npm attestation for 6.5.0 carries a SLSA v1 predicate whose subject digest is that same sha512 and whose `resolvedDependencies[0].digest.gitCommit` is `3b79af28e80785afce9f5998d8f03289402a1847` (workflow `.github/workflows/release.yml` of `https://github.com/morluto/rea`).
- observation — a second plain-HTTP fetch at 2026-10-22T12:16:28Z returned HTTP 200, 21 678 bytes, identical sha256 (`cmp` clean): the fetched bytes are stable.
- inference — the C1 pin can be stated as "npm-published rea-agents@6.5.0, sha512 C6BG7Lyr…", so the table's tool version is checkable against a third party, not only against the local npx directory.
- inference — the attestation binds the tarball to a source commit this seat did not open, so the row claims publish identity only; the provenance chain itself is out of scope here.
- unknown — whether the GitHub source at that commit builds byte-identical package output; not measured.

## Registry self-check (sandbox; lane untouched)

`sources-census.sh validate --file sandbox/corpus/SOURCES.md --today 2026-10-22` over a copy of `corpus/` plus the proposed row: red state (the two `used-by` paths absent) → `E11 S080 missing used-by corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md` and `E11 S080 missing used-by corpus/lessons/round-26.md`, exit 1 — the check can fail; green state (both paths present) → `ok`, exit 0, 79 rows, tier.A 73, status.mined 77, status.rejected 2, with no E01–E12 for S080 (11 cells NF=13, valid kind/tier/status, `opened` not in the future, `recheck` `on-release` accepted as symbolic cadence, no E04 because the normalized first URL `registry.npmjs.org/rea-agents/6.5.0` differs from S037's `…/6.7.0`).

## Dependency for the L1 integrator

- `used-by` names `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md` and `corpus/lessons/round-26.md`; the knowledge entry appeared in the working tree during this seat's run, the lesson file did not (both checked 2026-10-22), so census E11 flags S080 until the lesson lands. Land the entry, the lesson and the row in one commit.
- S080's id must also appear under `## Gate` in `corpus/lessons/round-26.md` for the frozen R26-C1 `entry_ok` rule (a SOURCES row with `opened` 2026-10-22 named in that Gate). Optional: the L1 may copy the three fetched documents into `corpus/evidence/round-26/sources/` and re-check their sha256 against the Gate table values.

## Artifacts (seat dir, sha256)

| file | sha256 |
|---|---|
| `…/SourceRowRegistry/receipt.txt` | 49485654ad6588ca017893783706d63b09b869fd06ecda422385393c744bf50f |
| `…/SourceRowRegistry/row-080.md` | 49096f720f1936a2d4b833bddbd737303936151d0879f8d38160076bffbccecc |
| `…/SourceRowRegistry/verify-installed.py` | bbfe631df07f56cfc659091772ed8345b98032e47175acd46518d33a3d9b283b |
| `…/rea-agents-6.5.0.json` (version document, 21678 B) | 52184d3129b17c15a223736c48a3235038f26aa8aaa959f30a4b0931453b5cde |
| `…/rea-agents-packument.json` (packument, 327312 B) | bfa6974e131d1bafa18cbfd5d2b590c9ae9ee9965916e0c45014f3e8fce36450 |
| `…/attest-6.5.0.json` (attestation bundle) | af5a2c203702c99a70713075860cdf87ef108383cc74d3e020a235ad2d7bdf0b |
| `…/slsa-payload.json` (decoded SLSA payload) | 6001416ab8008690e984ab77e56ff4c00b6e0b9f13d0e4347738af19a10d096a |
| `…/refetch-6.5.0.json` (stability refetch, 21678 B) | 52184d3129b17c15a223736c48a3235038f26aa8aaa959f30a4b0931453b5cde |
| `…/sandbox/` (census sandbox copy; lane untouched) | directory, reproducible from the copy command in the receipt |

## Out of scope / not done

- No REA run (this seat's deliverable is a source row; REA calls are bound to the C1 counter's argv and seat scratch).
- No lane file was edited (`corpus/SOURCES.md`, `corpus/`, `tools/` untouched); no git or jj write; only read-only git (`rev-parse`, `status --porcelain`) and read-only file reads. No tool was installed or upgraded.
- The GitHub source commit behind the SLSA provenance was not opened; the row claims publish identity, not build reproducibility. The 6.7.0 install under `/home/vgpnk/.npm/_npx/a1722018f28f9df2/` was not examined (covered by S037).
