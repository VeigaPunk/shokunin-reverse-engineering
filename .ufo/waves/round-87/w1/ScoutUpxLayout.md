# ScoutUpxLayout — R87-C1 scout report (round 87, kaidoku)

Full evidence: `.ufo/waves/round-87/w1/ScoutUpxLayout/notes.md` (17 v5.2.0 source receipts with HTTP 200, byte count and sha256; an assumption table with path:line quotes; a list of unhandled layouts; the NotPacked trace; the empirical probe).

- **Confirmed by v5.2.0 source:** the PackHeader is 32 bytes for version ≥ 10 and non-DOS formats (packhead.cpp:94-100). The checksum is the sum of bytes 4..30 mod 251, and the magic is excluded (packhead.cpp:62-70,182). `u_file_size` sits at +24 (packhead.cpp:237-239). The l_info, p_info and b_info layouts match (linux.h:570-592). `p_filesize` equals `u_file_size` (p_lx_elf.cpp:7067-7069). The sentinel is `{0, UPX!, 0}` and is written after the loader and the gap extents (p_lx_elf.cpp:789,806,816-820).
- **Contradicted or narrower than the source:**
  - (a) UPX gets past the loader deterministically: e_entry−sz_d_info, then lsize, or the C_BASE p_memsz (p_lx_elf.cpp:7948-7972). The tool scans heuristically instead. Its method-equality rule is narrower than UPX's `prev_method || NRV2B` (p_lx_elf.cpp:8008). That leads to refusal, not misrepair.
  - (b) UPX locates l_info via `overlay_offset`, the 4 bytes after the PackHeader (p_unix.cpp:592-595; p_lx_elf.cpp:7776). This anchor does not depend on the magic, and the tool ignores it.
  - (c) b_info is only 8 bytes for ph.version ≤ 11 (p_unix.cpp:615-616). The tool does not handle that.
  - (d) The tool's DOS exclusion list `(1,2,3,4)` should be `(1,2,3,7)`. This is harmless because the tool only accepts ELF.
- **Refused layouts:** big-endian ELF, PE, Mach-O, DOS, and pre-v10 headers. The tool's 512 B tail window is narrower than UPX's 8265 B buffer, which skips trailing zeros.
- **NotPacked trace:** packmast.cpp:253-256 → p_unix.cpp:567-590 → packer.cpp:531-534 → packhead.cpp:189-192 (`find_le32(UPX_MAGIC_LE32) < 0 → false`) → except.cpp:114-117.
- **Empirical finding (host xxd/jq, not the pinned carriers):** `upx --best` picks NRV2B (method 2), and those packs contain a 4th `UPX!`. It is the loader immediate `cmp edx,0x21585055`, the stub's end-of-chain check (amd64-linux.elf-main2.c:225). The repair restores only the 3 anchors. `upx -t` and `-d` still pass, `-d` restores the original, and the binaries run. But repaired ≠ the pre-tamper packed bytes. This does not falsify the frozen rule. A stricter byte-identity arm would fail on these carriers [INFERENCE for the pinned four]. `--lzma`, `--nrv2e` and `--nrv2d` packs have only the 3 anchors and repair byte-identically.
- **Installs:** none. Scratch has been deleted.
