# R39-C2 recon — non-extractable SquashFS-like inputs (development carriers only)

**Verdict: DONE.** One stable distinct triage class exists — `no-squashfs-chunk` (H empty, no
gaps, no files). `truncated-body` is **FALSIFIED** as a separable class: within the frozen
grammar a truncated body, a `bytes_used` overrun and a byte-for-byte non-filesystem control are
the *same* feature vector, and a truncated body inside a wrapper is a *different* vector. The
garbage-4 KiB-prefix case **is extractable** (chunk at offset 4096) and produces a second,
currently unlisted signal family: `extraction_gaps[].kind == "unknown-chunk-handler"` plus an
**unknown-chunk publication** (`…/<offset>-<end>.unknown` in `files[]`).

All numbers below are measured from rea-agents 6.5.0 `extract-firmware --format json --full-output`
envelopes on development carriers built in scratch from trees I authored, with unblob 26.6.4 and
`sasquatch-v4be` 4.5.1 reachable on the child `PATH`. No K5/K6 carrier and no held-out carrier was
built or run; no REA device (`xd://mcp__rea_*`) was used; envelopes are archived under
`.ufo/waves/round-39/w1/artifacts/R39C2ReconTruncate/env/`.

## 1. Carriers (deterministic, authored in scratch)

`dev-carriers.py` (artifact) authors one 7-file / 1-empty-dir tree (xorshift fill, fixed names,
sha256 per file in `manifest.json`), builds the base image with
`tools/round-37/gen-squashfs.py TREE OUT --endian le|be --comp gzip|xz`, and applies each mutation
as a pure function of the image and its superblock. Rebuilding under a second tree root gave
byte-identical carriers; the base image is stable at
`be-base-gzip.sqsh sha256 7fc66d5f478cf7245d84856c785fa7c03ea6ad8b268c4078646553a7c8099497`
(27 033 bytes, inodes 14, 96-byte superblock, `bytes_used` at offset 40).

| carrier | recipe | size | bytes_used (base) | declared in carrier | chunk starts at |
|---|---|---|---|---|---|
| be-base-gzip | base BE gzip | 27033 | 27033 | 27033 | 0 |
| be-base-xz | base BE xz | 27033 | 27033 | 27033 | 0 |
| be-trunc-half (a) | `img[:bytes_used//2]` | 13516 | 27033 | 27033 | – |
| be-trunc-quarter | `img[:bytes_used//4]` | 6758 | 27033 | 27033 | – |
| be-trunc-3q | `img[:bytes_used*3//4]` | 20274 | 27033 | 27033 | – |
| be-trunc-minus1 | `img[:bytes_used-1]` | 27032 | 27033 | 27033 | – |
| be-xz-trunc-half | xz base, half | 13516 | 27033 | 27033 | – |
| be-prefix4k (b) | 4 KiB garbage + img | 31129 | 27033 | 27033* | 4096 |
| be-xz-prefix4k | 4 KiB garbage + xz img | 31129 | 27033 | 27033* | 4096 |
| be-oversize-x2 (d) | patch `bytes_used = 2*len` | 27033 | 27033 | 54066 | – |
| be-oversize-plus4096 | patch `bytes_used = len+4096` | 27033 | 27033 | 31129 | – |
| be-oversize-plus1 | patch `bytes_used = len+1` | 27033 | 27033 | 27034 | – |
| be-trailing4k | img + 4 KiB garbage | 31129 | 27033 | 27033 | 0 |
| le-base-gzip / le-base-xz | base LE gzip / xz | 27033 | 27033 | 27033 | 0 |
| le-trunc-half (c) | LE base, half | 13516 | 27033 | 27033 | – |
| le-oversize-x2 | LE base, `bytes_used=2*len` | 27033 | 27033 | 54066 | – |
| le-prefix4k | LE base + 4 KiB prefix | 31129 | 27033 | 27033* | 4096 |
| be-prefix4k-trunc | prefix + half body | 17612 | 27033 | 27033* | – |
| le-prefix4k-trunc | LE prefix + half body | 17612 | 27033 | 27033* | – |
| be-trunc-half-resized | half body, `bytes_used=len` | 13516 | 27033 | 13516 | 0 |
| be-elfwrap | `/bin/true` (43320 B) + BE img | 70353 | 27033 | – | 43320 |
| be-elfwrap-trunc | `/bin/true` + half BE body | 56836 | 27033 | – | 43320 (elf64) |
| garbage-control | xorshift(0xBADC0DE, 4096) | 4096 | – | – | – |

