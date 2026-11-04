# ScoutUpxLayout — R87-C1 repair-tool assumptions vs UPX v5.2.0 source

Seat: ScoutUpxLayout (scout, read-only). Round 87, kaidoku. Subject:
`tools/round-87/upx-magic-repair.py` (sha256 prefix observed `f4ebd152495dc832`, matches the
declared f4ebd152…c49723). No production file edited. No tool installed or upgraded.

## 1. Source fetch receipts (tag v5.2.0, `https://raw.githubusercontent.com/upx/upx/v5.2.0/<path>`, curl, 2026-11-04)

| path | HTTP | bytes | sha256 |
|---|---|---|---|
| src/stub/src/include/linux.h | 200 | 19689 | 5de99480d6cfdc5df463dfb21153cee4ed3ac2509bbf0d3558855d1655a03ea9 |
| src/packhead.cpp | 200 | 13236 | 41b4a51ba4d78429241e2c970565402287fd79360445013f955e2b4cf137f37a |
| src/p_unix.cpp | 200 | 24181 | bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e |
| src/p_lx_elf.cpp | 200 | 373743 | 551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc |
| src/packer.cpp | 200 | 44586 | ab274d672d0985fa92d83e8c9c867d62ff30a1f31d2fb0b919e6d8826b03e040 |
| src/p_unix.h | 200 | 6651 | 73bd992ec0fb46022e299ec4b2cd696545412453a654573e6246034cf4881a88 |
| src/packhead.h | 200 | 3678 | 6cf2b14db8ffac097529f66628a8f1224237d5dccc285c9d320b2bf08cc87672 |
| src/conf.h | 200 | 31668 | ffdaa7190a50f375d3a62e3c60e23f70a03b97772bb4bb9584b57b53eb48962b |
| src/packmast.cpp | 200 | 9576 | 8b773e633a4849d9b7fc51ea106563436fef3b9aa5fbae1343ead850528056bf |
| src/except.cpp | 200 | 7284 | d99679925eb76f45b146de9f106c104e51f9d20b0696503c43b82d734afc7981 |
| src/work.cpp | 200 | 16730 | cee378b069899a79b2fce7ba07ec9ea3f8abc52b86c5f9e64a733b80b0aa178b |
| src/stub/src/amd64-linux.elf-main2.c | 200 | 30165 | aab8fedf4bc366e424c059407e4908bf959b1d68206c0652f53fbd22944dda0e |
| src/stub/src/amd64-linux.elf-main.c | 200 | 27515 | 98d3e56cd2db94745d3f4b029697c3bd46f5421cbd8a8389ae3f8a336448bf8b |
| src/stub/src/i386-linux.elf-main2.c | 200 | 31589 | 53e94a85612a0363481933a941d4a6b1be2c159e73e6d0dd08def77b7788672f |
| src/stub/src/amd64-linux.elf-entry.S | 200 | 16309 | e8796cfcc7f4d22b0540086df3028239c18645ff67af9f9a71849b81c04d483b |
| src/stub/src/amd64-linux.elf-fold.S | 200 | 9397 | 30b1938122bee4b2908fec249b1f14c82b27e8bd79b0834451fead2546d19988 |
| src/stub/src/amd64-expand.S | 200 | 7164 | 9b3ff31e9322b9b15c68946a0a72b89b1ed88ba72e8e5a33dd8d49b293fd1caf |

Line numbers below are 1-based lines of those exact bytes.

## 2. Assumption table

