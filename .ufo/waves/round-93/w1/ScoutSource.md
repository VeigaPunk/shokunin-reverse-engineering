# ScoutSource — round 93 seat report (R93-C1 / R93-C2 source re-opening)

Seat: `ScoutSource` (scout). Lane: `kaidoku-shokunin`. Wave `r93-w1`.
Lane HEAD at the time of this report: `92a240521bd1bf2213b75d18d9b176a8dafdc67c`
(declaration commit; base `0a2a23da5eb50410a8a0df90c031d9f4fdadb024`).

Scope executed: open and re-open this round's sources for the R93-C1 / R93-C2 entries
(CORPUS.md rule 1 — fleet root `/home/vgpnk/Projects/shokunin/CORPUS.md` line 112:
a row is written only after opening the source in the round that writes the row; the
round lesson's `## Gate` records URL, access date, and a ≤25-word quote with its
location grounding `teaches`).

Lane state: **no lane file was created, edited or deleted outside my seat directory**
(`.ufo/waves/round-93/w1/ScoutSource/`). All lane reads were read-only
(`git status --porcelain`, `git log`, `git rev-parse`); no mutating git/jj command was
run in the lane. No host state was mutated (no sysctls, no pacman transaction, no
namespace change). No tool was installed or upgraded — every tool used
(`curl`, `sha256sum`, `sed`, `grep`, `python3`, `upx 5.2.0`) was already present.

---

## 1. Per-source table

Access date for every row below: **2026-11-05**.

| # | source (URL) | HTTP | bytes | sha256 | located quote (≤25 words) with line |
|---|---|---|---|---|---|
| A | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp` | 200 | 24181 | `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` | line 496: `if (sz_cpr > sz_unc \|\| sz_unc > (int)blocksize)` |
| B | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp` | 200 | 373743 | `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc` | line 8065: `if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic` |
| C | `https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt` | 200 | 37208 | `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42` | line 74: `All UPX supported file formats can be unpacked using the -d switch, eg.` (13 words) |

**Expected-vs-measured pins.** A and B match the two pins named in the seat brief
**exactly** (24181 / `bf83c413…9642e`; 373743 / `551fc867…2d2dc`). C's size and
sha256 match the S271 registry row's recorded values (`37208 bytes`,
`4dc547ed…b8c42`) — S271 is re-opened cleanly.

Fetched bytes are copied into the seat at
`.ufo/waves/round-93/w1/ScoutSource/receipts/{p_unix.cpp,p_lx_elf.cpp,upx-doc.txt}`
(sha256 re-verified after the copy: identical to the table above).

Fetch command (exact, exit 0 for all three):
```
curl -fsSL -w '%{http_code}' -o <name> https://raw.githubusercontent.com/upx/upx/v5.2.0/<path>
```
Additional supporting fetches, same tag, recorded for completeness:
`src/p_unix.h` (200 / 6651 / `73bd992ec0fb46022e299ec4b2cd696545412453a654573e6246034cf4881a88`),
`doc/upx.1` (200 / 40077 / `09552b3cf4e9073c288060b8f50ed1c1dde3dca89dcaf1230367b6c3e15d4e25`),
`doc/upx.pod` (200 / 35451 / `cc93ccea8e9e9f4721b1b1cd983d960deea432c7d4913f1efe35f33d2a1c31c2`),
and the full upstream tree `https://codeload.github.com/upx/upx/tar.gz/refs/tags/v5.2.0`
(200 / 2322262 / `e58526f3e198164d63b99b3580dbb9a5111a02a3e4ab1b22b05add4f04c56bbc`),
used only to prove the caller list is **complete** across the whole upstream `src/`
tree (a per-file grep on two files could have missed a third caller file).

---

## 2. Caller map — verdict

### 2.1 `unpackExtent` is defined once, and `PackUnix::unpack` does **not** call it

