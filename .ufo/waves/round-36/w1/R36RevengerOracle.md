# R36RevengerOracle — how independent is the R36-C1 oracle, really?

Seat: `R36RevengerOracle` (leaf, advisory). Round 36, wave 1 (build drafts + first falsifiers).
Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; lane HEAD during this seat
`d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be`; freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`;
base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`.
Observed 2026-10-26T04:26Z–04:45Z. Read-only on the lane: no VCS mutation, nothing frozen touched,
no counter/carrier/oracle/predicate edited, no file written except this report. sasquatch was **not**
reinstalled or moved.

---

## 0. Answer in one line

The frozen oracle (`/usr/bin/unsquashfs` 4.7.5) is **not code-independent** of the tool under test
(sasquatch 4.5.1 = a patched `unsquashfs` 4.5.1): they share the same reader lineage — the v4
directory-walk, inode decode and (byte-identical) decompressor wrapper functions — and, at run time,
the **same codec shared objects**. A shared bug would therefore produce the same wrong tree twice and
the predicate would still pass. The tree itself is nevertheless correct, because three genuinely
code-disjoint readers reproduce it byte-for-byte on the carriers where they exist (details in §8).

Independence class of the frozen oracle: **release/version independence plus patch-layer
independence only — not implementation independence.**

---

## 1. Contract reconstruction (what the predicate actually compares)

From `plans/round-36-claims.md` (P36-C1), `tools/round-36/c1-run.sh`,
`tools/round-36/c1-counter.py`, and unblob 26.6.4's handler:

| Element | Reconstructed behaviour | Evidence |
|---|---|---|
| Tool under test ("after") | unblob `SquashFSExtractor` spawns `sasquatch -le -no-exit-code -f -d <outdir> <inpath>` for every LE v4 carrier | `~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py:24-66` (read directly; matches peer `R36ScoutUnblobHandler`) |
| Oracle production | `/usr/bin/unsquashfs -no-progress -o <off> -d <scratch/root> <carrier>`, then `os.walk` → `relpath TAB sha256 TAB size`, symlinks and non-regular files skipped, rows sorted | `tools/round-36/c1-run.sh:36-60` |
| Oracle comparison | `matched()`: for each oracle row, some published file must have **equal sha256** and equal relative path, or path ending `/<oracle-rel>`; pass requires `after_oracle_hits == oracle_files` | `tools/round-36/c1-counter.py:132-139`, `:175-190` |
| Gap arm | `sasquatch_gap()` only looks at `extraction_gaps[].kind == missing-extractor-dependency` with `sasquatch` in `dependencies` | `c1-counter.py:118-124` |
| What is *not* compared | anything about symlinks, xattrs, modes, ownership, empty directories, or extra files published beyond the oracle set | same code |

Two consequences that matter for §6 and §9: (a) the oracle is regular-files-only by construction, so K2's
frozen symlink `var/notice-link` never crosses the comparison; (b) the check is a **sha256 equality
between two extractions of the same image**, so any fault that both extractors make identically is
invisible.

**Harness reproduced.** `tools/round-36/c1-run.sh oracle` (with `HYAKU_SCRATCH` pointed at my scratch,
outdir in scratch — nothing written in the lane) on K1 and K3:

```
$ tools/round-36/c1-run.sh oracle <lane>/corpus/.../fixtures/k1-le-xz.sqsh $S/h1     # exit 0
{"mode":"oracle","carrier":"...k1-le-xz.sqsh","carrier_sha256":"93802938486d952a…b8a589",
 "utc":"2026-10-26T04:40:57Z","squashfs_offset":0,
 "unsquashfs":"unsquashfs version 4.7.5 (2026/03/01)","regular_files":3}
$ tools/round-36/c1-run.sh oracle $S/k3.appimage $S/h3                               # exit 0
{"mode":"oracle","carrier":"…/k3.appimage","carrier_sha256":"b644d034746aed32…35f29fb",
 "utc":"2026-10-26T04:40:57Z","squashfs_offset":944632,
 "unsquashfs":"unsquashfs version 4.7.5 (2026/03/01)","regular_files":2130}
```

