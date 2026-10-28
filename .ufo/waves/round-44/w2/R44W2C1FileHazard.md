# R44W2C1FileHazard — the `file(1)` hazard on the frozen R44-C1 carriers

Seat `R44W2C1FileHazard`, wave 2 (falsification), lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Measured revision `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`; freeze
`c48f8a4bfd449300c975668e59aae5b5538b6a84`. I changed no claim, counter, rubric, frozen byte or
production doc; everything below is measurement against the lane as committed.

**Verdict — CONFIRMED, with two precision defects and one record-level (not score-level) defect.**

1. The `file(1)` mislabel is real and reproducible, exactly where the record says it is: both BE
   carriers' compression token, and both v1 carriers' block size. `unsquashfs` reads all four
   correctly. (Record: `corpus/lessons/round-44.md` R44-CL5; `plans/round-44-claims.md:40-44`.)
2. **No scored path trusts `file`.** Proven four ways (§4): the freeze-time oracle invocation is the
   only `file` call in the tool tree, it writes into a *frozen* table that no consumer reads, and
   stripping or corrupting that table changes the counter's output by zero bytes. The counter's
   compression class is derived from the inode-table metadata block, as the claim states.
3. `R44-CL5`'s wording is accurate as written. Two supporting statements are not: the claim's
   byte-20 gloss (D3) and its `compression_family` field name (D2), which exists in no instrument.

---

## 1. Measurement — `file` vs `unsquashfs -s` on the four frozen carriers + the v2ns pair

`file` 5.48-1 (`/usr/bin/file`, sha256 `9e9ecf97…505e63d0`; magic `…/misc/magic.mgc` sha256
`c2f4e7e5…324f268`). `unsquashfs` 4.7.5 (2026/03/01). Raw outputs:
`artifacts/R44W2C1FileHazard/01-file-on-carriers.txt`, `02-unsquashfs-s.txt`; per-command exit,
stdout sha256 and wall time in `receipts.json` (receipts 0–11).

| carrier | file: endian/version | file: token | file: block size | unsquashfs: version | unsquashfs: compression | unsquashfs: block size | disagreement |
|---|---|---|---|---|---|---|---|
| `v1-le--squashfs_v1.0_le.bin` | le 1.0 | `compressed` | `-32768` | 1:0 le | inodes+data compressed | `32768` | **block size** (sign) |
| `v1-be--squashfs_v1.0_be.bin` | be 1.0 | **`uncompressed`** | `-32768` | 1:0 be | inodes+data compressed | `32768` | **token + block size** |
| `v2-le--squashfs_v2.0_le.bin` | le 2.0 | `compressed` | `65536` | 2:0 le | inodes+data+fragments compressed | `65536` | none |
| `v2-be--squashfs_v2.0_be.bin` | be 2.0 | **`uncompressed`** | `65536` | 2:0 be | inodes+data+fragments compressed | `65536` | **token** |
| `v2ns-le--squashfs_v2.0_le.bin` | — (`data`, exit 0) | none | none | exit 1 `FATAL ERROR: Can't find a valid SQUASHFS superblock` | none | none | both refuse to read it |
| `v2ns-be--squashfs_v2.0_be.bin` | — (`data`, exit 0) | none | none | exit 1 `FATAL ERROR: Can't find a valid SQUASHFS superblock` | none | none | both refuse to read it |

Endianness and `s_major`/`s_minor` are read correctly by `file` on all four carriers
(`hsqs`/`sqsh`, 1.0/2.0). The v2ns pair is not in `carriers.json` and is not scored; both tools
declining it is consistent with `squashfs_v2_nonstandard` staying Frontier.

Disagreements, in the record's terms — exactly as `R44-CL5` states, and no others:

- compression token: **both BE carriers**, wrong direction (`uncompressed` where the image is
  zlib-compressed on inodes, data and (v2) fragments);
- block size: **both v1 carriers**, `-32768` vs the image's `32768`. Same magnitude, negative sign —
  a signed-16 rendering of the true value, not a different number;
- v2 block size, all endianness, and every LE token: agree.

## 2. Root cause, measured (not inferred from the claim)

Controlled single-byte flips on a scratch copy (`/fast/scratch/hyaku/kaidoku-r44/R44W2C1FileHazard/
flip*.bin`; no fixture under `corpus/` is written). Full log:
`artifacts/R44W2C1FileHazard/04-flip-experiments.txt`.

The token is the **u16 at offset 20 read in the image's own endianness**, interpreted as the
SquashFS *v4* `compression` id:

