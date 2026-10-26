# R41C1Reader — round-40 pure-Python reader vs direct `sasquatch-v4be` on a large AVM-BE rootfs

**Verdict: CONFIRMED.** The hypothesis holds exactly: `tools/round-40/sqfs-list.py --layout avm`
reproduces a direct `sasquatch-v4be` (no `-be`) extraction of the development FRITZ!Box 7430 nested
`filesystem_core.squashfs` file-for-file — **6485/6485 regular files at the same relative path with
the same sha256, 628/628 symlink targets, 409/409 directories, the single char device at 247:0, zero
mismatches in any class** — in 3.2 s and 55 MB RSS. No reader defect was found; no patch is needed.
Four calibration findings bite the *round-41 C1 surface around the reader* (counter path strip, dev
fixture coverage, special-file coverage, a whitespace-parsing trap), listed in §Findings.

## Carrier and provenance (all measured here, nothing reused from another seat)

| object | bytes | sha256 |
|---|---|---|
| `FRITZ.Box_7430-07.31.image` (download) | 28 856 320 | `3dd6940c3aea429944d41508cc6c5a4e3573dae8ad9bf92e293e5bf945a6ecf4` (= the pin in my item) |
| tar member `./var/tmp/filesystem.image` | 25 825 288 | `b919a6a218a57c8bf69e64baeab28bd6cb4c77bfd1fe2e8e4c1880edb9342c6c` |
| nested `filesystem_core.squashfs`, extracted | 25 198 592 | — |
| **the tested image**: nested core carved to `bytes_used` | **25 194 540** | **`1588129540dfdcce09cb8304f724a66fd50aa1eb0bc6481cc6a2246670aa628f`** |

The `.image` is a plain tar (`2e2f 7661 722f` = `./var/`), not a squashfs: `sasquatch-v4be` on it
directly aborts with `Non-standard SquashFS Magic: './va'` (exit 1) — recorded so nobody repeats it.
The carve to `bytes_used` is lossless for reading: `bytes_used = mkfs_time = 25194540`, and the
extracted member carries 4052 trailing bytes past that.

Superblock as read by the reader (`7430-core-inspect.json`): magic `sqsh`, v4.0, `inodes = 7524`,
`block_size = 65536` (`block_log 16`), `fragments = 359`, `compression = 4` (xz), `flags = 0x2c0`,
`no_ids = 1`, `root_inode = 0xd7041e12`, `inode_table_start = 25047618`,
`directory_table_start = 25104328`, `fragment_table_start = 25179966`,
`lookup_table_start = 25194462`, `id_table_start = 25194532`, `xattr_id_table_start = -1`,
`mkfs_time == bytes_used == 25194540` → `avm_marker: true`.

## Result

Oracle: `sasquatch-v4be -d core-sasq -no-progress core.squashfs` (0.70 s, 94 MB RSS, **exit 2** —
`create_inode: could not create character device core-sasq/dev/led, because you're not superuser!`;
7114 non-dir inodes, 6485 files + 628 symlinks created + 1 device refused). Because the device is not
materialised, the device comparison uses `sasquatch-v4be -lls` (authoritative image metadata, 7524
lines, exit 0), not the extracted tree.

`compare.py core-sasq core-lls.txt core-reader-files.tsv core-reader-nonreg.tsv` → `compare.json`:

| class | reader | sasquatch `-lls` | extracted tree | mismatches |
|---|---|---|---|---|
| regular files (path+sha256) | 6485 | 6485 | 6485 | **0** (`reg_digest_mismatch: 0`, `reg_only_in_tree: 0`, `reg_only_in_reader: 0`, path sets equal in both directions) |
| size column vs `-lls` size | 6485 | 6485 | — | **0** |
| directories (non-root) | 409 | 409 | — | **0** (`dir_only_in_lls: 0`, `dir_only_in_reader: 0`) |
| symlinks (path+target) | 628 | 628 | 628 | **0** (`link_target_mismatch: 0`, set diff 0/0, extracted targets equal too) |
| char/block devices (major:minor) | `dev/led 247:0` | `dev/led 247:0` | not materialised | **0** |
| fifos / sockets | 0 | 0 | 0 | **0** |

