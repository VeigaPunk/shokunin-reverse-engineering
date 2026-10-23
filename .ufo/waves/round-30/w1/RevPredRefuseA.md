# RevPredRefuseA — frozen refusal-prediction review, mutants r-empty … r-inflate-ratio

Scope: verify, by the REA 6.5.0 code (no REA run), that the frozen predictions in
`corpus/evidence/round-30/c2/predictions.tsv` are correct for mutants `r-empty`,
`r-nobits`, `r-compressed-flag`, `r-two-sections`, `r-not-zlib`, `r-trailing-bytes`,
`r-over-1mib`, `r-inflate-ratio` of base carrier `elf-x86_64-uvx`.
Reviewer seat; lane read-only; mutant bytes inspected read-only (never executed).
REA was not invoked (no CLI run, no MCP). Node v24.21.0 was run alone for zlib
behaviour and for replaying the reader's inflate logic on extracted section bytes.

Code reviewed (dist, version 6.5.0 — `package.json:4`):
`~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/`
`rust/RustBinaryImage.js`, `rust/RustAuditableReader.js`, `rust/RustBinaryProvider.js`,
`go/GoBinaryImage.js`, `go/GoBinaryImage.js→readGoElfImage` in `go/GoElfImage.js`,
`go/GoBinaryContainer.js`, `domain/analysisErrorCore.js`,
`domain/analysisErrorProjection.js`, and the bundled CLI `cli-runtime/cli.js`
(handler at cli.js:5670–5673 → `projectAnalysisError`) plus
`cli-runtime/cliResultOutput-DsRMI8CJ.js` (`logCliCommand` 403–430, failure envelope
`{ok:false, error:{…}}` 722–740,750–755).

## Propagation chain (shared by all eight)

`readRustBinaryImage` (RustBinaryImage.js:9) → `readContainer` → `readGoBinaryContainer`
(GoBinaryImage.js:114–144; `\x7fELF` at 115–116 → `readGoElfImage`). ELF parse:
`readGoElfImage` (GoElfImage.js:4–139); the only per-section data checks are the
`.go.buildinfo` comparisons at 105–124 — the carrier's full section list
(`readelf -S -W r-empty`, sections [0]–[32]) contains no `.go.buildinfo`, so that
branch is dead for every mutant. All named sections are pushed by `recordElfSection`
(140–150). Then `dependencySection` (RustBinaryImage.js:42–55) runs its checks in
order: count>1 at 45–46 → `compressed` at 50–51 → `!file_backed` at 52–53 →
`readDependency` at 56 → `readAuditableSection` (RustAuditableReader.js:50–77):
empty 51–52, >1 MiB 53–57 (a `RustAuditableResourceFailure`), `inflateSection`
78–95 → `inflateFailure` 136–145, then `parseDocument` 146+.

Enveloping (observation): `RustBinaryProvider.failureFor` (RustBinaryProvider.js:99–118)
maps `RustAuditableFormatFailure` → `AnalysisInputError` with issue
`message: "Selected artifact <path>: <cause.message>"` (kind malformed, 111–117)
or `AnalysisUnsupportedTargetError` whose reason is `cause.message` verbatim
(108–110; message template at analysisErrorCore.js:11 embeds the reason), and
`RustAuditableResourceFailure` → `AnalysisResourceConstraintError` whose reason is
`"Selected artifact <path>: <cause.message>"` (105; template at
analysisErrorCore.js:35). `projectAnalysisError` (analysisErrorProjection.js:179–225)
copies `reason`/`issue.message` verbatim into `details`. With `--format json
--full-output` the CLI writes `{"ok":false,"error":{code,category,message,details},…}`
to stdout and exits 1 (cliResultOutput-DsRMI8CJ.js:415,722–740,750–755). So every
frozen message appears verbatim in stdout JSON and `env.ok !== true` holds —
both judge conditions (counter `judge`, c2-rust-refusals.py:202–207).

## Per-mutant findings

All mutant files verified against the frozen TSV: `sha256sum` and `stat -c %s`
match `predictions.tsv` columns 4–5 exactly for all eight (command run
2026-10-23 ~02:46Z, exit 0). Observation.

