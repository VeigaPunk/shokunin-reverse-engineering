# ScoutSource — R92-C1 frontier step (2b): S313 re-opened 2026-11-05

Seat: ScoutSource (scout). Round 92, attempt 1, declaration commit 11f8606178dfd9e72001b31daf412c5463106a63.
Axes: freshness (row re-fetched this round), calibration (row text checked line by line against the bytes), depth (callers traced into `p_lx_elf.cpp`).
No lane file was edited. `corpus/SOURCES.md` not written. No tools installed. No host state changed.
Tracing method: no LSP server serves an upstream C++ file fetched into scratch, so every location below comes from `grep -nF`/`awk` on the fetched bytes. That is literal text evidence, not semantic proof.

## Commands (all exit 0 unless stated)

```
S=/fast/scratch/hyaku/kaidoku-r92/ScoutSource
curl -fsSL -o p_unix.cpp        -w '%{http_code}\n' https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp     # 200
curl -fsSL -o p_unix.master.cpp -w '%{http_code}\n' https://raw.githubusercontent.com/upx/upx/master/src/p_unix.cpp     # 200
curl -fsSL -o p_lx_elf.cpp      -w '%{http_code}\n' https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp   # 200
curl -fsSL -o p_lx_elf.master.cpp -w '%{http_code}\n' https://raw.githubusercontent.com/upx/upx/master/src/p_lx_elf.cpp # 200
curl -fsSL -o packmast.cpp      -w '%{http_code}\n' https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packmast.cpp   # 200
curl -fsSL -H 'Accept: application/vnd.github.sha' https://api.github.com/repos/upx/upx/commits/master   # 7c7bea44146c7ad6e17cb2d0bb9566805b44a91a
curl -fsSL -H 'Accept: application/vnd.github.sha' https://api.github.com/repos/upx/upx/commits/v5.2.0   # 034b6d0d81c53998c07ad6f34bfead6f5c5445ce
curl -fsSL 'https://api.github.com/repos/upx/upx/commits?path=src/p_unix.cpp&per_page=3'
curl -fsSL 'https://api.github.com/repos/upx/upx/git/trees/v5.2.0?recursive=1'  + 24 src/p_*.h raw fetches (class map)
wc -c; sha256sum; grep -nF <anchors> p_unix.cpp p_unix.master.cpp; diff p_unix.cpp p_unix.master.cpp  # diff exit 1 (files differ)
```
Fetch time: Thu 05 Nov 2026 12:12:57 UTC.

## Gate block — S313 (tag v5.2.0)

| Field | Value |
|---|---|
| Row id | S313 |
| URL | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp |
| Tag commit | `034b6d0d81c53998c07ad6f34bfead6f5c5445ce` (GitHub API, `commits/v5.2.0`) |
| Access date | 2026-11-05 |
| HTTP code | 200 |
| Bytes | 24181 (row: 24181. **match**) |
| sha256 | `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` (row: same. **match**) |

Located quotes (v5.2.0, each at most 25 words):

| Anchor | Line | Exact line text | Row cites | Verdict |
|---|---|---|---|---|
| comment over the loop | 472 | `// Consumes b_info header block and sz_cpr data block from input file 'fi'.` | 472 | match |
| `unpackExtent` definition | 476 | `unsigned PackUnix::unpackExtent(unsigned wanted, OutputFile *fo,` | (not cited) | located |
| loop head | 484 | `while (wanted) {` | (not cited) | located |
| `readx(&hdr, szb_info)` | 485 | `fi->readx(&hdr, szb_info);` | 485 | match |
| bound | 496 | `if (sz_cpr > sz_unc \|\| sz_unc > (int)blocksize)` | (not cited by number) | located |
| `throwCantUnpack("corrupt b_info")` after the bound | 497 | `throwCantUnpack("corrupt b_info");` | 497 | match, but see note 1 |
| `readx(ibuf+j, sz_cpr)` | 504 | `fi->readx(ibuf+j, sz_cpr);` | 504 | match |
| `upx -t` branch | 554 | `else { // "upx -t": (!fo && !(is_rewrite < 0))` | (not cited) | located; shows `upx -t` runs through this loop with no output |

Note 1: `throwCantUnpack("corrupt b_info");` occurs at 491, 495, 497, 502 and 553 inside `unpackExtent`. Line 497 is the throw that belongs to the 496 bound, so the row's line is correct. A line number with no context is ambiguous here, though, and a future recheck should cite 496–497 as a pair.

Other guards in the same loop, read before the payload: 490 `if (sz_unc == 0 || M_LZMA < hdr.b_method) {`, 494 `if (sz_unc <= 0 || sz_cpr <= 0)`, 500–501 `int j = inlen + sz_unc + OVERHEAD - sz_cpr;` / `if (ibuf.getSize() < (unsigned)(j + sz_cpr)) {`. After the payload: 552 `else if (wanted < (unsigned)sz_unc) // mismatched end-of-block` (only when `fo==nullptr` and the call is not a peek).