\* the prefixed carrier has no superblock at offset 0, so `declared` is not meaningful; the
superblock starts at 4096 and still declares 27033.

Composed carriers (one extra signal on purpose, §6): `be-prefix4k-link-symlink` (prefix + in-tree
symlink `etc/config-link -> config.ini`), `be-prefix4k-escape-symlink` (prefix + escaping symlink
`etc/passwd-link -> ../../../etc/passwd`).

## 2. Feature table (exactly the L1 grammar features; all 24 runs, `ok:true`, exit 0)

`H` = squashfs* handlers in `normalized_result.chunks[]`; `G` = `extraction_gaps[].kind`;
`D` = union of `extraction_gaps[].dependencies`; `BE` from `diagnostics[].report.command`;
`SR` = `MaliciousSymlinkRemoved`; `P` = `len(normalized_result.files)`.
Full machine copy: `artifacts/R39C2ReconTruncate/dev-features.json` (+ `.md`).

| carrier | H | G | D | BE | SR | P | coverage | chunk@ | candidate label |
|---|---|---|---|---|---|---|---|---|---|
| be-base-gzip | {squashfs_v4_be} | {} | {} | n/a | no | 6 | complete | 0 | clean |
| be-base-xz | {squashfs_v4_be} | {} | {} | n/a | no | 6 | complete | 0 | clean |
| be-oversize-plus1 | {} | {} | {} | n/a | no | 0 | complete | – | no-squashfs-chunk |
| be-oversize-plus4096 | {} | {} | {} | n/a | no | 0 | complete | – | no-squashfs-chunk |
| be-oversize-x2 | {} | {} | {} | n/a | no | 0 | complete | – | no-squashfs-chunk |
| be-prefix4k | {squashfs_v4_be} | {unknown-chunk-handler} | {} | n/a | no | 7 | partial | 0:None,4096:sqsh_be | unknown-chunk-wrapper |
| be-xz-prefix4k | {squashfs_v4_be} | {unknown-chunk-handler} | {} | n/a | no | 7 | partial | 0:None,4096:sqsh_be | unknown-chunk-wrapper |
| be-trailing4k | {squashfs_v4_be} | {unknown-chunk-handler} | {} | n/a | no | 7 | partial | 0:sqsh_be,27033:None | unknown-chunk-wrapper |
| le-prefix4k | {squashfs_v4_le} | {unknown-chunk-handler} | {} | n/a | no | 7 | partial | 0:None,4096:sqsh_le | unknown-chunk-wrapper |
| be-trunc-3q | {} | {} | {} | n/a | no | 0 | complete | – | no-squashfs-chunk |
| be-trunc-half | {} | {} | {} | n/a | no | 0 | complete | – | no-squashfs-chunk |
| be-trunc-quarter | {} | {} | {} | n/a | no | 0 | complete | – | no-squashfs-chunk |
| be-trunc-minus1 | {} | {} | {} | n/a | no | 0 | complete | – | no-squashfs-chunk |
| be-xz-trunc-half | {} | {} | {} | n/a | no | 0 | complete | – | no-squashfs-chunk |
| le-trunc-half | {} | {} | {} | n/a | no | 0 | complete | – | no-squashfs-chunk |
| le-oversize-x2 | {} | {} | {} | n/a | no | 0 | complete | – | no-squashfs-chunk |
| be-prefix4k-trunc | {} | {} | {} | n/a | no | 0 | complete | – | no-squashfs-chunk |
| le-prefix4k-trunc | {} | {} | {} | n/a | no | 0 | complete | – | no-squashfs-chunk |
| garbage-control | {} | {} | {} | n/a | no | 0 | complete | – | no-squashfs-chunk |
| be-trunc-half-resized | {squashfs_v4_be} | {extractor-failure} | {} | yes | no | 0 | partial | 0:sqsh_be | body-extractor-failure |
| be-elfwrap | {squashfs_v4_be} | {} | {} | n/a | no | 7 | complete | 0:elf64,43320:sqsh_be | clean |
| be-elfwrap-trunc | {} | {unknown-chunk-handler} | {} | n/a | no | 2 | partial | 0:elf64,43320:None | unknown-chunk-wrapper |

