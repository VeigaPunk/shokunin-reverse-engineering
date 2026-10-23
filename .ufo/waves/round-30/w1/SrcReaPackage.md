# R30-C2 source package report — SrcReaPackage

## Behavior
Opened the npm 6.5.0 version record and published tarball by ordinary HTTPS `curl`; verified tarball SHA-1/SHA-512 against registry metadata; extracted the four requested members; SHA-256 of each extracted member equals the installed copy. Read the frozen C2 claim and predictions to scope the code anchors. Drafted S090 below; did not edit `corpus/SOURCES.md`.

## Gates
- **Registry integrity:** pass. Registry `dist.shasum` and `dist.integrity` exactly match the downloaded tarball's SHA-1 and SHA-512.
- **Installed-source identity:** pass for the four requested files; all four SHA-256 pairs match.
- **R30-C2/live REA gate:** not run by this seat. No live behavior or claim result is established here; the source only grounds frozen predictions. No carrier or mutant was executed.

## Touched surfaces
- Read-only lane inputs: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`, `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json`, and `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/predictions.tsv`.
- The requested knowledge entry `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` was absent when read; the draft row names its intended `used-by` path.
- Created only this report in the lane. Downloaded/extracted source artifacts are under `/fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/`.
- No install/update was made. No Git/jj writes, REA invocation, product edit, or source-registry edit.

## Out of scope and limits
- This is code-source evidence, not an REA run, a C2 counter receipt, or evidence that the predictions match live outcomes.
- Only the four requested dist members were extracted and compared; no full-package tree comparison, npm provenance/attestation validation, or other package version was checked.
- No carrier or mutant was executed. The source's declared limits/messages do not establish actual runtime behavior on any file.

## Findings

### F1 — npm version document and tarball provenance

**Metadata command** (bounded; `curl` returned success because the chained clock command ran):

```text
timeout 300 curl --fail --silent --show-error --location --proto '=https' --tlsv1.2 'https://registry.npmjs.org/rea-agents/6.5.0' --output /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/registry-6.5.0.json
```

UTC: `2026-10-23T02:42:24Z`; compound command exit 0. Registry metadata excerpt: `dist.tarball=https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz`, `dist.shasum=7ea5e6f669bc18c45dbf5dba653edaa1ada07ab3`, `dist.integrity=sha512-C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==`. Metadata SHA-256: `52184d3129b17c15a223736c48a3235038f26aa8aaa959f30a4b0931453b5cde` (final digest pass, 2026-10-23T02:46:03Z, exit 0).

**Tarball command**:

```text
timeout 300 curl --fail --silent --show-error --location --proto '=https' --tlsv1.2 'https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz' --output /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/rea-agents-6.5.0.tgz
```

UTC: `2026-10-23T02:42:47Z`; compound command exit 0. Tarball SHA-1 output `7ea5e6f669bc18c45dbf5dba653edaa1ada07ab3`; SHA-256 `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699`; OpenSSL SHA-512/base64 output `C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==`. The SHA-1 and SHA-512 exactly match `dist.shasum` and `dist.integrity`; final timestamped digest pass completed by `2026-10-23T02:46:03Z`, exit 0.

### F2 — extraction and installed-copy SHA-256 comparisons

Extraction command (exit 0; no stdout; each extracted file was subsequently read by `sha256sum`):

```text
timeout 300 tar -xzf /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/rea-agents-6.5.0.tgz -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage package/dist/rust/RustAuditableReader.js package/dist/rust/RustBinaryImage.js package/dist/go/GoElfImage.js package/dist/cli-runtime/cli.js
```

The final timestamped SHA-256 command completed successfully by `2026-10-23T02:46:03Z` (exit 0). Exact output; each extracted hash is identical to its installed counterpart:

```text
1f3748c9ed6d04721a9bef364195e5d9b3d86794088c8594a366a9fb97fd6505  /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/package/dist/rust/RustAuditableReader.js
1f3748c9ed6d04721a9bef364195e5d9b3d86794088c8594a366a9fb97fd6505  /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/rust/RustAuditableReader.js
08adaa596386428c84c2a8faa5d9e7b80199c14e5650ebd9fca41acd236ea681  /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/package/dist/rust/RustBinaryImage.js
08adaa596386428c84c2a8faa5d9e7b80199c14e5650ebd9fca41acd236ea681  /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/rust/RustBinaryImage.js
ee88b9cd54763d7106068d4ba4055eac8f6c57218bc34aaed5dc9eecaa483204  /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/package/dist/go/GoElfImage.js
ee88b9cd54763d7106068d4ba4055eac8f6c57218bc34aaed5dc9eecaa483204  /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/go/GoElfImage.js
168cd322a29c9baed02d7e44ab5ae9b2634b3f5b872ff5fcfa3bd20b718e2204  /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/package/dist/cli-runtime/cli.js
168cd322a29c9baed02d7e44ab5ae9b2634b3f5b872ff5fcfa3bd20b718e2204  /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cli-runtime/cli.js
```

### F3 — located source behavior

Read the tarball-extracted source after verification. `RustAuditableReader.js:5-14` declares the selected-input, section, inflate ratio, uncompressed/output and JSON-depth limits; `:51-57` emits the empty/over-1-MiB messages; `:78-94,136-145` bounds inflation and maps zlib failures; `:146-170` validates UTF-8, JSON and schema; `:188-205` bounds report expansion; `:220-285` checks package fields/kind and nesting; `:299-309` checks root count and dependency indices. `RustBinaryImage.js:42-56` rejects duplicate, compressed and non-file-backed `.dep-v0` sections. `GoElfImage.js:181-195` marks `SHT_NOBITS` non-file-backed and derives compressed/read-only flags. The CLI bundle identifies `inspect_rust_binary` at `cli.js:5117`, embeds the reader at `:5176-5217`, carries the failure messages at `:5284-5310`, root/index checks at `:5390-5410`, and section gates at `:5453-5457`. Source line reads were complete by the clock observation `2026-10-23T02:45:13Z`; the code bytes were rehashed at `02:46:03Z`.

#### Draft SOURCES row S090

```text
| S090 | rea-agents 6.5.0 Rust auditable-reader implementation — https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz (members `package/dist/...`), compared with `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/` | code | A | The `inspect_rust_binary` reader's Rust dependency-section gates, input/section/inflate/output/nesting limits, schema/root/index checks and refusal messages; not observed REA outcomes | Tarball SHA-256 `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699`; `RustAuditableReader.js` SHA-256 `1f3748c9ed6d04721a9bef364195e5d9b3d86794088c8594a366a9fb97fd6505`, `:5-14,51-57,78-94,136-170,188-205,220-285,299-309`; `RustBinaryImage.js` SHA-256 `08adaa596386428c84c2a8faa5d9e7b80199c14e5650ebd9fca41acd236ea681`, `:42-56`; `GoElfImage.js` SHA-256 `ee88b9cd54763d7106068d4ba4055eac8f6c57218bc34aaed5dc9eecaa483204`, `:181-195`; bundled `cli.js` SHA-256 `168cd322a29c9baed02d7e44ab5ae9b2634b3f5b872ff5fcfa3bd20b718e2204`, `:5117,5176-5217,5284-5310,5390-5410,5453-5457` | Grounds the frozen R30-C2 predictions in the matching published 6.5.0 reader and CLI-bundled implementation; actual prediction agreement requires the live C2 run and its receipts. | mined | 2026-10-23 | on-release | corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md |
```

### F4 — Gate note and source quotes

## Gate

The published source establishes the configured 1 MiB compressed-section constant, not a live refusal result. Located quote from the served tarball member `package/dist/rust/RustAuditableReader.js:7` (8 words): “export const RUST_SECTION_BYTES = 1024 * 1024;” The metadata response is a single minified JSON line (the `wc -l` command returned `0` newline characters); located quote at JSON line 1, `.dist.tarball`: `https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz`.

## Provenance commands and UTC observations

- Metadata fetch command and output/time are recorded in F1; registry URL `https://registry.npmjs.org/rea-agents/6.5.0`, opened `2026-10-23`, SHA-256 `52184d3129b17c15a223736c48a3235038f26aa8aaa959f30a4b0931453b5cde`, quote above.
- Tarball fetch command and output/time are recorded in F1; tarball URL `https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz`, opened `2026-10-23`, SHA-256 `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699`, quote above.
- Metadata line-shape check: `timeout 30 wc -l /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/registry-6.5.0.json && timeout 30 date -u +%FT%TZ`; output `0 .../registry-6.5.0.json` and `2026-10-23T02:45:13Z`; exit 0.
- The final checksum command was `timeout 30 sha256sum /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/registry-6.5.0.json /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/rea-agents-6.5.0.tgz /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/package/dist/rust/RustAuditableReader.js /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/rust/RustAuditableReader.js /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/package/dist/rust/RustBinaryImage.js /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/rust/RustBinaryImage.js /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/package/dist/go/GoElfImage.js /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/go/GoElfImage.js /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/package/dist/cli-runtime/cli.js /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cli-runtime/cli.js && timeout 30 sha1sum /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/rea-agents-6.5.0.tgz && timeout 30 sh -c 'openssl dgst -sha512 -binary "$1" | openssl base64 -A; printf "\n"' sh /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/rea-agents-6.5.0.tgz && timeout 30 date -u +%FT%TZ`; output is in F1/F2, UTC `2026-10-23T02:46:03Z`, exit 0.

## Scratch artifact paths and SHA-256

- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/registry-6.5.0.json` — `52184d3129b17c15a223736c48a3235038f26aa8aaa959f30a4b0931453b5cde`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/rea-agents-6.5.0.tgz` — `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/package/dist/rust/RustAuditableReader.js` — `1f3748c9ed6d04721a9bef364195e5d9b3d86794088c8594a366a9fb97fd6505`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/package/dist/rust/RustBinaryImage.js` — `08adaa596386428c84c2a8faa5d9e7b80199c14e5650ebd9fca41acd236ea681`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/package/dist/go/GoElfImage.js` — `ee88b9cd54763d7106068d4ba4055eac8f6c57218bc34aaed5dc9eecaa483204`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcReaPackage/package/dist/cli-runtime/cli.js` — `168cd322a29c9baed02d7e44ab5ae9b2634b3f5b872ff5fcfa3bd20b718e2204`
