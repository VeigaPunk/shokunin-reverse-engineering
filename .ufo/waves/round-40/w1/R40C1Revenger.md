# R40C1Revenger — where the AVM layout is handled (unblob 26.6.4 / sasquatch 4.5.1 / REA 6.5.0)

**Verdict: CONFIRMED** — the AVM-BE reading path is exactly *big-endian structs + little-endian
2-byte block-length headers*, implemented by unblob's marker branch (no `-be`) and sasquatch-v4be's
`FIX_BE` build with `swap = 0`; all three testable sentences hold on the round-11 fixture at 4/4
metadata-block boundaries. **One binding defect for R40-C1:** REA 6.5.0 does **not** record the
sasquatch child argv for a successful run, so “`-be` absent from the child argv” cannot be checked
on a successful C1 receipt; bind on `handler_name` + carrier-byte recomputation + rerun projection
instead.

Seat: leaf, round 40 wave 1 (pre-freeze). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` at `fa6a8a3f85ec` (read-only git only; nothing
committed or staged). No REA or unblob **CLI** run was made at all: no C1 carrier, no V1 vendor
image, no held-out carrier was extracted. The extraction evidence below is direct `sasquatch` /
`sasquatch-v4be` on a round-11 development fixture and on a lane-built control, plus the installed
unblob handler code invoked as a library. No tool installed, no pacman transaction; sasquatch,
sasquatch-v4be and unblob untouched.

## Inputs and identities

| input | identity |
|---|---|
| unblob handler (installed) | `/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`, 590 lines (equals S108/S112) |
| sasquatch sources at tag `sasquatch-v4.5.1-6` | commit `15573bf46c671c8ed23e8c0c50e6187e0c8d0b62`; file hashes in `artifacts/source-anchors.txt` and the draft SOURCES row |
| `sasquatch` / `sasquatch-v4be` binaries | 4.5.1 (2022/03/17); sha256 `ad02d27a…4754` / `fac88740…214c6` (equal to S107's package members) |
| REA | `rea-agents 6.5.0` under `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`; `dist/firmware/FirmwareCommand.js` sha256 `20ac4a27…5ca7`, `dist/firmware/FirmwareProvider.js` sha256 `3c1e929b…1654` |
| round-11 fixture (development) | `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/avm-be.squashfs` (read-only), 4096 B, sha256 `c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32`; copy in artifacts |
| lane-built control | `stdbe-control.squashfs`, 812 B, sha256 `5b7dcfe3f1a5cdf145e0b2b3dc449e3eaed22cbbce06d27d9f9bb0c4e775ee8d` |

## 1. unblob 26.6.4 — marker test, argv build, chunk end, validation

File: `.../unblob/handlers/filesystem/squashfs.py` (all line numbers from the installed copy).

**Marker test and argv build** (`SquashFSExtractor.extract`, `:33-66`):

```python
33  with File.from_path(inpath) as file:
34      endian = get_endian(file, self.big_endian_magic)        # magic only (file_utils.py:350-361)
...
39  match endian, self.version:
40      case Endian.BIG, 4:
41          executable = self.V4BE_EXECUTABLE                 # "sasquatch-v4be" (:26)
42          struct_parser = StructParser(SquashFSv4LEHandler.C_DEFINITIONS)
43          with File.from_path(inpath) as f:
44              header = struct_parser.parse(
45                  SquashFSv4LEHandler.HEADER_STRUCT, f, Endian.BIG
46              )
47              # see .../freetz/.../AVM-BE-format.txt
48              is_avm = header.bytes_used == header.mkfs_time
49              if not is_avm:
50                  commands_args.append("-be")
51      case Endian.BIG, _:  commands_args.append("-be")
53      case Endian.LITTLE, _: commands_args.append("-le")
56  commands_args.extend(["-no-exit-code", "-f", "-d", "{outdir}", "{inpath}"])
65  extractor = Command(executable, *commands_args)
66  extractor.extract(inpath, outdir)
```

So: handler selection is pattern/magic based (`:516-523`, `73 71 73 68 [24] 00 04`); **extractor
argument selection** is marker based on the v4-BE branch only. `-be` is appended *iff* the marker
does not hold. The tail is exactly `-no-exit-code -f -d {outdir} {inpath}` (`:56-63`).

**Chunk end for v4 BE** (`_SquashFSBase.calculate_chunk`, `:77-98`, shared by every version):

```python
82  end_of_data_offset = (start_offset + header.bytes_used) & 0xFF_FF_FF_FF
83  file.seek(end_of_data_offset)
84  padding = file.read(round_up(header.bytes_used, max(PAD_SIZES)) - header.bytes_used)
88  for pad_size in sorted(PAD_SIZES, reverse=True):           # 4096, then 1024
89      size = round_up(header.bytes_used, pad_size)
92      if padding.startswith(b"\00" * padding_length):
93          end_offset = start_offset + size
96  return ValidChunk(start_offset=..., end_offset=start_offset + header.bytes_used)
```

Yes, it rounds `bytes_used` up to 4096 then 1024 **only if the tail is zero-filled**; otherwise the
chunk ends at `start + bytes_used`. Two details worth recording: the seek target is masked to 32
bits (`& 0xFFFFFFFF`) while `round_up` uses the unmasked `bytes_used` — a latent wrap for images
≥ 4 GiB (no carrier is that large); and the header is parsed with `Endian.BIG` by `get_endian`, so
`bytes_used` itself is correct for BE.

**Block-length validation: none.** `calculate_chunk` parses only the 96-byte superblock and the
zero padding; `StructHandler.parse_header` (`unblob/models.py:571-574`) just unpacks the struct.
No metadata block is traversed and no 2-byte length header is read by the handler. Whether a
carrier is a real AVM layout or a marker-only standard-BE body is only discovered when sasquatch
runs.

**Direct handler run on the fixture** (`artifacts/unblob-handler-probe.py`, run with the unblob
venv interpreter, exit 0): `magic-endian=Endian.BIG`, `chunk=0x0-0x1000`,
`bytes_used=365 mkfs_time=365 is_avm=True`, `argv_tail=[] (no -be)`.

## 2. sasquatch 4.5.1 — what `sasquatch-v4be` without `-be` does, and what `-be` changes

File set at tag `sasquatch-v4.5.1-6` (hashes and full excerpts in `artifacts/source-anchors.txt`).

**The build really is two builds of one tree** (`debian/rules:9-18`):

```make
12  override_dh_auto_install:
13      dh_auto_clean
14      dh_auto_build
15      dh_auto_install -- INSTALL_DIR=$(CURDIR)/debian/sasquatch/usr/bin
16      dh_auto_clean
17      CFLAGS=-DFIX_BE dh_auto_build
18      cp $(CURDIR)/squashfs-tools/sasquatch $(CURDIR)/debian/sasquatch/usr/bin/sasquatch-v4be
```

`sasquatch` is the unsquashfs tool (`Makefile:409 sasquatch: $(UNSQUASHFS_OBJS)`), and
`read_fs.o` is **mksquashfs-only** (`Makefile:181-185`), so the `read_block` that the extractor
uses is the one in `unsquashfs.c:653`, not the compile-time-swapping one in `read_fs.c:46`.

**Compile-time half — `FIX_BE` swaps every filesystem struct, unconditionally**
(`squashfs_swap.h:32`):

```c
32  #if __BYTE_ORDER == __BIG_ENDIAN || defined FIX_BE
...
294 /* big endian architecture swap in-place macros */
295 #define SQUASHFS_INSWAP_SUPER_BLOCK(s)  _SQUASHFS_SWAP_SUPER_BLOCK(s, s, INSWAP_LE)
...
342 #define SQUASHFS_INSWAP_SHORTS(s, n)    inswap_le16_num(s, n)
```

with the byte primitives in `swap.c:24` (same guard), `:63-67`:

```c
24  #if __BYTE_ORDER == __BIG_ENDIAN || defined FIX_BE
63  unsigned short inswap_le16(unsigned short num)
65      return (num >> 8) | ((num & 0xff) << 8);
106 #define INSWAP_LE_NUM(BITS, TYPE) ... s[i] = inswap_le##BITS(s[i]);
```

Applied at `unsquash-4.c:697` (`SQUASHFS_INSWAP_SUPER_BLOCK(&sBlk_4)`) and `:46`
(`SQUASHFS_INSWAP_INTS(block_list, blocks)`), among others. On an LE host this makes the v4be
binary read the superblock, inode headers, directory entries and inode block-list sizes as
big-endian **regardless of any command-line flag**.

**Runtime half — only the 2-byte block-length header obeys `swap`** (`unsquashfs.c:653-670`):

```c
664 if(swap) {
665     if(read_fs_bytes(fd, start, 2, &c_byte) == FALSE) goto failed;
667     c_byte = (c_byte >> 8) | ((c_byte & 0xff) << 8);
668 } else
669     if(read_fs_bytes(fd, start, 2, &c_byte) == FALSE) goto failed;
```

`swap` is decided once in `read_super` (`unsquashfs.c:2252-2286`) by a heuristic on the generic
superblock, **inverted by `FIX_BE`**:

```c
2263 if(generic.s_major < SQUASHFS_MIN_VERSION || generic.s_major > SQUASHFS_MAX_VERSION
2265    || (generic.inodes & 0xFF) == 0) {
2267     ERROR("... suggests a SquashFS image of a different endianess\n", ...);
2269 #ifdef FIX_BE
2270     swap = 0;
2271 #else
2272     swap = 1;
2273 #endif
```

and `-be` / `-le` override the heuristic (`unsquashfs.c:4389-4400`): on an LE host `-be` sets
`swap = 1`, `-le` sets `swap = 0`.

Net effect on an AVM image (`sqsh`, `s_major = 4` stored BE): the generic read on an LE host sees
`s_major = 0x0400 = 1024` → “different endianess”; with `FIX_BE` that yields `swap = 0`, so the
length header is read little-endian while all structs are swapped big-endian. **`-be` changes only
the block-length header byte order (and suppresses the heuristic); it never changes the struct
endianness of this binary.** That is precisely the AVM-BE layout.

Measured (exact commands and full output in the artifacts):

| input | argv | exit | result |
|---|---|---|---|
| round-11 AVM fixture | `sasquatch-v4be` (no flag) | 0 | 4 files: `apple1.txt`=`apple\n`, `apple2.txt`=`banana\n`, `apple3.txt`=`cherry\n`, `apple4.txt`=`date\n` |
| round-11 AVM fixture | `sasquatch-v4be -be` | 1 | `read_id_table: failed to read id table block` / `FATAL ERROR: File system corruption detected`; 0 files |
| round-11 AVM fixture | `sasquatch` (no FIX_BE) | 1 | `FATAL ERROR: Block size too small. File system is corrupt.`; 0 files |
| lane-built standard BE (`stdbe-control.squashfs`, marker false, header `80a8`) | `sasquatch-v4be` | 1 | `read_id_table: failed to read id table block`; 0 files |
| same | `sasquatch-v4be -be` | 0 | `bin/run`, `docs/data.txt` |

The first stderr line `SquashFS version [1024.0] … suggests … a different endianess` is **not** a
failure signal: it appears on the successful no-flag AVM run and on the failing no-flag
standard-BE run alike (it is emitted at `:2267-2268` whenever the heuristic fires). Only exit code
plus extracted entry count separate the outcomes.

## 3. REA 6.5.0 — is the sasquatch child argv recorded for a **successful** run?

**No.** Three sites, then the receipt evidence:

- `dist/firmware/FirmwareCommand.js:155-163` returns
  `{ stdout, stderr, exit_code, signal, command, args, resource_limiter }` for the **top-level**
  process only (the `REA_UNBLOB_COMMAND` executable resolved at `:17-49`).
- `dist/firmware/FirmwareProvider.js:227-244` builds the unblob argv
  (`--process-num 1 --depth … --report … --log … --extract-dir … <input>`), and `:215` / `:279`
  assemble `raw = { report, execution: processRun, version_execution: versionRun }`. Nothing
  captures sasquatch.
- unblob records the extractor command **only on failure**:
  `unblob/extractors/command.py:59-65` constructs
  `ExtractCommandFailedReport(command=shlex.join(cmd), stdout, stderr, exit_code)` and raises;
  `report.py:91-95` is that report’s schema (`command: str`). The successful `ChunkReport`
  (`report.py:225-239`) carries `extraction_reports`, and it is empty.

Receipt evidence (`artifacts/rea-argv-evidence.txt`):

- round-39 C1 **K1** `after.json` (success): `raw_result.execution.command = …/unblob`,
  `args = [--process-num 1 …]`; the `ChunkReport` is `squashfs_v4_be` with
  `extraction_reports = []`; the whole receipt contains **0** occurrences of `sasquatch` and **0**
  of `-be`.
- round-39 C2 held-out **H13** (`avm-marker-be-dropped`, a marker-only standard-BE body) fails and
  therefore records `sasquatch-v4be -no-exit-code -f -d …` (no `-be`, exit 1); **H15**
  (`body-extractor-failure`) records `sasquatch-v4be -be -no-exit-code -f -d …` (exit 1).

**Consequence for R40-C1.** A successful C1 receipt cannot be audited for `-be` in the child argv,
because no child argv exists in the envelope. The counter must bind the AVM claim on what the
receipt *does* carry (`handler_name = squashfs_v4_be`, no failed chunk, published files) plus bytes
it can recompute from the pinned carrier (superblock BE + marker + LE metadata headers), plus the
scoring-time rerun projection. Asking for a `-be` field on success would be an unsatisfiable
predicate; asking for it only on failure would invert the claim.

## 4. The AVM layout rule as three testable sentences, tested on the round-11 fixture

> **S1 (superblock).** An AVM-layout SquashFS v4 image starts with a big-endian 96-byte superblock:
> magic `sqsh`, `s_major` (u16 @28) = 4, and `mkfs_time` (u32 @8) numerically equals `bytes_used`
> (u64 @40).
>
> **S2 (block-length headers).** Every metadata block-length header in that image is little-endian:
> the first one sits at `inode_table_start`; `LE(hdr) & 0x7fff` is ≤ 8192, its payload decodes
> (xz or stored) and the chain starts there, while `BE(hdr) & 0x7fff` is either > 8192 or overruns
> the used region. On a small image the stronger identity holds for **every** metadata block:
> `off + 2 + size` (LE) lands exactly on the next structural boundary.
>
> **S3 (extractor).** Because of S1+S2, stock `sasquatch-v4be` with **no** `-be` extracts the tree,
> while `sasquatch-v4be -be` and plain `sasquatch` fail on the same bytes; unblob 26.6.4 therefore
> yields `handler = squashfs_v4_be` with the argv `sasquatch-v4be -no-exit-code -f -d {outdir} {inpath}`.

Measured on `avm-be.squashfs` (`artifacts/avm-fixture-probe.txt`, stdlib only, exit 0):

**S1 — true.** `magic=b'sqsh'`, `s_major=4`, `s_minor=0`, `mkfs_time=365`, `bytes_used=365`.
Other fields: `block_size=65536`, `fragments=1`, `compression=4` (xz), `block_log=16`,
`inode_table_start=121`, `directory_table_start=239`, `fragment_table_start=343`,
`id_table_start=357`, `bytes_used=365`.

**S2 — true, 4/4.** The two index arrays are BE u64 at 343 → 325 and 357 → 351; the metadata
blocks then chain:

| block | header | LE size | kind | `next` | boundary |
|---|---|---|---|---|---|
| inode table @121 | `74 00` | 116 | xz → 160 B raw | 239 | `directory_table_start` = 239 |
| directory table @239 | `54 80` | 84 | stored | 325 | fragment-table metadata block (index value) |
| fragment table @325 | `10 80` | 16 | stored | 343 | `fragment_table_start` = 343 |
| id table @351 | `04 80` | 4 | stored | 357 | `id_table_start` = 357 |

The BE decodes of the same headers are `29696`, `21632`, `4224`, `1152` (flag bits `0x8000` clear)
— none lands on a boundary, and the first is rejected outright by sasquatch's
`size > SQUASHFS_METADATA_SIZE (8192)` check. (The fragment-table and id-table blocks are reached
through the index arrays, as unsquashfs does: `unsquash-4.c:50-111` reads
`SQUASHFS_FRAGMENT_INDEX_BYTES` at `fragment_table_start` and then `read_block` on each index.)

**S3 — true.** `sasquatch-v4be` no flag: exit 0, 4 files. `-be`: exit 1, 0 files. Plain
`sasquatch`: exit 1, 0 files. unblob’s own handler: `chunk=0x0-0x1000`, `is_avm=True`, no `-be`;
the round-11 log independently shows
`Running extract command command='sasquatch-v4be -no-exit-code -f -d /tmp/r11-avm3/…'` with
`handler=squashfs_v4_be` (`round11/work/unblob.log:6,8`).

## 5. Divergences, limits, and what the L1 should change

1. **R40-C1 binding (defect):** do not test the child argv on a successful receipt (§3). Bind the
   `-be` decision through the frozen carrier bytes and the handler code; the receipt supplies
   `handler_name`, gaps and publication, and the rerun supplies provenance.
2. **Marker ≠ layout (confirmed, not just plausible):** round-39 held-out **H13** has
   `mkfs_time == bytes_used` (73710 == 73710) but BE block lengths; unblob drops `-be` and
   extraction fails (`artifacts/rea-argv-evidence.txt`). My control with marker false + BE headers
   gets `-be` and succeeds. The discriminating field is the block-length header, exactly as S2
   states. This also means a “marker holds” check alone cannot certify a genuine AVM carrier.
3. **Round-39 critic’s exactness limit is lifted for the fixture:** `R39AssimAvmCritic.md` used
   only `121 + 2 + 116 == 239` because the real vendor members have multi-block inode tables. The
   fixture permits a stronger test: all four metadata blocks plus both index arrays land exactly
   (4/4). On the 5.4 MB vendor member only plausibility is available; that extrapolation is
   **[INFERENCE]** until the counter recomputes each carrier’s first header (the claim only
   requires the first metadata block).
4. **Chunk-end quirk:** `(start_offset + bytes_used) & 0xFFFFFFFF` (`squashfs.py:82`) wraps the
   *seek* for ≥ 4 GiB images while the returned end is unmasked. Harmless for a 5,442,392-byte
   member; worth a comment if the lane ever pins a larger carrier.
5. **Dependency-report nuance:** when `sasquatch-v4be` is absent, the recorded
   `ExtractorDependencyNotFoundReport` lists only the failing executable
   (`Command.get_dependencies`, `command.py:101-102`), not both names from
   `SquashFSExtractor.get_dependencies` (`squashfs.py:68-69`). The round-11 log
   (`avm-final.log:19`, `dependencies=['sasquatch-v4be']`) is that path, not a contradiction of
   S108/S112.
6. **S112/S121 anchors are slightly loose:** S112 says “lines 44-50”; the decision is
   `48` (`is_avm`), `49` (`if not is_avm`), `50` (`append("-be")`). S121 anchors
   `unsquashfs.c` + `debian/rules` but not the `FIX_BE` files; see §6.
7. **Carrier-building consequence (for L1/L2):** `tools/round-39/gen-squashfs.py --endian avm`
   cannot produce this layout — the round-39 critic measured it byte-identical to `--endian be`
   with bytes 8..12 overwritten by `bytes_used` (`R39AssimAvmCritic.md`, sha256 `762c06a6…`), i.e.
   a marker-only standard-BE body. Lane-built genuine carriers need a writer that emits the 2-byte
   metadata headers LE. Compression is not part of the layout test — the `compression` field is
   itself BE, and `sasquatch-v4be`’s `read_block` is compression-agnostic (the fixture is xz; my
   standard-BE control is gzip); but no gzip AVM-layout carrier exists on this host yet, so the
   gzip half of L1/L2 is a build task, not a measurement.

## 6. Sources row

The sasquatch source **location** is already a lane row: **S121** (`corpus/SOURCES.md:127`) pins
the tag and `unsquashfs.c` + `debian/rules`. It does not anchor the two files that carry the
`FIX_BE` switch (`squashfs_swap.h:32`, `swap.c:24`) or the object split (`Makefile:181-185,409`).
`artifacts/sources-row-draft.md` therefore contains (a) that finding and (b) a ready 11-column
companion row (`S123`, draft) with seven file hashes and line anchors, for the L1 to either admit
or fold into S121's anchor cell. S112 (unblob handler) and S114 (Freetz note) already cover their
parts; no change proposed to either beyond the line-number note in §5.6.

## 7. Artifacts (all under this seat's artifacts directory)

| artifact | what it is |
|---|---|
| `round11-avm-be.squashfs` | byte copy of the round-11 fixture (4096 B, sha256 `c7f74691…`) |
| `stdbe-control.squashfs` | lane-built standard-BE control (812 B, sha256 `5b7dcfe3…`) |
| `avm-fixture-probe.py`, `avm-fixture-probe.txt` | stdlib S1/S2/S3 probe and its output (exit 0) |
| `unblob-handler-probe.py`, `unblob-handler-probe.txt` | unblob’s own handler on the fixture: chunk `0x0-0x1000`, `is_avm=True`, no `-be` |
| `sasquatch-avm-test.txt` | the three sasquatch runs on the fixture, exits 0/1/1, file lists and contents |
| `sasquatch-standardbe-control.txt` | the two sasquatch runs on the standard-BE control, exits 1/0 |
| `rea-argv-evidence.txt` | K1 success receipt (no `sasquatch`/`-be` anywhere) vs H13/H15 failure commands; round-11 log lines |
| `source-anchors.txt` | every quoted file:line with file hashes (unblob handler, sasquatch tree, REA, Freetz) |
| `sources-row-draft.md` | S121 overlap finding + draft companion row |
| `fixture-provenance.txt` | fixture/control provenance and build commands |

## Evidence (commands, exit codes)

```
# 1. stdlib probe (S1/S2/S3)
python3 avm-fixture-probe.py /fast/scratch/hyaku/kaidoku-r40/R40C1Revenger/fx/avm-be.squashfs   # exit 0
# 2. unblob handler as a library (no extraction)
/home/vgpnk/.local/share/uv/tools/unblob/bin/python unblob-handler-probe.py <fixture>            # exit 0
#    -> magic-endian=Endian.BIG ; chunk=0x0-0x1000 ; is_avm=True ; argv_tail=[] (no -be)
# 3. direct sasquatch on the fixture (cwd=scratch, fresh -d dirs)
~/.local/bin/sasquatch-v4be        -d out1 avm-be.squashfs   # exit 0, 4 files
~/.local/bin/sasquatch-v4be -be    -d out2 avm-be.squashfs   # exit 1, 0 files
~/.local/bin/sasquatch             -d out3 avm-be.squashfs   # exit 1, 0 files
# 4. standard-BE control
python3 tools/round-39/gen-squashfs.py tree stdbe.squashfs --endian be --comp gzip  # exit 0, 812 B
~/.local/bin/sasquatch-v4be        -d o1 stdbe.squashfs      # exit 1, 0 files
~/.local/bin/sasquatch-v4be -be    -d o2 stdbe.squashfs      # exit 0, bin/run + docs/data.txt
# 5. receipts (read-only JSON)
python3 (walk raw_result of corpus/evidence/round-39/c1/K1/after.json and c2/heldout/H13,H15)
# 6. source fetches (scratch; hashes in source-anchors.txt)
curl -fsSL https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/squashfs-tools/<file>
curl -fsSL https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/debian/rules
curl -fsSL https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt
```

Scratch `/fast/scratch/hyaku/kaidoku-r40/R40C1Revenger` was created under `HYAKU_SCRATCH` and is
removed before this seat finishes; every cited byte is either copied into the artifacts directory
or pinned by sha256 plus the command that rebuilds it.

Report: .ufo/waves/round-40/w1/R40C1Revenger.md