## 3. Per-case answers (canonical carriers)

### (a) BE image truncated to half its `bytes_used` — `env/be-trunc-half.json`
- `data.normalized_result.chunks` = `[]` → **no squashfs chunk is reported** (H = ∅); no
  `extraction_failed` value exists because no chunk exists.
- `data.normalized_result.extraction_gaps` = `[]` (G = ∅, D = ∅).
- `data.normalized_result.diagnostics` = `[]` → `BE = n/a`, `SR = no`.
- `data.normalized_result.files` = `[]` → P = 0; `published_bytes` 0; `unpublished_entries` `[]`.
- **No unknown-chunk publication** (`files[]` has no `.unknown` row).
- `data.normalized_result.coverage` = `"complete"`; `data.ok` = `true`; envelope exit 0.
- The only residual squashfs evidence: `data.raw_result.report[0].reports[]` has a
  `FileMagicReport` with `magic = "Squashfs filesystem, big endian, version 4.0, zlib compressed,
  27033 bytes, 14 inodes, blocksize: 4096 bytes …"` while `stat` size is 13516.

### (b) BE image with a garbage 4 KiB prefix (chunk at 4096) — `env/be-prefix4k.json`
- **A squashfs chunk IS reported**: `chunks[] = [{handler:null, range:{offset:0,length:4096},
  encrypted:null, extraction_failed:false}, {handler:"squashfs_v4_be",
  range:{offset:4096,length:27033}, root_file_range:{4096,27033}, extraction_failed:false}]`
  (H = {squashfs_v4_be}, `extraction_failed = false`).
- `extraction_gaps[] = [{kind:"unknown-chunk-handler", handler:null, range:{0,4096},
  dependencies:[], …}]` → G = {unknown-chunk-handler}, D = ∅.
- `diagnostics` = `[]` → BE = n/a; SR = no.
- **Unknown-chunk publication: yes** — `files[0].relative_path =
  "firmware.bin_extract/0-4096.unknown"`, size 4096, sha256
  `edc9983a5f8a590052203d12c58e8d367f7c694a8746b7b9ef87bcc8f5af9e9f` = sha256 of the 4096 prefix
  bytes. `unpublished_entries` = `[]`. P = 7 (6 tree files + that carve), `published_bytes` =
  30251 = 26155 + 4096, `coverage` = `"partial"`. The remaining 6 files are the tree's regular
  files (sha256 identical to the tree, e.g. `boot/cmdline.txt` `e17f68d5…`).
- LE and xz variants are identical except `handler:"squashfs_v4_le"` / carve names.

### (c) LE image truncated — `env/le-trunc-half.json`
- Identical vector to (a): `chunks []`, `gaps []`, `diagnostics []`, `files []`, `coverage
  complete`, `ok true`. **The envelope carries no endianness signal at all** (magic `hsqs` at 0
  is only visible in `raw_result.report[].FileMagicReport.magic`), so (a) and (c) are the same
  class instance as far as the triage interpreter is concerned.

### (d) BE `bytes_used` patched larger than the file — `env/be-oversize-x2.json`
- Identical vector to (a)/(c). Also identical for `len+1` (`be-oversize-plus1`) and `len+4096`
  (`be-oversize-plus4096`) and for LE (`le-oversize-x2`). No diagnostics, no gap, no file.

**`command` field:** none of (a)–(d) contains `data.normalized_result.diagnostics[].report.command`
— the extractor was never invoked, so `BE = n/a` follows the contract's definition rather than a
missing observation. The path is populated only when a chunk exists and its extraction fails
(measured examples: `be-trunc-half-resized` → `"sasquatch-v4be -be -no-exit-code -f -d …"` with
`ExtractCommandFailedReport`, i.e. `BE = yes`; round-38 `rea-k1-avm.json` → `"sasquatch-v4be
-no-exit-code -f -d …"` with the same typename, i.e. `BE = no`).

## 4. Mechanism (measured, not inferred)

- unblob 26.6.4 `unblob/handlers/filesystem/squashfs.py:82-97` computes
  `end_of_data_offset = start_offset + bytes_used` and calls `file.seek(end_of_data_offset)`.
  `unblob/file_utils.py:74-79` turns an out-of-range seek into `SeekError`.
  `unblob/finder.py:33-58` `_calculate_chunk` catches `SeekError` and returns `None`
  (log line: `Seek outside file during chunk calculation handler=squashfs_v4_be`), so the
  magic match produces **no `ValidChunk`**.
