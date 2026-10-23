# WSourceEmitter — source-expectation review (Kaidoku R33 w1)

- Seat: `KaidokuR33.WSourceEmitter` (reviewer, leaf; no subagents, no background jobs).
- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only except this Report).
- Context: R33-C1 is STOPPED UNPROVABLE (claim-stop.json). This review is reachable primary-source evidence only — no code run, no fixture construction, no replacement benchmark, no revived carrier claim.
- Pinned revision: LLVM `0d261d1ca552c95a8f007e061c787ac7132fbcbc` (source-pins.json). All four assigned sources were re-read at exact ranges; sha256 digests match source-pins.json (recorded below).

## Files re-opened (source expectations only)

| File | Ranges | sha256 (verified vs source-pins.json) |
|---|---|---|
| `sources/Chunks.h` | 475–488 (getArm64ECRangeType); 433–437, 206–208, 269–271 (characteristics accessors); 794–813 (ECCodeMapEntry/Chunk) | `09e505a28bb8aa521f1023c30b2810198e3ea89e2d578423c2c6076d6e2db3f1` |
| `sources/Chunks.cpp` | 944–956 (ECCodeMapChunk size/write); 791–794 (CommonChunk); 1080–1082 (MergeChunk) | `550c20df652f683c20ef041e4feec63326b09ece9469fe4fe90b6ce03b79ab14` |
| `sources/Writer.cpp` | 593–632 (createECCodeMap); 1743–1755 (sortECChunks); 1112–1133, 2130–2148 (characteristics consumers); 1759–1766 (call order) | `229163a9be04e588b7b9c2bc6f3f6dc889138886bae660b713502a29aed587bd` |
| `sources/arm64ec-codemap.test` | 153–192 (CODEMAPCM + CODEMAPMS); plus 1–298 full context | `edf6964b69261a5354d90b2fed1689c089b8600393f5a7b63e5047b42c229022` |
| `sources/Object-COFF.h` | 734–773 (chpe_metadata, chpe_range_type, chpe_range_entry) | per source-pins.json |
| `sources/pe-format.md` | scanned for CodeMap/CHPE coverage (absent) | per source-pins.json |

No tool installs were performed (no Tooling directive triggered). Read-only OS utilities only: `sha256sum`, `grep`.

## A. Emitter behavior — verified source facts (not fresh Windows observations)

F1. **Membership gate is chunk-level, derived from the *input* section header — never from the output section's final merged characteristics.**
`createECCodeMap()` keys on `c->getArm64ECRangeType()`, which tests `getOutputCharacteristics() & IMAGE_SCN_MEM_EXECUTE` (Chunks.h 477). For `SectionChunk`, `getOutputCharacteristics()` returns `header->Characteristics & (permMask | typeMask)` — the input COFF section header (Chunks.h 269–271, masks at 44/47). `NonSectionCodeChunk` returns `READ|EXECUTE` unconditionally (Chunks.h 206–208); `MergeChunk` (`READ|CNT_INITIALIZED_DATA`) and `CommonChunk` (`UNINITIALIZED_DATA|READ|WRITE`) are non-execute.

Consequences, all confirmed by pinned tests:
- Code chunks merged into a data output section are still mapped (CODEMAPCM: X64 entry from `.text`/`test` merged into `.testdat`), because their input header still carries `EXECUTE`.
- Data chunks merged into a code output section are still excluded (CODEMAPDM: `test`/`.rdata` contents at 0x1000–0x1008 are unmapped; entries begin at 0x2000).
- Output-section attributes are irrelevant to entry membership. Any reader/profile rule that derives membership from output-section attributes alone rejects valid lld output.

F2. **Range type is per-chunk, from the input file's machine; tag 0 is a default bucket.**
`getArm64ECRangeType()` returns `Amd64` for AMD64 chunks, `Arm64EC` for ARM64EC chunks, and `Arm64` for every other executable chunk (Chunks.h 480–487). The `Arm64` tag therefore is the *default* bucket for executable chunks that are neither AMD64 nor ARM64EC (matches S101 tag-0 semantics). Mixed-machine links yield mixed ranges (CODEMAPX: ARM64, ARM64EC, X64 entries), so per-image single-type claims are unsupported.

F3. **Grouping is by maximal same-type run across the flat iteration of all output sections; section boundaries never close a run; any intervening untyped chunk does.**
`closeRange()` fires only when `chunkType != lastType` (or at end of list). `last` advances on every chunk, including untyped ones, so a run's Length covers any intervening untyped chunk/padding. Evidence:
- CODEMAPMS (153–192) expects **one** ARM64EC entry `0x5000 – 0x6008` spanning two output sections (`.test` and `.test2`, plus the inter-section alignment gap) — comment at line 183: "Test code map range entry spanning over multiple sections."
- CODEMAPDM expects *separate* ARM64EC entries `0x2000` and `0x7000` despite identical types, because untyped content intervenes in the iteration.
- Merged code extends an existing same-type run (CODEMAPM: single ARM64EC `0x1000–0x1010`, X64 `0x2000–0x200E`).

