# R41-C1 carrier **V3** — vendor provenance and oracle

**Verdict: DONE** — V3 is a genuine AVM-layout big-endian SquashFS v4 carrier with the AVM marker, its
provenance chain closes from the published image to the carve, and its oracle (8 regular files, 95
non-regular entries) reproduces from a direct `sasquatch-v4be` extraction with **0 mismatches**. No REA and
no unblob ran on V3 or on anything carved from it.

Seat `R41C1VendorV3`, round 41 wave 1 (pre-freeze). No VCS mutation, no tool install, no subagent.

---

## 0. What was assigned vs what was run

| assigned | done | evidence |
|---|---|---|
| download the 5490 07.31 image, record HTTP/bytes/sha256 | yes, sha256 equals the assigned pin | §1 |
| member `./var/tmp/filesystem.image`: sha256, size | yes | §1 |
| superblock: magic, version, comp, inodes, mkfs_time, bytes_used, marker | yes | §2 |
| carve `[0, bytes_used)` and sha256 it | yes | §1 |
| walk the inode-table metadata chain LE vs BE | yes, both walks executed | §2.2 |
| oracle `--layout avm` → `oracle.tsv` / `nonregular.tsv` in round-40 formats | yes | §3 |
| direct `sasquatch-v4be` extraction **without `-be`**, compare every regular file path+sha256, list suffix collisions | yes, 0 mismatches, 0 collisions | §3.2–3.4 |
| count entries vs REA staged-entry budget at depth 1 | yes, budget defaults read from the REA 6.5.0 schema | §4 |
| fetch `info_en.txt`, record product/version + short licence quotes | yes | §1.3 |
| `carriers.json` fragment + `oracle.tsv`/`nonregular.tsv`/`oracle-run.json` | yes, in this seat's artifacts dir | §5 |

Scratch `S=/fast/scratch/hyaku/kaidoku-r41/R41C1VendorV3`; every command below ran with `cd "$S"`, `TMPDIR="$S"`.
All cited files were copied into `artifacts/R41C1VendorV3/` before scratch removal; no vendor bytes were
copied into the lane.

---

## 1. Provenance chain (measured, not inferred)

### 1.1 Image

```
$ cd "$S" && curl -sS -o 5490.image -w 'http_status=%{http_code}\nbytes=%{size_download}\n' \
    'https://download.avm.de/fritzbox/fritzbox-5490/other/fritz.os/FRITZ.Box_5490-07.31.image'
http_status=200
bytes=33269760
$ sha256sum 5490.image
770efb4e368a58104bf362c990114db8b70a5060932ce8bcec7ef1bc75045ab7  5490.image
```

`770efb4e…5ab7` **equals the assigned pin**. HTTP 200, 33 269 760 bytes.

### 1.2 Member and carve

```
$ tar -tvf 5490.image
drwxr-xr-x 0/0          0 2023-09-02 10:24 ./var/
-rwxr-xr-x 0/0      28622 2023-09-02 10:24 ./var/install
-rw------- 0/0       2807 2023-09-02 10:24 ./var/info.txt
drwxr-xr-x 0/0          0 2023-09-02 10:24 ./var/tmp/
-rw-r--r-- 0/0    2690312 2023-09-02 10:24 ./var/tmp/kernel.image
-rw-r--r-- 0/0   30236680 2023-09-02 10:24 ./var/tmp/filesystem.image
-rw-r--r-- 0/0         35 2023-09-02 10:24 ./var/version
-rw-r--r-- 0/0         14 2023-09-02 10:24 ./var/install-features
-rw-r--r-- 0/0        340 2023-09-02 10:24 ./var/content
-rwxr-xr-x 0/0     297132 2023-09-02 10:16 ./var/chksum
-rw-r--r-- 0/0        128 2023-09-02 10:24 ./var/signature

$ tar -xf 5490.image -C m ./var/tmp/filesystem.image
$ sha256sum m/var/tmp/filesystem.image
87cc5d6b3ad105221114a86f6a4d4d868f731b868ff875979e7f0cb47bcea0f8  m/var/tmp/filesystem.image   (30236680 bytes)

$ python3 -c "open('v3-carve.sqfs','wb').write(open('m/var/tmp/filesystem.image','rb').read(30233394))"
$ sha256sum v3-carve.sqfs
c4f74f54a65e861e22f5d6a47977cdbb3b5345819174f33bc86c63d3d10f872a  v3-carve.sqfs            (30233394 bytes)
```

