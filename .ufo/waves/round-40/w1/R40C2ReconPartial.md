# R40C2ReconPartial — C2 `partial-body-failure` damage recipe and v2 contract recon (round 40, wave 1)

**Verdict: DONE — a deterministic, offset-computed damage recipe now produces
`extractor-failure` with `published files > 0` on 12/12 development carriers (3 fresh trees x
gzip/xz x BE/LE) plus 4 edge carriers and a repeat run, the round-39 `body-extractor-failure` recipe is
characterised as never giving `P > 0` (6/6), and the L1's v2 grammar is implemented, selftested
(13/13) and dev-scored (26/26) with four measured kill controls. Three contract points need a
freeze decision and are argued in §7.**

Seat `R40C2ReconPartial`, leaf. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base
`fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f` (read-only `rev-parse`; no VCS mutation, no commit, no
`corpus/`/`tools/`/`plans/`/`SKILL.md`/`PROVINCE.md` write). Wrote only
`.ufo/waves/round-40/w1/R40C2ReconPartial.md` and
`.ufo/waves/round-40/w1/artifacts/R40C2ReconPartial/`. Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40C2ReconPartial` (removed at the end; everything cited is copied
into the artifacts dir, `MANIFEST.sha256` = 107 files, 1.2 MB).

Tools used as installed — no install, upgrade or removal this wave, so no tooling authorisation
entry is needed: rea-agents **6.5.0** (`npx`, package root
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, `package.json` version 6.5.0),
unblob **26.6.4** (`unblob --version`), `sasquatch` / `sasquatch-v4be` **4.5.1 (2022/03/17)**
(`-version`), node v24.21.0, Python 3.14.8. pacman untouched. No `xd://mcp__rea_*` device used; REA
only via the CLI.

**Frozen-carrier discipline.** No REA or unblob run touched V1, any vendor image, any lane-built C1
carrier or any C2 held-out carrier, and no held-out carrier was built. Every carrier here comes from
a fresh tree this seat authored in scratch
(`tools/round-39/gen-squashfs.py TREE OUT --endian le|be|avm --comp gzip|xz`), plus one
empty-directory tree and two structural edge trees. Direct `sasquatch-v4be` / `sasquatch` reads of
those development images only (§3.3 fill probe, §3.2 direct extraction checks).

---

## 1. What was run

| group | carriers | REA runs | result |
|---|---|---|---|
| recipe matrix | 3 trees x {be,le} x {gzip,xz} = 12 | 12 + 1 repeat | all `extractor-failure`, `P=5`, `published_bytes=26500` |
| recipe edges | first data block, mid-file block, single-file tree, incompressible tail | 4 | all `extractor-failure`, `P` 5/5/1/2 |
| round-39 body failure | zero-id-table x5 (be/le, gzip/xz), bad-minor x1 | 6 | all `extractor-failure`, **`P=0`** |
| clean controls | be-gzip, be-xz, empty dir | 3 | no gap, `P=5/5/0`, `coverage complete` |
| non-`extract_firmware` probes | extract-artifact x2 (raw + tar), analyze x2, inspect x2 | 6 | all `{"ok":false,"error":{"code":"target_unavailable"}}` — see §7.1 |

26 `extract_firmware` envelopes and 2 non-`extract_firmware` envelopes are saved under
`envelopes/`; the feature extractor `feat.py` reads every field named in the assignment from each
one (`tables/feature-table.md`, `tables/features.json`).

Build command per image (and the rest of the sequence) is `build.sh` in the artifacts dir; it is
`sh -n` clean and is the exact reproduction (tree seeds `r40-partial-t1|t2|t3`).

REA command per run (`runrea.sh`, one fresh cwd per run so `unblob.log` never lands in the lane):

```
cd "$S/run/<name>" && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
  <carrier> "$S/run/<name>/out"
```

---

## 2. The recipe: `corrupt_partial(img_bytes) -> bytes`

Implementation: `artifacts/R40C2ReconPartial/sqfs-corrupt.py` (`corrupt_partial`,
`PARTIAL_FILL = 0xFF`). Rule, with every offset computed from the image:

1. Parse the superblock (96 bytes) — magic selects the endianness (`hsqs` / `sqsh`), and
   `inode_table_start`, `dir_table_start`, `id_table_start`, `bytes_used`, `block_size`,
   compression id come from the superblock itself.
2. Walk the directory tree from `root_inode` through the inode table and directory table metadata
   streams (decompressing metadata blocks when they are not flagged `0x8000`), collecting regular
   files **in stored (directory-scan) order** with each file's `start_block`, `file_size` and data
   block-size list from its inode.