| mutant | builder edit (c2-rust-refusals.py) | predicted message | first throw reached (dist lines) | verdict |
|---|---|---|---|---|
| r-empty | `sh_size←0` on `.dep-v0` (line 131) | `Dependency section is not file-backed` | `declaredFileRange` returns `file_backed: size>0n` = false (GoBinaryContainer.js:80); throw RustBinaryImage.js:52–53 | **agree** |
| r-nobits | `sh_type←8` SHT_NOBITS (line 134) | `Dependency section is not file-backed` | `elfImageSection` NOBITS override `file_backed:false` (GoElfImage.js:185–186); throw RustBinaryImage.js:52–53 | **agree** |
| r-compressed-flag | `sh_flags \|= 0x800` SHF_COMPRESSED (line 138) | `Compressed dependency sections are unsupported` | `compressed = flags & 0x800n` (GoElfImage.js:187); throw RustBinaryImage.js:50–51 (checked before file_backed) | **agree** |
| r-two-sections | `.comment`'s `sh_name` repointed at ".dep-v0" (line 142) | `Image contains more than one dependency section` | both shdrs decode name `.dep-v0`; `matches.length>1` throw RustBinaryImage.js:45–46 | **agree** |
| r-not-zlib | relocated section = 9870 garbage bytes (lines 144–145) | `Dependency section is not a complete zlib stream` | `inflateSync` throws `Z_DATA_ERROR` ("incorrect header check") inside `inflateSection` try (RustAuditableReader.js:81); mapped by `inflateFailure` `code.startsWith("Z_")` at 140–143 | **agree** |
| r-trailing-bytes | relocated = stream+4 junk bytes (line 146) | `Dependency section is not a complete zlib stream` | `rejectsTrailingJunk()===true` on node v24.21.0 → `rejectGarbageAfterEnd:true` at 83; `inflateSync` throws `ERR_TRAILING_JUNK_AFTER_STREAM_END`; mapped at 140–143 | **agree** |
| r-over-1mib | relocated = 1048577 raw bytes (line 148) | `Dependency section exceeds the 1 MiB compressed limit` | `bytes.length > RUST_SECTION_BYTES` (RustAuditableReader.js:53–57) → `RustAuditableResourceFailure`; inflate never reached | **agree** |
| r-inflate-ratio | relocated = zlib(JSON+~3 MiB spaces), 14009 compressed (line 149) | `Inflated dependency JSON exceeds the size limit` | `maximum = min(8 MiB, 14009×64) = 896576` (line 79); `inflateSync` `maxOutputLength` throws `ERR_BUFFER_TOO_LARGE` ("Cannot create a Buffer larger than 896576 bytes"); mapped at 138–139 | **agree** |

### Evidence excerpts (observation)

- `readelf -S -W` (2026-10-23T02:46–47Z, exit 0):
  r-empty `[31] .dep-v0 PROGBITS … Off 04e0cf Size 000000`;
  r-nobits `[31] .dep-v0 NOBITS … Off 04e0cf Size 00268e`;
  r-compressed-flag `[31] .dep-v0 PROGBITS … 00268e 00 C` (C flag shown);
  r-two-sections: exactly two `.dep-v0` rows ([30] PROGBITS e7 bytes — the renamed
  `.comment` — and [31] PROGBITS 268e bytes); `readelf … | grep -c dep-v0` → `2`, exit 0.
- Relocated sections (readelf, exit 0): all four zlib mutants `Off 0510f0`, sizes
  9870 / 9874 / 1048577 / 14009 — matching the builder's `len(raw)`, `+4`,
  `1 MiB+1`, and 14009-byte deflate of the padded JSON.
