# R44C1Oracle — round 44 wave 1, seat report

**Seat:** R44C1Oracle (executor) · **Lane:** `kaidoku-shokunin` ·
**Base:** `c29360e3ba5381a5ab69e372d0d9577970f85018` · **Date:** 2026-10-28

## What I built

`tools/round-44/c1-oracle.py` — the frozen oracle builder for R44-C1. Authored in
my artifacts dir; the L1 installs it under `tools/round-44/`.

| artifact (my artifacts dir) | sha256 |
|---|---|
| `c1-oracle.py` | `a90ddc3bfd89c3f167dedfa93a05b9af7707314958dfc1fdf9c60f1e09eee65e` |
| `c1-oracle.json` (full oracle blocks + receipt data) | see `receipt.json` |
| `carriers.oracle-block.json` (the `carriers.json` oracle block) | — |
| `receipt.json` (run receipt) | — |

## The two oracles

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
emitted block records this as `output_tree.producer_lineage` so the counter
cannot be built on a false independence premise.

## Result on the frozen carriers — all six

`tools/round-44/carriers.json` was frozen by the L1 mid-wave and grew to **six**
carriers (the four of my seat spec plus `v21le`/`v21be`, the `squashfs_v2` 2.1
pair). The tool reads that file as the authoritative carrier list (each entry
supplies its own `path`, `sha256`, `handler`, `endian`, `expected_regular` and
`output_tree`), so it covers all six, not just the four named in my spec.

| id | handler | endian | regular members | non-regular | oracle A digest | oracle B digest | agree |
|---|---|---|---|---|---|---|---|
| `v1le` | `squashfs_v1` | le | 3 | 0 | `8faae7739b14315c…` | `8faae7739b14315c…` | yes |
| `v1be` | `squashfs_v1` | be | 3 | 0 | `8faae7739b14315c…` | `8faae7739b14315c…` | yes |
| `v2le` | `squashfs_v2` | le | 4 | 0 | `4178bb8379de3e55…` | `4178bb8379de3e55…` | yes |
| `v2be` | `squashfs_v2` | be | 4 | 0 | `4178bb8379de3e55…` | `4178bb8379de3e55…` | yes |
| `v21le` | `squashfs_v2` | le | 4 | 0 | `4178bb8379de3e55…` | `4178bb8379de3e55…` | yes |
| `v21be` | `squashfs_v2` | be | 4 | 0 | `4178bb8379de3e55…` | `4178bb8379de3e55…` | yes |

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
| 1 | `python3 -I -B c1-oracle.py --selftest` | 0 | 20 cases, 0 failures |
| 2 | `python3 -I -B c1-oracle.py --root . --work … --json-out … --receipt …` | 0 | 6 carriers, 2 oracles agree |
| 3 | same, `--oracle-root <tampered tree>` (one `apple1.txt` rewritten) | 1 | carrier `v21le` fails on the sha256 divergence |
| 4 | same, `--oracle-root <nonexistent>` | 2 | could-not-evaluate |
| 5 | same, `--carriers <file with id v9-zz>` | 2 | unknown carrier id refused |
| 6 | same, `--only nosuch` | 2 | no carrier matches |
| 7 | same, `--only v1le --only V1LE` | 0 | id spelling is separator/case-insensitive |
| 8 | same, `--merge-carriers <copy of frozen carriers.json>` | 0 | all six entries receive an `oracle` block |

Receipt #2 (`exit 0`, `stdout_sha256 dd5fbfcc6f618c0230e3253ec61e2698bd4df3db1e0a41eeee5adfa74e4c5869`,
`wall_s 0.032`, `carriers: v1be v1le v21be v21le v2be v2le`, `problems: []`).

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