| # | Tool assumption (docstring / code) | Verdict | Source quote (path:line, ≤25 words) |
|---|---|---|---|
| A1 | PackHeader is 32 bytes for version ≥ 10, non-DOS format (`PH_SIZE = 32`) | CONFIRMED | packhead.cpp:94-100 `} else { if (format == UPX_F_DOS_COM \|\| format == UPX_F_DOS_SYS) n = 22; … else n = 32;` |
| A1b | DOS formats to exclude are `(1, 2, 3, 4)` (code: `fmt in (1, 2, 3, 4)`) | PARTLY CONTRADICTED (harmless) | conf.h:551-557 `UPX_F_DOS_COM 1 … DOS_SYS 2 … DOS_EXE 3 … DJGPP2_COFF 4 … DOS_EXEH 7 // OBSOLETE`; packhead.cpp:97 uses DOS_EXEH(7), not 4. 4 has a 32-byte header. Irrelevant because the tool requires `\x7fELF` first. |
| A2 | Header layout magic(4) version format method level u_adler c_adler u_len c_len u_file_size filter filter_cto n_mru checksum | CONFIRMED (LE, format<128) | packhead.cpp:167-170 `p[4] = version; p[5] = format; p[6] = method; p[7] = level;` · :151-152 `set_le32(p + 8, u_adler); set_le32(p + 12, c_adler);` · :143-149 `set_le32(p + 16, u_len); set_le32(p + 20, c_len); set_le32(p + 24, u_file_size); p[28] = filter; p[29] = filter_cto; … p[30] = n_mru` |
| A3 | u_file_size at PackHeader+24 (tool unpacks `<III` at +16 → u_len, c_len, u_file_size) | CONFIRMED | packhead.cpp:237-239 `u_len = get_le32(p + 16); c_len = get_le32(p + 20); u_file_size = get_le32(p + 24);` |
| A4 | checksum = sum(bytes 4..30) mod 251, EXCLUDING the magic (tool: `sum(buf[4:31]) % 251`) | CONFIRMED | packhead.cpp:62-70 `get_packheader_checksum(buf, blen) … buf += 4; blen -= 4; … c += *buf++; c %= 251;` · :182 `p[size - 1] = get_packheader_checksum(p, size - 1);` (size-1 = 31 ⇒ bytes 4..30) |
| A4b | …so a tampered header still validates | CONFIRMED in arithmetic; but UPX itself never reaches the checksum without the magic | packhead.cpp:190-192 `int boff = find_le32(…, UPX_MAGIC_LE32); if (boff < 0) return false;` (also :64 asserts magic before summing) |
| A5 | PackHeader is near EOF; tool searches last 512 bytes (`TAIL_WINDOW = 512`) | CONFIRMED in kind, NARROWER than UPX | p_unix.cpp:569-571 `small = 32 + sizeof(overlay_offset); // Allow zero-filled last page … bufsize = 2*4096 + 2*small +1;` · :586 `while (i > small && 0 == buf[--i]) { }` · p_unix.cpp:280-284 pack4 writes PackHeader then `overlay_offset` (4 bytes). Packed ELF observed: last `UPX!` at EOF-36. |
| A6 | l_info = {l_checksum, l_magic, l_lsize, l_version, l_format}; l_version/l_format equal PackHeader's | CONFIRMED | linux.h:579-585 `struct l_info … uint32_t l_checksum; uint32_t l_magic; uint16_t l_lsize; uint8_t l_version; uint8_t l_format;` · p_unix.cpp:254-257 `lp->l_magic = UPX_MAGIC_LE32; … l_version = ph.version; l_format = ph.format;` |
| A7 | p_info {p_progid, p_filesize, p_blocksize} follows l_info; p_filesize = l_magic+12; p_filesize == u_file_size | CONFIRMED | linux.h:588-592 `struct p_info // 12-byte packed program header … p_progid; p_filesize; p_blocksize;` · p_lx_elf.cpp:5476-5484 writes `linfo` then `hbuf` with `p_filesize = file_size` · p_lx_elf.cpp:7067-7069 `hdr.l.l_magic != UPX_MAGIC_LE32 … get_te32(&hdr.p.p_filesize) != ph.u_file_size` |
| A8 | b_info {sz_unc, sz_cpr, method, ftid, cto8, unused} (12 bytes) chain after p_info | CONFIRMED for version ≥ 12 | linux.h:570-576 `struct b_info { // 12-byte header … sz_unc; sz_cpr; b_method; b_ftid; b_cto8; b_unused;` · p_lx_elf.cpp:3999-4000 `overlay_offset = sz_elf_hdrs + sizeof(l_info); o_binfo = … + sizeof(l_info) + sizeof(p_info);` |
| A8b | (implicit) b_info is always 12 bytes | CONTRADICTED for ph.version ≤ 11 | p_unix.cpp:615-616 `if (ph.version <= 11) { szb_info = sizeof(bhdr.sz_unc) + sizeof(bhdr.sz_cpr); // old style` · p_lx_elf.cpp:7767-7772 (amd64 8-byte b_info) |
| A9 | Plausible block: 0 < sz_cpr ≤ sz_unc | CONFIRMED (UPX also requires sz_cpr > 5, sz_unc ≤ blocksize) | p_unix.cpp:680-682 `if (sz_unc <= 0 \|\| sz_cpr <= 5u \|\| sz_cpr > sz_unc \|\| sz_unc > blocksize) throwCantUnpack("corrupt b_info …")` |
| A10 | End-of-chain b_info: sz_unc 0, sz_cpr = magic, method/ftid/cto8/unused 0 | CONFIRMED | p_lx_elf.cpp:819-821 (Elf64::pack3) `b_info hdr; memset(&hdr, 0, sizeof(hdr)); set_le32(&hdr.sz_cpr, UPX_MAGIC_LE32); fo->write(&hdr, sizeof(hdr));` (Elf32: :620-622; generic: p_unix.cpp:320-322) · unpack check p_lx_elf.cpp:8062-8066 `if (sz_unc == 0) { … sz_cpr = get_le32(…); if (sz_cpr != UPX_MAGIC_LE32) throwCompressedDataViolation();` |
| A11 | Sentinel sits AFTER the loader (chain stops at the embedded loader, gap extents follow) | CONFIRMED | p_lx_elf.cpp:789 `total_out = super::pack3(fo, ft);  // loader follows compressed PT_LOADs` · :806 `// Then compressed gaps (including debuginfo.)` then sentinel at :816-819 |
| A12 | Executables carry 0-3 zero bytes between sentinel and PackHeader | CONFIRMED | p_lx_elf.cpp:820 `total_out = fpad4(fo, total_out);` then pack4 → p_unix.cpp:280 `writePackHeader(fo);` |
| A12b | Shared objects carry further data between sentinel and PackHeader | CONFIRMED (build-id/Shdr forwarding) | p_lx_elf.cpp:6706-6725 `forward_Shdrs(fo, &eho->ehdr); … fo->write(&shdrout, ssize); … fo->write(buildid_data, ssize1);` before :6732 `super::pack4` |
| A13 | "Get past the loader" = the same step UPX's unpacker takes | PARTLY CONTRADICTED | UPX skips DETERMINISTICALLY via e_entry/lsize: p_lx_elf.cpp:7948 `loader_offset = off_entry - sz_d_info;` · :7955 `fi->seek(up4(get_te64(&phdri[1].p_memsz)), SEEK_SET);  // past the loader` · :7960-7972 `// Loader is not at end; skip past it. … fi->seek(lsize - sz_d_info, SEEK_CUR);`. Tool instead SCANS forward for the first b_info whose chain ends in a sentinel. Closest UPX analogue is the recovery peek :7993-8009 `Getting past the loader is problematic… (method == prev_method \|\| M_NRV2B_LE32 == prev_method) && (0 == ftid) && (0 == cto8)` — UPX also accepts prev_method NRV2B; tool demands exact method equality (narrower → refusal, not misrepair). |
| A14 | l_info located by value search for u_file_size (`d.find(pack('<I', u_file_size))`) | CONFIRMED-VALID but NOT how UPX locates it | UPX uses the stored overlay_offset: p_unix.cpp:592-595 `int l = ph.buf_offset + ph.getPackHeaderSize(); … overlay_offset = get_te32(buf + i + l);` · p_lx_elf.cpp:7776-7777 `fi->seek(overlay_offset - sizeof(l_info), SEEK_SET); fi->readx(&linfo, sizeof(linfo));`. Tool ignores this exact, magic-independent anchor (4 bytes after PackHeader). |
| A15 | l_info for main executables sits right after Elf headers | CONFIRMED (shlib: at linfo_off/xct_off) | p_lx_elf.cpp:3588-3589 `3 == e_phnum … UPX_MAGIC_LE32 == get_le32(&((l_info *)&phdri[e_phnum])->l_magic)` · shlib :5475 `linfo_off = total_out;` |
| A16 | Only three `UPX!` anchors exist (PackHeader, l_info, sentinel) — "each anchor that does not read UPX! is rewritten" | CONTRADICTED for `--best` (NRV2B) packs: a 4th occurrence is loader code | Stub source amd64-linux.elf-main2.c:224-226 `if (h.sz_unc == 0) { // uncompressed size 0 -> EOF  if (h.sz_cpr != UPX_MAGIC_LE32) err_exit(2);`. Empirically the bytes `81 fa 55 50 58 21` (`cmp edx,0x21585055`) appear in the plaintext loader; see §5. Tool leaves that window tampered (by design: not an anchor). |

