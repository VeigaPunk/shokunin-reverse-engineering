# R36ExecSasquatchDirect — direct sasquatch 4.5.1 run against the frozen C1 carriers

Round 36, wave 1. Advisory findings only: no frozen predicate, counter, carrier or oracle was
changed. Read-only access to the lane; scratch under `/fast/scratch/hyaku/kaidoku-r36/R36ExecSasquatchDirect`
(removed on exit). No tool installed or upgraded (sasquatch 4.5.1 already present per L1).

## Question

Does the installed `sasquatch` 4.5.1 binary, invoked with the **exact argv unblob 26.6.4 builds**,
reproduce the frozen unsquashfs 4.7.5 oracle on K1/K2/K3 — and does it reproduce the committed REA
`after.json` receipts? Plus: dynamic deps and `sasquatch-v4be -help`.

## 1. Exact argv, read from the installed handler

`/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`

- L25–26: `EXECUTABLE = "sasquatch"`, `V4BE_EXECUTABLE = "sasquatch-v4be"`
- L54: `Endian.LITTLE` → `commands_args.append("-le")`
- L56–62: `commands_args.extend(["-no-exit-code", "-f", "-d", "{outdir}", "{inpath}"])`

Resolved argv for a little-endian image: **`sasquatch -le -no-exit-code -f -d <out> <img>`** — matches
the assignment's argv exactly. `unblob --version` → `26.6.4`; handler resolves through
`~/.local/bin/unblob` → `~/.local/share/uv/tools/unblob/bin/unblob`.

Note (relevant to the after-receipts being gap-free): `get_dependencies()` (L68–69) returns **both**
`sasquatch` and `sasquatch-v4be`, so the after run needs both names resolvable on PATH, not just the
LE one.

## 2. Binary identity and dynamic deps

| check | result |
|---|---|
| `sasquatch -version` | `unsquashfs version 4.5.1 (2022/03/17)` |
| `sasquatch-v4be -version` | `unsquashfs version 4.5.1 (2022/03/17)` |
| sha256 `sasquatch` | `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` (equals `sasquatch_sha256` in every `after-run.json`) |
| sha256 `sasquatch-v4be` | `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6` (distinct binary, not a copy/symlink) |
| `file` | ELF 64-bit LSB pie, x86-64, dynamically linked, stripped, BuildID `96e3fa39…` (v4be: `8facea80…`) |
| `sasquatch-v4be -help` | exit **0**, prints full SYNTAX/OPTIONS block |
| `sasquatch -help` | exit **0** |
| `command -v` / `shutil.which` | `/home/vgpnk/.local/bin/sasquatch`, `/home/vgpnk/.local/bin/sasquatch-v4be` (PATH entry 4) |

`ldd ~/.local/bin/sasquatch` (all resolve, no `not found`):

```
libpthread.so.0, libz.so.1, liblzma.so.5, liblzo2.so.2, liblz4.so.1, libzstd.so.1,
libstdc++.so.6, libm.so.6, libgcc_s.so.1, libc.so.6, ld-linux-x86-64.so.2
```

`ldd ~/.local/bin/sasquatch-v4be` is the same set. All seven decompressor libs needed by squashfs v4
(zlib, lzma, lzo2, lz4, zstd) are present, so no compression path is silently unavailable on this host.

## 3. Carrier digests (pre-run gate)

All four match `corpus/evidence/round-36/c1/carriers.json` before any run:

```
93802938486d952abe0f06a83b55ca882e2272805ea11dcc3c35b9b9c9b8a589  fixtures/k1-le-xz.sqsh
ce5bf60e765e9942c1d317cfdd201b8b072b61e546e8dbdb6f87d6fe36a2084f  fixtures/k2-le-gzip.sqsh
b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb  nvim-linux-x86_64.appimage
8efcec73cea1cebcd3a19da0bc782c0c6d95da7ae6006902a9d93b5ac9efe1c2  nvim-linux-arm64.appimage
```

K3/K4 were copied (read-only source, digest re-verified in my scratch) from
`/fast/scratch/hyaku/kaidoku-r36/L1/carriers/`. K3/K4 squashfs offsets taken from the committed
`K*/oracle-run.json`: **K3 = 944632**, **K4 = 936456**. Carves: `tail -c +<off+1> <appimage>`, giving
10510336 B (K3) and 10420224 B (K4); both begin `68 73 71 73` (`hsqs`, LE magic) and both sizes equal
`11454968-944632` / `11356680-936456`, i.e. the receipt chunk ranges `944632-11454968` and
`936456-11356680` exactly.

