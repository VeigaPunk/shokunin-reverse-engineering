# Round 33 source pin — R33SourceChpe

Seat `KaidokuR33.R33SourceChpe`. Measurement window 2026-10-23T08:10:10Z–08:14:03Z (`date -u +%Y-%m-%dT%H:%M:%SZ` at first fetch and after the layout sum). Registry `corpus/SOURCES.md` was not edited. No lane source, LOG, SKILL, SCORECARD, QUALITY, or fleet file other than this report was written. No git or jj write. No tool was installed. Pacman was not used. GitHub code search returned HTTP 401 and is not evidence.

**Verdict.** At pinned LLVM `llvmorg-23.1.3`, the code-map tag is verified, not assumed: `Arm64 = 0`, `Arm64EC = 1`, `Amd64 = 2`, stored in the low 2 bits of `chpe_range_entry::StartOffset` (`TypeMask = 3`). Tag 0 is the enum name `Arm64`, and lld also uses it as the default bucket for every executable chunk whose machine is neither AMD64 nor ARM64EC. `IMAGE_SCN_MEM_EXECUTE` is `0x20000000`, a different bit from `IMAGE_SCN_CNT_CODE` (`0x20`). The object parser checks that the tables fit in the file. It does not check the tag, the version, or the execute bit.

## Revision

Annotated tag `refs/tags/llvmorg-23.1.3`, tag object `856f0005e57023e63664c560a829c620360ea1f1`, tagger Tobias Hieta, `2026-10-06T10:41:31Z`, message first line `LLVM 23.1.3`. Target commit `0d261d1ca552c95a8f007e061c787ac7132fbcbc` (committer `2026-10-06T07:38:51Z`; subject `[NFC][clang][Serialization] Fix std::set_difference sorting mismatch in ASTReader (#219053)`). That subject is the commit the tag points at, not the commit that introduced CHPE. Every file below was fetched from `llvmorg-23.1.3` and again from `0d261d1ca552c95a8f007e061c787ac7132fbcbc`; `cmp -s` reported `EQ` for all nine. `compare_fail=0`.

## Captures

Each fetch: `curl --fail --location --silent --show-error --max-time 60 --max-filesize 1048576 -o <file> -w '<file> http=%{http_code} size=%{size_download}\n' <url>`. Observed HTTP 200 and curl exit 0. All sizes are below 1 MiB. sha256 is of the saved bytes (`sha256sum`). Retained under `/fast/scratch/hyaku/kaidoku-r33/R33SourceChpe/`. Primary URLs are `https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/<path>`.

| file | path | bytes | sha256 |
|---|---|---:|---|
| Object-COFF.h | `llvm/include/llvm/Object/COFF.h` | 50493 | `214d3f4a186be95dee7df0d19edaf04408b45f9d243152e2a4c2fb2f762f2320` |
| BinaryFormat-COFF.h | `llvm/include/llvm/BinaryFormat/COFF.h` | 29118 | `a44641df4bf2ecf96bbfa86b5145c3679b043a579a5df6afba1ac2852b593339` |
| Endian.h | `llvm/include/llvm/Support/Endian.h` | 18143 | `5c74b029699e4e664f4599ef7bb731824ea04585207f57e577da44ab99425bfe` |
| COFFObjectFile.cpp | `llvm/lib/Object/COFFObjectFile.cpp` | 90275 | `444fc3fafbca8d2c047df81fd22cf295de05d2d06f7c08524464dd143b881743` |
| Chunks.h | `lld/COFF/Chunks.h` | 33785 | `09e505a28bb8aa521f1023c30b2810198e3ea89e2d578423c2c6076d6e2db3f1` |
| Chunks.cpp | `lld/COFF/Chunks.cpp` | 47770 | `550c20df652f683c20ef041e4feec63326b09ece9469fe4fe90b6ce03b79ab14` |
| Writer.h | `lld/COFF/Writer.h` | 3024 | `5e68365334681aff6f835a4dcbd0e5957499e1aac590b989c712b1edb50ff75d` |
| Writer.cpp | `lld/COFF/Writer.cpp` | 117608 | `229163a9be04e588b7b9c2bc6f3f6dc889138886bae660b713502a29aed587bd` |
| Config.h | `lld/COFF/Config.h` | 11939 | `a136e88c247ed15b716348dc02904938b5fbe129d9f02831c1c7aa8958d63bc1` |

Tag-object JSON sha256 `bd76f196972ed297ec97d92fe69d52a1418f177279b792bf57924ef11cc65903` (2363 bytes). Commit JSON sha256 `9e6f5f3db781106bcb3ac4baf4d7408dede40cbb38d477ab581725c6ba9d410c`. Word counts below are `str.split()` on the stripped source line.

## What the low 2 bits are

`llvm/include/llvm/Object/COFF.h` at this tag:

- Line 762 (13 words): `enum chpe_range_type { Arm64 = 0, Arm64EC = 1, Amd64 = 2 };`
- Line 768 (11 words, or 10 without the slashes): `// The two low bits of StartOffset contain a range type.`
- Line 769 (6 words): `static constexpr uint32_t TypeMask = 3;`
- Line 771 (9 words): `uint32_t getStart() const { return StartOffset & ~TypeMask; }`
- Line 772 (9 words): `uint16_t getType() const { return StartOffset & TypeMask; }`

`chpe_range_entry` (lines 764–773) is `StartOffset` then `Length`, each `support::ulittle32_t`. The tag lives in `StartOffset`, not in `Length`. `getStart` clears the low 2 bits; it does not shift. `getType` is those 2 bits. Named values are 0, 1, and 2. Value 3 has no enumerator and no rejection in this struct.

This is not a 1-bit ARM-versus-EC flag. Mask `3` keeps three named types.

A different record, `chpe_code_range_entry` (lines 775–779), is `StartRva`, `EndRva`, `EntryPoint` (3×u32, 12 data bytes) and has no type bits. `chpe_metadata` (lines 734–760) starts `Version`, `CodeMap`, `CodeMapCount`, then `CodeRangesToEntryPoints`. The comment on line 756 says the fields from `AuxiliaryDelayloadIAT` were added in CHPE metadata v2. The header does not say which `Version` integer that is, and it states no byte cutoff.

## How lld writes the tag

`lld/COFF/Chunks.cpp` lines 952–954, inside `ECCodeMapChunk::writeTo`:

- `uint32_t start = entry.first->getRVA() & ~0xfff;`
- `table[i].StartOffset = start | entry.type;`
- `table[i].Length = entry.last->getRVA() + entry.last->getSize() - start;`

The writer ORs the type into a 4 KiB-aligned RVA. The low 12 bits of a value lld emits are therefore only the type (0, 1, or 2). `Length` is the span from that page start through the end of the last chunk. It is not a tag, and it is not an instruction-boundary length.

Who receives which type is `Chunk::getArm64ECRangeType` (`lld/COFF/Chunks.h` lines 475–487). Line 476: `// Data sections don't need codemap entries.` Line 477 returns `std::nullopt` when `getOutputCharacteristics()` does not include `IMAGE_SCN_MEM_EXECUTE`. The switch then uses the aliases in `lld/COFF/Config.h` lines 39–42 (`AMD64` = `IMAGE_FILE_MACHINE_AMD64`, `ARM64EC` = `IMAGE_FILE_MACHINE_ARM64EC`, `ARM64` = `IMAGE_FILE_MACHINE_ARM64`, `ARM64X` = `IMAGE_FILE_MACHINE_ARM64X`):

- machine AMD64 (`0x8664`) → `Amd64` (2)
- machine ARM64EC (`0xA641`) → `Arm64EC` (1)
- `default` → `Arm64` (0)

The default includes machine ARM64 (`0xAA64`), machine ARM64X (`0xA64E`), and any other machine. Tag 0 is therefore the enum name `Arm64` and, in this emitter, the leftover bucket. It is not a positive test that the chunk's machine is ARM64. `createECCodeMap` (`Writer.cpp` lines 592–631) drops a `nullopt` type and does not emit it. Empty section chunks are skipped. Nothing in this writer stores type 3.

## Execute flag, and a stricter code-section test

`llvm/include/llvm/BinaryFormat/COFF.h`:

- Line 303 (3 words): `IMAGE_SCN_CNT_CODE = 0x00000020,`
- Line 335 (3 words): `IMAGE_SCN_MEM_EXECUTE = 0x20000000,`

Neither line mentions CHPE or a code-map entry. Machine values on lines 101–103 are `IMAGE_FILE_MACHINE_ARM64 = 0xAA64`, `IMAGE_FILE_MACHINE_ARM64EC = 0xA641`, `IMAGE_FILE_MACHINE_ARM64X = 0xA64E`.

`OutputSection::isCodeSection` (`lld/COFF/Writer.h` lines 70–73) is the conjunction of `IMAGE_SCN_CNT_CODE`, `IMAGE_SCN_MEM_READ`, and `IMAGE_SCN_MEM_EXECUTE`. `Writer::assignAddresses` (lines 1796–1803) page-aligns to 4096 on an EC range-type change only inside `isCodeSection()`. Map membership uses only the execute bit. A chunk can be eligible for a map entry without meeting `isCodeSection`.

Other uses of the same flag in these files are not the code-map definition: builtin `.text` is created with `CNT_CODE|MEM_READ|MEM_EXECUTE` (`Writer.cpp` line 1091); address-taken function symbols are marked when their section is executable (lines 2140–2144); Thumb ARM relocations set the low bit of a target in an executable section (`Chunks.cpp` lines 222–225).

## What the object parser checks

