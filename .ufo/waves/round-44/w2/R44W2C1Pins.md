# R44W2C1Pins — frozen C1 carrier pins and the v1/v2 superblock, re-derived

Seat `R44W2C1Pins` · lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
measured revision `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac` · freeze
`c48f8a4bfd449300c975668e59aae5b5538b6a84`.

**Verdict.** The four frozen carrier pins are **confirmed 4/4** (byte-identical at the measured
revision and in the worktree, size 4096 each), and every field the frozen table binds —
magic/endianness, `s_major`, `s_minor`, `bytes_used` u32@8 — **matches** on all four. The
v1/v2 layout statement's *values* are true; its *provenance and one provenance-relevant field*
are not: the claim binds compression to `flags`-NOD-clear but neither the frozen table nor the
frozen counter ever reads byte 36, the frozen table calls the superblock 32 bytes when the
on-disk headers are 51 and 63 bytes, the counter's layout-conflict advisory cannot fire for the
frozen block's own key shape, and the layout is attributed to registry row **S119**, which is
the REA 6.5.0 npm tarball, not unblob's handler. **No lane byte was changed**; the four defects
below are record-level and route to round 45.

Evidence: `../w2/artifacts/R44W2C1Pins/evidence.json` (sha256 `37dcdd84…16df683a`),
`pins.json` (`1d32ea96…7b377459`), `src/` excerpts. Commands, exit codes, wall times and
stdout digests: `artifacts/R44W2C1Pins/receipt.json`.

## 1. Pins — confirmed

`git -C <lane> show 55bcce69:<path> | sha256sum` → exit 0 for all four; worktree bytes are
identical (`cmp`/byte equality via the evidence script, not the broken `cmp -l`).

| id | path under `corpus/evidence/round-42/c2/fixtures/` | sha256 @55bcce69 = frozen pin | size |
|---|---|---|---|
| v1le | `v1-le--squashfs_v1.0_le.bin` | `b45925fa779eae0293635ce0e6dc8760308f25227dd88645d677ba3ffce23e71` | 4096 |
| v1be | `v1-be--squashfs_v1.0_be.bin` | `529e10775cc152e6c5df0c6c63316811004cc73ce99f03989c86ffd396d631e6` | 4096 |
| v2le | `v2-le--squashfs_v2.0_le.bin` | `7c62dbe388b972119f5d17a12836a016737d58276184f4caa2a90dafd924f124` | 4096 |
| v2be | `v2-be--squashfs_v2.0_be.bin` | `79c0f3886291f4abcc656acd49932446cf16afaa67e6ffb0c5258e3c2e2dfcc0` | 4096 |

`tools/round-44/carriers.json` is the same blob at the freeze, the measured revision and HEAD
(`5f20d073b488f62b7ff501905621a7b6ba44b502`, sha256 `3b90b999…97868e9`), and the counter blob
at 55bcce69 equals HEAD's (`9695d586…b4fe1569`), so the instrument I read is the instrument that
scored.

Oracle consistency, re-derived from the frozen table (not from the tool): regular-member counts
are 3/3/4/4 = `expected_regular`, and the recomputed `output_tree_digest` (sha256 over
`<path>\t<sha256>\n` sorted bytewise) equals the frozen `8faae773…4894f2a48` (v1) and
`4178bb83…b0535f947` (v2).

## 2. Superblock — decoded fields vs the frozen expectations

Byte order taken from the magic only (`hsqs` = le, `sqsh` = be), exactly as the counter does;
all values below are measured from the frozen bytes.