Chain: image `770efb4e…` → member `87cc5d6b…` (30 236 680) → carve `c4f74f54…` (30 233 394). The member is
**3286 bytes longer than `bytes_used`**; the last 3286 bytes are zero except the final 8
(`23 de 53 c4 56 3d 05 73`). The carrier is the carve, not the member — a counter that pins the member
length would compute a different digest.

### 1.3 Identity (public, identity-only)

`info_en.txt`: HTTP 200, 50 653 bytes, sha256 `e3100cdaeae9d72c8f8637119e492677ef074c468394e6d52a21fe73b7360d18`.
Parsed lines: `Product: FRITZ!Box 5490`, `Version: FRITZ!OS 7.31`, `Release date: 09/04/2023`.
From the tar: `Product=Fritz_Box_HW223 (FRITZ!Box 5490)`, `Type=Release`, `Releasecycle=PSQ19P2NL4`,
`Version=07.31`, `Build=107857`; `var/version` = `FIRMWAREVERSION=151.07.31,,107857,`.

Licence, short quotes only (info_en.txt lines 663/665/667): "© AVM GmbH 2004-2021. All rights reserved.";
the package "contains files that are propagated under different licenses"; "AVM grants the non-exclusive
right to use this AVM firmware package, which is supplied exclusively in object code format"; "The licensee
may create only one copy of the software, which may be used exclusively for backup use." Consequence: no
vendor bytes are committed; this artifact cites digests plus the rebuild commands above.

---

## 2. Layout, measured

### 2.1 Superblock (`sqsh`, structural fields big-endian)

```
$ python3 -c "…struct.unpack('>5I6H8Q', d[:96])…"
field (BE)              value            (LE decode of the same bytes)
inodes                  104              1744830464
mkfs_time               30233394         844352769
block_size              65536            256
fragments               1                16777216
compression             4 (xz)           1024
block_log               16               4096
flags                   704              49154
no_ids                  1                256
s_major / s_minor       4 / 0            1024 / 0
root_inode              5288             12111305297906106368
bytes_used              30233394         3626467529142042624
id_table_start          30233386
xattr_id_table_start    18446744073709551615
inode_table_start       30231260
directory_table_start   30231986
fragment_table_start    30233062
lookup_table_start      30233372
```

- magic bytes `73 71 73 68` = `sqsh`; version 4.0; compression id 4 = xz.
- **marker `mkfs_time == bytes_used` holds (30233394).** This is the AVM identity signal, *not* the layout
  test — the layout is decided by the metadata block-length header order, measured next.
- The draft's V3 line ("AVM-BE wrapper, 104 inodes, `bytes_used = 30233394`") is **verified true**.
- First 32 bytes: `73 71 73 68 00 00 00 68 01 cd 53 32 00 01 00 00 00 00 00 01 00 04 00 10 02 c0 00 01 00 04 00 00`.

### 2.2 Inode-table metadata chain, little-endian headers vs big-endian headers

Walk from `inode_table_start` (30231260) toward `directory_table_start` (30231986), reading each 2-byte
block-length header in the two orders and xz-decoding the declared body (`inode-chain-walk.txt`):

```
LE headers: 1 block at 30231260, header=724, decompressed=5320
            chain end 30231260+2+724 = 30231986 == directory_table_start   (exact identity)
BE headers: first header reads 54274, only 2132 bytes remain in the carve -> truncated, walk fails
```

