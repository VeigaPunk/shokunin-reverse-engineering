# R36ScribeEntry — knowledge-entry draft: sasquatch SquashFS recursion (R36-C1)

Advisory scribe seat. Read-only on product surfaces. **No lane file was written except this report**; no
VCS mutation; no tool installed; no subagent, no background job, no `agent://all`. Scratch
`/fast/scratch/hyaku/kaidoku-r36/R36ScribeEntry` removed before finishing.

Draft target: `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` (absent at the measured
revision — `ls` → "No such file or directory"). Full markdown is §2. Every number in it is re-derivable
from a committed file whose path is printed next to the number; the only numbers not carried by
`corpus/evidence/round-36/c1` are the deb digest (S107, re-verified live — §4.10) and the v4be digest
(S107 only, not in the receipts).

---

## 1. What I ran (exact commands, outcomes)

| # | Command | Outcome |
|---|---|---|
| 1 | `read …/plans/round-36-claims.md` | Frozen P36-C1/P36-C2 read verbatim (freeze `790561d4`, base `cab59f22`, after receipts `3310d8fa`). |
| 2 | `ls -la corpus/evidence/round-36/c1{,/K1,/K2,/K3,/K4}` | 24 tracked evidence files + `fixtures/`; per-carrier `oracle.tsv`, `oracle-run.json`, `before.json`, `after.json`, `before-run.json`, `after-run.json`. |
| 3 | `python3 -` (read-only) over `K*/{before,after}.json` + `K*/oracle.tsv` | Per-carrier published counts, oracle hits, extras, gaps, bytes, chunk records (all §1.1 numbers). |
| 4 | `read tools/round-36/c1-counter.py:81-232:raw` | Exact predicate implementation: `published()`, `sasquatch_gap()`, `matched()` (sha256 + path-equality-or-`/<rel>`-suffix), binding list. |
| 5 | `read tools/round-36/c1-run.sh` | Oracle method: `hsqs` at offset 0, or `e_shoff + e_shnum*e_shentsize` for AppImages; `/usr/bin/unsquashfs -no-progress -o <off>`; regular files only (`islink`/`isfile` filter); `relpath TAB sha256 TAB size`, sorted. Before mode strips every PATH dir holding an executable `sasquatch`. |
| 6 | `curl` → `raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py` | HTTP 200, 19842 bytes, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`; `cmp` **IDENTICAL** to the installed unblob 26.6.4 handler. Tag is `26.6.4` (no `v`); the assignment's "tag v26.6.4" label does not resolve (`git/refs/tags/v26.6.4` → 404). |
| 7 | `curl` → `api.github.com/repos/neovim/neovim/releases/tags/v0.12.6` | tag `v0.12.6`, published `2026-10-09T15:43:25Z`, target `779c36969e31080503be2dfccbcc3f999e289606`; `nvim-linux-x86_64.appimage` 11454968 B `sha256:b644d034…f29fb`, `nvim-linux-arm64.appimage` 11356680 B `sha256:8efcec73…e1c2` — both equal `carriers.json`. |
| 8 | `curl` → `…/releases/download/sasquatch-v4.5.1-6/sasquatch_1.0_amd64.deb` | 187244 B, sha256 `efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95` (equals S107 digest). `ar x` + `tar -xJf data.tar.xz`: `usr/bin/sasquatch` `ad02d27a…4754`, `usr/bin/sasquatch-v4be` `fac88740…14c6` — both byte-identical to the installed `~/.local/bin` binaries. |
| 9 | `sha256sum ~/.local/bin/sasquatch{,-v4be}`; `… -version` | `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` / `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`; both print `unsquashfs version 4.5.1 (2022/03/17)`. |
| 10 | `python3 -I -B tools/round-36/c1-counter.py --root … --rev 3310d8fa27bfaa95ad858c4aaad6f6377f853982 --freeze 790561d4e3aca732a434081aa9573ec2fa5fd7d0 --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out $S/counter.json` | **`carriers_matched: 4`, `carriers_unchanged: true`, `met_target: false`, exit 1.** All four carriers `matched: true`; `before/after_evidence_id_ok: true` for all eight receipts; `before_sasquatch_gap: true` + `before_oracle_hits: 0`, `after_sasquatch_gap: false` + `after_oracle_hits == oracle_files`. `met_target` is false **only** because the four prose bindings are absent at that revision (`province_core_section/row`, `entry_present`, `sourced`, `coverage_map_row` all false) — the entry has not landed yet. This is the frozen counter's own reading of the committed receipts, not my arithmetic. |
| 11 | `python3 -` over `fixtures/k{1,2}-src` vs `K{1,2}/oracle.tsv` | K1: 3 regular source files, oracle 3 rows, byte-identical `(relpath, sha256)` lists → **True**. K2: 4 regular source files (plus symlink `var/notice-link -> ../usr/share/doc/NOTICE`), oracle 4 rows → **True**. |
| 12 | `git ls-files` / `git ls-tree` (read-only) | Evidence dir fully tracked; `K*/*.json`, `*.tsv`, `fixtures/*` present at `3310d8fa`. `.ufo/waves/round-36/w1/*` is **untracked** (`git ls-files --error-unmatch` → "did not match any file(s) known to git"), so the scout report is cited as a lane working file, never as committed evidence. |

### 1.1 Measured numbers (source of truth for §2)

| carrier | oracle rows | distinct digests | before files | before hits | before bytes | after files | after hits | after extras | after bytes | after chunk records | remaining gaps |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | 3 | 3 | 0 | 0 | 0 | 3 | 3 | 0 | 70086 | 1 | none |
| K2 | 4 | 4 | 0 | 0 | 0 | 4 | 4 | 0 | 273971 | 1 | 1 unpublished-entry (symlink) |
| K3 | 2130 | 2116 | 2 | 0 | 11454968 | 2147 | 2130 | 17 | 51122564 | 27 | 2 unpublished-entry (symlinks) |
| K4 | 2130 | 2116 | 2 | 0 | 11356680 | 2147 | 2130 | 17 | 51792724 | 27 | 2 unpublished-entry (symlinks) |

K3/K4 extras split: 9 `carved.elf` + 8 one-byte `.padding` (all `sha256 6e340b9c…`, which is the sha256
of a single NUL byte) = 17, identical composition in both carriers.

---

## 2. Drafted entry (verbatim; target `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`)

````markdown
source: S107 — https://github.com/onekey-sec/sasquatch/releases/tag/sasquatch-v4.5.1-6 — official sasquatch 4.5.1 Debian release, asset sasquatch_1.0_amd64.deb 187244 bytes sha256 efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95, published 2026-01-27T11:57:51Z; not unblob behaviour, not any carrier
source: S108 — https://github.com/onekey-sec/unblob/blob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — tag 26.6.4 (not v26.6.4), file sha256 2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287: SquashFSExtractor declares EXECUTABLE = sasquatch and V4BE_EXECUTABLE = sasquatch-v4be, and get_dependencies() returns both names
source: S109 — https://github.com/neovim/neovim/releases/tag/v0.12.6 — published 2026-10-09T15:43:25Z; nvim-linux-x86_64.appimage sha256 b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb, nvim-linux-arm64.appimage sha256 8efcec73cea1cebcd3a19da0bc782c0c6d95da7ae6006902a9d93b5ac9efe1c2
verified-at: 2026-10-26; receipts committed at 3310d8fa27bfaa95ad858c4aaad6f6377f853982 against the predicate/carrier/oracle freeze 790561d4e3aca732a434081aa9573ec2fa5fd7d0; the frozen counter reports carriers_matched 4 at that revision
recheck: 180d — tools/round-36/c1-run.sh after corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh /tmp/r36-recheck && jq -c '.normalized_result|{files:(.files|length),gaps:(.extraction_gaps|length)}' /tmp/r36-recheck/after.json

# SquashFS recursion in REA extract-firmware: sasquatch removes the dependency gap, symlinks stay metadata

## Question and novelty

The lane recorded the AppImage SquashFS route as a carve only: `corpus/README.md` `## Coverage map` Firmware
row — "AppImage SquashFS carved but recursion blocked by missing sasquatch" — and `PROVINCE.md`
`### Round-4 frontier (post-unlock)`, bullet `sasquatch` ("unblob's squashfs recursion extractor
(AUR-only); 7z fallback covers the carved-image path today"). Neither statement records the shape of the
blockage, the member list a working recursion would publish, or whether an official sasquatch build closes
it. This entry records the gap record verbatim and the member-level outcome on four frozen carriers against
an independent `unsquashfs` oracle. Measured configuration: REA `rea-agents` 6.5.0 `extract-firmware`,
unblob 26.6.4 (engine `executable_sha256`
`0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`), little-endian SquashFS v4 only.

## Frozen carrier set and oracle counts

Carrier digests are frozen in `corpus/evidence/round-36/c1/carriers.json`; oracle rows and offsets in
`corpus/evidence/round-36/c1/K*/oracle.tsv` and `…/K*/oracle-run.json`.

| carrier | kind (carriers.json) | carrier sha256 | oracle offset | oracle regular-file rows | distinct digests |
|---|---|---|---|---|---|
| K1 | bare SquashFS v4 LE, xz, 128 KiB blocks, synthetic (committed fixture) | `93802938486d952abe0f06a83b55ca882e2272805ea11dcc3c35b9b9c9b8a589` | 0 | 3 | 3 |
| K2 | bare SquashFS v4 LE, gzip, 4 KiB blocks, nested dirs + one symlink (committed fixture) | `ce5bf60e765e9942c1d317cfdd201b8b072b61e546e8dbdb6f87d6fe36a2084f` | 0 | 4 | 4 |
| K3 | shipped AppImage type 2, x86-64 runtime + squashfs payload, neovim v0.12.6 | `b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb` | 944632 | 2130 | 2116 |
| K4 | shipped AppImage type 2, aarch64 runtime + squashfs payload, neovim v0.12.6 | `8efcec73cea1cebcd3a19da0bc782c0c6d95da7ae6006902a9d93b5ac9efe1c2` | 936456 | 2130 | 2116 |

`oracle-run.json` in each carrier also records `unsquashfs version 4.7.5 (2026/03/01)`. K3 and K4 list
2130 rows over 2116 distinct sha256 values — 14 rows share their bytes with another row, and the frozen
predicate matches per oracle row by `(sha256, exact path or /<relpath> suffix)`, so all 2130 rows are
counted individually.

## Without sasquatch on PATH: one dependency gap, zero members

`before` receipts (`K*/before.json`, harness mode `before`, which removes every PATH directory holding an
executable named `sasquatch`; `K*/before-run.json` records `sasquatch: ""`). In all four carriers unblob
emits exactly one extraction gap:

| field | value (all four carriers) |
|---|---|
| `kind` | `missing-extractor-dependency` |
| `handler` | `squashfs_v4_le` |
| `dependencies` | `["sasquatch"]` |
| `input_path` | `$input` (the whole carrier is the chunk for K1/K2; the payload chunk for K3/K4) |
| `root_file_range` | K1 `{0, 73728}`; K2 `{0, 208896}`; K3 `{944632, 10510336}`; K4 `{936456, 10420224}` |
| `continuation_id` | `4ca863d04cc06d61e7be38d0811847a15f55c70f028fdf45e8fefdf75957a07a` (identical in all four) |

The single continuation carries this instruction verbatim (`extraction_continuations[0].instruction`):

> REA installs nothing. Add the named dependency to your own environment and rerun extract_firmware on the same immutable input with a fresh output_directory to re-evaluate the affected region; otherwise it stays unextracted.

`diagnostics` holds one `ExtractorDependencyNotFoundReport`, `severity: ERROR`, `dependencies:
["sasquatch"]`, `stage: squashfs_v4_le`. `coverage` is `partial` in all four.

What is published is the carve, not the members:

- **K1 and K2** — `files: []`, `published_bytes: 0`; the one chunk record is the input itself
  (`input_path: $input`, `root_file_range` = whole file) with `extraction_failed: true`. There is no
  separate payload file to publish because the carrier *is* the payload.
- **K3 and K4** — 2 files published (`published_bytes` 11454968 / 11356680, i.e. the whole carrier): the
  ELF64 runtime carve `firmware.bin_extract/0-<runtime_end>.elf64_extract/carved.elf` and the SquashFS
  payload chunk `firmware.bin_extract/<start>-<end>.squashfs_v4_le`. **Zero** oracle members are among
  them (oracle hits 0/2130). The payload chunk record carries `extraction_failed: true`; the two `elf64`
  records do not. Three chunk records total.

So "carved but recursion blocked" concretely means: the SquashFS chunk is located and either published as
a chunk file (AppImage) or is the input itself (bare image), its members are not extracted at all, and the
only machine-readable remedy is the continuation above — REA does not install the extractor.

## With sasquatch 4.5.1 on PATH: members published, recursion artifacts added

`after` receipts (`K*/after.json`; `K*/after-run.json` records `sasquatch:
/home/vgpnk/.local/bin/sasquatch`, `sasquatch_sha256:
ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`, `sasquatch_version: unsquashfs
version 4.5.1 (2022/03/17)`). `parameters.max_depth` is 3 in all eight receipts and
`depth_limited_paths` is empty in all of them.

| carrier | oracle rows | published files | oracle rows matched | extras (not in oracle) | `published_bytes` | `coverage` | remaining gaps |
|---|---|---|---|---|---|---|---|
| K1 | 3 | 3 | 3 | 0 | 70086 | `complete` | none |
| K2 | 4 | 4 | 4 | 0 | 273971 | `partial` | 1 `unpublished-entry` (symlink) |
| K3 | 2130 | 2147 | 2130 | 17 | 51122564 | `partial` | 2 `unpublished-entry` (symlinks) |
| K4 | 2130 | 2147 | 2130 | 17 | 51792724 | `partial` | 2 `unpublished-entry` (symlinks) |

Path shape: members are published under `<carrier>_extract/` for a bare image and under
`firmware.bin_extract/<chunk-range>.squashfs_v4_le_extract/` for an AppImage, preserving the in-image
relative path as a suffix — hence the predicate's suffix rule rather than equality.

Byte check on K1: 70086 = 59 (`README.txt`) + 27 (`etc/config.ini`) + 70000 (`payload.bin`). On K2: 273971 =
200000 + 73890 + 75 + 6.

### The 17 extras per AppImage are second-level recursion output

K3 and K4 each publish 17 files whose sha256 matches no oracle row, in the same composition:

- 1 `carved.elf` for the AppImage runtime — `firmware.bin_extract/0-944632.elf64_extract/carved.elf`
  (K3, 944632 B) / `…/0-936456.elf64_extract/carved.elf` (K4, 936456 B). This one is *also* published in
  the `before` run; it is a member's peer, not recursion output.
- 8 nested `carved.elf` from ELF carving inside the payload: `usr/bin/nvim` plus the seven
  `usr/lib/nvim/parser/*.so` (c, lua, markdown, markdown_inline, query, vim, vimdoc) — depth 3, the
  configured maximum.
- 8 one-byte `.padding` stubs (e.g. `usr/bin/nvim_extract/11170568-11170569.padding`), all `sha256
  6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d`, the sha256 of a single NUL byte.

No oracle row is left unmatched, and no extra is a member of the squashfs image. **The extras are a
publishing side-effect of recursion, not evidence of image content**: a consumer that treats
`normalized_result.files` as "the image's file list" will over-count by 17 on these carriers (2147 vs 2130).
The frozen predicate is immune to this because it counts matched oracle rows, not published files.

## Symlinks are retained as metadata, so coverage stays "partial"

K2's payload holds `var/notice-link -> ../usr/share/doc/NOTICE`; K3's and K4's payloads both hold
`.DirIcon -> usr/share/icons/hicolor/128x128/apps/nvim.png` and `nvim.png -> usr/share/icons/hicolor/128x128/apps/nvim.png`.
Each appears in `normalized_result.unpublished_entries` as `{kind: "symlink", link_target: …}` and produces
an `extraction_gap` with `kind: "unpublished-entry"`, `handler: null`, `dependencies: []`, and the shared
continuation id `602c674b7f83f4acd6bf01c5655a5dd669f206d33ee3bc9b8bc2c0ba9f08cfca`:

> The entry is retained as metadata; only regular files are published, without executable permission bits.

Two consequences worth keeping: (a) installing sasquatch moves the gap *kind* from
`missing-extractor-dependency` to `unpublished-entry` — it does not make an image with symlinks gap-free,
and `coverage` stays `partial` for K2/K3/K4 while K1 is `complete`; (b) the published regular files lose
executable permission bits, and the frozen oracle does not compare modes anyway.

## Install provenance

- Binary provenance: official onekey-sec release `sasquatch-v4.5.1-6` (S107), asset
  `sasquatch_1.0_amd64.deb`, 187244 bytes, sha256
  `efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95`. Unpacked without `dpkg` (`ar x` +
  `tar -xJf data.tar.xz`); members `usr/bin/sasquatch` (382824 B,
  `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`) and `usr/bin/sasquatch-v4be`
  (436232 B, `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`), both installed under
  `~/.local/bin/` and byte-identical to the deb members. Both report `unsquashfs version 4.5.1
  (2022/03/17)`.
- Receipt-side provenance: every `K*/after-run.json` records the `sasquatch` path, its sha256
  `ad02d27a…4754` and that version line; every `K*/before-run.json` records `sasquatch: ""`. The
  `sasquatch-v4be` digest is **not** in the receipts (it is only exercised by the big-endian path, which no
  carrier here uses).
- Why the fix is a dependency and not a code change: S108 shows `SquashFSExtractor.EXECUTABLE =
  "sasquatch"`, `V4BE_EXECUTABLE = "sasquatch-v4be"`, and `get_dependencies()` returning both, with the
  little-endian command line `-le -no-exit-code -f -d {outdir} {inpath}`. The missing-dependency gap and its
  continuation are therefore unblob's designed behaviour, not an REA defect.

## Oracle method and its limits

Method (`tools/round-36/c1-run.sh`, mode `oracle`): find the SquashFS offset — `0` when the first four bytes
are `hsqs`, otherwise the ELF section-table end `e_shoff + e_shnum*e_shentsize` for an ELF64 LE AppImage
runtime — assert `hsqs` at that offset, run `/usr/bin/unsquashfs -no-progress -o <offset> -d <dir>
<carrier>`, then walk the tree and emit `relpath TAB sha256 TAB size` for **regular files only**, skipping
symlinks, sorted. Counts and offsets are recorded in `K*/oracle-run.json` (`regular_files`, `squashfs_offset`,
`unsquashfs`); the table itself is `K*/oracle.tsv`.

Limits, stated so a reader does not over-read the match:

- **K1/K2 have an independent expected record**: their oracle rows equal the committed source trees
  `corpus/evidence/round-36/c1/fixtures/k1-src/` and `k2-src/` byte for byte, so for these two the oracle is
  not merely a second reader of the same payload.
- **K3/K4 do not.** The oracle is `unsquashfs`'s view of the same payload bytes that sasquatch reads. Both
  implement the same on-disk format, so agreement shows member parity between two independent SquashFS
  implementations, not format independence. Their *carrier* authenticity is separate and does hold: each
  AppImage's sha256 equals the vendor-published release digest (S109).
- Regular files only: symlinks (and therefore link targets), hardlinks, device nodes, FIFOs and directories
  are outside the comparison. Mode, uid/gid, mtime and xattrs are not compared, and are not published anyway.
- One fixed offset rule per carrier, no search for secondary filesystems, no nested-mount traversal.
- Little-endian SquashFS v4 only; `unsquashfs` 4.7.5 on this host only (a different unsquashfs is a
  different expected-author record).

## What this is not claimed to show

- **No big-endian or AVM result.** All four carriers are LE v4. S108 shows the handler's BE path selecting
  `sasquatch-v4be`, appending `-be`, and omitting `-be` when `header.bytes_used == header.mkfs_time` (the
  AVM heuristic). That is source reading; nothing here exercises it.
- **No vendor-mangled image result.** Broadcom (`qshs` magic) and other non-standard SquashFS handlers exist
  in the same file (S108); no carrier uses them.
- **No 7z-fallback comparison** (the base knowledge's old workaround is not re-tested).
- **No behaviour of the extracted programs.** Nothing was executed; the 2130 members are hashed bytes.
  Running an AppImage runtime or its payload is a separate, code-executing act.
- **Not gap-free extraction.** K2/K3/K4 keep an `unpublished-entry` gap for symlinks; only the
  missing-extractor-dependency gap disappears.
- **No claim about other REA verbs, other providers, other unblob versions or rea-agents 6.7.0**, and no
  security/authenticity claim about sasquatch or the neovim assets beyond digest equality.

## Sources

| id | source | what it grounds here | what it does not |
|---|---|---|---|
| S107 | onekey-sec/sasquatch release `sasquatch-v4.5.1-6` | the two installed binaries' provenance and digests, the release/publish date | unblob behaviour, source-to-binary provenance, any carrier |
| S108 | unblob `squashfs.py` at tag `26.6.4` | that `sasquatch`/`sasquatch-v4be` are declared extractor dependencies, the LE/BE command lines, the AVM heuristic | unblob's traversal engine, REA's gap/continuation wording, any carrier |
| S109 | neovim release `v0.12.6` | the published AppImage digests that K3/K4 must equal | AppImage runtime behaviour, the packaged programs |

## Receipts

| carrier | before evidence id | after evidence id |
|---|---|---|
| K1 | `ev_df7bef526779b3062cc0a8f149f6c32a2b5849ac2f40150df58b69df00178da3` | `ev_b5bd2e7f0ea0b9f6e65d04d68826507464983c2d226b6fa4c542f4dcf64fc860` |
| K2 | `ev_7506d2a8715ac018b5b2f7aa1f1c16dd43d78c5f1bbd489fa19ceba6d5767b3c` | `ev_c939cd88f616e8759ed2c8656f98745fd8e90aa6589a744b25f33b6366b0c88f` |
| K3 | `ev_91e4ab30b6a5edf4ab7a14d5a14867cac75b0e161090c5db7db6b73027e9a44a` | `ev_b83bd3056f103a72e2a611a5162f542715119490a44bb60135393b5002f5419b` |
| K4 | `ev_fffca90bc4b70989308fcc378c3cdefdd5baaf8ee878d8e624dc31709f5b1a01` | `ev_ff0fdb798eea077df0b11dcdd3795794c9069c667424b85c5f67f566c97379fa` |

Hashes are in `corpus/evidence/round-36/c1/K*/{before,after}.json` (stored `evidence_id`); the receipts are
committed at `3310d8fa27bfaa95ad858c4aaad6f6377f853982`, the predicate/carrier/oracle freeze at
`790561d4e3aca732a434081aa9573ec2fa5fd7d0`, the pre-claim base at
`cab59f221fe19726b5692bfa4d9a9679e96b8a73`. The frozen counter re-derives each stored id under the
rea-agents 6.5.0 rule and reports `before_evidence_id_ok` and `after_evidence_id_ok` true for all four
carriers.
````

---

## 3. Draft `corpus/SOURCES.md` rows (11 cells each; not written by this seat)

The counter accepts a row only if it has exactly 11 cells, `cells[0]` is the id, `cells[8] == "2026-10-26"`,
and `cells[10]` (used-by) contains `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`. No cell
may contain `|`. S107 is the last source id in `corpus/SOURCES.md` at `3310d8fa` (last registry row: S106);
S107/S108/S109 are free.

```
| S107 | onekey-sec/sasquatch release sasquatch-v4.5.1-6 — https://github.com/onekey-sec/sasquatch/releases/tag/sasquatch-v4.5.1-6 | code | A | The official sasquatch 4.5.1 Debian-package release: asset set, publish date and amd64 package digest; not unblob recursion behaviour, not any carrier, not a verdict | Published 2026-01-27T11:57:51Z; asset sasquatch_1.0_amd64.deb 187244 bytes sha256 efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95; its usr/bin/sasquatch sha256 ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754 and usr/bin/sasquatch-v4be sha256 fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6; re-downloaded 2026-10-26, both members byte-identical to the installed ~/.local/bin copies | Names the provenance and digests of the binaries REA extract-firmware needs for SquashFS recursion, so an install can be checked byte-for-byte | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md |
| S108 | unblob SquashFS handler at tag 26.6.4 — https://github.com/onekey-sec/unblob/blob/26.6.4/python/unblob/handlers/filesystem/squashfs.py | code | A | How SquashFSExtractor declares and invokes its extractor dependencies for SquashFS v1-v4, including the v4-BE executable choice and the AVM heuristic; not unblob's traversal engine, not REA's gap wording, not any carrier | Tag `26.6.4` (published 2026-06-04T08:52:43Z; the tag is not `v26.6.4`); file 19842 bytes sha256 2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287, byte-identical to the installed unblob 26.6.4 handler; SquashFSExtractor block lines 24-71 | Explains why a SquashFS chunk yields a missing-extractor-dependency gap naming sasquatch, and which command line recursion uses | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md |
| S109 | neovim v0.12.6 release — https://github.com/neovim/neovim/releases/tag/v0.12.6 | code | A | The published AppImage assets and their GitHub digests for the measured release; not AppImage runtime behaviour, not the packaged programs | Published 2026-10-09T15:43:25Z, target 779c36969e31080503be2dfccbcc3f999e289606; nvim-linux-x86_64.appimage 11454968 bytes sha256 b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb; nvim-linux-arm64.appimage 11356680 bytes sha256 8efcec73cea1cebcd3a19da0bc782c0c6d95da7ae6006902a9d93b5ac9efe1c2 (API assets[].digest) | Pins carriers K3 and K4 to a vendor-published digest, so the oracle compares member hashes of an authenticated image | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md |
```

If the lane prefers `tool` for a release-asset row (S001/S002 convention) instead of S107's `code`, that is
a convention call for L1 — the entry text is unaffected.

---

## 4. Bindings the entry needs that this seat did not write

The counter's `bind_ok` requires five things; three are outside a scribe's write scope. Reported, not done:

1. `province_core_section` + `province_core_row` — `PROVINCE.md` has **no** `## Round-36 additions to Core`
   heading at `3310d8fa` (counter: both false; `grep -n "Round-36" PROVINCE.md` → no match). The row must sit
   under exactly that heading, have `sasquatch` as a whole token in its **first cell**, and contain
   `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`.