| id | magic | inodes | bytes_used@8 | uid@12 | guid@16 | inode_tbl@20 | dir_tbl@24 | s_major@28 | s_minor@30 | **flags@36** | no_uids@37 | no_guids@38 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v1le | `hsqs` | 4 | 176 | 172 | 0 | 71 | 128 | 1 | 0 | **0x00** | 1 | 0 |
| v1be | `sqsh` | 4 | 177 | 173 | 0 | 71 | 129 | 1 | 0 | **0x00** | 1 | 0 |
| v2le | `hsqs` | 5 | 196 | 192 | 0 | 88 | 136 | 2 | 0 | **0x40** (DUPLICATE) | 1 | 0 |
| v2be | `sqsh` | 5 | 201 | 197 | 0 | 88 | 138 | 2 | 0 | **0x40** (DUPLICATE) | 1 | 0 |

* `magic`, `s_major`, `s_minor`, `bytes_used` (u32@8) and endianness equal the frozen
  `carriers.json` values and the frozen `oracle.superblock_info.probe_v1v2` rows on all four
  (`agree: True`, all ten checks per carrier true in `evidence.json`).
* `flags` bit 1 (`SQUASHFS_NOD`) is **clear on all four** — the claim's stated relation
  "NOD clear ⇒ compressed" is **true of these bytes**.
* No compression field exists in 0..31: the first 28 bytes are magic/inodes/bytes_used/
  uid_start/guid_start/inode_table_start/directory_table_start, then `s_major`/`s_minor`.
  The counter's own compression class comes from the inode-table metadata block:
  header `3700`/`0038`/`2e00`/`0030` (length 55/56/46/48, uncompressed bit clear), body starts
  `78da` on all four, and `inode_table_start + 2 + length == directory_table_start` in each
  endianness. `probe.ok = True`, `reason = null`, `compression = "gzip"` 4/4.
* `file(1)`'s token is an offset-20 artefact, reproduced: offset 20 is `47`/`00` for v1le/
  v1be and `58`/`00` for v2le/v2be, and `file` prints "compressed" for the two LE images and
  "uncompressed" for the two BE images whose high byte is zero — exactly claim item 4.

Corroboration that offsets past 32 are real structure, not padding (the point behind D2):
`mkfs_time@39` decodes to 1722842331 / 1722842338 / 1678381552 / 1678381590, i.e.
2024-08-05 04:18:51 / 04:18:58 and 2023-03-09 14:05:52 / 14:06:30 in the tool's local zone,
matching `unsquashfs -s` line for line; `no_uids@37`/`no_guids@38` = 1/0 match "Number of uids
1 / Number of gids 0"; v2's `block_size@51` = 65536 and `fragments@55` = 1 match "Block size
65536 / Number of fragments 1"; v1's `block_size_1@32` = 32768 matches "Block size 32768".
The v1 data region begins at byte 51 and the v2 data region at byte 63.

## 3. Attacks and outcomes

**A1 — "a field the counter would accept while the claim's prose says something else": FOUND.**
The claim binds the compression family to "the frozen expectation **plus `flags`-NOD-clear**"
(`plans/round-44-claims.md:135`; same relation at `:42`). The counter contains **zero**
occurrences of the `flags` field (`grep -c flags tools/round-44/c1-counter.py` → `0`, exit 1 =
no match), `SB_FIELDS` stops at `s_minor` (`tools/round-44/c1-counter.py:290-301`), and the
frozen `superblock_layout` block has no `flags` key at all (`tools/round-44/carriers.json:1071-1109`).
Counterfactual (`evidence.json → mutations.v1le`): take v1le, set byte 36 to `0x02` (NOD **set**,
i.e. "data uncompressed"), re-pin those bytes (`1a3a9f11…3224c93e`) — `carrier_pin_ok` is true and
`layout_probe` returns `ok: true, reason: null, compression: "gzip"`. Every clause the counter
evaluates is satisfied by a carrier whose own flags contradict the prose's binding.
The selftest cannot catch it: `sb_v12` builds `bytearray(SB_SIZE)` = 32 bytes and appends payload
immediately (`c1-counter.py:2530` ff.), so a synthetic carrier's byte 36 is the ASCII `0x6b` of
`block-payload-`, and no `--selftest` case mutates flags.
*Fair reading:* the sha256 pin does bind byte 36's identity for the four real carriers (all
flags 0x00/0x40, NOD clear), so the four frozen images do satisfy the prose. What is unproven is
the *semantic* conjunct: a future freeze that pins bytes with NOD set (or a carriers.json whose
`compression` label disagrees with byte 36) would reach the same green without any evaluator
objecting. → **D1**.

