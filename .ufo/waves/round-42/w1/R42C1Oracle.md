# R42C1Oracle — SquashFS v1–v3 multi-producer oracle (round 42, wave 1)

**DONE** — `sqfs3-oracle.py` (sha256
`9e03f9349db21c6a92a82ba96321401746df6fc7deb47fc739d1d99311547bdb`) builds the
round-41 oracle tables from the L1's decided pair — **backhand-cli primary +
7-Zip second, unsquashfs 4.7.5 third wherever it reads** — with a 30-check
`--selftest` green, and it was exercised on 42 inputs: **40 exit 0, 2 exit 2**
(the two v4 round-41 carriers, which the version gate refuses), **zero exit 3**.
Legacy-LZMA v3 — the boundary that made unsquashfs unusable as producer 1 — is
now covered: backhand reads it, and on the L1's dev OpenWrt 7.09 brcm47xx image
the oracle reproduces the L1's own independent check exactly (156 regular files,
163 symlinks, 362 entries, backhand and 7z identical).

Artifacts: `.ufo/waves/round-42/w1/artifacts/R42C1Oracle/`
(`sqfs3-oracle.py`, `run-matrix.sh`, `matrix.tsv`, `selftest.txt`,
`magic-support.md`, `fixtures/` + `MANIFEST.tsv`, `runs/`, `openwrt/NOTES.md`).

## 1. Producer set and what each one contributes

```
python3 -I sqfs3-oracle.py --work <dir> --files <oracle.tsv> \
        --nonregular <nonregular.tsv> --json <oracle-run.json> <image>
```

The four flags R42C1Run's harness greps for are advertised in `--help`
(`--work`, `--files`, `--nonregular`, `--json`), plus `--offset`,
`--backhand`, `--backhand-kind`, `--no-normalize-magic`, `--dev-allow-v4`,
`--probe`, `--keep-work`, `--selftest`.

| role | binary | listing | extraction | gives |
|---|---|---|---|---|
| **primary** | `unsquashfs-backhand` 0.25.5 (sha256 `88cf3ba5…72f`) | `-k <kind> -l` (path set only: no kinds, no sizes, no targets) | `-k <kind> -d <work>/root-backhand -f` | tree → dir/symlink/regular kinds, **symlink targets** (`readlink`), regular sha256/size; **reads legacy-LZMA v3** |
| **second** | `7z` 26.04 (sha256 `f802383f…ad4`) | `l -tSquashFS -slt` (path set, kind from `Mode`, sizes, archive header) | `x -tSquashFS -y` | kind cross-check, regular sha256/size, the compressor statement |
| **third** | `unsquashfs` 4.7.5 (sha256 `461e1fd9…67c`) | `-lls -no-progress` | `-d <work>/root-unsquashfs -no-xattrs -f` | **device major/minor** and link targets from the listing; reads gzip v1–v3 only |

The primary and 7z must agree on the path set, on `dir|symlink|regular` kinds and
on every regular `relpath/sha256/size`; when unsquashfs also reads the image, it
must agree as well and its symlink targets are compared against backhand's.
`cross_check` records `pair`, `third_producer`, `pair_mismatches`,
`third_mismatches`, `detail_mismatches`, `verdict`, `mismatch_count`, `first_20`
(kept flat so the frozen harness contract still binds). `producers.<name>.role`
labels the three; `producers.backhand.kind` and `.attempts` record which backhand
kind was used and why (`~/.local/.../unsquashfs-backhand` is auto-discovered;
`--backhand` / `$UNSQUASHFS_BACKHAND` override; `--backhand-kind` forces).

Exit codes: **0** agree + both tables written; **2** unreadable/unsupported
(`not_squashfs`, `truncated`, `unsupported_version`, `producer_missing:7z`,
`no_primary_producer`, `producer_incomplete:*`); **3** disagreement or
`path_not_representable`. Scratch is `--work` or `$TMPDIR`; with neither the run
is refused (no implicit `/tmp`).

## 2. Selftest (`--selftest`, 30 checks, 0 failures)

Green: magic table, backhand kind candidates per superblock/endianness (and the
v4 gate), all three listing parsers, the 7z header parse, size fill, backhand
tree → kinds + `readlink` target, primary pair agreement, third producer
agreement, magic-normalisation round-trip, bytewise table order, row counts, a
space-bearing path.
Red: sha / size / kind disagreement, path present in one producer only, a
kind the extraction *must* materialise but did not (`kind_missing`), a symlink
target disagreement between backhand and unsquashfs (`detail_mismatch`),
duplicate paths in each of the three listings, junk magic (`not_squashfs`), v4
superblock (`unsupported_version`), and a TAB-bearing path
(`path_not_representable`). `selftest.txt` is the captured run.