```
grep -n "unpackExtent" p_unix.cpp
  476:unsigned PackUnix::unpackExtent(unsigned wanted, OutputFile *fo,
```
`p_unix.cpp` contains exactly **one** occurrence: the definition at line 476. The
generic unpack loop `PackUnix::unpack` (line 609) has its **own inline** block loop
(`for (;;)` at line 652, `fi->readx(&bhdr, szb_info)` at 660, `sz_cpr` bound at
680–681) and never reaches `unpackExtent`.

**Answer to the brief's question 1 — does `PackUnix::unpack` (p_unix.cpp:609) call
`unpackExtent`? NO.** Verified two ways: the single-hit grep above, and a full read of
the function body (609–727) — its loop reads `bhdr` inline and calls `decompress()`
directly.

### 2.2 Complete caller list of `PackUnix::unpackExtent` (upstream `src/`, v5.2.0)

```
grep -rn "unpackExtent(" --include=*.cpp .   # from upx-5.2.0/src, stub/ excluded
```
16 call sites in 4 files, plus the definition. Enclosing function computed from the
definition lines in the same file:

| caller file:line | enclosing definition | function |
|---|---|---|
| p_lx_elf.cpp:7102 | 7011 | `PackLinuxElf64::un_shlib_1` (peek, `fo=nullptr`) |
| p_lx_elf.cpp:7181 | 7011 | `PackLinuxElf64::un_shlib_1` |
| p_lx_elf.cpp:7305 | 7214 | `PackLinuxElf32::un_shlib_1` (peek) |
| p_lx_elf.cpp:7381 | 7214 | `PackLinuxElf32::un_shlib_1` |
| p_lx_elf.cpp:7902 | 7755 | `PackLinuxElf64::unpack` |
| p_lx_elf.cpp:7907 | 7755 | `PackLinuxElf64::unpack` |
| p_lx_elf.cpp:8051 | 7755 | `PackLinuxElf64::unpack` |
| p_lx_elf.cpp:9149 | 9023 | `PackLinuxElf32::unpack` |
| p_lx_elf.cpp:9154 | 9023 | `PackLinuxElf32::unpack` |
| p_lx_elf.cpp:9296 | 9023 | `PackLinuxElf32::unpack` |
| p_lx_interp.cpp:258, 263, 272, 278 | 199 | `PackLinuxElf32x86interp::unpack` |
| p_mach.cpp:1576, 1624 | 1473 | `PackMachBase<T>::unpack` |

**Answers to the brief's questions 2–3:**
- `PackLinuxElf64::unpack` (**p_lx_elf.cpp:7755**) — **YES**, calls it at 7902, 7907, 8051.
- `PackLinuxElf32::unpack` (**p_lx_elf.cpp:9023**) — **YES**, calls it at 9149, 9154, 9296.
- `PackLinuxI386` / `PackBSDI386` — these do **not** call `unpackExtent` and do **not**
  have their own block loop; they **inherit** `PackUnix::unpack` (p_unix.cpp:609),
  i.e. the generic inline loop with its own bound at 680–681. Evidence:
  - `p_lx_exc.h:41` `class PackLinuxI386 : public PackUnixLe32`; `p_lx_exc.h:133`
    `class PackBSDI386 : public PackLinuxI386`.
  - `grep -n "::unpack\b" p_lx_exc.cpp` → **no matches** (the file defines only
    `pack1/pack4/getCompressionMethods/getFilters/generateElfHdr/newLinker/
    buildLinuxLoader/buildLoader/getLoaderPrefixSize/checkEhdr/canPack/patchLoader/
    patchLoaderChecksum/updateLoader`) — i.e. **no `unpack` override at all**.
  - `grep -n "unpackExtent" p_lx_exc.cpp` → **no matches**.
  - `p_lx_sh.h:42` `class PackLinuxI386sh : public PackLinuxI386`; its `unpack`
    override is **commented out** (`p_lx_sh.h:59` `// virtual void unpack(OutputFile *fo) { super::unpack(fo); }`).
  - `p_vmlinx.h:41` / `p_vmlinz.h:38,129` — the vmlinux/vmlinuz families derive from
    `Packer`, not `PackUnix`, and each has its own `unpack` (p_vmlinx.cpp:637,
    p_vmlinz.cpp:690, p_vmlinz.cpp:1047) with no `unpackExtent` use.
  - `p_mach.h:705` `class PackMachBase : public PackUnix` — Mach-O **does** call
    `unpackExtent` (p_mach.cpp:1576, 1624), so "the ELF families" is narrower than
    "the `unpackExtent` callers".

