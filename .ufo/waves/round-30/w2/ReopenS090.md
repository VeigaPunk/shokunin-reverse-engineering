# ReopenS090 — round 30, wave 2

Seat: `KaidokuR30.ReopenS090` (reviewer, leaf). Attacked: SOURCES row S090 (`corpus/SOURCES.md:96`, file sha256 `f81ff4e109174beba9e636490384c6f49ffbaf25b31cddd400d5ff32fb29722c`, last touched by `92b1dd2d`, row added `24da3459`): its tarball and member hashes, its line-7 quote (recorded in `.ufo/waves/round-30/w1/SrcReaPackage.md:77`, file sha256 `0ccd5ce7…ac4ea93`), every cited line range, and the claim that it matches the installed copy.

## Verdict

**Holds, with two low-severity defects in the CLI-bundle part of the anchor.** All five hashes reproduce from a fresh registry fetch, the line-7 quote is byte-exact, every `RustAuditableReader.js`, `RustBinaryImage.js` and `GoElfImage.js` range lands on the gate or message it is cited for, and the installed `dist/` tree is byte-identical to the tarball's `dist/` tree.

Wrong or defective items:

1. **Wrong member path (low).** The row says "bundled `cli.js`" with "members `package/dist/...`". `package/dist/cli.js` exists and hashes to `73ec2c86…75e97e` (120 lines). The anchored hash `168cd322…18e2204` is `package/dist/cli-runtime/cli.js` (41,847 lines). Someone rechecking the row as written would hash the wrong file and see a mismatch. The wave-1 report extracted and hashed `dist/cli-runtime/cli.js` (`SrcReaPackage.md:47,59-60`); the `cli-runtime/` part was dropped when the row was written. Fix: name `dist/cli-runtime/cli.js`.
2. **Range one line short (low): `cli-runtime/cli.js:5176-5217`.** The wave-1 report says the range "embeds the reader" (`SrcReaPackage.md:65`). The 1 MiB check opens at `:5215`, but its message `"Dependency section exceeds the 1 MiB compressed limit"` is on `:5218`, outside the range. The embedded reader region actually runs from `:5176` to `:5413` (`})))();` / `}`). Fix: `:5176-5218` (constants, schemas, empty and 1 MiB gates) or `:5176-5413` (the whole embedded reader).

No other range is wrong.

## Evidence

### Fetch and hashes (observation)

- Command: `timeout 120 curl -sS -o rea-agents-6.5.0.tgz -w 'http=%{http_code} size=%{size_download}\n' https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz` in `/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReopenS090/`. Output `http=200 size=5634033`, exit 0, 2026-10-23T03:12:16Z.
- `sha256sum rea-agents-6.5.0.tgz` gave `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699`, which **matches** the row. `tar -xzf` exit 0.
- Member hashes (tarball extraction vs `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/`, installed `package.json` `"version": "6.5.0"`), 2026-10-23T03:13:31Z, exit 0:

| member | tarball sha256 | installed sha256 | row anchor |
|---|---|---|---|
| `dist/rust/RustAuditableReader.js` | `1f3748c9…fb97fd6505` | identical | match |
| `dist/rust/RustBinaryImage.js` | `08adaa59…d236ea681` | identical | match |
| `dist/go/GoElfImage.js` | `ee88b9cd…aa483204` | identical | match |
| `dist/cli-runtime/cli.js` | `168cd322…218e2204` | identical | match (the row calls it "bundled `cli.js`"; see defect 1) |
| `dist/cli.js` | `73ec2c86…6c75e97e` | identical | not the anchored file |
| `dist/go/GoBinaryContainer.js` | `2db56f92…2e52788b2` | identical | not anchored by S090 (see residual risk) |

- Whole-tree check: `timeout 120 diff -rq x/package/dist <installed>/dist` printed nothing, `diff_rc=0` (observation: the installed `dist/` is byte-identical to the published `dist/`).

### Line-7 quote (observation)

- `grep -nF 'export const RUST_SECTION_BYTES = 1024 * 1024;' x/package/dist/rust/RustAuditableReader.js` printed `7:export const RUST_SECTION_BYTES = 1024 * 1024;`, rc 0, 2026-10-23T03:12:58Z. The quote and its line number **hold**.
- Nit: `SrcReaPackage.md:77` calls the quote "8 words". `awk 'NR==7{print NF}'` gives `7` whitespace tokens. It is under 25 words either way, so this has no effect.
- The S090 anchor cell itself carries no quote. Sibling rows S088, S089 and S091 don't carry quotes in their anchors either, so this follows lane convention (observation). The located quote is kept only in the wave-1 report.

### Cited ranges, `RustAuditableReader.js` (309 lines; read from the tarball copy, `cat -n`, exit 0)