3. Turn each block-size field into an absolute span: `offset = start_block`, and each following
   block starts at the previous `offset + (field & ~0x01000000)`; `field & 0x01000000` marks a
   stored-raw block, `(field & ~0x01000000) == 0` marks a sparse block.
4. Choose the target: scanning the file list **backwards**, the first file that owns a compressed,
   non-sparse data block, and inside it its **last** compressed block.
5. Overwrite that block's on-disk bytes with `0xFF` (`bytes([fill]) * length`). Nothing else in the
   image changes: `bytes_used`, the id table and every metadata block stay intact, so unblob still
   recognises the `squashfs_v4_be` / `squashfs_v4_le` chunk.

Preconditions raise instead of silently no-op'ing: fewer than 2 regular files, no compressed data
block anywhere, or a computed span beyond `bytes_used` all exit 2 with a message
(`SqfsError`). Reader cross-check: `cross-check.py` rebuilds every file's bytes from the parsed data
blocks and compares (path, sha256, size) with `tools/round-39/sqfs-list.py` (a reader sharing no code
with mine) — **12/12 images identical**, and `--verify-trees` compares each rebuilt payload with the
source tree — **0 problems** in all 13 images. Parser offsets are therefore not assumptions.

### 2.1 Why `0xFF`, and why a zero fill is a trap (`logs/probe-fills.log`)

`sasquatch` 4.5.1 is not a single-decompressor build: on a failed default decompressor it walks a
fallback chain and prints `Trying to decompress with lzo... lz4... xz... zstd... lzma...`. Measured
on the same target block of `t1-be-gzip` (2997+650) and `t1-le-xz` (3292+712), extractor run
directly (`probe-fills.py`, exit code + tree entries + whether the damaged file is all zeroes):

| fill | exit | verdict | damaged file | signal |
|---|---|---|---|---|
| `00` | **0** | **absorbed** | 3100 bytes, **all zeroes** | `Detected lzma-ddwrt compression` |
| `ff` | 1 | fails | 0 bytes | `FATAL ERROR: writer: failed to read/uncompress file …/readme.txt` |
| `a5` | 1 | fails | 0 bytes | same |
| `rand` | 1 | fails | 0 bytes | same |
| `inc` | 1 | fails | 0 bytes | same |
| `hdrs` (valid zlib header + garbage) | 1 | fails | 0 bytes | same |

So **`0x00` must never be used for this class**: the fallback chain "detects lzma-ddwrt" in the zero
block, emits a full-length block of zeroes, exits 0 and leaves the chunk `extraction_failed: false`
— the envelope then reads as a **clean** extraction with wrong content, not as a failure
(`logs/sasquatch-zero-fill-absorbed-t1-be-gzip.log` versus
`logs/sasquatch-clean-t1-be-gzip.log`, 53 vs 70 log lines, the extra lines being the chain).

### 2.2 Why the extractor fails at all: `-no-exit-code` does not suppress this path

unblob always appends `-no-exit-code` (`unblob/handlers/filesystem/squashfs.py:44-57`), and
`Command.extract` only reports failure on `returncode != 0`
(`unblob/extractors/command.py:59-70`). Measured: a data-block decompression failure reaches
sasquatch's `writer: failed to read/uncompress file` **FATAL** path, which exits 1 regardless of
`-no-exit-code`; the id-table failure (§4) does the same (`FATAL ERROR: File system corruption
detected`, exit 1). Consequences: (a) `extraction_failed`/`extractor-failure` is reachable for
these two damage classes only, (b) an exit-0 "damage" (§2.1 zeros) is invisible to REA.

---

## 3. Measurements

### 3.1 Recipe matrix — 3 fresh trees x gzip/xz x BE/LE (`tables/feature-table.md`)

Common feature vector of all 12 (identical apart from `handler`, the `-be` cell and the block span):

`operation=extract_firmware`, `provider.id=unblob`, `chunks[].extraction_failed=true`,
`extraction_gaps=[{kind:"extractor-failure", dependencies:[]}]`, `unpublished_entries=[]`,
`diagnostics[0].report.__typename__="ExtractCommandFailedReport"`, `len(files)=5`,
`published_bytes=26500`, `coverage=partial`.

