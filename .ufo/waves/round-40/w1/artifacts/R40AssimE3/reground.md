# Re-grounding evidence record — 2026-10-26 (seat R40AssimE3)

Not a captured shell session: each block is a command this seat ran, with the output it observed.
Read-only throughout except the generator controls, which wrote only into
`/fast/scratch/hyaku/kaidoku-r40/R40AssimE3` (TMPDIR set there).

## 1. The cited image (S123's payload), re-hashed this round

```
$ sha256sum /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/avm-be.squashfs
c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32  …/avm-be.squashfs      exit 0
$ wc -c  -> 4096
```

Equal to the digest the round-39 critic recorded and to the TSV's `image_bytes` 4096.

## 2. Superblock and first metadata header, decoded here (no sasquatch, no unblob)

```
$ python3 -I -B  (full big-endian superblock read + both-endian metadata header decode)
magic sqsh | inodes 5 | mkfs_time 365 | block_size 65536 | fragments 1 | compression 4
block_log 16 | flags 832 | no_ids 1 | s_major 4 | s_minor 0 | root_inode 128 | bytes_used 365
id_table_start 357 | xattr_id_table_start 0xffffffffffffffff | inode_table_start 121
directory_table_start 239 | fragment_table_start 343 | lookup_table_start 0xffffffffffffffff
marker mkfs==bytes_used: True
hdr bytes 7400  lenLE 116  lenBE 29696
identity it+2+lenLE == dir_table_start: 239 239 True
identity it+2+lenBE == dir_table_start: False                            exit 0
```

`compression 4` is xz; the identity holds only in the little-endian reading, so the body's
block-length headers are little-endian while the superblock is big-endian.

## 3. The other round-11 files, hashed

```
$ sha256sum  lead1-avm-image.tsv   f205807de8016ead8732d77f14acf5e99e6527e02d6281566f6070b7c8539eb0
             unblob.log            352e0d794143df9cc4fa6113d72ee5a620ea0aa201a930e00e91590518aed5d7
             freetz-squashfs4-host-be.mk  48fb043d8fb2e9b1ea916abb06316bb99a3c3d2232d8694e6f6f651a0393a3d5
             avm-final.sh          5f0c2957563fbc3686db5907f52a8d2a2272ed09cdfbbecd7abdc1956dd6a4e2
$ grep -c -F 'd92ab59aabf5173f2a59089531e30dbf' freetz-squashfs4-host-be.mk  -> 1
$ grep -c -F 'sasquatch-v4be -no-exit-code -f -d' lead1-avm-image.tsv          -> 2   (rows
  unblob_command and unblob_command_verbatim)
```

## 4. The retained extraction record (read, not re-run)

`unblob.log`, 2026-10-24 12:01.54, pid 54461, extract_root `.`:

```
Found valid chunk              chunk=0x0-0x1000 handler=squashfs_v4_be
Running extract command        command='sasquatch-v4be -no-exit-code -f -d /tmp/r11-avm3/avm-be.squashfs_extract …'
Processing file                path=avm-be.squashfs_extract/apple1.txt size=0x6
Processing file                path=…/apple2.txt size=0x7   …/apple3.txt size=0x7   …/apple4.txt size=0x5
```

No `-be` on the argv. No exit status line and no version banner in this file.

`avm-final.log` (earlier, 09:01, `-e /tmp/r11-avm`) ends:

```
handler=squashfs_v4_be
command='sasquatch-v4be -no-exit-code -f -d /tmp/r11-avm/avm-be.squashfs_extract …'
Can't run extract command
dependencies=['sasquatch-v4be']
```

So two runs are retained and only the 12:01 one published files; the earlier one hit
`ExtractorDependencyNotFound`. The TSV records the successful run's contents and
`sasquatch_v4be_version  unsquashfs version 4.5.1 (2022/03/17)`.

## 5. Tool pins, re-measured

```
$ sha256sum /home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py
2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287
$ sed -n '40,52p' (same file)   -> case Endian.BIG, 4: … is_avm = header.bytes_used == header.mkfs_time
                                   if not is_avm: commands_args.append("-be")
$ ~/.local/bin/unblob --version           -> 26.6.4                         exit 0
$ ~/.local/bin/sasquatch-v4be -version    -> unsquashfs version 4.5.1 (2022/03/17)   exit 0
$ python3 -V                              -> Python 3.14.8
```

