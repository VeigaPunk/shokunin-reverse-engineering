# R42C1Sentinel — probe log (commands, outputs, exit codes)

All probes 2026-10-26, cwd `S=/fast/scratch/hyaku/kaidoku-r42/R42C1Sentinel` unless a
command says otherwise; `TMPDIR=$S`. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
at base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c` (read-only). No lane file was written by
any probe. Host tools: python3 3.14, git, curl, `unsquashfs` 4.7.5 (2026/03/01),
7-Zip 26.04 (x64), `sasquatch`/`sasquatch-v4be` 4.5.1 in `~/.local/bin`, unblob 26.6.4
(`/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`, sha256
`0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`), `npx` from
`/run/user/1000/fnm_multishells/5071_1793027685454/bin/npx`, `rea-agents@6.5.0` cached at
`~/.npm/_npx/ad9a3fdbcad992c6`.

## P1 — large blobs at the base (`git ls-tree -r -l`)

    git ls-tree -r -l c4a38ea2 | awk '$4>1048576'            # 51 blobs, 156,406,692 B
    git ls-tree -r -l c4a38ea2 -- corpus/evidence | awk '$4>1048576'   # 6 blobs
    git cat-file blob <h> | head -c 4 | xxd -p               # ELF=7f454c46, ZIP=504b0304

Full table: `scan-large-blobs.tsv`. Binary subset (10 blobs, 17,973,892 B):

    2,939,928 ELF  corpus/evidence/round-34/elf/e10.bin
    2,939,928 ELF  .ufo/waves/round-34/prep/R34Expected-files/corpus/evidence/round-34/elf/e10.bin
    2,939,928 ELF  .ufo/waves/round-34/prep/R34Expected-files/corpus/evidence/round-34/elf-meta/m10.bin
    2,276,644 ZIP  .ufo/waves/arc3-loop1-round4/claims/c1/EX-02/pycryptodome-3.24.1-...whl
    1,195,144 ELF  corpus/evidence/round-34/elf/e05.bin + prep elf/e05.bin + prep elf-meta/m05.bin
    1,097,344 ELF  corpus/evidence/round-34/elf/e11.bin + prep elf/e11.bin + prep elf-meta/m11.bin

Identity of the ELFs (`.ufo/waves/round-34/expected.json` `source_path`): e05 `/usr/bin/bash`,
e10 `/usr/lib/libstdc++.so.6.0.36`, e11 `/usr/bin/net` (Samba); e01..e12 are copies of the
build host's Arch packages, "byte-for-byte copy of independent public originals"
(`.ufo/waves/round-34/input-transfer.json`). No licence text, source offer or notice is
committed for any of them; `corpus/evidence/round-34/elf` = 7,329,800 B, the prep copy
duplicates it under `.ufo/waves`.

## P2 — squashfs superblock scan over `corpus/evidence` + `.ufo/waves`

    24,019 distinct blobs, 479 with a squashfs v3/v4 magic at offset 0
    max hit size 447,853 B; hits >= 1 MiB: 0; total hit bytes 9,902,908
    by magic: sqsh 342, hsqs 136, qshs 1
    any hit equal to a round-41 carrier pin: none

Full table: `scan-squashfs-magic.tsv`. Every hit is a lane-built synthetic test image, e.g.
`00883652…` = `.ufo/waves/round-40/w1/artifacts/R40C2ReconEmpty/carriers/T2-avm-xz.sqsh`
(293 B), `00670a22…` = `.ufo/waves/round-39/w1/artifacts/R39C2ReconMarker/carriers/carrier-TA-be-xz.bin`
(1,586 B). No published/vendor filesystem image is committed at the base.

## P3 — the lane reader refuses major 3 (freeze-blocking)

    python3 -I -B tools/round-41/sqfs-list.py --layout le \
        --files /dev/null --nonregular /dev/null fixtures/squashfs_v3_le.bin
    sqfs-list: unsupported SquashFS version 3.0, need 4.0        EXIT=2
    (same for --layout be on the BE fixture: EXIT=2)

Source: `tools/round-41/sqfs-list.py:243-245`
`if (self.s_major, self.s_minor) != (4, 0): raise SqfsError('unsupported SquashFS version %d.%d, need 4.0')`.
Consumers: `c1-counter.py:682 layout_probe` (→ `layout_ok`, `carve_ok`),
`c1-extra.py:41 READER = 'tools/round-41/sqfs-list.py'` (→ `oracle_rederived`),
`fetch-vendor.py:69 load_sqfs` (→ member/nested parsing when a carrier sits inside a tar).

## P4 — do the two non-sasquatch readers read v3 and agree? (fixtures, MIT)

Fixtures fetched (4096 B each):

    .../tests/integration/filesystem/squashfs/squashfs_v3/little_endian/__input__/squashfs_v3_le.bin
      0161351caec8e9da6e3e5ac7b046fd11d832efb18eb09e33011e6d19d50cd1f7
    .../squashfs_v3/big_endian/__input__/squashfs_v3_be.bin
      4e9493d9c6f868005dea8f11992129c3399e0bcb8f3a966c750cb925989ca97c
    .../squashfs_v4_le/__input__/bad_symlink.squashfs
      0c55f810260e48d4db63d02b92a0a07e0e8b04c46070a2f3ef1f2314eaab0d37

    unsquashfs -s  v3_le  -> "Found a valid little endian SQUASHFS 3:0 superblock", rc 0
    unsquashfs -lls v3_le -> squashfs-root/ (dir), apple.txt 6 B, cherry.txt 7 B, rc 0
    7z l v3_le           -> Type = SquashFS, File System = SquashFS 3.0, Big-endian = -, rc 0
    unsquashfs -lls v3_be -> "Reading a different endian SQUASHFS filesystem", same 3 rows, rc 0
    7z l v3_be           -> File System = SquashFS 3.0, Big-endian = +, same 2 files, rc 0

Symlink semantics (v4 fixture; reader behaviour is version-independent):

    unsquashfs -lls -> lrwxrwxrwx 38 squashfs-root/badlink -> /etc/ssl/private/ssl-cert-snakeoil.key
    7z l           -> Attr "....." Size 38 name "badlink"          (a REGULAR file, no type)
    7z x -y        -> lrwxrwxrwx badlink -> /fast/scratch/.../x7/etc/ssl/private/ssl-cert-snakeoil.key
    unsquashfs -d out -> lrwxrwxrwx badlink -> /etc/ssl/private/ssl-cert-snakeoil.key

## P5 — REA envelope shapes on a v3 fixture (development input, MIT)

Three runs, each `cd $S`, fresh outdir, `npx -y rea-agents@6.5.0 extract-firmware --format
json --full-output --max-depth 1`, `REA_UNBLOB_COMMAND=~/.local/bin/unblob`.

E2 (inherited PATH, real sasquatch):

    handler squashfs_v3, extraction_failed false
    files: firmware.bin_extract/apple.txt (6, 303980bc…), firmware.bin_extract/cherry.txt (7, 86baf352…)
    gaps: one structural depth-limited; diagnostics: []
    provider: unblob 26.6.4; environment: null; execution.command = /home/vgpnk/.local/share/uv/tools/unblob/bin/unblob
    the string "sasquatch" does not occur anywhere in the envelope

E3 (`PATH` with `$HOME/.local/bin` removed):

    ok true, handler squashfs_v3, extraction_failed true, files []
    gaps[0]: kind "missing-extractor-dependency", handler "squashfs_v3", dependencies ["sasquatch"]
    diagnostics[0]: missing_dependencies ["sasquatch"], report.__typename__ "ExtractorDependencyNotFoundReport"

E4b (`PATH=$S/fake:$PATH`, `fake/sasquatch` = shim that execs `/usr/bin/unsquashfs -processors 1 -f -q -d`):

    ok true, handler squashfs_v3, extraction_failed false
    file projection IDENTICAL to E2 (same rel path, same sha256, same size)
    chunks, gaps and diagnostics IDENTICAL to E2

E4 (first shim attempt without `-processors 1`) failed inside REA's prlimit sandbox
("FATAL ERROR: Failed to create thread") and exposed, on the failure path only,
`diagnostics[0].report.command = "sasquatch -le -no-exit-code -f -d …"` — the shim's own
name, not the delegated binary.

## P6 — v3 refusal also seen on `7z`-independent paths? (no; recorded to bound the claim)

7-Zip 26.04 lists and extracts the v3 fixtures, so the "7z cannot read v3" hypothesis is
false; the measured problem is lossiness, not support (P4).

## P7 — npx cache and receipt timestamps (pre-run detection)

    stat ~/.npm/_npx/ad9a3fdbcad992c6            -> 2026-10-26 18:55:31 (my own E4b run)
    stat ~/.npm/_npx/ad9a3fdbcad992c6/node_modules/.package-lock.json -> 2026-10-26 01:12:53
    envelope: no "started_at"/"finished_at"/date tokens anywhere in `data`
    envelope: parameters.output_directory = <seat scratch>/out-full

## P8 — lane root already carries a tracked extractor log

    git ls-files --error-unmatch unblob.log -> tracked
    head unblob.log -> "Logging configured extract_root=. pid=2896387";
        "Activated FS access restrictions … ReadWrite(\"unblob.log\")";
        "Running extract command command='sasquatch-v4be -be -no-exit-code -f -d …'"
    mtime 2026-10-26 03:56, input /fast/scratch/hyaku/kaidoku-r38/R38W2SymlinkUnblob/P5.sqsh

An unblob run whose cwd was the lane root left its debug log in the work tree, and the log
names the extractor command line. That is the leak channel available to a pre-freeze check.

## P9 — OpenWrt Kamikaze 7.09 image size (development class, HEAD only)

    HEAD .../kamikaze/7.09/brcm-2.4/openwrt-brcm-2.4-squashfs.trx      -> 200, content-length 1,839,104
    HEAD .../kamikaze/7.09/brcm47xx-2.6/openwrt-brcm47xx-2.6-squashfs.trx -> 200, content-length 1,904,640

A v3 firmware image is ~1.8-1.9 MB, i.e. below the round's 5 MB artifact threshold.

## P10 — redirect behaviour of `fetch()` (`redirect-demo.py`, reproduces P10 output)

    same-host redirect  bytes_ok=True how=http 200 requests=[(33031,'/start'),(33031,'/final')]
    cross-host redirect bytes_ok=True how=http 200 hosts=[(34773,'/start','127.0.0.1:34773'),
                                                         (40405,'/final','localhost:40405')]
    cache files: ['fbcbf7a7…c555.image']

## P11-P14 — post-IRC re-measurement (report §10 A1-A5)

Fixtures `squashfs_v3_adaptive/__input__/squashfs_v3_{le,be}.lzma.bin`,
`squashfs_v3/little_endian/__input__/squashfs_v3.le.1kpad.bin` (all MIT, 4096 B / 1024 B,
copied into `fixtures/`).

    unsquashfs -s   squashfs_v3_le.lzma.bin   -> SQUASHFS 3:0 superblock, rc 0
    unsquashfs -lls squashfs_v3_le.lzma.bin   -> "gzip uncompress failed with error code -3"
                                                 "read_block: failed to read block @0x84"
                                                 "FATAL ERROR: read_inode: failed to read inode 132:64"  rc 1
    7z l            squashfs_v3_le.lzma.bin   -> File System = SquashFS 3.0, Method = LZMA Spec, 2 files, rc 0
    sasquatch -le -lls squashfs_v3_le.lzma.bin-> rc 0, 2 files (stderr: gzip/lzo/... decompressor probe)
    sasquatch -be -lls squashfs_v3_le.lzma.bin-> rc 1, "FATAL ERROR: Block size or block_log too large"
    NOTE: my first reading "rc 141" was SIGPIPE from piping into `head`; re-measured unpiped above.

    7z l -slt bad_symlink.squashfs            -> Path = badlink / Mode = lrwxrwxrwx / Size = 38 (no target)
    7z l      bad_symlink.squashfs            -> Attr "....." / Size 38 (default table has no type)

Synthetic divergence image (mksquashfs 4.7.5, v4, `fixtures/sentinel-symlink-divergence.sqfs`,
sha256 `92995175533942a18eb581397bafbe3636f1e0d0afb967bdd435faaa6671fdb1`), entries
`abs -> /etc/passwd`, `up -> ../outside`, `same -> hello.txt`:

    unsquashfs -lls -> abs -> /etc/passwd ; same -> hello.txt ; up -> ../outside
    7z l -slt       -> Mode lrwxrwxrwx for abs/same/up, no target strings
    7z x -y         -> "ERROR: Dangerous link path was ignored : up : ../outside"; ro sum "Sub items Errors: 1"
                       wrote: abs -> <outdir>/etc/passwd (rewritten, 61 B); same -> hello.txt;
                              up = 0-byte REGULAR file
    unsquashfs -d   -> rc 0; abs -> /etc/passwd ; same -> hello.txt ; up -> ../outside  (all preserved)

Padded carrier through REA (fresh outdir, `--max-depth 1`):

    pad1k.bin = squashfs_v3.le.1kpad.bin, 1024 B, "version 3.1, 320 bytes, 5 inodes"
    REA -> chunks[0].range {offset 0, length 1024}, root_file_range {0,1024},
           handler squashfs_v3, 4 files (apple1..4.txt)      -> envelopes/e5-padded-1k.json
    source: unblob handlers/filesystem/squashfs.py:77-98, `(start_offset + bytes_used) & 0xFF_FF_FF_FF`
            then round_up(bytes_used, 1024|4096) when the tail is zero padding

v3 superblock bytes (artifact fixtures, first 0x28):

    LE: 6873 7173 0300 0000 0000 0000 0000 0000 | 0000 0000 0000 0000 0000 0300 | 0000 1000 4001 00f5
    BE: 7371 7368 0000 0003 0000 0000 0000 0000 | 0000 0000 0000 0000 0000 0003 | 0000 0010 4001 0061
    -> s_major = 3 at 0x1c (u16, per-filesystem endianness), s_minor at 0x1e (1kpad fixture = 3.1);
       offset 0x14 = 0x0000 (no v3 compression field); bytes_used is not at the v4 offset 40:48.
       CORRECTION: an earlier line here said 0x1e for s_major; 0x1c is right (R42C1EntryDraft's bytes,
       re-checked). The frozen layout_probe's own output on these fixtures is in report §10 A8.

## P15 — lzma-adaptive v3 through REA (carrier-vs-oracle separation)

    env REA_UNBLOB_COMMAND=~/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \
        --format json --full-output --max-depth 1 fixtures/squashfs_v3_le.lzma.bin out-lzma
    -> rc 0; handler squashfs_v3; extraction_failed false;
       files firmware.bin_extract/{apple.txt 6, orange.txt 7}; gaps [depth-limited]
       (envelopes/e6-lzma-v3.json)

So unblob (forced -le) extracts an lzma-adaptive v3 image; `unsquashfs -lls` does not (rc 1). The
lzma constraint therefore binds the *oracle*, not the extraction.