Both `oracle.tsv` files are byte-identical (`diff` exit 0) to my independent `unsquashfs` runs. The
frozen oracle is exactly unsquashfs 4.7.5 at the declared offsets.

---

## 2. Provenance chain — both binaries pinned to source

### 2.1 sasquatch 4.5.1 (the tool under test)

```
$ strings -a ~/.local/bin/sasquatch | grep -m1 "unsquashfs version"
unsquashfs version 4.5.1 (2022/03/17)
$ sha256sum ~/.local/bin/sasquatch
ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754   (382824 B)
$ cp /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round8/work/sasquatch.deb . && ar t sasq.deb
debian-binary  control.tar.xz  data.tar.xz
$ tar xJf control.tar.xz -O ./control | head -3
Package: sasquatch
Version: 1.0
Architecture: amd64
$ tar xJf data.tar.xz ./usr/bin/sasquatch && sha256sum usr/bin/sasquatch
ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754   ← identical
```

- deb sha256 `efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95` = the GitHub release
  digest recorded by peer `R36ScoutSasquatchRelease` (release tag `sasquatch-v4.5.1-6`, published
  2026-01-27). `dpkg-deb` is absent on this host; `ar` + `tar` used instead.
- deb `Description: Tool to extract vendor specific SquashFS images`; `Depends: liblz4-1, liblzma5,
  liblzo2-2, libstdc++6, libzstd1, zlib1g` — i.e. it links the **system** codecs, not vendored ones.
- Source: `https://codeload.github.com/onekey-sec/sasquatch/tar.gz/refs/heads/main` → HTTP 200,
  498312 B. The tree is a complete squashfs-tools 4.5.1 tree (`README-4.5.1`, `RELEASE-READMEs/`,
  `version.mk` → `HASH := b34aa5ef`, `FULLDATE := 2026-04-13`) plus a `debian/` dir. `squashfs-tools/README.md`:
  *"This is the raw, patched source code for squashfs-tools."*
- **Source↔binary closed behaviourally:** `make sasquatch` in that tree (needs `CXX` because the
  shipped target links the C++ LZMA SDK; `make unsquashfs` links via `CC` and is *not* the shipped
  artifact) produced a 472960 B binary reporting `unsquashfs version 4.5.1 (2022/03/17)` whose
  extraction manifests are **identical** to the installed deb binary on all four carriers (§7), and
  which reproduces the vendor-magic tolerance behaviour (§5).

### 2.2 unsquashfs 4.7.5 (the oracle)

```
$ unsquashfs -version | head -1          → unsquashfs version 4.7.5 (2026/03/01)
$ pacman -Qo /usr/bin/unsquashfs         → owned by squashfs-tools 4.7.5-1   (build date 2026-03-02)
$ sha256sum /usr/bin/unsquashfs          → 461e1fd9eac39c12e673042807459985636030d5557319343fc3a6ed4ba1677c
```

`https://codeload.github.com/plougher/squashfs-tools/tar.gz/refs/tags/4.7.5` → HTTP 200, 412571 B;
built in scratch (`make unsquashfs`, exit 0) → `unsquashfs version 4.7.5 (2026/03/01)` with
`-DGZIP_SUPPORT -DLZO_SUPPORT -DLZ4_SUPPORT -DXZ_SUPPORT -DZSTD_SUPPORT -DXATTR_SUPPORT`, and its
extraction manifests are **identical** to `/usr/bin/unsquashfs` on K1, K3, K4. The source I analysed
is therefore the code of the frozen oracle.

(4.5.1 tarball: `…/tags/4.5.1` → HTTP 200, 270114 B. `codeload` 404s for `refs/tags/v4.5.1` and
`refs/heads/master`; GitHub API tag listing was rate-limited — see Limits.)

---

## 3. Patch scope: sasquatch ≡ squashfs-tools 4.5.1 + 2.00 %