### 2.3 The two bound sites in `p_unix.cpp` (this is what the S318 row is about)

```
grep -n "sz_cpr >\|sz_unc >\|sz_cpr <=\|sz_unc <=" p_unix.cpp
  494:        if (sz_unc <= 0 || sz_cpr <= 0)
  496:        if (sz_cpr > sz_unc || sz_unc > (int)blocksize)
  680:        if (sz_unc <= 0 || sz_cpr <= 5u
  681:        ||  sz_cpr > sz_unc || sz_unc > blocksize)
```
- `unpackExtent` (476) → bound at **496** (`sz_cpr > sz_unc || sz_unc > (int)blocksize`),
  with a separate zero-check at 494.
- `PackUnix::unpack` (609) → bound at **680–681** (`sz_unc <= 0 || sz_cpr <= 5u ||
  sz_cpr > sz_unc || sz_unc > blocksize`) — note the extra `sz_cpr <= 5u` minimum and
  the missing `(int)` cast relative to :496.

So `p_unix.cpp` holds **two distinct block-size bounds**, in two distinct loops.

---

## 3. Corrections needed to the S318 draft

Draft under review: `.ufo/waves/round-93/l1/drafts/s318-draft.md` (mtime 2026-11-05
10:55:15; the L1 revised it once during this seat's run — an earlier copy read the
first `cat` at 10:47 carried the older wording "supersedes S313 — the `unpackExtent`
block loop … serve the plain-unix consumers through `PackUnix::unpack`", which is
**wrong**; the current text below is the corrected one and is the one reviewed here).

Current draft teaches-sentence (verbatim, trimmed):
> supersedes S313 — the file holds two separate block-size bounds: `PackUnix::unpackExtent`
> (p_unix.cpp:476, bound at :496) is the consumer the ELF families call through `p_lx_elf.cpp`
> (`un_shlib_1` and `unpack`, e.g. :7181, :8051); `PackUnix::unpack` (p_unix.cpp:609,
> bound at :681) runs its own inline loop and is not the function that `unpackExtent`
> callers reach; so a claim that every executable carrier's unpack path rides one loop
> is too broad, and the correct statement names the call site; not any carrier, not other tags

**Every line number and quoted fragment in the current draft checks out against the
fetched bytes.** Verification:

| draft claim | command | result |
|---|---|---|
| `unpackExtent` at p_unix.cpp:476 | `sed -n '476p' p_unix.cpp` | `unsigned PackUnix::unpackExtent(unsigned wanted, OutputFile *fo,` — **match** |
| bound at :496 | `sed -n '496p' p_unix.cpp` | `if (sz_cpr > sz_unc || sz_unc > (int)blocksize)` — **match** |
| `PackUnix::unpack` at p_unix.cpp:609 | `sed -n '609p' p_unix.cpp` | `void PackUnix::unpack(OutputFile *fo)` — **match** |
| generic bound at :681 | `sed -n '680,681p' p_unix.cpp` | `if (sz_unc <= 0 || sz_cpr <= 5u` / `\|\|  sz_cpr > sz_unc \|\| sz_unc > blocksize)` — **match** (the `sz_cpr > sz_unc` clause is on 681) |
| "the ELF families call through `p_lx_elf.cpp` (`un_shlib_1` and `unpack`, e.g. :7181, :8051)" | `sed -n '7181p;8051p' p_lx_elf.cpp` | 7181 `unpackExtent(wanted, fo, c_adler, u_adler, false);` (in `PackLinuxElf64::un_shlib_1`, def 7011); 8051 `unpackExtent(size, fo,` (in `PackLinuxElf64::unpack`, def 7755) — **match** |
| "grep -n unpackExtent on the fetched file → line 476 only" | `grep -n "unpackExtent" p_unix.cpp` | one hit, 476 — **match** |
| "on `p_lx_elf.cpp` → callers at 7181, 7381, 7902, 7907, 8051, 9149, 9154, 9296" | `grep -n "unpackExtent" p_lx_elf.cpp` | full list is 12 lines (2 comments + **10** call sites): 7102, 7181, 7305, 7381, 7902, 7907, 8051, 9149, 9154, 9296 — **the draft's list omits 7102 and 7305** |
| sha256 pins `bf83c4133c27d394…` / `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc` | `sha256sum` | **match** |
| HTTP 200 / 24181 bytes | fetch log | **match** |