| probe (v1le, bytes@20–23 = `47 00 00 00`) | token |
|---|---|
| baseline | `compressed` |
| b20=0x00, b21=0x00 (u16 = 0) | `uncompressed` |
| b20=0x01 (u16 = 1) | `zlib compressed` |
| b20=0x02 (u16 = 2) | `lzma compressed` |
| b20=0x03 (u16 = 3) | `lzo compressed` |
| b20=0x00, b21=0x01 (u16 = 0x0100) | `compressed` |
| v1be b21=0x01 (BE u16 = 1) | `zlib compressed` |
| v1be b20=0x01 (BE u16 = 0x0100) | `compressed` |

`zlib`/`lzma`/`lzo` are the v4 compression ids, so the field being read is v4's `compression`
(u16@20), not any v1/v2 field. In a v1/v2 image offset 20 is `inode_table_start` u32@20
(`plans/round-44-claims.md:41-42`, `c1-counter.py:290-299`), so:

- LE carrier: u16@20 = `inode_table_start & 0xFFFF` = 71 / 88 → non-zero → "compressed"
  (right answer, wrong reason);
- BE carrier: u16@20 = `inode_table_start >> 16` = 0 for any image under 64 KiB of inode-table
  offset → "uncompressed". **Structural**: every v1/v2 BE image with `inode_table_start < 65536`
  mislabels this way.

Block size, by controlled flip: the v1 branch reads a **signed u16 at offset 32** (b32=0xFF →
`-32513`, b33=0xFF → `-256`) — offset 32 is the first byte outside the counter's own v1/v2 field
table (`SB_SIZE = 32`, `c1-counter.py:289`), and the value there happens to be `0x8000` on these
fixtures → `-32768` printed. The v2 branch was insensitive to every byte I flipped (32, 33, 34) and
reports a constant `65536`; for these two images
that constant coincides with the true block size. `[INFERENCE]` (not measured): the v2 branch
hard-codes `65536` in the magic rule rather than reading the image.

## 3. The literal `grep -n "file(" tools/round-44/*.py` audit

59 hits in 6 files (`artifacts/…/03-grep-file-calls.txt`, receipt 12, exit 0, stdout sha256
`606b1aea…d450d6424`). Classification of all 59:

| count | hit | is it `file(1)`? |
|---|---|---|
| 37 | `os.path.isfile(` | no — stat |
| 15 | `sha256_file(` | no — digest helper |
| 2 | `shutil.copyfile(` | no — copy |
| 1 | `tar.extractfile(` (`c2-counter.py:768`) | no — tar member |
| 1 | `member.isfile()` (`c2-counter.py:766`) | no — tar member |
| 3 | prose: `c1-counter.py:52`, `c1-oracle.py:421`, `c1-oracle.py:731` | no — comments/notes *about* `file(1)` |

The binary is invoked in exactly one place in the whole round-44 tree:

- `tools/round-44/c1-oracle.py:717` — `file_out = run(["/usr/bin/file", "-b", image])`;
- its result is stored at `c1-oracle.py:727` as `sb_summary["file_verdict"]` with the note
  `"informational only … Do not bind the counter to this word"` (`:729-736`);
- `sb_summary` becomes `"superblock_info"` on the carrier block (`c1-oracle.py:936`), and
  `c1-oracle.py --merge-carriers` rewrites `tools/round-44/carriers.json` in place
  (`c1-oracle.py:1174-1179`).

`grep -rln "usr/bin/file" tools/round-44 tools/round-45` → only `c1-oracle.py` and `carriers.json`.
Zero hits in `c1-counter.py`, `c1-run.py`, `c1-run.sh`, `c1-controls.py`, `c2-counter.py`,
`c2-controls.py`, `c2-rubric.json`, `tools/round-45/frozen-path-preflight.py`.

## 4. Which binding could read `file` text as an oracle property? None — four independent proofs

The only place `file` text is committed is `tools/round-44/carriers.json` (frozen), 4 blocks at
lines `190`, `433`, `703`, `976`, carrying e.g. `…version 1.0, uncompressed, 177 bytes … blocksize:
-32768 bytes…` for v1be.

1. **Static.** `file_verdict` occurs 0 times in `c1-counter.py`, `c2-counter.py`, `c2-rubric.json`,
   `c1-controls.py`, `c1-run.py`, `tools/round-45/frozen-path-preflight.py`. The counter's only
   `carriers.json` reads are the frozen-spec validator (`carriers_spec`, keys `handler`, `path`,
   `sha256`, `size`, `s_major`, `s_minor`, `compression`, `expected_regular`, `oracle.members`,
   `oracle.nonregular`, `oracle.output_tree*`, `oracle_root`, `receipt`) and the per-carrier
   `layout_probe`.
