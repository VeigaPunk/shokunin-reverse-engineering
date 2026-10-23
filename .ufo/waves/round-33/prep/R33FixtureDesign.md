# R33FixtureDesign — strict CHPE structural fixtures

Seat `KaidokuR33.R33FixtureDesign`. Observation window 2026-10-23T08:11:25Z–2026-10-23T08:17:40Z. No tool installed. No mutated DLL written. No parser executed (neither a new reader nor `tools/round-32/arm64x_oracle.py` on a mutant). Oracle outcomes below are control-flow traces of that frozen source against the measured bytes. This seat did not read `R33ChpeParser` output.

Axes used: source mandate versus emitter profile, old-oracle false-accept versus exception, RVA-exact deltas, and a passing near-miss for every defensive cut.

## Reference bytes

Reference carrier `k01.dll` (the other eleven are the same layout family; do not copy k01 file offsets onto them blindly).

- Path `/fast/scratch/hyaku/kaidoku-r32/carriers/k01.dll`
- SHA-256 `2f386dde73a262a657cc385f16594afce9369e05121916a8fd44a6cc45630989` (matches `corpus/evidence/round-32/c1/carriers.tsv`)
- Size 9216 (`0x2400`). COFF machine file `0x7c` = `64 aa` (`0xAA64`). ImageBase `0x180000000`. SizeOfImage `0x9000`.

Section virtual spans (k01):

| section | VA | VirtualSize | end (exclusive) | raw ptr | raw size |
|---|---|---|---|---|---|
| .text | 0x1000 | 0x105c | 0x205c | 0x400 | 0x1200 |
| .hexpthk | 0x3000 | 0x10 | 0x3010 | 0x1600 | 0x200 |
| .rdata | 0x4000 | 0x3dc | 0x43dc | 0x1800 | 0x400 |
| .data | 0x5000 | 0x7c | 0x507c | 0x1c00 | 0x200 |
| .pdata | 0x6000 | 0x8 | 0x6008 | 0x1e00 | 0x200 |
| .a64xrm | 0x7000 | 0x10 | 0x7010 | 0x2000 | 0x200 |
| .reloc | 0x8000 | 0x6c | 0x806c | 0x2200 | 0x200 |

Load config: data-directory 10 at file `0x150` = `00 40 00 00 40 01 00 00` (RVA `0x4000`, size `0x140`). Same eight bytes on k04 and k12. Load-config `Size` at file `0x1800` = `40 01 00 00`. `CHPEMetadataPointer` at file `0x18c8` = `00 50 00 80 01 00 00 00` (VA `0x180005000`). Same pointer bytes on k04 and k12.

Metadata RVA `0x5000` (first byte of `.data`, inside VirtualSize). k01 file `0x1c00`. k04 file `0x1e00` (verified). k12 file `0x1c00`. Field deltas below are metadata-relative; absolute file offsets are k01.

k01 metadata words (little-endian): Version `2` at +0; CodeMap RVA `0x415c` at +4; CodeMapCount `3` at +8; CodeRangesToEntryPoints `0x4174` at +0x0c; RedirectionMetadata `0x7000` at +0x10; CodeRangesToEntryPointsCount `1` at +0x30; RedirectionMetadataCount `1` at +0x34; HybridImageInfoBitfield `0` at +0x58. k12's two counts are `2`, not `1`.

Code map RVA `0x415c`, file `0x195c` on k01, k04, and k12 (`.rdata` raw ptr `0x1800`). Lengths are not shared:

| | entry0 ARM64 | entry1 ARM64EC | entry2 tag 2 |
|---|---|---|---|
| k01 | `00 10 00 00 10 00 00 00` [0x1000, 0x1010) | `01 20 00 00 5c 00 00 00` [0x2000, 0x205c) | `02 30 00 00 10 00 00 00` [0x3000, 0x3010) |
| k04 | start 0x1000 len 0x40 | start 0x2000 len 0x5c | start 0x3000 len 0x10 |
| k12 | start 0x1000 len 0x10 | start 0x2000 len 0x70 | start 0x3000 len 0x20 |

