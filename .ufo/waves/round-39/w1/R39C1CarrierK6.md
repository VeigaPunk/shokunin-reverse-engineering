DONE — K6 carrier built, deterministic, and dev-checked with `sasquatch-v4be` only; one material recon finding on the generator's compression id.

# R39-C1 carrier K6 — standard big-endian SquashFS v4 (`--comp xz`)

Seat `R39C1CarrierK6`, wave 1 (pre-freeze). Base `a2f64e1da78afcf8cc39287106604dbcc270844c`.
Nothing here is integrated; the L1 owns the commit. No VCS mutation, no REA/unblob run on this carrier.

## 1. Deliverables

Directory: `.ufo/waves/round-39/w1/artifacts/R39C1CarrierK6/`

| file | bytes | sha256 |
|---|---|---|
| `carrier.sqsh` | 14925 | `df85c10bde923bd6fcd3f4c1be21664215077866b8fdf33fc4871dd1df344f61` |
| `oracle.tsv` | 587 | `13493bc4ba95190e7f078efd917e6173c3d2284f80279fdb618c245dfdf2428e` |
| `symlinks.tsv` | 118 | `e0a0a72f727218b2f8328daf72fcdef5b3923b6b7fb0574b0ab4cd79872f9a74` |
| `build.sh` | 6738 | `669baf9c9308cc82e4049a2041f2e66c9fd89edc185285a8b7986537cc05b69d` |
| `dev-check.sh` | 1808 | `338ed14b53f87a7795d49221ff447baa6eb352b479bec57b856f0f83d3cf9473` |
| `sha256` | 79 | — (holds `df85c1…  carrier.sqsh`) |
| `src/` | 10 dirs, 7 files, 3 symlinks | tree is the oracle's source of truth |
| `determinism.txt` | 361 | `db40320c79ddf0ff9d76cac770ea0dddf3d5c28286205792d92cb70cf9e37c02` |
| `probe-dirlink.txt` | 951 | `eb9f78aace6181fa27b46db4b0400ba347b95fcb86e5357d5057ffbc14d21d58` |
| `listing-lls.txt` | 1863 | `712717d61ad24e210cc7429a53868a489d3b92134b948257380d12de05548c44` |
| `superblock.txt` | 1528 | `b38ad7e943945d5efedeff1f06643997f357300347280f200713b253ed6cd3ba` |
| `extract-exact.log` | 562 | `8c61d1f807e71ad15925dea26a6f85013f31194ba404d7a2faf678ca977009cc` |
| `dev-check.log` | 2940 | `7959aa165739bd9463469dab6425f12e2e3fcb8dc143526dd18d80f21df6c3f7` |

Suggested `carriers.json` row (freeze-time pin):

```json
{"id": "K6", "kind": "synthetic standard-BE v4, compression id 2 measured in the superblock (LZMA-declared; body is a raw LZMA2 stream; built with gen-squashfs.py --comp xz), 7 files + 1 in-tree / 2 escaping symlinks", "path": "corpus/evidence/round-39/c1/K6/carrier.sqsh", "oracle": "corpus/evidence/round-39/c1/K6/oracle.tsv", "symlinks": "corpus/evidence/round-39/c1/K6/symlinks.tsv", "sha256": "df85c10bde923bd6fcd3f4c1be21664215077866b8fdf33fc4871dd1df344f61"}
```

`build.sh` is the whole provenance: it authors `src/` deterministically, derives `oracle.tsv` +
`symlinks.tsv` from that tree, calls the round-37 generator, and then asserts (by re-extracting the
built image with `sasquatch-v4be`) that the image's inventory matches the tables — it exits non-zero
on any dropped, added or altered entry. It needs `sasquatch-v4be` on `PATH` (`~/.local/bin`).
`dev-check.sh` independently re-verifies a carrier against those two tables with `sasquatch-v4be`
and nothing else.

## 2. Tree (new, differs from K1/K2)

```
src/
  a/b/note.txt                 22 B  "note: two levels down\n"
  a/b/link-in -> ../../etc/config.ini      in-tree
  bin/tool.sh                  23 B  tiny text
  data/blob.bin             13579 B  random, seed 39 (4 blocks)
  data/manifest.txt            15 B
  data/escape-deep -> ../../../../etc/passwd   escaping
  docs/deep/notes.txt          11 B
  etc/config.ini               50 B
  var/log/app.log              19 B
  outside -> ../outside                    escaping
```