Diff of the two full source trees (`*.c *.h`, 63 files, 34314 lines):

| metric | value |
|---|---|
| files byte-identical | **41** |
| files changed | **22** |
| changed lines (`diff -u \| grep -c '^[+-][^+-]'`) | **685 / 34314 = 2.00 %** |

Changed files, by changed-line count: `lzma_wrapper.c` 295 (adds three extra LZMA decompressor ops),
`unsquashfs.c` 226, `compressor.c` 95, `unsquash-3.c` 38, `squashfs_fs.h` 37, `unsquash-4.c` 22,
`unsquash-2.c` 17, `compressor.h` 10, `squashfs_compat.h` 10, plus small edits in `read_fs.c`,
`swap.c`, `unsquash-1.c`, `unsquash-123.c`, `mksquashfs.c`, `process_fragments.c`, and five
`*_wrapper.h`.

Semantic surface of the patch (read from the diff, comment tag `CJH:`):

1. **Compressor fallback dispatcher** — new `compressor_uncompress()` tries the declared compressor,
   then every other decompressor, remembering the winner (`detected_compressor_index`). Three extra
   LZMA variants registered.
2. **Superblock acceptance** — endianness inferred when `s_magic` is not trustworthy; *"Non-standard
   SquashFS Magic"* is only a warning; `-be/-le/-major/-minor/-C` options added;
   `check_compression()` now continues on an unsupported compressor (`// CJH: Try to continue anyway`).
3. **Directory-loop detection** — `inumber_lookup()` guard added at the four `dir_scan`/`pseudo_*`
   recursion sites (`ERROR(...); return FALSE;`).
4. **Error tolerance** — `read_block`/`inflator` stop printing "uncompress failed"; decompressed-size
   mismatch is reported but not fatal; `processors = 1` default; `-no-exit-code`.
5. C23 prototype fixes (`sigwinch_handler(int)`, `sigalrm_handler(int)`), which the release body lists
   as PR #32 and which are *needed* on gcc 15+: the unpatched 4.5.1 tarball fails to build here with
   `passing argument 2 of 'signal' from incompatible pointer type [-Wincompatible-pointer-types]`.

Binary corroboration that the installed artifact is this patched tree and not stock 4.5.1
(string present in source+binary, absent from the 4.5.1 tarball):

| string | stock 4.5.1 src | sasquatch src | installed binary |
|---|---|---|---|
| `Trying to decompress using default` | 0 | 1 | 1 |
| `Successfully decompressed with default` | 0 | 1 | 1 |
| `Non-standard SquashFS Magic` | 0 | 1 | 1 |
| `Decompressed size did not match the expected size` | 0 | 1 | 1 |
| `File System corrupted: directory loop detected` | 2 | 4 | 1 |

and 4.7.5-only markers (`help-all`, `USAGE-UNSQUASHFS.md`) are absent from it. Unique-binary-string
overlap: 949 (sasquatch) vs 893 (oracle) unique strings, **553 shared**, 128 of them
squashfs/reader/dir/inode/decompress/superblock strings; sasquatch-only strings are its patch strings
plus C++ RTTI (`_ZTVN10__cxxabiv117__class_type_infoE`, `__cxa_throw`).

---

## 4. Shared code inventory, 4.5.1 → 4.7.5 (function level)

Changed lines per function, from `diff -U0` mapped onto 4.7.5's top-level function ranges:

| function (file) | changed lines | nature of the change |
|---|---|---|
| `squashfs_readdir` (unsquashfs.c) — directory-entry iterator | **0** | only `int` → `static int` |
| `dir_scan` (unsquashfs.c) — recursive walk, creates the tree | **7** | `static`; **loop check** (`EXIT_UNSQUASH`); `ASPRINTF` macro; `res` declarations moved |
| `read_block` (unsquashfs.c) — block/fragment decompress glue | **2** | `malloc`+NULL test → `MALLOC()` macro |
| `squashfs_opendir` (unsquash-4.c) — directory table open | **3** | bounds/robustness |
| `read_inode` (unsquash-4.c) — inode decode for all types | **9** | `time_opt` override; *new* negative-`file_size` rejection; `MALLOC()` |
| `create_inode` (unsquashfs.c) — writes dirs/files/links/devices | **17** | mode/time handling |
| `read_super_4` (unsquash-4.c) | **24** | **entirely** streamed-filesystem support (superblock at end of file) |
| `read_fs_bytes` (unsquashfs.c) | **8** | refactor onto `read_bytes()`; same semantics |
| `read_fragment_table`, `read_id_table` (unsquash-4.c) | 1 each | diagnostics |
| `xz_uncompress`, `gzip_uncompress`, `zstd_uncompress`, `lz4_uncompress`, `lzo_uncompress` | **0** each | **byte-identical** after whitespace normalisation; also identical in sasquatch |

The churn is elsewhere: `unsquashfs.c` is 33.1 % changed *by line*, but the changed lines sit in
`parse_options` 186, `parse_cat_options` 75, `check_sqfs_cmdline` 50, `option_with_arg` 47,
`exclude_match` 39, `pseudo_print/generate_pseudo` 36, `main` 19, `read_super` 9 — CLI/help/exclude/
pseudo generation, not extraction semantics. Wrapper churn is likewise option/usage code
(`zstd_wrapper.c`: `zstd_options` 15, file-scope 15, `option_args` 4, display 4 — not
`zstd_uncompress`; `lzo_wrapper.c`: `lzo_usage` 8, init 4; `lzma_xz_wrapper.c`: `lzma_usage` 1).

**Runtime codec sharing (the sharpest point):** both binaries load the *same* shared objects:

```
$ ldd /usr/bin/unsquashfs   → libz.so.1 liblzo2.so.2 liblz4.so.1 liblzma.so.5 libzstd.so.1 libm
$ ldd ~/.local/bin/sasquatch→ libpthread libz.so.1 liblzma.so.5 liblzo2.so.2 liblz4.so.1 libzstd.so.1
                              libstdc++ libm
system versions: xz 5.8.4-1, zlib 1:1.3.2-4, zstd 1.5.7-3, lz4 1:1.10.0-2, lzo 2.10-5
```

So for the frozen carriers the two "independent" extractors are: the same wrapper functions
(byte-identical `*_uncompress`), calling the same codec code mapped from the same files. On the
decompression axis there is **no** independence, not even at the library level. (Cf. the AppImage
runtime in §8, which statically embeds its own zstd 1.5.6.)

---

## 5. Where they are genuinely different

| axis | sasquatch 4.5.1 | unsquashfs 4.7.5 |
|---|---|---|
| image acceptance | tolerates non-standard magic, unknown compression, wrong endianness guess (falls back to the other endian) | rejects unknown magic; adds *streamed* SquashFS (magic at end, `read_super_4` +24 lines) |
| decompression | tries every registered codec until one works | uses the declared codec only |
| directory loops | `ERROR(...); return FALSE;` at four recursion sites | `EXIT_UNSQUASH("… directory loop detected")` at `dir_scan` |
| error handling | `-no-exit-code`, size mismatch non-fatal, `read_block` errors silent | errors fatal; diagnostics |
| sparse files, xattrs | 4.5.1 code | 4.7.3 SEEK_DATA path; `read_xattrs.c` 20.5 % changed |
| CLI/help/pager/excludes | 4.5.1 | rewritten (`help-all`, pager, regex help) |

**Observed divergence falsifier** — K1 copy with the 4 magic bytes rewritten `hsqs` → `XSQ!`:

```
$ /usr/bin/unsquashfs -no-progress -o 0 -d v-uq vend.sqsh      # exit 1
FATAL ERROR: Can't find a valid SQUASHFS superblock on vend.sqsh
$ ~/.local/bin/sasquatch -no-progress -o 0 -d v-sq vend.sqsh   # exit 0
Non-standard SquashFS Magic: 'XSQ!'
… created 3 files / 2 directories     → README.txt etc/config.ini payload.bin (all 3 extracted)
$ <source-built sasquatch> …                                    # exit 0, same 3 files (patch reproduced)
```