2. **The binding the claim names exists and is metadata-derived.** `c1-counter.py:1125-1137` sets
   `d['compression']` only from `compression_class(raw[its+2 : its+2+length])` of the **first
   inode-table metadata block body**, framed by `its + 2 + length == directory_table_start`
   (`:1135-1160`); `:1165-1168` compares it to the frozen `compression` (`zlib(gzip)`, normalised).
3. **Dynamic — stripping `file_verdict` changes nothing.** Importing `c1-counter.py` as a module at
   `55bcce69`, evaluating the frozen spec as-is, then again with `oracle.superblock_info` deleted
   from all four carriers: identical `ids`, `problems`, `notes` and per-carrier probes
   (`superblock_info_stripped_identical: true`). Corrupting every `file_verdict.stdout` to
   `"GARBAGE compressed OK"` and `exit: 99`: identical
   (`file_verdict_corrupted_identical: true`). Artifact `05-binding-experiment.json`, receipt 14.
4. **The binding can fail on its real source.** Setting the frozen `compression` to `lzma` makes the
   probe red with `observed compression 'gzip' is not the frozen 'lzma'` — so the pass is neither
   vacuous nor fed by `file`. Same artifact.

Runtime confirmation of 3–4 on the scored path: the full counter at `55bcce69` (REA rerun enabled,
`--pkg65` rea-agents 6.5.0) reports `compression_detail ["gzip","gzip","gzip","gzip"]` —
compare `file`'s own verdicts, `["compressed","uncompressed","compressed","uncompressed"]`. Its
per-carrier `layout` carries `meta_header_hex` `3700`/`0038`/`2e00`/`0030` and
`meta_uncompressed: false`, no `file_verdict` key, and the string `"Squashfs filesystem,"` appears
nowhere in the 18 403-byte output (`06-counter-at-55bcce69.json`, receipt 15, exit 1, wall 7.12 s,
stdout sha256 `eea45d37…b450f1`).

## 5. Findings

### D1 — a frozen artifact embeds an undigested tool's output (record-level, low; not score-level)

- Path:line: `tools/round-44/c1-oracle.py:717` (invocation) → `:727`/`:729-736` (recorded verdict) →
  `:936` (into the carrier block) → `tools/round-44/carriers.json:190,433,703,976` (committed bytes).
- Command / exit / observed:
  - `python3 -I -B tools/round-44/c1-counter.py … --rev 55bcce69 …` → exit 1,
    `carriers_matched 4`, `met_target false` — i.e. **the hazard changes no score**;
  - `grep -rln "usr/bin/file" tools/round-44 tools/round-45` → exit 0, only
    `c1-oracle.py`/`carriers.json`;
  - module experiment (§4.3) → exit 0, `identical: true` for both mutations.
- Why it is still a defect: `carriers.json.toolchain` pins exactly `7z`, `sasquatch`,
  `sasquatch-v4be`, `unblob`, `unsquashfs` — **`file` has no digest**. The four
  frozen `file_verdict` strings were produced by `file` 5.48 + this host's `magic.mgc`, so
  re-running `c1-oracle.py --merge-carriers` anywhere else (different `file`/magic) changes a
  **byte-frozen** file (`c1-counter.py:276`, and `FROZEN_PREFIXES 'tools/round-44/'`), which the
  counter would then report as `frozen_path_changed`. The record is safe today only because the
  bytes are already committed.
- Minimal future fix (not applied, mine to report): either add `file` + `magic.mgc` digests to the
  `toolchain` block, or drop `file_verdict`/`superblock_info` from the table the oracle writes into
  the frozen file — the tool's own note already says nothing should bind it.

### D2 — the claim names a field that exists in no instrument (low, prose)

- `plans/round-44-claims.md:43` and `:134` bind `compression_family == 'zlib(gzip)'`.
- Command / exit / observed: `grep -rc compression_family tools/round-44/*.py tools/round-44/*.json`
  → exit 1, **0 in all 8 files**. The instrument's frozen field is `compression`
  (`carriers.json:4,247,490,763`), the observed one is `compression_detail`
  (`c1-counter.py:2204`), the frozen-label normaliser is `normalize_compression` (`:308`).
- Effect: a reader can confirm the substance (the class *is* bound) but cannot grep the field the
  claim names. The record's own lesson wording (`R44-CL5`, "the C1 counter binds compression from
  the inode-table metadata block") avoids the name and is accurate.

### D3 — the byte-20 gloss is exact only for LE (low, precision)

- `plans/round-44-claims.md:40`: "`file`'s compressed/uncompressed token is byte-20's value, which is
  the low byte of `inode_table_start`".