Requirement-by-requirement (all from the assignment):

| requirement | K6 |
|---|---|
| 2+ directory levels | `a/b`, `docs/deep`, `var/log` — three two-level chains |
| ≥6 regular files | 7 (`a/b/note.txt`, `bin/tool.sh`, `data/blob.bin`, `data/manifest.txt`, `docs/deep/notes.txt`, `etc/config.ini`, `var/log/app.log`) |
| one > 2 blocks, random, fixed seed | `data/blob.bin` = 13579 B = 3×4096 + 1291 → **4** blocks; `random.Random(39).getrandbits(8)`; superblock `fragments = 0`, so all four are real data blocks |
| one tiny text file | `bin/tool.sh` 23 B (`docs/deep/notes.txt` 11 B is a second) |
| exactly ONE in-tree relative symlink, two dirs up and back down | `a/b/link-in -> ../../etc/config.ini` (POSIX resolve from `a/b`: `../../` → root, then `etc/config.ini`) |
| exactly TWO escaping relative symlinks | `outside -> ../outside` (one up from the image root) and `data/escape-deep -> ../../../../etc/passwd` (four up) |
| no absolute symlinks | 0; every target is relative |
| no hardlinks, devices, empty dirs | sasquatch reports `created 0 devices / 0 fifos / 0 sockets / 0 hardlinks`; all 10 directories are non-empty |

`oracle.tsv` (7 rows, `path TAB sha256 TAB size`, sorted — same format as
`corpus/evidence/round-37/c1/K2/oracle.tsv`):

```
a/b/note.txt	393f3259b68273073ef72f4e3d4f938ea91d89365278b5204e040d14b232a149	22
bin/tool.sh	9803ccbb2b9bb8836d78a22c729e169f285016cc019fc963670d353f96c9757e	23
data/blob.bin	482bc9e5829ad29f44d85693c988418322b090b7b717a72c86717b59f85c3c87	13579
data/manifest.txt	70b0818ec4718413f1ae5c7bee3c13e88e5662c04fe08347ebf7da0a3d6569f4	15
docs/deep/notes.txt	cca3c227b0b1e2589ae86aa7501162e4878b01162cca43557e248d822611d1ff	11
etc/config.ini	2b3b04fb08c4a126d4fd5e5dbd7d81b026ffffe1864ef18ea2c0b6af8da10b0f	50
var/log/app.log	445484dc8c55c6b147e935708840d1769c945a4f43913baf1f9713a6b9687d88	19
```

`symlinks.tsv` (`path TAB target TAB class`):

```
a/b/link-in	../../etc/config.ini	in-tree
data/escape-deep	../../../../etc/passwd	escaping
outside	../outside	escaping
```

Expected gap accounting for P39-C1 on K6: **7** published regular files, **1** extraction gap of
kind `unpublished-entry` at suffix `a/b/link-in`, **0** published paths for `outside` /
`data/escape-deep`. K6 exercises in one carrier what round-38 split across K1 (escaping
`link-to-hello -> ../hello.txt`) and K2 (in-tree `var/lib/run-link -> ../../a/run.sh`).

## 3. Build and determinism

```
build.sh
  python3 - "$TREE" "$here/oracle.tsv" "$here/symlinks.tsv"     # author tree + derive tables
  python3 tools/round-37/gen-squashfs.py "$TREE" "$OUT" --endian be --comp xz
  python3 - "$OUT" "$here/oracle.tsv" "$here/symlinks.tsv"      # image-truth assertion
```
Generator output: `wrote …/carrier.sqsh 14925 bytes, inodes 20`; then, from the build itself:

```
image truth: 7 regular files, 3 symlinks match the tables
```

The third step re-extracts the freshly built image with `sasquatch-v4be -be -no-exit-code -f -d`
and fails the build if the extracted inventory (regular files with sha256+size, symlink targets,
and any non-regular entry) differs from the two tables. Reason: `gen-squashfs.py` only sees what
`os.walk` yields, so an entry it never yields is dropped **silently** — reproduced below in §5.6.
The tables stay derived from the tree (an independent statement of intent), so this assert is a
real cross-check in both directions: a dropped entry fails the build, and the image cannot
"explain away" a table row. Build step 2 is sasquatch only — REA/unblob are never invoked.

