# ScoutUpxPack — round 90 (kaidoku), pack-side UPX v5.2.0 sources

Seat: `ScoutUpxPack` (scout). Lane `kaidoku-shokunin`. Wave `r90-w1`.
Scratch (NVMe, deleted at exit): `/fast/scratch/hyaku/kaidoku-r90/ScoutUpxPack/`.
Receipts (absolute): `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScoutUpxPack/receipts/`.

This seat is **read-only on the lane tree**. It wrote nothing outside its seat dir and its
scratch dir; it did not touch `LOG.md`, `SCORECARD.md`, `tools/round-89/`,
`corpus/lessons/round-89.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md` or `.ufo/waves/round-89/`
(read-only reads only). The proposed `SOURCES.md` row below is *text for the L1 to write*, not a write
I made. **No installs were performed** — `curl`, `python3` and `upx 5.2.0` were already present.

---

## 1. What I opened (task item 1)

All four files fetched from the tag-pinned upstream URL, then **independently cross-checked** against
the GitHub source tarball for the same tag (a second channel).

| file | HTTP | bytes | sha256 | tarball cross-check |
|---|---|---|---|---|
| `src/p_unix.cpp` | 200 | 24181 | `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` | byte-identical |
| `src/p_unix.h` | 200 | 6651 | `73bd992ec0fb46022e299ec4b2cd696545412453a654573e6246034cf4881a88` | byte-identical |
| `src/p_lx_elf.cpp` | 200 | 373743 | `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc` | byte-identical |
| `src/p_lx_elf.h` | 200 | 31147 | `895da5cd72da32bf17846ef4b8088b1ed75dc35ac2506f694098bb30c90c7d89` | byte-identical |

Tarball: `https://github.com/upx/upx/archive/refs/tags/v5.2.0.tar.gz`, HTTP 200, 2322262 bytes,
sha256 `e58526f3e198164d63b99b3580dbb9a5111a02a3e4ab1b22b05add4f04c56bbc`.
Every fetch and hash command exited 0 — `receipts/fetch-receipt.txt`, `receipts/http-status.txt`,
`receipts/sha256-fresh.txt`.

The three sha256 values for `p_unix.cpp`, `p_unix.h` and `p_lx_elf.cpp` **match the values already in
the registry** (S313, S312, S307/S311), so my bytes are the same bytes those rows were opened
against; `p_lx_elf.h` matches S314's.

### 1a. The pack-side writer of `b_info` (the answer to "where do `sz_unc`/`sz_cpr` come from")

**`PackUnix::packExtent`, `src/p_unix.cpp:335`, is the writer in force.** Exact `grep -n` lines:

```
p_unix.cpp:407:        b_info tmp;
p_unix.cpp:426:            set_te32(&tmp.sz_unc, hdr_u_len);
p_unix.cpp:427:            set_te32(&tmp.sz_cpr, hdr_c_len);
p_unix.cpp:430:            fo->write(&tmp, sizeof(tmp));
p_unix.cpp:438:        memset(&tmp, 0, sizeof(tmp));
p_unix.cpp:439:        set_te32(&tmp.sz_unc, ph.u_len);
p_unix.cpp:440:        set_te32(&tmp.sz_cpr, ph.c_len);
p_unix.cpp:449:        fo->write(&tmp, sizeof(tmp));
p_unix.cpp:456:        // write compressed data
p_unix.cpp:457:        if (ph.c_len < ph.u_len) {
p_unix.cpp:458:            fo->write(obuf, ph.c_len);
p_unix.cpp:463:        else {
p_unix.cpp:464:            fo->write(ibuf, ph.u_len);
p_unix.cpp:55:    COMPILE_TIME_ASSERT(sizeof(b_info) == 12);
```

So, per compressed block:

- the header is a 12-byte `b_info` (`p_unix.h:109-116`; `COMPILE_TIME_ASSERT(sizeof(b_info) == 12)`
  at `p_unix.cpp:55`);
- `sz_unc` is the **uncompressed** length the compressor was handed (`ph.u_len`, line 439) — for the
  first block of an extent it is the Elf-header length instead (`hdr_u_len`, line 426);