- Measured (§2): the token is a **u16** read at offset 20 (b21 alone flips it: u16 0x0100 →
  `compressed`), and for the BE carriers byte 20 is the **high** byte of `inode_table_start`, not the
  low one — which is precisely why BE reads `uncompressed`. Offset 20 is right; "byte" and "low byte"
  are not, for half the carrier set.
- No scored consequence: the claim's conclusion (never bind to `file` text) stands, and the counter
  never reads it.

### O-1 — observation outside this seat's hazard lane (for the C1-verdict seat / L1, not a `file` defect)

Running the full counter at `55bcce69` (receipt 15) gives `carriers_matched 4`, `met_target false`,
`frozen_path_changed []`, and **`bindings_false == ['province_core_section','province_core_row',
'frontier_note']`**. `provenance`/`path_shape_ok` are **true** for all four carriers, with
`output_directory = /fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/…/rea-out`.

- `province_core_section`/`province_core_row` are false by design under an honest stop — `PROVINCE.md`
  at `55bcce69` carries `## Round-44 measured, not promoted (R44-C1 honest stop)` (`:424`), not
  `## Round-44 additions to Core`.
- `frontier_note` is false because `c1-counter.py:2161` requires the note line to contain both
  `Round-44 frontier note` **and** the entry stem `2026-10-28-r44-squashfs-v1v2-core`; the note at
  `PROVINCE.md:430` contains the marker and neither the stem nor any knowledge-entry link
  (`git show 55bcce69:PROVINCE.md | sed -n '424,431p' | grep -c 2026-10-28-r44-squashfs-v1v2-core`
  → 0, exit 1).
- So the record's narrative (`R44-CL2`, `PROVINCE.md:428`) — the stop is the claim-vs-counter
  `output_directory` disagreement — is true of the *prose*, but no counter binding fails on it: the
  counter's `provenance_ok` (`c1-counter.py:1176-1182`) requires the `/kaidoku-r44/` segment and the
  receipts satisfy it. What actually reds are the promotion-doc bindings, which an honest stop
  makes false by construction. Whether the record should say that explicitly is the C1-verdict
  seat's call; I did not change any doc.

## 6. Limits of this seat's verification

- I did not rebuild `carriers.json` (that would touch a frozen path); the toolchain-drift claim in D1
  is reasoned from `c1-oracle.py`'s write path plus the missing `file` digest, not from an executed
  second build.
- The v2 branch's constant `65536` (§2) is `[INFERENCE]` from its insensitivity to flips of bytes
  32, 33 and 34; I did not disassemble `magic.mgc`.
- I re-ran the counter only at `55bcce69`; I did not re-run it at the lane tip (M44-2 is another
  seat's contract) and I make no claim about the tip's `frozen_path_changed` set.
- No tools were installed or upgraded for this seat.

## 7. Receipts and artifacts

All under `.ufo/waves/round-44/w2/artifacts/R44W2C1FileHazard/`; `receipts.json` carries seat,
exact argv, cwd, exit, stdout sha256, stdout bytes and wall time for every command.

| # | tool | subject | exit | stdout sha256 (16) |
|---|---|---|---|---|
| 0–5 | `/usr/bin/file -b` | the six carriers | 0 | `89077980…`, `efc4e315…`, `73825a75…`, `50839c4b…`, `6667b2d1…` ×2 |
| 6–11 | `/usr/bin/unsquashfs -s` | the six carriers | 0,0,0,0,1,1 | `d04c69f3…`, `890c069d…`, `5c30636f…`, `479d7299…`, `e3b0c442…` ×2 |
| 12 | `grep -n "file("` | 6 × `tools/round-44/*.py` | 0 | `606b1aea…` |
| 13 | flip harness | 15 controlled byte flips | 0 | `c467d729…` |
| 14 | `python3` (imports `c1-counter.py`) | strip / corrupt `file_verdict` | 0 | `d247a382…` |
| 15 | `c1-counter.py` full path | `--rev 55bcce69 --freeze c48f8a4` | 1 | `eea45d37…` |

Artifacts: `01-file-on-carriers.txt`, `02-unsquashfs-s.txt`, `03-grep-file-calls.txt`,
`04-flip-experiments.txt`, `05-binding-experiment.json` (pure payload; its sha256 equals the
recorded stdout sha256 of receipt 14) with the command header in
`05-binding-experiment.receipt.txt`, `06-counter-at-55bcce69.json`,
`06-counter-at-55bcce69.stdout`, `receipts.json`. Scratch
(`/fast/scratch/hyaku/kaidoku-r44/R44W2C1FileHazard/`, one `git clone --shared`, `work/`, `work2/`,
flip copies) is deleted on exit; no `/tmp` path is cited and no lane file other than this report and
its artifacts was written.
