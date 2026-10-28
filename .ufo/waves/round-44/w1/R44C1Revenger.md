# R44C1Revenger — unblob 26.6.4 v1/v2 handler → REA 6.5.0 derivation binding

Seat `R44C1Revenger` (revenger, wave 1). Claim under test: R44-C1 in
`plans/round-44-claims.md`. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Base at dispatch `c29360e3ba5381a5ab69e372d0d9577970f85018`. The L1 moved the round-44 tree
mid-seat: `3b0fcaa9` (frozen `tools/round-44/carriers.json` + S138 `__output__` trees), then
`f18bdfb9` (**+2 carriers: `squashfs_v2.1` le/be, 6 total**), then `9a8de923` (wave-1 receipts
sweep). HEAD when the last probes ran was `9a8de923053978342fdba6ce047e1cca4eda9dd2`; no lane
file was modified by this seat. The frozen carrier set is therefore **six**, not the four named in
this seat's brief — the two additions are covered below. Machine-readable probe record:
`.ufo/waves/round-44/w1/R44C1Revenger/probes.json` (`carriers_json_count: 6`,
`claim_text_target: 4`). Scratch:
`/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Revenger/`.

## Verdict (up front)

1. **The handler binding is exact and unambiguous.** For each of the **six** frozen carriers, unblob
   26.6.4 emits exactly one `ChunkReport` covering the whole 4096-byte file, with
   `handler_name` `squashfs_v1` (v1) or `squashfs_v2` (v2.0 and v2.1 alike), and REA 6.5.0 copies
   that string verbatim into `derivations[].handler` on the single
   `$input → $output/firmware.bin_extract` edge. Measured, not inferred (probes below).
2. **No v3/v4 collision exists under per-carrier EXACT equality.** The ten v1–v4 handler patterns
   are pairwise disjoint on these bytes: a full pattern scan of all six carriers at every offset
   matches only the carrier's own handler. The only prefix hazard in the whole family is
   `squashfs_v2` ⊂ `squashfs_v2_nonstandard` (and `squashfs_v3` ⊂ `squashfs_v3_{ddwrt,broadcom,nonstandard}`);
   the nonstandard handlers use different magics (`sqlz`/`zlqs`) and can never match these bytes.
3. **The extractor is `sasquatch` 4.5.1, never `unsquashfs`.** unblob's `SquashFSExtractor`
   hardcodes `EXECUTABLE = "sasquatch"` and appends exactly one endianness flag (`-be` for BE,
   `-le` for LE) plus `-no-exit-code -f -d {outdir} {inpath}`. `-da` is **never** passed by
   unblob; in sasquatch it is `-data-queue <size>` (an argument-taking memory knob). See §5.
4. **Three pre-freeze blockers, all in the already-committed round-44 tables.**
   - **Scope mismatch: claim text vs `carriers.json`.** `plans/round-44-claims.md` still lists four
     carriers and freezes `carriers_matched == 4` (lines 88, 108) with "bytes already committed
     under `corpus/evidence/round-42/c2/fixtures/` … `tools/round-42/fixtures.json` pins". The
     committed `tools/round-44/carriers.json` now has **six** entries: the four plus `v21le`/`v21be`
     (`squashfs_v2.1_le/be`, bytes at `corpus/evidence/round-44/carriers/`, handler `squashfs_v2`,
     `s_minor 1`). `tools/round-42/fixtures.json` has **no** v2.1 rows (its id list ends at v3ns),
     and the S138 oracle manifest records no `__input__` fetch (0 occurrences), so the two added
     carriers currently rest on `carriers.json`'s sha256 alone. I verified those bytes are
     byte-identical to the upstream media-LFS inputs
     (`…/squashfs_v2/{little,big}_endian/__input__/squashfs_v2.1_{le,be}.bin`,
     sha256 `6b6cd2fd…f253a` / `c0140bac…f35db`) — but the freeze must either amend the claim to
     six carriers (and `carriers_matched == 6`) or drop the two rows, and should pin the input
     URL+sha in a receipt. A reader of the claim as written scores 4; the frozen table offers 6.
   - `superblock_layout.bytes_used_offset = 40, len 8` and
     `compression_offset = 20, len 2` are **v3 offsets**. The v1/v2 superblock is a 32-byte
     packed struct with `bytes_used` a u32 at offset **8** and **no compression field at all**.
     A counter written to the frozen layout reads `inode_table_start_2` as "compression" and data
     bytes as `bytes_used`.
   - R44-C1's predicate text says the superblock probe checks "…/endianness/**compression**".
     v1/v2 store no compression id (zlib is the only v1/v2 codec; the format cannot express a
     choice). `file`'s "compressed/uncompressed" word is a libmagic rendering, not a format
     field: it prints `uncompressed` for **both** BE carriers and `compressed` for **both** LE
     carriers, i.e. it flips with byte order on these very fixtures. Freezing it as a
     superblock read is unfalsifiable; freeze it as the format constant `gzip` and verify it by
     extraction (the oracle + rerun already do), or drop the term.

