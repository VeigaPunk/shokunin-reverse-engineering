# R42C2ReconLegacy — real REA envelopes for SquashFS v1–v3, arms (a)–(d), the v3 table's error, A1 delta

**Verdict: DEFECTS FOUND** — the draft's legacy rows are sound on clean/zero-file/dependency envelopes,
but four things it needs are not true of the inputs it names: (i) all 43 unblob v1–v3 fixtures hold **no
data block** (every body sits in the single fragment block), so the round-41 "zero a late compressed data
block" recipe cannot be built from them and the only partial those fixtures can make publishes **every file
as 0 bytes** yet still lands `partial-body-failure`; (ii) a damaged v3 image loses a whole file with **no gap
at all** (`clean`/`in-tree-symlink-metadata`); (iii) the dependency gap names **one** executable — the
resolved one — so a big-endian v1–v3 chunk lands on `dep-missing-le`/`install-extractor-le`; (iv) the A1 TRX
example's gap set is `{depth-limited, unknown-chunk-handler}`, not `{depth-limited}`. On the same 135
envelopes the round-41 v3 table is right **9/135**, and never right on a v1–v3-only envelope (123 →
`unclassified`, 3 → `no-squashfs-chunk`).

Seat `R42C2ReconLegacy`, lane `kaidoku-shokunin`, base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c`,
wave 1 (pre-freeze). Report path:
`.ufo/waves/round-42/w1/R42C2ReconLegacy.md`; artifacts:
`.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/` (`manifest.json`, `envelopes/`, `REBUILD.md`,
`compare_a1.tsv`, `v3-results.json`, `a1-out.jsonl`, `fixtures.tsv`, `tools/`).

## 0. What was run

135 REA `extract-firmware` runs, **every envelope `ok:true`**, driver exit code 0 on every run (the
fixture-matrix driver persisted per-run `rc.txt`; the arm drivers printed `rc=0` per run). Pin set
(measured, not assumed): rea-agents 6.5.0, unblob 26.6.4 (commit
`1fcc7a0a584a70a96c31f5a276c20944d199a089`, binary sha256
`0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`), sasquatch 4.5.1 (`sasquatch
-version` prints `unsquashfs version 4.5.1 (2022/03/17)`), sasquatch-v4be 4.5.1, unsquashfs 4.7.5 and
7z 26.04 (readers only), python3 3.14.8. Command shape, PATH arms, input pins and every derived-image
recipe are in `artifacts/R42C2ReconLegacy/REBUILD.md`; per-run features and both label transcriptions are in
`manifest.json` / `compare_a1.tsv`.

Composition: 86 fixture runs (43 unblob v1–v3 files × max_depth {3, 1}); 10 dependency runs (2 PATH arms ×
{v1 LE, v2 LE, v3 LE, v3 BE, v3 ddwrt BE}); 12 legacy-damage runs; 4 dev-image clean baselines (2 images ×
{3, 1}); 3 concat runs; 2 v4 bad-symlink runs (SR arm); 9 A1-class runs (tar ×2, residue tails ×4, whole
TRX ×2, plus one residue-at-depth-1); 3 A1 combo runs; 2 untrimmed atheros runs (real-world residue).
Inputs were only unblob 26.6.4 test fixtures (MIT) and OpenWrt Kamikaze 7.09 images (designated
DEVELOPMENT). **No C1 carrier candidate was executed or carved**; no extractor ran on any other published
image; `unsquashfs`/`7z` were used only to read the two development images.

## 1. Base matrix — all 43 v1–v3 fixtures, both depths

Every fixture extracts with plain `sasquatch` at default depth (3) → `G=∅`, `P>0` → A1 step 14 `clean`;
every fixture at `--max-depth 1` → `G={depth-limited}`, `coverage:"partial"` → A1 step 10 `depth-limited`.
That is 43/43 and 43/43, no exception.

| fixture family | runtime handler in `H` | bytes_used | P (depth 3) |
| --- | --- | --- | --- |
| `squashfs_v1` (be, le) | `squashfs_v1` | 176 | 3 |
| `squashfs_v2` (2.0/2.1 × be/le) | `squashfs_v2` | 196 | 4 |
| `squashfs_v2_nonstandard` (4) | `squashfs_v2_nonstandard` | 196 | 4 |
| `squashfs_v3` `.1kpad/.4kpad/.nopad` (6) | `squashfs_v3` | 320 | 4 |
| `squashfs_v3` `squashfs_v3_{be,le}.bin` | `squashfs_v3` | 255 / 258 | 2 |
| `squashfs_v3_ddwrt` `.1kpad/.4kpad/.nopad` (6) | `squashfs_v3_ddwrt` | 320 | 4 |
| `squashfs_v3_broadcom` `.1kpad/.4kpad/.nopad` (6) | `squashfs_v3_broadcom` | 320 | 4 |
| `squashfs_v3_broadcom/squashfs_v3_le.bin` | `squashfs_v3_broadcom` | 258 | 2 |
| `squashfs_v3_nonstandard` (8) | `squashfs_v3_nonstandard` | 320 | 4 |
| `squashfs_v3_adaptive/*.lzma.bin` (2) | **`squashfs_v3`** | 256 / 257 | 2 |

Measured subtleties that the C2 generator's "clean per runtime handler name" must respect (finding **D7**):

* `squashfs_v3_adaptive` is **not a handler name** in unblob 26.6.4 (`squashfs.py` defines only
  `squashfs_v1`, `_v2`, `_v2_nonstandard`, `_v3`, `_v3_ddwrt`, `_v3_broadcom`, `_v3_nonstandard`, and the
  v4 handlers). Both adaptive fixtures report `squashfs_v3`.
* `squashfs_v3/squashfs_v3_be.bin` and `squashfs_v3_broadcom/squashfs_v3_be.bin` are the **same bytes**
  (sha256 `4e9493d9…`) and both report `squashfs_v3`; `squashfs_v3/squashfs_v3_le.bin` and
  `squashfs_v3_ddwrt/squashfs_v3_le.bin` are the same bytes (`0161351c…`). So 43 fixture paths are 41
  distinct images. To reach `squashfs_v3_ddwrt` or `…_broadcom` the generator must use the
  `.1kpad/.4kpad/.nopad` files (ddwrt/broadcom BE) or `squashfs_v3_broadcom/squashfs_v3_le.bin` (broadcom
  LE); the plain `…_be.bin/.….le.bin` in those directories are standard-magic.
* The 7 reachable runtime names are exactly A1's set `L`, and all 7 are exercised here.

Depth semantics (needed for `declared_features`): at `--max-depth 1` a **single-chunk** run records exactly
one structural `depth-limited` gap whose `input_path` is `$output/firmware.bin_extract` (the extract root,
not a nested path) — measured on all 43 fixture runs, and on the tar run, so it is not squashfs-specific.
A nested case instead points at the nested extract dir
(`$output/firmware.bin_extract/32-1904672.trx_v1_extract`). `coverage` becomes `partial`.

## 2. Arm (a) — sasquatch unreachable

Two arms, `REA_UNBLOB_COMMAND` absolute, `$HOME/.local/bin` stripped from the child PATH:
**A1** both binaries absent; **A2** a scratch symlink puts only plain `sasquatch` back.

| run | H | G | D | BE | P |
| --- | --- | --- | --- | --- | --- |
| A1 v1 LE / v2 LE / v3 LE / v3 BE / v3 ddwrt BE | that handler | `missing-extractor-dependency` | `["sasquatch"]` | `n/a` | 0 |
| A1 v4 BE | `squashfs_v4_be` | `missing-extractor-dependency` | `["sasquatch-v4be"]` | `n/a` | 0 |
| A1 v4 LE | `squashfs_v4_le` | `missing-extractor-dependency` | `["sasquatch"]` | `n/a` | 0 |
| A2 v1/v2/v3 (both orders)/ddwrt/v4 LE | that handler | ∅ | ∅ | `n/a` | 3 / 4 / 4 / 4 / 2 / 2 |
| A2 v4 BE | `squashfs_v4_be` | `missing-extractor-dependency` | `["sasquatch-v4be"]` | `n/a` | 0 |

Three things this settles:

1. **`D` is a singleton naming the executable the chunk resolved to.** Mechanism (source, not inference):
   `SquashFSExtractor.get_dependencies()` returns both names (`squashfs.py:68-69`) but that method feeds only
   the CLI dependency listing; the error REA surfaces is raised inside the plain `Command` that
   `SquashFSExtractor.extract` builds, and `Command`'s report carries `[self._executable]`
   (`extractors/command.py:70-72`, `:101-102`). The diagnostic shape is
   `{input_path:"$input", stage:"squashfs_v3", missing_dependencies:["sasquatch"], report:{__typename__:
   "ExtractorDependencyNotFoundReport", dependencies:["sasquatch"], severity:"ERROR"}}` — **no
   `report.command`**, hence `BE=n/a`.
2. **A2 proves plain `sasquatch` is sufficient for v1–v3 and v4 LE**: with `sasquatch-v4be` absent,
   v1/v2/v3/ddwrt/v4-LE all extract fully (`G=∅`, files published). Only a v4 *BE* chunk needs v4be.
3. **Consequence for A1 step 4 (finding D2):** `dep-missing-le`/`install-extractor-le` fires for a
   **big-endian** v1–v3 chunk too (measured `dep_A1_squashfs_v3_be`, `dep_A1_squashfs_v3.be.nopad`). The
   dependency name is right (`sasquatch`); the token's word "le" is not. A1's note now states the fact, but
   the table's action text and any class name that says "le" must say *plain sasquatch, both byte orders*,
   and the held-out set should include one BE legacy dependency carrier or the row is only ever seen on LE.
   Step 4's first branch is reachable only for v4 BE (2 of 10 dependency envelopes).

`P=0` on these envelopes is correct and expected: a squashfs chunk that **is the whole input file** is not
re-published as a carved blob. When the chunk is a sub-range (see §7, combo), a failed chunk *is* published
as `<start>-<end>.<handler>` and `P` rises — this decided `declared_features` for the residue/dependency
combos (`combo_tailpat_dep_d3`: P=2 = `0-4096.squashfs_v3` + residue).

## 3. Arm (b) — zero-file damage

| run | image | damage | H | G | BE | P | A1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `dmg_V1_inode_last` | v3 dev LE | last inode metadata block (1057701+845+2 B) | `squashfs_v3` | `extractor-failure` | no | 0 | 7 `legacy-body-failure` |
| `dmg_V2_inode_table` | v3 dev LE | inode table 1055746..1058548 | `squashfs_v3` | `extractor-failure` | no | 0 | 7 |
| `dmg_V3_dir_last` | v3 dev LE | last directory metadata block | `squashfs_v3` | `extractor-failure` | no | 0 | 7 |
| `dmg_V6_frag_index` | v3 dev LE | fragment table index (8 B at 1061797) | `squashfs_v3` | `extractor-failure` | no | 0 | 7 |
| `dmg_Z1_v1_inode_table` | v1 fixture LE | bytes 71..128 | `squashfs_v1` | `extractor-failure` | no | 0 | 7 |
| `dmg_Z2_v2_inode_table` | v2 fixture LE | bytes 88..136 | `squashfs_v2` | `extractor-failure` | no | 0 | 7 |
| `dmg_Z3_v3ddwrt_inode_table` | v3 ddwrt BE fixture | bytes 144..203 | `squashfs_v3_ddwrt` | `extractor-failure` | **yes** | 0 | 7 |

Representative stderr (V1): `get_metadata: failed to read block` / `read_inode: failed to read inode
1057701:3297`; (V6): `read_fragment_table: failed to read fragment table block` / `FATAL ERROR: File system
corruption detected`; all with a recorded argv (`sasquatch -le …` or `sasquatch -be …`) and exit 1.

The recipe generalises, and the offsets differ by level: v1/v2 keep the 32-bit compatibility fields —
`inode_table_start` is `u32@20`, `directory_table_start` `u32@24` (measured: v1 fixture 71/128, v2 fixture
88/136); v3 uses the 64-bit `inode_table_start` `u64@87` / `directory_table_start` `u64@95` of the **packed**
119-byte superblock (packed offsets verified byte-for-byte against `unsquashfs -s`: `mkfs_time` 39,
`bytes_used` 63, `fragment_table_start` 103, `lookup_table_start` 111). On a v3 image the `_2` compatibility
fields are zero/unused, so a damage tool that reads `u32@20` will zero nothing — a real trap for the
generator. `tools/v3tool.py` implements both walks (and handles the `0x8000` uncompressed metadata header bit,
exercised by the ddwrt image).

**A1 ordering is exercised correctly here**: the ddwrt BE run has `BE=yes`, so step 6 (`avm-marker-be-dropped`)
correctly does **not** fire and step 7 owns it. That is the only envelope in the wave with `BE=yes` and a
legacy handler.

## 4. Arm (c) — partial damage: the fixtures cannot supply the round-41 recipe

**Finding D3 (high).** No v1–v3 fixture has a data block. Measured `bytes_used` 176–320 B, `block_size`
65536 or 131072, `fragments` = 1, and every regular file's body is fragment-resident (e.g. the v3 nopad
image: 320 B total, superblock 119 B, data area 119..144 = the single fragment block, inode table at 144).
So `MAX_DAMAGED_BLOCK`/holdout-gen-v3's "zero the last compressed data block of the last-extracted file"
has **no target**. The only damage inside the data area is the fragment block:

* `dmg_F1_v3_fixture_fragment` (zero bytes 119..144 of `squashfs_v3.le.nopad.bin`): `extractor-failure`,
  `BE=no`, **P=4**, and all four published files are **0 bytes** (sha256 `e3b0c442…`). A1 step 5 →
  `partial-body-failure`/`salvage-partial` — a "salvage" label on an envelope where every published body is
  empty and the baseline body was 7 bytes. A lookup/label control cannot tell this from a genuine salvage.
* A real partial needs a larger legacy image. Measured on the OpenWrt 7.09 brcm47xx v3 image
  (`wrt54gs-v3.squashfs`, 1 061 809 B, sha256 `13a4f1b8…`, LZMA-patched squashfs 3.0):
  * `dmg_V4_data_tail` — zero **512 B at `inode_table_start-512`** = 1 055 234..1 055 746 →
    `extractor-failure` + `unpublished-entry`, `BE=no`, **P=155**; sasquatch log
    `writer: failed to read/uncompress file …/usr/share/udhcpc/default.script`, `FATAL ERROR`, exit 1.
  * rerun in a fresh directory (`dmg_V4b_data_tail`): **identical projection** (155 files, 164 gaps, 163
    unpublished entries, same paths/sizes/sha256) and a **different `evidence_id`** — `evidence_id` hashes
    `parameters`, i.e. the scratch paths. C2 must not bind on `evidence_id` for dev-arm envelopes.
  * same damage at `--max-depth 1` (`dmg_V4d1_data_tail`): `G={depth-limited, extractor-failure,
    unpublished-entry}`, P=155 → step 5 still wins over step 10. A1's partial-before-depth order confirmed.

**Finding D4 (high, calibration): silent body loss with no gap.** Zero 512 B at
`inode_table_start-65536-512` (989 698..990 210, `dmg_V5_data_tail2`): `G={unpublished-entry}` only,
`P=155` against the 156-file baseline — `usr/sbin/pppd` is simply **absent**, no `extractor-failure`, no
diagnostic. A1 → step 13 `in-tree-symlink-metadata` (on an image without symlinks the same envelope would be
step 14 `clean`). The precedence has no way to see it, and no REA envelope carries it: `P` counts published
entries, not verified bodies. If row 5 (`salvage-partial`) and row 14 (`clean`) are to mean anything about
bodies, the class definitions must say that C2 envelopes are triaged on *observed gaps + publish count* only,
and that body correctness is C1's oracle job.

## 5. Arm (d) — v3 concatenated after v4 (two chunks)

| run | input | sqfs chunks (offset..end) | G | P | A1 |
| --- | --- | --- | --- | --- | --- |
| `concat_C1` | v4 LE fixture + v3 LE dev image | `squashfs_v4_le` 0..4096, `squashfs_v3` 4096..1065905 | `unpublished-entry` | 158 | 13 `in-tree-symlink-metadata` |
| `concat_C1_d1` | same | same | `depth-limited, unpublished-entry` | 158 | 10 `depth-limited` |
| `concat_C2` | v4 LE fixture + v3 BE trimmed image | `squashfs_v4_le` 0..4096, `squashfs_v3` 4096..1003520 | `unpublished-entry` | 149 | 13 |

Both handlers are named, both chunks extract, `F={squashfs_v4_le, squashfs_v3}`, `L={squashfs_v3}`. At
default depth REA also descends into the extracted legacy rootfs and adds 58 (C1) / 54 (C2) non-squashfs
chunks (`elf32`), which `F` correctly ignores.

**Finding D10 (low, but a table-scope statement is needed):** the pair is per *envelope*, so a clean v4 chunk
plus a v3 chunk with symlink gaps reports `in-tree-symlink-metadata` for the whole envelope; a v4 chunk that
fails and a clean v3 chunk would report the failure. The v4 table should state that the pair is envelope-level
and precedence-ordered (the first matching row names the envelope), or the combos will score a pair that hides
the other chunk's disposition.

## 6. Where the round-41 v3 table is wrong (same 135 envelopes)

Command (as the wave asks):
`python3 -I -B tools/round-41/sqfs-triage-v3.py --skill <(git show c4a38ea2…:SKILL.md) --json runs/*/envelope.json`
(the base `SKILL.md` was materialised from git first; the interpreter reads the table under
`<!-- sqfs-triage-table v3 -->` at `SKILL.md:434-449`).

Result: **9/135 agree** with the A1 transcription, and **all 9 are envelopes that contain a
`squashfs_v4*` chunk** (2 concat runs, 4 v4 dependency runs, 2 bad-symlink runs, 1 concat-at-depth-1).
On the 126 envelopes with no v4 handler the v3 table is wrong 126/126:

| A1 label (truth) | n | v3 label |
| --- | --- | --- |
| `clean` | 51 | 50 `unclassified`, 1 `clean` |
| `depth-limited` | 48 | 46 `unclassified`, 2 `depth-limited` |
| `unknown-residue` | 6 | 6 `unclassified` |
| `in-tree-symlink-metadata` | 6 | 3 `unclassified`, 3 `in-tree-symlink-metadata` |
| `dep-missing-le` | 8 | 5 `unclassified`, 3 `dep-missing-le` |
| `dep-missing-be` | 2 | 2 `dep-missing-be` |
| `legacy-body-failure` | 7 | 7 `unclassified` |
| `partial-body-failure` | 4 | 4 `unclassified` |
| `container-depth-limited` | 3 | 3 `no-squashfs-chunk` |

**Finding D1 — the routed defect R41-CL4's wording is wrong (it matters for CTL-C2-0b).** The v3 table's
`no-squashfs-chunk` row has handler cell `none`, so it only matches when **no** squashfs chunk exists; a
v1–v3 chunk matches no row at all and falls through to the interpreter's default `unclassified`
(`row:null, rule:null`). Measured: 123 `unclassified` vs 3 `no-squashfs-chunk`, and the three
`no-squashfs-chunk` runs are exactly the F=∅ container runs (`a1_tar_d1`, `a1_trx_d1`, `combo_tar_dep_d1`).
So `corpus/lessons/round-41.md`'s "sends every SquashFS v1–v3 chunk to `no-squashfs-chunk`" should read
"falls through to `unclassified`". The draft's hedge ("`no-squashfs-chunk` or `unclassified`") is right, and
CTL-C2-0b will score 0 on legacy envelopes — but its *labelled* output is `unclassified`.

## 7. A1 delta (new decisions, measured)

### 7.1 `container-depth-limited` (step 2)

| input | depth | H | G | P | A1 |
| --- | --- | --- | --- | --- | --- |
| `tar_v3_le.tar` (tar containing `squashfs_v3_le.bin`) | 1 | `tar` | `depth-limited` | 1 | 2 `container-depth-limited` ✓ |
| same | 3 | `tar`, `squashfs_v3` | ∅ | 3 | 14 `clean` ✓ (the inner chunk is carved and extracted) |
| `openwrt-wrt54gs-2.6-squashfs.bin` (whole 7.09 TRX) | 1 | `trx_v1` | `depth-limited, unknown-chunk-handler` | 4 | 2 `container-depth-limited` |
| same | 3 | `elf32, gzip, lzma, padding, squashfs_v3, trx_v1` | `depth-limited, unknown-chunk-handler, unpublished-entry` | 167 | 9 `unknown-residue` |

**Finding D5:** the A1 text's TRX example (`H={trx_v1}`, `G={depth-limited}`) is not what REA produces: the
TRX has a 32-byte unclaimed prefix, published as `0-32.unknown`, so `unknown-chunk-handler ∈ G`. The pair is
unaffected (step 2 precedes step 9), but `declared_features` for that named class must carry
`unknown-chunk-handler` or `observed_features_match_declared` fails. The tar variant *is* exactly
`G={depth-limited}`.

### 7.2 `unknown-residue` (step 9) — the tail must be non-uniform

| tail after `squashfs_v3.le.4kpad.bin` | H | G | P | A1 |
| --- | --- | --- | --- | --- |
| 256 × `0xAA` (uniform fill) | `padding, squashfs_v3` | ∅ | 5 (`4096-4352.padding`) | 14 `clean` (**not** the class) |
| 256 B `"ABCD"` repeated | `squashfs_v3` | `unknown-chunk-handler` | 5 (`4096-4352.unknown`) | 9 `unknown-residue` ✓ |
| 256 B deterministic non-uniform bytes | `squashfs_v3` | `unknown-chunk-handler` | 5 | 9 ✓ |
| 244 B ASCII text | `squashfs_v3` | `unknown-chunk-handler` | 5 (`4096-4340.unknown`) | 9 ✓ |
| untrimmed atheros dev image (180 224 trailing bytes) | `elf32, squashfs_v3` / `squashfs_v3` | `unknown-chunk-handler` (+`depth-limited` at d1) | 147 | 9 ✓ |

**Finding D6:** a uniform tail is claimed by unblob's `padding` handler — `H` gains `padding`, a
`<range>.padding` file is published, and the envelope is `clean`. The generator's residue class must use
non-uniform bytes (and should pin them, not draw them, so the class stays byte-identical).

Also note `P` includes the residue artifact (`<range>.unknown`) and any `padding` artifact. Any counter that
compares published files against a filesystem oracle must exclude `<start>-<end>.(unknown|padding|squashfs_*)`
artefacts (finding **D9**, relevant to C1 too).

### 7.3 step ordering and combos

| combo (two factors) | H | G | D | P | A1 |
| --- | --- | --- | --- | --- | --- |
| residue (pattern tail) + unreachable extractor, depth 3 | `squashfs_v3` | `missing-extractor-dependency, unknown-chunk-handler` | `sasquatch` | 2 | 4 `dep-missing-le` (step 4 before 9) ✓ |
| tar + unreachable extractor, depth 1 | `tar` | `depth-limited` | ∅ | 1 | 2 `container-depth-limited` |
| tar + unreachable extractor, depth 3 | `tar, squashfs_v3` | `missing-extractor-dependency` | `sasquatch` | 1 | 4 `dep-missing-le` ✓ |
| residue + depth 1 | `padding, squashfs_v3` | `depth-limited` | ∅ | 5 | 10 `depth-limited` (step 9 not matched) |
| partial + depth 1 | `squashfs_v3` | `depth-limited, extractor-failure, unpublished-entry` | ∅ | 155 | 5 `partial-body-failure` (5 before 10) ✓ |
| residue + depth 3 | `squashfs_v3` | `unknown-chunk-handler` | ∅ | 5 | 9 `unknown-residue` (9 before 10) ✓ |
| TRX d3 (residue + depth + links) | … | `depth-limited, unknown-chunk-handler, unpublished-entry` | ∅ | 167 | 9 ✓ |

**Finding D8 (combo factor that does not materialise):** a container wrap at `--max-depth 1` with the
extractor unreachable produces **no dependency gap at all** — the inner squashfs is never carved, so unblob
never asks for sasquatch (`combo_tar_dep_d1`: `G={depth-limited}`). A combo that "draws dependency
unreachable + container wrap" at `max_depth 1` therefore has only one observable factor, which weakens
`combo_unseen_majority` accounting; the generator should pair that factor set with `max_depth ≥ 2` (or declare
it as a one-factor draw).

**A1 limits confirmed:** no v1–v3 fixture envelope contains a symlink, device or any non-regular entry
(`unpublished_entries` empty in all 86 fixture runs; zero `unpublished-entry` gaps), so rows 11–13 are
unreachable on a legacy chunk — the A1 text is right. Legacy clean/damage classes at `max_depth 3` are right
too: every single-chunk run at depth 1 carries `depth-limited` (43/43), so a depth-1 "clean" class is
impossible.

## 8. Defects and risks for the freeze (ranked)

1. **D1** R41-CL4's wording (`no-squashfs-chunk`) is wrong; measured label is `unclassified` (123 vs 3).
   Only affects narrative + CTL-C2-0b expectation, not the v4 table.
2. **D2** `dep-missing-le`/`install-extractor-le` owns **every** BE v1–v3 dependency envelope (D is the
   resolved singleton). Rename or scope the token; include a BE legacy dependency carrier.
3. **D3** The named legacy classes cannot get a genuine partial from the unblob fixtures (no data blocks);
   the fixture fragment-zero recipe lands `salvage-partial` with **all bodies 0 bytes**. Use the pinned 7.09
   dev image (`zero 512 B at inode_table_start-512`, P=155) or state the class as "publish-count partial".
4. **D4** Silent body loss has no gap (`P` drops, `G=∅`) and is labelled `clean`/`in-tree-symlink-metadata`.
   State that the v4 labels triage gaps/publish counts, not body correctness.
5. **D5** The A1 TRX example's `G` omits `unknown-chunk-handler`; `declared_features` must include it.
6. **D6** `unknown-residue` requires a **non-uniform** tail; a uniform tail becomes a `padding` chunk and
   lands `clean`.
7. **D7** `squashfs_v3_adaptive` is not a handler name (→ `squashfs_v3`); two fixture paths are byte-identical
   across families. "clean per runtime handler name" must pin the right file; 43 paths = 41 images = 7 names.
8. **D8** container + unreachable extractor at depth 1 yields one factor, not two.
9. **D9** `<start>-<end>.{unknown,padding,squashfs_*}` artefacts are published files; oracle comparisons must
   exclude them (C1 rule and C2 `P` semantics).
10. **D10** The pair is envelope-level; state the scope, or combos with heterogeneous chunks hide one side.

## 9. Limits of this wave

* Development inputs only (unblob MIT fixtures + OpenWrt Kamikaze 7.09, designated development). No C1
  carrier candidate was run through any extractor and nothing was carved out of a published image; the
  `7.09` dev images were read only with `unsquashfs -s` before the REA runs.
* No v3 writer exists in the lane, so the partial/zero-file recipes here are *byte-range* damage on pinned
  images, not synthesized carriers. Byte-identical regeneration requires the pinned inputs and the recipes
  in `REBUILD.md` (all derived inputs carry their sha256 in `manifest.json`).
* `unblob.log`, REA staging, clones and every extraction root lived under
  `/fast/scratch/hyaku/kaidoku-r42/R42C2ReconLegacy` and were removed at the end; envelopes keep the scratch
  paths they were run with (that is why `evidence_id` is not reproducible across directories).
* Envelopes above 256 KiB are manifest-only (9 of 135); `REBUILD.md` gives their input pins and commands.
* Tool installs: **none**. Nothing in `~/.local/bin` or any PATH directory was written, moved or removed.
* The A1 transcription (`tools/a1-label.py`) and the earlier draft transcription (`tools/label_v4.py`) are
  transcriptions of claim text, not the freeze evaluator; `[INFERENCE]` where they read a step the text leaves
  ambiguous (only steps 6/7 needed the HF fallback, which A1 defines explicitly).
* Nothing was committed; lane VCS untouched; scratch removed. Files changed: this report and
  `.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/` only.