## 3. Validation matrix — 42 inputs (`matrix.tsv`, per-input `runs/`)

| group | inputs | outcome |
|---|---|---|
| `squashfs_v3` LE/BE × {nopad, 1kpad, 4kpad} | 8 | exit 0; backhand `le_v3_0`/`be_v3_0`, three producers agree |
| `squashfs_v3_ddwrt` (`hsqt`/`tqsh`; LE canonical is `hsqs`, BE has no canonical file) | 7 | exit 0 after 4-byte magic normalisation |
| `squashfs_v3_broadcom` (`shsq`/`qshs`) | 8 | exit 0 after normalisation |
| `squashfs_v3_nonstandard` (`zlqs`/`sqlz`) | 8 | exit 0 after normalisation |
| `squashfs_v3_adaptive` (LE+BE, legacy LZMA) | 2 | **exit 0** — backhand `le_v3_0_lzma`/`be_v3_0_lzma` + 7z, unsquashfs not a producer |
| `v4/*` (dev only, `--dev-allow-v4`) | 3 | exit 0; every kind exercised |
| OpenWrt Kamikaze 7.09 x86 / 7.09 brcm-2.4 / 8.09.2 brcm-2.4 / 7.09 brcm47xx | 4 | **exit 0** (LZMA-3), see §5 |
| round-41 carriers L3/L4 (v4 BE) | 2 | exit 2 `unsupported_version` (gate works) |

Totals: **40 × exit 0, 2 × exit 2, 0 × exit 3**; 976 regular rows emitted; 35 of
the 41 agreeing runs had unsquashfs as third producer (all six LZMA-3 images
did not). backhand kinds used: `le_v3_0` 16, `be_v3_0` 15, `le_v3_0_lzma` 5,
`be_v3_0_lzma` 1, `le_v4_0` 4. Fixtures are the unblob 26.6.4 MIT files, copied
into `fixtures/` with a per-file sha256 and source URL (`MANIFEST.tsv`);
third-party images are cited by URL + sha256 + carve command
(`openwrt/NOTES.md`), never copied.

Additional measured checks:

* **L1 cross-check reproduced** — on the 7.09 brcm47xx chunk
  (`runs/external/owrt__brcm47xx-2.6.sqfs/`) the oracle reports backhand and 7z
  each at 362 entries = 156 regular + 43 dir + 163 symlink, 0 mismatches: the
  same 156/156 regular and 163 symlinks the L1 measured independently.
* **Scale / hostile names** — locally generated 12 KiB v4 image
  (`runs/external/scale-v4-dev/`, sha256 `c5ee82b5…390`, recipe in the
  directory): 520 entries = 301 regular, 210 dir, 4 symlink, 2 char-device,
  1 block-device, 1 fifo, 1 socket; names with space, `+ = : ; $ & # @ ~ ' [ ]`,
  the literal ` -> `, UTF-8; symlinks relative-escaping, absolute, dangling,
  `..`. All producers agree, 0 mismatches.
* **Determinism** — the same fixture run twice gives byte-identical tables
  (`638a6f75…d23` both times; empty `nonregular.tsv` = `e3b0c442…b855`).
* **Carved offset** — a gzip v3 fixture with 512 junk bytes prepended,
  `--offset 512`, agrees and emits the same two rows as the offset-0 run.
* **Round-41 counter compatibility** — `tools/round-41/c1-counter.py`
  `parse_oracle()` / `parse_nonregular()` accept the tables (4 rows, and 5 rows
  with all four device/fifo/socket kinds, `err=None`). No parser change needed.
* **Only pure readers touched published bytes** — no REA, no unblob, no
  extractor ran on any candidate this seat. The four OpenWrt images were read
  with `unsquashfs`, `7z` and `backhand` only (backhand is a reader, and the
  ticket allows the oracle seats to read candidates); `sasquatch` was run once,
  on the 7.09 x86 chunk which the ticket designates DEVELOPMENT, purely to
  record that the tool under test reads LZMA-3.

## 4. Native magic support (measured; `magic-support.md`)

| magic | backhand 0.25.5 | `unsquashfs` 4.7.5 | `7z` 26.04 |
|---|---|---|---|
| `hsqs` (LE) / `sqsh` (BE) | reads | reads | reads |
| `shsq`/`qshs` Broadcom | **reject** | **reject** | reads |
| `hsqt`/`tqsh` DD-WRT | **reject** | **reject** | **reject** |
| `zlqs`/`sqlz` non-standard | **reject** | **reject** | **reject** |