## 3. Layouts the tool does not handle (per source) — refuse vs misrepair

| Layout | Source evidence | Tool behaviour |
|---|---|---|
| Big-endian ELF (ppc32/ppc64/mips/armeb, formats ≥128) | packhead.cpp:244-251 BE header: `u_len = get_be32(p + 8); c_len = get_be32(p + 12); … u_file_size = get_be32(p + 24);`; conf.h:598-609 formats 129-140; p_unix.cpp:254 `l_magic = UPX_MAGIC_LE32;  // LE32 always` | REFUSES: `d[5] != 1` → "not a little-endian ELF"; also `fmt >= 128` skipped in find_packheader. No misrepair. |
| PE / Mach-O / DOS / Atari / PS1 / vmlinuz | conf.h:551-609 (W32PE 9, W64PE 36, MACH_* 29/32/34/37, DOS 1-3/7…) | REFUSES: not `\x7fELF`. (vmlinux/vmlinuz are not user ELF packs here.) |
| UPX < v10 headers (versions ≤ 9: 20/25/28-byte, no checksum) | packhead.cpp:85-93 sizes 24/20/25/28; :280 `if (version >= 10) { … checksum` | REFUSES: `version < 10` skipped → no PackHeader. |
| UPX version 10-11 with 8-byte b_info | p_unix.cpp:615-616; p_lx_elf.cpp:7765-7772 | NOT HANDLED: tool walks 12-byte b_info; [INFERENCE] chain walk/sentinel test almost surely fails → refusal; a coincidental 12-byte parse is the only misrepair path (low probability, untested). |
| `--lzma` (M_LZMA=14) and nrv2d/nrv2e | p_unix.cpp:490 `M_LZMA < hdr.b_method` (method is just a byte to the chain) | HANDLED: empirically repaired (§5). Method is only used for consistency in the walk. |
| Mixed methods across extents (gap extents NRV2B while first is other) | p_lx_elf.cpp:8008 `method == prev_method \|\| M_NRV2B_LE32 == prev_method` | Tool requires exact method equality in resume/walk → REFUSES where UPX would recover. Not observed in probe. |
| ELF32 LE (i386, arm LE, mipsel), arm64, riscv64, ppc64le | packmast.cpp:200-210 VISIT list; linux.h structs are uint32 for both classes | [INFERENCE] structurally handled (no EI_CLASS/e_machine check; structs identical). Untested here (no foreign-arch carriers). Loader-skip scan is arch-agnostic. |
| Shared libs with asl "blank extra l_info" | p_lx_elf.cpp:7780-7785 `Workaround for bug of extra linfo … if (0==lp[0] && 0==lp[1] && 0==lp[2])` | Tool value-search for p_filesize is unaffected by the blank l_info; [INFERENCE] handled. |
| Zero-filled last page (Mac code signing style padding) | p_unix.cpp:570 `// Allow zero-filled last page`, bufsize 8265 | Tool TAIL_WINDOW=512 → REFUSES if > ~480 trailing zero bytes follow overlay_offset. Refusal, not misrepair. |
| Over-tolerant PackHeader acceptance | packhead.cpp:209-211 rejects unknown formats; :277 `version == 0xff` rejected | Tool has no upper version/format-range check; guarded by checksum (1/251) + `0 < c_len <= n` (≈ n/2^32 for random bytes) → [INFERENCE] negligible false-positive risk. |

