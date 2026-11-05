# ScoutUpxSrc — UPX v5.2.0 sources that bound `b_info` fields (round 89, L1 KaidokuR89)

Seat: `ScoutUpxSrc` (scout). Scope: open the UPX v5.2.0 sources that bound the
`b_info` fields for the round's SOURCES rows. No instrument was modified; no tool was
installed; no git/jj mutation was run. Only read-only `curl`, `sha256sum`, `grep` and
`git` were used, plus a scratch pack/tamper probe under
`/fast/scratch/hyaku/kaidoku-r89/ScoutUpxSrc/` (deleted before this report).

Fetch receipts (verbatim) are in `receipts/fetch-sha256.tsv` and
`receipts/fetch-receipts.json` beside this file. The sources themselves are **not**
committed and are not in the lane.

## 1. Fetch table — every URL the seat opened

| path | URL | HTTP | bytes | sha256 |
|---|---|---|---|---|
| `src/p_lx_elf.cpp` | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp` | 200 | 373743 | `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc` |
| `src/p_unix.h` | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.h` | 200 | 6651 | `73bd992ec0fb46022e299ec4b2cd696545412453a654573e6246034cf4881a88` |
| `src/packhead.h` | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packhead.h` | 200 | 3678 | `6cf2b14db8ffac097529f66628a8f1224237d5dccc285c9d320b2bf08cc87672` |
| `src/p_lx_elf.h` | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.h` | 200 | 31147 | `895da5cd72da32bf17846ef4b8088b1ed75dc35ac2506f694098bb30c90c7d89` |
| `src/headers.h` | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/headers.h` | **404** | 14 | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` (body is the literal text `404: Not Found`) |
| `src/p_unix.cpp` | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp` | 200 | 24181 | `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` |
| `src/packhead.cpp` | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packhead.cpp` | 200 | 13236 | `41b4a51ba4d78429241e2c970565402287fd79360445013f955e2b4cf137f37a` |
| `src/stub/src/include/header.S` | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/stub/src/include/header.S` | 200 | 2804 | `e9537fc2551d92ac3e141d93b02a2014db8307706815d0a62082dff4fbff6250` |
| `src/stub/src/include/linux.h` | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/stub/src/include/linux.h` | 200 | 19689 | `5de99480d6cfdc5df463dfb21153cee4ed3ac2509bbf0d3558855d1655a03ea9` |
| `src/except.cpp` | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/except.cpp` | 200 | 7284 | `d99679925eb76f45b146de9f106c104e51f9d20b0696503c43b82d734afc7981` |
| `src/bele.h` | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/bele.h` | 200 | 38863 | `e043afa4e9ad37801aa56ec57a95c0ff51a3e2878c86bc1a7e8c3336461f1595` |

Command form, verbatim, exit 0 for each:
`curl -sS -o <file> -w '%{http_code}' https://raw.githubusercontent.com/upx/upx/v5.2.0/src/<file>`

Independent corroboration of the same tree: `https://github.com/upx/upx/archive/refs/tags/v5.2.0.tar.gz`
→ HTTP 200, 2322262 bytes, sha256 `e58526f3e198164d63b99b3580dbb9a5111a02a3e4ab1b22b05add4f04c56bbc`;
the tarball copies of `p_lx_elf.cpp`, `p_lx_elf.h`, `p_unix.h`, `p_unix.cpp`, `packhead.h`
and `stub/src/include/header.S` hash **identically** to the per-file fetches above
(`551fc867…`, `895da5cd…`, `73bd992e…`, `bf83c413…`, `6cf2b14d…`, `e9537fc2…`).

`src/headers.h` is a **rejection row, not a silence**: HTTP 404, and the v5.2.0 tree
listing (`git/trees/v5.2.0?recursive=1`) contains exactly one `*headers.h*` path,
`src/util/system_headers.h` — there is no `src/headers.h` at that tag.

## 2. Located quotes (≤25 words each) with line numbers

### 2a. `src/p_lx_elf.cpp` — the `corrupt b_info` throws and the `sz_unc`/`sz_cpr` bounds