Divergence exists exactly where the patch lives, i.e. in *whether an image is accepted*, not in how a
vanilla image's tree is decoded.

---

## 6. Could a shared bug make both agree on a wrong tree? Yes — four concrete channels

1. **No integrity data in the format.** SquashFS 4.0 stores no checksum: `grep -ci "checksum\|crc32"
   4.7.5/squashfs-tools/squashfs_fs.h` → **0**; the v4 superblock (read from source) has
   `s_magic, inodes, mkfs_time, block_size, fragments, compression, block_log, flags, no_ids,
   s_major, s_minor, root_inode, bytes_used, id_table_start, xattr_id_table_start,
   inode_table_start, directory_table_start, fragment_table_start, lookup_table_start` — no digest
   field. `c1-run.sh` hashes the *extracted files*, which validates transport, not decoding. A codec
   that returns a correct-length wrong block produces two identical wrong sha256s and the predicate
   passes.
2. **Decompression is shared twice over** (§4): byte-identical `*_uncompress` wrappers plus the same
   `liblzma.so.5` / `libz.so.1` / `libzstd.so.1` images. Any fault in those libraries is common-mode
   by construction; the block/fragment size accounting around them changed by 3 lines in total
   (`read_block` 2, `read_fragment_table` 1).
3. **Tree walking is shared.** `dir_scan` (7 lines), `squashfs_readdir` (0 semantic lines),
   `squashfs_opendir` (3), `read_inode` (9) — a bug in name assembly (`asprintf("%s/%s")` in both),
   inode-number bookkeeping, or directory-table offset arithmetic lands identically in both, and the
   oracle would bless it. `create_inode` — where hardlinks, symlinks and mode bits are materialised —
   is byte-identical between sasquatch and its 4.5.1 base (17 lines of drift only vs 4.7.5).

4. **Shared truncation is not detectable at all.** The counter's pass rule is
   `after_oracle_hits == oracle_files` with `oracle_files > 0` read from the frozen `K*/oracle.tsv`
   (`c1-counter.py:158-190`). If the shared walker stops early at the same directory in both tools, the
   frozen oracle is short, sasquatch's tree is equally short, every oracle row matches, and the predicate
   passes with a wrong (sub)tree. Nothing in the counter pins an expected row count. The only guards are
   counts established outside the squashfs-tools lineage — the committed source trees (3, 4) and the
   code-disjoint readers (2130, 2130). This is not hypothetical for this code area: upstream's own
   `CHANGES.md` records **4.6 (17 MAR 2023)** item "Following a symlink in Sqfscat or where
   `-follow-symlinks` option is given with Unsquashfs, incorrectly triggered the corrupted filesystem
   loop detection code" — i.e. the exact `inumber_lookup`-style guard that both sasquatch and 4.7.5 now
   carry in `dir_scan` shipped with a false positive that *dropped directory entries*. A related guard bug
   would truncate both trees identically.

Not a channel: the vendor/endianness/fallback layer (patch-only) and 4.7.x's image-acceptance work —
they change *which* images are read, not the decoded contents of a vanilla image. Measured: on all
four frozen carriers the declared compressor succeeded first time and **no** codec fallback was ever
used (`Detected … compression` count = 0 in every sasquatch log; `Trying to decompress using default …`
counts K1 1, **K2 21**, K3 1, K4 1). The K2 count of 21 is a patch quirk worth knowing:
`lookup_compressor_index("gzip")` returns **0**, which collides with the "nothing detected yet"
sentinel, so the gzip path re-runs the "default decompressor" branch per block instead of caching the
detection. [INFERENCE: that is the mechanism; only the log counts are observed.] Output is unaffected
because the default *is* gzip.

---

## 7. Measured agreement (adversarial, all four carriers)