| run | handler | `-be` | P | bytes | block span overwritten | damaged file |
|---|---|---|---|---|---|---|
| t1-be-gzip-partial | squashfs_v4_be | yes | 5 | 26500 | 2997+650 | readme.txt |
| t1-be-xz-partial | squashfs_v4_be | yes | 5 | 26500 | 3292+712 | readme.txt |
| t1-le-gzip-partial | squashfs_v4_le | no | 5 | 26500 | 2997+650 | readme.txt |
| t1-le-xz-partial | squashfs_v4_le | no | 5 | 26500 | 3292+712 | readme.txt |
| t2-be-gzip-partial | squashfs_v4_be | yes | 5 | 26500 | 2960+635 | readme.txt |
| t2-be-xz-partial | squashfs_v4_be | yes | 5 | 26500 | 3268+696 | readme.txt |
| t2-le-gzip-partial | squashfs_v4_le | no | 5 | 26500 | 2960+635 | readme.txt |
| t2-le-xz-partial | squashfs_v4_le | no | 5 | 26500 | 3268+696 | readme.txt |
| t3-be-gzip-partial | squashfs_v4_be | yes | 5 | 26500 | 2994+640 | readme.txt |
| t3-be-xz-partial | squashfs_v4_be | yes | 5 | 26500 | 3284+696 | readme.txt |
| t3-le-gzip-partial | squashfs_v4_le | no | 5 | 26500 | 2994+640 | readme.txt |
| t3-le-xz-partial | squashfs_v4_le | no | 5 | 26500 | 3284+696 | readme.txt |

Spans differ per tree and per compression, which is the point: nothing is hardcoded. Exact
diagnostic strings (from the envelopes, e.g. `envelopes/t1-be-gzip-partial.json`):

* BE: `sasquatch-v4be -be -no-exit-code -f -d <outdir> <inpath>`, `exit_code: 1`,
  stderr ends `FATAL ERROR: writer: failed to read/uncompress file …/firmware.bin_extract/readme.txt`
* LE: `sasquatch -le -no-exit-code -f -d <outdir> <inpath>`, `exit_code: 1`, same tail.

Content check against the source trees (REA-published sha256 vs `trees/tN/...`): the four files
before the damaged one are **byte-identical**; the damaged file is published as a **0-byte stub**
(`{'readme.txt', size 0}`), which is why `P=5` while `published_bytes=26500` (4 x real bytes).
A repeat run of the same carrier (`t1-be-gzip-partial-repeat`) yields an identical semantic
projection (handler list, `extraction_failed`, gap kinds, dependencies, per-file path/size/sha256,
diagnostic typenames). Rebuilding the carrier from the tree gives the same image
`sha256 b22c5213fca985f29c23a81f189256efadffebc922ce57d68575752c56d69bfe`, so the recipe is a pure
function of the clean image.

### 3.2 Edge carriers

| carrier | damage | P | bytes | note |
|---|---|---|---|---|
| `t1-be-gzip-firstblock` | first file's only compressed block | 5 | **0** | sasquatch created the whole tree before writing data, so `P` saturates at `n` |
| `t1-be-gzip-midblock` | `payload.bin` block 1 of 4 | 5 | 17596 | block 0 of that file survived; later files are stubs |
| `one-be-gzip-partial` | single-file tree (guard bypassed inline) | 1 | 4096 | class boundary: `P=1` is still `P>0` |
| `rawtail-be-gzip-partial` | tree whose last file is incompressible (stored-raw blocks) | 2 | 0 | the recipe **fell back** to `aaa.txt`, skipping the raw blocks |

`P` is therefore a **path-entry count** (the extractor pre-creates empty files for the whole
directory tree and then streams contents), not a survival count; `published_bytes` is the survival
measure (26500 / 17596 / 4096 / 0 in the four cases above). The class the claim needs
(`partial-body-failure`, `P>0`) is nevertheless stable: it only requires that the failure happen
**after** the tree is created, which any data-block damage does, even on the first file. The
damage-ordering rule in §2.4 is kept because it maximises `published_bytes` (real survivors rather
than stubs), which is what a triage row should trust.

### 3.3 Clean controls (corroborating that the damage, not the writer, is the cause)