### Corrections to apply

1. **The p_lx_elf.cpp caller list is short by two.** The draft records 8 call sites
   (7181, 7381, 7902, 7907, 8051, 9149, 9154, 9296); the file has **10** — 7102 and
   7305 are the `unpackExtent(sz_elf_hdrs, nullptr, …)` *peek* calls in
   `PackLinuxElf64::un_shlib_1` and `PackLinuxElf32::un_shlib_1` respectively
   (7102: `unsigned const sz_block1 = unpackExtent(sz_elf_hdrs, nullptr,`; 7305: the
   32-bit twin). Add them, or state "8 call sites plus the two `un_shlib_1` peeks at
   :7102 and :7305" — the current sentence implies it is the complete list.
   (The peeks are the ones S311 already anchors, so this is a completeness fix, not a
   contradiction.)
2. **"the ELF families call through `p_lx_elf.cpp`" is slightly over-broad in the other
   direction — the ELF *interp* family calls it from a different file.**
   `PackLinuxElf32x86interp::unpack` (p_lx_interp.cpp:199) calls `unpackExtent` at
   p_lx_interp.cpp:258, 263, 272, 278. Since the row's scope excludes other files, the
   safe wording is "the ELF families in `p_lx_elf.cpp`" (the row's anchor is one file),
   or "the ELF unpack paths in `p_lx_elf.cpp`".
3. **The sentence does not say that `unpackExtent` also has non-ELF callers.**
   `PackMachBase<T>::unpack` (p_mach.cpp:1473) calls it at p_mach.cpp:1576 and 1624.
   The row's "not any carrier" scope excludes it, so this is not an error, but the
   teaches clause "is the consumer the ELF families call through" reads as if ELF were
   the only caller family. Recommend one clause: "also called by the ELF-interp path
   (`p_lx_interp.cpp`) and by Mach-O (`p_mach.cpp`); those are out of this row's scope".
   If the L1 prefers to keep the row single-file, a scope clause "not the ELF-interp or
   Mach-O callers (other files)" suffices.
4. **Optional strengthening: the counter-example that pins the narrowing.** The row
   supersedes S313's "every executable carrier's unpack path calls" wording. The sharp
   counter-example is now on file and belongs in the row's `teaches`: `PackLinuxI386`
   (p_lx_exc.h:41) and `PackBSDI386` (p_lx_exc.h:133) **do not override `unpack` at
   all** (`grep -n "::unpack\b" p_lx_exc.cpp` → no matches) and **do not call
   `unpackExtent`** (`grep -n "unpackExtent" p_lx_exc.cpp` → no matches) — they ride
   the generic `PackUnix::unpack` inline loop instead. `PackLinuxI386sh` (p_lx_sh.h:42)
   is the same, with its override commented out at p_lx_sh.h:59. That is a concrete
   i386/BSD carrier that the S313 wording would wrongly cover.
5. **One optional nuance for the "two bounds" clause:** the two bounds are not
   textually identical — :496 is `sz_cpr > sz_unc || sz_unc > (int)blocksize` while
   :680–681 adds the minimum `sz_cpr <= 5u` and drops the `(int)` cast. If the row
   wants a quotable pair, quoting both lines (rather than only :681) is exact.

No correction is needed to the row's `supersedes S313` framing, its scope exclusions
(`not any carrier, not other tags`), its sha256/size/HTTP anchors, or its `used-by`
pointer. The row's `status`/`recheck` fields (`mined`, `2026-11-05`, `on-release`)
follow the registry's append-only rule 2 shape.

---

## 4. Re-opening S271 — CLI contract for the fresh-pack oracle

S271 (`corpus/SOURCES.md` line 188) records `doc/upx-doc.txt` at 37208 bytes,
sha256 `4dc547ed…b8c42`, anchor "NOTES FOR LINUX/ELF386 lines 441-442, heading 433".
**All re-checked against the fetched bytes:**

```
sed -n '433p;441,442p' upx-doc.txt
  433:  NOTES FOR LINUX/ELF386
  441:    Packed programs will be byte-identical to the original after
  442:    uncompression.
```
— heading and both lines are verbatim; the row's anchor still holds.

### The four CLI options the fresh-pack oracle uses

| option | line(s) in `upx-doc.txt` | located quote (≤25 words) | words |
|---|---|---|---|
| `-d` (decompress) | 73–75 | 74: `All UPX supported file formats can be unpacked using the -d switch, eg.` / 75: `upx -d yourfile.exe will uncompress the file you've just compressed.` | 13 / 10 |
| `-t` (test) | 77–82 | 78: `The -t command tests the integrity of the compressed and uncompressed` / 79: `data, eg. upx -t yourfile.exe check whether your file can be safely` / 80: `decompressed. Note, that this command doesn't check the whole file, only` | 11 / 12 / 11 |
| `-o` (output) | 110 | 110: `-o file: write output to file` | 6 |
| `--best` | 115, 125–129 | 115: `UPX offers ten different compression levels from -1 to -9, and --best.` / 125: `Compression level --best may take a long time.` | 12 / 9 |

These are the same options the round-93 counter invokes: `tools/round-92/stop-boundary-battery-v2.py`
line 179 `run([UPX, "-t", "-q", p])`, line 187 `run([UPX, "--best", "-q", "-o", outp, inp])`,
and `tools/round-93/stop-boundary-repair-battery-v3.py` line 142
`v2.run([v2.UPX, "-d", "-q", "-o", outp, cand])`. Every flag the counter uses is
documented in the fetched doc at the lines above. Note the doc's `-t` caveat
(line 80–82: the test "doesn't check the whole file, only the part that will be
uncompressed during program execution") — that is exactly the scope of the
`upx -t` red/green atoms used in the craft block-31/32 criterion columns.

The same content is present in the tag's man sources (doc/upx.1: `-d` at 139–140,
`-t` at 143–144, `-o` at 175, `--best` at 181/190; doc/upx.pod: `-d` 94, `-t` 99,
`-o` 135, `--best` 144/163), so the CLI contract has two additional corroborating
files at the same tag.

### Oracle-relevant CLI fact, verified on this host (UPX 5.2.0)

`/usr/bin/upx` → `upx 5.2.0`, sha256
`cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969` — matches the
pinned packer recorded in `corpus/knowledge/2026-11-05-r92-stop-boundary-repair.md`
limit 7. `/usr/bin/env` sha256 =
`a9ba02dcad338ee7f0b03e58a1cf44009b2bd645b09c2b423242e9791d202301` — matches the
frozen pin in `.ufo/waves/round-93/claims.json` (`fresh_pack_oracle_source`).

**Round-trip oracle assumption, measured (not inferred).** I re-created the counter's
own fresh-pack recipe by hand in scratch (`/usr/bin/env` → ELF64 program headers →
largest non-executable PT_LOAD = ph[4], off 49152, p_filesz 13608 → marker
`KAIDOKU-R93-a1b2c3d4e5f60718` written at offset 55956):

```
upx --best -q -o packed mut.bin   → rc 0, 68312 → 34420 bytes, linux/amd64
upx -d -q -o dec packed           → rc 0
sha256(mut.bin) = sha256(dec) = 1fe28fba3b1a307ea616e8026b6a033345fab884775826fd1b247df87d2eb0ea
ROUNDTRIP identical: True (68312 == 68312 bytes)
```
So the counter's `fresh-roundtrip` premise — that `upx -d` on a freshly packed image
reproduces the **mutated source bytes** byte-for-byte — holds on this host with
UPX 5.2.0 for the pinned `/usr/bin/env` source, at the exact marker site the counter
computes. (An unpack of the *unmutated* `/usr/bin/env` also returned the pinned
sha256 exactly.)

---

## 5. Existing rows' anchors — all still match

Every anchor of S313, S316, S317 (and S311, for completeness) was re-read from the
fetched bytes with `sed -n`:

| row | anchor in the row | measured | verdict |
|---|---|---|---|
| S313 | p_unix.cpp **496** `if (sz_cpr > sz_unc \|\| sz_unc > (int)blocksize)` | identical | **match** |
| S313 | p_unix.cpp 472 `// Consumes b_info header block and sz_cpr data block from input file 'fi'.` | identical | **match** |
| S313 | p_unix.cpp 485 `fi->readx(&hdr, szb_info);` | identical | **match** |
| S313 | p_unix.cpp 497 `throwCantUnpack("corrupt b_info");` | identical | **match** |
| S313 | p_unix.cpp 504 `fi->readx(ibuf+j, sz_cpr);` | identical | **match** |
| S316 | p_unix.cpp **335** `void PackUnix::packExtent(` (region 335–345 = signature + body head) | identical | **match** |
| S316 | p_unix.cpp 439 `set_te32(&tmp.sz_unc, ph.u_len);` | identical | **match** |
| S316 | p_unix.cpp 449 `fo->write(&tmp, sizeof(tmp));` | identical | **match** |
| S316 | p_unix.cpp 458 `fo->write(obuf, ph.c_len);` | identical | **match** |
| S317 | p_lx_elf.cpp **8065** `if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic` | identical | **match** |
| S317 | p_lx_elf.cpp 8066 `throwCompressedDataViolation();` | identical | **match** |
| S311 | p_lx_elf.cpp 7011 `PackLinuxElf64::un_shlib_1` | identical | **match** |
| S311 | p_lx_elf.cpp 7060–7068 header read + `p_filesize` cross-check vs `ph.u_file_size` | 7060 `fi->seek(overlay_offset - sizeof(l_info), SEEK_SET);` … 7069 `\|\| get_te32(&hdr.p.p_filesize) != ph.u_file_size` — the cross-check is on **7069**, not 7068 | **partial**: the row's "lines 7060-7068" range stops one line short of the `p_filesize` comparison it names; the quote itself is right. Suggest citing 7060–7069 in the Gate rather than editing the row (rule 2 is append-only). |
| S271 | doc/upx-doc.txt 433 heading + 441–442 | identical | **match** |

**A second partial anchor** found while re-opening S311: the row's evidence cites
"the `unpackExtent(sz_elf_hdrs, …)` peek **line 7098**". Line 7098 is a *comment*
(`// will just decompress it all.  For new style, the first compressed`); the peek
**call** is on **7102** (`unsigned const sz_block1 = unpackExtent(sz_elf_hdrs, nullptr,`),
and the `throwCantUnpack("corrupt b_info");` it names is on **7105** (correct). The
32-bit twin: the row says the same throw is on 7308 — measured: 7305 is the peek
call, 7308 is the throw (correct). So one anchor in S311 (7098 → 7102) and one range
end (7068 → 7069) are off; both are record-level drift to be handled by the
append-only route (a new row or the round lesson's Gate), not by editing S311.

**S313's `used-by` scope note still holds.** S313 says the `unpackExtent` loop is
"every executable carrier's unpack path" — measured false in two independent ways:
(a) `PackUnix::unpack` (609) has a separate inline loop, and (b) `PackLinuxI386` /
`PackBSDI386` / `PackLinuxI386sh` inherit that generic loop and never call
`unpackExtent`. The v3 fresh-pack arm's own oracle rides `PackLinuxElf64::unpack`
(7755) → `unpackExtent` (7902/7907/8051), i.e. the ELF-class path, consistent with
S317's trailer-check row.

---

## 6. Search log — UPX output determinism documentation

Question: does upstream UPX document a guarantee that packing the same input twice
yields byte-identical output (the property the fresh-pack arm's *determinism guard*
asserts, `packed1 == packed2`)?

| # | query / command | where | date | identified | included | excluded | result |
|---|---|---|---|---|---|---|---|
| 1 | `grep -rIn --include=*.txt --include=*.md --include=*.cpp --include=*.h --include=*.c -i "reproducib\|determinis"` | upstream v5.2.0 tree (`src/`, `doc/`, `stub/` excluded) | 2026-11-05 | 4 hits | 0 | 4 (all are unrelated sort-order comments: `src/p_mach.cpp:580`, `src/p_vmlinx.cpp:105`, `src/pefile.cpp:847`, `src/pefile.cpp:1041` — "make sort order deterministic" in *comparison* code) | **no upstream documentation of output determinism** |
| 2 | `grep -rIn -i "deterministic\|reproducible\|byte-identical" doc/ README* NEWS*` | upstream v5.2.0 `doc/` | 2026-11-05 | 18 hits | 0 | 18 | all 18 are the **`upx -d` restore** property ("Packed programs will be byte-identical to the original after uncompression", doc/upx-doc.txt lines 192/211/253/287/384/441/487/530, and `--exact` at 101–106). **Nothing about the packing step being deterministic.** |
| 3 | GitHub API `search/issues?q=repo:upx/upx+deterministic` | upx/upx issue tracker | 2026-11-05 | 7 | 2 | 5 | #927 "Output not deterministic" (closed 2025-08-28; reporter retracted it in the last comment: *"there was an environment variable on the VM that affected Go compilation. Sorry for the false alarm"* — the difference was in the **input**, not in UPX); #18850 "Non-deterministic unpacking results (different binary hash after pack→unpack with UPX 5.1.1)" (closed 2026-05-01; PE/WindowsSCP, ~1–2 MB structural difference — a *reconstruction*, not a packing-determinism report) |
| 4 | GitHub API `search/issues?q=repo:upx/upx+reproducible` | upx/upx issue tracker | 2026-11-05 | 49 | 0 | 49 | none is about packing determinism (they are Android/arm64 crashes, TLS, PE debug dirs, …) |
| 5 | web search `UPX reproducible builds deterministic packed output byte-identical packing twice` | open web | 2026-11-05 | 8 sources | 0 | 8 | generic reproducible-builds material; **no primary UPX document** surfaced; the upstream issue behind the claim is #927, which upstream closed as a false alarm |
| 6 | web search `site:github.com/upx/upx issues non-deterministic different output same file packed twice` | open web | 2026-11-05 | 0 | 0 | — | the `site:` constraint returned **no results**; the relaxed fallback returned only generic packing-determinism advice, no upstream record |
| 7 | **empirical, this host**: `upx --best -q -o p{1,2,3} src.bin` ×3 on `/usr/bin/env` | local scratch | 2026-11-05 | 3 packs | 3 | 0 | all three byte-identical: sha256 `e703277bc092ad8845bd9539d0743266573863b2da1e57884632383d59eb61c5`, 34404 bytes; `cmp p1 p2` and `cmp p1 p3` both clean. `upx -d` on p1 → sha256 `a9ba02dc…d202301` = the original `/usr/bin/env` pin, byte-identical; `upx -t -q p1` → rc 0, `testing p1 [OK]` |

**Stop rationale.** Queries 1–2 exhausted the upstream *documentation* surface at the
pinned tag (the only doc claims are about the unpack direction). Queries 3–6
exhausted the upstream *issue* surface for the packing direction: the single
determinism-titled upstream issue (#927) was closed as a false alarm whose cause was
the input build, and #18850 concerns PE reconstruction on unpack. Query 7 is the
in-host measurement that the counter's guard actually rests on. **The search is
closed: upstream UPX 5.2.0 ships no documentation promising byte-identical packed
output, and the only upstream record of a determinism failure was withdrawn by its
reporter.**

**Consequence for the round-93 instrument (an honest note, not a defect):** the fresh
arm's `deterministic` provenance atom is an *empirical* guard, not a documented
UPX guarantee. On this host with UPX 5.2.0 and the pinned `/usr/bin/env` source it
holds (query 7, and the hand-recreated mutate→pack→unpack round trip in §4). If it
ever fails on a future host, the counter's `unevaluable: "fresh provenance atoms
failed"` path is the correct disposition — not a relaxation of the atom. This should
be recorded as a **Limit** in the round-93 knowledge entry (the packer, not the
oracle, is the source of any non-determinism), and it is a fair candidate for the
next round's held-out arm (a second fresh source, to show the determinism guard is
not a property of one file).

---

## 7. R93-C2 side — what this seat can and cannot attest

This seat's item is the source re-opening. The R93-C2 claim is about a *citation
semantics* counter over the lane's own files; the drafts under review are
`.ufo/waves/round-93/l1/drafts/block32-draft.md` and `row188-draft.md`.

Facts measured about the lane's own files (read-only), for the L1's benefit:

- The craft section currently ends at **SKILL.md line 766** (line 766 is blank) and
  the next heading is **`## Config custody for live-probe rounds (SOP)` at line 767** —
  confirming the stated insertion point for block 32.
- The existing block-31 row 3 that D-91-3 names is at **SKILL.md line 763**:
  `| intact input refused by mistake | ... | never refuse an intact input: the refusal follows the packer's verdict, not the geometry | QUALITY 169 |`
  — its criterion cell cites **QUALITY 169**, whose text (per the row-188 draft) is
  guard inheritance for superseding instruments, i.e. it does not state the
  intact-input rule. The mis-cite is confirmed present in the committed file at the
  base revision.
- `tools/round-93/craft-citation-semantic.py` and the two frozen manifests exist in
  the lane at HEAD `92a24052` (`.ufo/waves/round-93/manifests/block31-before.json`,
  `block32-after.json`).

What this seat did **not** do (out of item scope, and it would require the frozen
manifests' exact invocation): it did not run the R93-C2 counter, did not score the
after-manifest, and did not touch `corpus/`. The claims' kill rule for R93-C2 is the
L1's to discharge.

---

## 8. Files written by this seat

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-93/w1/ScoutSource.md`
  (this report)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-93/w1/ScoutSource/receipts/p_unix.cpp`
  (24181 B, `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e`)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-93/w1/ScoutSource/receipts/p_lx_elf.cpp`
  (373743 B, `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc`)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-93/w1/ScoutSource/receipts/upx-doc.txt`
  (37208 B, `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42`)

Scratch `${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r93/ScoutSource` was removed
after the receipts were copied. No other path was written.

## 9. Confidence and remaining unknowns

- **High confidence** (byte-level, reproduced by the commands above): every line
  number, quote and sha256 in §1, §3, §4 and §5; the caller map in §2; the empirical
  round-trip and determinism measurements in §4 and §6.
- **Medium confidence**: that the *complete* upstream caller list is the 16 call sites
  in §2.2 — the tarball grep covers upstream `src/` at tag v5.2.0 exactly; a different
  tag could differ (the row is explicitly scoped to v5.2.0).
- **Open / not established**: (a) whether the L1 wants the S318 `teaches` clause to
  name the ELF-interp and Mach-O callers (correction 3 above is a wording judgement,
  not a factual defect — the facts are in §2.2 for the L1 to use); (b) whether
  `PackLinuxElf32x86interp` and `PackMachBase` should get their own registry rows in a
  later round (they are named nowhere in `corpus/SOURCES.md` today — verified by
  grepping the registry for `p_lx_interp` and `p_mach`: no hits); (c) the S311 anchor
  drift (7098 → 7102; 7068 → 7069) needs an append-only disposition from the L1.