k01 EC end `0x205c` equals `.text` VirtualSize end. k01 tag-2 end `0x3010` equals `.hexpthk` VirtualSize end. Next bytes at file `0x1974` are the one `chpe_code_range_entry`: `00 30 00 00 10 30 00 00 00 30 00 00` = Start `0x3000`, End `0x3010`, EntryPoint `0x3000` (the tag-2 range). Redirection at file `0x2000`: `00 30 00 00 04 20 00 00` then zeros (`0x3000 → 0x2004`). `.hexpthk` raw padding at file `0x1610` is 32 zero bytes.

## What the pinned source actually requires

Fetched 2026-10-23T08:11:41Z from `llvmorg-23.1.3` (curl `-fsSL --retry 3 --max-time 60`). Hashes:

- `lld/COFF/Writer.cpp` `229163a9be04e588b7b9c2bc6f3f6dc889138886bae660b713502a29aed587bd`
- `lld/COFF/Chunks.cpp` `550c20df652f683c20ef041e4feec63326b09ece9469fe4fe90b6ce03b79ab14`
- `lld/test/COFF/arm64ec-codemap.test` `edf6964b69261a5354d90b2fed1689c089b8600393f5a7b63e5047b42c229022`
- `llvm/lib/Object/COFFObjectFile.cpp` `444fc3fafbca8d2c047df81fd22cf295de05d2d06f7c08524464dd143b881743`
- `llvm/tools/llvm-readobj/COFFDumper.cpp` `f107c5a884bbf0b69b8af2cfa92e0b5578e1357477ec9f8aead241c26b4047a3`
- `llvm/include/llvm/Object/COFF.h` `214d3f4a186be95dee7df0d19edaf04408b45f9d243152e2a4c2fb2f762f2320`

Header (`COFF.h`): `chpe_range_type` is Arm64=0, Arm64EC=1, Amd64=2. `chpe_range_entry` is `{u32 StartOffset, u32 Length}`; low 2 bits of StartOffset are the type (`TypeMask = 3`); `getStart()` is `StartOffset & ~3`. No field says sorted, non-overlapping, length-aligned, page-aligned, or executable. `chpe_code_range_entry` is three u32s (12 bytes). `chpe_redirection_entry` is two u32s (8 bytes). Comment at the v2 tail: AuxiliaryDelayloadIAT, AuxiliaryDelayloadIATCopy, HybridImageInfoBitfield were "Added in CHPE metadata v2". `CHPEMetadataPointer` in `coff_load_configuration64` is `ulittle64_t` (a VA). The assembler input uses `.xword __chpe_metadata` and `.rva __hybrid_code_map` (`corpus/evidence/round-32/c1/inputs/loadconfig-arm64ec.s`).

Object reader (`COFFObjectFile.cpp`): `getRvaPtr` accepts only `VirtualAddress <= RVA < VirtualAddress+VirtualSize`. `getRvaAndSizeAsBytes` additionally requires `Size <= VirtualSize - OffsetIntoSection` and comments "Be careful about integer overflow." `initLoadConfigPtr` reads the pointer only when `Config->Size` covers `offsetof(CHPEMetadataPointer)+8` (0xD0) and the pointer is non-zero, then subtracts `getImageBase()`. It then `checkOffset`s the metadata struct, and, when each count is non-zero, `checkOffset`s `count * sizeof(entry)` from the resolved pointer against the **file buffer**, not against VirtualSize. It does not compare `Config->Size` to the data-directory size. It does not inspect range tags, order, overlap, or length.

Emitter (`Chunks.cpp` `ECCodeMapChunk::writeTo`): `start = first->getRVA() & ~0xfff`; `StartOffset = start | type`; `Length = last->getRVA() + last->getSize() - start`. Length has no modulo. `Writer.cpp` `createECCodeMap` skips empty `SectionChunk`s and comments that MS link.exe generates empty code ranges. `sortECChunks` sorts **within a section** by type. The upstream test's own `CODEMAP` block is not globally monotonic: ARM64EC, X64, ARM64EC, X64, and an X64 range whose end is not 4-aligned (`0x2000 - 0x2006`). `CODEMAPX` repeats ARM64EC after X64.

