# External development inputs (not copied into the lane)

No third-party firmware bytes live in this artifacts tree.  Each input below is
identified by publisher URL, the sha256 of the downloaded file and the sha256 of
the carved chunk, plus the exact carve command.  Measure with the pure readers
(`unsquashfs`, `7z`) only; the unblob fixtures under `../fixtures/` are MIT and
are copied.

All work happened under the seat scratch
`/fast/scratch/hyaku/kaidoku-r42/R42C1Oracle` (removed at hand-off), with
`TMPDIR` inside it.

## 1. OpenWrt Kamikaze 7.09 x86-2.6 - the required DEV input

    URL     https://archive.openwrt.org/kamikaze/7.09/x86-2.6/openwrt-x86-2.6-squashfs.image
    sha256  a0a4fcf30e0a42fa09d1f6e9577d624ef78e402590f23549389a59e250441c12
    size    5529092

    # superblock at 4677120 (kernel + MBR before it); bytes_used 785823, carved
    # to the 786432-byte erase-block boundary 7z reports
    dd if=openwrt-x86-2.6-squashfs.image of=owrt709.sqfs bs=1 skip=4677120 count=786432
    sha256  5b8aee4ceac0820676842f9d78ef04469a5fbd45daf3c9359735ca65778a96d8  owrt709.sqfs

Measured (2026-10-26):

| probe | result |
|---|---|
| `unsquashfs -s -o 4677120 <image>` | rc 0, "valid little endian SQUASHFS 3:0", 332 inodes, 9 fragments, block 65536, filesystem size 785823 |
| `unsquashfs -lls -no-progress owrt709.sqfs` | **rc 1** - `gzip uncompress failed with error code -3` / `read_block: failed to read block @0xbfd46` / `read_fragment_table: failed to read fragment table block` / `FATAL ERROR: File system corruption detected` |
| `unsquashfs -d OUT -no-xattrs -f -no-progress owrt709.sqfs` | **rc 1**, same fatal |
| `7z l -tSquashFS -slt owrt709.sqfs` | rc 0; `File System = SquashFS 3.0`, `Method = LZMA Spec`; **331 entries = 137 regular, 42 dir, 152 symlink** |
| `7z x -tSquashFS -y owrt709.sqfs` | rc 2; 80 x `ERROR: Dangerous link path was ignored` (relative `..` targets); all 137 regular files extracted, 72 symlinks created, 80 zero-byte placeholders where the link was refused |
| `sasquatch -ls owrt709.sqfs` (calibration only - NOT an oracle producer) | rc 0; tries gzip/lzo/lz4/xz/zstd then **`Detected lzma-adaptive compression`**; 332 entries; `-d` extracts 137 files + 152 symlinks |

Oracle verdict (with backhand as primary): **exit 0** - backhand
(`-k le_v3_0_lzma`) and 7z agree on 331 entries / 137 regular files / 152
symlinks, 137 regular rows + 194 non-regular rows written.  unsquashfs 4.7.5 has
no v3 LZMA path and is therefore not a producer here (`third_producer: null`).
Recorded in `../runs/external/owrt__owrt709.sqfs/oracle-run.json`; backhand's own
extraction yields 137 files + 152 symlinks, i.e. it materialises the relative
`..` links that 7z refuses.

### Why a stdlib reader is not a 20-line addition (measured)

First compressed metadata block of `squashfs_v3_adaptive/__input__/squashfs_v3_le.lzma.bin`
(the small LZMA-3 fixture, inode table at 132, header `0x0035` = 53 bytes,
payload starts `00 21 06 bc 0f ee 65 ca`) fails all three candidate framings:

    zlib.decompress                        -> Error -3, incorrect header check
    lzma FORMAT_ALONE (13-byte header)     -> Corrupt input data
    lzma FORMAT_RAW LZMA1, 5-byte header, props 0x00 (lc0 lp0 pb0), dict from
      bytes 1..4 (0x0fbc0621 -> 264 MB)    -> Corrupt input data