## 4. Runs (exact argv, exit codes captured without a pipe)

```
~/.local/bin/sasquatch -le -no-exit-code -f -d "$S/out-k1" corpus/.../fixtures/k1-le-xz.sqsh   -> exit 0
~/.local/bin/sasquatch -le -no-exit-code -f -d "$S/out-k2" corpus/.../fixtures/k2-le-gzip.sqsh  -> exit 0
~/.local/bin/sasquatch -le -no-exit-code -f -d "$S/out-k3" "$S/k3-carve.sqsh"                  -> exit 0
~/.local/bin/sasquatch -le -no-exit-code -f -d "$S/out-k4" "$S/k4-carve.sqsh"                  -> exit 0
```

Self-reported totals (stdout):

| carrier | files | dirs | symlinks | hardlinks | stderr |
|---|---|---|---|---|---|
| K1 (xz, 128 KiB) | 3 | 2 | 0 | 0 | 1 pair `Trying…/Successfully decompressed with default xz decompressor` |
| K2 (gzip, 4 KiB) | 4 | 7 | 1 | 0 | 21 pairs `…default gzip decompressor` (one per block group; noise, no error) |
| K3 (zstd) | 2130 | 115 | 2 | 0 | 1 pair `…default zstd decompressor` |
| K4 (zstd) | 2130 | 115 | 2 | 0 | 1 pair `…default zstd decompressor` |

## 5. Comparison with the frozen oracle (`K*/oracle.tsv`)

Per row: same relative path, recomputed sha256 over the extracted bytes, same size.

| carrier | oracle rows | matched | missing | sha/size mismatch | extra published |
|---|---|---|---|---|---|
| K1 | 3 | **3** | 0 | 0 | 0 |
| K2 | 4 | **4** | 0 | 0 | 0 |
| K3 | 2130 | **2130** | 0 | 0 | 0 |
| K4 | 2130 | **2130** | 0 | 0 | 0 |

4267/4267 oracle rows reproduced byte-for-byte, with no extra regular file published. This is
independent of the REA receipts: the sha256s were recomputed from sasquatch's own output files.

## 6. Parity with the committed REA after-receipts

Compared `after.json` `normalized_result.files[]` (prefix stripped:
`<off>-<end>.squashfs_v4_le_extract/`, `firmware.bin_extract/`) against my direct extraction.

| carrier | receipt squashfs files | direct files | only-in-receipt | only-in-direct | sha/size diff |
|---|---|---|---|---|---|
| K1 | 3 | 3 | 0 | 0 | 0 |
| K2 | 4 | 4 | 0 | 0 | 0 |
| K3 | 2131 | 2130 | 1 | 0 | 0 |
| K4 | 2131 | 2130 | 1 | 0 | 0 |

The single only-in-receipt entry on K3/K4 is `0-944632.elf64_extract/carved.elf`
(`0-936456.…` on K4) — the AppImage runtime ELF that unblob carves from the region *before* the
squashfs offset, not a squashfs-published file. A further 16 entries per AppImage are nested
recursion artifacts of other handlers (`*/_extract/*/carved.elf`, `*.padding`); all were excluded
from the squashfs comparison and none collide with an oracle path. Conclusion: the direct binary and
the committed pipeline produce identical squashfs file sets and identical sha256s.

## 7. Gap inventory in the receipts (relevant to the C1 predicate's "no sasquatch extraction gap")

- **before.json (all four)**: exactly one gap each — `kind = missing-extractor-dependency`,
  `dependencies = ["sasquatch"]`, `handler = squashfs_v4_le`; squashfs chunk
  `extraction_failed = true`; published files 0/0/2/2.
- **after.json (all four)**: `grep -o 'sasquatch'` → **0** occurrences in each; **0**
  `missing-extractor-dependency` gaps; the `squashfs_v4_le` chunk has `extraction_failed = false`.
