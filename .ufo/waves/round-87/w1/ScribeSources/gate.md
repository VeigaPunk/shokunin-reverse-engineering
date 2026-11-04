# Round-87 SOURCES gate draft (ScribeSources)

Opened by ScribeSources on 2026-11-04 from live fetches of the three URLs (HTTP 200 each, second fetch byte-identical; receipts in `notes.md` and `receipts/fetch_sha256.txt`). Status change for each new row: absent (no row at base `99f8b6a8979978fe02dc3c8f674ce4fdee3ab44b`) -> `mined`. Quotes are verbatim from the fetched bytes; runs of internal spaces are collapsed to one space, and `//` comment markers are kept as written.

| source / decision | URL and location | located quote (<=25 words) | scoped use | status old->new |
|---|---|---|---|---|
| S306, admit | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/stub/src/include/linux.h — accessed 2026-11-04, line 540 | `#define UPX_MAGIC_LE32 0x21585055 /* "UPX!" */` (6 tokens) | Defines the magic constant as the little-endian `UPX!` value; the header structs at lines 570, 579 and 588 carry it or sit beside it. Not the bytes of any carrier. | absent -> mined |
| S306, admit | same URL, line 579 | `struct l_info // 12-byte trailer in header for loader (offset 116)` (11 words) | Names the loader trailer whose `l_magic` field (line 582) the unpacker tests. | absent -> mined |
| S306, admit | same URL, line 582 | `uint32_t l_magic;` | The field the trailer check at `p_lx_elf.cpp` 7778 and 9046 reads. | absent -> mined |
| S306, admit | same URL, line 572 | `uint32_t sz_cpr; // compressed_size` | A `b_info` field; the end-of-file reuse is S307's line 8065, not this header's. | absent -> mined |
| S307, admit | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp — accessed 2026-11-04, line 8065 (and 9310) | `if (sz_cpr != UPX_MAGIC_LE32) // sz_cpr must be h->magic` (8 tokens) | The end-of-file block of a Linux ELF 64-bit unpack must carry the magic in `sz_cpr`; the 32-bit unpack repeats it at 9310. | absent -> mined |
| S307, admit | same URL, line 7778 (and 9046) | `if (UPX_MAGIC_LE32 != get_le32(&linfo.l_magic)) {` (7 tokens) | The loader-trailer magic check that precedes the mismatch path at 7780-7787. | absent -> mined |
| S307, admit | same URL, line 7993 (and 9239) | `// Getting past the loader is problematic, due to unintended` (9 words) | Opens the comment naming variance between released versions as the reason loader traversal is fragile; the rest of the comment is on the following lines. | absent -> mined |
| S307, admit | same URL, lines 7755 and 9023 | `void PackLinuxElf64::unpack(OutputFile *fo)` / `void PackLinuxElf32::unpack(OutputFile *fo)` | Locates the two Linux ELF unpack overrides that the S307 checks belong to. | absent -> mined |
| S308, admit | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packhead.cpp — accessed 2026-11-04, lines 62-66 | `assert(get_le32(buf) == UPX_MAGIC_LE32);` then `buf += 4;` then `blen -= 4;` | The checksum routine's first reads skip the four magic bytes before summing. | absent -> mined |
| S308, admit | same URL, line 70 | `c %= 251;` | Completes the byte-sum definition: a plain sum reduced modulo 251, returned as one byte. | absent -> mined |
| S308, admit | same URL, lines 114-115 | `assert(get_le32(p) == UPX_MAGIC_LE32);` and `if (get_le32(p + 4) != UPX_MAGIC2_LE32) {` | The writer asserts the first word is the magic and checks the second word against a separate magic. | absent -> mined |
| S308, admit | same URL, line 282 | `if (size > blen || p[size - 1] != get_packheader_checksum(p, size - 1))` | The header verifier compares the stored last byte with the checksum. | absent -> mined |

## Not admitted: `src/p_unix.cpp` (decision for L1)

Not drafted as a row. Fetched `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp` (HTTP 200, 24181 bytes, sha256 `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e`, accessed 2026-11-04). It contains the same line at 671, `if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic`, inside `PackUnix::unpack` (defined at line 609). The Linux ELF classes in `p_lx_elf.cpp` define their own `unpack` at 7755 and 9023, and the base `PackLinuxElf::unpack` at 9334 throws `internal error`, so the Linux ELF checks are the `p_lx_elf.cpp` lines above. [INFERENCE: that the ELF classes reach their own overrides rather than `PackUnix::unpack` depends on `unpack` being virtual in the header, which was not opened.] Consequence: the sibling candidate `.ufo/waves/round-87/w1/ScribeEntry/candidate/corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md`, which cites its S307 as `src/p_unix.cpp`, should re-point that locator to `src/p_lx_elf.cpp` lines 8065 and 9310. The p_unix line may be cited only as a base-class copy, with that scope stated.

## Gate line for the knowledge entry (copy-ready)

- S306: https://raw.githubusercontent.com/upx/upx/v5.2.0/src/stub/src/include/linux.h, accessed 2026-11-04; `#define UPX_MAGIC_LE32 0x21585055 /* "UPX!" */` (line 540); absent -> mined.
- S307: https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp, accessed 2026-11-04; `if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic` (lines 8065, 9310); absent -> mined.
- S308: https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packhead.cpp, accessed 2026-11-04; `buf += 4;` (line 65) inside `get_packheader_checksum`; absent -> mined.