- `unblob/processing.py:773-779` `calculate_unknown_chunks()` starts with
  `if not chunks or file_size == 0: return []`. With zero valid chunks there is therefore **no
  `UnknownChunkReport`**, hence no gap and no carved file.
- rea-agents 6.5.0 derives all gaps from the chunk list
  (`dist/firmware/FirmwarePublication.js`: `chunkGaps("unknown-chunk-handler", chunk =>
  chunk.handler === null)` at :286, `chunkGaps("extractor-failure", chunk =>
  chunk.extraction_failed…)`, dependency gaps at :150-190) and publishes only files that the
  provider report names (`:79-104`). Zero chunks ⇒ `extraction_gaps[] = []`,
  `files[] = []`, `published_bytes = 0`, `coverage = "complete"`.
- Direct unblob runs confirm the bytes: `unblob/trunc-report.json` contains only
  Stat/FileMagic/Hash/Randomness reports for the input (no `ChunkReport`, no
  `UnknownChunkReport`), `extracted/` is empty, and `unblob/trunc-unblob.log` shows
  `Seek outside file during chunk calculation handler=squashfs_v4_be` followed by
  `Ended searching for chunks all_chunks=[]`. `unblob/prefix-report.json` by contrast holds
  `UnknownChunkReport 0-4096` **and** `ChunkReport squashfs_v4_be 4096-31129`, and
  `extracted/…/0-4096.unknown` is byte-identical to the prefix.
- The extractor is never invoked in (a)/(c)/(d). Direct probes show it would fail if it were:
  `sasquatch-v4be -be` on `be-trunc-half` exits 1 (`Read on filesystem failed because EOF`,
  `read_id_table: failed to read id index table`), on `be-oversize-x2` exits 1 (`Bad id count in
  super block`), and `-le` on `le-trunc-half` exits 1 (`Block size too small`).

## 5. Stability and the deciding invariant

Thirteen envelopes share the exact zero-chunk vector (H ∅, G ∅, D ∅, BE n/a, SR no, P 0):
truncation at ¼, ½, ¾ and −1 byte of `bytes_used`; xz as well as gzip; BE and LE; `bytes_used`
overrun by +1, +4096 and ×2; prefix + truncated body (BE and LE); and the non-filesystem control.
The deciding invariant is **`bytes_used > file_size`** (with the magic intact at the chunk start):
a one-byte overrun is enough, a one-byte truncation is enough. The opposite direction is not the
same class: `bytes_used < file_size` (prefix, trailing bytes) keeps the chunk and adds
`unknown-chunk-handler` + a published `.unknown` carve; a body cut *with the header amended* keeps
the chunk and lands in the existing `body-extractor-failure` class
(`be-trunc-half-resized`: G={extractor-failure}, BE=yes, P=0), which is the clean proof that
`body-extractor-failure` and the zero-chunk class are different causes, not two names for damage.

## 6. Separability controls against the existing classes

`features.py` applied to the round-38 receipts (`ref/`, read-only copies) and both AVM-probe
envelopes reproduces every known class and never the new one (`ref-features.md`):

| envelope | H | G | BE | SR | P | label |
|---|---|---|---|---|---|---|
| r38-K1-after / r38-k1-orig | {squashfs_v4_be} | {} | n/a | yes | 5 | escaping-symlink-removed |
| r38-K2-after | {squashfs_v4_be} | {unpublished-entry} | n/a | no | 3 | in-tree-symlink-metadata |
| r38-K3-after, r38-K4-after | {squashfs_v4_be} | {} | n/a | no | 4 | clean |
| r38-K1..K4-before | {squashfs_v4_be} | {missing-extractor-dependency} | n/a | no | 0 | dep-missing (D={sasquatch-v4be}) |
| r38-k1-avm | {squashfs_v4_be} | {extractor-failure} | **no** | no | 0 | avm-marker-be-dropped |
| (mine) be-trunc-half-resized | {squashfs_v4_be} | {extractor-failure} | **yes** | no | 0 | body-extractor-failure |

`no-squashfs-chunk` cannot shadow any of these: every existing class carries a squashfs handler
and/or a non-empty gap set, while the new class requires H ∅ **and** G ∅. The condition
`P = 0` is implied (zero chunks ⇒ no file can be published) but should be kept — it is the cell
that separates the class from a hypothetical non-squashfs input that publishes other extracts.