Nothing here widens R44-C1. Items 1–3 confirm the claim's binding premise; item 4 is the set of
corrections the freeze must absorb before the L1 freezes bytes.

## 1. Reconstructed contract (the chain, with source anchors)

```
plans/round-44-claims.md R44-C1
  └─ tools/round-44/c1-run.sh (L1 only)  rea-agents@6.5.0 extract-firmware --format json --full-output
       └─ REA copies the selected bytes to <tmp>/firmware.bin        FirmwareFiles.js:37 (`join(root,"firmware.bin")`)
       └─ REA runs unblob 26.6.4                                      FirmwareProvider.js:228-241
            --process-num 1 --depth <max_depth> --randomness-depth 0
            --report <json> --log <log> --extract-dir <tmp>/extracted <tmp>/firmware.bin
            └─ unblob detects the largest chunk(s)                     processing.py
                 whole-file single chunk → extract into
                 `get_extract_dir_for(path)` = `<name>_extract`        processing.py:561-568, 125-127
                 several chunks → carve `<start>-<end>.<handler.NAME>`
                 and extract into `<…>_extract`                        extractor.py:130-135
                 └─ SquashFSExtractor(argv)                            squashfs.py:24-69
                      `sasquatch [-be|-le] -no-exit-code -f -d {outdir} {inpath}`
       └─ normalizeUnblobReport → logical paths                        FirmwareReports.js:145
            `chunks[].handler = ChunkReport.handler_name`              FirmwareReports.js:289-300
            `derivations[].handler` = MultiFileReport/FileReport
              handler_name recorded per [parent, child blob id]        FirmwareReports.js:158-163, 312-313
            child path = `$output/firmware.bin_extract`                FirmwareFiles.js:191-202
```

Handler strings are unblob's `Handler.NAME`, not the doc name: `models.py:202`
(`Chunk.as_report`) and `models.py:267` (`MultiFile.as_report`) both set
`handler_name=self.handler.NAME`; the `NAME` values are `squashfs_v1` / `squashfs_v2`
(`squashfs.py:102,159`). REA does not rewrite them (`FirmwareProvider.js:141` picks the engine
name `unblob`; handler strings pass through `addBlobOrigin(..., {handler: parsed.handler_name})`).

**Emitted shape for a whole-file chunk (all six carriers):**

```
chunks:      1 entry, input_path "$input", range {0, 4096}, handler "squashfs_v1"|"squashfs_v2",
             extraction_failed false
derivations: 1 edge with a non-null handler:
             {parent_path "$input", child_path "$output/firmware.bin_extract",
              provider_blob_id "<id>:1", handler "<carrier handler>",
              parent_file_range {offset 0, length 4096}}
             plus one edge per published member with handler null
             (e.g. {$output/firmware.bin_extract → $output/firmware.bin_extract/apple1.txt, handler null})
```