## 4. How `upx -t` / `-l` / `-d` find the PackHeader (origin of NotPackedException)

1. packmast.cpp:253-256 `PackMaster::getUnpacker(InputFile *f) … visitAllPackers(try_can_unpack, f, opt, f); … throwNotPacked();` (ELF packers listed packmast.cpp:200-210).
2. Each ELF packer: p_lx_elf.cpp:3503-3516 `PackLinuxElf64::canUnpack() … if (super::canUnpack()) { return true; }` → PackUnix.
3. p_unix.cpp:567-578 `PackUnix::canUnpack() … bufsize = 2*4096 + 2*small +1; … fi->seek(-(off_t)bufsize, SEEK_END); … return find_overlay_offset(buf);`
4. p_unix.cpp:586-590 `while (i > small && 0 == buf[--i]) { } i -= small; if (i < 0 || !getPackHeader(buf + i, bufsize - i, true)) return false;`
5. packer.cpp:531-534 `Packer::getPackHeader … if (!ph.decodePackHeaderFromBuf(…)) return false;`
6. packhead.cpp:189-192 `decodePackHeaderFromBuf … int boff = find_le32(…, UPX_MAGIC_LE32); if (boff < 0) return false;` ← a tampered PackHeader magic dies here: every packer returns false → step 1 throws.
7. except.cpp:114-117 `void throwNotPacked(const char *msg) { … msg = "not packed by UPX"; throw NotPackedException(msg);`