**`corrupt b_info` — the shared-object unpack path, `PackLinuxElf64::un_shlib_1`** (lines 7104–7106):

> `if (sz_block1 < sz_elf_hdrs) {`
> `    throwCantUnpack("corrupt b_info");`

(2 words; the 32-bit twin is lines 7307–7309, identical text.) Both sit inside
`PackLinuxElf64::un_shlib_1` (function opens at line 7011) / `PackLinuxElf32::un_shlib_1`
(opens 7214), immediately after the peek at lines 7102–7103 / 7305–7306:
`unsigned const sz_block1 = unpackExtent(sz_elf_hdrs, nullptr,` …

**`b_info corrupted` — the main-executable unpack path, block 0's own `b_info`** (lines 7810–7812, `PackLinuxElf64::unpack`, opens 7755):

> `if (ph.c_len > file_size_u || ph.c_len == 0 || ph.u_len == 0`
> `||  ph.u_len > orig_file_size)`
> `    throwCantUnpack("b_info corrupted");`

(18 words; 32-bit twin lines 9078–9080, the only difference being
`ph.c_len > (unsigned)file_size`). The bound reads `ph.c_len` (= `sz_cpr`) and
`ph.u_len` (= `sz_unc`), assigned two lines earlier at 7807–7808:
`ph.u_len = get_te32(&bhdr.sz_unc);` / `ph.c_len = get_te32(&bhdr.sz_cpr);`

**The end-of-chain sentinel** (lines 8060–8066, `PackLinuxElf64::unpack`):

> `unsigned const sz_unc = ph.u_len = get_te32(&bhdr.sz_unc);`
> `if (sz_unc == 0) { // uncompressed size 0 -> EOF`
> `unsigned const sz_cpr = get_le32(&bhdr.sz_cpr);`
> `if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic`

(32-bit twin: 9303–9311.) This is the sentinel the round-89 derivation law calls
"the end-of-chain sentinel": `sz_unc == 0` marks EOF and `sz_cpr` must then carry
`UPX_MAGIC_LE32`.

**The writer that makes `sz_cpr` the compressed length of block 0**
(`PackLinuxElf::pack2_shlib_overlay_write`, opens 5488; lines 5494–5495):

> `set_te32(&tmp.sz_unc, u_len);`
> `set_te32(&tmp.sz_cpr, c_len);`

**The block-end marker the walker must reach** (`PackLinuxElf32::pack3`, opens 578;
lines 619–622; the 64-bit twin at 816–819):

> `// write block end marker (uncompressed size 0)`
> `b_info hdr; memset(&hdr, 0, sizeof(hdr));`
> `set_le32(&hdr.sz_cpr, UPX_MAGIC_LE32);`

### 2b. `src/p_unix.h` — the `p_info` struct fields (`p_filesize`, `p_blocksize`)

`packed_struct(p_info)`, base `PackUnix` (lines 126–130):

> `packed_struct(p_info) { // 12-byte packed program header`
> `    NE32 p_progid;`
> `    NE32 p_filesize;`
> `    NE32 p_blocksize;`

(13 words.) The little-endian sibling is at lines 200–204 (`LE32 p_progid;` /
`LE32 p_filesize;` / `LE32 p_blocksize;`), the big-endian one at 168–171.
`NE32` is native-endianness (`src/bele.h:1092-1105`: `typedef LE32 NE32;` under
`ACC_ABI_LITTLE_ENDIAN`), so on this LE host the NE32 `p_info` is byte-identical to
the LE32 one and the on-disk order is little-endian.

`packed_struct(b_info)`, same file (lines 109–111):

> `packed_struct(b_info) { // 12-byte header before each compressed block`
> `    NE32 sz_unc;  // uncompressed_size`
> `    NE32 sz_cpr;  //   compressed_size`

(17 words.) The field **names** and their meanings (`uncompressed_size`,
`compressed_size`) are here; `src/p_unix.h` is the only one of the four assigned files
that names what `sz_cpr` means.

### 2c. `src/packhead.h` — the `b_info`/PackHeader field list

