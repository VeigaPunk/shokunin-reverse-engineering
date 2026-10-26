# R40W2ReproV1 — independent reproduction of R40-C1 carrier V1

**Verdict: CONFIRMED.** I rebuilt V1 from its pinned vendor chain by hand (curl → image sha256 → `tar -xOf`
member → `head -c 5442392` → carrier pin; no lane tooling, no `fetch-vendor.py`) and ran REA 6.5.0
`extract-firmware --max-depth 1` on it myself. Every semantic dimension I was asked to compare — chunk
handler/range/`extraction_failed`, the 697 published files (path suffix, sha256, size), gap kinds and
counts, unpublished entries, diagnostics typenames — is **identical** to the committed receipt
`corpus/evidence/round-40/c1/V1/after.json`. Zero differences on all compared dimensions; the fresh
extraction also reproduces the frozen oracle `oracle.tsv` **byte-for-byte** (same sha256).

What I attacked: the representational honesty of the V1 evidence record — that it is a real run of the
pinned bytes through the pinned unblob + `sasquatch-v4be` pair under the frozen `--max-depth 1` parameter,
and not an oracle-derived fabrication or a run of different bytes/toolchain. I did not touch C2, the L2
path-suffix reading, PROVINCE/README/SOURCES/knowledge edits, or the score arithmetic (other seats).

## 1. Reproduction chain (my own, byte by byte)

Scratch `S=/fast/scratch/hyaku/kaidoku-r40/R40W2ReproV1`. All commands and exit codes in
`artifacts/R40W2ReproV1/reproduction-chain.txt`.

| step | command | result |
|---|---|---|
| 1 | `curl -fsSL --retry 3 -o image.bin https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/FRITZ.Box_6490_Cable-07.57.image` | exit 0, 39741440 bytes, 4.7 s; `sha256 = f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d` = `external.image_sha256` |
| 2 | `tar -xOf image.bin ./var/remote/var/tmp/filesystem.image > member.bin` | exit 0, 5443592 bytes; `sha256 = 334e56dfba6a785590bb5cdbd78fcb5be183b9af160b51fc8935a3015ad3f3d4` = `external.member_sha256` |
| 3 | `head -c 5442392 member.bin > carrier.bin` | `sha256 = ac4098bd11a76f8ad001faac0f1a5e018708d9b03943dfebb2b18a24e0038e95` = `carriers.json` V1 pin, 5442392 bytes |
| 4 | `cd $S && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1 $S/carrier.bin $S/out1` | exit 0, 3.5 s wall; `ok=true`, `meta.duration=2667ms` |
| 5 | `~/.local/bin/unblob -v --process-num 1 --depth 1 --extract-dir $S/ub1 $S/carrier.bin` | exit 0, 0.6 s; handler + argv in log (§4) |
| 6 | `PATH=/usr/bin:/bin ~/.local/bin/unblob …` (no `sasquatch-v4be`) | exit 1, `ExtractorDependencyNotFoundReport` (§5) |
| 7 | `PATH=<node>:/usr/bin:/bin npx -y rea-agents@6.5.0 extract-firmware … $S/carrier.bin $S/out_nodep` | exit 0, `ok=true`, **0 files**, `extraction_failed=true`, gap `missing-extractor-dependency` (§5) |

