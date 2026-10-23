# WSourceFields — S101 field/tag statement verification (Object/COFF.h:734-773)

Reviewer seat, round 33 w1. Scope: re-open official LLVM commit
`0d261d1ca552c95a8f007e061c787ac7132fbcbc` `llvm/include/llvm/Object/COFF.h`
lines 734-773; verify the S101 located quote and each field/tag statement
against the raw source capture; distinguish tag-0 default-bucket semantics and
the separate entrypoint record. No parser runs performed. Read-only lane
observation; all scratch under `/fast/scratch/hyaku/kaidoku-r33/w1/WSourceFields/`.

## Source-access identity (retained)

- URL fetched: `https://raw.githubusercontent.com/llvm/llvm-project/0d261d1ca552c95a8f007e061c787ac7132fbcbc/llvm/include/llvm/Object/COFF.h`
- Fetched UTC: 2026-10-23T09:30Z (argv: `curl -sS -fL --max-time 60 -o Object-COFF.h <URL>`)
- Fetched sha256: `214d3f4a186be95dee7df0d19edaf04408b45f9d243152e2a4c2fb2f762f2320` (50493 bytes)
- Retained capture `corpus/evidence/round-33/sources/Object-COFF.h`: identical sha256; `cmp -s` reports byte-identical (`IDENTICAL-TO-RETAINED`).
- Pin in `.ufo/waves/round-33/source-pins.json` and `source-anchor-map.json` matches. Note: the SOURCES S101 row displays the `llvmorg-23.1.3` tag URL; the anchor map and this check use the commit-pinned URL — same revision, no discrepancy.

## Located quote check (line 768, <= 25 words)

- Raw line 768 bytes: `  // The two low bits of StartOffset contain a range type.` (verified via `cat -A`; trailing `$` newline only, no hidden characters).
- Quote `"The two low bits of StartOffset contain a range type."` is an exact substring of line 768.
- Word count: 10 (verified `len(quote.split()) == 10`). Manifest `quote-manifest.json` says 10, `<= 25`. **PASS.**

## Field/tag statements vs raw capture (lines 734-773)

| # | Statement under review | Source evidence (line) | Verdict |
|---|---|---|---|
| 1 | `chpe_metadata` begins with `Version`, `CodeMap`, `CodeMapCount`, each little-endian u32 | 734-737, all `support::ulittle32_t` | AGREE |
| 2 | CHPE v2 tail adds `AuxiliaryDelayloadIAT`, `AuxiliaryDelayloadIATCopy`, `HybridImageInfoBitfield` | 756-759, comment `// Added in CHPE metadata v2` | AGREE |
| 3 | Range type enum names 0 Arm64, 1 Arm64EC, 2 Amd64 | 762: `enum chpe_range_type { Arm64 = 0, Arm64EC = 1, Amd64 = 2 };` | AGREE |
| 4 | Range record = two u32 words, `StartOffset` then `Length` | 764-766, both `support::ulittle32_t` | AGREE |
| 5 | Type = `StartOffset & 3`; RVA/start = `StartOffset & ~3` | 769 `TypeMask = 3`; 771 `getStart() { return StartOffset & ~TypeMask; }`; 772 `getType() { return StartOffset & TypeMask; }` | AGREE — mask is named `TypeMask`, value literally 3 |
| 6 | `Length` is a separate u32; tag lives in `StartOffset`, not `Length`; `getStart` clears (does not shift) | 765-766, 771 | AGREE |
| 7 | Tag value 3 unnamed | 762 enumerates only 0/1/2; no rejection code inside the struct (764-773) | AGREE |
| 8 | No field encodes ordering, non-overlap, length-alignment, page-alignment, or executability | struct has only `StartOffset`+`Length` (764-773) | AGREE |

Precision notes (no defect): `getType()` returns `uint16_t`, `getStart()` returns
`uint32_t`; the table's "Type = StartOffset & 3" describes the mask value, not
the accessor return width. `Length` at line 766 is a plain u32 — the emitter
(Chunks.cpp:954) computes it as `last->getRVA() + last->getSize() - start` with
no modulo, so no length-alignment rule exists in either the struct or the writer.

## Tag-0 default-bucket vs enum name (required distinction)

- In `Object/COFF.h` itself tag 0 is only the **enum name** `Arm64` (line 762); the header assigns no provenance semantics.
- The default-bucket behavior is in the emitter, `Chunks.h:475-487` `Chunk::getArm64ECRangeType()`: returns `std::nullopt` when `IMAGE_SCN_MEM_EXECUTE` is absent (477-478), then `switch (getMachine())` maps `AMD64 -> Amd64` (481-482), `ARM64EC -> Arm64EC` (483-484), and **`default -> Arm64`** (485-486). Any executable chunk whose machine is neither AMD64 nor ARM64EC falls into tag 0.
- Consequence: tag 0 on disk does not affirm that the range contains ARM64 instructions; it is lld's fallback classification. The SKILL/S101 statement "Tag 0 is also lld's default machine bucket; it does not authenticate ARM64 instruction content" is **AGREE**, and the enum-name vs default-bucket distinction is real and correctly drawn.
- Supporting emitter detail: `Chunks.cpp:952-954` writes `start = getRVA() & ~0xfff` then `StartOffset = start | entry.type` — emitted low 12 bits carry only the tag; the decoder mask remains 2 bits. Page alignment is producer behavior, not a format requirement.

## Separate entrypoint record (required distinction)

- `chpe_code_range_entry` at lines 775-779 is `{StartRva, EndRva, EntryPoint}` — three `support::ulittle32_t` words (12 bytes), **no low-bit tag packing**. It is a distinct layout from `chpe_range_entry` (8 bytes, tagged `StartOffset`).
- `chpe_redirection_entry` at 781-784 is `{Source, Destination}` — two u32s, also untagged; same width as `chpe_range_entry` but different fields.
- Metadata fields `CodeRangesToEntryPoints`/`CodeRangesToEntryPointsCount` (738, 747) reference the separate table. The SKILL/knowledge statement "The separate code-range-to-entrypoint record is not the same layout" is **AGREE**.

## Findings by severity

- **Critical/major:** none.
- **Minor:** none. All checked statements agree with the raw capture.

## Residual risk and verification gaps

- Verification covers lines 734-773 plus the emitter/reader anchors cited for tag-0 semantics (Chunks.h:475-487, Chunks.cpp:944-955). Header code outside this window (e.g., `coff_load_configuration64` ending at 732, `CHPEMetadataPointer` offset use in `COFFObjectFile.cpp`) was not re-derived by this seat beyond the cited rows.
- Tag-3 handling: the header names no enumerator for 3 and contains no in-struct rejection; whether LLVM's object reader rejects tag 3 is a `COFFObjectFile.cpp` question outside this seat's window — the claim that "value 3 has no enumerator" in the header is verified, nothing more is asserted.
- "Default bucket" conclusion relies on `default:` in the Chunks.h switch (485-486); other LLVM consumers of `chpe_range_type` were not enumerated (grep-free scope kept to the assigned window plus the two cited emitter anchors).
- Single fetch instant 2026-10-23T09:30Z; byte-identity with the retained 2026-10-23 capture means both observations name the same bytes.

## Tooling

No installs or updates performed; `curl`, `sha256sum`, `cmp`, `python3`, `sed`/`cat` already present. No pacman transactions (host-wide pause observed). No parser runs, no fixture writes, no lane mutations other than this report.
