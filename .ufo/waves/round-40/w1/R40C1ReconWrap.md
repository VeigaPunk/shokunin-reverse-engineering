**Verdict: DEFECTS FOUND** — the carrier question is answered by measurement, and the answer
removes two of the draft's three carrier forms and one clause of its predicate: a whole AVM
`.image` can never produce a REA envelope (two independent hard caps, both measured), a raw carved
member costs an extra `unknown-chunk-handler` gap plus a published `*.unknown` file plus ~0.95 MB of
report, and the clause "recomputes to its evidence id" is false — `evidence_id` changes between two
runs of the identical carrier. A clean carrier exists and its receipt noise is now enumerated: the
REA `--offset/--length` selection over the pinned vendor image, or the equally clean
`align_up(bytes_used,4096)` carve.

Seat: `R40C1ReconWrap` (leaf). Lane corpus untouched. Nothing written outside
`.ufo/waves/round-40/w1/R40C1ReconWrap.md` and
`.ufo/waves/round-40/w1/artifacts/R40C1ReconWrap/`. Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40C1ReconWrap` removed at exit; every cited envelope is copied
into the artifacts directory (gzip where large). No `git` write, no mutating `jj`. No tool installed
or upgraded (see §10). V1 was **not** downloaded and **no REA/unblob run touched** V1's AVM-BE
member, a named (frozen or draft-named) carrier, a lane-built carrier, or a C2 held-out carrier.
Every run used a development input: the 6590 07.57 image (this wave's dev image) and, as the single
deliberate second-image probe, the 6890 LTE 07.57 member — whose cap failure is itself the answer to
"can V2 be built from another model" (§6). That probe also means 6890 is no longer a clean V2
candidate, so the report does not propose it as one.

## 1. Inputs and carrier discipline

Development vendor image (this wave's only REA subject): **FRITZ!Box 6590 Cable 07.57**
`https://download.avm.de/fritzbox/fritzbox-6590-cable/other/fritz.os/FRITZ.Box_6590_Cable-07.57.image`,
39 290 880 B, sha256 `0c539499044a807c2dfa3ffdf5eafe6016096912fa6e13374f48afa46cd0abae`.
Its members (offsets re-derived from the tar headers, not guessed):

| member | tar data offset | bytes | magic | `bytes_used` | marker | metadata-hdr LE / BE | align4096 | slack | residual |
|---|---|---|---|---|---|---|---|---|---|
| `./var/remote/var/tmp/filesystem.image` | 31 575 552 | 5 443 592 | `sqsh` | 5 441 468 | **true** | **1380 / 25605** | 5 443 584 | 2 124 | **8** |
| `./var/remote/var/tmp/x86/filesystem.image` | 270 848 | 27 750 408 | `hsqs` | 27 748 075 | true | 1916 / 31 751 | 27 750 400 | 2 333 | **8** |
| `./var/remote/var/tmp/kernel.image` | 37 020 160 | 1 932 808 | `\x12\x91\xed\xfe` (0xfeed9112) | — | — | — | — | — | — |
| `./var/remote/var/tmp/x86/kernel.image` | 28 022 272 | 3 552 264 | gzip at 14 958 | — | — | — | — | — | — |

The BE member's geometry is the same shape as V1's: V1's member is 5 443 592 B with
`bytes_used 5 442 392` (round-39 adjudication), so `align4096 = 5 443 584` and `residual = 8`
too — [INFERENCE] from those two recorded numbers; V1's bytes were not opened this wave.

Screened but **not** REA'd (pure-Python reads only): 7590 08.25, 6591 Cable 08.25, 6660 Cable
08.25, 5530 Fiber 08.25, 7560 07.30, 7490 07.62 — `carrier-screen.tsv`.
REA ran on exactly: the 6590 image, four carves of its BE member, one padded carve, one
marker-stripped carve, its two kernel images and its LE member, plus the 6890 BE member (the
one deliberate "does a second vendor member fit?" probe, §6).

Environment: unblob 26.6.4 (`executable_sha256 0ce7b624…`, engine block of every envelope),
sasquatch-v4be 4.5.1 reachable on the child PATH, `npx -y rea-agents@6.5.0` (already in the npx
cache). `TMPDIR` and cwd were the scratch dir for every call.

## 2. Does REA reach the AVM-BE member from a whole `.image`? No — and not for lack of recursion