S099 (`corpus/evidence/round-32/sources/arm64x-pe.md` lines 50 and 64) says an Arm64X binary contains classic Arm64 and Arm64EC code and by default appears Arm64. It does not define tags or offsets. S100 remains rejected for this layout (round-32 source reopen). Tag authority for this seat is the LLVM 23.1.3 header plus the carrier bytes.

Old oracle (`tools/round-32/arm64x_oracle.py` `code_map` / `classify`): `arm64x` is machine `0xAA64` plus at least one tag 0 and one tag 1. It resolves RVAs with `max(VirtualSize, SizeOfRawData)`, ignores Version, ignores both side tables, ignores directory size, and does not test range geometry. `off(cm_rva)` runs even when `CodeMapCount` is 0. Tag 3 becomes the string `type3` and does not by itself clear `arm64x`.

Outcome words: **accepts** = `classify` returns `arm64x: true`; **clean false** = returns `arm64x: false` with no exception; **errors** = exception, no classification. "Strict" means reject the metadata as malformed, unless the row says otherwise.

## Twelve structural failures

Each delta is one change to k01. Expected strict result is malformed metadata (not a usable mixed map), except where noted.

### F1 — reserved range tag

- Delta: file `0x196c` `02` → `03` (`02 30 00 00` → `03 30 00 00`). Tag-2 start becomes RVA `0x3000` with low bits 3. Same low-byte change on k04 and k12.
- Strict: malformed. Tags are only 0, 1, 2.
- Justification: `enum chpe_range_type` has three enumerators; `TypeMask` is 3; readobj's default arm prints the raw low bits and has no name (`COFFDumper.cpp` switch). Not an `initLoadConfigPtr` error — a strict reader still cannot call it a mapped architecture.
- Legitimate counterpart: the live byte `02`, which readobj names X64 and the oracle names AMD64. Same bitfield.
- Old oracle: **accepts** (ARM64 and ARM64EC entries remain).

### F2 — range end one byte past VirtualSize, still inside SizeOfRawData

- Delta: file `0x1968` `5c 00 00 00` → `5d 00 00 00`. EC interval becomes [0x2000, 0x205d). `.text` virtual end is 0x205c; `.text` raw covers through VA 0x2200. k04 has the same EC length and the same virtual end; k12's EC length is 0x70, so this byte is k01/k04 only.
- Strict: malformed. The extra byte is file padding, not a mapped RVA.
- Justification: `getRvaPtr` section end is `VirtualAddress+VirtualSize`. Emitter length is `lastRVA+lastSize-start` (`Chunks.cpp`), so a honest length stops at mapped content. The live k01 EC length stops on that boundary.
- Legitimate counterpart: live `5c 00 00 00`, end exactly 0x205c.
- Old oracle: **accepts**.

### F3 — entire range sits in a virtual hole

- Delta: file `0x196c` `02 30 00 00` → `02 28 00 00`. Tag 2, RVA 0x2800, length unchanged 0x10, end 0x2810. Hole between `.text` end 0x205c and `.hexpthk` 0x3000. k04 shares this start byte; keep k12's length word `20 00 00 00`.
- Strict: malformed.
- Justification: `getRvaPtr` returns "RVA not found" for 0x2800. Neither virtual span contains it. Distinct from F2: F2 starts inside a section and spills; F3 never enters one.
- Legitimate counterpart: live `02 30 00 00`, start 0x3000, the first byte of `.hexpthk`.
- Old oracle: **accepts** (no range geometry check).
- Alternate one-field witness of the same geometry rule, not a second mechanism: CodeMapCount `03` → `04` at k01 file `0x1c08`. The fourth 8-byte slot is the entry-point record `00 30 00 00 10 30 00 00`, decoded as tag 0, RVA 0x3000, length 0x3010, end 0x6010 (crosses `.hexpthk`, the hole, and `.rdata`, and overlaps the real tag-2 range). Table span of 4 entries is still inside `.rdata` VirtualSize, so a span check alone passes; per-range containment fails. Oracle **accepts**.

### F4 — length addition wraps past 32 bits