Three-way byte equality (`determinism.txt` rows verbatim):

```
build 1 (default, guarded): df85c10bde923bd6fcd3f4c1be21664215077866b8fdf33fc4871dd1df344f61  carrier.sqsh
build 2 (independent scratch tree, guarded): df85c10bde923bd6fcd3f4c1be21664215077866b8fdf33fc4871dd1df344f61  carrier.sqsh
rebuild from committed src/ (unguarded generator): df85c10bde923bd6fcd3f4c1be21664215077866b8fdf33fc4871dd1df344f61  carrier.sqsh
```

Build 2 authored its tree in scratch (`/fast/scratch/hyaku/kaidoku-r39/R39C1CarrierK6/src2`); the
third run regenerated from the shipped `src/` alone, which is what pins the oracle to the image.
`find . -printf '%y %p %l %s'` manifests of `src/` and the second-authoring tree are identical for
every file, link and link target (directory `st_size` differs only because it is a host-FS
artifact).

## 4. Dev checks — `sasquatch-v4be` only (no REA, no unblob)

Versions: `sasquatch-v4be` `unsquashfs version 4.5.1 (2022/03/17)`, Python 3.14.8,
`mksquashfs 4.7.5` (reference only, `/usr/bin`). No installs or upgrades were needed.

**(a) Listing** — `sasquatch-v4be -be -lls carrier.sqsh` → exit 0, first line
`Reading a different endian SQUASHFS filesystem on …/carrier.sqsh`, then all 10 dirs, 7 files and
3 symlinks with exact sizes and targets (full text in `listing-lls.txt`).

**(b) Extraction with the *exact* argument vector unblob's extractor builds** (see §5.3) —
`sasquatch-v4be -be -no-exit-code -f -d <out> carrier.sqsh` → exit 0, stdout:

```
Parallel unsquashfs: Using 1 processor
10 inodes (10 blocks) to write
created 7 files
created 10 directories
created 3 symlinks
created 0 devices
created 0 fifos
created 0 sockets
created 0 hardlinks
```

**(c) Oracle verification** against that extraction: 7/7 regular files match sha256+size, 3/3
symlink targets match (`bad = 0`). `dev-check.sh` reproduces (a)+(b)+(c) in one run → exit 0
(`dev-check.log`).

`--comp xz` **does** extract cleanly with `sasquatch-v4be`; no fallback to gzip was taken or needed.

**(d) Superblock** (`superblock.txt`) — `-stat`: `Found a valid SQUASHFS 4:0 superblock`,
`Filesystem size 14925 bytes`, `Block size 4096`, `Number of inodes 20`, `Number of ids 1`,
`Number of fragments 0`, `Compression lzma`; `file(1)`: `Squashfs filesystem, big endian,
version 4.0, lzma compressed, 14925 bytes, 20 inodes, blocksize: 4096 bytes`. Header bytes:

| off | field | K6 |
|---|---|---|
| `0x00` | magic | `73 71 73 68` (`sqsh`, BE) |
| `0x04` | inodes | 20 |
| `0x08` | mkfs_time | 1700000000 (`0x6553F100`) |
| `0x0c` | block_size | 4096 |
| `0x10` | fragments | 0 |
| `0x14` | compression | **2** |
| `0x16` | block_log | 12 |
| `0x18`/`0x1a` | flags / no_ids | 0 / 1 |
| `0x1c`/`0x1e` | major / minor | 4 / 0 |
| `0x20` | root_inode | 676 |
| `0x28` | bytes_used | 14925 (= file size) |
| `0x30` | id_table_start | 14917 |
| `0x38` | xattr_id_table_start | `0xFFFF…` |
| `0x40` | inode_table_start | 13815 |
| `0x48` | dir_table_start | 14525 |
| `0x50`/`0x58` | fragment / lookup table | `0xFFFF…` |

## 5. Recon that the freeze should carry

### 5.1 FINDING — the generator's `--comp xz` writes superblock compression id **2**, not 4

`gen-squashfs.py` has `COMP = {'gzip': 1, 'xz': 2}` and compresses with
`lzma.FORMAT_RAW` + `FILTER_LZMA2` (`dict_size=block_size`). On disk that is **compression id 2**,
which SquashFS v4 reserves for LZMA; **XZ is id 4**. Evidence:

| image | `xxd -s 20 -l 2` | `file(1)` |
|---|---|---|
| K6 (`gen-squashfs.py --comp xz`) | `0002` | `lzma compressed` |
| `mksquashfs -comp xz` reference | `0400` (LE) | `xz compressed` |
| `mksquashfs -comp lzma` reference | `0200` (LE) | `lzma compressed` |
| `mksquashfs -comp gzip` reference | `0100` (LE) | `zlib compressed` |

References were built in scratch from a one-file tree
(`mksquashfs ref/tiny ref/xz.sqsh -comp xz -noappend -all-root -mkfs-time 0 -all-time 0 -no-xattrs -processors 1`) purely to read the id byte; they are not carriers.

Consequence: K6 is a standard big-endian v4 image whose **body** is a raw LZMA2 stream labelled
LZMA (id 2), not byte-level XZ. `sasquatch-v4be` decodes it (proof in §4), because id 2 selects
its lzma path. Three things follow for the freeze wording:

1. The carrier `kind` string must not claim "xz id 4" (§1 row now reads `compression id 2
   measured in the superblock (LZMA-declared; body is a raw LZMA2 stream; built with
   gen-squashfs.py --comp xz)`). Claiming plain "standard xz" would be a citation the bytes do not
   support.
2. **Record the measured field, not the typed flag.** `.ufo/waves/round-39/c1/carriers.json`
   should carry the measured superblock value in `kind` — "compression id 2 (LZMA-declared; body
   is a raw LZMA2 stream)" — not "xz", because a reviewer reading "xz" expects id 4 and a real
   `mksquashfs -comp xz` image. If the counter ever binds on compression, the honest binding is
   **`compression != 1`** (id 1 = gzip is what K1–K4 carry), explicitly not `== 2 (xz)`.
3. If K5 is built with the same generator and the same flag, K5 has the same id 2. Both carriers
   stay consistent; but if the L1 wants a real id-4 carrier, that is a **generator change**
   (`COMP['xz'] = 4` and an XZ container format), which is out of this seat's write bounds and
   would also have to be an independent oracle concern. Recorded as a decision for the L1, not a
   blocker: the predicate names the handler, not the compression id.

Independent cross-check: `R39C1AxisFit` measured the same carrier separately
(`.ufo/waves/round-39/w1/artifacts/R39C1AxisFit/superblock-compression.txt`) — 14925 B, magic
`sqsh`, block_size 4096, **compression 2**, s_major 4 / s_minor 0, bytes_used 14925 = file size —
and separately established that K1–K4 are all id 1. Two independent readers agree on every field,
so the id-2 finding is not an artifact of one parser.

[INFERENCE] A real mksquashfs xz image would be id 4, and unblob's handler pattern does not read
the compression field (§5.2), so id 2 does not gate detection; extraction is delegated wholesale to
`sasquatch-v4be`, which succeeded here with the identical argv.

### 5.2 Handler pattern matches (detection is magic-only)

unblob 26.6.4 `handlers/filesystem/squashfs.py`, `SquashFSv4BEHandler.PATTERNS`:
`73 71 73 68 [24] 00 04` (`squashfs_v4_magic_be`). K6 bytes `0x00-0x03` = `sqsh`, `0x1c-0x1d` =
`00 04` → match. The pattern carries no compression or mkfs_time constraint, so nothing in K6's
header can push it to another handler. `squashfs_v4_le` needs `hsqs`, `squashfs_v4_broadcom` needs
`qshs`, v1/v2/v3 need other versions → [INFERENCE] `squashfs_v4_be` is the only candidate handler.

### 5.3 The AVM discriminator does not fire on K6

`SquashFSExtractor.extract` (same file, lines 28-59) picks the argv:

```
endian BIG, version 4: executable = sasquatch-v4be
                       is_avm = header.bytes_used == header.mkfs_time
                       if not is_avm: append "-be"
then: ["-no-exit-code", "-f", "-d", "{outdir}", "{inpath}"]
```