Manifests are `relpath TAB sha256 TAB size`, regular files only, symlinks excluded (the oracle rule),
computed with `os.walk` + `hashlib` in scratch. "stock451" = squashfs-tools 4.5.1 tarball built here
with `XZ/LZO/LZ4/ZSTD/GZIP_SUPPORT=1` (its Makefile defaults compile gzip only — a default build
reports *"Filesystem uses xz compression, this is unsupported by this version"* on K1 and extracts
nothing, so the codec flags matter for K1/K3/K4; the K2 row was measured with the gzip-capable build,
K2 being gzip); "sasq-built" = the sasquatch source tree's `sasquatch` (C++ link) target built here.

| carrier | compression (superblock) | rows | unsquashfs 4.7.5 | sasquatch 4.5.1 (deb) | stock 4.5.1 | sasq-built | 7-Zip 26.04 | source tree / AppImage runtime |
|---|---|---|---|---|---|---|---|---|
| K1 `k1-le-xz.sqsh` (fixture, xz, 128 KiB) | xz | 3 | 3 | 3 (=) | 3 (=) | 3 (=) | 3 (=) | **`fixtures/k1-src` 3 (=)** |
| K2 `k2-le-gzip.sqsh` (fixture, gzip, 4 KiB) | gzip | 4 | 4 | 4 (=) | 4 (=) | 4 (=) | 4 (=), symlink written as 0-byte file | **`fixtures/k2-src` 4 (=)** |
| K3 nvim x86_64 appimage @944632 | zstd | 2130 | 2130 | 2130 (=) | 2130 (=) | 2130 (=) | 2130 (=) | **`--appimage-extract` 2130 (=)** |
| K4 nvim arm64 appimage @936456 | zstd | 2130 | 2130 | 2130 (=) | 2130 (=) | 2130 (=) | 2130 (=) | runtime is aarch64 → not runnable here |

" =" means the full manifest is byte-identical (`diff` exit 0), not merely equal counts.

Full-tree checks (directories + symlink targets, not just regular files): K1, K2, K3, K4 — unsquashfs
vs sasquatch **identical**; K3 also identical to the AppImage runtime extraction,
including `.DirIcon -> nvim.png` and `nvim.png -> usr/share/icons/…/nvim.png`; 7-Zip reproduces both
K3/K4 symlinks as symlinks but flattened K2's `var/notice-link -> ../usr/share/doc/NOTICE` into a
0-byte regular file (sha256 `e3b0c442…b855`, the empty-file digest).

Carrier integrity re-verified: K3 sha256 `b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb`
(11454968 B) and K4 `8efcec73cea1cebcd3a19da0bc782c0c6d95da7ae6006902a9d93b5ac9efe1c2` (11356680 B) equal
`carriers.json`; fixture digests K1 `93802938…8a589`, K2 `ce5bf60e…2084f` equal too. Payload offsets
derived from the ELF header (`e_shoff + e_shnum*e_shentsize`) are 944632 (K3) and 936456 (K4), both
carrying `hsqs`.

---

## 8. Which carriers have an oracle that shares no code — per carrier

**K1, K2 — yes, already committed in the repo.** `fixtures/k1-src` and `fixtures/k2-src` are the
input trees the fixtures were built from; they contain no squashfs reader at all, so they are disjoint
from every extractor in play. I recomputed their manifests and they equal the frozen-oracle rule
exactly (3/3 and 4/4 rows). Independent of the squashfs lineage *and* of `mksquashfs`: mksquashfs
4.7.5 shares `squashfs_fs.h` and the compressor wrappers with the oracle, so a writer bug is only
detected by comparing against these trees — which is exactly what the source-tree comparison does.
(Peer `R36ExecSourceTreeOracle` reached the same result and additionally reproduced both fixture
digests by rebuilding from the trees.)

