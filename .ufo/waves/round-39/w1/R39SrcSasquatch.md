DONE — sasquatch-v4be source opened and pinned: `-be` only sets a `swap` flag; the v4 byte order is compiled in by `-DFIX_BE`, so v4be reads only BE v4 (and plain reads only LE v4). One SOURCES row drafted. Installed binaries match the release digests.

# R39SrcSasquatch — sasquatch / sasquatch-v4be source behaviour

Seat: R39SrcSasquatch. Artifacts: `.ufo/waves/round-39/w1/artifacts/R39SrcSasquatch/`. Nothing installed or upgraded. No REA run, no K5/K6 or held-out carrier touched.

## 1. Pin

- Repo: https://github.com/onekey-sec/sasquatch
- Tag `sasquatch-v4.5.1-6`, annotated commit `15573bf46c671c8ed23e8c0c50e6187e0c8d0b62` (2026-01-23, "fix: remove unnecessary magic checks"). It is the latest `sasquatch-v*` tag and also the release published 2026-01-27T11:57:51Z.
- GitHub API (access 2026-10-26T16:38:54Z, HTTP 200): `/repos/onekey-sec/sasquatch/releases` and `/tags`, trimmed copy in `api-release-and-tags.json`.
- Release body names only 3 PRs: #33 CI, #32 C23 prototypes, #34 magic checks. No `-be` or endianness notes. Notes for `-4` and `-5`, the other tags I read, say nothing on endianness either.
- Raw fetch at the tag (access 2026-10-26T16:42:30Z to 16:42:34Z, all HTTP 200). Each file is byte-identical to a `git clone` checkout at the tag (`raw-fetch-index.txt`):

| file | lines | sha256 |
|---|---|---|
| `squashfs-tools/unsquashfs.c` | 4619 | `ece42b66f37ba67707c2c51b47b643c027232153705f59d238da79958a54cb40` |
| `debian/rules` | 23 | `b49d25e9f17ca3806c8ea83d52c4807509f6ad333c63b38385a2485f80f6d885` |
| `squashfs-tools/squashfs_swap.h` | 425 | `997c221dce59067528c5867173b2927c7bb1519d55bdfe6b80bf80da16cdb0e4` |
| `squashfs-tools/swap.c` | 117 | `832143441689e7a3743a85eb5a54be26d1f3298b193c52fd585433f12da77c03` |
| `.github/workflows/release.yml` | 47 | `d2c72f8b7341c686c730512c23e840482cf7870446ac5a33c7548f884d1f0e69` |
| `README` (root) | 9 | `ce4b10a959aea87324775ea68b06ee9fc9287f34fe8258947fe18aa934c19137` |

The root `README` is an unrelated 9-line 2022 "NEWS" note. The tag has no prose doc for `-be`, so the code and the commit message are the primary sources. Line-numbered excerpts are in `source-excerpts.txt`.

## 2. What `-be` does (`unsquashfs.c`; the binary is named `sasquatch`)

- Lines 3941-3942 (help): "-be Treat the filesystem as big endian" / "-le Treat the filesystem as little endian".
- Lines 4389-4400, the flag parser:
  - `-be` becomes `#if __BYTE_ORDER == __BIG_ENDIAN swap = 0; #else swap = 1;`. On a little-endian host (this machine) `-be` sets `swap = 1`.
  - `-le` sets `swap = 0` on an LE host. The flags only set the global `swap` int (declared `swap = -1` at line 58).
- `swap` is consulted only in `read_block` (lines 664-668, byte-swaps the 2-byte metadata `c_byte`) and in the v1/v2/v3 readers (`unsquash-1.c`, `-2.c`, `-3.c`).
- `swap` is never referenced in `unsquash-4.c`. The v4 superblock goes through the `SQUASHFS_INSWAP_SUPER_BLOCK` macros (line 697). Those macros are real swaps only when `__BYTE_ORDER == __BIG_ENDIAN || defined FIX_BE` (`squashfs_swap.h:32`, `swap.c:24`).
- Origin commit `0c65f00de7c7cc3382302256fddd06ba10ed7b01` (Marton Illes, 2022-02-23, "support for v4 bigendian filesystems (#2)"). It states the design:
  - "for the v4 extraction logic the swap variable is ignored and macro magic is used to do the swapping"
  - "just enable a compile time flag hardcode BIG endian operation"
  - "would create a special sasquatch binary that would work on v4 BIG endian images"
  - "compile it twice and have a normal and a be version"

