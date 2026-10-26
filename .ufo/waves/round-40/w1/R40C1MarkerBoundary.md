# R40C1MarkerBoundary — where the AVM marker boundary actually sits, measured on development inputs

**Verdict: DONE — H1, H2 and H3 are all CONFIRMED, on eleven development images and fifteen REA
runs.** The marker (`mkfs_time == bytes_used`) is a *proxy* that is neither necessary nor
sufficient for the AVM layout: it agrees with the block-length endianness on the diagonal (genuine
AVM-BE, plain standard BE) and mispredicts unblob 26.6.4's extractor argv on both off-diagonals,
which fail with `extractor-failure`, 0 files and `published_bytes: 0` while unblob still exits 0
and REA still reports `ok: true`. Seven boundary findings follow; four of them constrain how
R40-C1's byte clause, its rerun projection and its kill controls must be worded before the freeze,
and one of them (the L1/L2 writer) is a positive result: the genuine AVM layout **is** buildable
from pinned sources on this host in both gzip and xz.

Seat: `R40C1MarkerBoundary` (leaf executor). Lane `kaidoku-shokunin` at base
`fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`; nothing committed, nothing staged, no VCS mutation, no
pacman transaction, no tool installed or removed (`sasquatch`, `sasquatch-v4be` and `unblob` are
untouched, only exercised). Scratch `/fast/scratch/hyaku/kaidoku-r40/R40C1MarkerBoundary` was the
only work area and is removed at exit; everything cited here is in
`.ufo/waves/round-40/w1/artifacts/R40C1MarkerBoundary/` and listed in §9.

## 0. Bounds compliance (what was *not* done)

- **No C1 carrier was touched.** V1 (`FRITZ.Box_6490_Cable-07.57.image`, sha256 `f518ce6b…ede6d`)
  was not downloaded, opened or run; the second vendor member was not downloaded; no lane-built
  AVM-layout image exists as a carrier yet, so none could be run. Every REA/unblob call below is on
  a *development input*: copies of the round-11/round-13 lane images, my own fresh trees, and
  bodies I built in scratch from the pinned Freetz toolchain.
- **No C2 held-out carrier was built or run**; no `heldout-gen.py` invocation; no SKILL.md,
  PROVINCE.md, corpus, tools/ or plans/ write.
- Shokuknow was read-only: three images were hashed in place and **copied** into scratch
  (`round11/work/avm-be.squashfs`, `round13/work/avm-le-genuine.squashfs`,
  `round13/work/avm-le-standard-time.squashfs`). Nothing was written under
  `/home/vgpnk/Projects/shokuknow`.
- Writes are confined to `.ufo/waves/round-40/w1/R40C1MarkerBoundary.md` and
  `.ufo/waves/round-40/w1/artifacts/R40C1MarkerBoundary/`.

## 1. Axes (Godspeed)

| axis | what moved |
|---|---|
| **coverage** | the off-diagonal cells of the marker/layout square are now measured rather than argued: 11 images × {unblob argv, unblob files, REA envelope, direct `sasquatch-v4be` with and without `-be`}. Includes the first multiblock genuine AVM-layout bodies in the lane's record (vendor-member shape, xz *and* gzip) and the first `squashfs_v4_broadcom` row. |
| **depth** | the discriminating test is no longer "first metadata block length, plausibility only": an exact span walk decides block-length endianness on tables spanning many metadata blocks (measured 11/11, opposite endianness overshoots on the first block). Plus: the marker branch is generic v4-BE (Broadcom too), the marker is a u32/u64 compare (unreachable ≥ 4 GiB), the two failing modes are outcome-identical in the normalised envelope, and REA's `evidence_id` is now recomputable in pure Python — with the measured caveat that it is not rerun-stable. |
| **calibration** | every claim below carries the command, exit code and byte-level difference; the negative controls (marker-only body, marker-stripped genuine body, plain BE body, LE marker-false body) are all measured, not asserted. |

## 2. Method, and what was read before any data was taken

Sources first, data second — no classifier was fitted to observations.