- Delta: file `0x1960` `10 00 00 00` → `ff ff ff ff`. Start stays 0x1000. uint32 end = `0x1000+0xffffffff` wraps to 0x00000fff, which is below the start. k04's length word is `40 00 00 00`; the replacement is the same four `ff` bytes.
- Strict: malformed.
- Justification: `getRvaAndSizeAsBytes` says to be careful about integer overflow and uses `Size <= VirtualSize - Offset` rather than a wrapping add. Header length is a bare u32; nothing caps it.
- Legitimate counterpart: live k01 length `10 00 00 00`, end 0x1010, no wrap.
- Old oracle: **accepts** (Python int does not wrap; tags remain).

### F5 — code-map array leaves section VirtualSize but stays in the file

- Delta: CodeMapCount at metadata+8, k01 file `0x1c08`, `03 00 00 00` → `51 00 00 00` (81). Map RVA 0x415c. In-section budget: `.rdata` virtual end 0x43dc minus 0x415c = 0x280 = 80 entries. 81 entries occupy 0x288 bytes, end RVA 0x43e4. File end of that read is 0x195c+648 = 0x1be4, inside the 9216-byte file, so `checkOffset` on the file buffer passes.
- Strict: malformed.
- Justification: `getRvaAndSizeAsBytes` would reject; `initLoadConfigPtr` uses the weaker file `checkOffset`. Strict reader uses the VirtualSize span.
- Legitimate counterpart: count `50 00 00 00` (80). 80*8 = 0x280, which satisfies `Size <= VirtualSize-offset`. Oracle accepts 80 too. Live count 3 is the carrier.
- Old oracle: **accepts** 81 (first three entries still supply tags 0 and 1; the extra bytes are inside the file).

### F6 — code-map array leaves the file

- Delta: same count field `03 00 00 00` → `55 01 00 00` (341). 340 entries fit in `0x2400-0x195c` (2720 bytes, 4 bytes spare); the 341st needs 8. End file offset 0x2404.
- Strict: malformed.
- Justification: `initLoadConfigPtr` `checkOffset(CodeMapCount * sizeof(chpe_range_entry))` with `sizeof` 8.
- Legitimate counterpart: F5's count 80, or the live count 3. Distinct from F5 because the file bound fails here and the VirtualSize bound already failed earlier.
- Old oracle: **errors** (`struct.unpack_from` past the buffer). Does not accept. A strict reader should return malformed, not raise out of `classify`.

### F7 — code-range-to-entry-point array leaves VirtualSize

- Delta: count at metadata+0x30, k01 file `0x1c30`, `01 00 00 00` → `34 00 00 00` (52). Table RVA 0x4174, stride 12. Budget `0x43dc-0x4174 = 0x268`; 51*12 = 0x264 fits; 52*12 = 0x270 ends at RVA 0x43e4. File end 0x1974+624 = 0x1be4, so the LLVM file `checkOffset` still passes. k12's live count is already 2; recompute the budget per carrier.
- Strict: malformed.
- Justification: `initLoadConfigPtr` checks `CodeRangesToEntryPointsCount * sizeof(chpe_code_range_entry)` only against the file. `sizeof` the three-u32 struct is 12. Strict reader applies VirtualSize.
- Legitimate counterpart: count 51 (`33 00 00 00`), which fits, and the live count 1 whose single record equals the tag-2 interval [0x3000, 0x3010) → entry 0x3000.
- Old oracle: **accepts** (the field is never read).

### F8 — redirection array leaves `.a64xrm` VirtualSize

- Delta: count at metadata+0x34, k01 file `0x1c34`, `01 00 00 00` → `03 00 00 00`. Stride 8. VirtualSize 0x10. 2*8 = 16 fits with `Size <= VirtualSize`; 3*8 = 24 does not. Raw size 0x200 and the following bytes are zeros, so the file `checkOffset` passes. k12 already stores count 2; count 3 is still the overflow if its VirtualSize is 0x10 — measure that section before reusing the byte.
- Strict: malformed.
- Justification: same pair of checks as F7, applied to `chpe_redirection_entry` (8 bytes) and this section's VirtualSize, not `.rdata`.
- Legitimate counterpart: count 2 (`02 00 00 00`). The second record is the zeros at file `0x2008`. Span-valid. Do not additionally require the zero source RVA to land in a tag-2 range; the header does not say that.
- Old oracle: **accepts** both count 2 and count 3.

### F9 — CHPE pointer VA is outside every section