K6: `bytes_used = 14925` vs `mkfs_time = 1700000000` → not equal → `-be` appended. That is the
exact vector exercised in §4(b). This is the structural difference from the round-38 AVM probe
(`.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/rea-k1-avm.json`, where the generator writes
`mkfs = bytes_used`): K6 cannot be classified AVM, so it is a clean standard-BE sample for C1,
and it keeps K6 out of the `avm-marker-be-dropped` class that R39-C2 will build separately.

[INFERENCE] Because the chunk is computed from `bytes_used`, and K6's file is exactly 14925 bytes
with no 4 KiB/1 KiB zero pad (`calculate_chunk` reads past EOF, gets `b""`, so neither pad branch
matches), the valid chunk is `[0, 14925)` — the whole image, no truncation, no failed chunk.

### 5.4 Incompressible data blocks are stored raw (generator fallback)

For each 4096-byte block the generator stores the LZMA2 stream only if it is shorter than the
input (`raw = len(c) >= len(chunk)`). `data/blob.bin` is random, so all four of its blocks are
stored uncompressed with the `0x01000000` size flag; the text blocks and the metadata blocks are
the compressed ones. That is what mksquashfs does to incompressible input too, so it is expected
behaviour rather than a defect — but it means K6's compressed surface is metadata + 6 small text
files, not the 13 KiB blob.

### 5.5 Generator scope notes (unchanged from round 37/38, relevant to the oracle)

No fragments (`fragments = 0`, fragment table `0xFFFF…`), no export/lookup table, no xattrs, one
id (1000). Consequence for the predicate: every regular file must appear as a full data-block
sequence, so a "same sha256" match cannot be satisfied by a fragment-table accident.

### 5.6 REPRODUCED — a symlink whose target is a directory is dropped silently

Independent reproduction of `R39C1AxisFit`'s build hazard on this generator (probe in
`probe-dirlink.txt`, tree `a/f.txt` 2 B + `dirlink -> a` + `flink -> a/f.txt`):

```
wrote p.sqsh 306 bytes, inodes 4
tree:  d ./a   f ./a/f.txt   l ./dirlink a   l ./flink a/f.txt
image: squashfs-root   squashfs-root/a   squashfs-root/a/f.txt   squashfs-root/flink -> a/f.txt
```

`dirlink` is absent from the image: `os.walk(..., followlinks=False)` yields a symlink-to-directory
in `dnames`, the generator only inspects `fnames`, and the `islink` branch never sees it. The
inode count (4 = two dirs, one file, one symlink) confirms it was never written.

Applied to K6: **every K6 symlink targets a file or a non-existent path, never a directory**
(`a/b/link-in -> ../../etc/config.ini` = file; `outside -> ../outside` and
`data/escape-deep -> ../../../../etc/passwd` = non-existent). All three are present in the built
image — asserted at build time by §3's image-truth step and visible in `listing-lls.txt`. The same
hazard class is now impossible to ship unnoticed from `build.sh`.

Cross-check with the other points raised by `R39C1AxisFit`:

- *Absolute targets* — K6 has **none**: all three targets are relative, so no unblob re-rooting
  (`/etc/passwd` → `etc/passwd`, one gap) can occur. The two escaping links are relative and
  therefore removed as `MaliciousSymlinkRemoved` with no gap, matching the claim's rule.
- *Oracle derivation* — the tables are tree-derived (independent of the image) **and** the build
  asserts the image reproduces them exactly (file sha256+size, link target, link count, no extra
  non-regular entry); `dev-check.sh` repeats the check against the extraction. Deriving the tables
  from the image alone would be weaker: it could not detect a silently dropped entry.
- *Cardinality per link* — K6 has 1 in-tree link → exactly 1 `unpublished-entry` gap, and 2
  escaping links → 0 gaps, 0 published paths.
- *xz on BE is new ground* — confirmed extracted exactly once, with the unblob argv, §4(b).

### 5.7 Symlink removal requires a RELATIVE target; K6 has no absolute target

Measured on unblob 26.6.4 by `R39C2Triage`
(`.ufo/waves/round-39/w1/R39C2Triage.md` §5.3-5.5, `extractor.py:66-79`): an **absolute** target is
never escaping — the leading `/` is stripped and only the relative remainder is checked, so
`/etc/passwd` is *kept* as metadata and yields an `unpublished-entry` gap with no
`MaliciousSymlinkRemoved`. Removal needs a **relative** target that resolves above the image root
(`../../outside/secret`, `a/b/climb-link -> ../../../hello.txt`).