The null-handler member edges matter for the port: `derivations[].handler == expected` selects the
one root edge; a rule that required *every* edge to name the handler would fail. The round-42
helper already does the right thing: `squashfs_roots()` filters by exact handler equality
(`tools/round-42/c1-counter.py:1465-1494`), and `subject_root()` fails closed on ambiguity
(`:1495-1520`).

## 2. Per-carrier binding (required table)

All six: extract root is the whole-file chunk root, handler is the exact unblob `NAME`, and the
endianness flag is the only argv difference.

| carrier | handler | root_example | flag_set | collision_risk |
|---|---|---|---|---|
| `v1le` (`v1-le--squashfs_v1.0_le.bin`, sha256 `b45925fa…23e71`) | `squashfs_v1` | `$output/firmware.bin_extract` | `sasquatch -le -no-exit-code -f -d {outdir} {inpath}` | none under exact equality: `squashfs_v1` is not a prefix of, nor prefixed by, any other squashfs handler; pattern disjoint from v2/v2ns/v3/v3*/v4* |
| `v1be` (`v1-be--squashfs_v1.0_be.bin`, sha256 `529e1077…631e6`) | `squashfs_v1` | `$output/firmware.bin_extract` | `sasquatch -be -no-exit-code -f -d {outdir} {inpath}` | none (same) |
| `v2le` (`v2-le--squashfs_v2.0_le.bin`, sha256 `7c62dbe3…4f124`) | `squashfs_v2` | `$output/firmware.bin_extract` | `sasquatch -le -no-exit-code -f -d {outdir} {inpath}` | **exact equality: none.** Prefix-only hazard: `"squashfs_v2_nonstandard".startswith("squashfs_v2")`; that handler needs magic `zlqs`/`sqlz` + major 2 and these bytes do not match it. v3/v4 cannot match (major differs). |
| `v2be` (`v2-be--squashfs_v2.0_be.bin`, sha256 `79c0f388…2dfcc0`) | `squashfs_v2` | `$output/firmware.bin_extract` | `sasquatch -be -no-exit-code -f -d {outdir} {inpath}` | same as `v2le` |
| `v21le` (**L1-added** `squashfs_v2.1_le.bin`, sha256 `6b6cd2fd…f253a`, `s_minor 1`) | `squashfs_v2` | `$output/firmware.bin_extract` | `sasquatch -le -no-exit-code -f -d {outdir} {inpath}` | same as `v2le`; note the v2 handler pattern checks `s_major` only, so **`s_minor` does not change the emitted handler** — v2.0 and v2.1 both bind `squashfs_v2` |
| `v21be` (**L1-added** `squashfs_v2.1_be.bin`, sha256 `c0140bac…f35db`, `s_minor 1`) | `squashfs_v2` | `$output/firmware.bin_extract` | `sasquatch -be -no-exit-code -f -d {outdir} {inpath}` | same as `v21le` |

`root_example` assumes the carriers stay whole-file single-chunk images (they do — §3). If a
carrier ever gained a second chunk, unblob would carve and the root would become
`$output/firmware.bin_extract/<start>-<end>.<handler>_extract` (observed in the round-42 dev arm,
`C17`/`C18`/`H54`), and `carriers.json` would need `oracle_root` (stored **without** the
`$output/` prefix — `subject_root` compares against `strip_output(child_path)`,
`tools/round-42/c1-counter.py:1495-1520`). For all six, do **not** freeze `oracle_root`: the
single-root rule is the stronger check.

## 3. Observed handler detection (unblob 26.6.4, chunk-only pass)

Method: `unblob -s -p 1` (`--skip-extraction`) on a scratch copy named `firmware.bin`, report to
JSON. Exit 0 for all six. Each report contains exactly one `ChunkReport`:

| carrier | chunk | report sha256 |
|---|---|---|
| `v1le` | `squashfs_v1` 0–4096, encrypted=false | `33c8f2d82a4fbf5c8cd2d2cd14b79d8d88503393c1c09207bb4a6dc900b87747` |
| `v1be` | `squashfs_v1` 0–4096, encrypted=false | `37f1f01f6103304d13dbab5e438d79fb88528bebf02f15179091552954965bde` |
| `v2le` | `squashfs_v2` 0–4096, encrypted=false | `c10bd1ac1e73ed97b15b163e5edb27f86748a0587f23fddf268c004d351f3a91` |
| `v2be` | `squashfs_v2` 0–4096, encrypted=false | `7558a33e0a98a9a10dc5c36ff118b6f4b265c7c14526570342b71441f0769aa8` |
| `v21le` | `squashfs_v2` 0–4096, encrypted=false | `0b744b44f36b6b8248b3853ad9540dba45381cabbad3d44dfd2805ca88c53be5` |
| `v21be` | `squashfs_v2` 0–4096, encrypted=false | `9c2f1ec35b6ab0122953966b0d77bcf0c9401c3448e2d39dde2b7d3777c38bda` |

No `UnknownChunkReport`, no padding chunk, no second chunk — so `is_whole_file_chunk` is true for
each carrier (`processing.py:561`) and the root is `<name>_extract`.

**Pattern-disjointness scan** (all ten unblob squashfs patterns transcribed from
`squashfs.py:104-198,247-597`, scanned at every byte offset of every fixture): each fixture matched
exactly one handler at offset 0 and nothing else anywhere. Verified superblock fields
(endianness-aware):

| carrier | magic | s_major | s_minor | bytes_used (u32@8) | inode_table (u32@20) | dir_table (u32@24) |
|---|---|---|---|---|---|---|
| `v1le` | `hsqs` | 1 | 0 | 176 | 71 | 128 |
| `v1be` | `sqsh` | 1 | 0 | 177 | 71 | 129 |
| `v2le` | `hsqs` | 2 | 0 | 196 | 88 | 136 |
| `v2be` | `sqsh` | 2 | 0 | 201 | 88 | 138 |
| `v21le` | `hsqs` | 2 | **1** | 196 | 88 | 136 |
| `v21be` | `sqsh` | 2 | **1** | 201 | 88 | 138 |

`bytes_used ≤ 4096`, `32 ≤ inode_table < dir_table ≤ bytes_used` holds for all six (the counter's
sanity clause is satisfiable and true here). v2.0 and v2.1 differ in exactly **two bytes** —
`s_minor` (0→1) and one body byte at image index 39 (LE) / 42 (BE) — and extract to the same
member set; the unblob v2 pattern does not read `s_minor`, so the handler string cannot
distinguish v2.0 from v2.1.

## 4. Collision analysis under per-carrier EXACT equality

- **v1/v2 → v3/v4: impossible.** Every handler pattern encodes `(4-byte magic, 24-byte gap,
  2-byte s_major)` (`squashfs.py:104-122,161-198,247-263,318-340,363-387,409-432,454-511,513-525,548-575`).
  v1 requires `01 00`/`00 01` at offsets 28–29, v2 `02 00`/`00 02`, v3 `03 00`/`00 03`, v4
  `04 00`/`00 04`. A v1/v2 image cannot satisfy a v3/v4 pattern; the scan confirms the converse.
- **v2 → v2_nonstandard: cannot happen, but the string relationship is the one real prefix trap.**
  `squashfs_v2` is a strict prefix of `squashfs_v2_nonstandard`; the two handlers use disjoint
  magics (`hsqs/sqsh` vs `zlqs/sqlz`, `squashfs.py:206-238`). A counter using
  `startswith('squashfs_v2')` would still not see v2ns on these bytes (unblob emits `squashfs_v2`),
  but the rule is unsound in principle and would silently accept a v2ns carrier if one were added
  later. Keep exact equality, as the claim requires.