- `sz_cpr` is the **compressed** length (`ph.c_len`, line 440; `hdr_c_len`, line 427);
- the 12-byte header is written at line 449 and is immediately followed by **exactly `sz_cpr` bytes**
  of payload: line 458 writes `ph.c_len` bytes when compressed, and line 464 writes `ph.u_len` bytes
  in the incompressible branch — where `ph.c_len` was forced equal to `ph.u_len` at line 400, so the
  byte count written still equals `sz_cpr`. **Nothing is written between the header and its payload
  and nothing is written between a payload and the next header.** That is the whole pack-side
  geometry: successor offset = block offset + 12 + `sz_cpr`, with no padding term.

`p_unix.cpp:335` is the *only* definition of `PackUnix::packExtent` in the whole v5.2.0 tree
(`grep -rn "::packExtent" tree/upx-5.2.0/src/` → 5 hits: 4 comments in `p_lx_elf.cpp` + this one
definition; exit 0) and no header declares an override (only the virtual at `p_unix.h:82`). So the
base-class body is what packs the carriers. `receipts/grep-packExtent-tree.txt`, `receipts/scope-probe.txt`.

### 1b. What ends the chain — and a scope correction the L1 needs

The end-of-compression sentinel is a `b_info` with `sz_unc == 0` and `sz_cpr == UPX_MAGIC_LE32`
(`0x21585055`, `conf.h:534`). **Where it is written depends on the class, and the generic Unix site
is dead for these carriers:**

```
p_unix.cpp:318:    if (pack2(fo, ft)) {
p_unix.cpp:319:        // write block end marker (uncompressed size 0)
p_unix.cpp:320:        b_info hdr; memset(&hdr, 0, sizeof(hdr));
p_unix.cpp:321:        set_le32(&hdr.sz_cpr, UPX_MAGIC_LE32);
p_unix.cpp:322:        fo->write(&hdr, sizeof(hdr));
```
…is inside `PackUnix::pack` (`p_unix.cpp:287`), guarded by `pack2` returning nonzero. But
`PackLinuxElf64::pack2` **returns 0** — `p_lx_elf.cpp:6080: return 0;  // omit end-of-compression bhdr for now`
(32-bit twin `p_lx_elf.cpp:5802`) — so for the ELF carriers the in-force end marker is

```
p_lx_elf.cpp:816:    // write block end marker (uncompressed size 0)
p_lx_elf.cpp:817:    b_info hdr; memset(&hdr, 0, sizeof(hdr));
p_lx_elf.cpp:818:    set_le32(&hdr.sz_cpr, UPX_MAGIC_LE32);
p_lx_elf.cpp:819:    fo->write(&hdr, sizeof(hdr));
```
(32-bit twin `p_lx_elf.cpp:621-622`.)

**Also dead for the carriers:** `PackUnix::pack2` (`p_unix.cpp:150`) has its own `b_info` writer at
lines 211-229 (`set_te32(&blk_info.sz_unc, ph.u_len)` 213, `set_te32(&blk_info.sz_cpr, ph.c_len)`
214, `fo->write(&blk_info, sizeof(b_info))` 220, payload 225/229), but `pack2` is declared
`virtual int  pack2(OutputFile *, Filter &);` at `p_unix.h:65` and is **overridden** by
`PackLinuxElf32::pack2` (`p_lx_elf.cpp:5684`) and `PackLinuxElf64::pack2` (`p_lx_elf.cpp:5955`).
So `p_unix.cpp:150-243` does not run for these carriers; `p_unix.cpp:335-469` does.

### 1c. The shared-object path writes its first `b_info` in `p_lx_elf.cpp`, not `p_unix.cpp`

```
p_lx_elf.cpp:5492:    b_info tmp;
p_lx_elf.cpp:5494:    set_te32(&tmp.sz_unc, u_len);
p_lx_elf.cpp:5495:    set_te32(&tmp.sz_cpr, c_len);
p_lx_elf.cpp:5498:    fo->write(&tmp, sizeof(tmp));   total_out += sizeof(tmp);
p_lx_elf.cpp:5500:    fo->write(mb, c_len); total_out += c_len;
```
(`PackLinuxElf::pack2_shlib_overlay_write`, called at `p_lx_elf.cpp:5889` with
`u_len = sz_elf_hdrs` from line 5855.) Same 12-then-`sz_cpr`-bytes geometry, different file.

---

## 2. Measured confirmation (independent of the lane's tools)