## Item 4 — is the next header cross-checked against `sz_cpr`?

**Inside `PackUnix::unpackExtent` (S313 scope): it is not.** Lines 484–558 (the `while (wanted)` body) contain no `seek`, `tell` or position comparison (`awk 'NR>=484 && NR<=558' p_unix.cpp | grep -c -E 'seek|tell'` printed 0). The cursor advances only through 485 `fi->readx(&hdr, szb_info);` and 504 `fi->readx(ibuf+j, sz_cpr);`. The next pass of `while (wanted)` reads the next header at whatever offset follows those `sz_cpr` bytes. Every check on a header (490, 494, 496, 501) tests that header's own fields against `blocksize`/`ibuf`. None relates header i+1 to header i's `sz_cpr`. This confirms the row's "places the next header immediately after it".

**Outside S313, the caller does check.** This affects how far the row's chain law ("desynchronises only the block it belongs to") reaches for the round-91/92 *last-block* class:
- `src/p_lx_elf.cpp` v5.2.0 (sha256 `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc`, 373743 B), `PackLinuxElf64::unpack`, after the last extent: 8057 `// check for end-of-file`, 8058 `fi->readx(&bhdr, szb_info);`, 8065 `if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic`, then `throwCompressedDataViolation();`. The `else` branch (`// extra bytes after end?`) throws as well. A wrong `sz_cpr` on the last block therefore misplaces the EOF `b_info` read, and this trailer check is what catches it. The stop-boundary verdict comes from the caller, not from the S313 loop. The ELF32 copy is at 9302/9310.
- Same function, gap blocks (8012–8046): the first header of a PT_LOAD gap is shape-checked. When the check fails, UPX scans a ±32-byte window for a plausible `b_info` and reseeks: 8012 `infoWarning("bad b_info at %#zx", (size_t)pos);`, 8013 `unsigned const N_PEEK(16 * sizeof(int)), H_PEEK(N_PEEK >> 1);`, 8045 `infoWarning("... recovery at %#zx", (size_t)pos);`. This is an upstream *re-synchronisation* window, and it exists only at gap starts.
- Inference, not tested here: for R92-C1, a `upx -t` pass on a ±7 last-block mutant is decided either by the trailer magic check (8058–8066) or by the decompressor/adler, not by the 496 bound. The C1 knowledge entry should cite p_lx_elf.cpp 8057–8069 next to S313 for the stop boundary. That calls for a new row or an S314-style sibling. I did not create it.

## Master drift (recheck field; row unchanged)

| Field | Value |
|---|---|
| URL | https://raw.githubusercontent.com/upx/upx/master/src/p_unix.cpp |
| master HEAD | `7c7bea44146c7ad6e17cb2d0bb9566805b44a91a` |
| HTTP / bytes / sha256 | 200 / 24365 / `6b17409f51fe087ded4d843f497df1458e982dcc0ff77b208ba427fa76a0aed3` |
| Drift | **yes**. Upstream commit `dcc519ba856f` (2026-10-12) "unpackExtent: de-compress each block from its own buffer". Before it: `cc31c1e36510` (2026-06-29) "Increase de-compression OVERHEAD by (size >> ELF_NRV_FUDGE)". |

| Anchor | v5.2.0 | master | Holds? |
|---|---|---|---|
| comment `// Consumes b_info header block and sz_cpr data block ...` | 472 | 475 | yes (shifted +3) |
| `unpackExtent` definition | 476 | 479 | yes |
| `fi->readx(&hdr, szb_info);` | 485 | 488 | yes |
| `if (sz_cpr > sz_unc \|\| sz_unc > (int)blocksize)` | 496 | 499 | yes |
| `throwCantUnpack("corrupt b_info");` (bound) | 497 | 500 | yes |
| `fi->readx(ibuf+j, sz_cpr);` | 504 | **absent** | **no**. Replaced by 505 `MemBuffer cbuf(sz_cpr);` / 506 `fi->readx(cbuf, sz_cpr);`. The `ibuf` guard also became `if (ibuf.getSize() < inlen + (unsigned)sz_unc) {`. |
| `upx -t` branch | 554 | 556 | yes |

The chain law survives on master: the loop still reads exactly `sz_cpr` payload bytes after the 12-byte header and does no position check. Only the buffer placement changed. Master `p_lx_elf.cpp` (HEAD above, 379059 B, sha256 `1ea773307a2c4680be0f9843ac6f63bd0eec7d9298e296117a4d029359495bbb`) keeps the EOF check at 8135/8143 and the gap recovery at 8090/8091/8123, shifted +78. The row's 504 quote is v5.2.0-only. A recheck against master must cite 506 `fi->readx(cbuf, sz_cpr);`.