`struct PackHeader final` opens at line 37. Its stored length fields are lines 55–59:

> `unsigned u_len;`
> `unsigned c_len;`
> `unsigned u_adler;`
> `unsigned c_adler;`
> `unsigned u_file_size;`

(10 words.) `int header_checksum;` is line 66. **`packhead.h` contains no `b_info`
at all** — `grep -c b_info packhead.h` → `0`, exit 1. The PackHeader is a different
structure from `b_info`; its own source comment at line 49 points elsewhere:
`// fields stored in compressed file => see stub/src/include/header.S`.

### 2d. `src/p_lx_elf.h` — the class graph that decides the unpack path

> `class PackLinuxElf : public PackUnix`  (line 40)
> `class PackLinuxElf64 : public PackLinuxElf`  (line 315)
> `virtual void unpack(OutputFile *fo) override;`  (line 339, 64-bit; line 167, 32-bit)
> `unsigned o_binfo;  // offset to first b_info`  (line 107)

`p_lx_elf.h` names no `b_info` field and no bound: `grep -n 'b_info' p_lx_elf.h`
returns exactly one hit (line 107).

### 2e. The two bounds the claim's law actually rests on (not in the four assigned files)

`src/p_unix.cpp`, `PackUnix::unpackExtent` (opens 476) — the per-block walk every
ELF unpack calls (call sites `p_lx_elf.cpp` 7102, 7305, 7902, 7907, 8051, 9149, 9154,
9296):

> `if (sz_unc == 0 || M_LZMA < hdr.b_method) {`  (490)
> `    throwCantUnpack("corrupt b_info");`  (491)
> `if (sz_cpr > sz_unc || sz_unc > (int)blocksize)`  (496)
> `    throwCantUnpack("corrupt b_info");`  (497)

`src/p_unix.cpp:51` fixes the header stride: `methods_used(0), szb_info(sizeof(b_info))`,
and `src/p_unix.cpp:55` asserts it: `COMPILE_TIME_ASSERT(sizeof(b_info) == 12);`

`src/packhead.cpp:342-350` (`ph_decompress`) is the stage that produces the round-89
class's `compressed data violation`:

> `if (ph.u_len < ph.c_len)`  (342) → `throwCantUnpack("header corrupted");`  (343)
> `if (r != UPX_E_OK || new_len != ph.u_len)`  (349) → `throwCompressedDataViolation();`  (350)

and `src/except.cpp:122` is the text: `void throwCompressedDataViolation() { throw Exception("compressed data violation"); }`

`src/stub/src/include/header.S:59-65` is the stub's own PackHeader byte layout
(`.long 0 // 16 uncompressed len`, `// 20 compressed len`, `// 24 original file size`,
`// 28 filter id`, `// 29 filter_cto`, `// 30 filter_misc / n_mru`, `// 31 header checksum`),
which is the on-disk counterpart of `packhead.h`'s field list.

## 3. Tier-A adjudication for this lane's carriers (Linux ELF, `PackLinuxElf64`/`32`, not base `PackUnix::unpack`)

The lane's four carriers are all ELF64 x86-64 (`e_machine 62`; `e_type` 3 for jq/xxd/libz,
2 for docker-init). Their unpacking goes through `PackLinuxElf64::unpack`, because
`PackLinuxElf64amd : PackLinuxElf64Le : PackLinuxElf64 : PackLinuxElf : PackUnix`
(`p_lx_elf.h` 518/489/315/40) — i.e. the **`PackUnix` base**, so the `NE32` variants of
`p_unix.h` are the ones in force, and `PackUnixLe32` (the LE32 copy) is reached only
through `PackLinuxI386` in `src/p_lx_exc.h:41-43` (`linux.exec/i386`), a different
format. `PackUnix::unpack` (the base unpacker, `p_unix.cpp:609`) is **not** the
carriers' path; `PackUnix::unpackExtent` (the shared block walk) **is**.