`2 + 724 + 30231260 == 30231986` is the exact identity `squashfs` guarantees for a one-block inode table,
so the header is little-endian and the structural fields are big-endian: **AVM layout, confirmed by direct
measurement, not by the marker.**

Two reader cross-checks:

| run | exit | observation |
|---|---|---|
| `sqfs-list.py --layout auto --inspect …` | 0 | `layout=avm`, `header_endian=little`, `block_length_signal=exact`; `oracle.tsv`/`nonregular.tsv` **byte-identical** to the `--layout avm` run |
| `sqfs-list.py --layout be …` | 2 | `sqfs-list: metadata body out of bounds: offset 30231262 length 21506, image 30233394 bytes` — an all-BE reader cannot read V3 |

### 2.3 What unblob 26.6.4 will do with these bytes (source quote, not a run)

Installed handler `…/site-packages/unblob/handlers/filesystem/squashfs.py`
(sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`, 591 lines):

```
case Endian.BIG, 4:
    executable = self.V4BE_EXECUTABLE
    …
    is_avm = header.bytes_used == header.mkfs_time
    if not is_avm:
        commands_args.append("-be")
…
commands_args.extend(["-no-exit-code", "-f", "-d", "{outdir}", "{inpath}"])
```

Pattern `73 71 73 68 [24] 00 04` matches V3 (`bytes[0:4] == sqsh`, `bytes[28:30] == 00 04`, s_major BE 4),
so `squashfs_v4_be` claims the chunk and — because the marker holds — runs
`sasquatch-v4be -no-exit-code -f -d {outdir} {inpath}` **without `-be`**. Excerpt: `unblob-handler-excerpt.py.txt`.

---

## 3. Oracle and independent cross-check

### 3.1 Oracle (`tools/round-40/sqfs-list.py`, sha256 `1079fa9b…53cd9`, selftest 13/13 exit 0)

```
$ python3 -I -B tools/round-40/sqfs-list.py --layout avm --inspect \
      --files oracle.tsv --nonregular nonregular.tsv v3-carve.sqfs      # exit 0
```

`oracle.tsv` (8 rows, round-40 grammar `relpath TAB sha256 TAB size`):

```
bin/busybox                 936ea8fbbd76ce04a0f28ac03128d8f17ad6152e7c3563f5e8ecb78fbe37a1d9  631572
etc/inittab                 d3abf489ee563a1607f7ccba784f63fc94a96be84df14512232d96fbcd1f9520  385
filesystem_core.squashfs    cc6c19250c5a2df8260ad664b1fd82d5a6b14ce4da3b766249c21f5ed9dfbe43  29597696
lib/ld-uClibc-1.0.31.so     c262da1fa1eaaf7e25a9c7e8039db7e0f8e2d3a537810f69f71465b77a73effa  31788
lib/libuClibc-1.0.31.so     9080801a11bbc0412c1b7352dc865cb495f33ce3a1a2bf46450f403de83ed851  952992
sbin/flash_update           2cdab7bfc7f2c22753d30742b5ff4b5c1a6a0a2ba7af510d7557624bd6af121d  12617
sbin/reboot                 3ddee36a365a2c7b068b0da8f89664f8ec2db3a9d87462bbe1474a180f383891  54
tmp/mtab                    e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0
```

`nonregular.tsv` (95 rows): 9 dirs (`bin core dev etc lib proc sbin tmp var`), 85 symlinks, 1 char device
(`dev/led 247:0`). Inode identity: 8 + 9 + 85 + 1 + root = **104** = superblock `inodes`.

Reader `--inspect` (`inspect-avm.txt`): `layout=avm`, `avm_marker=true`, `escaping_symlinks=0`,
`symlink_reasons={absolute-inside:5, inside:80}`, `warnings=[]`, `decode_paths={raw_data_blocks:448,
compressed_data_blocks:29, raw_metadata_blocks:1, compressed_metadata_blocks:2, fragments_used:4,
fragment_slices:4}`.

Table digests: `oracle.tsv` `782953dcba14e1cd55e93636c13090322078483cf937879a5ae021ecfcd10a94` (700 B),
`nonregular.tsv` `3e9b3e5196eeb3ef1b8566e4452bc687ec03392bda9a84e6cac28d6c8b05f7b7` (2595 B). Both reproduce
byte-identically on a second run (`timing.json`).

### 3.2 Direct `sasquatch-v4be` extraction, **no `-be`**

```
$ ~/.local/bin/sasquatch-v4be -no-exit-code -f -d rerun/sq v3-carve.sqfs    # exit 0, 21 ms
SquashFS version [1024.0] / inode count [1744830464] suggests a SquashFS image of a different endianess
Trying to decompress using default xz decompressor...
Successfully decompressed with default xz decompressor
create_inode: could not create character device rerun/sq/dev/led, because you're not superuser!
Parallel unsquashfs: Using 1 processor
94 inodes (481 blocks) to write
created 8 files / created 10 directories / created 85 symlinks
created 0 devices / 0 fifos / 0 sockets / 0 hardlinks
```

Binary sha256 `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`, version line
`unsquashfs version 4.5.1 (2022/03/17)`. Run three times (`-d`, `-f -no-exit-code -n -d`,
`-no-exit-code -f -d`), always exit 0.

### 3.3 Cross-check: oracle vs extraction (`crosscheck.txt`)

Per regular file: rel path, sha256, size. Per symlink: `os.readlink` target.

```
oracle_regular 8
sq-sh-out: regular=8 only_oracle=[] only_sasq=[] sha_mismatches=[] size_mismatches=[]
sq2:       regular=8 only_oracle=[] only_sasq=[] sha_mismatches=[] size_mismatches=[]
symlink_target_mismatches 0 []   (85 symlinks compared)
```

**0 mismatches expected, 0 observed** — 8/8 file digests, 85/85 symlink targets. `sasquatch` also created
10 directories (= 9 listed + root), matching the oracle. The char device is the only non-created entry and
is uncreatable unprivileged; `-no-exit-code` keeps the run at exit 0, which is exactly the argv unblob
builds.

### 3.4 Collision census (`collision-census.txt`)

Component-wise suffix test, both directions, over 8 regular paths × 85 symlink paths:

```
symlink_path_suffix_of_regular: 0 []
regular_path_suffix_of_symlink: 0 []
exact_collisions: 0
basename_shared_reg_vs_link: {'mtab': ['tmp/mtab', 'etc/mtab']}
```

V3 carries **no both-direction path collision** (the only near-miss is `tmp/mtab` regular vs `etc/mtab`
symlink → `/tmp/mtab`; neither path is a suffix of the other). So V3 neither confirms nor falsifies the
R40-CL1 exact-match fix: that demonstration must come from L3/L4 and the counter's own fixtures.

---

## 4. Depth-1 projection budget vs REA 6.5.0 staging budgets

Read from `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cli-runtime/cutterToolContracts-TZH9EHr5.js:1761-1763`
(`extract_firmware` schema):

| parameter | default | min | max | V3 at `--max-depth 1` |
|---|---|---|---|---|
| `max_depth` | 3 | 1 | 10 | **1** (frozen) |
| `max_output_files` | 10 000 | 1 | 100 000 | **103 entries measured** (root + 9 dirs + 85 symlinks + 8 files; 104 if `dev/led` is created) = 1.0 % of budget |
| `max_output_bytes` | 268 435 456 | 1 | 536 870 912 | **30 233 394** = 11.3 % of budget |

Entry accounting is `inventoryFirmwareOutput` (`dist/firmware/FirmwareFiles.js:122-153`), which counts
directory entries including links and throws `Staging entry budget exceeded` only above the bound. At
depth 1 the nested 29 597 696-byte core is published as **one regular file** and is not recursed into, so
V3 cannot approach either budget.

---

## 5. Deliverables

All in `kaidoku-shokunin/.ufo/waves/round-41/w1/artifacts/R41C1VendorV3/` (this seat may not write
`corpus/`; the L1 moves these in the freeze commit):

| artifact | sha256 | intended lane path after integration |
|---|---|---|
| `carriers-fragment.json` | `d1ebdc4b…4b38` | merge as the `V3` element of `.ufo/waves/round-41/c1/carriers.json` |
| `provenance.json` | `8c100a72…bb5d` | `corpus/evidence/round-41/c1/V3/provenance.json` |
| `oracle.tsv` | `782953dc…0a94` | `corpus/evidence/round-41/c1/V3/oracle.tsv` |
| `nonregular.tsv` | `3e9b3e51…f7b7` | `corpus/evidence/round-41/c1/V3/nonregular.tsv` |
| `oracle-run.json` | `586f9939…1b9b` | `corpus/evidence/round-41/c1/V3/oracle-run.json` |
| `superblock.json` | `0ca347ae…8812` | advisory (may be folded into `oracle-run.json`) |
| `fetch-5490.json` | `6b6e84a4…0dadb7` | advisory (identity + licence quotes + fetch/digest chain) |
| `inspect-avm.txt` | `08050f28…0e77` | advisory (`sqfs-list --inspect` stdout of the frozen run) |
| `inspect-auto.json` | `3b0158db…fe17` | advisory (auto-layout cross-check) |
| `inode-chain-walk.txt` | `f6c163e5…5138` | advisory (LE vs BE header walk) |
| `crosscheck.txt` | `b4b7fccf…0cb8` | advisory (oracle vs sasquatch, 0 mismatches) |
| `collision-census.txt` | `a642a8ec…b00b` | advisory (0 collisions both directions) |
| `sasquatch-crosscheck.log` | `3c2cfd83…cdd6a` | advisory (extractor log) |
| `layout-be.log` | `d42d2669…7ed6` | advisory (all-BE reader exits 2) |
| `unblob-handler-excerpt.py.txt` | `03d96f4a…2b8c` | advisory (handler source quote + pattern match) |
| `timing.json` | `37301aa8…ad97` | advisory (run timings, byte-identical reproduction) |

Fragment (verbatim, merge-ready):

```json
{"id":"V3","sha256":"c4f74f54a65e861e22f5d6a47977cdbb3b5345819174f33bc86c63d3d10f872a",
 "external":{"url":"https://download.avm.de/fritzbox/fritzbox-5490/other/fritz.os/FRITZ.Box_5490-07.31.image",
   "image_sha256":"770efb4e368a58104bf362c990114db8b70a5060932ce8bcec7ef1bc75045ab7",
   "member":"./var/tmp/filesystem.image",
   "member_sha256":"87cc5d6b3ad105221114a86f6a4d4d868f731b868ff875979e7f0cb47bcea0f8",
   "length":30233394,"product":"FRITZ!Box 5490, FRITZ!OS 07.31"},
 "kind":"vendor",
 "oracle":"corpus/evidence/round-41/c1/V3/oracle.tsv",
 "nonregular":"corpus/evidence/round-41/c1/V3/nonregular.tsv"}
```

`length` is the **carve** length (30 233 394), matching the round-40 convention where `length` equals the
carrier size. Lane rebuild (no vendor bytes committed):

```
curl -sS -o 5490.image 'https://download.avm.de/fritzbox/fritzbox-5490/other/fritz.os/FRITZ.Box_5490-07.31.image'
sha256sum 5490.image                                   # 770efb4e…5ab7
tar -xf 5490.image -C m ./var/tmp/filesystem.image
sha256sum m/var/tmp/filesystem.image                   # 87cc5d6b…a0f8
python3 -c "open('V3.carrier','wb').write(open('m/var/tmp/filesystem.image','rb').read(30233394))"
sha256sum V3.carrier                                   # c4f74f54…872a
python3 -I -B tools/round-40/sqfs-list.py --layout avm --files oracle.tsv --nonregular nonregular.tsv V3.carrier
```

---

## 6. Risks and notes for the freeze (nothing here blocks V3)

1. **The frozen envelope does not exist yet — by rule.** The reserved-carrier bound forbids REA/unblob on
   V3 or its members, so *no one has measured V3's REA after-receipt*. [INFERENCE] Its shape is that of
   round-40 V2 (same 8/85/9/1 counts, same xz AVM wrapper, same `dev/led` char device, same dangling
   `sbin/udevadm -> /usr/bin/udevadm`), which scored `matched` at round 40 under `plus-extractor` — so the
   frozen predicate should hold once the counter runs REA at the freeze, but that is an argument, not a
   measurement.
2. **`dev/led` is never published unprivileged.** `sasquatch-v4be` exits 0 (`-no-exit-code`) with
   `created 0 devices`. The round-40 gap rule sets `allowed["char-device"] = []` and
   `required["char-device"] = false`, and `nonregular_unpublished_ok` only rejects a *published regular
   path that equals a non-regular oracle path* — so the missing device is not a failure, but the round-41
   counter must not start requiring char-device publication.
3. **Four dangling absolute/in-tree symlinks** ride along: `sbin/udevadm -> /usr/bin/udevadm` (no `usr`
   dir), `sbin/showaddrs -> /./sbin/showroutes` (no such entry), `sbin/localize -> /sbin/eventadd`,
   `bin/usermand -> usermand2`. All are classified `inside`/`absolute-inside` and
   `escaping_symlinks=0`; a future "sanitise escaping links" change in the counter must not reclassify them.
4. **V3 exercises no path collision** (§3.4). The R41-C1 selftest cases for R40-CL1 must come from L3/L4
   and counter fixtures; V3 contributes symlink *volume* (85 published links), not collision coverage.
5. **V3 is shape-identical to the round-40 V2 carrier** (8 regular files / 95 non-regular, xz, marker).
   Bytes differ — 4 of 8 files differ in digest and size, five symlink members swap (`+supportdata_argo.fiber`,
   `+fsck.ext2/3/4`, `-iwgetid/iwlist/iwpriv/iwspy`) — but the *class* of carrier is the same. If the
   freeze wants four independent carriers, V3 and V2 are two samples of one wrapper body layout; that
   overlap is a calibration note for the L1, not a defect in V3.
6. **The carve length matters.** The member carries 3286 trailing bytes (last 8 non-zero). Any tool that
   carves to the member length, or appends, produces a different sha256 than the pin `c4f74f54…`.
7. **Observation (not this seat's item):** the V3 wrapper contains a full nested core,
   `filesystem_core.squashfs`, 29 597 696 bytes, sha256 `cc6c1925…be43`, magic `sqsh`,
   `mkfs_time == bytes_used == 29596276`, 7361 inodes, xz — i.e. an AVM-layout full rootfs inside the 5490
   wrapper. [INFERENCE] it would be a viable V4-shaped body if the 5491 nested core did not qualify; it was
   **not** extracted or further analysed by this seat.

---

## 7. Compliance

- **Reserved carriers untouched:** no REA, no unblob on the 5490 image or anything carved from it; no
  command of any kind ran on the 3490/5491/7560 images or on L3/L4. The only extractors used on V3 bytes
  were `sqfs-list.py` (reader) and `sasquatch-v4be` (GPL squashfs-tools binary, explicitly assigned).
- **No VCS mutation:** only `sha256sum`/`diff`/`cat`/`ls` reads; no git command was issued.
- **No writes outside scope:** artifacts only under
  `.ufo/waves/round-41/w1/artifacts/R41C1VendorV3/`, plus this report. No vendor bytes copied into the lane.
- **No tool install/upgrade** was needed (no pacman, uv, npx or PATH writes).
- **Scratch removed:** `/fast/scratch/hyaku/kaidoku-r41/R41C1VendorV3` deleted after every cited file was
  copied into the artifacts directory; the assets above are the retained evidence.