**K3 — yes, and verified.** The AppImage's own type-2 runtime
(`https://github.com/AppImage/type2-runtime/commit/8f39b89`, `squashfuse 0.5.2` from
vasi/squashfuse, plus libfuse) extracts via `--appimage-extract` with **no external extractor** —
`strings k3.appimage | grep -c unsquashfs` → **0** — and its regular-file manifest equals the oracle
2130/2130, as does the full tree. Its codecs are statically embedded (no `libzstd.so`/`liblzma.so`
strings; embedded zstd reports **1.5.6**, while the system both unsquashfs and sasquatch use is
**1.5.7**). So on K3 the decompression code is disjoint as well. Peer `R36ExecAppImageExtract`
reproduced this twice.

**K4 — yes, but not via the runtime.** The aarch64 AppImage's runtime cannot execute on this host
(no `qemu-aarch64`, no binfmt), so that route is unavailable — that is what peer
`R36ExecAppImageExtract` reported as "no second oracle". **Correction (advisory):** 7-Zip 26.04's own
SquashFS implementation (`7zip 26.04-1`, `File System = SquashFS 4.0`) reads the K4 payload directly
and reproduces the oracle's 2130 regular files with equal sha256 and size, and the two symlinks; same
result on K3. 7-Zip shares no code with squashfs-tools (independent C++ implementation, own bundled
codecs). Its known limitation is symlink policy — observed on K2 — so it is a regular-file-content
oracle, not a tree-shape oracle.

**7-Zip works on all four carriers** (K1 3/3, K2 4/4 regular files, K3 2130, K4 2130) and is the
cheapest cross-family check available in this environment.

So: the *frozen* oracle is code-shared on all four; a *code-disjoint* oracle exists and agrees on all
four (source trees for K1/K2, runtime for K3, 7-Zip for all four, runtime unavailable for K4).

---

## 9. Bounded verdict

| claim | verdict | confidence |
|---|---|---|
| sasquatch 4.5.1 is a patched squashfs-tools 4.5.1 reader (2.00 % of lines, 22 of 63 files) | **established** (source diff + patch strings in the deb binary + source-built binary behaviourally identical on K1–K4) | high |
| oracle `/usr/bin/unsquashfs` 4.7.5 and sasquatch share the directory-walk, inode-decode and decompression code paths | **established**: `squashfs_readdir` 0 semantic lines, `dir_scan` 7, `squashfs_opendir` 3, `read_inode` 9, `create_inode` 17, `read_block` 2; all five `*_uncompress` byte-identical | high |
| they even share the codec implementation at run time | **established**: same `liblzma.so.5` / `libz.so.1` / `libzstd.so.1` / `liblz4` / `liblzo2` in both processes | high |
| a shared bug in those paths would produce a wrong tree that the predicate accepts | **structurally established**, not demonstrated with a real bug: SquashFS v4 carries no checksum, the predicate compares two extractions by sha256, and there is no third-party arbiter in the counter | medium-high (inference from shared code + absent integrity data) |
| for the four frozen carriers the patch layer is inert, so the tool under test behaves as plain 4.5.1 | **established empirically**: stock 4.5.1 built here and the source-built sasquatch both reproduce the deb sasquatch's manifests exactly; zero codec fallbacks fired | high |
| the tree the oracle publishes is correct | **corroborated independently** for K1/K2 (committed source trees), K3 (`squashfuse 0.5.2`), all four (7-Zip 26.04) | high for the assertable set; K4 lacks a *runtime* oracle on this host |

**Wording finding (report, not repair).** `plans/round-36-claims.md:24` and the harness header call the
oracle "the frozen **independent** unsquashfs oracle". That is true only in the sense "outside the REA/
unblob pipeline". It is not implementation-independent of sasquatch.

The knowledge entry that has since landed (`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`,
untracked at the time of writing) is **already honest in its limits section** and I confirm its claims
against my measurements:

- line 17 (intro): "…the member-level outcome on four frozen carriers against an independent `unsquashfs`
  oracle" — the one unqualified use; everything later is qualified.
- lines 163-167: "The oracle is `unsquashfs`'s view of the same payload bytes that sasquatch reads, and
  both come from one code family… Agreement is member parity between two versions of one lineage, not two
  independent implementations." **Correct, and my §3-§4 quantify it** (2.00 % patch; ≤17 changed lines in
  each of the walk/inode/decompress functions — the one 24-line item, `read_super_4`, is streamed-image
  acceptance, not tree decoding; all five `*_uncompress` byte-identical; shared codec `.so`).