## 3. The endianness-mismatch message

`unsquashfs.c` `read_super`, lines 2252-2285, only when `swap == -1` (no `-be`/`-le` given):

- Line 2263-2265 condition: `s_major < SQUASHFS_MIN_VERSION(1) || s_major > SQUASHFS_MAX_VERSION(5) || (inodes & 0xFF) == 0`. The fields are read in host order from the 32-byte generic header.
- Lines 2267-2268, printed when the condition is true: "SquashFS version [%d.%d] / inode count [%d] suggests a SquashFS image of a different endianess".
- Lines 2277-2278, printed when it is false: "... of the same endianess".
- Both messages are advisory. They only choose the default `swap`:

| build | condition true ("different") | condition false ("same") |
|---|---|---|
| plain | `swap = 1` (2272) | `swap = 0` (2282) |
| FIX_BE | `swap = 0` (2270) | `swap = 1` (2280) |

- Lines 2293-2296 additionally print "Reading a different endian SQUASHFS filesystem on %s" whenever `swap != 0` (also after `-be` on an LE host).
- A standard BE v4 image read on an LE host shows `[1024.0]`, because 0x0400 is read little-endian. That trips the "different endianess" branch. In v4be that branch picks `swap = 0`, the wrong value for `read_block`.
- Result: v4be without `-be` fails (§5).

## 4. sasquatch-v4be versus sasquatch

- `debian/rules` lines 15-18 (`override_dh_auto_install`) build the same `squashfs-tools` twice. The second pass is `CFLAGS=-DFIX_BE dh_auto_build`, then `cp ... sasquatch-v4be`. Quote: "CFLAGS=-DFIX_BE dh_auto_build".
- `release.yml` builds the Debian package (bullseye, amd64/arm64/arm) with `dawidd6/action-debian-package`, so both binaries ship in one `.deb`.
- FIX_BE touches 12 files in `0c65f00` (`stat` read): `squashfs_swap.h`, `swap.c`, `squashfs_compat.h`, `unsquash-1/2/3.c` (one `#if` line each), `gzip/lz4/lzo/xz/zstd_wrapper.h` (their swap guards) and `unsquashfs.c` (the auto-detect inversion).
- Net effect: v4be hard-wires v4 superblock/inode/dir/fragment parsing to big-endian regardless of `swap`. `swap` still drives only `read_block`'s 2-byte metadata header and the v1-v3 paths. v4be therefore needs `-be` for `read_block` to agree.

## 5. Installed binaries versus source

- `sha256sum ~/.local/bin/sasquatch` is `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`.
- `sha256sum ~/.local/bin/sasquatch-v4be` is `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`.
- Both match the amd64 `.deb` members already recorded in S107.
- `strings -a ~/.local/bin/sasquatch-v4be | grep -n -i endian`:
  - 1555: "SquashFS version [%d.%d] / inode count [%d] suggests a SquashFS image of a different endianess"
  - 1556: same with "same endianess"
  - 1558: "Reading a different endian SQUASHFS filesystem on %s"
  - 1740-1741: the `-be` / `-le` help lines
