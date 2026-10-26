# R40C1AvmWriter — genuine AVM-layout SquashFS writer (round-40 wave 1)

**Verdict: DONE** — `gen-squashfs.py --endian avm-genuine` emits the genuine AVM layout
(BE superblock/inode/directory/data-size/fragment/lookup fields, **LE 2-byte metadata
block-length headers**, `mkfs_time == bytes_used`); `sasquatch-v4be` (no `-be`) extracts
every file with equal sha256 on 5 fresh trees × gzip/xz, `-be` fails, the round-39 reader
refuses it, `be`/`le`/`avm` stay byte-identical to the round-39 writer on single-block
trees, and unblob 26.6.4 selects `squashfs_v4_be` with a no-`-be` argv on two throwaway
dev images. Three latent round-39/37 writer defects surfaced and were fixed (advisory
below — they matter if the freeze builds a larger carrier tree).

Seat: leaf. Lane corpus/tools/plans untouched; writes only to
`.ufo/waves/round-40/w1/R40C1AvmWriter.md` and
`.ufo/waves/round-40/w1/artifacts/R40C1AvmWriter/`. Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40C1AvmWriter` removed at exit; no `git` mutation; no
tool installed (all tools needed were already pinned); **no REA call at all**; unblob was
run on exactly two throwaway dev images (log + argv retained); no unblob/REA run and no
sasquatch run on any C1 carrier (the V1 members were read pure-Python only).

## Axes (Godspeed)

| axis | move |
|---|---|
| **coverage** | the AVM layout gets a producer, so R40-C1's lane-built carriers (L1 gzip / L2 xz) can exist at all; the layout's field classes are now measured, not quoted, on two retained genuine images. |
| **depth** | the discriminating rule is executable: `diff-be-vs-avmgenuine.py` proves the mode differs from `--endian be` **only** in `mkfs_time` and the metadata headers, and the extractor matrix separates the two. |
| **calibration** | three round-39/37 writer defects (multi-block refs, record straddling, directory symlinks) were measured; the claims' "byte-identical to the round-39 writer" requirement is met on the trees that matter and the divergence is documented and tested. |

## What was delivered

`artifacts/R40C1AvmWriter/gen-squashfs.py` (sha256 `309c502d…042e`) — round-40 writer.

```
python3 gen-squashfs.py TREE OUT --endian le|be|avm|avm-genuine --comp gzip|xz
python3 gen-squashfs.py --selftest [--ref-writer PATH] [--sasquatch PATH] [--keep]
```

- `avm-genuine`: `sqsh` magic; superblock, inode, directory, data-block-size, fragment-entry
  and lookup-table fields exactly as `--endian be`; **every** 2-byte metadata block-length
  header little-endian; `mkfs_time = bytes_used`.
- `le` / `be` / `avm` unchanged in semantics; byte-identical to
  `tools/round-39/gen-squashfs.py` for tables that fit one metadata block (proof below).
- `--selftest`: 71 checks, exit 0. Categories: `layout` ×10, `extract` ×10, `-be-fails`
  ×10, `deterministic` ×10, `reader39-misreads` ×10, `byte-identical` ×18,
  `round39-ref-multiblock-broken`, `round39-ref-drops-dir-symlink`, `std-be-needs--be`.
  It builds its own trees under `TMPDIR` and needs only `sasquatch-v4be`.

Companions in the artifact directory: `make-dev-images.py` (rebuilds the 10 dev images +
`manifest.tsv` + `tree-files.tsv`), `diff-be-vs-avmgenuine.py` (structural diff proof),
`probe-v1-member.py` (pure-Python layout probe used for the measurements below).

## The genuine AVM layout, measured (not quoted)

Probe transcripts: `probe-v1-be.txt` (V1 BE member), `probe-round11-avm-be.txt` (lane
fixture). Tool pins: `unblob 26.6.4` (handler `2d7b901b…9287`, re-hashed),
`sasquatch-v4be 4.5.1`, `python3 3.14.8`. Image provenance: `genuine-images.txt`.

| field class | endianness | witness |
|---|---|---|
| superblock | BE | V1 BE: inodes 1079, mkfs_time 5442392 **==** bytes_used 5442392 (marker), block_size 65536, comp 4 (xz), inode_table 5421468, dir_table 5430042; every LE decode is nonsense |
| inode fields | BE | V1 BE: root/reg/dir inodes parse; 697 reg + 263 symlink + 118 dir + 1 char dev = **1079 = superblock inode count** |
| directory header + entries | BE | V1 BE: header `start_block` values are inode-table byte offsets and the whole tree walks; fixture: count 3, start 0, inode 1, four `appleN.txt`, type 2, name_size 9, offsets 0/32/64/96 |
| data-block size list | BE | V1 `usr/sbin/dispatcher`: `00005268 00005054 00000e90` = 21096/20564/3728 B (BE) vs 5.2/5.2/0.9 MiB (LE, impossible) |
| fragment entry `{u64,u32,u32}` | BE | fixture: start 96, size `0x01000019` = 25 B with the `1<<24` stored-uncompressed bit; V1: start 0x60, size 0x3be4 |
| fragment / export / id index u64s | BE | fixture 343→325 and 357→351; V1 fragment 5440850→5440192, export 5442362→5440858, id 5442384→5442378 (only the BE reading is a plausible block offset) |
| **2-byte metadata block-length header** | **LE** | fixture inode `7400`→116 (BE 29696), dir `5480`→84 stored (BE 21632); V1 inode `6405`→1380 (BE 25605), dir `900c`→3216, fragment block `9002`→656, export block `3405`→1332, id block `0480`→4 stored |

Behavioural cross-check on the lane fixture (not a carrier):
`sasquatch-v4be -f -d OUT avm-be.squashfs` → exit 0, 4/4 files, sha256s equal;
`sasquatch-v4be -be -f -d OUT …` → exit 1 `read_id_table: failed to read id table block`,
`FATAL ERROR: File system corruption detected`, 0 files.

## Validation matrix (exact evidence)

All runs `cd "$S"` with `TMPDIR="$S"`, `python3 -I -B`. Full log: `selftest.log`.

1. **Five fresh trees × gzip/xz extract under `sasquatch-v4be` (no `-be`).**
   `extract[small/gzip]: exit=0 files=5/5 links=0/0 missing=[] bad_links=[]` (all 10 cells
   PASS; trees: `small`, `multiblock` 20 000 B multi-block file, `many` 61 files + UTF-8
   name, `bulk` 400 files crossing metadata blocks, `links` 4 symlink kinds).
   Standalone images + per-image sha256: `manifest.tsv` (all `marker=True`,
   `le_walk_lands=True`, `be_walk_lands=False`, `extract_ok=True`, `sasquatch_exit=0`).
2. **`-be` fails.** `-be-fails[small/gzip]: exit=1 files=0 first_err=FATAL ERROR: File
   system corruption detected` (all 10 cells PASS).
3. **Determinism.** Build twice → same sha256 (`deterministic[*]` 10/10). Cross-process:
   selftest and `make-dev-images.py` (separate processes) produce the same
   `small-gzip` sha256 `bfc446ff…dc2e`.
4. **Round-39 reader (BE mode) refuses.** `reader39-misreads[small/gzip]: exit=2
   first_err=sqfs-list: metadata body out of bounds: offset 7154 length 21633, image …`
   (10/10; it decodes the header big-endian and chases a 21633-byte block).
5. **`be`/`le`/`avm` byte-identity** with `tools/round-39/gen-squashfs.py`, 3 trees × 3
   modes × 2 compressions = 18 sha256-equal pairs, e.g.
   `byte-identical[small/be/gzip]: 425946cc…a707`, `[small/le/gzip]: 53f9c99d…ad3`,
   `[small/avm/gzip]: 33ebb667…b050`; `multiblock` `94e62cde…619e` (be/gzip),
   `2078f1eb…fbbc` (le/gzip), `19e52d98…df8a` (avm/gzip); `many` `22578875…7132`,
   `e0d71fe1…506c`, `fa4a6238…49d8`. `avm` remains the marker-only standard-BE transform.
6. **`avm-genuine` differs from `be` only where the claim says.**
   `diff-be-vs-avmgenuine.log`: for all 5 trees,
   `set(differing bytes) == {8,9,10,11} ∪ {2-byte header positions}` —
   `PASS small: differing 10, outside header/mkfs set 0, mkfs be=1700000000 avm=7690
   bytes_used=7690` (same for `multiblock`, `many`, `links`; `bulk`: differing 12 with 4
   headers). Superblock is identical except those 4 bytes; every header flips
   `8154→5481`, `80b4→b480` etc. with the decoded length unchanged.
7. **unblob 26.6.4 (two throwaway dev images only).**
   `unblob-dev1.log`: `Found valid chunk handler=squashfs_v4_be`,
   `Running extract command command='sasquatch-v4be -no-exit-code -f -d …/dev1.sqsh_extract
   …/dev1.sqsh'` (no `-be`), exit 0, 5/5 files sha256-equal; dev2 identical (chunk
   `0x0-0x6577`, 3/3 files). `dev1.sqsh` / `dev2.sqsh` are byte-identical copies of
   `small-gzip-avm-genuine.sqsh` (`bfc446ff…`) and `multiblock-xz-avm-genuine.sqsh`
   (`25dba8cc…`), recorded in `unblob-dev-provenance.txt`.
