# V1 carrier carve — exact commands and the byte-extent decision

Seat `R40C1VendorV1`, round 40 wave 1 (pre-freeze). No REA and no unblob run was made on this
carrier or on the vendor image it comes from (bounds). Everything below reproduces from public
bytes with `curl`, `tar`, `head`, `sha256sum` and the two pure-stdlib parsers in this directory.

## Exact carve command (reproduces `carrier-v1-be.sqsh`)

```sh
export TMPDIR=/fast/scratch/hyaku/kaidoku-r40/R40C1VendorV1   # or any scratch dir
cd "$TMPDIR"

# 1. image  (HTTP 200, 39741440 bytes, sha256 f518ce6b…ede6d — matches the pin)
curl -sS -D headers.txt -o fw.image \
  https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/FRITZ.Box_6490_Cable-07.57.image
sha256sum fw.image      # f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d

# 2. tar members (BE carrier source, plus the two provenance files)
mkdir -p x
tar -xvf fw.image -C x ./var/remote/var/tmp/filesystem.image ./var/info.txt ./var/version
sha256sum x/var/remote/var/tmp/filesystem.image   # 334e56df…f3d4  (5443592 bytes)

# 3. carve the SquashFS extent (bytes_used, big-endian u64 at superblock offset 40..48)
BU=$(python3 -c "import struct;print(struct.unpack('>Q',open('x/var/remote/var/tmp/filesystem.image','rb').read(48)[40:48])[0])")
head -c "$BU" x/var/remote/var/tmp/filesystem.image > carrier-v1-be.sqsh
sha256sum carrier-v1-be.sqsh     # ac4098bd11a76f8ad001faac0f1a5e018708d9b03943dfebb2b18a24e0038e95
stat -c %s carrier-v1-be.sqsh    # 5442392
```

`BU` evaluates to `5442392`; the command is byte-exact (`head -c 5442392`).

## The member's byte shape (measured)

| range | bytes | content |
|---|---|---|
| `0 .. 5442392` | 5442392 | the SquashFS v4 filesystem (`bytes_used`) |
| `5442392 .. 5443584` | 1192 | zero padding to the next 4096 boundary (all bytes `0x00`) |
| `5443584 .. 5443592` | 8 | vendor trailer `23 de 53 c4 2a 99 c5 51` |

The same shape holds in the LE sibling member (`./var/remote/var/tmp/x86/filesystem.image`): 28200968
bytes, `bytes_used` 28200029, 931 zero bytes to 28200960, then the same 8-byte trailer. So the
trailer and the pad are an AVM image convention, not part of either filesystem.

## Why the carrier is `[0, bytes_used)` and not the whole member

`unblob` 26.6.4 `_SquashFSBase.calculate_chunk`
(`…/site-packages/unblob/handlers/filesystem/squashfs.py:77-98`, sha256 `2d7b901b…9287`) walks
`PAD_SIZES = [4096, 1024]` (line 21): it reads `round_up(bytes_used, pad) - bytes_used` bytes at
`bytes_used` and, **if that read starts with that many zero bytes** (line 92), returns a chunk
ending at the rounded-up offset; otherwise it returns a chunk ending exactly at `bytes_used`
(lines 96-98).

Measured on three dev fixtures built with `tools/round-39/gen-squashfs.py --endian be --comp gzip`
(own fresh tree, `bytes_used` 3526 — a development input, never a carrier). `unblob -e … --report
…` JSON, chunk/unknown records only (`chunk-arithmetic.txt`, `rep-A/B/C.json`):

| fixture | shape | chunks |
|---|---|---|
| A `dev-A-exact.sqsh` | exactly `bytes_used` (3526 B) | `ChunkReport 0->3526 squashfs_v4_be`; **no unknown chunk**; 4 files extracted, `Chunk identification ratio: 100.00%` |
| B `dev-B-pad4096.sqsh` | `bytes_used` + 570 zero bytes to 4096 | `ChunkReport 0->4096`; no unknown chunk |
| C `dev-C-pad-trailer.sqsh` | B + the vendor's 8-byte trailer | `ChunkReport 0->4096` **plus `UnknownChunkReport 4096->4104 size=8`** |

The V1 member has exactly shape **C**. Consequences:

- **Whole member (5443592 B)** → chunk `0 -> 5443584` (the 1192-byte read is all zeros, so the
  rounding branch fires; this is exactly the round-39 observation "chunk 0-5443584") **plus an
  8-byte `UnknownChunkReport`** `5443584 -> 5443592`. That is unknown-chunk noise inside the C1
  subject and would have to be carried or explained by the frozen projection.
- **`[0, bytes_used)` (5442392 B)** → the read at `bytes_used` is short (EOF), the `startswith`
  test is false, and the fallback returns `0 -> 5442392`: one chunk, the whole file, no unknown
  chunk. This keeps the claim literally about *an AVM-BE SquashFS v4 and nothing else*, and adds a
  checkable invariant: the carrier's size equals its own `bytes_used`.
- **`[0, 5443584)` (padded to 4096)** also yields one clean chunk (`0 -> 5443584 = EOF`), but it
  ships 1192 vendor zero bytes that belong to no filesystem, and it destroys the `size ==
  bytes_used` invariant. It is the fallback if any downstream tool ever insists on a 4 KiB
  multiple; nothing measured here needs it.

Direct reads of the carved carrier (allowed; `sasquatch-v4be` 4.5.1, sha256
`fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`; `sasquatch-v4be -version` →
`unsquashfs version 4.5.1 (2022/03/17)`):

```
$ sasquatch-v4be -ll carrier-v1-be.sqsh      # no -be
exit=0   1079 listing lines (118 dirs, 697 files, 263 symlinks, 1 char device)
stderr (3 lines): "SquashFS version [1024.0] / inode count [923009024] suggests a SquashFS image
of a different endianess" / "Trying to decompress using default xz decompressor..." /
"Successfully decompressed with default xz decompressor"

$ sasquatch-v4be -be -ll carrier-v1-be.sqsh
exit=1   0 listing lines
stderr: "Reading a different endian SQUASHFS filesystem on carrier-v1-be.sqsh" /
        "read_id_table: failed to read id table block" /
        "FATAL ERROR: File system corruption detected"
```

That is the marker-driven split the claim rests on, measured on the carved bytes: the same file
extracts completely **without** `-be` and dies **with** it.

## What may not run on this carrier before the freeze

REA 6.5.0 `extract-firmware` and `unblob` were **not** run on `carrier-v1-be.sqsh`, on the member,
or on the vendor image. The chunk-arithmetic measurements above used fresh dev fixtures only.