| range | content at that range | verdict |
|---|---|---|
| `:5-14` | `RUST_BINARY_INPUT_BYTES = 256 MiB` (5), `RUST_SECTION_BYTES` (7), `RUST_INFLATE_RATIO = 64` (9), `RUST_UNCOMPRESSED_BYTES` (11), `RUST_OUTPUT_BYTES` (13), `JSON_DEPTH = 32` (14) | holds |
| `:51-57` | `"Dependency section is empty"` (52); `> RUST_SECTION_BYTES` and the `"…exceeds the 1 MiB compressed limit"` message (53-57) | holds |
| `:78-94` | `inflateSection`: `min(8 MiB, len*64)` (79), `rejectGarbageAfterEnd` (83), `"…has bytes after the zlib stream"` (87), `inflateFailure` (93); closing `};` is at 95 | holds |
| `:136-170` | `inflateFailure` (`ERR_BUFFER_TOO_LARGE` gives "Inflated dependency JSON exceeds the size limit" at 139; zlib codes give "…not a complete zlib stream" at 143), `parseDocument` (UTF-8 152, depth 154, JSON 160, format schema 164, package schema 170) | holds |
| `:188-205` | `admitGraphExpansion` and the `admit` budget throw, "…complete report byte budget before expansion" (204) | holds (the loop at 206-218 is outside the range, but the message is inside it) |
| `:220-285` | `PACKAGE_FIELDS`, `rejectMalformedPackages` with "Dependency package N does not match the package schema" (236), `packageRecord` kind check (251-254), `assertDepth` with "…nesting exceeds 32 levels" (285) | holds |
| `:299-309` | `rootIndex`: "…more than one root package" (302), "Dependency index … is outside the package list" (306) | holds |

### Cited ranges, other files

| range | content | verdict |
|---|---|---|
| `RustBinaryImage.js:42-56` | `dependencySection`: duplicate (46), compressed (51), not file-backed (53); `readDependency` (56) | holds |
| `GoElfImage.js:181-195` | `elfImageSection`: `SHT_NOBITS` gives `file_backed: false` (186), `compressed = flags & 0x800` (187), read-only derivation (188-193) | holds |
| `cli-runtime/cli.js:5117` | `OPERATION$31 = "inspect_rust_binary";` | holds |
| `cli-runtime/cli.js:5176-5217` | `//#region dist/rust/RustAuditableReader.js` (5176), constants (5181-5186), schemas (5187-5196), failure classes, empty gate (5214), 1 MiB condition (5215); the **message is at 5218** | **one line short** (defect 2) |
| `cli-runtime/cli.js:5284-5310` | inflate-size message (5287), zlib message (5288), UTF-8 (5296), JSON (5303), format schema (5306), package schema (5310) | holds |
| `cli-runtime/cli.js:5390-5410` | nesting (5391), root count (5405), index range (5408) | holds |
| `cli-runtime/cli.js:5453-5457` | duplicate (5453), compressed (5456), not file-backed (5457) | holds |

Producing command for the CLI rows: `awk` line windows over `x/package/dist/cli-runtime/cli.js`, exit 0, 2026-10-23T03:12:58Z. The excerpt `5218 			}, "Dependency section exceeds the 1 MiB compressed limit");` is preserved in `raw.txt`.

## Residual risk and verification gaps

- Inference: the `RustAuditableReader.js` ranges skip the zod schema definitions at `:15-30`. One of them, `documentVersionSchema` `format: …nonnegative()` at `:24`, is the clause that refuses mutant `r-format-negative`. The schemas are covered only through `cli-runtime/cli.js:5187-5196` inside the short `5176-5217` range. This is not wrong, but the dist-file anchor doesn't by itself show the schema the row's scope names.
- Observation: the knowledge entry `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md:1` attributes `dist/go/GoBinaryContainer.js` to S090, but the S090 anchor has no hash or range for that file. I verified it is byte-identical to the installed copy (`2db56f92…`), but the row doesn't anchor it.
- Not checked: the registry metadata JSON (`.dist.integrity` / `.dist.shasum`) for 6.5.0. The hash check was against the row's sha256 only. No REA run was made (none was assigned), and no carrier or mutant was touched.

## Artifacts (`/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReopenS090/`)

- `rea-agents-6.5.0.tgz`: sha256 `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699`
- `x/package/…`: full tarball extraction (member hashes in the table above)
- `raw.txt`: consolidated hash, diff, quote and CLI-line receipts, sha256 `6aa0c46a06729d1b15f20fb3b0bcb0307df79c8c65d7eafd630670a9514d8378`

Source record: https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz, accessed 2026-10-23, sha256 `531717a0…218e699`. Located quote: `package/dist/rust/RustAuditableReader.js` line 7, "export const RUST_SECTION_BYTES = 1024 * 1024;".

Tool installs or updates: none. No lane files edited other than this report, no git or jj writes, and no processes left running.