**A2 — "the claim's v1/v2 layout statement vs the record": CONTRADICTION FOUND.**
`carriers.json:1098` states "SquashFS v1/v2 superblock is **32 bytes** (packed)" while the claim
at `:46` names `flags@36` in the same layout, and byte 36 is the genuine flags byte (measured
0x00/0x40, and unsquashfs derives "Inodes/Data are compressed" from exactly that byte —
`unsquash-1.c` maps `sBlk.s.flags = sBlk_3->flags`). The 32-byte figure is the size of unblob's
*identification* struct (S112, `squashfs.py:123-134`, ending at `s_minor`); the on-disk headers
are **51 bytes (v1)** and **63 bytes (v2)**, measured from where data begins and corroborated by
the block-size/fragments fields unsquashfs reads from 32/51/55. The claim cites both structs as
one layout (`squashfs.py:124-140` **and** `squashfs_compat.h:38-64`); only the second contains
`flags@36`. → **D2**.

**A3 — layout-conflict advisory cannot fire for the frozen block: FOUND.**
`carriers_spec` only inspects keys named `<field>_offset` / `<field>_len`
(`c1-counter.py:882-884`), while the frozen block expresses every offset as `field: [offset, len]`
(`carriers.json:1071-1109`). Demonstrated (`evidence.json → layout_counterfactual`): rewriting the
frozen list values to v4 offsets (`bytes_used [40,8]`, `s_major [0,2]`) yields
`problems: []`, `advisories: []`; adding the key `bytes_used_offset: 40` yields the intended
advisory. So the comment's promise ("a block that declares v3/v4 offsets is recorded") holds only
for a key shape this round does not use. Advisory-only, so no false green today. → **D3**.

**A4 — layout attributed to the wrong registry row: FOUND.**
`carriers.json:1098` and `c1-counter.py:43, :288, :876, :1074` cite `S119` for
`SquashFSv1Handler.C_DEFINITIONS`. `corpus/SOURCES.md:125` defines **S119 = the rea-agents 6.5.0
published package** (npm tarball). The unblob handler row is **S112** (`SOURCES.md:118`), which
the claim itself cites at `:46`. Separately, `squashfs_compat.h:38-64` — the source of
`flags@36`, `mkfs_time@39` and the legacy offsets — has **no registry row**: the sasquatch rows
are S107 (Debian release), S121 (`unsquashfs.c`), S136/S137 (releases), none `squashfs_compat.h`.
The measured values are independently reproducible (this file), but the frozen record's
provenance is wrong. → **D4**.

**A5 — negative controls: counter rejects correctly (no finding).** `layout_probe` returns
`ok: false` with the right reason for: bad magic (`XXXX`), `zlqs`-class endianness misbinding,
`s_major` 3 against a frozen 1 or 2, `bytes_used` 0, and a 24/31-byte truncation. Endianness is
not guessed from the frozen label; it is taken from the magic and compared.

## 4. Numbered defects (route to round 45; no frozen byte may change now)