| run | exit | report | failure |
|---|---|---|---|
| `dev6590.image`, default flags | 1 | 589 B | `Staging entry budget exceeded (10000)` (13.1 s) |
| `dev7590.image`, default flags (single LE member) | 1 | 588 B | `Staging entry budget exceeded (10000)` (2.1 s) |
| `dev6590.image --max-output-files 40000` | 1 | 2 901 B | `Report exceeded 8388608 bytes` (17 s) |
| `dev6590.image --max-output-files 40000 --filter-output normalized_result` | 1 | 2 901 B | same report cap — filtering happens after the cap |

Recursion itself works. In the 40 000-file run unblob finished and printed a chunk distribution the
error message preserves (`artifacts/…/unblob-summaries-from-failed-runs.txt`): 5 427 files, 530
dirs, 875 links, 191.81 MB extracted, chunk types ELF32 74.97 MB, TAR 46.71 MB,
**SQUASHFS_V4_LE 26.46 MB, SQUASHFS_V4_BE 5.19 MB**, GZIP 3.35 MB, AR 277 KB, UNKNOWN 34.64 KB,
identification ratio 99.98 %, one `MaliciousSymlinkRemoved`. So the `tar` handler reaches both
members and both squashfs handlers run; REA then cannot hand the report back.

The 8 388 608-byte report cap is not reachable by any flag: `extract-firmware --help` lists
`--max-depth`, `--max-output-bytes`, `--max-output-files` only. **Consequence:** any carrier whose
published set is large cannot be enveloped at all. `--max-output-files 40000` on the 6590 image
moves the failure from the entry budget to the report cap — the whole-`.image` form is dead at every
setting, on two structurally different images.

## 3. Carved member forms, measured (development BE member, 2 942 published files, 697 oracle files)

| form | input bytes | exit | report B | files | chunks | gaps | published_bytes | wall |
|---|---|---|---|---|---|---|---|---|
| raw tar member as shipped (trailer kept) | 5 443 592 | 0 | 8 299 343 | **2 943** | **404** | 263 `unpublished-entry` + **1 `unknown-chunk-handler`** `[5443584,8)` | 24 054 885 | 20.2 s |
| carve to `bytes_used` | 5 441 468 | 0 | 7 364 889 | 2 942 | 403 | 263 `unpublished-entry` | 24 054 877 | 18.1 s |
| carve to `align_up(bytes_used,4096)` | 5 443 584 | 0 | 7 345 487 | 2 942 | 403 | 263 `unpublished-entry` | 24 054 877 | 11.9 s |
| **REA selection inside the `.image`** (`--offset 31575552 --length 5443584`) | — | 0 | **7 324 911** | 2 942 | 403 | 263 `unpublished-entry` | 24 054 877 | 12.6 s |
| span + 65 536 zero bytes | 5 507 004 | 0 | 8 301 691 | 2 943 | 404 | 263 `unpublished-entry` (padding chunk, **no** unknown gap) | 24 054 877 | 20.5 s |

Every row's single top-level chunk is `squashfs_v4_be` at `[0, 5443584]` (or `[0, 5441468]`) with
`extraction_failed: false`; 402 further chunks come from containers inside files (351 `elf32`,
49 `tar`, 2 `ar`); chunk nesting is 1 root, 296 at depth 1, 106 at depth 2, `depth_limited_paths`
empty, `max_depth` parameter 3.

Receipt noise each choice adds (the numbers the gap rule has to absorb):

- **263 `unpublished-entry` gaps are unavoidable** — one per in-tree symlink (263 symlinks: 29
  `absolute-inside`, 234 `inside`, 0 escaping). A future "no gaps" reading of the predicate is
  impossible on a real vendor carrier.
- raw member adds: 1 `unknown-chunk-handler` gap of exactly 8 bytes, 1 published file
  `firmware.bin_extract/5443584-5443592.unknown`, a second `extraction_continuations` entry
  ("select a materially narrower range…"), a **changed relative-path prefix** (every file gains a
  `0-5443584.squashfs_v4_be_extract/` component), +954 KB of report.
- zero padding past `bytes_used` is harmless as long as it stops at `align4096` (the span carve and
  the 2 116-byte zero-padded carve are **sha256-identical**, `767124f0…`); padding beyond it
  becomes a `padding` chunk and is published as a file (`…-5507004.padding`), not a gap.
- non-zero trailing bytes past `align4096` are the only source of the unknown gap here.

## 4. Trailing bytes past `bytes_used` — the mechanism, and it is structural

`residual = size − align_up(bytes_used,4096) = 8` on **every** member measured, six images, both
endiannesses (`probe-sqfs-out.tsv`):

