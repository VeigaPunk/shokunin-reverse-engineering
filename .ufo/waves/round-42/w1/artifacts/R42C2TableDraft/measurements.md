# Measurements for block 21 (table v4) — commands, exit codes, verbatim output

Regenerate: `./make-measurements.sh > measurements.md` in this directory.

## 0. Pins

```
# installed sources (sha256 must equal the SOURCES row pins)
2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287  handlers/filesystem/squashfs.py
1bb498119429ed80ae29caf9772d2b6210c22b6a8a2c8beb6cfea94550bcd23a  extractor.py
2329783fc645de8aae94b82443277bceb6ceac968549ff65917c7b2d454cc9ee  report.py
8ae7d2a3980b80b25274d2351a724631be40c79bc8a2da3be14dae2bf09f85af  extractors/command.py
# REA 6.5.0 dist files
bb4f3246bee70a5b32b048e5ef956e649626b6449b1d457454440739a8d51029  firmware/FirmwarePublication.js
2cbc1cc4ceaa760a8e47b8883a6b7b85040d640032546864fa9cba4898243aa5  domain/firmware/firmwareAnalysis.js
9876cd9a9803fc46ee7a78c8f244e1211727c12fc52387412d05823058d66801  firmware/FirmwareRelease.js
# readers
unsquashfs version 4.7.5 (2026/03/01)
 64-bit locale=en_US.UTF-8 Threads:32 OPEN_MAX:524288, ASM
```

## 1. Fixtures (unblob 26.6.4 test fixtures, MIT; LFS media path)

```
base=https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs
# fetched: squashfs_v1/big_endian/__input__/squashfs_v1.0_be.bin
#          squashfs_v2/big_endian/__input__/squashfs_v2.0_be.bin
#          squashfs_v3/little_endian/__input__/squashfs_v3_le.bin
#          squashfs_v3/big_endian/__input__/squashfs_v3_be.bin
# rebuild: curl -sSL -o <name> "$base/<handler>/<endian>/__input__/<name>"
529e10775cc152e6c5df0c6c63316811004cc73ce99f03989c86ffd396d631e6  squashfs_v1.0_be.bin
79c0f3886291f4abcc656acd49932446cf16afaa67e6ffb0c5258e3c2e2dfcc0  squashfs_v2.0_be.bin
4e9493d9c6f868005dea8f11992129c3399e0bcb8f3a966c750cb925989ca97c  squashfs_v3_be.bin
0161351caec8e9da6e3e5ac7b046fd11d832efb18eb09e33011e6d19d50cd1f7  squashfs_v3_le.bin
4096 squashfs_v1.0_be.bin
4096 squashfs_v2.0_be.bin
4096 squashfs_v3_be.bin
4096 squashfs_v3_le.bin
```

## 2. unsquashfs 4.7.5 and 7-Zip 26.04 read v1, v2 and v3 (both endiannesses)