2. `coverage_map_row` — one `|`-leading line inside `corpus/README.md` `## Coverage map` must contain the stem
   `2026-10-26-r36-sasquatch-squashfs-recursion` (the Firmware row is the natural home; its current text still
   says "recursion blocked by missing sasquatch").
3. `sourced` — the three rows in §3 must be appended with opened `2026-10-26` and the entry in used-by.

The `### Round-4 frontier (post-unlock)` bullet `sasquatch` also still reads "(AUR-only)". That is a factual
drift against S107 (the upstream project publishes an official Debian package, which is what the after-run
used); correcting it is L1's call, since removing a Frontier bullet is a PROVINCE edit, not a scribe act.

---

## 5. Findings (reported, not repaired)

- **F1 — the after receipts are not gap-free.** K2/K3/K4 keep `unpublished-entry` gaps for symlinks and
  `coverage: partial`. Anything that reads the after-run as "extraction now succeeds" overstates it; the frozen
  predicate is correctly scoped (`after_sasquatch_gap == false`, i.e. no `missing-extractor-dependency` naming
  sasquatch — not "no gaps"). Calibration cost if misread: 3 of 4 carriers look clean when they are only
  dependency-clean.
- **F2 — published-file count ≠ member count.** 2147 published vs 2130 members on each AppImage (17 extras:
  9 carved ELFs + 8 one-byte padding stubs). The entry states this explicitly; a future counter that counted
  `files` instead of oracle hits would drift by 17 per AppImage.
