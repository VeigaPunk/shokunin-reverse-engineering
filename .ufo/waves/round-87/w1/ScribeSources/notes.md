# ScribeSources notes — round 87 (kaidoku), seat ScribeSources (scribe, leaf)

Date of every fetch and of the registry read: 2026-11-04 (UTC session clock 2026-11-04T22:02Z). Scope: draft SOURCES rows and gate lines for R87-C1 (UPX magic-tamper repair). Candidates only; `corpus/SOURCES.md` was read and not written.

## 1. Registry schema and next id

- Schema (header line 5 of `corpus/SOURCES.md`): `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by` = 11 cells.
- Highest existing id, computed by numeric sort over `^| S[0-9]+`: **S305** (rows S300-S305 as the lane described). Next ids: **S306, S307**, and **S308** for the third document (see §4).
- Existing status vocabulary (column 9, counted over the base file): `mined` 187, `rejected` 23.
- Existing UPX rows: S269, S270, S271 only (`doc/upx-doc.txt`, `src/help.cpp`, `src/main.cpp`). No row cites `linux.h`, `p_lx_elf.cpp`, `packhead.cpp` or `p_unix.cpp`; `grep -n -i 'p_lx_elf\|linux\.h\|packhead\|upx/upx'` at base returned only S269-S271.
- A sibling candidate (`.ufo/waves/round-87/w1/ScribeEntry/candidate/corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md`) already cites S306 = linux.h (matches) and S307 = `src/p_unix.cpp` (does not match this seat's S307; see §5).

## 2. Fetch receipts (live, 2026-11-04)

Raw bytes kept in scratch (`/fast/scratch/hyaku/kaidoku-r87/ScribeSources/`), deleted before yield; the sha256 values are copied to `receipts/fetch_sha256.txt`, and the verification run to `receipts/verify_quotes.out`.

| URL (tag v5.2.0) | HTTP | bytes | sha256 | ETag (second fetch, identical bytes) |
|---|---|---|---|---|
| https://raw.githubusercontent.com/upx/upx/v5.2.0/src/stub/src/include/linux.h | 200 | 19689 | `5de99480d6cfdc5df463dfb21153cee4ed3ac2509bbf0d3558855d1655a03ea9` | `"91a92607daa23b3bd206a70ccd975c0f9562aa441737d2f4d184a7f7a10129c7"` |
| https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp | 200 | 373743 | `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc` | `"c51d13415d41b652ed0491ce53cb01efb38392e3a0cff2b8a5bbe1efe0ea1b5b"` |
| https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packhead.cpp | 200 | 13236 | `41b4a51ba4d78429241e2c970565402287fd79360445013f955e2b4cf137f37a` | `"1974f5d1cd63c833d65e2488f0739022262f6601412afa81b90a94fb6e31b583"` |
| (extra, not admitted) https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp | 200 | 24181 | `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` | not recorded |

Command used: `curl -sSL -o <file> -w "%{http_code} %{size_download}\n" <url>` then `sha256sum`. Second fetch: `curl -sSL -D <file>.hdr -o <file>` into `refetch/`; `cmp` against the first fetch: identical for all three.

Supporting fetches for the bridge check (not admitted as rows): `src/p_unix.h` (HTTP 200, 6651 B), `src/packhead.h` (HTTP 200, 3678 B) at v5.2.0. Neither defines `patchPackHeader`.

## 3. Quote location and verification

`receipts/verify_quotes.py` asserts every quote in `rows.md` / `gate.md` (and the p_unix.cpp locators used in §4-5) at its stated line (whitespace-collapsed comparison). Result: `bad= 0` over 23 located strings (`receipts/verify_quotes.out`). Line checks also done by `sed -n` and `grep -n`.

Key located lines:
- linux.h: 540 `#define UPX_MAGIC_LE32  0x21585055  /* "UPX!" */`; 570 `struct b_info`; 572 `uint32_t sz_cpr;`; 579 `struct l_info`; 582 `uint32_t l_magic;`; 588 `struct p_info`.
- p_lx_elf.cpp: 6654 `super::pack4(fo, ft);  // write PackHeader and overlay_offset`; 7755 `PackLinuxElf64::unpack`; 7778 trailer magic check; 7780-7787 blank-record workaround (`// Workaround for bug of extra linfo by some asl_pack2_Shdrs().` at 7780; `if (UPX_MAGIC_LE32 == get_le32(&linfo.l_magic)) {` at 7783; `throwCantUnpack("l_info corrupted")` in the else branch); 7993 `// Getting past the loader is problematic, due to unintended`; 8062 `if (sz_unc == 0) { // uncompressed size 0 -> EOF`; 8063 `// note: magic is always stored le32`; 8065 `if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic`; 9023 `PackLinuxElf32::unpack`; 9046 trailer check; 9239 same comment; 9302 `// check for end-of-file`; 9310 EOF check; 9334 `PackLinuxElf::unpack` throws `internal error`.
- packhead.cpp: 62-72 `get_packheader_checksum` (`assert(get_le32(buf) == UPX_MAGIC_LE32);` 64, `buf += 4;` 65, `blen -= 4;` 66, `c %= 251;` 70); 111 `PackHeader::putPackHeader`; 114 magic assert; 115 `get_le32(p + 4) != UPX_MAGIC2_LE32`; 282 verifier.
- p_unix.cpp (extra): 97-114 `PackUnix::writePackHeader` (writes `UPX_MAGIC_LE32` at buf+0 line 106, `UPX_MAGIC2_LE32` at buf+4 line 107, calls `patchPackHeader(buf, hsize)` line 110, `fo->write` line 113); 278 `PackUnix::pack4` (calls `writePackHeader` line 280); 327 caller comment; 609 `PackUnix::unpack`; 671 `if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic`.

## 4. Decisions

- **S306 (linux.h): admit.** Primary source, pinned tag, defines the magic and the header structs the repair and counter reason about. Four located quotes in gate.md. Teaches only what the header shows; the end-of-file use is cited to S307 rather than inferred here.
- **S307 (p_lx_elf.cpp): admit.** The operative Linux ELF unpack code (`PackLinuxElf64::unpack`, `PackLinuxElf32::unpack`). Carries the EOF check and the loader-variance comment the lane specified. Overlap: the identical EOF line also sits in `p_unix.cpp:671`, but the "Getting past the loader" comment is absent from p_unix.cpp (grep returned no match), and p_unix.cpp:671 is inside the base `PackUnix::unpack`.
- **S308 (packhead.cpp): admit, narrow scope — the third row is kept.** Not redundant: no other fetched file gives the checksum's byte range, and it is the only source showing that the PackHeader sum starts after the four magic bytes. Limit: the Linux ELF header write path goes `PackUnix::pack4` (p_unix.cpp:278) → `writePackHeader` (p_unix.cpp:97) → `patchPackHeader` (line 110), and `patchPackHeader` was **not located** in the fetched files (linux.h, p_lx_elf.cpp, packhead.cpp, p_unix.cpp) or the probed headers (p_unix.h, packhead.h). So whether a Linux ELF header carries this checksum is unverified; the row's scope says so, and the knowledge entry must not assert ELF checksum coverage from this row alone.
- **p_unix.cpp: not admitted as a row** (reason in gate.md, "Not admitted"). Same EOF line exists at 671 inside `PackUnix::unpack` (base class). The Linux ELF classes define their own `unpack` in p_lx_elf.cpp; `PackLinuxElf::unpack` (9334) throws `internal error`. Reaching the base copy from an ELF object would need virtual dispatch, which was not verified: `p_unix.h` and `packhead.h` were grepped for patch/checksum/putPackHeader only, and the `unpack` declaration was not inspected. Recommendation: the entry cites S307 for the ELF check.

## 5. Findings for the L1 (not repaired in any frozen file)

1. **Sibling locator mismatch.** `ScribeEntry` candidate's S307 = `src/p_unix.cpp` ("end-of-chain b_info; sz_cpr must be h->magic"). The quoted comment exists in p_unix.cpp:671, but the ELF-specific reading and the "Getting past the loader" comment are in p_lx_elf.cpp (8065/9310, 7993/9239). Re-point to p_lx_elf.cpp, or add a separately scoped p_unix row if the entry needs the base-class copy.
2. **Bridge gap for the header checksum.** `patchPackHeader` location unverified (see §4, S308). Any sentence in the entry that the Linux ELF PackHeader checksum does or does not cover the magic is `[INFERENCE]` until that routine is opened.
3. **Magic-only edit and the header sum (fact, scoped).** packhead.cpp:65 skips bytes 0-3; so a PackHeader whose only change is the `UPX!` at offset 0 keeps its checksum. Relevant to the claim's tamper class only if the ELF header carries this checksum (finding 2).
4. **Loader-trailer fallback (fact, scoped).** p_lx_elf.cpp 7778-7787: a mismatched `l_magic` triggers a blank-record re-read workaround before `throwCantUnpack("l_info corrupted")`; the other branch (7788-) was not read and is not quoted. The entry must not claim the mismatch path refuses in all cases.
5. The lane's id plan named two ids (S306, S307); S308 is needed because packhead.cpp is kept. A third id is also requested of L1 at append time; check the highest id again before appending.

## 6. Status and recheck

Every admitted row: status `mined` (absent -> mined), opened 2026-11-04, recheck `180d` (pinned tag; same cadence as S269, which pins the same tag family), used-by `corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md`. No row rejected in this seat.

## 7. Host and scratch

- No write to `corpus/SOURCES.md`, no production file, no fleet-root file, no `.ufo/state/`, no MANIFEST, no git/jj mutation. Read-only git not used.
- Scratch `/fast/scratch/hyaku/kaidoku-r87/ScribeSources/` holds the raw fetches; removed before yield (`rm -rf`), after copying receipts into `receipts/`.
- Tools: none installed.
- Files written: `rows.md`, `gate.md`, `notes.md`, `receipts/verify_quotes.py`, `receipts/verify_quotes.out`, `receipts/fetch_sha256.txt`, `receipts/refetch_headers.txt`, `DONE`; report at `.ufo/waves/round-87/w1/ScribeSources.md`.