`t1-be-gzip-clean`: `P=5`, `published_bytes=29600`, `coverage=complete`, `G=[]`, no diagnostics,
every published sha256 equal to the tree. `t3-be-xz-clean`: identical (so the round-39 D2 "xz
carriers are undecodable" defect is indeed fixed in `tools/round-39/gen-squashfs.py`: `COMP
xz=4`, real `.xz` container). `empty-be-gzip-clean` (one empty directory): `P=0`,
`published_bytes=0`, `coverage=complete`, `G=[]` — the "clean with zero files" shape R39-CL3 D2
required (`clean` must accept `published files = 0`).

---

## 4. The round-39 `body-extractor-failure` recipe: it never gives `P > 0`

Recipe as frozen in `tools/round-39/heldout-gen.py` (`corruption_zero_id_table`, §"corruptions"):
read `id_table_start` (u64 at superblock offset 48), read the 8-byte id-table index there to get the
id metadata block start, zero the block from there to `id_table_start`. Measured this wave:

| carrier | handler | `-be` | P | bytes | gap |
|---|---|---|---|---|---|
| t1-be-gzip-zero-id-table | squashfs_v4_be | yes | **0** | 0 | extractor-failure |
| t1-be-xz-zero-id-table | squashfs_v4_be | yes | **0** | 0 | extractor-failure |
| t1-le-gzip-zero-id-table | squashfs_v4_le | no | **0** | 0 | extractor-failure |
| t1-le-xz-zero-id-table | squashfs_v4_le | no | **0** | 0 | extractor-failure |
| t2-be-gzip-zero-id-table | squashfs_v4_be | yes | **0** | 0 | extractor-failure |
| t1-be-gzip-bad-minor (s_minor 4 -> 5) | squashfs_v4_be | yes | **0** | 0 | extractor-failure |

So the round-39 recipe gives `P=0` in **6/6** cases and can never produce the `P>0` class: sasquatch
reads the id table during filesystem init, **before** the directory tree is created (direct run:
`read_id_table: failed to read id table block` / `FATAL ERROR: File system corruption detected`,
exit 1, output tree empty). `bad-minor` fails even earlier, at header validation. This is the
discriminator the v2 table needs: same gap kind and same `dependencies` (`[]`), opposite `P`.

---

## 5. Envelope facts the v2 grammar depends on (all read from the saved envelopes)

| feature | path | measured value |
|---|---|---|
| operation | `data.operation` | `"extract_firmware"` in all 26 extract runs; two probe envelopes have no `data` at all |
| provider | `data.provider` | object `{"id":"unblob","name":"Unblob","version":"26.6.4"}` — the grammar's `provider` cell is `data.provider.id` = `unblob` (also present in the bare-`data` receipts, e.g. round-39 `c1/K1/after.json`) |
| handler | `data.normalized_result.chunks[].handler` | `squashfs_v4_be` / `squashfs_v4_le`; `[]` when no chunk matched |
| failed chunk | `…chunks[].extraction_failed` | `true` for all 23 failure runs, `false` for the 3 clean runs |
| gaps | `…extraction_gaps[].kind` / `.dependencies` | `extractor-failure` with `[]`; `missing-extractor-dependency` with `["sasquatch-v4be"]` / `["sasquatch"]` (round-39); `[]` when clean |
| unpublished | `…unpublished_entries[].kind` | `[]` in every run here |
| diagnostics | `…diagnostics[].report.__typename__` (+ `.command`, `.exit_code`, base64 `.stderr`) | `ExtractCommandFailedReport`; command strings as in §3.1; `MaliciousSymlinkRemoved` from round-39 receipts |
| files | `…files` | `len()` = P |
| survival | `…published_bytes`, `…coverage` | `26500`/`partial`, `29600`/`complete`, `0`/`partial` |

Exact grammar feature definitions were reused verbatim from `tools/round-39/sqfs-triage.py`
(`features`, `extractor_commands`, `match_set`, `rule_matches`) so v1 and v2 cannot drift on `H/G/D/
BE/SR/P`; `-be` is `n/a` when no command names a `sasquatch*` binary, else `yes` iff a token equals
`-be` (v1's token rule, which keeps `sasquatch -le …` at `no`).

---

## 6. The v2 grammar, implemented and scored

`artifacts/R40C2ReconPartial/sqfs-triage-v2-dev.py` is the L1 contract written as code —
marker `<!-- sqfs-triage-table v2 -->`, the table being the **first markdown table after that line
inside `## Queue-drain craft`**, 12-cell header in the drafted order, `<!-- sqfs-triage-actions:
tok1 tok2 ... -->` above it, first full match top-to-bottom, no match -> `(unclassified, none)`.
`--selftest` = **13/13** (`tables/v2-selftest.txt`): green parse, first-match order, domain guard on
`operation` and on `provider`, duplicate label -> exit 2, action outside the vocabulary -> exit 2,
malformed `published files`/set/`-be`/action cells -> exit 2, header mismatch -> exit 2, marker
absent -> exit 2, table outside the craft section -> exit 2, actions line missing or displaced ->
exit 2, bare `data` == full `{ok,data,meta}`, error envelope -> exit 2, `-be` yes/no/n-a.

`candidate-triage-v2.md` is the row set this recon supports (10 rows, `partial-body-failure`
between `avm-marker-be-dropped` and `body-extractor-failure`, both `files` cells exercising `>0` vs
`0`). Dev score over the 26 saved envelopes (`dev-score.py`, `tables/dev-score.txt`):

| table | score | what it shows |
|---|---|---|
| candidate | **26/26** | the P>0 row and the P=0 row coexist; LE/BE and gzip/xz all land correctly |
| A: v1 transcribed (no partial row, body row `files=0`) | 9/26 | the 17 partial envelopes fall to `unclassified` — R39-CL3 D1 / `R39W2C2TableReview.md:239` reproduced on new carriers |
| B: catch-all first row | 0/26 | one label for everything is worthless |
| C: label right, action wrong | 9/26 | the action column carries 17 of 26 decisions |
| D: best table + trailing `*` default row | 26/26 | **non-discriminating** as a kill control here (§7.3) |

---

## 7. Contract points that need a freeze decision

### 7.1 The `out-of-domain` class cannot be produced by a real REA run (freeze-blocking for C2)

The draft class is "a non-`extract_firmware` REA operation on a SquashFS carrier". Measured: every
non-extract operation REA 6.5.0 exposes for a raw file **rejects** a SquashFS image (and a tar that
contains it) with an error envelope and **no `data` object**:

```json
{"ok":false,"error":{"code":"target_unavailable","category":"unsupported_target",
  "message":"Cannot open artifact: unsupported binary format.", ...},
 "meta":{"command":"extract-artifact","duration":"151ms"}}
```

(`extract-artifact` on the raw image and on a tar, `analyze`, `inspect`: 6/6 runs, `logs/`
holds one of each shape.) Consequence: an interpreter that keeps v1's rule ("no
`normalized_result` -> exit 2") cannot classify such an envelope at all, so the class is
unattainable. Two workable options, both deterministic:

* **recommended**: the v2 envelope reader accepts `{ok:false, error:{…}, meta:{command:…}}` and maps
  it to features `OP = meta.command` (or `null`), `PV = null`, everything else empty — the domain
  guard then yields `unclassified` naturally, and the held-out carrier can be a real, reproducible
  run (no synthesis, no REA on a frozen carrier);
* alternative: the class carrier is a real `extract_firmware` envelope whose `data.operation` /
  `data.provider.id` the generator rewrites before the freeze; then the interpreter can stay strict,
  but the held-out evidence no longer comes from a REA run and the claim must say so.

The dev interpreter implements the **strict** reading today (error envelope -> exit 2, one selftest
case) so the L1 can flip one function (`envelope_data`) once the decision is made.

### 7.2 "directly above the table" must allow one blank line

A GFM table needs a blank line after an HTML-comment block, so `<!-- sqfs-triage-actions: … -->`
followed immediately by `| label | …` is fragile. Read it as "the nearest non-blank line above the
table header, with only blank lines in between"; any non-blank line in between is still exit 2.
Implemented that way; the dev table has the blank line and parses.

### 7.3 `none` must be in the action vocabulary, and control D is not a control

The no-match default is `(unclassified, none)`, so `none` has to be a declared token (the dev
interpreter exits 2 without it). Note also: appending `| unclassified | * | * | * | * | * | * | * |
* | none | … |` as a "best table + `*` default row" kill control scores **26/26** — identical to the
no-match default once every scored envelope already matches a real row. As a scored control it
proves nothing unless the held-out set contains an envelope that no row matches (or unless the
appended row carries a *different* label/action, which is then just control B).

### 7.4 Class construction constraints (for the round-40 held-out generator)

1. `partial-body-failure` **must** be built with data-block damage and a **non-zero fill**
   (§2.1: `0x00` is absorbed, exit 0, `extraction_failed=false`, i.e. it lands in `clean`).
2. `body-extractor-failure` keeps the round-39 id-table recipe — it is `P=0` by construction
   (§4), and `bad-minor` is a second, interchangeable recipe under that label.
3. `partial-body-failure` needs at least one regular file; with `n` files the outcome is `P=n`
   (pre-created tree) and `published_bytes` = the bytes written before the damaged file. Two or
   more files with at least one survivor is the shape worth freezing (the dev carriers give
   `P=5, published_bytes=26500`).
4. If the L1 wants "failure with content" separated from "failure with only stubs" (first-block
   damage gives `P=5, published_bytes=0`), the grammar needs `published_bytes > 0` or a
   `chunks[].extraction_failed` cell — the current `published files` cell cannot see the
   difference. Not required by the draft; recorded so the choice is deliberate.
5. `xz` carriers are safe again: the round-39 `gen-squashfs.py` writes real `.xz` containers with
   comp id 4, and both clean xz controls extract completely (§3.3). Raw-LZMA2 carriers (the
   round-39 D2 shape) would read as `partial-body-failure` (`extractor-failure`, `P>0`), so they
   must not be used to build `body-extractor-failure`.

---

## 8. Artifacts (all under `.ufo/waves/round-40/w1/artifacts/R40C2ReconPartial/`)

| path | contents |
|---|---|
| `sqfs-corrupt.py` | stdlib SquashFS 4.0 reader (superblock -> inode table -> directory table, both endiannesses, gzip/xz) + `corrupt_partial` (recipe) + `corruption_zero_id_table` / `bad-minor` / `bad-major` |
| `make-tree.py` | deterministic compressible tree builder (seed -> bytes) |
| `cross-check.py` | my payload reconstruction vs `tools/round-39/sqfs-list.py` (12/12 identical) |
| `probe-fills.py` | fill-pattern probe against the extractor directly |
| `feat.py` | envelope -> feature rows (`tables/feature-table.md`, `tables/features.json`) |
| `runrea.sh` | the one REA invocation template (fresh cwd + fresh outdir per run) |
| `build.sh` | exact reproduction of trees, images, damage, runs, tables (`sh -n` clean) |
| `sqfs-triage-v2-dev.py` | dev v2 interpreter + 13-case selftest |
| `candidate-triage-v2.md` | dev v2 table (10 rows, marker, actions line) |
| `dev-score.py`, `controls/*.md` | 26-envelope dev score and the four kill controls |
| `carriers/` | 37 images: 15 clean development images (12 matrix + `empty` + `one` + `rawtail`), 14 partial (`*-partial`), 6 body-failure (5 zero-id-table + bad-minor), 2 block-position specials (`firstblock`, `midblock`) |
| `envelopes/` | 28 REA envelopes, 2 of them the non-extract error shape |
| `trees/` | the six source trees (t1-t3, empty, one, rawtail) |
| `logs/` | sasquatch clean vs zero-fill-absorbed logs, fill probe log, capabilities, one error envelope |
| `MANIFEST.sha256` | sha256 of all 107 files |

Reproduction: `S=/fast/scratch/hyaku/kaidoku-r40/R40C2ReconPartial sh build.sh` (or with your own
`S`; the script creates its own trees, images and runs and never writes into the lane).

---

## 9. Risks

1. **A zero-fill partial recipe is silently a clean carrier** (§2.1). If the round-40 generator
   copies the "zero the block" idiom, `partial-body-failure` carriers will score as `clean` and the
   class will look satisfied while the table is never exercised. `PARTIAL_FILL` is fixed at `0xFF`
   and the probe script can be run as a pre-freeze check.
2. **P is a tree-entry count** (§3.2). Any assertion of the form "partial failure loses files" is
   wrong for sasquatch; use `published_bytes` if survival matters.
3. **The out-of-domain class has no real envelope today** (§7.1); without a decision the class is
   unattainable and the domain guard stays unexercised by held-out data.
4. **Control D proves nothing** as drafted (§7.3); replace it with an envelope that no row matches
   (e.g. a non-`unblob` provider with `extractor-failure`), or drop it.
5. The v2 scorer needs the *action* to be scored, not just the label: control C shows labels alone
   lose 17/26 decisions on this dev set.

[INFERENCE] marked items: the claim that `-no-exit-code` only suppresses the normal error path
(§2.2) rests on measured exit codes 1 for both FATAL paths and on the absence of a `-be`-related
exit-0 failure in 26 runs; I did not read sasquatch's source. The statement that sasquatch
pre-creates the tree (§3.2) is supported by `P=n` under first-block damage with
`published_bytes=0`; an alternative explanation (files created lazily but all before the first data
write) would produce the same measurements and the same recipe, so the choice does not affect the
recipe or the table. The provider object shape was read from `normalized_result`-bearing envelopes
only; no other REA provider appears in any extract-firmware envelope I produced.

Report: `.ufo/waves/round-40/w1/R40C2ReconPartial.md`