- **F3 — k3/k4 oracle rows double-count content.** 2130 rows / 2116 distinct digests, and the predicate counts
  rows. Not a defect (the rule is frozen and stated), but a reader who assumes "2130 distinct files" is wrong
  about 14 of them.
- **F4 — the v4be dependency is declared but untested.** S108 `get_dependencies()` returns both binaries, and
  the gap reports only `["sasquatch"]` for these LE carriers. A host with `sasquatch` but without
  `sasquatch-v4be` would still report no gap for a v4-LE image and fail on a big-endian one. No carrier tested
  that split.
- **F5 — assignment wording vs tag name.** The task text says "unblob squashfs.py at tag v26.6.4"; upstream tag
  is `26.6.4` (the `v`-prefixed ref 404s). The draft entry and the S108 row carry the resolvable URL.
- **F6 — S107's provenance surface is untracked.** The deb digest used by the scout lives in
  `.ufo/waves/round-36/w1/R36ScoutSasquatchRelease.md`, which is not tracked by git. I re-derived the digest
  and both member hashes live (§1 rows 8–9) so the number in the entry does not depend on that file alone.
- **F7 — K1/K2 oracle independence is stronger than K3/K4's.** Only the fixtures' source trees make the oracle
  independent; for K3/K4 the oracle shares the SquashFS format assumption with sasquatch. The entry states this
  in the oracle-limits section; it is not a defect, but it bounds what "2130/2130 matched" proves (member
  parity, not format independence).

