# Round-40 AVM layout facts measured by R40C1Reader

Provenance (V1): `https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/FRITZ.Box_6490_Cable-07.57.image`
sha256 `f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d`, 39 741 440 B, tar.
Members carved with Python `tarfile` (stdlib):

| member | tar offset | bytes | sha256 |
|---|---|---|---|
| `./var/remote/var/tmp/filesystem.image` (AVM-BE) | 32 026 112 | 5 443 592 | `334e56dfba6a785590bb5cdbd78fcb5be183b9af160b51fc8935a301ad3f3d4` |
| `./var/remote/var/tmp/x86/filesystem.image` (LE) | 270 848 | 28 200 968 | `7ea4c628def17c25dc05f6103f8563884022dd1a5baf0c4fba38a85b546a0419` |

Offsets are `tarfile.TarInfo.offset_data` on the pinned image (GNU tar, 512-byte blocks).

## Measured layout (the reader's `--layout avm`)

* **Superblock, inodes, directory headers/entries, block-size lists, fragment
  table index and entries: big-endian.** The AVM marker
  `mkfs_time == bytes_used` holds on both members (BE: 5 442 392; LE: 28 200 029)
  but is not the layout test.
* **Metadata block-length header (the 2-byte value at the start of every
  metadata block): little-endian.** This is the only length field that differs
  from a standard big-endian image (Freetz note, lane S114/S192). Data-block
  size lists are *not* little-endian: they are fields inside the inode record
  and stay big-endian.

Evidence, V1 AVM-BE member (`inspect/vendor-be.json`):

```
header at inode_table_start, decoded both ways (0x8000 masked):
  le = 1380   be = 25605      block_length_signal = plausibility
first data-block list entry of usr/sbin/FwUpstreamDocsis2_D.bin:
  bytes 00 00 01 90
  structural (BE)  value 0x00000190 size 400    -> decompress ok, 65536 bytes
  swapped    (LE)  value 0x90010000 size 65536  -> decompress error (xz)
first fragment entry:
  structural (BE) start 96 size 15332 -> plausible
  swapped    (LE) start 6.9e18 size 3.8e9 -> implausible
```

Round-11 genuine AVM image (`avm-be.squashfs`, 4096 B, sha256
`c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32`) on the same
reader:

```
header at inode_table_start: le 116, be 29696  (exact identity: 121+2+116=239=dir table)
fragment entry bytes 10 80 | 00..60 | 01 00 00 19 | 00 00 00 00
  header 0x8010 LE = 16-byte uncompressed metadata block
  start=96 (BE), size=0x01000019 (BE) = BLOCK_UNCOMPRESSED | 25
  payload at 96: 'apple\nbanana\ncherry\ndate\n' -> the four files' fragment
```

AVM-LE member (magic `hsqs`): every field little-endian, no AVM block-header
exception; same fragment/data evidence decodes little-endian
(`inspect/vendor-le.json`).

## Auto detection

`--layout auto` reads the magic, then picks the metadata-header endianness with
(exact) `inode_table_start + 2 + len == directory_table_start`, else
(plausibility) `0 < len <= 8192`, else decodes the inode + directory metadata
chains under both endiannesses (this also resolves palindromic header bytes such
as `0x0101`). It reports `layout`, `header_endian`, `block_length_signal` and
the two candidate lengths.

Measured on all nine images: see `validation-matrix.tsv`. `auto` reproduced the
forced-layout file list byte-for-byte on all nine (the driver compared
`out/<image>.auto.files.tsv` with `out/<image>.files.tsv`, `cmp` exit 0).

## Discriminators (format vs marker)

| image | marker | auto layout | auto signal |
|---|---|---|---|
| round-39 `carrier-avm.sqsh` (marker-only standard-BE body, sha256 `762c06a6…`) | yes | **be** | exact (le 14209 / be 311) |
| round-39 `carrier-be.sqsh` (standard-BE, no marker) | no | **be** | exact |
| round-39 `avm-be-markerstripped.sqsh` (genuine AVM layout, marker normalised) | no | **avm** | exact (le 116 / be 29696) |

So the marker does not decide the layout, and a genuine AVM body stays readable
after its marker is normalised. Forcing the wrong layout fails loudly with exit
2 (`--layout be` on `avm-be.squashfs`, `--layout avm` on K1 or on the
marker-only image); see `negative-cases.txt`.
