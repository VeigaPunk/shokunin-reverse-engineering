# RevPredRefuseB — code-trace review of 11 frozen C2 predictions vs REA 6.5.0

Seat: `KaidokuR30.RevPredRefuseB` (reviewer). Round 30 wave 1.
Scope: mutants `r-not-utf8`, `r-bad-json`, `r-nesting-33`, `r-format-negative`,
`r-extra-field`, `r-kind-dev`, `r-two-roots`, `r-index-outside` and acceptances
`g-relocated`, `g-recompressed`, `g-no-root` — are the frozen predictions
(`kind`, `message`) correct by the REA 6.5.0 code? No REA run was made.
Mutant/carrier bytes were read only (never executed). Timestamps UTC
2026-10-23T02:44Z–02:47Z. No lane file modified outside this report.

## Verdict: all 11 predictions AGREE with the code

| mutant | frozen kind/message | verdict |
|---|---|---|
| r-not-utf8 | refuse `Dependency JSON is not valid UTF-8` | **agree** |
| r-bad-json | refuse `Dependency section JSON is invalid` | **agree** |
| r-nesting-33 | refuse `Dependency JSON nesting exceeds 32 levels` | **agree** |
| r-format-negative | refuse `Dependency JSON does not match the format schema` | **agree** |
| r-extra-field | refuse `Dependency package 0 does not match the package schema` | **agree** |
| r-kind-dev | refuse `Dependency package 0 does not match the package schema` | **agree** |
| r-two-roots | refuse `Dependency JSON declares more than one root package` | **agree** |
| r-index-outside | refuse `Dependency index 584 from package 0 is outside the package list` | **agree** |
| g-relocated | ok (accepted) | **agree** |
| g-recompressed | ok (accepted) | **agree** |
| g-no-root | ok (accepted) | **agree** |

## Check order traced (observation, dist line cites)

`readRustBinaryImage` (dist/rust/RustBinaryImage.js:9-56) → container via
`readGoBinaryContainer` → `dependencySection` (one `.dep-v0`, not `compressed`,
`file_backed`) → `readAuditableSection` (dist/rust/RustAuditableReader.js:50-77):
size ≤ 1 MiB (53) → `inflateSection` (78-95) → `parseDocument` (146-172):
fatal UTF-8 decode (149-152) → `assertDepth` (154; impl 264-290) →
`JSON.parse` (157-160) → `documentVersionSchema` (162-164) →
`admitGraphExpansion` (165; impl 188-219) → `rejectMalformedPackages`
(167; impl 228-238 via `packageRecord` 239-262) → `documentSchema` strict
(168-170) → `normalizePackages` (60; impl 291-298) → `rootIndex` (61; impl
299-309): >1 root throws (301-302), then out-of-range dependency throws
(303-307), else `roots[0] ?? null` (308).

Refusals surface verbatim: malformed → `AnalysisInputError` whose
`issues[].message = "Selected artifact <path>: <cause.message>"`
(RustBinaryProvider.js:106-117), projected into `details.issues[].message`
(cliResultOutput-DsRMI8CJ.js:160-169). Unsupported kind →
`AnalysisUnsupportedTargetError` (provider 107-110). Resource →
`AnalysisResourceConstraintError` reason embeds the message (104-105).
The judge greps `out_text`/`err_text`, so the frozen message appears.

## Per-mutant trace (mutant bytes verified; sha256+size match predictions.tsv)

Base carrier `elf-x86_64-uvx`: `.dep-v0` at off 319695, size 9870 (≤1 MiB),
SHT_PROGBITS, flags 0; inflates to 55 724 B JSON, `format:1`, 584 packages,
exactly one `root:true` at index 463 (`uv 0.13.0`), package keys ⊆
{name,version,source,kind,dependencies,root}, all dep indices < 584.
All scoped mutants pass every earlier container gate: `.dep-v0` count=1,
type 1, flags 0, offset+size ≤ file length.

- **r-not-utf8** — inflated bytes `ff fe fd`; `TextDecoder(fatal)` throws →
  message at RustAuditableReader.js:152 "Dependency JSON is not valid UTF-8".
  agree. (Pointer 151-152 ✓.)
- **r-bad-json** — inflated `{"packages":[` is valid UTF-8, depth 2, but
  `JSON.parse` throws → :160 "Dependency section JSON is invalid". agree.
  (Pointer 159-160 ✓.)
- **r-nesting-33** — inflated `[`*33 + `]`*33 (66 B): depth reaches 33 > 32 at
  the 33rd `[` → `assertDepth` :285 "Dependency JSON nesting exceeds 32
  levels". Fires *before* `JSON.parse`; the parse itself would succeed
  (observed: Python parsed it as nested lists), so depth is the operative
  refusal. agree. (Pointer 285 ✓.)
- **r-format-negative** — inflated `{"format":-1,"packages":[]}`: UTF-8 ok,
  depth 2, parses; `documentVersionSchema` (non-negative int ≤ 0xffffffff,
  :24) fails → :164 "Dependency JSON does not match the format schema".
  `admitGraphExpansion`/`rejectMalformedPackages` are *not* reached; the
  `packages` array being empty is irrelevant. agree. (Pointer 162-164 ✓.)
- **r-extra-field** — package 0 (`adler2`) carries `features:[]`, the only
  extra key in the doc (observed). All records pass `admitGraphExpansion`
  (counts only); `packageRecord` rejects `features` ∉ `PACKAGE_FIELDS`
  (:243-245) inside `rejectMalformedPackages` → :236 "Dependency package 0
  does not match the package schema". This fires before the strict
  `documentSchema`, which would produce the different message "Dependency
  JSON does not match the package schema" (:170). agree. (Pointer 220-246 ✓.)