---

## 6. Gates observed

| gate | state | evidence |
|---|---|---|
| Kill rule (CTL-C1-0/1/2 must not meet target) | holds — all three exit 1, `met_target: false`, `carriers_matched: 0` | `.ufo/waves/round-36/controls/ctl-c1-*.out` (read verbatim) |
| Carriers matched at the after-receipts revision | **4 / 4**, `carriers_unchanged: true` | frozen counter, `--rev 3310d8fa…` (command 10) |
| Evidence-id recompute (both modes, all carriers) | true ×8 | same counter run |
| Predicate `met_target` | **false** at `3310d8fa`, exit 1 — only the five prose bindings are missing (§4) | same counter run |
| Entry present | false (this is the draft) | `ls` |

I did not run the selftest (`--selftest`); it is outside a scribe's remit and its 14 cases are the L1's
kinetic surface.

---

## 7. Touched surfaces

- Written: `.ufo/waves/round-36/w1/R36ScribeEntry.md` (this file) — the only lane write.
- Read-only: `plans/round-36-claims.md`, `corpus/evidence/round-36/c1/**`, `tools/round-36/{c1-counter.py,
  c1-run.sh}`, `corpus/SOURCES.md`, `corpus/README.md`, `PROVINCE.md`, `corpus/knowledge/2026-10-23-r34-elf-version-needs.md`
  (style reference), `.ufo/waves/round-36/{controls/*.out,w1-spec.json,w1-gen.py,w1/R36ScoutSasquatchRelease.md}`.