- lines 160-163: "**K1/K2 have an independent expected record**: their oracle rows equal the committed
  source trees … byte for byte, so for these two the oracle is not merely a second reader of the same
  payload." **Correct** (I recomputed 3/3 and 4/4), but note the *compared* artifact in the counter is
  still `K*/oracle.tsv` (unsquashfs); the source trees are corroboration, not the counted record. If the
  claim ever wants the count to lean on an implementation-independent artifact, the source-tree manifests
  are the thing to compare in the counter — that is a predicate change, so out of scope here.
- line 169: "K4 rests on the unsquashfs oracle alone" — true for *runtime* oracles; **refined above**:
  7-Zip 26.04 supplies a code-disjoint K4 check (2130/2130). Note that this is 7-Zip used as an
  independent reader, not a re-test of the 7z *fallback path* inside unblob, which the entry correctly
  still declines to claim.

I changed nothing frozen and recommend no predicate change: the target is already met, and the evidence is
stronger with the corroboration attached.

---

## 10. Limits of this seat

- GitHub API was rate-limited (`{"message":"API rate limit exceeded …"}`), so the sasquatch tag list
  and tag→commit sha were not fetched; the source analysed is `refs/heads/main` (2026-04-13). The
  release tag (`sasquatch-v4.5.1-6`, 2026-01-27) and the deb digest come from peer
  `R36ScoutSasquatchRelease`. Source↔binary is established *behaviourally* (identical manifests + the
  patch's own log/error strings), not by byte-reproducing the shipped build.
- 4.7.5 could be built here; 4.5.1 needs `-Wno-error=incompatible-pointer-types` (the C23 issue the
  sasquatch release fixes); the sasquatch tree needs the `sasquatch` (C++ link) target, not
  `unsquashfs`.
- I did **not** hunt for an actual shared bug, so "a shared bug would pass" stays an inference from
  code identity plus the absence of checksums. Deliberate fault injection (e.g. LD_PRELOAD into
  `lzma_code`) was considered and rejected as evidence: it would demonstrate that identical input
  yields identical output, not that the code is shared.
- Not examined: xattr handling (the oracle ignores xattrs; `read_xattrs.c` diverges 20.5 %), big-endian
  / AVM images, `sasquatch-v4be` (never spawned for the four LE carriers — peer
  `R36ScoutUnblobHandler`), 4.7.5's sparse/`SEEK_DATA` path, and whether 7-Zip's K2 symlink flattening
  is a policy or a defect.
- K4 has no executable runtime oracle here; the 7-Zip K4 result is the only code-disjoint K4 check I
  could run.

---

## 11. Hygiene / tooling record

- Scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36RevengerOracle`, `TMPDIR="$S"`, removed before yield;
  `/tmp` used only for two transient diff files. Everything cited above was produced in scratch and is
  quoted verbatim here (no evidence path points at scratch).
- Wrote exactly one lane file: this report. No VCS command beyond read-only `git status --porcelain`,
  `git rev-parse`.
- No tool installed or upgraded: used existing `curl`, `ar`, `tar`, `make`, `gcc 16.2.1`, `7z`
  (`7zip 26.04-1`), `/usr/bin/unsquashfs` (squashfs-tools 4.7.5-1), `~/.local/bin/sasquatch`
  (sasquatch 1.0 deb, sha256 `ad02d27a…4754`), `python3 3.14.8`. No pacman transaction was attempted.
- Sources fetched (scratch only, HTTP 200): squashfs-tools tags `4.5.1` (270114 B) and `4.7.5`
  (412571 B); `onekey-sec/sasquatch` `refs/heads/main` (498312 B); neovim v0.12.6
  `nvim-linux-x86_64.appimage` (11454968 B) and `nvim-linux-arm64.appimage` (11356680 B), both matching
  the frozen digests.