## 7. Composition hazard (grammar-level, worth freezing a rule about)

The grammar's gap/dependency cells are exact-set matches, so one carrier with two independent
signals has no row unless a combination row is added:

| carrier | H | G | SR | P | label |
|---|---|---|---|---|---|
| be-prefix4k-link-symlink | {squashfs_v4_be} | {unknown-chunk-handler, unpublished-entry} | no | 7 | **unclassified** |
| be-prefix4k-escape-symlink | {squashfs_v4_be} | {unknown-chunk-handler} | **yes** | 7 | **unclassified** |

Recommendation: the frozen held-out generator must apply **exactly one mutation per carrier**
(one damage/wrapper/symlink signal), otherwise the frozen class list is unevaluable for those
carriers by construction. The two `no-squashfs-chunk` recipes are composition-safe because a
zero-chunk input cannot grow a second gap.

## 8. Recommendation for the frozen C2 table

**8.1 Adopt exactly one new class: `no-squashfs-chunk`.** Suggested data row (cells in the frozen
column order; place it after every other row — its conditions are disjoint from all of them):

```
| no-squashfs-chunk | none | none | none | n/a | no | 0 | declared superblock extent exceeds the input (bytes_used > file size, magic intact): the handler seek fails past EOF, no ValidChunk and no UnknownChunkReport exist, so the envelope shows zero chunks, zero gaps, zero files and coverage "complete" -> obtain the complete image or the true extent; no extractor ran, nothing to install, and no gap marks the region | unblob 26.6.4 file_utils.py:74-79, finder.py:33-58, handlers/filesystem/squashfs.py:82-97, processing.py:773-779; rea-agents 6.5.0 dist/firmware/FirmwarePublication.js:150-190,286; artifacts env/be-trunc-half.json, env/be-oversize-x2.json, env/le-trunc-half.json |
```

**8.2 Reject `truncated-body`.** Four measured reasons:
1. Endianness is invisible: (a) BE-truncated and (c) LE-truncated are the identical vector; no
   grammar cell can separate them (the only endian evidence is a `FileMagicReport` string the
   interpreter does not read).
2. Truncation ≡ overrun: `be-trunc-minus1` and `be-oversize-plus1` differ by one byte in opposite
   directions and produce the same vector; both are one class, "declared extent exceeds input".
3. "Truncated" is not one vector: a truncated body inside an ELF wrapper is
   `G={unknown-chunk-handler}`, P=2, coverage partial (`be-elfwrap-trunc`), and a prefixed
   truncated body is the zero-chunk vector (`be-prefix4k-trunc`). One label, three vectors.
4. Nothing in the envelope names truncation: no diagnostic, no gap, no size field; the only
   difference from a clean run is absence, which is exactly what `no-squashfs-chunk` states.

**8.3 Optional second row — `unknown-chunk-wrapper`** (needed only if the held-out set contains
garbage-prefix/tail or wrapped carriers; the draft class list would leave them `unclassified`):

```
| unknown-chunk-wrapper | * | unknown-chunk-handler | none | n/a | no | >0 | input bytes outside the validated squashfs chunk were carved and published as <offset>-<end>.unknown and the gap carries that exact range (garbage prefix, trailing bytes, or an ELF wrapper whose squashfs body did not validate) -> read the filesystem at the gap range or the chunk range offset; the .unknown file is raw wrapper bytes, not decoded content | unblob 26.6.4 processing.py:780-803; rea-agents 6.5.0 dist/firmware/FirmwarePublication.js:286; artifacts env/be-prefix4k.json, env/be-trailing4k.json, env/le-prefix4k.json, env/be-elfwrap-trunc.json |
```

Note the observed detail: `be-elfwrap` (intact wrapper) has `G = {}` and is a legitimate `clean`
with a chunk at 43320; only a *failing* body leaves `unknown-chunk-handler`. Both wrapper and
zero-chunk vectors publish a raw `.unknown` carve — the wrapper class must state that the carve is
not extracted content, and `clean` must not be claimed from `P > 0` alone.

**8.4 Deterministic recipe function** (freeze-safe: no constants, reads the generated header):