- Scratch: `/fast/scratch/hyaku/kaidoku-r36/R36ScribeEntry` (fetches + counter receipt), removed.
- No VCS mutation; `git` used only as `ls-files`, `ls-tree`, `log`, `check-ignore`, `rev-parse`.

## 8. Out of scope / not done

- Entry, SOURCES rows, PROVINCE Core row, README coverage-map row, and the Frontier bullet correction were
  **not written** — drafted only (§2, §3, §4).
- No selftest run, no C2 measurement, no control re-run, no re-execution of extract-firmware.
- No security review of the installed binaries (that is the sentinel's seat).
- No BE/AVM or vendor-mangled-image carrier was built or tested (explicitly not claimed by P36-C1).

## 9. Tooling record

Nothing installed, upgraded or removed. Used host `curl`, `ar`, `tar`, `sha256sum`, `python3`, `jq`, `node`
(via the frozen counter), `npx` only inside `c1-run.sh`'s own command line (not executed by me). No pacman
transaction was attempted (host-wide pause respected). `sasquatch` 4.5.1 was already installed by L1 and was
neither reinstalled nor removed.

## 10. Limits of this report

- All per-carrier numbers come from committed files under `corpus/evidence/round-36/c1`; the recomputation is
  the frozen counter's (`carriers_matched: 4`), plus my own read-only aggregation. Both agree.
- The deb/v4be digests and the two GitHub release facts are **live observations on 2026-10-26**, recorded in §1
  rows 6–9 with expected values; they are not stored in the lane's evidence tree.
- Line numbers quoted for S108 (`lines 24-71`) are from the byte-identical local file, not from rendered HTML.
- Inference is marked where used: the extras-composition reading (which recursion level produced each file) is
  derived from path shape and chunk records, not from an unblob traversal log — [INFERENCE] on the depth
  attribution only; the file names, sizes and digests are observation.