8. **Standard BE needs `-be` (negative control).** `std-be-needs--be: exit=1` — a
   `--endian be` image read with the AVM argv fails, so the AVM mode is not merely "BE with
   a marker".

### Dev images (artifacts, rebuildable)

`python3 make-dev-images.py --work "$S/dev" --out .` → `manifest.tsv`.
All ten images: `mode=avm-genuine`, `marker=True`, `bytes_used==mkfs_time`,
`sasquatch_exit=0`, `extract_ok=True`, `le_walk_end==dir_table`,
`be_walk_end!=dir_table`.

| image | B | sha256 |
|---|---|---|
| small-gzip | 7690 | `bfc446ffec3fe737d0db41b3a883c34a17afa30f67ba9b4320383f18dfd9dc2e` |
| small-xz | 7751 | `68c44a3b6a1a1f06d43a3991000b8ec184af02057da54edfb89e300d7424f9ae` |
| multiblock-gzip | 25652 | `5d78962013abff8c1e7339b93f8334fe6fcfd124db4f2c0652ae5c702e8e5f25` |
| multiblock-xz | 25975 | `25dba8ccb8ab84d25e3084b824afecc0d6e66a5df9b2a44a0ee900525dacb3e4` |
| many-gzip | 5056 | `f61a341bb9e781196577c668234f0adcccce3926b88e1da534a834189f2ead7b` |
| many-xz | 5533 | `d4aa820a5d776a47cdd1025c418a29a6c0f36bb77cb60af96456c4275510dee9` |
| bulk-gzip | 22788 | `0543e2df2552071241385486974af3a3d695a45d83bc32f43a21d0b6f7f13c78` |
| bulk-xz | 22788 | `072ecf277051c0c97eb7721d50eeebc1d5dafad3fdc2e312972f89f2c8a42e4e` |
| links-gzip | 599 | `31fc23962b99d398b9acbceb72b62ebc598104e85fdcc932a473eb56af311443` |
| links-xz | 599 | `14253fef984d2c7c10d02eb56fcd73640fb05f99feb80d3c38f9508f5c8ed822` |

