# ScoutUpxSrc — UPX v5.2.0 sources that bound `b_info` fields (round 89, L1 KaidokuR89)

Seat report: `.ufo/waves/round-89/w1/ScoutUpxSrc/report.md`
Fetch receipts: `.ufo/waves/round-89/w1/ScoutUpxSrc/receipts/fetch-sha256.tsv`,
`…/receipts/fetch-receipts.json`. Sources themselves are not committed.

## 1. Fetch (every URL opened, `curl -sS -o <file> -w '%{http_code}' <url>`, exit 0)

| path | HTTP | bytes | sha256 |
|---|---|---|---|
| `src/p_lx_elf.cpp` | 200 | 373743 | `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc` |
| `src/p_unix.h` | 200 | 6651 | `73bd992ec0fb46022e299ec4b2cd696545412453a654573e6246034cf4881a88` |
| `src/packhead.h` | 200 | 3678 | `6cf2b14db8ffac097529f66628a8f1224237d5dccc285c9d320b2bf08cc87672` |
| `src/p_lx_elf.h` | 200 | 31147 | `895da5cd72da32bf17846ef4b8088b1ed75dc35ac2506f694098bb30c90c7d89` |
| `src/headers.h` | **404** | 14 | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` (body = literal `404: Not Found`) |
| `src/p_unix.cpp` | 200 | 24181 | `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` |
| `src/packhead.cpp` | 200 | 13236 | `41b4a51ba4d78429241e2c970565402287fd79360445013f955e2b4cf137f37a` |
| `src/stub/src/include/header.S` | 200 | 2804 | `e9537fc2551d92ac3e141d93b02a2014db8307706815d0a62082dff4fbff6250` |
| `src/stub/src/include/linux.h` | 200 | 19689 | `5de99480d6cfdc5df463dfb21153cee4ed3ac2509bbf0d3558855d1655a03ea9` |
| `src/except.cpp` | 200 | 7284 | `d99679925eb76f45b146de9f106c104e51f9d20b0696503c43b82d734afc7981` |
| `src/bele.h` | 200 | 38863 | `e043afa4e9ad37801aa56ec57a95c0ff51a3e2878c86bc1a7e8c3336461f1595` |

All at `https://raw.githubusercontent.com/upx/upx/v5.2.0/…`. Corroborated independently by
the release tarball `https://github.com/upx/upx/archive/refs/tags/v5.2.0.tar.gz`
(HTTP 200, 2322262 B, sha256 `e58526f3e198164d63b99b3580dbb9a5111a02a3e4ab1b22b05add4f04c56bbc`):
the tarball copies of the six overlapping files hash **identically** to the per-file
fetches. `src/headers.h` does not exist at `v5.2.0` — the tree listing has exactly one
`*headers.h*` path, `src/util/system_headers.h`.

## 2. Located quotes (all ≤25 words, with lines)

`src/p_lx_elf.cpp`
- 7104–7106 / 7307–7309 — `throwCantUnpack("corrupt b_info");` in
  `PackLinuxElf64::un_shlib_1` (opens 7011) / `PackLinuxElf32::un_shlib_1` (7214),
  after the `unpackExtent(sz_elf_hdrs, nullptr, …)` peek at 7102–7103 / 7305–7306.