```python
be64 = lambda b: int.from_bytes(b, 'big')          # BE superblock; LE -> 'little'
def bytes_used(img, endian='be'):
    return int.from_bytes(img[40:48], 'big' if endian == 'be' else 'little')

def no_squashfs_chunk(img, endian='be'):           # canonical class instance
    bu = bytes_used(img, endian)
    assert img[:4] == (b'sqsh' if endian == 'be' else b'hsqs') and bu >= 96
    return img[:bu // 2]                            # or head -c $((bu/2)); len < bu by construction

def no_squashfs_chunk_overrun(img, endian='be'):   # same class, other half of the cause
    return img[:40] + (len(img) + 1).to_bytes(8, 'big' if endian == 'be' else 'little') + img[48:]
```

Both recipes were measured (`be-trunc-half`, `be-oversize-plus1`). If the frozen generator wants
two instances of this class, use one of each; if it wants one, use the truncation recipe (it also
covers LE and xz). Requirements: the carrier keeps the magic at its first byte and its unchanged
`bytes_used`; the file must be strictly shorter than `bytes_used`; do not wrap it and do not
append a second valid chunk (either turns it into `unknown-chunk-wrapper`). Seed usage: pick tree
contents/endian/compression from the freeze-hash seed, then derive the cut from the *generated*
header, never from a hard-coded length.

**8.5 Counter/interpreter pitfalls this recon exposes**
- `coverage` is not an extraction indicator: zero-chunk inputs report `"complete"` while nothing
  was extracted. Do not build a control that trusts `coverage`.
- `P > 0` is not "files extracted": an unknown-chunk carve counts as a published file.
- `FileMagicReport.magic` (`raw_result.report[].reports[]`) is the only squashfs evidence in a
  zero-chunk envelope; the frozen grammar deliberately does not read it, so the class label must
  be read as "no chunk was reported", not "the bytes were not squashfs".
- Exact-set gap cells make composed carriers unlabelled (§7) — a do-nothing/catch-all control
  should not be confused with this; here the *absence* of a match is structural.

## 9. Evidence inventory (all under `.ufo/waves/round-39/w1/artifacts/R39C2ReconTruncate/`)

| file | content |
|---|---|
| `env/*.json` (24) | full `{ok,data,meta}` envelopes, one per dev carrier; `data.subject.digest.sha256` equals the carrier sha256 in `manifest.json` for all 24 |
| `comp-env/*.json` (2) | composed prefix+symlink envelopes |
| `manifest.json`, `comp-manifest.json`, `build.json`, `build2.json` | carrier sha256/recipe/declared-extent records and the generator invocations |
| `dev-carriers.py`, `features.py` | deterministic carrier builder; grammar-faithful feature extractor + candidate-row evaluator |
| `dev-features.{json,md}`, `ref-features.{json,md}`, `comp-features.{json,md}` | feature tables quoted above |
| `unblob/trunc-report.json`, `trunc-unblob.log`, `prefix-report.json`, `prefix-unblob.log` | direct unblob 26.6.4 mechanism evidence |
| `sasquatch/*.stdout.txt`, `*.stderr.txt`, `*.exit.txt` | direct extractor probes (all exit 1) |
| `commands.txt` | exact commands, versions, hashes |

Tooling: no installation, upgrade or removal was performed (unblob 26.6.4, rea-agents 6.5.0 via
the existing npx cache, sasquatch/sasquatch-v4be 4.5.1, Python 3.14.8). No pacman transaction,
no VCS mutation, no writes outside this report and the artifacts directory, scratch removed.

## 10. Risks / limits

- Development carriers are small (27 KB images, gzip/xz, no fragments/xattrs/export table per
  `gen-squashfs.py`); unblob's zero-chunk behaviour depends on the seek/overflow
  path only, not on image size, but a held-out carrier with a much larger `bytes_used` is still
  only [INFERENCE] until one is run.
- I did not test a truncated *AVM-marked* image (mkfs_time patched); the decide point is the seek
  before the extractor's AVM branch, so it is expected to be the zero-chunk vector, not measured.
- The wrapper row's `P > 0` is measured on 5 carriers; a zero-length or all-padding wrapper region
  would instead surface as a padding chunk and no gap [INFERENCE].
- The `unknown-chunk-handler` family is orthogonal to C1's coverage claim and does not touch
  K1–K4 evidence; no held-out or K5/K6 carrier was built or run.