`--layout auto` on the same image resolves to `layout: avm`, `header_endian: little`, and its TSV is
byte-identical to `--layout avm` (`cmp` clean); `block_length_signal` is **`plausibility`**, not
`exact` (see F2). `--layout be` on the same bytes exits 2 with
`metadata offset 7698 beyond block 25102662 (len 6)` — the little-endian chain is load-bearing.
`warnings: []` in both modes; the reader's own `--selftest` is 13/13.

Determinism: two consecutive `--layout avm` runs produce `cmp`-identical `--files` and
`--nonregular` TSVs. Runtime 3.24 s / 3.29 s / 3.31 s (`--inspect`), peak RSS 55.7–55.8 MB.

### Continuity with the frozen round-40 evidence (extra, not in the item)

I rebuilt the four round-40 **development** carriers and re-ran the reader against the committed
receipts (`fetch-vendor.py --rev 7fce3086…`, image+member+carrier sha256 all re-verified, then
`sqfs-list.py --layout avm`):

- V1, V2, L1, L2: `cmp` says the regenerated `--files` TSV is **byte-identical** to
  `corpus/evidence/round-40/c1/<id>/oracle.tsv`, and the `--nonregular` TSV is byte-identical to
  `nonregular.tsv`, on all four. Byte-identical means the committed oracles are still exactly this
  code's output — oracle drift between the round-40 freeze and the round-41 base is zero.
- Counts: V1 697 files / 117 dirs / 263 links / 1 char device; V2 8 / 9 / 85 / 1; L1 7 / 4 / 2 / 0;
  L2 6 / 5 / 2 / 0.

## Code review — is there any suffix/basename logic that could collide?

No. In `tools/round-40/sqfs-list.py` there is **no path matching at all**: no `endswith`, no
`basename`, no glob, no comparison against a second listing. Paths are produced only by
`walk()` (`sqfs-list.py:631`): `child_path = name if not path else path + '/' + name` (line 652) from
the directory entries `dir_entries()` yields, with `.`/`..` rejected as reserved names and duplicates
rejected inside one directory (`duplicate entry %r in directory %r`, line 649). Every `rsplit('/', 1)` in the file
(lines 944, 1033, 1064, 1152) is in the *self-test writer* `_build_image`/`_dir_body_len`, which
builds fixtures; they never touch read paths. `write_tsv` (line 714) sorts by UTF-8 bytes and is the only
ordering authority. `classify_link` (line 674) resolves link targets component-wise against the `kinds` map
with exactly one semantic decision (`in-tree` vs `escaping`), and it never rewrites a published path.

So the R40-CL1 false negative cannot originate in the reader — it lives entirely in the counter's
`same_rel`. Measured here, the class of input that trips a suffix matcher is real and abundant:
on the 7430 core there are **130** regular/symlink pairs sharing a 1-component tail and **32**
sharing a 2-component tail (`suffix-census.json`); e.g. symlink `sbin/sysctl` vs regular
`etc/boot.d/core/sysctl`, symlink `usr/www/cgi-bin/captive_pic` vs regular
`usr/www/avm/cgi-bin/captive_pic`. A basename matcher mis-scores this carrier immediately.

## Coverage — what the carrier exercises, and what it does not

Exercised (from `census.json` / `7430-core-inspect.json` `decode_paths`):

- **fragments are the dominant path**: 359 fragments, **6198 fragment slices** (95.5 % of files
  end in a fragment), 1298 compressed data blocks, 4 raw (uncompressed) data blocks, 2 sparse
  blocks, 56 compressed metadata blocks (the inode table spans 8 metadata blocks), 0 raw metadata
  blocks. Total regular-file bytes 111 615 238.
- **multi-block files**: 269 files > 65536 B, largest `lib/modules/3.10.107/kernel/drivers/dsld/kdsldmod.ko`
  (3 490 848 B = 53 blocks); 18 empty files; max path depth 12.
- **charset**: 5 non-ASCII names (UTF-8 umlauts under `usr/www/avm/help/`), 1 name with a space
  (`etc/internal_memory_default_de/Videos/FRITZ! Clips.html`), no name with tab/newline/CR/NUL.
- regular-file/`-lls` size agreement on all 6485 rows means the reader's `file_size`-vs-bytes-read
  assertion (line 821, `%r: read %d bytes, inode declares %d`) never had to fire.