Packer: `/usr/bin/upx`, sha256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969` —
**matches the round-90 pin** in `.ufo/waves/round-90/claims.json` exactly. `upx --version` → `upx 5.2.0`.
Command: `upx --best -o <out> <carrier>` on copies of the four pinned carriers (their own sha256 values
match the battery's `CARRIERS` table: jq `e815667…7806`, xxd `7b1e5d0c…3ae65`, libz `6c78c5e5…5ca9`,
docker-init `0bd49c8d…e115`). Walker: my own two-segment walk (b0 = `l_magic`+20, step 12+`sz_cpr`).

### 2a. Block 0's `sz_unc` is predicted by the source formula, on all four carriers

`receipts/block0-prediction.txt`:

| carrier | phnum | predicted `64 + phnum*56` | measured block0 `sz_unc` | match |
|---|---|---|---|---|
| jq | 15 | 904 | 904 | yes |
| xxd | 15 | 904 | 904 | yes |
| docker-init | 12 | 736 | 736 | yes |
| libz | 11 | 680 | 680 | yes |

The predicted value is `hdr_u_len = sizeof(Elf64_Ehdr) + sz_phdrs` (`p_lx_elf.cpp:6008`) for the
main-program/PIE carriers and `sz_elf_hdrs` (`p_lx_elf.cpp:4316`, `5855`) for the shared object. This
grounds round-89's block-0 law in the packer's own arithmetic rather than in a search.

### 2b. The chain is contiguous, and the successor fixes the previous `sz_cpr`

jq, segment 1 (each step verified `next == off + 12 + sz_cpr`):

```
0x240 sz_unc=904  sz_cpr=252  -> 0x348
0x348 sz_unc=5408 sz_cpr=1651 -> 0x9c7
0x9c7 sz_unc=9561 sz_cpr=4758 -> 0x1c69
0x1c69 sz_unc=5528 sz_cpr=2626 -> 0x26b7
0x26b7 sz_unc=1184 sz_cpr=174  -> 0x2771
```

Derivation check on the interior block the class tampers: block at `0x9c7`, stored `sz_cpr = 4758`,
true successor at `0x1c69`; `0x1c69 − (0x9c7 + 12) = 4758` — the stored value, exactly. With the
stored value overwritten by +7 the walk lands at `0x1c70`, 7 bytes past the true successor
(`receipts/chain-measurement.txt`).

`upx -t` on both tampers (jq block2, `stored−7` and `stored+7`) → `Exception: compressed data
violation`, rc 1; the intact file → `[OK]`, rc 0. The message text is `except.cpp:122`
(`throw Exception("compressed data violation")`). [inference] the ELF64 end-of-file check at
`p_lx_elf.cpp:8062-8066` (`sz_unc == 0` → `sz_cpr` must be `UPX_MAGIC_LE32`, else
`throwCompressedDataViolation()`) is one route to that text after a desynchronised walk; I did not
instrument which branch fires, so I report the measured message, not the branch.

### 2c. The chain is **two** segments, split by the loader — this is what "first contiguous segment" means

jq: segment 1 = five blocks ending at `0x2771`, where the bytes are `00 00 00 00 | 00 00 00 40 …`
(`sz_unc == 0` but `sz_cpr == 0x40000000`, **not** the magic) — i.e. the loader, not an end marker.
Segment 2 = four blocks `0x33ac…0x33fe`, then the real end marker at `0x36a4`
(`00 00 00 00 55 50 58 21 00 00 00 00` → `sz_unc == 0`, `sz_cpr == UPX_MAGIC_LE32`), then the
PackHeader's own `UPX!` at `0x36b0`. The loader is written by `PackUnix::pack3`
(`p_unix.cpp:262`, `fo->write(p, lsize)` at 274) via `p_lx_elf.cpp:789`
(`total_out = super::pack3(fo, ft);  // loader follows compressed PT_LOADs`), and the gap blocks come
after it from `packExtent` at `p_lx_elf.cpp:813`. The chain therefore resumes after the loader.

Accounted `u_len`, measured the same way the round-90 law accounts it:

- jq: segment 1 = 22585, segment 2 = 8215 → **30800 = `p_filesize`**, the whole file.
- libz: segment 1 = 87421, segment 2 = 11171 → **98592 of 108560**. This **reproduces the plan's
  declared limit exactly** (the plan says libz's chain accounts 98,592 of 108,560 `u_len`), which is
  why libz is a `P2`/`P3`-only carrier: the shared-object layout leaves 9968 bytes unaccounted.

`receipts/chain-measurement.txt`, `receipts/scope-probe.txt`.

---

## 3. Re-opening S311 and S312 (task item 2)

Both rows' anchors re-verified line-by-line against the fetched bytes.

### S311 — `src/p_lx_elf.cpp`, the shared-object unpacker block-walk refusal — **scope confirmed, anchor has two line slips**

Scope claim ("the `un_shlib_1` unpack paths' `unpackExtent` peek and its `corrupt b_info` refusal,
for `PackLinuxElf64` and `PackLinuxElf32`") is **correct**: `PackLinuxElf64::un_shlib_1` at
`p_lx_elf.cpp:7011` and `PackLinuxElf32::un_shlib_1` at `7214`; the `l_info`/`p_info`/`b_info` header
read at `7060-7074`; the `unpackExtent(sz_elf_hdrs, …)` peek at `7102` (32-bit `7305`); the
`throwCantUnpack("corrupt b_info")` at `7105` (32-bit `7308`).

Two line numbers in the S311 anchor cell do not match the bytes:

| S311 anchor says | the bytes are at | what is actually there |
|---|---|---|
| "`p_filesize` cross-checked against `ph.u_file_size` **line 7067**" | **7069** | `7067` is `if (hdr.l.l_magic != UPX_MAGIC_LE32`; the `p_filesize` comparison is `7069: ||  get_te32(&hdr.p.p_filesize) != ph.u_file_size` |
| "the `unpackExtent(sz_elf_hdrs, …)` peek **line 7098**" | **7102** | `7098-7099` are comment lines ("will just decompress it all. For new style…"); the call is `7102: unsigned const sz_block1 = unpackExtent(sz_elf_hdrs, nullptr,` |

The quoted text and the scope are right; only the two line pointers are off (by 2 and 4). This is a
routed defect in an existing row's anchor, so under `CORPUS.md` rule 2 / QUALITY 93 it closes by a
**new `supersedes S311 —` row**, not by editing S311 in place. I did not write it (read-only seat); the
L1 owns that write.

### S312 — `src/p_unix.h`, the NE32 `p_info`/`b_info`/`l_info` layout — **scope confirmed, one wording precision item**

Scope claim confirmed line-by-line:

```
p_unix.h:109:    packed_struct(b_info) { // 12-byte header before each compressed block
p_unix.h:110:        NE32 sz_unc;  // uncompressed_size
p_unix.h:111:        NE32 sz_cpr;  //   compressed_size
p_unix.h:118:    packed_struct(l_info) { // 12-byte trailer in header for loader
p_unix.h:126:    packed_struct(p_info) { // 12-byte packed program header
p_unix.h:127:        NE32 p_progid;
p_unix.h:128:        NE32 p_filesize;
p_unix.h:129:        NE32 p_blocksize;
```

and the class chain that makes the **NE32** copy the one in force for the carriers is
`p_lx_elf.h:518` `class PackLinuxElf64amd : public PackLinuxElf64Le` → `489`
`class PackLinuxElf64Le : public PackLinuxElf64` → `315` `class PackLinuxElf64 : public PackLinuxElf`
→ `40` `class PackLinuxElf : public PackUnix`; the LE32 twin is `p_unix.h:183/192/200` in
`PackUnixLe32` (`p_unix.h:176`), reached only via `PackLinuxI386 : public PackUnixLe32`
(`p_lx_exc.h:41-43`). S312's scope text is right on every point.

**One wording precision item.** S312's `teaches` cell says "the locator finds the PackHeader's
`u_file_size` at `l_info + 12` and why `b0` is `l_info + 20`". That arithmetic is correct and my
measurement reproduces it, **but "l_info" there denotes the `l_magic` *word* position** (the round-89
tool's variable `m`), not the start of the `l_info` *struct*. Measured on jq: `l_magic` at `0x22c`,
`p_info` at `0x234` (= `l_magic`+12), first `b_info` at `0x240` (= `l_magic`+20); the `l_info` struct
itself starts at `0x228`, so `p_info` is at `l_info`+12 and `b0` at `l_info`+24. The cell is
internally consistent (`p_filesize` is "twelve bytes after `l_magic`"), but a reader taking "l_info"
as the struct start would be off by four. A wording fix in a new superseding row, not a scope change.

**Byte-order note worth carrying into the new row.** `NE32` is *host* endian
(`bele.h:1091-1105`: `typedef BE32 NE32` / `typedef LE32 NE32`), but the bytes on disk are written by
`set_te32`, which is `bele->set32` (`packer.h:272`) under the **target** policy — `le_policy` for
`PackLinuxElf64Le` (`p_lx_elf.h:496`). On this LE host the two coincide, and I measured the on-disk
`b_info` fields as little-endian, which is why the repair tools' `struct.unpack_from("<II", …)` is
correct for these carriers. A packer on a BE host would still write LE bytes for an LE target.

### Which lines ground "the successor position determines the previous block's `sz_cpr`"

Two distinct places, and the round-90 law uses both:

- **Forward (the walker's step).** `PackUnix::unpackExtent`, `src/p_unix.cpp:472-556`: reads a
  12-byte header (`485: fi->readx(&hdr, szb_info);`) then exactly `sz_cpr` payload bytes
  (`504: fi->readx(ibuf+j, sz_cpr);`), so the next header's offset is a function of the stored value.
  This is **S313**, already in the registry.
- **Inverse (the repair's derivation) and its no-padding premise — the pack side, which is the new
  row.** `src/p_unix.cpp:439-440` (`sz_cpr := ph.c_len`), `449` (the 12-byte header write), `458`
  and `464` (exactly `sz_cpr` payload bytes, with no padding term). Because the writer emits
  header-then-payload-then-next-header with nothing in between, `sz_cpr = successor_offset −
  (block_offset + 12)` is exact rather than approximate. The chain terminates at the sentinel
  `sz_unc == 0`, `sz_cpr == UPX_MAGIC_LE32` written at `p_lx_elf.cpp:816-819`.

For the ELF64 LE amd64 carriers the class chain is `PackLinuxElf64amd : PackLinuxElf64Le :
PackLinuxElf64 : PackLinuxElf : PackUnix` (`p_lx_elf.h:518,489,315,40`).

---

## 4. Is pack-scope `src/p_unix.cpp` a new row, or the round-87 rejection again? (task item 3)

**Verdict: a NEW row, on a distinct scope — not a revival of the rejected row.**

The rejected row, quoted verbatim from `corpus/lessons/round-87.md` `## Gate` (line 31):

> | UPX v5.2.0 `src/p_unix.cpp` | **reject** (no row) | HTTP 200, 24181 bytes, sha256 `bf83c413…642e` | line 671 carries the same `sz_cpr` check inside `PackUnix::unpack`, but the Linux ELF classes override `unpack` (`p_lx_elf.cpp` 7755, 9023), so the ELF claim rests on S307. Flip: a carrier class unpacked through `PackUnix::unpack` |

That rejection is **scope-bound to `PackUnix::unpack`** — the generic whole-file unpacker at
`p_unix.cpp:611`, whose end-of-file check is at `p_unix.cpp:667-672`. The Linux ELF classes override
`unpack` (`p_lx_elf.cpp:7755` `PackLinuxElf64::unpack`, `9023` `PackLinuxElf32::unpack`), so that
function never runs for these carriers — hence the rejection, and hence its flip condition ("a
carrier class unpacked through `PackUnix::unpack`").

The pack scope is a **different function with the opposite reachability**:

| | round-87 rejected scope | proposed pack scope |
|---|---|---|
| function | `PackUnix::unpack` (`p_unix.cpp:611`) | `PackUnix::packExtent` (`p_unix.cpp:335`) |
| overridden for ELF? | **yes** — `p_lx_elf.cpp:7755, 9023` | **no** — no override anywhere in v5.2.0 (`grep -rn "::packExtent"` → 1 definition + 4 comments) |
| in force for the carriers? | **no** | **yes** |
| direction | reader | writer |
| what it grounds | the walker's step | the no-padding premise that makes the inversion exact |

The rejection's *reason* ("the ELF classes override it, so the ELF claim rests on S307") therefore does
**not** transfer: the pack-side writer is not overridden, so the pack-side claim genuinely rests on
`src/p_unix.cpp`.

Two further reasons it is not the same proposition:

1. **The URL already carries a different-scope row.** S313 admits `src/p_unix.cpp` at *unpack* scope
   (`PackUnix::unpackExtent`, the block-extent consumer). The round-90 lesson records the pattern
   explicitly: "`src/p_unix.cpp` as a whole (`PackUnix::unpack`) stays **rejected** … this round's
   S313 is a *different scope* on the same URL". A pack-scope row is a third scope on the same file,
   and the precedent for parallel scopes on one file is direct: **S307 and S311 are both rows on
   `src/p_lx_elf.cpp`** with different scopes and neither supersedes the other.
2. **The rejected scope stays rejected.** Nothing here meets the flip condition, and this row does
   not need it to.

**Flip condition for the new row** (its own, since a mined row needs a recheck trigger rather than a
rejection flip): if a future UPX release gives a Linux ELF class its own `packExtent` override, or
changes `PackUnix::packExtent` to emit padding between a header and its payload, the row's scope
must be re-based on the overriding class and the no-padding premise re-measured. Cadence `on-release`
(the URL is tag-pinned; S313/S314 use `on-release`).

---

## 5. Proposed `corpus/SOURCES.md` row (text for the L1 to write)

The L1 owns the write and must take the **next unused id at write time** — S315 is the highest
present now, so **S316** is the suggestion, but round-89's L1 is landing record work on this checkout
concurrently and may have taken it. The L1 must re-check `grep -c '^| S316 ' corpus/SOURCES.md`
before writing, and re-read the insertion anchor after the edit (QUALITY 74).

```
| S316 | UPX 5.2.0 pack-side block writer, `src/p_unix.cpp` at tag `v5.2.0` — https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp | code | A | The base class's `PackUnix::packExtent` writer that lays down each compressed block's twelve-byte `b_info` while packing: the provenance of `sz_unc`/`sz_cpr` from the compressor's own lengths, the twelve-byte header write, and the payload write whose length equals `sz_cpr`; not `PackUnix::pack2`'s own block writer (the ELF classes override `pack2`, so that code is dead for these carriers), not `PackUnix::unpackExtent` (S313), not the whole `PackUnix::unpack` (the rejected round-87 scope), not the shared-object `un_shlib_1` path (S311), not any carrier | `v5.2.0`; fetched 2026-11-05 HTTP 200, 24181 bytes, sha256 `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e`; `PackUnix::packExtent` line 335; `b_info tmp` line 407; `set_te32(&tmp.sz_unc, ph.u_len)` line 439 and `set_te32(&tmp.sz_cpr, ph.c_len)` line 440; the twelve-byte header write line 449; the payload writes line 458 (`fo->write(obuf, ph.c_len)`) and line 464 (`fo->write(ibuf, ph.u_len)`); the header-block variant lines 426-433; `COMPILE_TIME_ASSERT(sizeof(b_info) == 12)` line 55 | The packer writes a block's header and then exactly `sz_cpr` bytes of payload with nothing in between, so the next header's offset is the stored `sz_cpr` away and a repair can invert a successor's position back into the previous block's `sz_cpr` | mined | 2026-11-05 | on-release | corpus/lessons/round-90.md, corpus/knowledge/2026-11-04-r90-interior-block-szcpr.md |
```

**Located quote for the `teaches` cell** (contiguous served bytes, ≤25 words, with its line):

> `src/p_unix.cpp:456-459` — "// write compressed data / if (ph.c_len < ph.u_len) { / fo->write(obuf, ph.c_len); / total_out += ph.c_len;" (14 words)

Wider alternative, if the L1 prefers the header write in the same run (contiguous, 24 words by
whitespace tokens): `src/p_unix.cpp:449-458` — "fo->write(&tmp, sizeof(tmp)); total_out += sizeof(tmp); b_len += sizeof(b_info); … fo->write(obuf, ph.c_len);". I recommend the shorter 456-459 run, because `sz_cpr = ph.c_len` is already anchored at line 440.

**`used-by` caveat.** `corpus/lessons/round-90.md` and
`corpus/knowledge/2026-11-04-r90-interior-block-szcpr.md` both exist (verified). The knowledge entry
currently cites S313 as its `source:` line for the chain law; the L1 must add this row's citation there
(and to the lesson's `## Gate`) or the `used-by` cell would name documents that do not cite it.

**Row-count / census note.** Adding a row changes the registry census; QUALITY 74 requires the row
count **and** the per-status and per-tier tallies to be checked against the base blob, and the
insertion anchor re-read after the edit. This row is `mined`/`A`/`code`, so the histograms move by
one `mined` and one `A` and the row count by one.

---

## 6. What I refused, and what I did not do

- **Did not write to any lane file.** `corpus/SOURCES.md`, `corpus/lessons/round-90.md`,
  `corpus/knowledge/2026-11-04-r90-interior-block-szcpr.md`, `LOG.md`, `SCORECARD.md`,
  `tools/round-90/*` are untouched. The row in §5 is proposed text, not a write. Every file I created
  is under `.ufo/waves/round-90/w1/ScoutUpxPack/` or my scratch dir.
- **Did not read-and-write** any round-89-owned path (`tools/round-89/`,
  `corpus/lessons/round-89.md`, `corpus/QUALITY.md`, `.ufo/waves/round-89/`); round-89's L1 owns
  those writes. (I read `corpus/lessons/round-87.md` and `corpus/SOURCES.md` read-only, which the seat
  rules allow.)
- **Did not run** the round-90 counters or the L1's batteries; the counters are the executors' and
  the L1's. My measurements above are independent, produced with my own walker and the pinned packer.
- **Did not open** the `NEWS` file (S315 already rejects it), `packhead.cpp` (S308) or
  `src/packhead.h` (S309) — the pack-side half of the law needed `p_unix.cpp`, `p_unix.h`,
  `p_lx_elf.cpp`, `p_lx_elf.h` only, and I opened nothing I did not use.
- **No installs.** No `pacman`/`uv`/`npm`/`cargo` transaction was run; nothing was added to
  `~/.local/bin` or any other PATH directory.
- **No credentials, no private URLs.** Only the two public tag-pinned upstream URLs above.

---

## 7. Receipts (absolute paths)

All under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScoutUpxPack/receipts/`:

| file | what it holds |
|---|---|
| `http-status.txt` | HTTP status + byte count per file, four `curl -w` runs |
| `sha256-fresh.txt` | sha256 from a second, independent fetch of each file |
| `fetch-receipt.txt` | both of the above plus the tarball sha256 and the per-file byte-identity check |
| `grep-p_unix-pack.txt` | `grep -n "" src/p_unix.cpp` over 406-451, 438-464, 309-323 (pack side) |
| `grep-p_lx_elf-pack.txt` | `grep -n "" src/p_lx_elf.cpp` over 6025-6031/6055-6063, 783-790/806-820, 5488-5503, 4316-4322 |
| `grep-packExtent-tree.txt` | `grep -rn "::packExtent" tree/upx-5.2.0/src/` — the override census |
| `scope-probe.txt` | which writer/end-marker is in force per carrier, with the measured bytes at `0x2771` and `0x36a4` |
| `chain-measurement.txt` | the two-segment walk of all four carriers, the interior-block derivation, `upx -t` before/after |
| `block0-prediction.txt` | block0 `sz_unc` predicted from the source formula vs measured, all four carriers |
| `line-numbers.txt` | every `grep -n` line number cited in this report, with command exit codes |

Scratch `/fast/scratch/hyaku/kaidoku-r90/ScoutUpxPack/` is **deleted on exit** (per the lane rules);
every receipt was copied into the seat dir first.

## 8. Open questions for the L1

1. The **S311 anchor line slips** (7067→7069, 7098→7102) and the **S312 "l_info" wording** are
   routed defects in existing rows; each closes by a new `supersedes` row (CORPUS rule 2 / QUALITY 93),
   not by an in-place edit. The L1 owns those writes.
2. The pack-side row's `scope` deliberately excludes `p_unix.cpp:150-243` (`PackUnix::pack2`'s own
   writer, dead for these carriers) and `p_unix.cpp:318-323` (the generic end marker, skipped
   because `PackLinuxElf64::pack2` returns 0). If the L1 wants the row to cover the *end marker* too,
   that is a different scope on `p_lx_elf.cpp:816-819` — the in-force site — and would need its own id.
3. **Not measured here:** the `--lzma` method path, 32-bit carriers, and a carrier whose chain
   self-resumes with no loader stop (the round-90 entry's own `[unknown]`). No claim is made about
   them.