K6 is compliant by construction and needs no rebuild:

| K6 link | target kind | POSIX resolve from the link's dir | class |
|---|---|---|---|
| `a/b/link-in` | relative | `a/b/../../etc/config.ini` → `etc/config.ini` | in-tree → 1 gap |
| `outside` | relative | `../outside` → above root | escaping → removed, 0 gaps |
| `data/escape-deep` | relative | `data/../../../../etc/passwd` → `../../../etc/passwd` | escaping → removed, 0 gaps |

There are **zero absolute targets** in K6 (`symlinks.tsv` row 2 column 2 never starts with `/`;
`build.sh` asserts that), so the absolute-target rewrite hazard — an envelope's
`unpublished_entries[].link_target` reporting the rewritten target (`/etc/passwd` → `etc/passwd`),
which would make a raw-text oracle comparison disagree — cannot apply to this carrier. The only
comparable path is the in-tree link, whose target text is unmodified in the envelope.

## 6. Risks / limits

- **R1 (material, wording).** Compression id 2 vs 4 (§5.1). Freeze wording must say
  "generator `--comp xz`, id 2 / raw LZMA2", or the claim overstates "standard xz".
- **R2 (by design).** K6 has never been through REA/unblob, per the held-out discipline. The
  `squashfs_v4_be`-handler and gap expectations in §2 are `[INFERENCE]` from handler source plus
  the direct `sasquatch-v4be` run; they are not observed REA output and must not be recorded as if
  they were. If the after-run disagrees on the gap count, the id-2 body or the symlink rule is the
  first thing to look at.
- **R3 (low, now measured).** `outside -> ../outside` has a target that does not exist on the
  host; it escapes *by relative path* (`../` from the image root), which is exactly the shape
  `R39C2Triage` measured as removed (`../../outside/secret`, `a/b/climb-link -> ../../../hello.txt`).
  The claim's rule ("resolved POSIX-style against the link's own directory inside the image root")
  and unblob's measured behaviour agree for both K6 escaping links, so the expected count is 2
  removals, 0 gaps. The hazard the measurement does expose is the opposite one: an *absolute*
  target would be kept — K6 has none (§5.7).
- **R4 (low, informational).** `data/escape-deep` points at a host-critical path string
  (`/etc/passwd` after four `../`). It is never dereferenced by anything in this seat, and
  `sasquatch-v4be` extracted it as a literal link. Any after-run consumer must not follow it.
- No blockers.

## 7. Bounds compliance

- Wrote only `.ufo/waves/round-39/w1/artifacts/R39C1CarrierK6/**` and this report. No writes to
  `corpus/`, `tools/`, `plans/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `LOG.md`,
  the fleet repo, sibling lanes, or `shokuknow`.
- No `git`/`jj` invocation at all (no fixture was needed).
- `REA`, `npx`, `unblob` never invoked — dev check was `sasquatch-v4be` extract + `-lls` only, as
  instructed; `build.sh`'s image-truth step also uses `sasquatch-v4be` only. `mksquashfs` was used
  once in scratch, read-only w.r.t. the lane, to read reference compression-id bytes (§5.1); the
  `probe-dirlink.txt` probe used the generator on a scratch-only tree.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r39/R39C1CarrierK6` (trees, second build, reference
  images, extraction dirs). Evidence cited in this report lives in the artifacts dir, not in
  scratch; scratch is removed before yielding.
- No tool installs or upgrades; no pacman transaction.
- No subagents, no background jobs, no `agent://all`.

## 8. What the L1 still has to do

1. Commit `carrier.sqsh`, `src/`, `oracle.tsv`, `symlinks.tsv`, `build.sh`, `sha256` at
   `corpus/evidence/round-39/c1/K6/` and pin `df85c10b…` in `.ufo/waves/round-39/c1/carriers.json`
   (K5 alongside, from its own seat).
2. Decide the `kind` wording for id 2 (§5.1, R1) — and whether K5 was built the same way.
3. Ensure K6 reaches REA for the first time in the after-run, with `sasquatch-v4be` on the child
   PATH, and reconcile the result against §2's expected gap count (7 files / 1 `unpublished-entry`
   at `a/b/link-in` / 0 escaping paths).