- Plain `sasquatch` has the same strings (lines 2409-2471, in a different order).
- Both report "unsquashfs version 4.5.1 (2022/03/17)".
- Behavioural check. The commands: `~/.local/bin/<bin> -no-exit-code -f [-be|-le] -d out carrier`, run in scratch on the K1 and K3 carriers copied from `corpus/evidence/round-37/c1/` (sha256 equal to the repo files), plus fresh trees from `gen-squashfs.py` (unblob's `-no-exit-code -f -d` argv). Full matrices are in `matrix-k1-k3-round37-carriers.txt` and `matrix-fresh-dev-trees.txt`.

| carrier | plain `sasquatch` | `sasquatch-v4be` |
|---|---|---|
| LE v4 gzip | auto and `-le`: extracts 3 entries; auto prints "same endianess"; `-be`: "failed to read id table block" | all flags fail: "Block size too small" |
| BE v4 gzip (gen `be`; also K1, K3) | all flags fail: "Block size too small" (auto, `-be`) or "Block size or block_log too large" (`-le`) | auto fails ("different endianess" then "failed to read id table block"); `-le` fails; **`-be` extracts** |
| K1 (BE v4) with `-be` | n/a | exit 0, 5 files |
| K3 (BE v4) with `-be` | n/a | 4 files, "Successfully decompressed" lines; shell `PIPESTATUS` 141 from `| head -6` closing the pipe (SIGPIPE), not a sasquatch exit |
| gen `avm` | all flags fail | auto and `-le` fail; `-be` extracts 3 entries |
| gen BE xz | all flags fail | `-be`: 3 entries created, then FATAL "writer: failed to read/uncompress file o/.../d/n.txt" (cause not investigated) |

- Fresh-tree sha256 values are in `carrier-sha256.txt`. The trees are in `dev-tree/`. The carriers are K1 `1cfb6c33…`, K3 `9c7c523c…`, and four dev carriers `dev-le`, `dev-be`, `dev-avm`, `dev-be-xz`.
- On the gen `avm` carrier, `-be` extracts even though unblob (S108) omits `-be` for AVM. The generator only mimics the `mkfs_time == bytes_used` marker, so this says nothing about real AVM-BE images [INFERENCE].
- Triage use: the "different endianess" line is a heuristic hint, not a verdict. A BE v4 image prints it under both binaries, yet only v4be with an explicit `-be` can extract it. A v4be run without `-be` that ends in "read_id_table: failed to read id table block" is a flag or endianness mismatch. "Block size too small" from either binary means the wrong binary/endianness pairing, or a really corrupt image.

## 6. Draft SOURCES row (11 columns; L1 assigns the id, next free is S118)

```
| S118 | onekey-sec/sasquatch source at tag sasquatch-v4.5.1-6 — https://github.com/onekey-sec/sasquatch/tree/sasquatch-v4.5.1-6 (raw: https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/squashfs-tools/unsquashfs.c) | code | A | What `-be`/`-le` do, when the "different endianess" message prints, and how the sasquatch-v4be build differs from plain sasquatch, at one tag only; not unblob's argv decision, not REA's gap wording, not later commits, not any carrier | tag sasquatch-v4.5.1-6 = commit 15573bf46c671c8ed23e8c0c50e6187e0c8d0b62 (2026-01-23); `squashfs-tools/unsquashfs.c` 4619 lines sha256 ece42b66f37ba67707c2c51b47b643c027232153705f59d238da79958a54cb40: lines 4389-4400 `-be` -> "swap = 1" on an LE host, 2252-2285 auto-detect inverted under FIX_BE, 2267-2268 "suggests a SquashFS image of a different endianess", 2294-2296 "Reading a different endian SQUASHFS filesystem"; `debian/rules` 23 lines sha256 b49d25e9f17ca3806c8ea83d52c4807509f6ad333c63b38385a2485f80f6d885 line 17 "CFLAGS=-DFIX_BE dh_auto_build" then `cp` to sasquatch-v4be; `squashfs_swap.h:32` and `swap.c:24` "#if __BYTE_ORDER == __BIG_ENDIAN \|\| defined FIX_BE"; commit 0c65f00 "for the v4 extraction logic the swap variable is ignored"; installed ~/.local/bin/sasquatch-v4be sha256 fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6 and sasquatch ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754 equal the S107 release members; opened 2026-10-26T16:38Z-16:43Z HTTP 200 | v4be hard-wires v4 parsing to big-endian at compile time and `-be` only supplies the `read_block` swap; plain sasquatch cannot read BE v4 and v4be cannot read LE v4; the "different endianess" message is an advisory heuristic, so a v4be run without `-be` that dies with "failed to read id table block" is a flag mismatch, not a corrupt image | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md |
```

Sanity check on the row: the tier-A source is one tag's code. S107 already covers the release assets, S108/S112 the unblob argv, and S114 the AVM semantics, so this row has no scope overlap with them. The `\|` is a Markdown-table escape; confirm the table renders as 11 cells.

## 7. Tools, limits, hygiene

- Tools: curl, git clone (read-only, into scratch), `strings`, `nm`, and the installed sasquatch binaries. No install, upgrade or pacman call. `RULES.md` read (channel order; pacman paused, not needed).
- Slip, corrected: my first `bash` call died on a `cd` and ran in the fleet root. It left three curl output files there: `f96fe7.out`, `234826.out`, `f8923e.out`. I moved the two I needed into scratch, deleted the third, and did not touch other fleet files. The fleet root listing shows none of them now. No VCS commands were run there beyond reading.
- `swap`/FIX_BE conclusions come from reading the source plus black-box runs. I did not disassemble the binary beyond the string and sha checks.
- Not verified: K2 and K4 were not run through sasquatch here, REA behaviour was not tested, and the gen-xz BE failure is uninvestigated.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r39/R39SrcSasquatch` is removed at the end of this report.