- Delta: file `0x18c8` `00 50 00 80 01 00 00 00` → `00 90 00 80 01 00 00 00` (VA `0x180009000`, RVA 0x9000 = SizeOfImage). Same file offset on k04 and k12.
- Strict: malformed.
- Justification: `initLoadConfigPtr` does `getRvaPtr(CHPEMetadataPointer - ImageBase)`. `getRvaPtr` fails with "RVA not found" when no section contains it.
- Legitimate counterpart: live VA `0x180005000`, RVA 0x5000, first byte of `.data` and inside its VirtualSize.
- Old oracle: **errors** (`off` raises `ValueError`). Does not accept.

### F10 — CHPE pointer lands in raw padding past VirtualSize

- Delta: file `0x18c8` → `10 30 00 80 01 00 00 00` (VA `0x180003010`, RVA 0x3010). `.hexpthk` virtual end is 0x3010, so `Addr < SectionEnd` is false. Raw size 0x200 still covers it. File `0x1610` is zeros.
- Strict: malformed. Do not parse the zeros as a metadata header.
- Justification: `getRvaPtr` uses VirtualSize, not SizeOfRawData. The comment about stripped sections is the opposite case (virtual beyond raw).
- Legitimate counterpart: F9's live pointer, inside VirtualSize. A zero pointer is a different, valid absence (see P8).
- Old oracle: **errors**. `off` uses `max(VirtualSize, SizeOfRawData)`, so 0x3010 resolves, the 12 zero bytes yield CodeMap RVA 0, and `off(0)` then raises. The padding must not become a successful empty map.

### F11 — data-directory size does not cover the CHPE slot

- Delta: file `0x154` `40 01 00 00` → `c0 00 00 00` (directory size 0x140 → 0xC0). Load-config `Size` at file `0x1800` stays `40 01 00 00`. The pointer occupies [0xC8, 0xD0). Directory size 0xC0 ends before that slot. Same directory bytes on k04 and k12.
- Strict: malformed inconsistency; do not consume the pointer.
- Justification: `initLoadConfigPtr` `checkOffset`s `DataEntry->Size`, then trusts `Config->Size` alone to decide whether offset 0xC8 is live. It never requires `Config->Size <= DataEntry->Size`. The slot is inside the struct the Size field claims and outside the directory.
- Legitimate counterpart: directory size exactly `d0 00 00 00` (0xD0), which covers the 8-byte pointer and is the minimum `initLoadConfigPtr` itself uses. The unmutated pair (directory size and Size both 0x140) is the carrier. Shrinking **Size** below 0xD0 is not this failure (see P9).
- Old oracle: **accepts** (directory size is ignored; Size 0x140 still passes the 0xD0 test).

### F12 — version is not 2

- Delta: metadata+0, k01 file `0x1c00`, `02 00 00 00` → `01 00 00 00`. k04 file is `0x1e00`, same four bytes. Code-map prefix is unchanged.
- Strict: not v2 metadata; do not apply the v2 tail or the ARM64EC range-type reading as if Version were 2.
- Justification: `COFF.h` marks the last three fields added in v2. `COFFDumper.cpp` prints those three only when `Version >= 2`. The object reader does not reject other versions; a strict reader of this carrier family must, because the version word selects that layout. Version 0 or 3 is the same failure (not observed on the carriers).
- Legitimate counterpart: live `02 00 00 00` on all twelve.
- Old oracle: **accepts** (the version word is unpacked and discarded).

## Positive lookalikes

Strict result for each is: metadata stays well-formed. Where the map still has tags 0 and 1 inside VirtualSize, it stays a mixed map. These are the near-misses of the cuts above, or of profile checks that must not be promoted to format rejects. Old oracle **accepts** every row except P8 and P9, which are clean false (not hybrid, no exception).

### P1 — adjacent, not overlapping (near-miss of an overlap policy)