F4. **Page-rounded start, exact byte length (includes non-code prefix/slack).**
`ECCodeMapChunk::writeTo` (Chunks.cpp 948–955): `start = getRVA() & ~0xfff; StartOffset = start | type; Length = last->getRVA() + last->getSize() - start`. Length is *not* independently aligned, and the range start is pulled down to the page boundary even when the first code byte is later. Observed: CODEMAPCM's X64 entry starts at `0x4000` while the first code byte in `.testdat` is at `0x4010` — 0x10 non-code bytes inside the range.

F5. **Empty ranges: lld skips empty `SectionChunk`s; the in-tree comment explicitly records that MS link.exe does NOT skip and generates empty code ranges.**
Writer.cpp 613–616: "Skip empty section chunks. MS link.exe does not seem to do that and generates empty code ranges in some cases." So a "zero length invalid" universal rule has no source support — the pinned source names a producer that emits empty ranges, and lld's skip is a policy choice (to avoid emitting them), not a validity invariant. Empty non-section chunks (`EmptyChunk`) are not skipped at all but are harmless (size 0, `last` untouched in practice). The empty-section test (lines 58–62) confirms adding empty sections does not change ranges.

F6. **Table layout: plain array of two-u32 entries; count is emitted separately, not inline.**
`chpe_range_entry` = `StartOffset` + `Length` (u32 each); low 2 bits of StartOffset carry the type (`TypeMask = 3`), `getStart()` masks them, `getType()` returns bits (Object-COFF.h 764–773). `ECCodeMapChunk::getSize() = map.size() * sizeof(chpe_range_entry)` — no header, no inline count; the count is exported via the `__hybrid_code_map_count` absolute symbol (Writer.cpp 630–631) for the metadata `CodeMapCount` field. A reader assuming an inline count header is unsupported by this emitter.

F7. **Sorting: `arm64ec`-only, within code output sections, typed-before-untyped, ascending enum.**
`sortECChunks()` (Writer.cpp 1743–1755) applies only when the *link machine* is ARM64EC and only to `sec->isCodeSection()` sections; it stable-sorts typed chunks first by ascending `chpe_range_type`. Data output sections are never sorted (CODEMAPCM's `.testdat` keeps data-before-code input order — this is why the X64 run starts at the page-rounded 0x4000 covering the preceding data bytes). `mergeSections()` runs before `sortECChunks()` (Writer.cpp 788–789); `createECCodeMap()` runs inside `assignAddresses()` (1765), which is why `codeMap.clear()` exists (597–599).

## B. Unsupported universal rules (findings)

U1. **"Code-map entries always have nonzero Length"** — unsupported. Contradicted by F5 (source comment documents MS link.exe empty ranges). lld's skip is a policy; no pinned test exercises 0-length entries, so even as an lld-output fact it is unexercised.

U2. **"Each entry maps exactly one output section / a contiguous code region with no intervening non-code bytes"** — unsupported. Contradicted by F3 (CODEMAPMS span) and F4 (page prefix/slack inclusion).

U3. **"Membership/type derives from output-section attributes"** — unsupported. Contradicted by F1 (input header characteristics + chunk kind). A reader or profile predicate tying code-map membership to the final section characteristics would reject valid lld files.

U4. **"Tag space {0,1,2} is a universal producer invariant"** — unsupported as a universal. It is a pinned *lld-writer* fact (enum + `TypeMask=3` + masked OR). No pinned producer-side evidence covers other emitters; tag value 3 is undefined in the enum, and the reader-side `getType()` merely masks. "Named tags only" remains a conservative *profile*, not a universal validity rule.

U5. **"Global sortedness / non-overlap / page-aligned starts are universal producer contracts"** — unsupported. For lld they hold *by construction* (incremental non-overlapping RVA assignment + F7 sorting + F4 rounding); the pinned set contains no external-producer evidence, so these cannot be asserted as universal invariants.

U6. **"Same-type chunks always join a single run"** — unsupported. F3 shows any intervening untyped chunk splits a run (CODEMAPDM). Conversely, same-type chunks in *different* sections merge when adjacent (CODEMAPMS). The only consistent model is: maximal same-type runs in the flat output-section chunk iteration, split by type transitions regardless of section identity.

## C. Relation to the stopped claim (no revival)

The knowledge doc `corpus/knowledge/2026-10-23-r33-chpe-structural-profile.md` cites these two source expectations ("LLVM's empty-range comment and cross-section test") as reasons NOT to call conservative profile exclusions universal invalidity. This review confirms both citations:
- The empty-range comment (F5) names a real producer behavior (MS link.exe empty ranges), so rejecting zero-length entries on universal grounds is not source-supported; treating it as a conservative profile exclusion is.
- The cross-section test (CODEMAPMS) demonstrates lengths spanning multiple sections and gaps, so exclusions like "single-section file-backed spans only" are profile choices, not universal validity rules.

The original claim (32-row independent fixture measurement) remains STOPPED UNPROVABLE; nothing in this report replaces or revives it.

## Verification gaps

- `OutputSection::isCodeSection()` is not among the pinned captures (defined outside the pinned files); it affects only F7's sort/pad decisions, not F1–F6.
- No fresh Windows/link.exe behavior was observed (out of scope by design); all statements above are pinned-source expectations.
- Held/quarantine material untouched; no builds, tests, linters, or formatters run; no lane writes other than this Report.