| candidate | admit / reject | reason | flip condition |
|---|---|---|---|
| `src/p_lx_elf.cpp` | **ADMIT (tier A)** for the ELF-carrier `b_info` refusal and bounds | it is the carriers' own unpack override: `PackLinuxElf64::unpack` (7755) reads block 0's `b_info` (7806-7808), applies the `c_len`/`u_len` bound (7810-7812), and checks the EOF sentinel (8060-8066); the 32-bit twin is `PackLinuxElf32::unpack` (9023, 9078-9080, 9303-9311). The `corrupt b_info` throws at 7105/7308 are the shared-object variant of the same walk. **Caveat: the URL is already held twice in `corpus/SOURCES.md` (S307 and S311) and the census already prints `W04 S311 duplicate url …/p_lx_elf.cpp across scopes`** — a third row on the same URL needs `supersedes S307`/`supersedes S311` in `teaches` or a materially distinct scope, else the validator's E04/W04 machinery bites. | flip to REJECT if the carriers' format class changed to `linux.exec/i386` (`PackUnixLe32`/`PackLinuxI386`), which would make `src/p_unix.h`'s LE32 copies primary and `p_lx_elf.cpp` only secondary; flip to a *new scope* (not a new row) if the row is scoped to the ELF64-only block-0 bound rather than to the shared `b_info` refusal |
| `src/p_unix.h` | **ADMIT (tier A)** for the *meaning* of `b_info.sz_cpr`/`sz_unc` and of `p_info.p_filesize`/`p_blocksize` | it is the only one of the four assigned files that states what the fields mean: `NE32 sz_unc; // uncompressed_size` / `NE32 sz_cpr; // compressed_size` (110-111) and `NE32 p_filesize;` / `NE32 p_blocksize;` (128-129), plus the 12-byte header size. The `NE32` copy at 109-130 is the one the carriers instantiate (base `PackUnix`); the LE32 copy at 200-204 belongs to `PackUnixLe32` (`linux.exec/i386` only). **Caveat: the URL is already held as S312** (its anchor cites the LE32 copy at 200-203, which is *not* the carriers' copy) — a new row must scope the NE32/base-class copy explicitly and carry `supersedes S312` or a distinct scope. | flip to REJECT-as-primary if the lane ever targets `linux.exec/i386` or a big-endian ELF, where `p_unix.h`'s LE32/BE32 copies become the in-force ones; flip if a future UPX moves `b_info` out of `p_unix.h` |
| `src/packhead.h` | **ADMIT (tier A) but only for the PackHeader field list; REJECT for `b_info`** | `struct PackHeader final` (37) with `u_len`/`c_len`/`u_adler`/`c_adler`/`u_file_size` (55-59) and `header_checksum` (66) is the authority for the accounting bound the round-89 law uses ("the PackHeader's declared `u_len`"). But `grep -c b_info packhead.h` → **0**: the file contains no `b_info` and no `sz_cpr`/`sz_unc` at all, so any row citing it for the `b_info` field meaning is wrong. Its own comment (49) points at `stub/src/include/header.S` for the on-disk layout. **Caveat: the URL is already held as S309** — reuse S309 rather than opening a duplicate. | flip to REJECT-as-primary for the PackHeader if the on-disk layout claim is what is being made (then `src/stub/src/include/header.S` is the authority); flip to ADMIT-as-`b_info`-primary only if a future UPX version moves `b_info` into `packhead.h` |
| `src/p_lx_elf.h` | **REJECT (tier B at best) as a primary source for the field's meaning; ADMIT (tier A) for the class-graph proposition** | it names no `b_info` field and no bound (one `b_info` mention, line 107, `unsigned o_binfo;  // offset to first b_info`, which is the *linker symbol offset*, not the field layout). What it does hold is the class graph that decides the path: `class PackLinuxElf : public PackUnix` (40) and the `virtual void unpack(OutputFile *fo) override;` declarations (167, 339) — the evidence that the carriers take the ELF override and not `PackUnix::unpack`. | flip to ADMIT for the field meaning if the row's proposition is scoped to `o_binfo` / the ELF override graph rather than to `b_info`'s layout; flip to REJECT entirely if a row tries to use it for `sz_cpr`'s meaning |
| `src/headers.h` | **REJECT — HTTP 404** | the path does not exist at tag `v5.2.0`; body is the 14-byte literal `404: Not Found` (sha256 `d5558cd4…`). The upstream tree at that tag lists exactly one `*headers.h*` path, `src/util/system_headers.h`. A 404 is a recorded rejection, not a silence. | flip to ADMIT if the file appears in a later tag that the lane pins |

**Recommended new SOURCES rows for round 89** (each with a scope that does *not*
duplicate S306/S307/S309/S311/S312, and with `teaches` carrying the `supersedes Sxxx`
token the census validator requires for a same-URL row):

1. `src/p_unix.cpp` — the per-block walk bounds (`corrupt b_info` at 491/495/497/502/553)
   and the `szb_info(sizeof(b_info))` stride (51) — **not currently in the registry**
   (`grep -c 'upx/v5.2.0/src/p_unix.cpp' corpus/SOURCES.md` → 0).
2. `src/packhead.cpp` — `ph_decompress`'s `header corrupted` / `compressed data violation`
   gate (342-350). The URL is already held as S308 but with the checksum scope; a new
   scope is needed (E04 otherwise).
3. `src/stub/src/include/header.S` — the stub's on-disk PackHeader offsets (59-65) that
   `packhead.h:49` points to; **not in the registry**.
4. `src/bele.h` — `NE32` = native-endianness (1092-1105), which is what lets the NE32
   `p_unix.h` copy be read as little-endian; **not in the registry**.
5. `src/except.cpp` — the literal refusal texts (`compressed data violation`, 122);
   **not in the registry**.

## 4. Independent measurement (scratch, deleted)

Not a substitute for the L1's own receipts; recorded because it pins which upstream
line each refusal comes from.

Carriers packed with the pinned packer `/usr/bin/upx` (sha256
`cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`, `upx 5.2.0`),
then block 0's `b_info` located with the lane's own locator
(`tools/round-87/upx-magic-repair.py` `find_packheader`/`find_linfo`) and tampered:

| carrier | path taken (measured) | `sz_cpr:=0` | `sz_cpr:=stored-8` | `sz_cpr:=0xFFFFFFF0` | `sz_cpr:=sz_unc+1` |
|---|---|---|---|---|---|
| jq (ET_DYN, PIE) | main-exe, `PackLinuxElf64::unpack` | rc 1 `CantUnpackException: b_info corrupted` | rc 1 `Exception: compressed data violation` | rc 1 `CantUnpackException: b_info corrupted` | rc 1 `CantUnpackException: header corrupted` |
| libz.so.1.3.2 (ET_DYN, shlib) | shlib, `un_shlib_1` → `unpackExtent` | rc 1 `CantUnpackException: b_info corrupted` | rc 1 `Exception: compressed data violation` | rc 1 `CantUnpackException: b_info corrupted` | rc 1 `CantUnpackException: corrupt b_info` |
| docker-init (ET_EXEC) | main-exe | rc 1 `CantUnpackException: b_info corrupted` | rc 1 `Exception: compressed data violation` | rc 1 `CantUnpackException: b_info corrupted` | — |

Verbatim refusal strings, exactly as printed by `upx -t`:
`CantUnpackException: b_info corrupted`,
`Exception: compressed data violation`,
`CantUnpackException: header corrupted`,
`CantUnpackException: corrupt b_info`.

Attribution, cross-checked against the quotes above. Note the **ordering**: in
`PackLinuxElf64::unpack` the block-0 bound (7810-7812) is evaluated *before* the
shlib/main-executable split (7816-7837), so it fires for both carrier classes.

- `b_info corrupted` ← `p_lx_elf.cpp:7812` (64-bit) / `:9080` (32-bit) — the block-0
  bound `ph.c_len > file_size_u || ph.c_len == 0 || ph.u_len == 0 || ph.u_len >
  orig_file_size`. This is the message for `sz_cpr := 0` (`c_len == 0`) and for
  `sz_cpr := 0xFFFFFFF0` (`c_len > file_size_u`), on **both** jq and libz.
- `corrupt b_info` ← `p_unix.cpp:491/495/497` (the `unpackExtent` per-block walk),
  reached by the shlib carrier's `un_shlib_1` peek at `p_lx_elf.cpp:7305` — this is
  the message for libz's `sz_cpr := sz_unc+1`, because `681 > 680` trips
  `sz_cpr > sz_unc` inside the walk. The main-executable carrier (jq) never reaches
  that walk for block 0 and answers `header corrupted` instead. **The two paths
  therefore word the same field differently**, which is a scope boundary a new row
  must record.
- `compressed data violation` ← `src/packhead.cpp:350` inside `ph_decompress`
  (`r != UPX_E_OK || new_len != ph.u_len` after a truncated `upx_decompress`), reached
  from `Packer::decompress` (`src/packer.cpp:306-308`) via `decompress(ibuf, …)` at
  `p_lx_elf.cpp:7865` (main-exe) / `p_unix.cpp:511` (shlib walk). The `Exception:`
  prefix with **no** `CantUnpackException:` is `src/except.cpp:122`'s
  `throw Exception("compressed data violation")`; the other candidate site, the
  `sz_cpr != UPX_MAGIC_LE32` sentinel at `p_lx_elf.cpp:8066` / `p_unix.cpp:672`, is
  *not* the one that fires for `stored-8`, because the payload decompress fails first.
- `header corrupted` ← `src/packhead.cpp:342-343` (`if (ph.u_len < ph.c_len)`),
  because `sz_cpr := sz_unc+1` makes `ph.u_len < ph.c_len`. It is the only
  `header corrupted` **without** a digit suffix; the digit-suffixed variants
  (`header corrupted 3` etc.) are `packhead.cpp:283/286/195/229/236/246/259` and belong
  to the PackHeader-level gate, not to `b_info`.

Consistency with the round's own law: `sz_cpr` for block 0 is the **compressed length
of that block's payload** (`p_unix.h:111`, written at `p_lx_elf.cpp:5495`), and the
payload starts at `b0 + 12` (`sizeof(b_info) == 12`, asserted at `p_unix.cpp:55`;
`szb_info` at `:51`), so the *next* `b_info` candidate lies at `b0 + 12 + sz_cpr`.
That is exactly the round-89 derivation's "distance from block 0's payload start
(`b0 + 12`) to the next plausible `b_info` candidate", and the walk terminates at the
sentinel written at `p_lx_elf.cpp:621` (`sz_cpr = UPX_MAGIC_LE32`) and read back at
`p_lx_elf.cpp:8065`. The round's own repair, run against the freshly packed carriers,
derived the stored values exactly (`intact: stored 252 -> derived 252`, `201 -> 201`,
`226 -> 226`, `249 -> 249`), so the law reproduces on a fresh pack.

## 5. Known gaps / not resolved by this seat

- No row was opened for `src/conf.h` (`UPX_MAGIC_LE32 0x21585055`, line 534) — it is
  reachable from `src/bele.h`/`src/except.cpp` scope and the lane already holds the
  magic via S306 (`src/stub/src/include/linux.h:540`), so it was not fetched for a row.
- The **32-bit** `PackLinuxElf32::unpack` path was located and quoted but not
  exercised by measurement: none of the lane's four carriers is ELF32. The
  `linux.exec/i386` format (`PackLinuxI386 : PackUnixLe32`) was not measured at all.
- `src/p_unix.cpp` was fetched beyond the four assigned files because the assigned
  `p_lx_elf.cpp` alone does **not** contain the per-block `sz_cpr`/`sz_unc` bounds —
  they are in `PackUnix::unpackExtent`. Whether the L1 wants a `p_unix.cpp` row is the
  L1's call; the seat's recommendation is in §3.

## 6. Tooling

No tool was installed, upgraded or removed. The operator's `PACMAN GUARD` (all pacman
transactions paused host-wide) was respected: no `pacman`, `uv tool install`,
`cargo install`, `npm -g` or `~/.local/bin` write was attempted. Everything used was
already present: `curl`, `sha256sum`, `awk`, `grep`, `python3` (3.14), and the pinned
`/usr/bin/upx` 5.2.0.