- Delta: k01 file `0x1960` `10 00 00 00` → `00 10 00 00`. ARM64 becomes [0x1000, 0x2000). EC starts at 0x2000. Half-open, no shared RVA, both ends inside `.text`. k04/k12 ARM64 also starts at 0x1000, so the same replacement abuts EC; their previous lengths differ.
- Why it must pass: `COFF.h` does not forbid or require overlap. `initLoadConfigPtr` does not look. Rejecting `end == next.start` false-rejects a half-open map.
- Profile only, not one of the twelve: the overlapping neighbor is `10 00 00 00` → `04 10 00 00` on k01 (end 0x2004, overlaps EC by 4). Oracle accepts it. Do not score that neighbor as a format failure. If a later profile wants a single type per RVA, label it profile and keep P1 green.

### P2 — length not a multiple of 4 (near-miss of a length-alignment policy)

- Delta: k01/k04 file `0x1970` `10 00 00 00` → `06 00 00 00`. Tag-2 becomes [0x3000, 0x3006), still inside `.hexpthk` VirtualSize 0x10. k12's length is `20 00 00 00`; use `06 00 00 00` there too (0x3006 is inside a 0x20 virtual thunk section if that VirtualSize is at least 0x20 — k12's map end is 0x3020).
- Why it must pass: `Chunks.cpp` length is `lastRVA+size-start` with no modulo. Upstream `arm64ec-codemap.test` expects `0x2000 - 0x2006 X64`.

### P3 — zero length (near-miss of "empty means corrupt")

- Delta: k01/k04 file `0x1970` `10 00 00 00` → `00 00 00 00`. Interval [0x3000, 0x3000), start inside `.hexpthk`, tags 0 and 1 untouched.
- Why it must pass: `Writer.cpp` `createECCodeMap` says MS link.exe generates empty code ranges; lld skips empty section chunks and does not define a zero length as corrupt. Treat as an empty mapped interval, not malformed metadata.

### P4 — start not page-aligned (near-miss of the emitter mask)

- Delta: file `0x195c` `00 10 00 00` → `04 10 00 00` on k01, k04, and k12 (all three begin `00 10 00 00`). Tag stays 0, RVA 0x1004. k01 length 0x10 ends at 0x1014, still before EC at 0x2000 and inside `.text`. k04 length 0x40 ends at 0x1044, same relation.
- Why it must pass: `getStart()` clears only the low 2 bits, so RVA 0x1004 is representable (`0x1004 & 3 == 0`). The `& ~0xfff` mask is the emitter (`Chunks.cpp`), not the header. Requiring page alignment false-rejects a header-legal range.

### P5 — type order swapped (near-miss of a global sort policy)

- Delta: swap the first two 8-byte slots at file `0x195c`. k01 becomes `01 20 00 00 5c 00 00 00` then `00 10 00 00 10 00 00 00`, tag-2 slot unchanged. Intervals unchanged.
- Why it must pass: type lives in the low bits, not in slot index. Upstream `CODEMAP` / `CODEMAPX` already repeat ARM64EC after X64. `sortECChunks` is per section only.

### P6 — tag-2 range moved into non-executable `.rdata` (near-miss of an executable-bit policy)

- Delta: k01 file `0x196c` `02 30 00 00 10 00 00 00` → `02 40 00 00 10 00 00 00`. [0x4000, 0x4010) is inside `.rdata` VirtualSize and disjoint from [0x1000, 0x1010) and [0x2000, 0x205c). `.rdata` characteristics are initialized data, not code.
- Why it must pass: the header stores an RVA and a type, not a section flag. Strict structural result: accept. Semantic result: unknown. Not a required negative.

### P7 — one code byte inside an otherwise untouched mixed map (semantic unknown)

- Delta: file `0x1400` `11` → `10`. That file offset is RVA 0x2000, the first byte of the ARM64EC range (`11 00 00 00 88 01 80 52 …`). No metadata byte changes. Ranges stay disjoint and inside VirtualSize.
- Why it must pass: a structural reader does not decode instruction bytes. Disjoint in-bounds tags over altered or even A64-only bytes are structural-pass / semantic-unknown. The round-32 forged hybrid that overlapped [0x1000, 0x1020) with [0x1010, 0x1020) is not this case; do not reuse that overlap as the structural negative.

### P8 — count zero, and a zero CHPE pointer (near-miss of F5–F10)