Note `links` stores four symlink kinds (in-tree file, escaping `../../etc/passwd`,
absolute `/etc/shadow`, and a symlink to a directory); the C1 carriers do not need
symlinks for the file-sha256 predicate, but mixed symlinks are C2's ground.

## Findings for the freeze (advisory; routed defects candidate)

1. **`gen-squashfs.py --endian avm` (rounds 37–39) is marker-only.** Unchanged and
   re-verified: `avm` output stays byte-identical to the round-39 writer (proof 5 above);
   it must not be used for a C1 carrier. `avm-genuine` is the AVM layout.
2. **Round-39/37 writer breaks on multi-block metadata tables** — two independent bugs:
   (a) inode/directory references stored the *block index* instead of the table-relative
   *byte offset* the format requires; (b) a metadata record could straddle two 8192-byte
   blocks (`sasquatch-v4be`: `uid index in inode too large (uid: 65535)`), and the
   directory header repeated `start_block = 0` for every child, which is only valid while
   every child inode lives in block 0. Measured with a 400-file tree:
   `round39-ref-multiblock-broken[bulk]: round-39 writer image extracts 0/400 files,
   exit 1; this writer: 400`. Any table crossing one metadata block is affected
   about 227 file inodes, or about 8 KiB of directory body. The claims' carriers are small, so
   their rebuilds are unaffected — but if the freeze builds L1/L2 from a bigger tree, the
   round-39 writer silently produces an image that extracts nothing.
3. **The round-39/37 writer silently drops symlinks-to-directories** (`os.walk` lists them
   in `dnames`): `round39-ref-drops-dir-symlink[links]: round-39 writer drops
   ['bin/dirlink']`. An oracle that walks the source tree would then disagree with the
   extraction. Fixed: they are stored as symlink inodes and extract.