Chain links that could have rotted and did not: the vendor URL still serves the pinned image (exit 0,
exact sha256), and the tar member is still exactly the pinned member. The carrier is a **1200-byte
truncation** of a 5443592-byte member (`head -c` to the superblock's `bytes_used`), which is what the
committed carve did too.

Tool pins on this host, matching the committed `run.json` pins exactly:
`unblob 26.6.4` sha256 `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`;
`sasquatch-v4be` 4.5.1 (`unsquashfs version 4.5.1 (2022/03/17)`) sha256
`fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`; `rea-agents 6.5.0` from
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`. No tool was installed or upgraded for
this seat (nothing to record under the 2026-10-19 tooling authorization).

## 2. Receipt vs my fresh run — dimension by dimension

Diff script (mine, `artifacts/R40W2ReproV1/compare_v1.py`) compares the committed `after.json` against my
envelope's `.data`; full output `artifacts/R40W2ReproV1/compare.json`. `nonzero_differences: []`.

| dimension | committed `V1/after.json` | my fresh run | equal |
|---|---|---|---|
| chunk `handler` | `squashfs_v4_be` | `squashfs_v4_be` | yes |
| chunk `range` | offset 0, length 5442392 | offset 0, length 5442392 | yes |
| chunk `root_file_range` | 0, 5442392 | 0, 5442392 | yes |
| chunk `extraction_failed` / `encrypted` | `false` / `false` | `false` / `false` | yes |
| raw `ChunkReport` (`handler_name`/`start`/`end`/`size`/`is_encrypted`/`extraction_reports`) | `squashfs_v4_be`, 0, 5442392, 5442392, false, `[]` | identical | yes |
| unblob stdout chunk table | `SQUASHFS_V4_BE │ 5.19 MB │ 100.00% │` | identical | yes |
| `files` | 697 | 697 | yes |
| file path suffix / sha256 / size mismatches | — | **0** | yes |
| files missing / extra | — | **0 / 0** | yes |
| gaps: kinds and counts | `depth-limited` 1, `unpublished-entry` 263 | same | yes |
| gap set `(kind, path suffix)` incl. the null-path structural gap | 264 entries | identical set, 0 missing / 0 extra | yes |
| `unpublished_entries` `(path suffix, kind, link_target)` | 263 | identical set (raw string equality, not just kind counts) | yes |
| `diagnostics` typenames | `[]` (none) | `[]` (none) | yes |
| `coverage` | `partial` | `partial` | yes |
| `published_bytes` | 21681493 | 21681493 | yes |
| `depth_limited_paths` | `["$output/firmware.bin_extract"]` | identical | yes |
| `selection` | 0 / 5442392 / `ac4098bd…8e95` | identical | yes |
| `engine` | unblob 26.6.4, sha256 `0ce7b624…` | identical | yes |
| magic report | `Squashfs filesystem, big endian, version 4.0, xz compressed, 5442392 bytes, 1079 inodes, blocksize: 65536 bytes, created: Wed Mar  4 23:46:32 1970` | identical | yes |
| `extraction_continuations` | `3b54e297…` (raise max_depth), `602c674b…` (retained metadata) | same two ids/instructions | yes |

These two fields necessarily differ between any two runs and are **not** semantic differences:
`chunk.provider_id` / raw `blob_id` (`1726346:1` committed vs `794674:1` mine) is a per-run pipeline id,
and `evidence_id` (`ev_d672b81d…` vs `ev_fcf69806…`) digests the whole record including subject
`local_path` and `parameters`. The frozen counter's projection deliberately drops both (it canonicalises
`unpublished_entries` to `[kind, path suffix]`, `c1-counter.py:122-124,839-842`, and project keys
`subject_sha256, files, chunks, extraction_gaps, unpublished_entries, diagnostics`, `:875-876`), so
neither can mask or fake a match. `parameters.max_depth = 1` is present in both.

The committed receipt is also self-consistent with its own run record: `sha256(after.json) =
98aaa5f90abb434694a26a0599d8bcc6cf6301c35c7aa1befa6de98b00567776`, equal to `run.json`
`receipt.sha256`; `corpus/evidence/round-40/c1/V1/{after,oracle,nonregular}` have no working-tree diff
against HEAD (`git diff --stat HEAD -- corpus/evidence/round-40/c1` empty), and `after.json` was added in
`73c7bf9c` (the C1-receipts revision) and never touched since.

## 3. Oracle cross-check (independent of the receipt)

My fresh extraction's published set equals the frozen independent-reader table **byte-for-byte**:
`LC_ALL=C sort fresh-files.tsv | sha256sum` = `9130bac70b8d10ee09ab23244d8363eb04bfc9325e5fdf159f4b3e6cdfb4b6ef` =
`sha256sum corpus/evidence/round-40/c1/V1/oracle.tsv` (697 rows, `cmp` clean). So the receipt's file list
is not merely internally consistent — it is the oracle's list, produced by a different producer.

Non-regular accounting closes against the superblock: 697 regular + 117 dir + 263 symlink + 1 char device =
1078 entries + root inode = **1079** = `inodes` in the superblock.

One convention difference worth recording (it did not affect V1's score and does not affect the receipt vs
rerun comparison, which matched on the raw strings): the oracle's `nonregular.tsv` `detail` column carries
the symlink target **as stored** (`/var/Country_iso`, `./libavmssl.so.2.0.0`, `ld-uClibc.so.1`), while
REA/unblob publishes the **retargeted** form (`../var/Country_iso`, `libavmssl.so.2.0.0`,
`ld-uClibc-1.0.14.so` — absolute targets made relative, `./` dropped, in-tree chains resolved). For V1,
219/263 are string-identical, 44 differ only that way, and I resolved all 263 inside the extracted tree:
**263/263 resolve to the same final inode**, 0 disagreements. This is exactly the class of comparison
convention that the frozen counter avoids by projecting `(kind, path suffix)` only; I note it so no later
seat reads a raw-target mismatch as a defect.

## 4. Attribution: the handler really is the AVM branch running `sasquatch-v4be` without `-be`

- `unblob -v` log, my carrier: `Found valid chunk chunk=0x0-0x530b58 handler=squashfs_v4_be` (0x530b58 =
  5442392) then `Running extract command command='sasquatch-v4be -no-exit-code -f -d $S/ub1/carrier.bin_extract
  $S/carrier.bin'` — the external BE extractor, **no `-be` flag**, then `Reached maximum depth, stop further
  processing depth=0x1`. Artifact `unblob-verbose-extractor.txt`.
- Independent superblock probe (my own struct/lzma code, `superblock-avm.txt`): magic `sqsh`, BE structural
  fields (inodes 1079, block_size 65536, compression 4 xz, `mkfs_time == bytes_used == 5442392` → AVM
  marker true), while the inode-table metadata header bytes `64 05` read **little-endian 1380** (stored
  flag clear) and xz-decompress to 8192 bytes, versus big-endian 25605 = larger than the 8 KiB maximum
  metadata block. A little-endian read of the superblock is nonsense (inodes 923009024, block_size 256).
  That is precisely the claimed format: BE superblock fields, LE metadata block-length headers.
- The carrier's `bytes_used` equals both the AVM marker and the carve length, so the carrier is the image
  body the marker describes, not a padded or re-cut variant.

## 5. Negative arm: the success is attributable, not vacuous

With `sasquatch-v4be` removed from PATH (it lives only in `~/.local/bin`; nothing in `/usr/bin`), both
producers degrade exactly as the claim's disclosed limits say they should:

- `unblob` 26.6.4: exit **1**, chunk still identified `SQUASHFS_V4_BE`, error table
  `Severity.ERROR | ExtractorDependencyNotFoundReport`, no extraction (`artifacts/…/unblob-nodep-report.txt`).
- REA 6.5.0: envelope `ok=true` (it reports, it does not fail), `files: 0`, chunk
  `handler=squashfs_v4_be`, **`extraction_failed: true`**, one gap `kind=missing-extractor-dependency`,
  `handler=squashfs_v4_be`, `dependencies=["sasquatch-v4be"]`, and one diagnostic with
  `__typename__=ExtractorDependencyNotFoundReport`, `stage=squashfs_v4_be`
  (`artifacts/…/rea-nodep-summary.json`).

So the committed receipt's empty `diagnostics`, `extraction_failed=false`, 697 published files and its
single `depth-limited` structural gap are the signature of a run that **did** have the external extractor
and did extract to depth 1 — the negative arm shows what the same bytes look like without it (0 files, a
`missing-extractor-dependency` gap and a populated diagnostics typename). It also confirms the gap
vocabulary is larger than V1's two kinds, so V1's gap profile is not the trivial one.

## 6. What this does and does not establish

Establishes: the committed V1 receipt is reproducible end-to-end from the public vendor chain and the
pinned toolchain; its file list is the frozen oracle's list; its gaps obey `gap-rule.json` (263
`unpublished-entry` on exactly the 263 symlinks, no duplicates, none on the 117 dirs or the 1 char device,
1 `depth-limited`, 0 `unknown-chunk-handler`, art. `gap-rule-check.txt`); its chunk is the AVM

BE handler with no failed extraction; and the success depends on the external BE extractor.

Does not establish (limits): (a) I am not an independent implementer — same host, same unblob sha256, same
`sasquatch-v4be` sha256 as the committed run, so this is reproduction, not independent-oracle agreement
beyond the oracle cross-check in §3; (b) it cannot say which process wrote the committed `after.json`; a
receipt equal to a real run on the same projection is accepted by design — my run shows such a run exists
today, not that the committed one was it; (c) no extractor argv appears in a successful REA receipt, so
the absence of `-be` is evidenced by the handler branch and the direct `unblob -v` log (§4), not by the
receipt; (d) I did not test V2, L1, L2, the score arithmetic, the frozen-path rule, or the L2
`nonregular_unpublished_ok` reading. [INFERENCE] the `provider_id` stability across reruns is a per-run
pipeline id by construction; I observed two different values for the same bytes and did not read the REA
source to confirm the generator.

## 7. Artifacts

Under `.ufo/waves/round-40/w2/artifacts/R40W2ReproV1/` (no vendor firmware bytes and no extracted vendor
files were copied into the lane; only hashes and my own run metadata):

- `reproduction-chain.txt` — exact commands, exit codes, sizes, hashes, timings, tool pins.
- `compare_v1.py`, `compare.json` — my receipt-vs-rerun diff and its full output (`nonzero_differences: []`).
- `fresh-files.tsv` — my run's 697 `relpath<TAB>sha256<TAB>size` rows (equals `oracle.tsv` after `LC_ALL=C sort`).
- `gap-rule-check.txt` — formal conformance of my run's gaps to `.ufo/waves/round-40/c1/gap-rule.json`.
- `superblock-avm.txt` — independent superblock/marker/metadata-endianness probe.
- `unblob-verbose-extractor.txt` — handler + `sasquatch-v4be` argv (no `-be`) + depth stop.
- `unblob-nodep-report.txt`, `rea-nodep-summary.json` — the no-`sasquatch-v4be` arms.

Scratch `/fast/scratch/hyaku/kaidoku-r40/R40W2ReproV1` (vendor image, member, carrier, extraction trees)
is removed before this seat yields; nothing was written outside this report and the artifacts directory.