- **r-kind-dev** — package 0 has `kind:"dev"` (observed kinds {null,"build",
  "dev"}). `packageRecord` rejects kind ∉ {"runtime","build"} (:251-253) →
  :236, same message. agree. (Pointer 251-254 ✓.)
- **r-two-roots** — observed `root:true` at indices 0 and 463. All packages
  pass version/admit/malformed/schema gates (`root` is a boolean, allowed).
  `rootIndex` sees roots.length=2 → :302 "Dependency JSON declares more than
  one root package". agree. Pointer cited `RustAuditableReader.js:151-153`
  but the actual throw is :302 (in `rootIndex`); message+kind correct —
  pointer is the only inaccuracy.
- **r-index-outside** — observed package 0 `dependencies:[584]`; 584 =
  packages.length → out of range. Single root, so the >1-root check passes;
  `rootIndex` finds `outside=584` in package 0 → :306 "Dependency index 584
  from package 0 is outside the package list". agree. Pointer cited
  `RustAuditableReader.js:154-157`; actual throw :306 — pointer-only
  inaccuracy. Note the message embeds 584 and index 0, matching the frozen
  string exactly.
- **g-relocated** — `.dep-v0` re-pointed to 16-aligned EOF (off 332016,
  size 9870, observed bytes identical to base section). Container layer: one
  named section, type 1 → `file_backed` (size>0, in-file), flags 0 → not
  compressed. `readDependency` (:56) → full pipeline succeeds; report
  ≤ RUST_OUTPUT_BYTES, `rustBinarySchema` passes → accepted, `ok:true`.
  agree. (Pointer RustBinaryImage.js:56 ✓.)
- **g-recompressed** — section bytes differ (size 9797 vs 9870) but inflate
  to the identical 55 724 B JSON (observed `doc==base`, `inf==base`). Same
  parse path → accepted. agree. (Pointer 76 labels `inflateSection`; the
  function spans 78-95 — off by two lines, correct symbol.)
- **g-no-root** — observed zero `root` keys across 584 packages, rest
  identical to base. Schema allows omitted `root`; `normalizePackages` →
  `root:false` (:297); `rootIndex` → `roots[0] ?? null` = null (:308).
  Domain cross-check `root===null ? roots.length!==0` passes
  (domain/rust/rustBinary.js:108). Provider wraps in Evidence with
  `auditable_metadata` intact → accepted. agree. (Pointer 159 names the
  correct expression but cites the UTF-8 catch region; actual :308 —
  pointer-only inaccuracy.)

## Prior-check coverage for each refusal (observation)

| mutant | gates passed before the predicted refusal |
|---|---|
| r-not-utf8 | section count/flags/file-backed, 1 MiB cap, inflate |
| r-bad-json | above + UTF-8, depth (depth of `{`+`[` = 2) |
| r-nesting-33 | above (fails depth before JSON.parse) |
| r-format-negative | above + UTF-8, depth, JSON.parse |
| r-extra-field | above + format schema, admitGraphExpansion |
| r-kind-dev | same as r-extra-field |
| r-two-roots | above + rejectMalformedPackages + documentSchema + normalize |
| r-index-outside | same (single root → passes the >1-root guard first) |

## Evidence & artifacts

- Predictions read: `corpus/evidence/round-30/c2/predictions.tsv` (frozen rows
  quoted above). Builder read: `tools/round-30/c2-rust-refusals.py` lines
  93-168, 200-228 (`relocate`, `build_mutants`, `judge`).
- REA code read: `dist/rust/RustAuditableReader.js`, `RustBinaryImage.js`,
  `RustBinaryProvider.js`, `dist/go/GoBinaryContainer.js` (declaredFileRange
  69-81), `dist/go/GoElfImage.js` (elfImageSection 181-195),
  `dist/domain/rust/rustBinary.js` (schema + checkPackages 82-114),
  `dist/domain/analysisErrorCore.js`, `dist/cli-runtime/cliResultOutput-*.js`,
  `dist/application/rust/RustBinaryService.js` under
  `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/`.
- Byte checks: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/RevPredRefuseB/inspect_mutants.py`
  (sha256 `fcc7c1a6415c1e87f1e8a62749855022ac95d379b9dea73c1518f740e89d7c95`),
  output `inspect_output.txt` (sha256
  `0d8e52003af21680e1a6682f26434b688cd4f7604a53443a70263047513e9219`) —
  exit 0 at 2026-10-23T02:46:43Z; every scoped mutant's sha256 and size equal
  the frozen row (`sha_ok=True size_ok=True` on all 11 lines).
- No REA invocation (per assignment); no installs; no git/jj writes.

## Residual risk / gaps

- Verdicts are a code trace plus byte verification, not an observed REA run;
  `rejectsTrailingJunk`-style runtime branching is irrelevant to these 11.
- Three `code_pointer` cells cite slightly wrong line numbers
  (`r-two-roots` 151-153 vs actual 302; `r-index-outside` 154-157 vs 306;
  `g-no-root` 159 vs 308; `g-recompressed` 76 vs 78-95). Judge consumes only
  `kind`/`message`, so predictions still match; flag for knowledge-entry
  accuracy.
- Out of scope: the other 8 predictions, counter/oracle logic beyond the
  traced calls, and live-run envelope shape (traced only as far as
  `createEvidence`/`cliError` projections).

Report: .ufo/waves/round-30/w1/RevPredRefuseB.md