```
dev6590 BE 5 443 592 / used 5 441 468 -> align 5 443 584 residual 8  trailer 23de53c4a4224eb2
dev6590 LE 27 750 408 / used 27 748 075 -> align 27 750 400 residual 8  trailer 23de53c44f84cfce
dev7590 LE 35 835 912 / used 35 834 769 -> align 35 835 904 residual 8  trailer 23de53c4c688c892
d6890 BE  44 072 968 / used 44 069 608 -> align 44 072 960 residual 8  trailer 23de53c4951e26df
d7560 BE  26 697 736 / used 26 695 962 -> align 26 697 728 residual 8  trailer 23de53c4e05ecf0f
d7490 BE  35 012 616 / used 35 008 578 -> align 35 012 608 residual 8  trailer 23de53c4923bb024
```

So the vendor member is `align_up(bytes_used,4096)` plus an **8-byte AVM trailer** whose first four
bytes are the constant tag `23 de 53 c4` and whose last four vary per image. The trailer is not
crc32, adler32 or a sha256 prefix of `[0:bytes_used]`, `[0:size−8]` or `[0:align4096]` (all tested,
no hit) — its function is **not determined** here.

Receipt consequence, exactly as measured: keeping the trailer produces the 8-byte
`unknown-chunk-handler` gap and publishes those 8 bytes as `…unknown`; dropping it at `align4096`
produces a clean envelope. The 2 116 bytes of real slack are **zeros** in this member (the span
carve and a zeros-padded carve of the truncated member hash identically).

## 5. Handlers / chunks / gaps recorded for the tar, the kernel images and the LE member

| input | envelope | content |
|---|---|---|
| whole `.image` (tar) | none (both caps, §2) | unblob's own summary is the only record: TAR root, SQUASHFS_V4_BE 5.19 MB, SQUASHFS_V4_LE 26.46 MB, ELF32/TAR inside files, UNKNOWN 34.64 KB |
| `./var/remote/var/tmp/kernel.image` (AVM main, 1 932 808 B, 0xfeed9112) | **ok, 5 423 B** | `coverage: complete`, **0 files, 0 chunks, 0 gaps** — silence, not a gap |
| `./var/remote/var/tmp/x86/kernel.image` (3 552 264 B) | ok, 19 771 B | 6 chunks: `gzip` at `[14958, 3531766)`, `elf32`, `cpio_portable_ascii`, 3 top-level `unknown`; gaps `unknown-chunk-handler ×3` (`[0,14958)`, `[3531766,20498)`…) + `depth-limited ×1`; 5 files |
| `./var/remote/var/tmp/x86/filesystem.image` (LE member alone, 27 750 408 B) | **exit 1, 2 804 B** | `Report exceeded 8388608 bytes`; unblob summary: 6 916 files, 1 214 dirs, 615 links, `SQUASHFS_V4_LE 26.46 MB`, **UNKNOWN 8 B** (the trailer again) |

The AVM kernel container is invisible to REA while `coverage` still says `complete` — anything that
reads "no failed chunk, coverage ok" as evidence of full understanding will be wrong on AVM images.

## 6. Recommendation: carrier form, and the V2 problem it exposes

**Primary (no carve step):** frozen carrier = the pinned vendor `.image` plus
`--offset <member data offset> --length <align_up(bytes_used,4096)>`. Measured cleanest report
(7 324 911 B), 403 chunks, 263 gaps, 2 942 files, and `selection.sha256 = 767124f0…` is the
sha256 of those bytes — an independent, frozen-checkable projection of
`image[p : p+len]`, so the counter can verify the selection without re-carving.
**Equal-footing alternative:** a committed carve to `align_up(bytes_used,4096)`
(7 345 487 B, identical projection, `selection` absent because the file *is* the subject).
**Forbidden by measurement:** the whole `.image` (§2) and the raw tar member (§3/§4 — extra gap,
extra published file, ~+1 MB report, different path prefix).

Report headroom on the recommended form: 8 388 608 − 7 324 911 = **1 063 697 B (12.7 %)**. That
headroom is the carrier sizing limit, and it is what kills V2:

| second-image candidate | AVM-BE member? | oracle regular files | REA verdict |
|---|---|---|---|
| 6590 Cable 07.57 | yes (`sqsh`, marker, LE hdr) | 697 | **works** (this wave's dev image) |
| 6890 LTE 07.57 | yes | 7 667 | **measured fail** — report cap at 40 000-file budget |
| 7560 07.30 | yes (both-endian header **ambiguous**, 2060/3080) | 8 855 | predicted fail [INFERENCE] |
| 7490 07.62 | yes (outer only) | 8 files + 86 links, **inner `filesystem_core.squashfs` 34 422 784 B** | recursion would hit the cap [INFERENCE] |
| 6591 / 6660 Cable 08.25 | `var/firmware-update.uimg` wrapper, no member | — | needs nested uimg extraction first |
| 5530 Fiber 08.25 | `var/tmp/fit-image` wrapper | — | — |
| 7590 08.25 | no — member is `hsqs` (LE) | 13 358 | whole image fails entry budget |

So on `download.avm.de` the **only** AVM-BE member that fits REA's report cap besides V1's is the
6590 07.57 member — the image this wave used as its development input. The draft's V2 clause ("a
second vendor image … no REA run before the freeze") is therefore unsatisfiable as written. Options,
for the L1 to choose (not mine to decide):

1. **V2 = 6590 07.57 member** with the disclosure that wave-1 recon ran REA on it — the gap rule
   below is derived from that same member, so the independence the rule was written for is gone;
2. **drop V2** and keep two lane-built carriers (gzip + xz) as L1/L2, recording "second vendor
   member does not fit REA's 8 MiB report cap" as a measured limitation instead of a carrier;
3. keep V2 = 6890/7560 and abandon the `extract-firmware` route for it — that contradicts the
   predicate, which names `extract-firmware`.

## 7. Gap rule the freeze can fix from this recon (development data only)

For a carrier carved/selected at `align_up(bytes_used,4096)` of an AVM-BE member:

- allowed gap kinds: `unpublished-entry` **only**, one per in-tree symlink, count = the oracle's
  `in_tree_symlinks` (263 on the development member; zero escaping links);
- `unknown-chunk-handler` allowed **only** if the 8-byte AVM trailer is kept, and then pinned to
  `range = [align_up(bytes_used,4096), member_end)` with `length = 8` and a published `.unknown`
  file whose sha256 is the trailer's;
- `extractor-failure`, `depth-limited` and `dependency-missing` are **not** allowed;
- `coverage` is `partial` on a healthy vendor carrier (symlinks are metadata) — the predicate must
  not require `complete`;
- the test for a healthy run is `chunk.extraction_failed == false` **plus** the gap set above, not
  the exit code: a marker-stripped member returns **exit 0, `ok: true`** with `extraction_failed:
  true`, one `extractor-failure` gap and 0 files (`artifacts/…/envelopes/rea-member-nomarker2.json`,
  diagnostic argv `sasquatch-v4be -be …`).

## 8. The oracle: the round-39 reader cannot read a genuine AVM member; the AVM-mode patch can

`python3 -I -B tools/round-39/sqfs-list.py carves/member-span4096.sqsh --files … --symlinks …`
→ **exit 2**, `sqfs-list: metadata body out of bounds: offset 5435948 length 29708, image 5443584
bytes`. It decodes the 2-byte metadata length header with the superblock's endianness; the genuine
member stores it little-endian (`inode_table_start` header `6405`: LE 1380, BE 25605;
`directory_table_start` header `900c`: LE 3216, BE 36876). Exactly one decode is plausible (≤ 8192,
in bounds) on five of the six members measured; **7560 is ambiguous both ways**, so the round-40
oracle needs a stated tie-break, not only the marker.

Proof patch shipped in the artifacts (`sqfs-list-avm.py`, sha256 `4e7426ba…` = round-39 reader
`1808c3f5…` plus `_pick_header_endian()` and a 4-key addition to `--inspect`; no other change):

```
span member        exit 0  layout avm-be  metadata_header_endian little  697 regular files
                         263 symlinks (29 absolute-inside, 234 inside, 0 escaping), 1 special
                         277 compressed data blocks, 9 compressed metadata blocks, 622 fragment slices, 1 sparse
round-39 K5 (standard BE, no marker)   exit 0, 10 files, 3 symlinks (2 inside / 1 above-root)
round-39 K6 (standard BE, no marker)   exit 0, 3 symlinks (1 inside / 2 above-root)
                                       both equal the round-39 counter's own counts; the
                                       header-endian switch is inert on standard-BE images
marker-only carrier-avm.sqsh           exit 0, layout standard + warning
                        "marker holds but the metadata length header reads BE"  <- the R39 defect, now refused
```

Agreement with REA on the same bytes: **697/697 oracle files published at a path with the same
suffix and the same sha256** (0 missing, 0 mismatched — true for both the exact and the span carve),
**263/263 oracle symlinks equal to REA's 263 `unpublished_entries`**. REA's own file list is
**2 942**, not 697: 697 at `analysis_depth 1` (the image) and 2 245 at depth 2 (containers inside
files). The predicate's "publishes every regular file of the frozen independent oracle" must stay a
**subset/suffix test against the oracle**, never an equality test against REA's file list.

## 9. Defects routed at the draft (freeze-visible)

- **D1 — `evidence_id` is not reproducible.** Two runs of the identical carrier (same sha256, same
  flags, fresh outdirs): `ev_ebd91141…` vs `ev_e8e13257…`. The id hashes a report containing the
  temp extraction directory name and blob provider ids. "Recomputes to its evidence id" cannot be
  scored; it must become the projection below. Report bytes also move run to run (7 345 487 vs
  7 344 290, Δ 1 197 B).
  **Projection that measured stable (values *and* order):** `subject.digest`, `parameters` minus
  `output_directory`, `normalized_result.{engine, selection, coverage, published_bytes,
  extraction_gaps, unpublished_entries, diagnostics, depth_limited_paths, extraction_continuations}`,
  and `files|chunks|derivations` keyed on
  `(relative_path,size,sha256,analysis_depth,mime_type)` / `(input_path,range,handler,extraction_failed)`
  / `(parent_path,child_path,handler,parent_file_range)`. **Must be dropped:** `evidence_id`,
  `raw_result`, `*output_directory`, `files[].path`, `chunks[].provider_id`,
  `derivations[].provider_blob_id` (`nondeterminism.json`).
- **D2 — V2 is unsatisfiable** as drafted (§6). Decision needed in the freeze.
- **D3 — bar the whole-`.image` form explicitly**, with the measured reason (entry budget 10 000;
  report cap 8 388 608 B unreachable by flag).
- **D4 — the oracle must be AVM-mode**, and the round-39 reader's exit-2 on a genuine AVM member is
  the proof that the AVM layout is not a superblock-marker property only.
- **D5 — do not test `exit`/`ok` for extraction health**: marker-stripped member → exit 0,
  `ok: true`, 0 files, `extraction_failed: true` (§7).

## 10. Limits, inference, tooling

- V1's 8-byte residual is inferred from recorded numbers, not measured (V1 not opened).
- The trailer's checksum/length identity is undetermined; the tag `23de53c4` is measured.
- 7560 and 7490 carrier verdicts are [INFERENCE] (no REA run on them — they are candidate carriers);
  only 6890 is a measured cap failure.
- The tier-1 claim that the chunk span is `align_up(bytes_used,4096)` is read from the envelopes'
  own chunk ranges plus the sha256 identity of the zeros-padded carve, not from unblob source.
- Report sizes are per-run (Δ ≈ 1.2 KB); carrier headroom is therefore ~1.06 MB, not exact.
- No install or upgrade was performed: `npx -y rea-agents@6.5.0` resolved from the existing npx
  cache, unblob 26.6.4 / sasquatch-v4be 4.5.1 were preinstalled and untouched, no pacman
  transaction (host-wide pause respected).

## Artifacts (`.ufo/waves/round-40/w1/artifacts/R40C1ReconWrap/`, 3.2 MB)

`rea-carrier-matrix.tsv` (`403b12ae…`, 17 measured rows: form, exit, report bytes, files, chunks,
gaps, published bytes, wall) · `carrier-screen.tsv` (`03cc25b2…`, 9 vendor images: url, sha256,
member offset/size, magic, marker, header endianness, align/residual, oracle counts, verdict) ·
`probe-sqfs.py` (`9f223d5d…`) + `probe-sqfs-out.tsv` (residual-8 and `23de53c4` trailer) ·
`sqfs-list-avm.py` (`4e7426ba…`, AVM-mode oracle; round-39 reader `1808c3f5…` + one decode switch) ·
`oracle-span-files.tsv` (`8ed6734a…`, 697 rows), `oracle-span-links.tsv` (`e367693e…`, 263 rows),
`oracle-span-inspect.json` · `nondeterminism.json` (`1b00b865…`) ·
`unblob-summaries-from-failed-runs.txt` (the chunk distributions the caps hide) ·
`commands.log` (every command, exit code, wall time) · `envelopes/` — gzip of the seven member-form
envelopes (`rea-member-span4096.json.gz`, `…-astric_ttl`, `…-exact_sqsh`, `…-pad4096_sqsh`,
`…-pad64k_sqsh`, `rea-sel-span`, `rea-span-rerun`) and plain JSON for the small ones
(`rea-member-nomarker2`, both kernel images, all cap failures).
Rebuild any envelope with the exact command in `commands.log`; the carrier carves are byte-derived
from the pinned image (sha256 above) and are therefore reproducible without storing them.