```
$ curl -fsSL -m 60 -o unsquashfs.c https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/squashfs-tools/unsquashfs.c
http 200  bytes 120167  sha256 ece42b66f37ba67707c2c51b47b643c027232153705f59d238da79958a54cb40
   (equal to S121's anchor digest; the `-be` branch at 4390-4394 sets swap=1 on a little-endian host)
$ sed -n '655,670p' unsquashfs.c
   int read_block(…)   … if(swap) { read 2 bytes; c_byte = (c_byte >> 8) | ((c_byte & 0xff) << 8); }
                       … else    { read 2 bytes; }
```

So the flag reaches the 2-byte metadata block-length header itself: with `swap` the header is
byte-swapped, without it the header is taken in host order. That is the field Freetz's bullet (S125
line 8) says AVM stores little-endian.

## 6. Freetz's own description (S125's document), fetched this round

```
$ curl -fsSL -m 60 -o avm-be-format.txt https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt
http 200  bytes 1496  sha256 c1c43f6f97d7477dcdab15203d11e43b49beb12e3a43a3b52bdd71b672a9a5d5
$ grep -n -i "little|block length|mkfs_time|bytes_used"
5:  - instead of the little-endian data layout (the only layout supported by the original/unmodified
8:  - the only data field stored in the little-endian format is the block length value at the beginning
9:    of each block
13:  - super-block field 'mkfs_time' contains (instead of the filesystem creation time) the same value
14:    as the super-block field 'bytes_used'
```

## 7. Id collision check (prompt §10 command, output dir in scratch)

```
reg=122  staged=132  collisions=17
S106 S107 S108 S109 S110 S111 S112 S113 S114 S115 S116 S117 S118 S119 S120 S121 S122
next free lane id = 122 + 1
```

Retained: `collision/reg-ids`, `collision/staged-ids`, `collision/collisions`.

## 8. Guard proof (indented-row fixture)

```
$ fixture registry:  | S001 | …   and   "  | S002 | …" (two leading spaces)
$ staged fixture:    | S002 | …   and   | S900 | …
0-3-space pattern:      reg=[S001 S002 ]  collisions=1 -> [S002 ]
column-zero-only:       reg=[S001 ]       collisions=0    (false green)
$ grep -cE '^ {0,3}\| S[0-9]{3}' reg-fixture.md -> 2   (the indented row is census-countable)
```

Retained: `collision/reg-fixture.md`, `collision/staged-fixture.md`, `collision/fx-*`.

## 9. The marker-vs-layout controls (this seat's own bytes, 2026-10-26)

```
$ python3 tools/round-39/gen-squashfs.py tree control-standard-be.sqsh --endian be  --comp gzip
wrote control-standard-be.sqsh 373 bytes, inodes 5                     exit 0
$ python3 tools/round-39/gen-squashfs.py tree control-avm-mode.sqsh --endian avm --comp gzip
wrote control-avm-mode.sqsh 373 bytes, inodes 5                        exit 0
$ python3 -I -B probe-avm-layout.py <image> <standard-be> <avm-mode> <markerpatched> <markerstripped>
probe exit=0     # full output: probe-output.tsv
```

| image | marker | meta header | len LE / BE | identity fit | class |
|---|---|---|---|---|---|
| avm-be.squashfs (round 11) | true | `7400` | 116 / 29696 | LE | AVM layout |
| control-avm-markerstripped.sqsh | false | `7400` | 116 / 29696 | LE | AVM layout |
| control-standard-be.sqsh | false | `80a8` | 10368 / 168 | BE | standard BE |
| control-avm-mode.sqsh | true | `80a8` | 10368 / 168 | BE | standard BE |
| control-standard-be-markerpatched.sqsh | true | `80a8` | 10368 / 168 | BE | standard BE |

```
$ markerpatched vs gen --endian avm: differing bytes = 0, len 373 / 373
  sha256 both e68f6a530b8fe2d73caf3216c592d9d17ed7bdee955b27531c81c20e7363fd73
$ avm original mkfs_time 365 -> stripped to 1; bytes_used stays 365; layout verdict unchanged (LE fits)
```

## 10. What this seat did NOT run

No `unblob`, no `sasquatch`/`sasquatch-v4be` extraction, and no REA call: the round-11 extraction is
read from its retained log, and the `-be` decision is read from the pinned handler source. No vendor
firmware image was downloaded, opened or extracted. No frozen C1 carrier was touched, no C2 held-out
carrier was built or run, nothing was written outside this seat's artifacts directory and this
report. No tool was installed or upgraded; `sasquatch`, `sasquatch-v4be` and `unblob` were not
modified.