```
$ unsquashfs -s squashfs_v1.0_be.bin | grep 'Found a valid'
Found a valid big endian SQUASHFS 1:0 superblock on /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C2TableDraft/squashfs_v1.0_be.bin.
$ unsquashfs -lls squashfs_v1.0_be.bin
Reading a different endian SQUASHFS filesystem on /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C2TableDraft/squashfs_v1.0_be.bin
drwxrwxrwx vgpnk/vgpnk              42 2024-08-05 04:18 squashfs-root
-rw-rw-r-- vgpnk/vgpnk               6 2024-08-05 03:53 squashfs-root/apple.txt
-rw-rw-r-- vgpnk/vgpnk               7 2024-08-05 04:18 squashfs-root/banana.txt
-rw-rw-r-- vgpnk/vgpnk               7 2024-08-05 03:54 squashfs-root/cherry.txt
  exit=0

$ unsquashfs -s squashfs_v2.0_be.bin | grep 'Found a valid'
Found a valid big endian SQUASHFS 2:0 superblock on /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C2TableDraft/squashfs_v2.0_be.bin.
$ unsquashfs -lls squashfs_v2.0_be.bin
Reading a different endian SQUASHFS filesystem on /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C2TableDraft/squashfs_v2.0_be.bin
drwxrwxr-x vgpnk/vgpnk              56 2022-04-06 08:20 squashfs-root
-rw-rw-r-- vgpnk/vgpnk               7 2022-04-06 08:44 squashfs-root/apple1.txt
-rw-rw-r-- vgpnk/vgpnk               7 2022-04-06 08:44 squashfs-root/apple2.txt
-rw-rw-r-- vgpnk/vgpnk               7 2022-04-06 08:44 squashfs-root/apple3.txt
-rw-rw-r-- vgpnk/vgpnk               7 2022-04-06 08:44 squashfs-root/apple4.txt
  exit=0

$ unsquashfs -s squashfs_v3_be.bin | grep 'Found a valid'
Found a valid big endian SQUASHFS 3:0 superblock on /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C2TableDraft/squashfs_v3_be.bin.
$ unsquashfs -lls squashfs_v3_be.bin
Reading a different endian SQUASHFS filesystem on /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C2TableDraft/squashfs_v3_be.bin
drwxrwxr-x vgpnk/vgpnk              41 2021-11-22 11:42 squashfs-root
-rw-rw-r-- vgpnk/vgpnk               6 2021-11-22 11:42 squashfs-root/apple.txt
-rw-rw-r-- vgpnk/vgpnk               7 2021-11-22 11:42 squashfs-root/cherry.txt
  exit=0

$ unsquashfs -s squashfs_v3_le.bin | grep 'Found a valid'
Found a valid little endian SQUASHFS 3:0 superblock on /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C2TableDraft/squashfs_v3_le.bin.
$ unsquashfs -lls squashfs_v3_le.bin
drwxrwxr-x vgpnk/vgpnk              41 2021-11-22 11:42 squashfs-root
-rw-rw-r-- vgpnk/vgpnk               6 2021-11-22 11:42 squashfs-root/apple.txt
-rw-rw-r-- vgpnk/vgpnk               7 2021-11-22 11:42 squashfs-root/cherry.txt
  exit=0

$ 7z l squashfs_v3_le.bin   (tail)
Characteristics = DUPLICATES_REMOVED
Code Page = UTF-8

   Date      Time    Attr         Size   Compressed  Name
------------------- ----- ------------ ------------  ------------------------
2021-11-22 11:42:16 .....            6           13  apple.txt
2021-11-22 11:42:22 .....            7            0  cherry.txt
------------------- ----- ------------ ------------  ------------------------
2021-11-22 11:42:22                 13           13  2 files
  exit=0

$ 7z l squashfs_v3_be.bin   (tail)
Characteristics = DUPLICATES_REMOVED
Code Page = UTF-8

   Date      Time    Attr         Size   Compressed  Name
------------------- ----- ------------ ------------  ------------------------
2021-11-22 11:42:16 .....            6           13  apple.txt
2021-11-22 11:42:22 .....            7            0  cherry.txt
------------------- ----- ------------ ------------  ------------------------
2021-11-22 11:42:22                 13           13  2 files
  exit=0

```

## 3. unblob 26.6.4 argv on a v1-v3 chunk (plain sasquatch, -le or -be)

```
unblob exit=0
2026-10-26 22:10.56 [debug    ] Calculating chunk for pattern match handler=squashfs_v3 pid=1123180 real_offset=0x0 start_offset=0x0
2026-10-26 22:10.56 [debug    ] Running extract command        command='sasquatch -le -no-exit-code -f -d squashfs_v3_le.bin_extract /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C2TableDraft/squashfs_v3_le.bin' pid=1123180

unblob exit=0
2026-10-26 22:10.56 [debug    ] Calculating chunk for pattern match handler=squashfs_v3 pid=1126691 real_offset=0x0 start_offset=0x0
2026-10-26 22:10.56 [debug    ] Running extract command        command='sasquatch -be -no-exit-code -f -d squashfs_v3_be.bin_extract /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C2TableDraft/squashfs_v3_be.bin' pid=1126691

```

## 3b. The residue: unblob's unknown-chunk carve and REA's gap mint

```
S118 extractor.py:116: def carve_unknown_chunk(
S118 extractor.py:117:     extract_dir: Path, file: File, chunk: UnknownChunk | PaddingChunk
S118 extractor.py:118: ) -> Path:
S118 extractor.py:119:     extension = "unknown"
S118 extractor.py:120:     if isinstance(chunk, PaddingChunk):
S118 extractor.py:121:         extension = "padding"
S118 extractor.py:122: 
S118 extractor.py:123:     filename = f"{chunk.start_offset}-{chunk.end_offset}.{extension}"
S118 extractor.py:124:     carve_path = extract_dir / filename
S118 extractor.py:125:     logger.info("Extracting unknown chunk", path=carve_path, chunk=chunk)
S119 FirmwarePublication.js:226:         kind,
S119 FirmwarePublication.js:227:         input_path: chunk.input_path,
S119 FirmwarePublication.js:228:         ...emptyGap,
S119 FirmwarePublication.js:233:         dependencies: [],
S119 FirmwarePublication.js:234:         continuation_id: kind === "unknown-chunk-handler" &&
S119 FirmwarePublication.js:235:             chunk.input_path.startsWith("$output/")
S119 FirmwarePublication.js:236:             ? nestedContinuationId(chunk.input_path)
S119 FirmwarePublication.js:286:         ...chunkGaps("unknown-chunk-handler", (chunk) => chunk.handler === null),
```