4. **Kill-control semantics:** a `--endian be` image must be read with `-be`; running the
   AVM argv (`sasquatch-v4be` with no flag) on a standard-BE image fails for the *argv*
   reason, not for a claim-relevant reason. Both my selftest and the round-39 critic use
   the correct pairing; worth restating in the freeze's control table so a "marker
   stripped" control does not pass for the wrong cause.
5. **Calibration note on the V1 member's file count** [INFERENCE on cause]: the
   inode-count-consistent walk of the carved BE member gives **1079 inodes = 697 regular
   files + 263 symlinks + 118 directories + 1 char device**, and 697+263+118+1 equals the
   superblock's `inodes` exactly. `R39AssimAvmCritic.md` records "2942 files" for that
   member; that number cannot be a regular-file count of this filesystem. The C1 oracle
   count should come from the oracle's own walk, not from that row.
6. **Limits of the writer for carrier design** (documented in the module docstring):
   no fragments (`frag_count 0`), so the fragment-entry endianness is measured but not
   emitted; no xattrs, export table, sparse blocks or device nodes; all metadata blocks
   are stored **uncompressed** (the LE length field is exercised, the compressed-length
   path is not). Empty directories do extract correctly (measured).
7. **Reader consequence:** the round-40 oracle (`tools/round-40/sqfs-list.py`, other seat)
   must take the metadata header endianness from the *layout*, not from the magic; the
   round-39 reader's BE mode refuses an AVM-genuine image with exit 2 (a ready-made
   negative control, proof 4).

## Integration pointers (L1)

- Copy `artifacts/R40C1AvmWriter/gen-squashfs.py` → `tools/round-40/gen-squashfs.py`
  (sha256 `309c502d21dfeef9b7b2a5a9a62bfa875270fdf79eec671461070996d291042e`).
- Build carriers with `--endian avm-genuine`; per-image sha256s are in
  `artifacts/…/manifest.tsv`. If a carrier must be small enough to stay byte-identical to
  a round-39 rebuild, keep it under one metadata block (inode table < 8192 B and
  directory body < 8192 B) — the five trees here are all in that range except `bulk`.
- Carrier shape the C1 predicate can score without qualifiers: regular files (no
  fragments are emitted; zero-byte files are fine — `small` contains one), optional
  symlinks (in-tree ones are metadata, escaping ones are removed by unblob).
- Suggested frozen control: the `links` image is not a carrier, but it is a useful
  development control for the oracle's symlink classification.

## Limits (what was not examined)

- No REA run at all this wave, so no envelope-level claim is made here.
- No unblob/REA run on V1 or any carrier; the V1 member was never extracted by
  squashfs-tools either (pure-Python reads only). The AVM LE member (`hsqs`) was carved
  for its digest only — C1 explicitly does not claim LE members.
- The Freetz patch itself was not re-read from source; the field-class table is measured
  on two retained genuine images and cited to the R39 lane note, not re-derived from the
  patch.
- The writer emits no fragments and no compressed metadata (see finding 6); a carrier that
  needs either would need a writer extension, not a different claim.
- `--selftest` uses `sasquatch-v4be` from PATH (`--sasquatch` overrides); it does not
  invoke unblob or REA.

## Bounds compliance

No writes outside the report + this seat's artifact directory; no VCS mutation; no
subagents; scratch removed; no `find`/`du` sweeps under `/fast/scratch`; every tool run
honoured `TMPDIR`; no pacman/uv/npm install (nothing was needed — `sasquatch-v4be`,
`unblob`, `python3` were already pinned); `sasquatch`, `sasquatch-v4be` and `unblob` were
not reinstalled, moved or removed. Carrier bytes were never copied into artifacts; only
sha256s and paths are recorded (`genuine-images.txt`).

## Artifacts (directory `artifacts/R40C1AvmWriter/`, 304 KB, `SHA256SUMS`)

`gen-squashfs.py` · `make-dev-images.py` · `diff-be-vs-avmgenuine.py` ·
`probe-v1-member.py` · `manifest.tsv` · `tree-files.tsv` · `selftest.log` ·
`diff-be-vs-avmgenuine.log` / `.json` · `probe-v1-be.txt` ·
`probe-round11-avm-be.txt` · `make-dev-images.log` · `unblob-dev1.log` ·
`unblob-dev2.log` · `unblob-dev-provenance.txt` · `genuine-images.txt` ·
10 × `*-avm-genuine.sqsh` · `SHA256SUMS`.