- 7810–7812 / 9078–9080 — `if (ph.c_len > file_size_u || ph.c_len == 0 || ph.u_len == 0`
  `||  ph.u_len > orig_file_size)` → `throwCantUnpack("b_info corrupted");`
  (block 0's bound; `ph.u_len`/`ph.c_len` assigned from `sz_unc`/`sz_cpr` at 7807–7808).
- 8060–8066 / 9303–9311 — the end-of-chain sentinel: `if (sz_unc == 0) { // uncompressed
  size 0 -> EOF` … `if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic`.
- 5494–5495 — `set_te32(&tmp.sz_unc, u_len);` / `set_te32(&tmp.sz_cpr, c_len);`
  (`PackLinuxElf::pack2_shlib_overlay_write`, opens 5488): `sz_cpr` **is** the compressed
  length of that block's payload.
- 619–622 / 816–819 — the block-end marker `set_le32(&hdr.sz_cpr, UPX_MAGIC_LE32);`
  that the chain walk must reach (`pack3`, opens 578 / 783).

`src/p_unix.h`
- 126–130 — `packed_struct(p_info) { // 12-byte packed program header` /
  `NE32 p_progid;` / `NE32 p_filesize;` / `NE32 p_blocksize;` (LE32 twin 200–204,
  BE32 twin 168–171).
- 109–111 — `packed_struct(b_info) { // 12-byte header before each compressed block` /
  `NE32 sz_unc;  // uncompressed_size` / `NE32 sz_cpr;  //   compressed_size`.

`src/packhead.h`
- 37 `struct PackHeader final {`; 55–59 `unsigned u_len;` … `unsigned u_file_size;`;
  66 `int header_checksum;`. **`packhead.h` contains no `b_info`** (`grep -c` → 0);
  its comment at 49 defers the on-disk layout to `stub/src/include/header.S`.

`src/p_lx_elf.h`
- 40 `class PackLinuxElf : public PackUnix`; 315 `class PackLinuxElf64 : public
  PackLinuxElf`; 339 / 167 `virtual void unpack(OutputFile *fo) override;`;
  107 `unsigned o_binfo;  // offset to first b_info` (the only `b_info` mention).

## 3. Tier-A adjudication (carriers: Linux ELF64 x86-64, `PackLinuxElf64::unpack`)

Carrier class chain: `PackLinuxElf64amd : PackLinuxElf64Le : PackLinuxElf64 :
PackLinuxElf : PackUnix` (p_lx_elf.h 518/489/315/40) → the **`NE32`** `p_unix.h`
copies are in force; the LE32 copies belong to `PackUnixLe32`, reached only by
`PackLinuxI386` (`linux.exec/i386`, `src/p_lx_exc.h:41-43`), a different format.

| candidate | verdict | reason | flip |
|---|---|---|---|
| `src/p_lx_elf.cpp` | **ADMIT A** | the carriers' own unpack override: block-0 `b_info` read (7806-7808), bound (7810-7812), sentinel (8060-8066), 32-bit twin (9078-9080, 9303-9311). URL already held twice (S307, S311); census already prints `W04 S311 duplicate url …/p_lx_elf.cpp across scopes` — a new row needs `supersedes S307`/`S311` or a materially distinct scope | REJECT if the carrier class becomes `linux.exec/i386` (`PackUnixLe32`); else scope the row to the ELF64-only block-0 bound |
| `src/p_unix.h` | **ADMIT A** | the only assigned file that states what the fields *mean* (`sz_cpr` = `compressed_size`, 111; `p_filesize`/`p_blocksize`, 128-129) and the 12-byte header size. URL already held as S312, whose anchor cites the **LE32** copy at 200-203 — not the carriers' NE32 copy — so the new scope must name the base-class copy explicitly and carry `supersedes S312` | REJECT-as-primary for a `linux.exec/i386`/BE target, where the LE32/BE32 copies become primary |
| `src/packhead.h` | **ADMIT A for the PackHeader list; REJECT for `b_info`** | `u_len`/`c_len`/`u_file_size` (55-59) are the accounting bound's fields; but the file has **no** `b_info` (grep count 0), so a row citing it for the `b_info` meaning is wrong. URL already S309 — reuse, do not duplicate | for an on-disk-layout claim, `src/stub/src/include/header.S` is the authority instead |
| `src/p_lx_elf.h` | **REJECT B for the field meaning; ADMIT A for the class graph** | names no `b_info` field and no bound (one `b_info` mention, 107, and it is the *linker symbol* offset); what it does hold is `class PackLinuxElf : public PackUnix` (40) + the `unpack` overrides (167, 339), the evidence that the carriers take the ELF override and not `PackUnix::unpack` | ADMIT if the row's proposition is scoped to `o_binfo`/the override graph rather than to `b_info`'s layout |
| `src/headers.h` | **REJECT — 404** | no such path at `v5.2.0`; 14-byte body `404: Not Found`. A recorded rejection, not a silence | ADMIT if the file appears in a later pinned tag |

**New rows the L1 may want** (URLs not currently in `corpus/SOURCES.md`; each needs its
own distinct scope and, where the URL is held, a `supersedes Sxxx` token in `teaches`):
`src/p_unix.cpp` (the per-block walk bounds `corrupt b_info` at 491/495/497/502/553 and
`szb_info(sizeof(b_info))` at 51, `COMPILE_TIME_ASSERT(sizeof(b_info) == 12)` at 55),
`src/packhead.cpp` (`ph_decompress` 342-350, new scope vs S308's checksum scope),
`src/stub/src/include/header.S` (59-65), `src/bele.h` (NE32 = native endianness,
1092-1105), `src/except.cpp` (122, the literal refusal texts).

## 4. Measured cross-check (scratch, since deleted)

Packed with the pinned `/usr/bin/upx` (sha256 `cf2f6e7c…`, `upx 5.2.0`), block 0
located with the lane's own `tools/round-87/upx-magic-repair.py` locator:

| carrier | path | `sz_cpr:=0` | `sz_cpr:=stored-8` | `sz_cpr:=0xFFFFFFF0` | `sz_cpr:=sz_unc+1` |
|---|---|---|---|---|---|
| jq (ET_DYN, PIE) | main-exe | rc 1 `CantUnpackException: b_info corrupted` | rc 1 `Exception: compressed data violation` | rc 1 `CantUnpackException: b_info corrupted` | rc 1 `CantUnpackException: header corrupted` |
| libz.so.1.3.2 (ET_DYN, shlib) | shlib | rc 1 `CantUnpackException: b_info corrupted` | rc 1 `Exception: compressed data violation` | rc 1 `CantUnpackException: b_info corrupted` | rc 1 `CantUnpackException: corrupt b_info` |
| docker-init (ET_EXEC) | main-exe | rc 1 `CantUnpackException: b_info corrupted` | rc 1 `Exception: compressed data violation` | rc 1 `CantUnpackException: b_info corrupted` | — |

Attribution: `b_info corrupted` ← `p_lx_elf.cpp:7812`/`:9080`; `corrupt b_info` ←
`p_unix.cpp:491/495/497` via the shlib peek `p_lx_elf.cpp:7305`;
`compressed data violation` ← `src/packhead.cpp:350` (via `p_lx_elf.cpp:7865` /
`p_unix.cpp:511`) with the bare `Exception:` prefix from `src/except.cpp:122`;
`header corrupted` ← `src/packhead.cpp:342-343` (the only digit-less variant; the
digit-suffixed ones at `packhead.cpp:195/229/236/246/259/283/286` are the PackHeader
gate). **The block-0 bound (7810-7812) is evaluated before the shlib/main split
(7816-7837), so it fires for both carrier classes; the two paths word the same field
differently** (`b_info corrupted` vs `corrupt b_info`) — a scope boundary a new row
must record, and a correction to the round-89 knowledge entry's S311 line, which
currently reads as if the `corrupt b_info` message were the single carrier-facing one.

The round's own repair, run on these fresh packs, derived the stored values exactly
(`intact: stored 252 -> derived 252`, `201 -> 201`, `226 -> 226`, `249 -> 249`), so the
chain law reproduces on a fresh pack.

## 5. Gaps

`src/conf.h` (magic constant) was not fetched for a row — the lane already holds the
magic via S306. The 32-bit `PackLinuxElf32::unpack` path was located and quoted but not
exercised (no ELF32 carrier in the lane). `linux.exec/i386` was not measured at all.
`src/p_unix.cpp` was opened beyond the four assigned files because `p_lx_elf.cpp` alone
does **not** contain the per-block `sz_cpr`/`sz_unc` bounds — they are in
`PackUnix::unpackExtent`.

## 6. Tooling

No tool installed, upgraded or removed. The operator's PACMAN GUARD was respected (no
pacman / `uv tool` / `cargo` / `npm -g` / `~/.local/bin` write). Everything used was
already present: `curl`, `sha256sum`, `awk`, `grep`, `python3` 3.14, and the pinned
`/usr/bin/upx` 5.2.0. No git/jj mutation was run; no file outside this seat's
directory and the scratch tree was written.