Backhand was probed with explicit `-k le_v3_0` / `-k le_v3_0_lzma` **and** with
its own auto-detect (which prints `Failed <kind>:` for all thirteen kinds): every
vendor magic fails, and the same bytes with four magic bytes standardised read
fine. 7z declares the same set from the inside (`7z i`: `h s q s || s q s h ||
s h s q || q s h s`). The tool therefore writes one copy under `--work` with
those bytes standardised (`hsqt|zlqs|shsq -> hsqs`, `tqsh|sqlz|qshs -> sqsh`),
feeds **all** producers that copy, and records `original_magic`,
`normalized_magic`, the normalised sha256 and the transform. The carrier pin
stays the original bytes and magic. Without this, three of the four v3 handler
families (including the draft's DD-WRT `tqsh` example) could never have two
producers.

## 5. Legacy-LZMA v3 is now covered — and that changes an exit code

Measured on the four published Kamikaze rootfs images (details, hashes and carve
commands in `openwrt/NOTES.md`):

| input | backhand kind | backhand | 7z | unsquashfs 4.7.5 | oracle |
|---|---|---|---|---|---|
| 7.09 x86 `5b8aee4c…` | `le_v3_0_lzma` | 331 entries, 137 regular, 152 symlink, rc 0 | same counts, `Method = LZMA Spec`, rc 2 (80 refused relative links) | **rc 1** `gzip uncompress failed … File system corruption detected` | exit 0, 137+194 rows |
| 7.09 brcm-2.4 `69b01a38…` | `le_v3_0_lzma` | 363 entries, 160 regular, 160 symlink | same | rc 1 | exit 0 |
| 8.09.2 brcm-2.4 `d7256e0f…` | `le_v3_0_lzma` | 673 entries, 404 regular, 175 symlink | same | rc 1 | exit 0 |
| 7.09 brcm47xx `13a4f1b8…` | `le_v3_0_lzma` | 362 entries, 156 regular, 163 symlink | same | rc 1 | exit 0 |

Consequences to carry into the freeze:

1. **LZMA-3 carriers are now admissible.** The earlier warning ("C1 carriers
   must be gzip-3") is withdrawn: backhand reads the vendor LZMA wrapper
   (`le_v3_0_lzma`), 7z reads it too, and the two agree file-for-file on all
   four Kamikaze images measured.
2. **The exit-code semantics changed for exactly this family**: an LZMA-3 image
   used to be `exit 2 producer_incomplete:unsquashfs` and is now **`exit 0` with
   tables**. R42C1Run's harness is frozen and maps oracle exit 2 → "cannot be a
   frozen carrier"; any LZMA-3 carrier therefore has no receipt from that arm
   and the C1 arm has to be re-run (or the frozen receipts kept to gzip-3
   carriers) before the freeze. Flagged to the L1.
3. unsquashfs remains the *third* producer only, so its LZMA blindness no longer
   gates a carrier; it is still the only source of **device major/minor** and it
   corroborates every gzip-3 carrier.

## 6. Calibration: what each producer may and may not be trusted for

* **Backhand `-l` is a path set only** — no kind, no size, no link target. Kinds
  and targets come from the extraction tree (`lstat`, `readlink`), hashes from
  the extracted files. A path listed but not materialised is recorded in
  `producers.backhand.unmaterialised` with `kind: null`.
* **Backhand does not materialise devices, fifos or sockets** as an unprivileged
  run (measured on a v4 image with all four: `-l` lists them, the tree has only
  dir/symlink/regular). A `kind: null` entry is therefore *not* a disagreement
  when 7z says `char-device|block-device|fifo|socket`; it *is* one
  (`kind_missing`) when 7z says `regular|dir|symlink`. Device numbers are then
  taken from unsquashfs when it reads the image, and are empty otherwise (the
  `detail` column documents this).
* **Backhand kind selection is explicit and recorded.** Candidates are filtered
  by superblock byte order/version and tried in backhand's own auto-detect order
  (`le_v3_0`, `le_v3_0_lzma`, `le_v3_0_lzma_swap_standard`, `le_v3_1_lzma_swap`,
  plus the two `netgear_be_…` kinds for BE); the first kind that lists the image
  wins and `attempts` records every try with its exit code. Selection is
  independent of 7z, so a mis-detected kind shows up as a disagreement rather
  than being silently accepted.
* **7z `-slt` has no symlink target and no device numbers**, and `7z x` rewrites
  absolute link targets, refuses relative `..` targets (`ERROR: Dangerous link
  path was ignored`, 80 on the 7.09 x86 rootfs) and writes a **zero-byte regular
  file** in place of each refused link. It also exits **2** while having
  extracted every regular file. Completeness is therefore judged per input as
  *"every regular relpath in that producer's own listing exists under its root
  with the listed size and hashes"*, never by exit code; both raw exit codes are
  recorded.
* **`unsquashfs` exits 2 on EPERM `mknod`** while extracting all regular files —
  same rule applies.
* **Compressor statement** — a v1-v3 superblock has no compressor field, so the
  tool reports 7z's header reading with provenance: `compression.method` is the
  magic-independent value (bind the counter to it), `compression.native` is what
  7z says about the untouched bytes. For the Broadcom magic `shsq`, 7z labels
  the *variant*: `LZMA ZLIB` / `SquashFS-LZMA 3.0` for content that is plain
  gzip, while the same bytes under `hsqs` read `ZLIB` / `SquashFS 3.0`
  (`runs/squashfs_v3_broadcom/little_endian/__input__/squashfs_v3_le.bin/oracle-run.json`).
* **Limits** (documented, all fail-closed): a relpath containing TAB/CR/LF is
  refused with exit 3 `path_not_representable` (real end-to-end test:
  `runs/external/tab-path-exit3/`); a symlink whose *target* contains ` -> ` is
  split at the last ` -> ` in the unsquashfs listing; a filename containing a
  newline would break the line-oriented listings (no such input available). An
  image with zero regular files is legal and warns, because the round-41
  `parse_oracle` rejects an empty `oracle.tsv`.

## 7. What the freeze should record

1. Freeze `tools/round-42/sqfs3-oracle.py` with sha256
   `9e03f9349db21c6a92a82ba96321401746df6fc7deb47fc739d1d99311547bdb`; a
   `--work`/`$TMPDIR`-honouring run must appear in the C1 dry-run receipt.
2. Pin the three producers in the receipt: backhand 0.25.5 (L1 build,
   `88cf3ba5…72f`, kinds `le_v3_0`, `be_v3_0`, `le_v3_0_lzma`, `be_v3_0_lzma`,
   `netgear_be_v3_0_lzma*`, `le|be_v3_1_lzma_swap`, `le_v4_0`, `be_v4_0`,
   `avm_be_v4_0`), 7-Zip **26.04** (`f802383f…ad4` — the draft says "7-Zip 7z"),
   unsquashfs 4.7.5 (`461e1fd9…67c`, third producer).
3. Record `producers.backhand.kind` per carrier; it is the backhand parse that
   actually produced the tree, and the L1 asked for it explicitly.
4. Permit the 4-byte magic normalisation explicitly (`original_magic` →
   normalised copy, both hashes recorded); no producer accepts the vendor words.
5. Bind the carrier compression to `compression.method` and keep
   `compression.native` as the raw-bytes record (the Broadcom variant label
   differs from the content).
6. Decide the LZMA-3 re-run question from §5: the frozen harness maps oracle
   exit 2 to "cannot be a carrier", and LZMA-3 carriers now exit 0.
7. The REA `after` receipt may carry `Dangerous link path` style gaps for 7z;
   the oracle's `unpublished-entry` rule keys on unsquashfs/backhand details, so
   the round-41 gap rule stands unchanged.

## 8. Tooling

No installs, no upgrades, nothing written into any PATH directory, no pacman
transaction, no VCS mutation. Used as shipped: `squashfs-tools 4.7.5-1`
(`/usr/bin/unsquashfs`), `7zip 26.04-1` (`/usr/bin/7z`), backhand 0.25.5 at
`/home/vgpnk/.local/opt/backhand-0.25.5-v3/bin/unsquashfs-backhand` (the L1's
build, read-only for this seat), `python3 3.14.8` (stdlib only: `argparse
hashlib json os re shutil stat subprocess sys tempfile`). `sasquatch` 4.5.1 was
read-only calibration, never an oracle producer.

## 9. Reproduce

```sh
A=.ufo/waves/round-42/w1/artifacts/R42C1Oracle
python3 -I $A/sqfs3-oracle.py --selftest                       # 30 checks, 0 failures
TMPDIR=$PWD/work $A/run-matrix.sh $A/fixtures $A/runs $A/matrix.tsv   # 36 fixtures
# external arms (URLs, sha256, carve commands): $A/openwrt/NOTES.md
```

Scratch (`/fast/scratch/hyaku/kaidoku-r42/R42C1Oracle`) was removed at hand-off;
everything cited lives in the artifacts dir or is reproducible from the commands
in `openwrt/NOTES.md` and `runs/external/*/REBUILD.md`.