- Extracted `.dep-v0` bytes (python3 struct parse of shdrs, read-only; exit 0) and
  node v24.21.0 replay of `inflateSection`'s exact logic, same run, exit 0:
  `trailingJunkRejected = true` (probe threw `ERR_TRAILING_JUNK_AFTER_STREAM_END`);
  `r-not-zlib` → code `"Z_DATA_ERROR"` errno −3 "incorrect header check" →
  RustAuditableFormatFailure "Dependency section is not a complete zlib stream";
  `r-trailing-bytes` → code `"ERR_TRAILING_JUNK_AFTER_STREAM_END"` → same message;
  `r-over-1mib` → 1 MiB check fires before inflate;
  `r-inflate-ratio` → code `"ERR_BUFFER_TOO_LARGE"` "Cannot create a Buffer larger
  than 896576 bytes" → RustAuditableResourceFailure "Inflated dependency JSON
  exceeds the size limit" (896576 = 14009×64, i.e. the ratio bound, not the
  8 MiB absolute bound — inference from the equality, observation of the code path).
- Node version: `node --version` → `v24.21.0` (fnm shim), exit 0. This is the
  runtime `npx` will use; `rejectGarbageAfterEnd` support is required by the
  predicted code_pointer and is present.

## Disagreements

None. All eight predictions agree: message text verbatim, failure class
(`AnalysisInputError` for r-empty/r-nobits/r-two-sections/r-not-zlib/r-trailing-bytes
malformed; `AnalysisUnsupportedTargetError` for r-compressed-flag unsupported;
`AnalysisResourceConstraintError` for the two resource refusals), and the judged
contract (`ok` not true, message in stdout) holds by code inspection of the
envelope path.

## Residual observations (not judged fields, no prediction defect)

1. `code_pointer` column for the reader-file mutants cites line numbers shifted
   ~2–5 from `dist/rust/RustAuditableReader.js` (e.g. 1 MiB check at dist 53–57 vs
   predicted "54–58"; `inflateFailure` Z_* branch at dist 140–143 vs "131–134";
   ratio maximum at dist 79/138–139 vs "73,128–129"). The cited functions and
   branches are the right ones; the package ships no TS source or `.js.map`, so the
   numbers appear to reference a source-side numbering. `judge` never reads this
   column; flagging for record only.
2. The `r-empty` refusal is reached via `declaredFileRange` `file_backed: size>0n`
   (GoBinaryContainer.js:80), not the NOBITS rule — the predicted pointer already
   names GoBinaryContainer.js:80, correct.
3. `readAuditableSection`'s own "Dependency section is empty" (line 52) is never
   reached by r-empty because the container layer refuses first — consistent with
   the prediction, worth noting since the empty-check text exists and could be
   mistaken for the expected refusal.

## Risk / verification gaps

- The ELF-path conclusions (first four mutants) rest on code reading + readelf
  header dumps; no JS execution of `readGoElfImage` was performed (REA modules
  were not invoked, per "No REA run"). The data-dependent branches are fully
  pinned by the header fields shown above; residual risk is a missed earlier
  throw in `readElfFixedHeader`/phdr checks, which are identical between mutants
  and the already-inspected base carrier except the four edited fields.
- zlib-path conclusions are stronger: the reader's exact inflate logic was
  replayed under node v24.21.0 on the mutant's true section bytes and produced the
  predicted failure class/message each time.
- `rejectsTrailingJunk` is process-cached; a future node version lacking the
  option would route r-trailing-bytes to "Dependency section has bytes after the
  zlib stream" instead. Pinned to v24.21.0 on this host — holds as frozen.

## Seat artifacts

- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/RevPredRefuseA/tmp/r-not-zlib.sec`
  sha256 `ce1a33c4d93d7003f2b649042e208b7213e7510c96de23ed1609feb7380690be`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/RevPredRefuseA/tmp/r-trailing-bytes.sec`
  sha256 `ce51fc9a3dc817e06e3bed5cd7f5c6ce2b080aa8fbe5fcf1487e4f1a67c33608`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/RevPredRefuseA/tmp/r-over-1mib.sec`
  sha256 `039b54d9077559fc79dbb99ebd98422339286c4a35a5cd347845fcce89f5e399`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/RevPredRefuseA/tmp/r-inflate-ratio.sec`
  sha256 `5334ce018a2ce0d54e34e2f74dc0c49183888be9535fbf07613131f79c61f610`

Installs/updates: none (all tools already present: node v24.21.0, readelf,
python3, sha256sum; pacman untouched per pause rule).