- **v2.0 vs v2.1 is not a handler distinction.** `SquashFSv2Handler.PATTERNS` matches magic +
  `s_major == 2` only (`squashfs.py:161-198`); `s_minor` is never matched. Both L1-added v2.1
  carriers therefore emit `squashfs_v2`, exactly like the v2.0 carriers, and their extracted
  member sets are byte-identical to the v2.0 sets. Per-carrier identity rests on the carrier
  sha256 (and the receipt's subject digest), not on the handler string or the minor; a counter
  that assumed `s_minor == 0` for every `squashfs_v2` carrier would reject v2.1.
- **A v3/v4 handler *can* appear in the same receipt** if a carrier were wrapped with a second
  image (round-42 dev `C17`, `C18`, `H54`). Exact equality on `derivations[].handler` plus
  `subject_root`'s single-root rule excludes it; `chunk_handlers(env)`
  (round-42 `c1-counter.py:1625-1627`) must **not** be used as the binding, because it returns
  every chunk's handler including the foreign one.
- **`handler` may be null** on member edges inside the extraction (H42). Bind on the edge whose
  `child_path` is the root (`firmware.bin_extract`), never on "the first derivation".

## 5. Extractor identity and exact flags

**unblob 26.6.4 emits** (`squashfs.py:24-69`; tag file sha256
`2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`, byte-identical to the
installed copy at `/home/vgpnk/.local/share/uv/tools/unblob/.../squashfs.py`):

```python
EXECUTABLE = "sasquatch"          # :25   ← v1..v4 default; unsquashfs is never invoked
V4BE_EXECUTABLE = "sasquatch-v4be"# :26   ← only reachable in `case Endian.BIG, 4` (:40-50)
case Endian.BIG,  _: commands_args.append("-be")   # :51-52
case Endian.LITTLE,_: commands_args.append("-le")  # :53-54
commands_args.extend(["-no-exit-code", "-f", "-d", "{outdir}", "{inpath}"])  # :56-64
```

So for the v1/v2 carriers the argv is exactly
`sasquatch -le` (LE) or `sasquatch -be` (BE), then `-no-exit-code -f -d <extract-dir> <input>`;
the executable never becomes
`sasquatch-v4be` (the v1/v2 extractor tuple is `SquashFSExtractor(3, 0x73717368)`,
`squashfs.py:75`, and `version == 4` is the only v4be gate). The six chunk-only JSON reports are
archived as `.ufo/waves/round-44/w1/R44C1Revenger/unblob-<carrier>.json` (sha256s in §3).

**sasquatch 4.5.1 source, onekey-sec/sasquatch @ `sasquatch-v4.5.1-6`
(`squashfs-tools/unsquashfs.c`, sha256 `ece42b66f37ba67707c2c51b47b643c027232153705f59d238da79958a54cb40`):**

| flag | source lines | semantics |
|---|---|---|
| `-be` | `4389-4394` | `strcmp(argv[i], "-be")` → `swap = (host is LE) ? 1 : 0` |
| `-le` | `4395-4401` | `strcmp(argv[i], "-le")` → `swap = (host is BE) ? 1 : 0` |
| `-no-exit-code` (alias `-no-exit`) | `4019-4020` (`parse_cat_options`), `4147-4148` (`parse_options`) | `set_exit_code = FALSE` |
| `-f` (alias `-force`) | `4270-4271` | `force = TRUE` (overwrite extract dir) |
| `-d` (alias `-dest`) | `4210-4211` | destination path (the `{outdir}` argument) |
| `-da` (alias `-data-queue`) | `4049-4060` (`parse_cat_options`), `4241-4252` (`parse_options`); help `3817,3918` | **takes a size argument**, sets the data queue in Mbytes (default 256). It is a memory-tuning knob, **not** in unblob's argv for any version. |

Correction to the seat premise: there is no `-da` flag *emission*. The only flags unblob adds are
the one endianness selector and the fixed tail above; `-da` exists in the binary and is unused by
the extractor. The extracted bytes are identical either way (probe below).

SOURCES-id mapping for the L1 (the seat brief's numbering differs from `corpus/SOURCES.md`):
unblob 26.6.4 handler source = **S108** (also S112 for the v4-BE argv);
onekey-sec/sasquatch source at the release tag = **S121**; rea-agents 6.5.0 package rows =
**S119/S123** (S119 is the derivation/gap-schema quote used in §1; nothing in S119 names
`sasquatch` or carries extractor argv — a grep of the package's `dist/` for `sasquatch` returns no
hits).

## 6. Independent oracle cross-check (probe, no REA)

Read-only probes to scratch: `unsquashfs 4.7.5` (`/usr/bin/unsquashfs`) lists the four v1/v2
fixtures with `-lls` (exit 0; BE inputs print "Reading a different endian SQUASHFS filesystem" on
stderr — autodetect, not a refusal) and extracts all six carriers with `-d` (exit 0); sasquatch
4.5.1 with the exact unblob argv extracts all six with exit 0. The two producers agree
member-for-member:

| carrier | members (rel, size, sha256) | sasquatch == unsquashfs | == committed S138 `__output__` |
|---|---|---|---|
| `v1le`/`v1be` | `apple.txt` 6 `303980bc…197d0`; `banana.txt` 7 `5a81483d…016b1`; `cherry.txt` 7 `86baf352…cbcf55` | yes (3/3) | yes (3/3) |
| `v2le`/`v2be` | `apple1.txt` 7 `6181259c…e1c30`; `apple2.txt` 7 `919fc82d…8d4aff`; `apple3.txt` 7 `2d95014e…bd21ec6`; `apple4.txt` 7 `08d9b05b…8a959d` | yes (4/4) | yes (4/4) |
| `v21le`/`v21be` | the same four members with the same digests | yes (4/4) | yes (4/4) |

The committed `corpus/evidence/round-44/oracle/**/__output__/<fixture>_extract/*.txt` blobs are real
bytes (6–7 B, not LFS pointers; `git ls-files -s` mode 100644) and hash to the same values. Three
witnesses (unblob expected tree, sasquatch, unsquashfs) therefore agree on the member set, so the
oracle premise of R44-C1 holds. For the two L1-added carriers the **inputs** were checked too:
`corpus/evidence/round-44/carriers/squashfs_v2.1_{le,be}.bin` hash byte-identically to the
upstream media-LFS objects at
`…/squashfs_v2/{little,big}_endian/__input__/squashfs_v2.1_{le,be}.bin`
(`6b6cd2fd…f253a` / `c0140bac…f35db`), so the added bytes are the real S138 dataset, not a lane
artifact — though the S138 manifest records only `__output__` (no `__input__` fetch), so that URL
belongs in a fetch receipt. Note the trees are named by the *fixture* filename
(`squashfs_v1.0_le.bin_extract`); under REA the input is renamed `firmware.bin`, so the after-root
is `firmware.bin_extract` — the counter must compare members **relative to the root**, not the
tree directory name.

Probe ledger (all exit 0; `probes.json` carries the per-member digests):

| probe | command (scratch copy `firmware.bin` unless noted) | exit | wall |
|---|---|---|---|
| chunk-only detection ×6 | `/home/vgpnk/.local/bin/unblob -s -p 1 -e <out>/extract --report <out>/report.json --log <out>/unblob.log <out>/firmware.bin` | 0 | ≈0.56 s each (mtime deltas of the four serial v1/v2 runs; v2.1 probed the same way) |
| sasquatch extract ×6 | `/home/vgpnk/.local/bin/sasquatch {-le,-be} -no-exit-code -f -d <out> <carrier>` | 0 | 0.00 s each |
| unsquashfs read ×4 + extract ×6 | `/usr/bin/unsquashfs -lls <fixture>`; `/usr/bin/unsquashfs -no-progress -d <out> <carrier>` | 0 | not individually timed |
| upstream input fetch ×2 | media-LFS `__input__/squashfs_v2.1_{le,be}.bin` → scratch | 0 | not individually timed |
| source comparison | tag downloads under `<scratch>/src/` | 0 | n/a |

No `extract-firmware` run and no `tools/round-44/c1-run.sh` was executed by this seat.

## 7. Observed REA-side evidence already in the repo (no new run)

Round-42 C2 dev envelopes are real REA 6.5.0 receipts on the same MIT fixtures (committed under
`corpus/evidence/round-42/c2/dev/`); their `run.json.subject_sha256` matches the carrier pins:

| envelope | input | observed |
|---|---|---|
| `H42` | `79c0f388…` = **v2be**, undamaged, `max_depth 3`, after arm | `chunks[0].handler "squashfs_v2"`, `extraction_failed false`; derivation `$input → $output/firmware.bin_extract` handler `"squashfs_v2"`; 4 members directly under the root; exit 0; coverage complete |
| `C17` | composite `54ebabce…` whose first chunk is the declared `v1-le` fixture, two-chunk carrier | v1 chunk handler `"squashfs_v1"`, extraction success, 3 members under `$output/firmware.bin_extract/0-4096.squashfs_v1_extract` |
| `H43` | `529e1077…` = **v1be**, sasquatch absent from the child PATH (`home_bin_on_path false`, gap `dependencies ["sasquatch"]`) | chunk handler `"squashfs_v1"`, `extraction_failed true`, gap `missing-extractor-dependency`, 0 files, no derivations, REA exit 0 |
| `H46` | `7c62dbe3…` = **v2le**, sasquatch absent from the child PATH | chunk handler `"squashfs_v2"`, `extraction_failed true`, gap `missing-extractor-dependency`, 0 files |
| `C11` | `79c0f388…` = **v2be**, before arm, dependency absent | chunk handler `"squashfs_v2"`, gap `missing-extractor-dependency`, 0 files |
| `H48` | damaged v1 variant `de685787…` (round-42 damage window) | chunk handler `"squashfs_v1"`, `extractor-failure` — a damaged copy is not a carrier match |

This is direct evidence for R44-C1's CTL-C1-3 shape ("sasquatch stripped → non-zero with
`missing-extractor-dependency`") on the same v1/v2 bytes, and for the clean after-shape on
`v2be`. It is not a substitute for the after-receipts; it is the pre-freeze prior.

No round-42 dev envelope covers the two v2.1 carriers (they are absent from
`tools/round-42/fixtures.json`, so the round-42 generator could not have produced them). Their
REA-side prior is the same source-read contract, corroborated by the v2.0 twin receipts
(`C11`/`H42`/`H46`): same handler string, same body bytes, same whole-file single-chunk shape.

## 8. Port hazards for `tools/round-44/c1-counter.py`

Port source is frozen at `tools/round-42/c1-counter.py`; these v3-specific parts do not carry over:

1. **`carriers.json` layout (blocker, see Verdict-4).** Correct v1/v2 offsets:
   `magic@0..4`, `s_major@28..2`, `s_minor@30..2`, `bytes_used@8..4` (u32),
   `inode_table_start@20..4`, `directory_table_start@24..4`; superblock size 32 B; **no**
   `compression` field. The frozen JSON's `bytes_used_offset 40 / len 8` and
   `compression_offset 20 / len 2` are v3 offsets and contradict its own cited source
   (unblob `squashfs.py:123-137` lists exactly `s_magic,inodes,bytes_used,uid_start,guid_start,
   inode_table_start,directory_table_start,s_major,s_minor`; `uint32 bytes_used` is at `:128`).
2. **Tables.** `MAGIC_BY_VARIANT`/`HANDLER_BY_VARIANT`/`VARIANT_BY_HANDLER`
   (`c1-counter.py:438-450`) model v3's "magic chooses the variant". For v1/v2 the magic is
   **shared** (`hsqs`/`sqsh`) and the discriminator is `s_major == 1|2`; a magic→variant map
   cannot distinguish v1 from v2. Bind `(endianness, s_major) → handler` and then require
   `handler == carrier.handler` by exact string equality.
3. **`layout_probe()`** (`c1-counter.py:1173-1225`) reads the 119-byte v3 struct at offsets
   63/87/95/103/111 and walks compressed chunks; drop it. The v1/v2 probe only needs
   magic/major/minor/endianness and `32 ≤ inode_table < dir_table ≤ bytes_used ≤ len`.
4. **`HANDLER_RE`/`SQFS3_TEXT_RE`** (`c1-counter.py:454-455`) are v3 text bindings for the
   PROVINCE/README checks; the round-44 analogues must accept `squashfs_v1` and `squashfs_v2`
   (tolerating `_nonstandard`/v3/v4 text as *unrelated* text, not as matches).
5. **`COMPRESSIONS = ('gzip','lzma')`** (`:452`) has no v1/v2 analogue; v1/v2 are zlib-only.
   Do not read a compression field; freeze `"gzip"` as a declared format property.
6. **Oracle root/rows.** `same_rel()` compares extract-root-relative paths exactly
   (`:1591-1599,1602-1608`); the S138 trees are rooted at `<fixture>_extract/` and the
   `unsquashfs -lls` census is rooted at `squashfs-root/`. Both prefixes must be stripped when
   the frozen oracle table is written; the after-root is `firmware.bin_extract` under REA.
7. **Handler binding scope.** Use `derivations[].handler == carrier.handler` then
   `subject_root()`; do **not** certify from `chunk_handlers()` (all chunks) and do not require
   member edges (handler `null`) to match.
8. **`s_minor` is not bound by the handler.** `SquashFSv2Handler.PATTERNS` reads magic and
   `s_major` only (`squashfs.py:161-198`); v2.0 and v2.1 both emit `squashfs_v2`. `carriers.json`
   already freezes `s_major` — it must also check `s_minor` (0 vs 1) in the probe if the two v2.1
   rows stay, and no rule may reject a carrier for `s_minor != 0`.
9. **Provenance pin for the two added carriers.** `v21le`/`v21be` have no
   `tools/round-42/fixtures.json` row and the S138 manifest has no `__input__` fetch. Their bytes
   are upstream-identical (verified), but add a fetch receipt (URL + sha256) so the freeze's
   provenance chain is as strong as the four v2.0-era carriers'.

## 9. Confidence and limits

- **Measured (high):** one whole-file chunk per carrier with the exact handler string for all six
  frozen carriers; the `-be`/`-le`/`-no-exit-code`/`-f`/`-d` argv and the absence of `-da` from
  unblob's argv; sasquatch and unsquashfs both extract all six carriers with identical members
  equal to the committed `__output__` trees; the v1/v2 superblock values (including `s_minor 1`
  on v2.1); the pattern disjointness; the upstream byte-identity of the two added carriers; the
  round-42 dev receipts' REA shape on `v2be`/`v1le`(chunk)/`v1be`/`v2le`.
- **Inferred (medium-high):** that the L1's `c1-run.sh` invocation (`--format json --full-output`,
  no range selection) on the six carriers yields exactly the H42 shape — the unblob half is
  measured and REA's normalization is read from source and corroborated on `v2be`; the remaining
  inference is only that nothing in the L1's runner differs from the round-42 dev harness
  (`FirmwareProvider.js:228-241` is the same code path), plus the v2.1 extension by body identity.
- **Not measured (out of seat scope):** the actual round-44 after-receipts (the L1's data
  procedure), the counter's own score, and any v1/v2 carrier beyond these six fixtures. R44-C1's
  disclosed limit stands: six 4 KiB fixtures with 3–4 members promote the handler family, not
  every v1/v2 image.
- **Corrected premises:** `-da` is `-data-queue` and is not emitted; "compression" is not a v1/v2
  superblock field and `file`'s compressed/uncompressed word flips with byte order here; the
  frozen `superblock_layout` block's `bytes_used`/`compression` offsets are v3 offsets; the
  frozen carrier set is six while the claim text still says four.