## 4. Damage arms: both readers fail with sasquatch's message

```
=== zeroed 0x40-0x80
  unsquashfs -s   exit=0
  unsquashfs -lls exit=1
    read_ids: Bad inode count in super block
    FATAL ERROR: File system corruption detected
  sasquatch       exit=1
    read_ids: Bad inode count in super block
    FATAL ERROR: File system corruption detected
=== zeroed 0x60-0x100
  unsquashfs -s   exit=0
  unsquashfs -lls exit=1
    parse_exports_table: Bad inode count in super block
    FATAL ERROR: File system corruption detected
  sasquatch       exit=1
    parse_exports_table: Bad inode count in super block
    FATAL ERROR: File system corruption detected
=== zeroed 0xD0-0x110
  unsquashfs -s   exit=0
  unsquashfs -lls exit=1
    read_fragment_table: failed to read fragment table block
    FATAL ERROR: File system corruption detected
  sasquatch       exit=1
    read_fragment_table: failed to read fragment table block
    FATAL ERROR: File system corruption detected
=== zeroed 0xC0-0x100
  unsquashfs -s   exit=0
  unsquashfs -lls exit=1
    read_fragment_table: failed to read fragment table block
    FATAL ERROR: File system corruption detected
  sasquatch       exit=1
    read_fragment_table: failed to read fragment table block
    FATAL ERROR: File system corruption detected
=== zeroed 0xE0-0x102
  unsquashfs -s   exit=0
  unsquashfs -lls exit=1
    read_fragment_table: failed to read fragment table block
    FATAL ERROR: File system corruption detected
  sasquatch       exit=1
    read_fragment_table: failed to read fragment table block
    FATAL ERROR: File system corruption detected
=== zeroed 0x60-0x70
  unsquashfs -s   exit=0
  unsquashfs -lls exit=1
    parse_exports_table: Bad inode count in super block
    FATAL ERROR: File system corruption detected
  sasquatch       exit=1
    parse_exports_table: Bad inode count in super block
    FATAL ERROR: File system corruption detected

=== intact body (control)
  unsquashfs -lls exit=0
  sasquatch       exit=0
    oi/x/apple.txt
    oi/x/cherry.txt
```

## 5. The drafted block parses in situ, and its reader's selftest

```
$ make-fixture.sh LANE c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c $T/fixture-SKILL.md
fixture written: fixture-SKILL.md (1570 lines)
$ v4-refparse.py --skill $T/fixture-SKILL.md --table-only   (head)
skill: /fast/scratch/hyaku/kaidoku-r42/R42C2TableDraft/r42meas.pHOoNl/fixture-SKILL.md
marker line: 525  actions line: 526  table line: 527  rules: 15
actions (14): none inspect-input install-extractor-be install-extractor-le wrap-extractor-be cross-read-legacy isolate-residue preserve-failure salvage-partial raise-depth audit-symlinks expect-link-absent count-gap confirm-empty
1. container-depth-limited  (line 529)
$ v4-refparse.py --selftest
ok   match-single-row                 ('clean', 'none')
ok   domain-mismatch                  domain guard
cases: 12, failures: 0
```

## 6. Drafted block vs the drafted precedence