Not exercised by this carrier (must be supplied by the lane-built L3/L4 or by the reader's own
self-test):

- **no block devices, no fifos, no sockets** — the only special file in the whole 7524-inode rootfs
  is one char device `dev/led 247:0` (V1 and V2 also carry exactly one char device and nothing
  else). So a round-41 vendor carrier V3/V4 will *not* exercise the `TYPE_BLKDEV/TYPE_FIFO/
  TYPE_SOCKET` decode paths or their `DEV_TYPES`/`IPC_TYPES` branches; that coverage can only come
  from the lane writer.
- **zero files whose size is an exact multiple of `block_size`** (6467 tailed + 18 empty = 6485), so
  the `n = size // block_size` branch chosen when `fragment != INVALID_FRAG` and the tail is empty
  is never taken here.
- **zero `escaping` symlinks** (628 in-tree: 108 absolute-inside, 520 relative-inside; 282 distinct
  targets, 108 containing `..`). The `above-root` / `empty-target` / `loop` reasons are not
  reachable on this carrier.

## Findings

**F1 — the R40-CL1 collision shape is absent from every dev carrier except L2, and the reverse
direction is absent everywhere (affects C1's pre-freeze dry run).** Full-path suffix pairs
(regular path ending with `/`+symlink path) on the core: **0**; reverse direction: 0. Same on V1
(0/0), V2 (0/0), L1 (0/0), and on the wrapper (0/0). Only **L2** carries it, and it is exactly the
round-40 failing case: symlink `bin/busy -> /usr/bin/busy` with regular `usr/bin/busy` (1 pair).
Consequence for the draft: the "pre-freeze dry run 4/4 + both-direction collision fixture" cannot
get its *reverse* direction (symlink path ending with a regular file's path) from any dev carrier —
it exists only in a fixture. That is consistent with the claim as written, but it means: (a) do not
drop L2 from the dry run, it is the only fixture-free evidence that exactness is scored; (b) the
both-direction fixture must carry the reverse pair, because no carrier ever will.

**F2 — on a rootfs-sized carrier the AVM layout is decided by plausibility, not by the
exact-adjacency signal the prose cites (affects the C1 knowledge doc's wording).** For this core the
inode table is 8 metadata blocks, so `inode_table_start + 2 + len == directory_table_start` cannot
hold; `--layout auto` reports `block_length_signal: "plausibility"` with
`header_length_candidates {le: 2016, be: 24583}` (be is > 8192, therefore implausible). The layout
determination is still correct and unambiguous, but the round-41 knowledge entry / PROVINCE row
should state the evidence as "superblock BE `sqsh` + `mkfs_time == bytes_used` + only the LE header
length is within the 8192-byte metadata maximum, corroborated by decoding both chains to a parseable
root", not "exact block-length identity" — the exact signal only exists on small carriers. Smallest
safe correction: one clause in the knowledge entry; the predicate itself (marker + LE block lengths)
is unaffected.

**F3 — the round-40 counter's `extract_rel` strips *any* first component ending in `_extract`
(affects the round-41 C1 counter port).** `c1-counter-exact-match.diff` adds
`if parts and parts[0].endswith('_extract'): parts = parts[1:]`. The 7430 core has no such top-level
name (`bin data dev etc lib mnt nohup.out proc run sbin sys tmp usr var var.tar wrapper`), so nothing breaks
today, but a round-41 carrier or nested fixture with a genuine top-level `foo_extract/` directory is
silently re-rooted one level too deep and every row mismatches. Smallest safe correction: compare
against the chunk's *own* staged name, i.e. strip `parts[0]` only when
`parts[0] == staged_chunk_name + '_extract'` (names the counter already has from the receipt),
never a wildcard. Worth fixing before the port is frozen, because the L3/L4 builders are free to
pick directory names and `tmp_extract`-style names are exactly what a nested-extraction fixture
produces.

**F4 — whitespace parsing of `sasquatch -lls` mis-reads this rootfs (affects any oracle cross-check
written during the freeze).** One path contains a space (`etc/internal_memory_default_de/Videos/
FRITZ! Clips.html`), so a `line.split()`-style `-lls` parser reports one phantom missing and one
phantom extra row (my first `compare.py` did exactly that; `reg_only_in_lls:
["etc/internal_memory_default_de/Videos/FRITZ!"]`). The fix is `line.split(None, 5)[5]` for `-lls`
rows (kept in `compare.py`). The frozen TSV oracle is immune because `_text()` (line 106) rejects
tab/newline/CR/NUL bytes in names — but that same guard means **one tab or newline in a vendor
carrier's filename aborts the whole oracle with exit 2** rather than escaping the name. No such
name exists in the 7430 core, the wrapper, V1, V2, L1 or L2; a one-line "cannot be written as TSV"
failure is the disclosure the C1 knowledge entry should carry for V3/V4.

**F5 — memory is 2.2× the image (not a defect, a ceiling to state).** `SquashFS.__init__` does
`self.buf = fh.read()` (line 177), so RSS is ≈ image size plus metadata cache: 25 194 540 B → 55.8 MB peak.
Fine for the 5491 core class (≈34 MB) and for a 200 MB image (~450 MB), but the round-41 counter
should not run the reader on a whole vendor `.image` (the 7430 image itself is not a squashfs anyway,
F0 in §Carrier).

**F6 — `directories` excludes the root** (409 vs the 410 `-lls` lines that include
`squashfs-root`). Any counter clause that compares directory counts against an `-lls`-derived
number must subtract one; the round-40 oracle stores dirs in the non-regular TSV, so the row-level
comparison is unaffected.

## Non-findings I checked and rejected

- Reader's non-regular table ordering/duplicity: 7523 distinct paths, no duplicate keys, no
  case-insensitive collision except two intentional pairs (`etc/init.d/E40-dsl` vs `e40-dsl`,
  `E45-avmnexusd` vs `e45-avmnexusd`) which are distinct on a case-sensitive filesystem and must
  not be normalised by the counter.
- Hard links: `sasquatch-v4be` reported `created 0 hardlinks`; the reader lists each path
  independently and all 6485 digests agree with the extracted tree, so no inode-dedup behaviour is
  lost.
- Empty directories: all 409 are present in both reader and `-lls` (the walk is entry-driven, not
  content-driven).
- The outer wrapper `./var/tmp/filesystem.image` (AVM-BE, `bytes_used = mkfs_time = 25824314`,
  109 inodes) compares clean too: 8 files / 9 dirs / 90 links / 1 char device, 0 mismatches
  (`wrapper-compare.json`), and the reader reports the same 25 198 592-byte nested
  `filesystem_core.squashfs` row that `sasquatch-v4be` writes.

## Reproduction

Scratch `S=/fast/scratch/hyaku/kaidoku-r41/R41C1Reader`, `TMPDIR=$S`; scratch removed before yield.
Exact command sequence, exit codes and limits are in
`artifacts/R41C1Reader/README.md`; every number above regenerates from it. Summary of the sequence:

```
curl -fsSL -o 7430.image https://download.avm.de/fritzbox/fritzbox-7430/other/fritz.os/FRITZ.Box_7430-07.31.image
tar -xf 7430.image ./var/tmp/filesystem.image                       # 25 825 288 B
~/.local/bin/sasquatch-v4be -d fs-extract -no-progress var/tmp/filesystem.image   # exit 2 (mknod only)
head -c 25194540 fs-extract/filesystem_core.squashfs > core.squashfs
~/.local/bin/sasquatch-v4be -d core-sasq  -no-progress core.squashfs             # exit 2 (mknod only)
~/.local/bin/sasquatch-v4be -lls -no-progress core.squashfs > core-lls.txt        # exit 0, 7524 lines
python3 -I -B <lane>/tools/round-40/sqfs-list.py --layout avm \
  --files core-reader-files.tsv --nonregular core-reader-nonreg.tsv core.squashfs # exit 0
python3 -I -B compare.py core-sasq core-lls.txt core-reader-files.tsv core-reader-nonreg.tsv
```

Isolation respected: no REA, no unblob, no extractor run on any reserved image or member (only the
7430 dev image this item names); no writes outside this seat's artifacts dir; VCS untouched (only
`fetch-vendor.py`'s read-only `git show`); no tool installed or upgraded (pacman paused anyway;
`/usr/bin/time` absent, so timing/RSS come from `resource.getrusage(RUSAGE_CHILDREN)`).