The same image's directory table (offset 187, header `0x8026`) is stored
**uncompressed**, so the failure is specific to the compressed blocks.  A
lane-side v3 reader for this family has to reproduce the vendor wrapper
(sasquatch calls it lzma-adaptive) before it can be an oracle producer - that is
a sub-project, not a patch.

## 2. OpenWrt Kamikaze 7.09 brcm-2.4

    URL     https://archive.openwrt.org/kamikaze/7.09/brcm-2.4/openwrt-brcm-2.4-squashfs.trx
    sha256  0ebf0491c96e198c52e94c1228b9068151793031e3ff8026050e8fd3e26a953a
    size    1839104
    # squashfs magic at 517120; bytes_used (superblock +63, 8 bytes LE) = 1187016
    dd if=openwrt-brcm-2.4-squashfs.trx of=brcm-2.4.sqfs bs=1 skip=517120 count=1187016
    sha256  69b01a38043f35c76609498b64321d84d65f70f07c3aac87d88904f2ce73d555  brcm-2.4.sqfs

`7z`: 363 entries = 160 regular, 43 dir, 160 symlink, `Method = LZMA Spec`;
`unsquashfs`: rc 1 (same gzip/LZMA fatal).  Oracle: **exit 0** - backhand
`le_v3_0_lzma` + 7z agree (160 regular, 160 symlink).

## 3. OpenWrt Kamikaze 8.09.2 brcm-2.4

    URL     https://archive.openwrt.org/kamikaze/8.09.2/brcm-2.4/openwrt-brcm-2.4-squashfs.trx
    sha256  922c5d172b04c04fa8fb70677a5a7f01f9f359089a83ae0950b39a736f956abb
    size    2166784
    # squashfs magic at 507904; bytes_used = 1581251
    dd if=openwrt-brcm-2.4-squashfs.trx of=owrt809-brcm.sqfs bs=1 skip=507904 count=1581251
    sha256  d7256e0f509c614597bf0114913dfb541e666314158018a9b0cc2839cc0acc55  owrt809-brcm.sqfs

`7z`: 673 entries = 404 regular, 94 dir, 175 symlink, `Method = LZMA Spec`;
`unsquashfs`: rc 1.  Oracle: **exit 0** - backhand `le_v3_0_lzma` + 7z agree.
This is the "OpenWrt Kamikaze 8.09 squashfs-3.0 image" the draft names as a
carrier candidate: it is LZMA-3, which the backhand-primary oracle covers.

## 4. OpenWrt Kamikaze 7.09 brcm47xx-2.6 (the L1's dev cross-check)

    URL     https://archive.openwrt.org/kamikaze/7.09/brcm47xx-2.6/openwrt-brcm47xx-2.6-squashfs.trx
    sha256  42b0259f62505bd5573ca762fae6ec5799e602e87f9e9d6ce7676aacef5bb446
    size    1904640
    # squashfs magic at 753664, bytes_used 1061809
    dd if=openwrt-brcm47xx-2.6-squashfs.trx of=brcm47xx-2.6.sqfs bs=1 skip=753664 count=1061809
    sha256  13a4f1b8f30044185730b92ad46ff39feebf959d554b6b33c742373b737c6912  brcm47xx-2.6.sqfs

Oracle: exit 0, backhand `le_v3_0_lzma` and 7z both 362 entries = **156
regular + 43 dir + 163 symlink**, 0 mismatches - the same 156/156 regular files
and 163 symlinks the L1 measured independently with backhand + 7z.

## 5. Round-41 C1 carriers (v4, for the version gate)

`corpus/evidence/round-41/c1/L3/carrier.sqsh`
(sha256 `04cfb4cd6189742eaba94d0022d242d4194726a6f0684fd8381b39bc4e6c45a3`) and
`L4/carrier.sqsh` (`4c0e545975d2993f5b3417d55990a5df5ad67fa2f21164b831119f6e85cbcfbc`)
both begin `sqsh` / major 4; the oracle exits 2 `unsupported_version`, as
designed (`../runs/external/L3__carrier.sqsh/`, `L4__carrier.sqsh`).