```
$ python3 -I -B LANE/tools/round-41/sqfs-triage-v3.py --skill $T/base-SKILL.md LANE/corpus/evidence/round-41/c2/heldout/*/envelope.json > $T/c-v3pairs.tsv
  rows=52 exit=0
$ python3 -I -B check.py --skill $T/fixture-SKILL.md --heldout LANE/corpus/evidence/round-41/c2/heldout \
      --dev <the 8 dev envelopes> --out-prefix $T/c
table: marker 525 actions 526 table 527 rules 15 actions 14
labels (15): container-depth-limited no-squashfs-chunk dep-missing-be dep-missing-le partial-body-failure avm-marker-be-dropped legacy-body-failure body-extractor-failure unknown-residue depth-limited mixed-symlinks escaping-symlink-removed in-tree-symlink-metadata clean clean-empty
grid: 38664 points, 38664 agree, 0 other
heldout: 52 envelopes, 52 agree, 0 seam, 0 other; v4==v3 on 52
dev dev-v3le-d1.json   H=squashfs_v3 G=depth-limited P=2 -> v4 depth-limited/raise-depth, prec depth-limited/raise-depth
dev dev-v3le-d3.json   H=squashfs_v3 G=none P=2 -> v4 clean/none, prec clean/none
dev trx-img-with.json  H= G=depth-limited P=3 -> v4 container-depth-limited/raise-depth, prec container-depth-limited/raise-depth
dev trx-img-without.json H= G=depth-limited P=3 -> v4 container-depth-limited/raise-depth, prec container-depth-limited/raise-depth
dev trx-fs-with.json   H=squashfs_v3 G=depth-limited,unpublished-entry P=156 -> v4 depth-limited/raise-depth, prec depth-limited/raise-depth
dev trx-fs-without.json H=squashfs_v3 G=missing-extractor-dependency P=0 -> v4 dep-missing-le/install-extractor-le, prec dep-missing-le/install-extractor-le
dev x86-fs-with.json   H=squashfs_v3 G=depth-limited,unknown-chunk-handler,unpublished-entry P=138 -> v4 unknown-residue/isolate-residue, prec unknown-residue/isolate-residue
dev x86-fs-without.json H=squashfs_v3 G=missing-extractor-dependency,unknown-chunk-handler P=2 -> v4 dep-missing-le/install-extractor-le, prec dep-missing-le/install-extractor-le
  exit=0
```

## 7. R41-CL4 executed: the same legacy envelopes under v3 and under v4

```
$ python3 -I -B LANE/tools/round-41/sqfs-triage-v3.py --skill $T/base-SKILL.md <the 8 dev envelopes>
dev-v3le-d1.json	unclassified	none
dev-v3le-d3.json	unclassified	none
trx-img-with.json	no-squashfs-chunk	inspect-input
trx-img-without.json	no-squashfs-chunk	inspect-input
trx-fs-with.json	unclassified	none
trx-fs-without.json	unclassified	none
x86-fs-with.json	unclassified	none
x86-fs-without.json	unclassified	none
$ python3 -I -B v4-refparse.py --skill fixture-SKILL.md --json <the 8 dev envelopes>
dev-v3le-d1.json	depth-limited	raise-depth	10
dev-v3le-d3.json	clean	none	14
trx-img-with.json	container-depth-limited	raise-depth	1
trx-img-without.json	container-depth-limited	raise-depth	1
trx-fs-with.json	depth-limited	raise-depth	10
trx-fs-without.json	dep-missing-le	install-extractor-le	4
x86-fs-with.json	unknown-residue	isolate-residue	9
x86-fs-without.json	dep-missing-le	install-extractor-le	4
```

## 8. The four round-41 C1 receipts (real AVM envelopes), v4 and v3

```
corpus/evidence/round-41/c1/V3/after.json	depth-limited	raise-depth	10
corpus/evidence/round-41/c1/V4/after.json	depth-limited	raise-depth	10
corpus/evidence/round-41/c1/L3/after.json	depth-limited	raise-depth	10
corpus/evidence/round-41/c1/L4/after.json	depth-limited	raise-depth	10
corpus/evidence/round-41/c1/V3/after.json	depth-limited	raise-depth
corpus/evidence/round-41/c1/V4/after.json	depth-limited	raise-depth
corpus/evidence/round-41/c1/L3/after.json	depth-limited	raise-depth
corpus/evidence/round-41/c1/L4/after.json	depth-limited	raise-depth
```

## 9. REA 6.5.0 dev-arm envelopes (commands as run)

```
cd $S && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \
  --format json --full-output --max-depth 1 fx/squashfs_v3_le.bin out/rea-v3le     # exit 0
cd $S && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \
  --format json --full-output --max-depth 3 fx/squashfs_v3_le.bin out/rea-v3le-d3  # exit 0
# the envelopes are copied here as dev-v3le-d1.json (--max-depth 1) and dev-v3le-d3.json (3):
feba02a3188182f6b4d20c7389a355a65249b7c1c04d0df6d69f28125eb9deea  dev-v3le-d1.json
ffe6d8db3f0fa6623975e0bf1120f33b8ecfa8c91c60ca2ffeb26e7f68e2dbb8  dev-v3le-d3.json
dev-v3le-d1.json  H=['squashfs_v3'] G=['depth-limited'] P=2 BE=n/a SR=no diag_files=0 -> precedence depth-limited/raise-depth
dev-v3le-d3.json  H=['squashfs_v3'] G=none P=2 BE=n/a SR=no diag_files=0 -> precedence clean/none
```