## Disagreements with the row

1. **"that every executable carrier's unpack path calls" is too broad.** In v5.2.0, `PackLinuxI386 : public PackUnixLe32` (`p_lx_exc.h:41`), `PackBSDI386` (`p_lx_exc.h:133`) and `PackLinuxI386sh` (`p_lx_sh.h:42`, whose `unpack` override is commented out at line 59) do not override `unpack`. They inherit `PackUnix::unpack` (p_unix.cpp 609). That function has its **own** block loop, which never calls `unpackExtent`: 658 `fi->readx(&bhdr, szb_info);`, 680–682 a different bound (`sz_unc <= 0 || sz_cpr <= 5u` / `||  sz_cpr > sz_unc || sz_unc > blocksize`), 691 `fi->readx(buf+i, sz_cpr);`, plus an inline EOF magic check at 667–673. All three classes are registered (`packmast.cpp` 211, 213, 215; packmast sha256 `8b773e633a4849d9b7fc51ea106563436fef3b9aa5fbae1343ead850528056bf`). The accurate scope is "every `PackLinuxElf32`/`PackLinuxElf64` carrier". That includes the round's `PackLinuxElf64amd` (`packmast.cpp:201`), whose `PackLinuxElf64::unpack` calls `unpackExtent` at 7902/7907 (PT_LOAD) and 8051 (gaps). Mach-O (`p_mach.h:758,1257`) and vmlinux (`p_vmlinx.h:89`) override `unpack` too. I did not trace whether they call `unpackExtent`.
2. **Line 497 is ambiguous**, as note 1 above explains: five identical throw lines sit in the loop. The row's choice is the correct one.
3. **The "only the block it belongs to" chain law needs a caller-side caveat for the last block.** The S313 loop does not catch a misplaced next header, but `PackLinuxElf64::unpack` 8057–8069 does. The round-92 C1 knowledge entry should not credit S313 with the stop-boundary verdict.

## Attack — what upstream fact would make the row's scope claim false

The scope claim is: the cited lines are the block loop of `PackUnix::unpackExtent`, not `un_shlib_1`, not the whole `PackUnix::unpack`.
- **It would be false if** (a) lines 485/496–497/504 sat inside `PackUnix::unpack` (609–) rather than `unpackExtent` (476–560). They do not: 476 opens `unpackExtent` and 609 opens `unpack`. Or (b) the ELF64 executable path reached its blocks through `un_shlib_1` or through `PackUnix::unpack` instead of `unpackExtent`. It does not: `un_shlib_1` runs only when `is_shlib = 1`, which 7829 `if (dynhdr && !(Elf64_Dyn::DF_1_PIE & elf_unsigned_dynamic(Elf64_Dyn::DT_FLAGS_1))) {` sets (7831), and the call is at 7835. Otherwise the PT_LOAD loop at 7890–7911 calls `unpackExtent` directly (7902/7907).
- **Weak point found:** the exclusion "not the shared-object `un_shlib_1` path" excludes a *function*, not a *loop*. `un_shlib_1` itself calls the same `unpackExtent` (`p_lx_elf.cpp` 7102 `unsigned const sz_block1 = unpackExtent(sz_elf_hdrs, nullptr,` and 7181 `unpackExtent(wanted, fo, c_adler, u_adler, false);`). A reading that uses the exclusion to mean "shlib blocks obey a different chain law" is therefore false: shlib blocks go through the very loop S313 cites, and only the surrounding function (`un_shlib_1`, S311) differs.
- **Row text that is false as written:** "every executable carrier", per disagreement 1. **Row text that holds:** 12-byte header (`COMPILE_TIME_ASSERT(sizeof(b_info) == 12)` at line 55; `szb_info(sizeof(b_info))` at 51), the bound, and payload-then-next-header adjacency.

Confidence: high for the Gate fields, line numbers and drift, which are byte-verified. High for the class/override map (header grep at tag v5.2.0). Medium for the inference about which check decides `upx -t` on the C1 mutants, which I did not execute.

## Remaining unknowns
- Whether `PackMachBase::unpack` / `PackVmlinux*::unpack` call `unpackExtent`. Not traced; outside the C1 ELF64 scope.
- Which exact check (trailer magic 8065, the decompressor, or adler) rejects each C1 ±7 mutant under `upx -t`. That needs a run, not a source read.

## Files written
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-92/w1/ScoutSource/ScoutSource.md` (this file)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-92/w1/ScoutSource.md` (Report trailer copy, identical)
- Scratch `/fast/scratch/hyaku/kaidoku-r92/ScoutSource` removed before yield.