With PackHeader magic restored but l_info magic still tampered: p_lx_elf.cpp:7778-7791 `if (UPX_MAGIC_LE32 != get_le32(&linfo.l_magic)) { … throwCantUnpack("l_info corrupted");`. With sentinel still tampered: p_lx_elf.cpp:8065-8066 `if (sz_cpr != UPX_MAGIC_LE32) throwCompressedDataViolation();`. These three checks are exactly the tool's three anchors.

## 5. Empirical cross-check (scratch, deleted; host /usr/bin/upx 5.2.0, host /usr/bin/xxd and /usr/bin/jq — not necessarily the counter's pinned carriers)

Command shape: `upx -q <method> -o X.p X.orig`; tamper `d.replace(b'UPX!', b'\0'*4 | b'KDK!')`; `python3 -I -B upx-magic-repair.py --in X.p.Tn --out X.r.Tn --json`; `upx -q -t X.r.Tn`; `upx -q -d`.

| carrier/method | `UPX!` offsets in packed | PH method | T1 / T2 repair rc | repaired == packed | `upx -t` | `-d` == original |
|---|---|---|---|---|---|---|
| xxd `--best` | 0x22c, **0x4073**, 0x4c39, 0x4c44 | 2 (NRV2B) | 0 / 0 | **no** (0x4073 left tampered) | 0 / 0 | yes (T2) |
| jq `--best` | 0x22c, **0x2adb**, 0x36a8, 0x36b0 | 2 (NRV2B) | 0 / 0 | **no** (0x2adb left tampered) | 0 / 0 | yes (T2) |
| xxd/jq `--lzma` | 3 anchors only | 14 | 0 / 0 | yes | 0 | — |
| xxd/jq `--best --nrv2e` | 3 anchors only | 8 | 0 / 0 | yes | 0 | — |
| xxd/jq `--best --nrv2d` | 3 anchors only | 5 (NRV2D) | 0 / 0 | yes | 0 | — |

Context at xxd 0x4073: `…fa 55 50 58 21 d8 77 dd 85…` = `cmp edx, 0x21585055` (loader code; the stub's end-of-chain check, main2.c:225). The tampered packed file (`xxd.best.p.T1`) and repaired files still RUN (rc 0) because the loader only reaches that compare at sz_unc==0. Repair JSON (xxd --best T1): anchors `{packheader: 19524, l_info: 556, b_info_end: 19513}`, walk `{blocks_first: 5, resume: 18756, blocks_resumed: 4}` — resume lands past the loader, consistent with A11/A13.

## 6. Findings for the critic / L1 (frozen claim not edited)

- F1 (calibration): Every structural constant the tool uses (32-byte header, checksum 4..30 mod 251, u_file_size @+24, l_info/p_info/b_info layouts, p_filesize = l_magic+12, sentinel {0, UPX!, 0}) is confirmed verbatim by v5.2.0 source.
- F2 (coverage gap vs docstring): "Each anchor … nothing else changes" is true, but the docstring's implied claim that `UPX!` occurs only at the three anchors is false for `--best` (NRV2B) packs: a 4th `UPX!` is a loader immediate. T1/T2 tamper it; the repair does not restore it, so "recovered" ≠ byte-identical restoration of the packed file. The counter's rule (changes only inside windows now reading UPX!, `upx -t`, `upx -d` sha256, REA) does not require that, so this does not falsify R87-C1 — but a stricter arm (restored == pre-tamper packed bytes) would score 0/8 on `--best` NRV2B carriers [INFERENCE for the pinned carriers; observed for host xxd/jq].
- F3 (depth): UPX gets past the loader deterministically (e_entry − sz_d_info, then lsize; or C_BASE p_memsz). The tool's forward scan is a heuristic and is narrower than UPX's own recovery rule (exact method vs `prev_method || NRV2B`). Failure mode is refusal, not misrepair.
- F4 (depth): UPX finds l_info via overlay_offset (4 bytes after the PackHeader, magic-independent); the tool value-searches p_filesize instead. A stronger, source-faithful anchor is available and unused.
- F5: Tool refuses BE ELF, PE, Mach-O, DOS, pre-v10 headers; v10-11 8-byte b_info is unhandled (likely refusal, untested); window 512 B vs UPX 8265 B with zero-skip (refusal on large zero padding).

## Install record
None (curl, python3, /usr/bin/upx 5.2.0 already present).
