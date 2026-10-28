# R44C1Oracle — round 44 wave 1, seat report

**Seat:** R44C1Oracle (executor) · **Lane:** `kaidoku-shokunin` ·
**Base:** `c29360e3ba5381a5ab69e372d0d9577970f85018` · **Date:** 2026-10-28

## What I built

`tools/round-44/c1-oracle.py` — the frozen oracle builder for R44-C1.

**Installed** (on the L1's request, 2026-10-28) at
`tools/round-44/c1-oracle.py`, sha256
`455c8a553a058c7fa01cc6930d30d5319b7815c70c68854fac86834163981336`, mode 755 —
byte-identical to the artifacts copy (`cmp` clean), parses, and its `--selftest`
runs green (24 cases, 0 failures) from the installed path.

**Scope ids are the carriers' own `id` values, never a spelling constant.**
The L1 caught a real defect here: the tool emitted `scope.target_ids` from the
module constant `TARGET_IDS` (spelled `v1-le`, matching the draft claims'
carrier table and the seat spec), while `carriers.json` keys its entries
`v1le`. A consumer binding `scope.target_ids` to carrier ids would have
matched **nothing**. `scope_ids()` now derives both lists from the loaded
carriers, so the emitted names are always the entries' own ids:

| field | value |
|---|---|
| carrier `id` | `v1le`, `v1be`, `v2le`, `v2be` (`v21le`, `v21be`) |
| carrier `fixture_id` | `v1-le`, `v1-be`, `v2-le`, `v2-be` (`v2.1-le`, `v2.1-be`) |
| `scope.target_ids` (now) | `v1le`, `v1be`, `v2le`, `v2be` — **matches `id`** |

`fixture_id` is a descriptive label for the upstream fixture, **not** the
carrier key; the counter must bind to `id`. A selftest guard (4 cases) fails
if `scope_ids()` ever returns anything but the carriers' own ids, and it was
proven to catch this exact regression: a copy patched back to
`targets = list(TARGET_IDS)` exits 1 with
`scope_ids did not mirror the carrier ids`.

The merge mode also writes the top-level `scope` and `toolchain` blocks into
the merge target, so the frozen `carriers.json` ends up carrying the
target/exploratory split statement and the five verified tool digests. An
existing `superblock_layout` is left untouched (the counter's to own).

| artifact (my artifacts dir) | sha256 |
|---|---|
| `c1-oracle.py` | `455c8a553a058c7fa01cc6930d30d5319b7815c70c68854fac86834163981336` |
| `c1-oracle.json` (full oracle blocks + receipt data) | — |
| `carriers.oracle-block.json` (the `carriers.json` oracle block, v3) | `df16adc89ec6444ad0dbc48097a88c07f3d4e015c765acce762acc6a8a3eeaf4` |
| `receipt.json` (run receipt) | — |

## The three oracles

**Oracle A — `unsquashfs` 4.7.5 (squashfs-tools upstream), independent.**
`/usr/bin/unsquashfs`, sha256 `461e1fd9eac39c12e673042807459985636030d5557319343fc3a6ed4ba1677c`,
version line `unsquashfs version 4.7.5 (2026/03/01)`. This is a **different producer**
from sasquatch 4.5.1 (the extractor unblob 26.6.4 drives), so it is a genuine
independent oracle. Per carrier the tool runs `-lls` (member census: type, mode,
owner, size, mtime, path), extracts into a fresh scratch dir and sha256s every
REGULAR file, and records every non-regular member as a non-regular row.

**Oracle B — the committed unblob `__output__` expected trees (S138), second
reading.** The tool walks the committed tree named by each carrier's
`output_tree` in `tools/round-44/carriers.json` and records its member digests.
The tool cross-checks A against B per member (path, sha256, size) and fails the
carrier on any divergence.

**Independence caveat, stated plainly.** Oracle B is unblob's *own* expectation
for these fixtures — produced by unblob's sasquatch-backed handler. It
cross-checks the member set and is a second reading of the same bytes, but it
is **not** an independent producer lineage. The independent oracle is A. The
emitted block records this as `output_tree.producer_lineage`, and the block's
`oracle.expected_tree_source` now says "a second reading of the same bytes,
NOT an independent producer" — the source note never calls it independent.

**Oracle C — 7-Zip 26.04, a third producer (corroboration only).** `7z` reads
all six carriers and agrees with oracle A on the member set and every content
digest. It is distinct from both `unsquashfs` and sasquatch, so it is a
genuine third reading — but it *corroborates* oracle A; it does not replace
the independent oracle, which remains `unsquashfs` 4.7.5.

## Toolchain (measured on this host, re-derivable by the counter)

| tool | path | version | sha256 | role |
|---|---|---|---|---|
| `unsquashfs` | `/usr/bin/unsquashfs` | 4.7.5 | `461e1fd9eac39c12e673042807459985636030d5557319343fc3a6ed4ba1677c` | **the independent oracle** (upstream squashfs-tools) |
| `sasquatch` | `/home/vgpnk/.local/bin/sasquatch` | 4.5.1 | `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` | the extractor unblob 26.6.4 drives — **not** an oracle for this claim |
| `sasquatch-v4be` | `/home/vgpnk/.local/bin/sasquatch-v4be` | 4.5.1 | `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6` | the squashfs v4 BE sasquatch variant (not used by the v1/v2 carriers) |
| `unblob` | `/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob` | 26.6.4 | `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09` | the extractor under REA 6.5.0 — the committed `__output__` trees are **its** expectation |
| `7z` | `/usr/bin/7z` | 26.04 | `f802383f13b8331aabaf779def00a356c8d2b8148255170b75b03028f4d23ad4` | third producer, corroboration only |

Version lines as measured: `unsquashfs version 4.7.5 (2026/03/01)`;
`unsquashfs version 4.5.1 (2022/03/17)` (both sasquatch binaries);
`26.6.4` (unblob); `7-Zip 26.04 (x64) : Copyright (c) 1999-2026 Igor Pavlov :
2026-10-05` (7z). The block also carries each version command's exit code and
stdout sha256, so a counter can re-derive every value.

REA 6.5.0 package root (unchanged from round 42, `tools/round-42/rea-pkg.json`):
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`,
`package_json_sha256 a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`,
`package_lock_sha256 d42d56f0f4f8baf3ecc24f2bd24f9f09e3c99b83592ef85201f74df255e0c6ca`.

## Three-producer agreement

All six carriers agree across `unsquashfs` (oracle A), the committed
`__output__` trees (oracle B) and `7z` (oracle C). Only the four `target`
rows are scored; the two `exploratory` rows are retained measurements.

| id | unsquashfs digest | `__output__` digest | 7z digest | 7z `File System` | 7z `Method` |
|---|---|---|---|---|---|
| `v1le` | `8faae7739b14315c…` | `8faae7739b14315c…` | `8faae7739b14315c…` | SquashFS 1.0 | ZLIB |
| `v1be` | `8faae7739b14315c…` | `8faae7739b14315c…` | `8faae7739b14315c…` | SquashFS 1.0 | ZLIB |
| `v2le` | `4178bb8379de3e55…` | `4178bb8379de3e55…` | `4178bb8379de3e55…` | SquashFS 2.0 | ZLIB |
| `v2be` | `4178bb8379de3e55…` | `4178bb8379de3e55…` | `4178bb8379de3e55…` | SquashFS 2.0 | ZLIB |
| `v21le` | `4178bb8379de3e55…` | `4178bb8379de3e55…` | `4178bb8379de3e55…` | SquashFS 2.1 | ZLIB |
| `v21be` | `4178bb8379de3e55…` | `4178bb8379de3e55…` | `4178bb8379de3e55…` | SquashFS 2.1 | ZLIB |

**7z independently corroborates the compression finding.** Its
`Method = ZLIB` on all six carriers confirms that every carrier is
gzip/zlib-compressed — including the three big-endian ones that `file(1)`
mislabels "uncompressed". 7z reads the v1/v2 superblock by its own
(v4-layout-aware) code path and reports the real compression method, so it is
a third independent witness that the `file` word is an artifact. 7z also
reports `Big-endian = -` for the LE carriers and the correct `File System`
version for all six.

The v2.1 member digests (oracle C, `7z x -tSquashFS` on
`corpus/evidence/round-44/carriers/squashfs_v2.1_{le,be}.bin`):

| path | size | sha256 |
|---|---|---|
| `apple1.txt` | 7 | `6181259c6b2ca629a56920b422e9a8f212a4d0bcead923df92dbd66fbb7e1c30` |
| `apple2.txt` | 7 | `919fc82d6f1031d305dbce2fc5a74a6df5ddf2da472ee4d137c681cef28d4aff` |
| `apple3.txt` | 7 | `2d95014ed3f24e86ce5fc3a4529f057d7b2318d9b24b54f2e9476b154bd21ec6` |
| `apple4.txt` | 7 | `08d9b05b15b998f2dbc741399fef4350c7863cc85df2305d7da4e83e8c8a959d` |

(identical for `v21le` and `v21be`; both equal the `v2le`/`v2be` member set —
see the note below on digests not being carrier discriminators.)

## Result on the carriers — four scored, two exploratory

`tools/round-44/carriers.json` was frozen by the L1 mid-wave and grew to **six**
carriers (the four preregistered ones plus `v21le`/`v21be`, the `squashfs_v2`
2.1 pair). **The L1's 2026-10-28 amendment reverts the C1 target to the four
preregistered v1.0/v2.0 carriers** — the v2.1 pair's REA probe was exploratory
and unretained, so widening a claim after data would be unsound.

This seat's tool therefore splits the two sets explicitly and the delivered
oracle block does too:

- **`carriers`** — the **scored** set, exactly four: `v1le`, `v1be`, `v2le`,
  `v2be`. This is the only set the counter may bind.
- **`exploratory`** — `v21le`, `v21be`: measured and retained (the
  measurements are real and cost nothing to keep), but **unbound exploratory
  data, not scored**. They carry no `oracle` block and the merge mode writes
  no `oracle` key for them, so a v2.1 carrier cannot be scored as a C1
  carrier by accident.

| id | scope | handler | endian | regular | non-regular | oracle A digest | oracle B digest | oracle C digest | agree |
|---|---|---|---|---|---|---|---|---|---|
| `v1le` | **target** | `squashfs_v1` | le | 3 | 0 | `8faae7739b14315c…` | `8faae7739b14315c…` | `8faae7739b14315c…` | A=B=C |
| `v1be` | **target** | `squashfs_v1` | be | 3 | 0 | `8faae7739b14315c…` | `8faae7739b14315c…` | `8faae7739b14315c…` | A=B=C |
| `v2le` | **target** | `squashfs_v2` | le | 4 | 0 | `4178bb8379de3e55…` | `4178bb8379de3e55…` | `4178bb8379de3e55…` | A=B=C |
| `v2be` | **target** | `squashfs_v2` | be | 4 | 0 | `4178bb8379de3e55…` | `4178bb8379de3e55…` | `4178bb8379de3e55…` | A=B=C |
| `v21le` | exploratory | `squashfs_v2` | le | 4 | 0 | `4178bb8379de3e55…` | `4178bb8379de3e55…` | `4178bb8379de3e55…` | A=B=C |
| `v21be` | exploratory | `squashfs_v2` | be | 4 | 0 | `4178bb8379de3e55…` | `4178bb8379de3e55…` | `4178bb8379de3e55…` | A=B=C |

`output_tree_digest` rule (recorded in every block as
`output_tree_digest_def`): sha256 over the concatenation of
`"<path>\t<sha256>\n"` lines of the **regular** members, sorted bytewise by
path. `members` holds regular files only, so the rule is unambiguous;
non-regular members live in `nonregular` with no sha256.

Note the digests are equal **across** byte orders: `v1le` and `v1be` have the
same member set and content, likewise the v2 pairs. The digest therefore
identifies the *member set*, not the carrier. The per-carrier identity is
carried by the carrier `sha256` pin and the superblock probe, not by
`output_tree_digest` — worth stating so the counter is not built to treat the
digest as a carrier discriminator.

**Zero non-regular members across all six carriers** (no symlink, device,
fifo, socket, no subdirectory). Consistent with the amended claim note #5.

## Measured v1/v2 superblock (the counter's binding input)

The v1/v2 superblock is **32 bytes packed**, per unblob 26.6.4's
`SquashFSv1Handler.C_DEFINITIONS` (S119): magic `0:4`, inodes `4:8`,
bytes_used `8:12`, uid_start `12:16`, guid_start `16:20`,
inode_table_start `20:24`, directory_table_start `24:28`, s_major `28:30`,
s_minor `30:32`.

**There is no compression field in the v1/v2 superblock.** The compression
class is observed from the inode-table metadata block (a 2-byte header whose
top bit is the "stored uncompressed" flag; the body starts with a zlib
`78 xx` header ⇒ gzip).

| id | magic | endian | major | minor | bytes_used | inode_table_start | dir_table_start | compression | metadata chain lands |
|---|---|---|---|---|---|---|---|---|---|
| `v1le` | `hsqs` | le | 1 | 0 | 176 | 71 | 128 | gzip | yes |
| `v1be` | `sqsh` | be | 1 | 0 | 177 | 71 | 129 | gzip | yes |
| `v2le` | `hsqs` | le | 2 | 0 | 196 | 88 | 136 | gzip | yes |
| `v2be` | `sqsh` | be | 2 | 0 | 201 | 88 | 138 | gzip | yes |
| `v21le` | `hsqs` | le | 2 | 1 | 196 | 88 | 136 | gzip | yes |
| `v21be` | `sqsh` | be | 2 | 1 | 201 | 88 | 138 | gzip | yes |

The metadata chain witness (`inode_table_start + 2 + meta_len ==
directory_table_start`) lands exactly for all six, in the carrier's own
endianness — the same witness style round-42 used, so the counter can carry
it over verbatim in spirit.

## ⚠ Finding for the L1 and R44C1Counter: the frozen `superblock_layout` is wrong on two of four fields

`tools/round-44/carriers.json` currently carries a `superblock_layout` block:

```json
{"magic_offset": 0, "magic_len": 4,
 "compression_offset": 20, "compression_len": 2,
 "s_major_offset": 28, "s_major_len": 2,
 "s_minor_offset": 30, "s_minor_len": 2,
 "bytes_used_offset": 40, "bytes_used_len": 8}
```

Those offsets are the **squashfs v4** layout, not v1/v2. Measured against the
six frozen carriers:

| id | `compression` u16@20 | `bytes_used` u64@40 | truth: u32@8 = bytes_used | truth: u32@20 = inode_table_start |
|---|---|---|---|---|
| `v1le` | 71 | 862367868 | 176 | 71 |
| `v1be` | 0 | 12717287937415315456 | 177 | 71 |
| `v2le` | 88 | 1617168913 | 196 | 88 |
| `v2be` | 0 | 725666679215882240 | 201 | 88 |
| `v21le` | 88 | 1617168913 | 196 | 88 |
| `v21be` | 0 | 725674375797276672 | 201 | 88 |

Three concrete defects:

1. **`compression_offset: 20` reads `inode_table_start`.** The v1/v2
   superblock has no compression field at all, so any binding that reads a
   u16 at offset 20 and compares it to `"gzip"` is reading the wrong field.
   It happens to be nonzero for the LE carriers and **zero for all three BE
   carriers** — so a wrong probe looks like a clean endianness signal and
   would not announce itself.
2. **`bytes_used_offset: 40, bytes_used_len: 8` is v4.** For v1/v2, bytes_used
   is a u32 at offset 8. The u64@40 read returns pure garbage
   (`12717287937415315456` for `v1be`), and a `bytes_used_sane` range check
   would fail every carrier.
3. `s_major`/`s_minor` at 28/30 **are** correct for v1/v2 — they coincide
   with the v3/v4 layout — which is why the block looks plausible.

The correct v1/v2 layout is emitted in my
`carriers.oracle-block.json` as `superblock_layout_v1v2`; the L1 can install
it in place of the current block.

### Why this matters: `file(1)` "uncompressed" is a v4-layout artifact, not a property

`file(1)` applies the squashfs **v4** superblock layout to *every* squashfs
image, so for a v1/v2 image its `compressed`/`uncompressed` word is read from
offset 20 — i.e. from `inode_table_start`. It therefore reports
**"uncompressed" for all three BE carriers** and "compressed" for the LE ones,
purely as a byte-order artifact. Proof (measured, not inferred):

- v1le: offset-20 u16 LE = 71 (its=71) → `file` says "compressed";
  v1be: offset-20 u16 BE = 0 (its=71, high bytes zero) → `file` says
  "uncompressed"; v2le: 88 → "compressed"; v2be: 0 → "uncompressed";
  v21be: 0 → "uncompressed".
- Setting byte 20 of the BE image to `0x47` flips `file` from "uncompressed" to
  "compressed" with no other byte changed.
- Zeroing bytes 20–21 of the LE image flips `file` to "uncompressed" while
  `unsquashfs -s` still reports "Data is compressed".
- `unsquashfs -s` reports **inodes/data/fragments compressed on all six**,
  and every carrier's metadata block decompresses as zlib (`78 da …`).

The amended claim note #4 already reaches the right conclusion ("`file(1)`
mislabels both BE carriers 'uncompressed' while `unsquashfs -s` reports
inodes/data/fragments compressed on all six"). This seat independently
confirms it with the offset-level proof above, and adds that the mislabel
affects **three** carriers (all BE), not two, and that the cause is the v4
layout — which is also the root cause of the `superblock_layout` defect.
**The counter must never bind to `file` text**; the amended note already says
so, and the frozen `compression` value in `carriers.json` (`"gzip"` for all
six) is correct and matches the metadata-block observation.

## Verification actually exercised

Every receipt below carries seat name, command, exit code, stdout sha256 and
wall time (the tool writes `receipt.json` with exactly those fields).

| # | command | exit | expected |
|---|---|---|---|
| 1 | `python3 -I -B c1-oracle.py --selftest` | 0 | 24 cases, 0 failures |
| 2 | `python3 -I -B c1-oracle.py --root . --work … --json-out … --receipt …` | 0 | 4 scored + 2 exploratory carriers, 3 oracles agree |
| 3 | same, `--oracle-root <tampered tree>` (one `apple1.txt` rewritten) | 1 | carrier `v21le` fails on the sha256 divergence |
| 4 | same, `--oracle-root <nonexistent>` | 2 | could-not-evaluate |
| 5 | same, `--carriers <file with id v9-zz>` | 2 | unknown carrier id refused |
| 6 | same, `--only nosuch` | 2 | no carrier matches |
| 7 | same, `--only v1le --only V1LE` | 0 | id spelling is separator/case-insensitive |
| 8 | same, `--merge-carriers <copy of frozen carriers.json>` | 0 | the four target entries receive an `oracle` block; the two exploratory ones do not |
| 9 | same, invoked from a foreign cwd (`/tmp`) with absolute `--root` | 0 | identical digests, cwd-independent |

Final run receipt: `exit 0`, `stdout_sha256
b4befe16b1baf82cf7d3929bf99b598f3104aee3be0d8ca9243d4b2ea8a56b2b`, `wall_s 0.969`,
`carriers: v1be v1le v2be v2le`, `exploratory: v21be v21le`, `problems: []`.

Tool digest `455c8a553a058c7fa01cc6930d30d5319b7815c70c68854fac86834163981336`;
oracle block digest `df16adc89ec6444ad0dbc48097a88c07f3d4e015c765acce762acc6a8a3eeaf4`.

**Note on the toolchain version-command exit codes.** `unsquashfs -version`
(and therefore `sasquatch`, which is a patched `unsquashfs`) prints its
version and then exits **1** — the tool's own convention, not a failure. The
toolchain block records each command's real exit code plus a
`version_argv_exit_note` so the counter does not read a non-zero exit as a
broken toolchain. `7z` and `unblob` exit 0.

**The merge mode now strips, not just skips.** The L1's merged
`carriers.json` already carried an `oracle` block on the two exploratory
carriers (from the earlier pre-scope build). `--merge-carriers` now deletes
any stale `oracle` key on a non-target carrier and records it in
`merged_stripped_exploratory`, so after the merge the file carries exactly
four `oracle` blocks — the four scored C1 carriers — and the v2.1 pair cannot
be bound by the counter by accident.

Two self-test cases were **red before they were green**, and the tool caught
them: the truncated-superblock case (`b"hsqs" + bytes(28)` is exactly 32
bytes, not truncated — fixed to `bytes(27)`), and the `--only` filter
(argparse `store` overwrote repeated flags and the code then iterated a
string's characters; fixed with `action="append"`). Both were found by the
tool's own selftest, not by inspection.

## Exit-code semantics

`0` met/clean · `1` failed · `2` could-not-evaluate (never counts toward a
target). Verified by cases 3–6 above.

## Scope discipline

- I authored `c1-oracle.py` and my artifacts only. I did **not** modify
  `tools/round-44/carriers.json` (the L1's frozen file) — the oracle block
  for it is delivered as `carriers.oracle-block.json` for the L1 to install,
  and `--merge-carriers` exists for the L1 to apply it.
- I did **not** run the after-side C1 data procedure (`c1-run.sh`); the L1
  runs it after the freeze. No REA `extract-firmware` run was performed by
  this seat.
- No git mutation in the lane. Scratch only under
  `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Oracle/`.
- The oracle is derived from `unsquashfs` (upstream) and the committed
  `__output__` trees — never from a REA/sasquatch receipt.

## Risks / open items for the L1

1. **`superblock_layout` must be corrected** to the v1/v2 offsets above (or
   the counter must hard-code them) before the freeze. As frozen, a counter
   that reads that block fails every carrier on `bytes_used`, and its
   compression binding reads the wrong field. This is the one item I judge
   **blocking for C1**.
2. **The L1 should confirm the counter binds the superblock by reading the
   superblock itself**, not by comparing to `file` output or to a frozen
   `compression` string. `carriers.json`'s per-carrier `compression: "gzip"`
   is a *derived* fact; the frozen `output_tree`/`members` digests are the
   oracle proper.
3. **`output_tree_digest` is not a carrier discriminator** (equal across byte
   orders). The counter must bind carrier identity to the image `sha256` pin
   and the superblock probe.
4. Oracle B is not an independent producer (see above). If the claim's
   wording leans on "two independent oracles", it should say "two oracles,
   one independent producer (unsquashfs) plus unblob's own expected trees".
5. The `v2ns` / broadcom / nonstandard / v3 / v4 families stay Frontier; I
   confirmed `unsquashfs` 4.7.5 refuses `v2ns-le`
   (`FATAL ERROR: Can't find a valid SQUASHFS superblock`), consistent with
   the claim's disclosed limits.