`COFFObjectFile::initLoadConfigPtr` (`llvm/lib/Object/COFFObjectFile.cpp` lines 756–799) loads CHPE metadata only on the 64-bit path. It requires `Config->Size >= offsetof(coff_load_configuration64, CHPEMetadataPointer) + sizeof(pointer)` and a nonzero pointer, resolves that value as an RVA minus the image base, then `checkOffset` of `sizeof(chpe_metadata)`. If `CodeMapCount` is nonzero, it checks that `CodeMapCount * sizeof(chpe_range_entry)` bytes are in the file. The same pattern covers the entry-point-range and redirection tables. A zero `CodeMapCount` skips the code-map check even if `CodeMap` is nonzero. No line in this function reads `CHPEMetadata->Version`, calls `getType()`, or tests `IMAGE_SCN_MEM_EXECUTE`. The 32-bit `else` branch does not load CHPE metadata. `getMachine` (Object/COFF.h lines 949–959) reports AMD64 as ARM64EC and ARM64 as ARM64X when `CHPEMetadata` is non-null. That is LLVM's reported machine, not a check that any range is mapped or executable.

## Derived sizes (not a source literal)

`support::ulittle32_t` / `ulittle64_t` are `packed_endian_specific_integral<..., unaligned>` (`Endian.h` lines 29, 33–36, 220–223, 262, 290–295). `unaligned = 1`, so `alignas(1)`. No `static_assert` in Object/COFF.h gives `sizeof` of `coff_load_configuration64` or `chpe_metadata`. Summing the field widths in the captured header, and a local replica with `alignas(1)` buffers (`c++ -std=c++17`, GCC 16.2.1 20260810, exit 0), both give:

- 64-bit `CHPEMetadataPointer` at offset 200; the parser's Size gate is 208
- 32-bit `CHPEMetadataPointer` at offset 124 (not used by `initLoadConfigPtr`)
- `chpe_metadata` 92 data bytes; the v2 tail starts at offset 80 (`AuxiliaryDelayloadIAT`)
- `chpe_range_entry` 8 data bytes; `chpe_code_range_entry` 12

No source line states the decimal 200. This does not flip S100: S100's flip requires the two Microsoft PE-format representations to document the field. These are LLVM files.

## Does / does not prove

Proves, for this tag only: the enum values and which field holds them; that lld's emitter writes `type` into those bits after clearing the low 12 bits of the RVA; that lld omits a chunk with no execute bit and tags ARM64EC as 1, AMD64 as 2, and every other machine as 0; that the object parser's CHPE check is a 64-bit in-bounds check.

Does not prove: Windows loader or Microsoft ABI behavior (S100 still rejected for that); that tag 0 was produced by machine ARM64 rather than by the default arm; that type 3 is rejected; that `Length` excludes padding or stops on an instruction; that ranges are sorted, non-overlapping, in-section, or executable; that `Version` must be 2; that a zero `CodeMapCount` means there is no map RVA; that the derived offset 200 is an LLVM-asserted constant; any linked carrier or REA result. S098 remains the assembler inputs only.

## Proposed S101 row (not written)

Do not treat this as registered. One row, status mined, kind code, tier A. `used-by` stays empty until a decision table cites it.

`| S101 | LLVM llvmorg-23.1.3 CHPE code-map tag and PE execute bit — https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/llvm/include/llvm/Object/COFF.h ; https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/llvm/include/llvm/BinaryFormat/COFF.h ; https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/lld/COFF/Chunks.h ; https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/lld/COFF/Chunks.cpp | code | A | LLVM's CHPE code-map tag, the execute-bit test lld uses before emitting a range, and the separate CNT_CODE bit; not the Windows loader, not a linked carrier, and not tag enforcement by the object parser | tag llvmorg-23.1.3 = annotated tag 856f0005e57023e63664c560a829c620360ea1f1 = commit 0d261d1ca552c95a8f007e061c787ac7132fbcbc (2026-10-06); Object/COFF.h sha256 214d3f4a186be95dee7df0d19edaf04408b45f9d243152e2a4c2fb2f762f2320 lines 762 and 768; BinaryFormat/COFF.h sha256 a44641df4bf2ecf96bbfa86b5145c3679b043a579a5df6afba1ac2852b593339 line 335; Chunks.h sha256 09e505a28bb8aa521f1023c30b2810198e3ea89e2d578423c2c6076d6e2db3f1 lines 475-486; Chunks.cpp sha256 550c20df652f683c20ef041e4feec63326b09ece9469fe4fe90b6ce03b79ab14 lines 952-954 | Low 2 bits of code-map StartOffset are Arm64=0, Arm64EC=1, Amd64=2. lld omits a chunk with no IMAGE_SCN_MEM_EXECUTE and uses tag 0 for every executable machine other than AMD64 and ARM64EC. The object parser checks the table is in-file, not that the tag is defined. | mined | 2026-10-23 | on-release | — |`

Located quote for the row, 10 words, Object/COFF.h line 768: "The two low bits of StartOffset contain a range type."

## Limits

The offsetof 200 result is a packed-layout sum plus a replica compile, not an LLVM `static_assert` and not a compiled `llvm::object::coff_load_configuration64`. `getArm64ECRangeType`'s `default` arm was read as source; it was not executed. No carrier was parsed. S100 was not re-fetched.

Report: .ufo/waves/round-33/prep/R33SourceChpe.md