- Residual after-gaps are `kind = unpublished-entry` only: K2 one (`var/notice-link`), K3/K4 two each
  (`.DirIcon`, `nvim.png`). I verified these three are **symlinks** in the images
  (`.DirIcon -> nvim.png`, `nvim.png -> usr/share/icons/hicolor/128x128/apps/nvim.png`,
  `var/notice-link -> ../usr/share/doc/NOTICE`) and that `oracle.tsv` (regular files only) contains
  none of them — consistent, not a defect. `tools/round-36/c1-counter.py:124-127` filters on
  `kind == 'missing-extractor-dependency'` and `'sasquatch' in dependencies`, so these
  `unpublished-entry` gaps do not affect the predicate.

## 8. Falsifier probes (negative controls)

| probe | command | result |
|---|---|---|
| un-carved AppImage | `sasquatch -le -no-exit-code -f -d out nvim-linux-x86_64.appimage` | **exit 1**, stderr `Non-standard SquashFS Magic: 'ELF'` + `FATAL ERROR: Block size or block_log too large. File system is corrupt.` → the dd carve is load-bearing; sasquatch does not honour the AppImage offset itself. |
| same, without `-no-exit-code` | `sasquatch -le -f -d out2 <appimage>` | **exit 1**, identical stderr → `-no-exit-code` does **not** mask a fatal superblock error; it only affects non-fatal extraction status. The pipeline cannot silently pass a corrupt image on this path. |
| pre-existing outdir **with** `-f` | `-d` pointed at a dir holding a stale `README.txt` | exit 0; `README.txt` overwritten to the oracle sha `88dc952a…d595961` → `-f` is what makes unblob's pre-created outdir work. |
| pre-existing outdir **without** `-f` | same dir, `-f` dropped | **exit 1**, `FATAL ERROR: dir_scan: failed to make directory …/etc, because File exists` → dropping `-f` from the argv breaks extraction. |
| `sasquatch-v4be` on a non-image | `sasquatch-v4be -ls /dev/null` | exit 1 (expected; binary is functional, not a stub) |
| determinism | K3 re-run into a fresh dir, whole-tree `sha256sum` diff | **IDENTICAL**; K1 re-run likewise **IDENTICAL** |

File modes are preserved from the image (`AppRun` and `usr/bin/nvim` 0755, `nvim.desktop` and
`c.so` 0644), so the extraction is not flattening permissions.

## 9. Findings

1. **The direct binary satisfies the C1 surface for K1/K2/K3** (and K4, same run shape): the exact
   unblob argv on sasquatch 4.5.1 publishes every regular file of the unsquashfs 4.7.5 oracle with
   identical sha256 and size, no extra regular files, no sasquatch gap, deterministically.
2. **No cross-version divergence observed.** sasquatch 4.5.1 vs the oracle's unsquashfs 4.7.5 agree
   byte-for-byte on 4267 regular files across xz/gzip/zstd squashfs v4 LE images. `[INFERENCE]` this
   agreement is not evidence about formats outside the four carriers (no BE/AVM, no vendor mangling,
   no xattr or hardlink coverage beyond `created 0 hardlinks`).
3. **`sasquatch-v4be` presence matters for the after run** even though no BE carrier is measured:
   `get_dependencies()` names both binaries, so a missing `sasquatch-v4be` would still produce a
   dependency gap and could block `met_target`. Both are installed and both `-help`/`-version` run.
4. **The after receipts' `coverage: partial` on K2/K3/K4 is symlink-driven**, not a squashfs
   extraction failure — see §7. Any future predicate wording that keys on `coverage == "complete"`
   rather than on the gap kind would misread these receipts.
5. **No defect found in the installed binary or the argv transcription.** `-no-exit-code` is
   confirmed not to be a failure-masking hazard for superblock corruption.

## 10. Limits

- K3/K4 were carved offset→EOF, matching the receipts' chunk ranges; the exact-bytes_used carve was
  not separately probed (unblob's own chunk end here was already EOF).
- The comparison covers regular-file content and mode only. Symlink targets were read for
  classification (§7) but not compared per-row, since the oracle excludes symlinks.
- No unsquashfs 4.7.5 re-run was performed; the oracle files were taken as frozen input.
- Scratch `/fast/scratch/hyaku/kaidoku-r36/R36ExecSasquatchDirect` removed before yield; every cited
  path is either in the lane or in §2–§4's quoted output. Nothing written outside this report.