| id | severity | path:line | finding | command / exit / observed |
|---|---|---|---|---|
| D1 | medium (record ↔ instrument) | `plans/round-44-claims.md:135` (also `:42`), `tools/round-44/carriers.json:5,248,491,764`, `tools/round-44/c1-counter.py:289-301` | Claim binds `compression_family == zlib(gzip)` to "frozen expectation **plus** flags-NOD-clear"; the counter never reads byte 36 and the frozen table has no `flags` key, so the semantic conjunct is unenforced and unexpressed. | `grep -c flags tools/round-44/c1-counter.py` → exit 1, `0`; `python3 -I -B evidence.py` → exit 0, v1le byte36 `0x02` + re-based pin `1a3a9f11…`: `layout_probe ok true`, `compression gzip`, `carrier_pin_ok true` |
| D2 | medium (record) | `tools/round-44/carriers.json:1098`; `tools/round-44/c1-counter.py:287-289, :1094`; `plans/round-44-claims.md:46-47` | "32-byte superblock" contradicts `flags@36` in the same layout and the measured header extent. unblob's 32-byte struct is a prefix; on-disk headers are 51 (v1) / 63 (v2) (`squashfs_compat.h:38-65`, `unsquash-1.c` reads `block_size_1`, `flags`, `mkfs_time` beyond 32). | `python3 -I -B evidence.py` → exit 0, `header_extent_first_data_byte` 51,51,63,63; `unsquashfs -s` → exit 0, block size 32768 (v1, from @32) vs 65536 (v2, from @51), fragments 1 (@55) |
| D3 | low (instrument advisory) | `tools/round-44/c1-counter.py:879-896` vs `tools/round-44/carriers.json:1071-1109` | Offset-conflict advisory keys on `<field>_offset`/`_len`; the frozen block uses `field: [off,len]`, so no declaration is ever checked and a v4-offset list would be silent. | `python3 -I -B evidence.py` → exit 0, `layout_counterfactual.wrong_list_shape.advisories == []`; `bytes_used_offset: 40` → advisory emitted |
| D4 | medium (provenance) | `tools/round-44/carriers.json:1098`; `tools/round-44/c1-counter.py:43,288,876,1074`; `plans/round-44-claims.md:46-47` | `S119` is cited for unblob's v1/v2 struct but S119 is the rea-agents 6.5.0 tarball (`SOURCES.md:125`); the correct row is S112 (`SOURCES.md:118`). `squashfs_compat.h:38-64` has no registry row. | read `corpus/SOURCES.md:118,125`; `grep -n S119 tools/round-44/c1-counter.py` → 4 hits, all layout |

## 5. What this changes — and what it does not

* **Does not** change the R44-C1 verdict: the claim stops with `carriers_matched 4`,
  `met_target false`. None of D1–D4 creates a green path, and none was used as evidence of a
  promotion. The provenance reason for the stop is outside this seat and is unrefuted here.
* **Does not** touch R44-C2, any counter, rubric, frozen byte, `PROVINCE.md`, `README.md`,
  `SOURCES.md`, SCORECARD or LOG.
* **Does** narrow what a future green would prove: at a future `carriers_matched == 4`, the
  flags-NOD-clear conjunct would still be unproven (D1), the "32-byte" description would still
  be wrong (D2), and the layout provenance would still point at the wrong row (D4).
* No repair is possible in-round: all four defects sit in frozen artifacts. They are written as
  findings, not edits.

## 6. Limits

* The full counter (`measure()`) was **not** run: it needs `--pkg65` and counter-time REA
  reruns, and C1's receipt/provenance clauses are other seats' surface. Counter claims here come
  from executing the frozen module's own functions on the real bytes and the real spec
  (`layout_probe` per carrier, `carriers_spec` on the frozen table, `sb_v12`), plus source
  reading — not from a full score run.
* Header extents (51/63) are measured from where the data region begins and corroborated by the
  fields unsquashfs reports from those offsets; they are not read from a struct-size constant.
* `unsquashfs -s` and `file(1)` are corroboration only; neither is used as a binding.
* `grep -c` exit 1 above means "no match", not failure.
* Scratch `/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1Pins/` deleted before yield; no `/tmp`
  evidence; no mutating `git`/`jj`; no tool installs.

## 7. Receipt

`artifacts/R44W2C1Pins/receipt.json` — seat, exact commands, exit codes, stdout sha256, wall
times. Runs: `pin_probe.py` exit 0, stdout sha256 `1d32ea96…7b377459`, 0.024 s;
`evidence.py` exit 0, stdout sha256 `37dcdd84…16df683a`, 0.0328 s.