- Count: k01 file `0x1c08` `03 00 00 00` → `00 00 00 00`. CodeMap RVA stays 0x415c, which still resolves. Strict: well-formed, not a hybrid, not malformed. Oracle: **clean false** (`off` succeeds, the loop does not run). A nonzero RVA with count 0 is how `initLoadConfigPtr` behaves: the `if (CodeMapCount)` guard skips the table.
- Pointer: file `0x18c8` eight bytes → `00`. Strict: CHPE absent, not malformed. Oracle: **clean false** (explicit `chpe_va == 0` return). This is the plain-ARM64 shape, not F9/F10.

### P9 — Size field stops before the CHPE slot (near-miss of F11)

- Delta: file `0x1800` `40 01 00 00` → `c8 00 00 00` (Size 0xC8). Directory size stays 0x140. Pointer bytes stay at +0xC8.
- Strict: the slot is not in the declared struct (`Size < 0xD0`). Not a hybrid. Not malformed. Do not read those eight bytes as a pointer.
- Oracle: **clean false** (`size < 0xD0` returns None).
- Distinct from F11, where Size still claims 0x140 and the directory is the short side.

## Explicit non-failures (do not add as required negatives)

- Overlap, global type order, length modulo 4, page-aligned start, executable section bit, zero length: profile or emitter habit. Positives P1–P6 are the able-to-fail controls if a counter grows one of those checks.
- Tag 2 on a real carrier is mandatory to accept. A reader that allows only tags 0 and 1 false-rejects all twelve DLLs.
- HybridImageInfoBitfield is 0 on k01 (readobj and the dword at metadata+0x58). Requiring a nonzero bitfield false-rejects the family. No bit definition in the fetched header was used to invent reserved-bit failures.
- Helpers past metadata+0x5c (six RVAs in the assembler input) are outside `struct chpe_metadata` (ends at HybridImageInfoBitfield, 0x5c bytes). Do not require them.
- On-disk machine stays `0xAA64`. `0xA64E` / `0xA641` are not in these files. Patching file `0x7c` is a COFF-machine change, not a CHPE-metadata malformation; the old oracle already returns clean false. Left out of the twelve.
- Coverage stays the twelve synthetic exported-leaf DLLs. No third-party ARM64X binary, no loader, no instruction decoder.

## Fixture-builder notes

Apply metadata-relative and RVA-relative edits after section lookup. Shared across k01/k04/k12: directory-10 at file `0x150`, load config at file `0x1800`, CHPE pointer at file `0x18c8`, code-map RVA `0x415c` at file `0x195c`. Not shared: metadata file offset (k04 is `0x1e00`), per-entry lengths, k12 side-table counts.

Suggested pairs so an all-false or no-reader control cannot ignore the near-miss: F2 with the live EC length; F5 with count 80; F7 with count 51; F8 with count 2; F11 with directory size 0xD0; F12 with the live version 2; F1 with the live `02` byte; P7 beside any tag check. Each mutant is a few bytes inside a 9216-byte file, under the 1 MiB cap. Do not execute the DLL.

## Method, pins, limits

- Bytes opened read-only: `/fast/scratch/hyaku/kaidoku-r32/carriers/k01.dll`, `k04.dll`, `k12.dll`. `sha256sum` of k01 at 2026-10-23T08:11:25Z matched the carriers table. Python `struct` unpack of those files only; no oracle process; no `llvm-readobj` on a mutant.
- Lane oracle traced: `tools/round-32/arm64x_oracle.py` `PE.code_map` (lines 79–96) and `classify` (lines 104–109).
- LLVM pin: tag `llvmorg-23.1.3`, hashes above. Installed host header `/usr/include/llvm/Object/COFF.h` matches that struct layout; the report quotes the fetched tag, not a newer git tree.
- S099 text used only for the hybrid-versus-appearance sentence. S100 not re-opened; prior reject stands.
- Limits: oracle and LLVM mutant behavior are source traces, not runs. k02–k11 section VirtualSizes were not re-measured; only k01's spans are exact, with k04/k12 checks limited to the offsets and map bytes cited. Empty-range acceptance follows the MS-link comment, not a Windows loader test. No claim score, no production fixture, no C2v3 use, held item `U064N008Hf47eb933` not opened.

Trailer: `.ufo/waves/round-33/prep/R33FixtureDesign.md`