`/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`
(sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`), byte-identical to the
file round 39 pinned. Decision lines, unedited:

```
40:            case Endian.BIG, 4:
48:                    is_avm = header.bytes_used == header.mkfs_time
49:                    if not is_avm:
50:                        commands_args.append("-be")
51:            case Endian.BIG, _:
52:                commands_args.append("-be")
53:            case Endian.LITTLE, _:
54:                commands_args.append("-le")
82:        end_of_data_offset = (start_offset + header.bytes_used) & 0xFF_FF_FF_FF
```

`SquashFSv4LEHandler.C_DEFINITIONS` (same file) declares `uint32 mkfs_time` and `uint64
bytes_used`; the v4 superblock is 96 B, `mkfs_time` at offset 8, `bytes_used` at offset 40,
`inode_table_start` 64, `directory_table_start` 72, `fragment_table_start` 80, `lookup_table_start`
88. `SquashFSv4BEHandler` only supplies `EXTRACTOR = SquashFSExtractor(4, 0x73717368)`;
`SquashFSv4BroadcomHandler` supplies `EXTRACTOR = SquashFSExtractor(4, 0x71736873)` — it inherits
`extract()` unchanged, so the marker branch is reached from **both** v4 handlers (§4.B2).

REA side: `rea-agents@6.5.0 dist/domain/evidence.js:182`
`computeEvidenceId = (evidence) => \`ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}\``
and `dist/cli-runtime/reconstructionObligationLedgerSchemas-Bao0xMr-.js:30-92` (`emitCanonical`:
sorted keys, no whitespace, JS `JSON.stringify` primitives). §4.B6 is a pure-Python
reimplementation validated on real envelopes.

Tool pins: unblob 26.6.4 (`…/uv/tools/unblob/bin/unblob`, sha256
`0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`; envelope
`engine.executable_sha256` equals this), `sasquatch-v4be` sha256
`fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`, `sasquatch` sha256
`ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`, both
`unsquashfs version 4.5.1 (2022/03/17)`; `python3` 3.14.8; `gen-squashfs.py` (round-39 revision)
sha256 `f535e60ee15222a7b0809cf53858e72a82040a519450c562e369224d4fe41188`. Every REA run used
`REA_UNBLOB_COMMAND=/home/vgpnk/.local/bin/unblob` and cwd inside my scratch, so `unblob.log` never
landed anywhere else.

## 3. Hypotheses and verdicts

Eleven development images (fixtures retained, §9). `marker` = `mkfs_time == bytes_used`;
`blocklen` = metadata block-length endianness decided by the exact span walk (§4.B4).

| image | size | magic | comp | marker | blocklen | unblob handler | unblob argv | files | `ExtractCommandFailedReport` | `sasquatch-v4be` noflag | `sasquatch-v4be -be` | REA (cov / files / P / gaps) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `avm-be.squashfs` (round11, genuine AVM-BE, xz) | 4096 | `sqsh` | 4 | **T** | LE | `squashfs_v4_be` | no `-be` | 4 | 0 | **4, exit 0** | 0, exit 1 | complete / 4 / 25 / — |
| `d2-avm-markerstripped.sqsh` (= above, `mkfs_time:=1700000000`) | 4096 | `sqsh` | 4 | **F** | **LE** | `squashfs_v4_be` | **`-be`** | **0** | **1** | **4, exit 0** | 0, exit 1 | partial / **0** / **0** / `extractor-failure` |
| `d4-carrier-be.sqsh` (fresh tree, `--endian be`) | 609 | `sqsh` | 1 | F | BE | `squashfs_v4_be` | `-be` | 3 (+1 symlink) | 0 | 0, exit 1 | **3, exit 0** | partial / 3 / 222 / `unpublished-entry` |
| `d5-avm-markeronly.sqsh` (same tree, `--endian avm`) | 609 | `sqsh` | 1 | **T** | **BE** | `squashfs_v4_be` | **no `-be`** | **0** | **1** | 0, exit 1 | **3, exit 0** | partial / **0** / **0** / `extractor-failure` |
| `d6-broadcom-markeronly.sqsh` (= d5, magic `qshs`) | 609 | `qshs` | 1 | **T** | **BE** | `squashfs_v4_broadcom` | **no `-be`** | **0** | **1** | 0, exit 1 | **3, exit 0** | partial / **0** / **0** / `extractor-failure` |
| `avm-le-genuine.squashfs` (round13) | 4096 | `hsqs` | 4 | T | LE | `squashfs_v4_le` | `-le` | 4 | 0 | 4, exit 0 (`sasquatch`) | 4, exit 0 (`-le`) | complete / 4 / 25 / — |
| `le-standard-time.sqsh` (round13, marker false) | 4096 | `hsqs` | 4 | F | LE | `squashfs_v4_le` | `-le` | 4 | 0 | 4, exit 0 | 4, exit 0 (`-le`) | complete / 4 / 25 / — |
| **`m1-avm-xz.sqsh`** (my tree, Freetz AVM_BE `-comp xz`, multiblock) | 49152 | `sqsh` | 4 | **T** | LE | `squashfs_v4_be` | no `-be` | **256** (+1 symlink) | 0 | **256, exit 0** | 0, exit 1 | partial / 256 / 44253 / `unpublished-entry` |
| **`m1s-avm-markerstripped.sqsh`** (= m1, marker stripped) | 49152 | `sqsh` | 4 | F | LE | `squashfs_v4_be` | **`-be`** | **0** | **1** | **256, exit 0** | 0, exit 1 | partial / **0** / **0** / `extractor-failure` |
| **`m2-avm-gzip.sqsh`** (same tree, `-comp gzip`, multiblock) | 49152 | `sqsh` | 1 | T | LE | `squashfs_v4_be` | no `-be` | 256 (+1) | 0 | 256, exit 0 | 0, exit 1 | partial / 256 / 44253 / `unpublished-entry` |
| **`m2s-avm-markerstripped.sqsh`** (= m2, marker stripped) | 49152 | `sqsh` | 1 | F | LE | `squashfs_v4_be` | **`-be`** | **0** | **1** | **256, exit 0** | 0, exit 1 | partial / **0** / **0** / `extractor-failure` |

(Bold cells are the boundary cells. Machine-readable: `matrices/master.tsv`, sha256
`2937640aec8bbbe7c83a8aec533422421f293aad016c170807bacaab645f5d3e`; the unblob argv column is
verbatim from `logs/unblob/*.log`; every run's `unblob` exit code was **0**, including both failing
modes.)

### H1 — genuine AVM layout with the marker stripped ⇒ unblob adds `-be`, extraction fails; `sasquatch-v4be` without `-be` still extracts — **CONFIRMED**

Three bodies, two compression modes, single-*and* multi-metadata-block tables:

- `d2` (4096 B, xz, inode span 1 block / dir span 2 blocks), `m1s` (49152 B, xz, inode span 2 / dir
  span 3), `m2s` (49152 B, gzip, same spans). Each is its source image with **exactly four bytes**
  changed, at offsets `[8, 9, 10, 11]` (`mkfs_time`); `bytes_used` is untouched.
- unblob argv: `sasquatch-v4be -be -no-exit-code -f -d <out>/…_extract …` (vs no `-be` on the
  source). 0 regular files; `ExtractCommandFailedReport` present; unblob exit 0.
- REA 6.5.0: `ok: true`, `coverage: partial`, `files: 0`, `published_bytes: 0`,
  `extraction_gaps: [{kind: extractor-failure, handler: squashfs_v4_be, dependencies: []}]`,
  `chunks[0].extraction_failed: true`.
- Direct extractor: `sasquatch-v4be` **without** `-be` → exit 0 with 4 / 256 / 256 files; **with**
  `-be` → exit 1, 0 files, first stderr line `Reading a different endian SQUASHFS filesystem on …`.

So the marker is what unblob reads, and the layout is what the extractor reads: on this body
unblob's own decision is wrong and the extractor would have succeeded with the argv unblob withheld.

### H2 — marker-only standard-BE body (`gen-squashfs.py --endian avm`) fails the other way — **CONFIRMED**

- `d5` (fresh tree, gzip, 609 B): argv **without** `-be`; 0 files; `ExtractCommandFailedReport`;
  REA partial / 0 / 0 / `extractor-failure`. `sasquatch-v4be -be` extracts 3 files, exit 0;
  `sasquatch-v4be` noflag exits 1 with 0 files.
- Re-verified the generator identity the round-39 critic proved, at the round-39 revision
  (`f535e60e…`): `d4` (`--endian be`) sha256 `5c7e0c6d…c07ff`; patching `d4[8:12] := bytes_used`
  gives sha256 `a13bb9f3…0c73` = `d5`, **0 differing bytes**. `--endian avm` is still exactly the
  marker transform on a standard-BE body — it cannot write LE block lengths.

### H3 — LE AVM image (`hsqs`, marker true) goes through `squashfs_v4_le` with `-le` and extracts — **CONFIRMED**

`avm-le-genuine.squashfs` (round13, 4096 B, xz, `mkfs_time 361 == bytes_used 361`): handler
`squashfs_v4_le`, argv `sasquatch -le -no-exit-code -f -d …`, 4 files, `ExtractCommandFailedReport`
absent, REA `complete / 4 / 25 / no gaps`. The LE branch appends `-le` unconditionally
(handler:53-54); `le-standard-time.sqsh` (`mkfs_time 1792871460 ≠ bytes_used 361`) also gives
`complete / 4 / 25`, so **the LE path is marker-blind** — "the marker is invisible to unblob" is
true only in LE scope and false in BE-v4 scope, which is precisely the round-39 E6/E4 split.

## 4. Boundary findings

### B1 — the marker is neither necessary nor sufficient: both off-diagonals fail

```
                     blocklen BE            blocklen LE
marker ==  F     d4 -be      -> 3 files    d2/m1s/m2s -be  -> 0 files, extractor-failure
marker ==  T     d5/d6 no-be -> 0 files    avm-be/m1/m2 no-be -> 4 / 256 files
```

The diagonal is correct; both off-diagonal cells are wrong, and both fail loudly. The draft's kill
control "a genuine AVM body with the marker stripped (unblob adds `-be`, extraction fails)" is
exactly the `marker=F / LE` cell (`m1s`), measured. **Note for the predicate:** the *marker* conjunct
cannot reject the marker-only control — that body has `marker == True` by construction. The
discriminating conjunct is the block-length one (§4.B4), so the byte clause must be a conjunction
with the layout half load-bearing, and the freeze should say so.

### B2 — the branch is generic v4-BE, not AVM-scoped

`d6` is `d5` with the magic rewritten `sqsh` → `qshs`. unblob selects `squashfs_v4_broadcom`
(`SquashFSv4BroadcomHandler`, `EXTRACTOR = SquashFSExtractor(4, 0x71736873)`), inherits `extract()`,
lands in `case Endian.BIG, 4:` with `marker == True`, therefore appends **no** `-be`:
`sasquatch-v4be -no-exit-code -f -d …` → 0 files, `ExtractCommandFailedReport`, REA
`partial / 0 / 0 / extractor-failure`. `sasquatch-v4be -be` on the same bytes exits 0 with 3 files,
printing only `Non-standard SquashFS Magic: 'qshs'`. [INFERENCE] any big-endian v4 SquashFS whose
superblock happens to satisfy `bytes_used == mkfs_time` loses `-be`, vendor-independent — the
handler calls this an AVM marker; the code applies it to every BE v4 image.

### B3 — the marker comparison is u32 vs u64: unreachable at ≥ 4 GiB

`mkfs_time` is `uint32`, `bytes_used` is `uint64`; the comparison at handler:48 is numeric equality
of a 32-bit and a 64-bit field, so it can only hold for `bytes_used < 2**32`. Demonstrated
arithmetically against the same field widths: `mkfs_time = 46829`, `bytes_used = 0x1_0000_0000 +
46829` → `bytes_used == mkfs_time` is `False` while the low 32 bits are equal. `calculate_chunk`
additionally masks the chunk end to 32 bits (handler:82), so a >4 GiB AVM image is mishandled twice.
No planned carrier is anywhere near this bound (the V1 member is 5 442 392 B; my largest dev body is
49 152 B); the limit sentence in the knowledge entry should still scope it, because "unblob reads
the AVM marker" is a sub-4 GiB statement.

### B4 — "first metadata block length decodes as little-endian" is not decidable on its own; the span walk is

Metadata tables are contiguous: every metadata block is `u16 header` + payload, with the block
length in the low 15 bits and `0x8000` marking an uncompressed block. Walking `2 + len` from
`inode_table_start` must land **exactly** on the next table start. Measured on all eleven images
(`matrices/probe-matrix.tsv`, sha256 `3b95da5c…`; `tools/probe_sqfs.py`):

| image | blocklen | first len LE / BE | inode-span walk LE / BE | dir-span walk LE / BE |
|---|---|---|---|---|
| `avm-be.squashfs` | LE | 116 / 29696 | 1/exact · 1/overshoot | 2/exact · 1/overshoot |
| `m1-avm-xz.sqsh` | LE | 912 / 4099 | **2/exact** · 1/overshoot | **3/exact** · 1/overshoot |
| `m2-avm-gzip.sqsh` | LE | 1397 / 29957 | **2/exact** · 1/overshoot | **3/exact** · 1/overshoot |
| `d2`/`m1s`/`m2s` (marker stripped) | LE | as their sources | exact · overshoot | exact · overshoot |
| `avm-le-genuine` / `le-standard-time` | LE | 112 / 28672 | 1/exact · 1/overshoot | 2/exact · 1/overshoot |
| `d4` / `d5` / `d6` | BE | 11393 / 300 | 1/overshoot · 1/exact | 1/overshoot · 2/exact |

Correct endianness: every span exact (2–3 metadata blocks per span on the multiblock bodies);
wrong endianness: overshoot on the **first** block in 11/11 cases. This resolves the endianness on
multi-block tables exactly, which lifts round 39's "on the real firmware members … only plausibility
separates them (1380 vs 25605)" limit — that sentence was about single-value plausibility, not about
the walk. A single 2-byte length is also degenerate in principle ([DERIVED] from the encoding: bytes
`01 01` read as 257 in both byte orders, and 257 is a plausible length); the span walk has no such
degenerate case because it must also land on the next table offset.

### B5 — the two failing modes are outcome-identical in the normalised envelope

`d2` vs `d5`, and `m1s` vs `m2s`, differ in **no** outcome field of
`normalized_result`: same handler, `extraction_failed: true`, `coverage: partial`, `files: 0`,
`published_bytes: 0`, `gaps: [extractor-failure]`. Only the following separate them: the subject
digest, `selection`, the chunk `range` length, and inside `raw_result` the extractor `command`
(`-be` present vs absent) and the base64 `stderr`. Consequence for the freeze: an outcome-only
projection cannot tell a marker-stripped genuine body from a marker-only standard body, so the rerun
projection must carry the subject digest (and, if the freeze wants it, the `-be` token from the
recorded argv) — the draft's "semantic projection" must be specified, not implied. Conversely,
`m1` (xz) and `m2` (gzip) are *different bodies with the same tree* and their stable projections
differ **only** in subject/selection sha256: same 256 per-file hashes, same `published_bytes 44253`.
Without the subject digest in the projection, an xz/gzip pair is interchangeable.

### B6 — REA's `evidence_id` is recomputable in pure Python, but it is a tamper seal, not provenance, and it is not rerun-stable

`tools/recompute_evidence_id.py` implements `ev_ + sha256(canonical(semanticProjection(data)))` from
the installed `evidence.js:182` + `emitCanonical`. Results (`matrices/evidence-id-check.txt`):

```
python3 -I -B tools/recompute_evidence_id.py envelopes/*.envelope.json   -> exit 0, 15/15 MATCH, 0 MISMATCH
python3 -I -B recompute_evidence_id.py corpus/evidence/round-39/c1/K{1,2,6}/after.json -> exit 0, 3/3 MATCH
```

So R40-C1's clause "recomputes to its evidence id" is executable, and any edit to a committed
receipt breaks it (the projection includes `raw_result` and `normalized_result`). It does **not**
prove provenance — a fabricator holding the algorithm can mint a self-consistent id — and it is
**not** stable across runs: three fresh `extract-firmware` runs of `m1` into different output
directories differed in **1850 leaf values**, all of them path-, PID- or scratch-derived:

```
.normalized_result.output_directory        .parameters.output_directory
.normalized_result.chunks[].provider_id    (re-minted per run: 28325:1 -> 2724035:1)
.normalized_result.derivations[].provider_blob_id
.normalized_result.files[].path            (absolute)
.raw_result.execution.args[]               (absolute outdir)
.raw_result.report[].task.path / .subtasks[].path / .subtasks[].blob_id / .reports[].path / .reports[].id
```

Therefore the rerun binding cannot compare evidence ids; it must compare a projection defined over
the stable subset — and "recomputes to its evidence id" must be worded as *self-consistency of the
committed record*, with provenance resting on the rerun clause.

### B7 — the rerun-comparable projection, measured

`tools/stable_projection.py` keeps subject digest, operation, provider, engine
(name/version/executable_sha256), selection, coverage, published_bytes, chunks
(handler/extraction_failed/range), files (relative_path suffix after the `*_extract/` root + sha256
+ size), gaps (kind/relative_path/handler/dependencies) and unpublished entries. It drops exactly
the fields B6 lists as unstable. Measured (`matrices/projection-rerun-check.txt`):

```
m1-avm-xz  ffa29de2193ea16641934869d09be9f75bc4c0b766274320aca0ef0092436e60
m1-run2    ffa29de2193ea16641934869d09be9f75bc4c0b766274320aca0ef0092436e60
m1-run3    ffa29de2193ea16641934869d09be9f75bc4c0b766274320aca0ef0092436e60
d4-carrier-be  f063a4ccaa3bf86753c663f7e337b19270a0ec171ad290589b843b4472aca5de
d4-run2        f063a4ccaa3bf86753c663f7e337b19270a0ec171ad290589b843b4472aca5de
d4-run3        f063a4ccaa3bf86753c663f7e337b19270a0ec171ad290589b843b4472aca5de
```

Three runs, two carriers (one 256-file multiblock, one 3-file with a symlink), identical
projections. This is the field set the freeze can name.

### B8 — exit codes are not signals, and one stderr sentence lies in both directions

`unblob` exited **0 on all eleven runs**, including the four that extracted nothing; REA exited 0
with `ok: true` on all fifteen runs, including the five with `published_bytes: 0`. The only reliable
signals are the `ExtractCommandFailedReport` event / `chunks[].extraction_failed` / the file count.
The stderr sentence `suggests a SquashFS image of a different endianess` appears on a **successful**
run too (`m1` noflag: exit 0, 256 files) and on a failing one (`m2s` noflag: exit 1, 0 files), which
reproduces the round-39 warning against keying on it.

## 5. Comparison with the round-39 matrix (`R39AssimAvmCritic.md`, `artifacts/matrix.tsv`)

| round-39 row | reproduced here | delta |
|---|---|---|
| round11 `avm-be.squashfs` — marker yes, len LE, no `-be`, 4 files | yes, byte-identical (`c7f74691…`) | adds the REA envelope (`complete / 4 / 25`) and the `-be` arm (0 files, exit 1) |
| round13 `avm-le-genuine.squashfs` — `hsqs`, `-le`, 4 files | yes (`18d3ad05…`) | adds the REA envelope and the marker-false LE control (`le-standard-time`, `complete / 4 / 25`) |
| round9 `sqimg-avm-probe.bin` — marker-only BE, no `-be`, 0 files, exit 1 | yes, with my own gzip build `d5` | adds `-be` arm (3 files) and the REA envelope |
| round37 K1/K4, fresh `carrier-be.sqsh` — no marker, `-be`, files | yes, `d4` (3 files; tree differs, as expected) | adds the REA envelope |
| fresh `carrier-avm.sqsh` — marker yes, BE, no `-be`, 0 files | yes, `d5` | same |
| fresh `avm-be-markerstripped.sqsh` — marker no, LE, `-be`, 0 files | yes, `d2` | same |
| AVM 07.57 BE member / LE member | **not re-run** (carrier discipline) | none — the vendor image was not opened this wave |
| — | **new**: `m1/m1s`, `m2/m2s` multiblock genuine AVM (xz, gzip) with and without the marker | first vendor-member-shape off-diagonal evidence in the lane |
| — | **new**: `d6` `squashfs_v4_broadcom` marker-true row | the branch is not AVM-scoped |
| — | **new**: exact span walk, evidence-id recomputation, stable projection | see §4.B4, B6, B7 |

Nothing in the round-39 matrix is contradicted; the two-direction misprediction it reported is
confirmed and extended to multiblock bodies and both compression modes.

## 6. Feed-forward to the freeze (R40-C1, and the C2 rows it touches)

1. **Byte clause.** Keep `mkfs_time == bytes_used` as the marker, but state (a) the layout conjunct
   is the load-bearing one — the marker-only control satisfies the marker by construction (§4.B1);
   (b) the marker is a u32/u64 compare, so it is a sub-4 GiB statement (§4.B3); (c) the branch fires
   on every BE v4 image, `squashfs_v4_broadcom` included (§4.B2). Replace "its first metadata block
   length decodes as little-endian" with the span walk of §4.B4 (`inode_table_start → next table
   start` and `directory_table_start → next table start`, all `2+len` steps exact, at least one span
   longer than one block) — decidable, exact on multiblock tables, and it has no degenerate case.
2. **Kill control "genuine AVM body with the marker stripped".** Measured exactly as drafted
   (`m1s`: `-be`, 0 files, `extractor-failure`, `P=0`; `sasquatch-v4be` noflag 256 files). A
   fabricated *success* receipt for such a body cannot survive the rerun; a fabricated *failure*
   receipt for it is indistinguishable from the marker-only control's real receipt in outcome fields
   (§4.B5) — which is why the byte clause, not the envelope, must adjudicate "which body is the
   carrier".
3. **Carriers L1/L2 are buildable — positive result.** The genuine AVM layout is reproducible on
   this host from pinned sources: SourceForge `squashfs4.3.tar.gz`, md5
   `d92ab59aabf5173f2a59089531e30dbf` (the Freetz pin; re-downloaded and matched this wave, 182 550 B),
   plus the 17 round-11 Freetz patches (`build/tc-pins.txt` carries every sha256), built with
   `EXTRA_CFLAGS="-fcommon -DTARGET_FORMAT=AVM_BE -std=gnu89" LEGACY_FORMATS_SUPPORT=1 GZIP_SUPPORT=1
   LZMA_XZ_SUPPORT=1 XZ_SUPPORT=1`. `mksquashfs` then writes LE block lengths **and** sets
   `mkfs_time := bytes_used` itself (`m1` 46829==46829, `m2` 47866==47866) — the marker is a writer
   side effect, which is exactly why it is only a proxy. Both `-comp xz` and `-comp gzip` produce
   multiblock genuine bodies in under a minute. **My `m1`/`m2` are development fixtures and were run
   before the freeze; they must not be nominated as L1/L2.** The freeze should nominate *fresh*
   builds from this recipe, with the tarball md5 + patch hashes recorded, and no pre-freeze run.
4. **Rerun projection.** Name the field set of §4.B7 (`tools/stable_projection.py`) and the exclusion
   list of §4.B6 verbatim; include the subject digest and `selection.sha256`, otherwise an xz/gzip
   pair with the same tree collides (§4.B5).
5. **"recomputes to its evidence id".** Executable today (`tools/recompute_evidence_id.py`, 15/15 +
   3/3). Word it as self-consistency of the committed receipt, not as provenance, and do not expect a
   rerun to reproduce the id — it will not (§4.B6). R39-CL5's residual risk is therefore unchanged by
   this clause alone; the rerun binding must carry provenance.
6. **C2 rows this touches.** Key the `avm-marker-be-dropped` row/class on block-length layout (BE
   lengths, or `-be` present in the recorded `command`), not on `mkfs_time == bytes_used`; two
   measured classes are available for a v2 table: `avm-layout-be-flag-passed` (marker false + LE
   lengths → 0 files, `extractor-failure`, `P=0`: `d2`/`m1s`/`m2s`) and `marker-only-be` (marker true
   + BE lengths → 0 files, `extractor-failure`: `d5`), plus, if in scope, `v4-broadcom-marker-true`
   (`d6`). Adding these does not touch C2's out-of-domain guard.

## 7. Evidence — exact commands, outputs, exit codes

```
# layout probe (pure stdlib; never sasquatch, never unblob)
python3 -I -B tools/probe_sqfs.py avm-be.squashfs d2-avm-markerstripped.sqsh d4-carrier-be.sqsh \
  d5-avm-markeronly.sqsh d6-broadcom-markeronly.sqsh avm-le-genuine.squashfs le-standard-time.sqsh \
  m1-avm-xz.sqsh m1s-avm-markerstripped.sqsh m2-avm-gzip.sqsh m2s-avm-markerstripped.sqsh
  -> exit 0, 11 rows (matrices/probe-matrix.tsv)

# 4-byte marker transforms
D1 vs D2 differ at offsets [8,9,10,11];  D4 vs D5 differ at offsets [8,9,10,11]
d4[8:12] := bytes_used  -> sha256 a13bb9f39e3f99b57cec034e521149072a1d628edbba3742e8b3d1c6a9dd0c73
                           == d5-avm-markeronly.sqsh, 0 differing bytes

# direct unblob (cwd = a scratch subdir, so unblob.log lands there)
cd <run-dir> && /home/vgpnk/.local/bin/unblob -v -e out <image>
  m1   -> handler=squashfs_v4_be   cmd='sasquatch-v4be -no-exit-code -f -d …'         exit 0, 256 files
  m1s  -> handler=squashfs_v4_be   cmd='sasquatch-v4be -be -no-exit-code -f -d …'     exit 0,   0 files, ExtractCommandFailedReport
  d2   -> … '-be' … exit 0, 0 files;  d5 -> … no '-be' … exit 0, 0 files
  d6   -> handler=squashfs_v4_broadcom  no '-be'  exit 0, 0 files
  avm-le-genuine -> squashfs_v4_le  'sasquatch -le …'  exit 0, 4 files

# direct extractor matrix (no unblob)
sasquatch-v4be [noflag|-be] -f -d out <img>   -> logs/sasquatch/*.stderr.txt
  m1   noflag 256/exit0        -be 0/exit1      m1s noflag 256/exit0  -be 0/exit1
  d2   noflag 4/exit0          -be 0/exit1      d5  noflag 0/exit1    -be 3/exit0
  d6   noflag 0/exit1          -be 3/exit0 ("Non-standard SquashFS Magic: 'qshs'")
  avm-le-genuine  'sasquatch -le' 4/exit0 ; 'sasquatch' noflag 4/exit0
  le-standard-time 'sasquatch -le' 4/exit0 ; 'sasquatch' noflag 4/exit0

# REA (15 runs, all exit 0, all `ok: true`)
cd "$S/<run>" && REA_UNBLOB_COMMAND=/home/vgpnk/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <img> <run>/extract
  m1/m2  : coverage=partial files=256 P=44253 gaps=[unpublished-entry] chunk extraction_failed=false
  m1s/m2s/d2/d5/d6 : coverage=partial files=0 P=0 gaps=[extractor-failure] chunk extraction_failed=true
  avm-be/avm-le-genuine/le-standard-time : coverage=complete files=4 P=25 gaps=[]

# evidence-id recomputation (pure Python, from evidence.js:182 + emitCanonical)
python3 -I -B tools/recompute_evidence_id.py envelopes/*.envelope.json  -> exit 0, 15 MATCH, 0 MISMATCH
… corpus/evidence/round-39/c1/K1|K2|K6/after.json                       -> exit 0, 3 MATCH

# rerun stability
runs of m1 into three different outdirs: 1850 differing leaf values, all path/PID/scratch derived
stable_projection.py sha256: m1 x3 = ffa29de2…, d4 x3 = f063a4cc…

# L1/L2 writer feasibility (scratch only)
curl https://downloads.sourceforge.net/project/squashfs/squashfs/squashfs4.3/squashfs4.3.tar.gz
  -> 182550 B, md5 d92ab59aabf5173f2a59089531e30dbf  (== the Freetz pin)
patch -p0 with the 17 round-11 patches (2 files already carry AVM_BE; _endian.h present)
make … TARGET_FORMAT=AVM_BE … -> exit 0 (mksquashfs 204704 B, unsquashfs 113240 B)
mksquashfs bigtree m1-avm-xz.sqsh   -comp xz   … -b 65536 -> marker T, blocklen LE, 2+3 metadata blocks
mksquashfs bigtree m2-avm-gzip.sqsh -comp gzip … -b 65536 -> marker T, blocklen LE, 2+3 metadata blocks
```

## 8. Limits (what this report does not show)

- **No vendor image was opened**, so nothing here is measured at real-flash size or on AVM's own
  writer output; §4.B3's 4 GiB bound is derived from the field widths and demonstrated
  arithmetically, not exercised on a 4 GiB image. The vendor-member shape is approximated by my
  49 152 B multiblock bodies (2 inode blocks, 3 directory blocks).
- `sasquatch`'s endianness detection was **exercised, not re-derived from source**; the claim that it
  keys on the metadata block-length field rests on its behaviour (11/11 images, both directions) and
  on the round-11/Freetz bullet already in the lane.
- Only two AVM writer builds were observed (`m1`, `m2`) plus round 11's retained image; whether every
  AVM_BE `mksquashfs` writes `mkfs_time := bytes_used` unconditionally is [INFERENCE] from three
  artefacts, not from the patch source.
- The stable projection was validated on two carriers × three runs; a carrier with a fragment table
  or an escaping symlink may add fields this projection does not yet list.
- No C2 work: the C2 rows in §6.6 are offered as measured inputs, not as a proposed table.
- `/fast/scratch` sweeps were avoided; no `find`/`du` under it.

## 9. Artifacts (all under `.ufo/waves/round-40/w1/artifacts/R40C1MarkerBoundary/`, 74 files, 2.6 MB)

- `tools/` — `probe_sqfs.py` (sha256 `3715d39d…425e9a`: pure-stdlib layout probe, exact span walk),
  `mk-matrix.py` (assemble `master.tsv` from retained runs), `recompute_evidence_id.py`
  (`56334537…c0d76b`), `stable_projection.py` (`a3432d5a…24e95e`).
- `matrices/` — `master.tsv` (`2937640a…`), `probe-matrix.tsv` (`3b95da5c…`), `sq-matrix.tsv`
  (`5d91b014…`), `ub-matrix.tsv` (`92f8e503…`), `evidence-id-check.txt` (15/15 MATCH),
  `projection-rerun-check.txt`.
- `logs/unblob/` — the eleven `unblob.log` files the argv column is quoted from;
  `logs/sasquatch/` — 22 extractor stderr transcripts (one per `sq-matrix.tsv` row).
- `envelopes/` — all fifteen REA envelopes (`{ok,data,meta}`): the eleven images plus `m1`×2 and
  `d4`×2 reruns into different output directories (the rerun evidence).
- `build/` — `tc-pins.txt` (tarball md5, 17 patch hashes, build command, binary hashes, tool pins),
  `mk-m1.log`, `mk-m2.log`.
- `fixtures/` — the eleven dev images with `sha256sums.txt`: `avm-be.squashfs` `c7f74691…` (copy of
  `shokuknow/lanes/kaidoku/round11/work/`), `avm-le-genuine.squashfs` `18d3ad05…` and
  `le-standard-time.sqsh` `6d787405…` (copies of `round13/work/`), `d2` `abfd7ec9…`, `d4`
  `5c7e0c6d…`, `d5` `a13bb9f3…`, `d6` `864c0458…`, `m1` `bbe714e6…`, `m1s` `189484e8…`, `m2`
  `55b2934b…`, `m2s` `40ff4782…`. **All dev fixtures; none is or may become a C1 carrier.**
- `inventory.sha256` — every artifact except itself.

## 10. Tooling record

No installs, no upgrades, no pacman transaction (host guard respected), no changes to `unblob`,
`sasquatch` or `sasquatch-v4be`. `npx -y rea-agents@6.5.0` used the already-present package
(`--version` → `6.5.0`). The `squashfs4.3` AVM_BE toolchain was **built inside scratch** from the
pinned SourceForge tarball and the read-only round-11 patch set, used to build two dev fixtures, and
removed with the scratch; it was never installed to `PATH`.
