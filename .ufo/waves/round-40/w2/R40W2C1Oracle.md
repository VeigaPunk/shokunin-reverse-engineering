CONFIRMED — the R40-C1 oracle is exact on all four carriers (frozen reader byte-identical to the committed tables; independent `sasquatch-v4be` extraction agrees on 718/718 file sha256+size, 352/352 symlink targets, 145/145 directories, 2/2 devices; the AVM identity is real and locally reproducible). The L2 miss that produced 3/4 is a counter-side path-suffix false positive — DEFECTS FOUND in `c1-counter.py`'s `nonregular_unpublished_ok`, not in the carriers or the oracle.

# R40W2C1Oracle — attack on the R40-C1 oracle (round 40, wave 2)

Seat: `R40W2C1Oracle`. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scope attacked: the four frozen carriers (V1, V2 rebuilt by `fetch-vendor.py`; L1, L2 from `corpus/evidence/round-40/c1/*/carrier.sqsh`), the frozen reader
`tools/round-40/sqfs-list.py` at freeze `7fce308631a8b457d6b7c5a4b39a923c4e9a49de`, the committed `oracle.tsv` / `nonregular.tsv` tables, the AVM layout
identity itself, and — laterally, because the author's NOT-MET verdict rests on it — the single failing counter clause.
Everything below was run in scratch `/fast/scratch/hyaku/kaidoku-r40/R40W2C1Oracle` and removed at the end; the citable outputs are in
`.ufo/waves/round-40/w2/artifacts/R40W2C1Oracle/`. No tool was installed or upgraded (python3 git, `sasquatch`/`sasquatch-v4be` 4.5.1, unblob 26.6.4 were already present and untouched).

## 1. Frozen reader reproduces the committed tables, byte for byte

`reader/sqfs-list.py` = `git show 7fce308…:tools/round-40/sqfs-list.py`, sha256 `1079fa9b36a87e62b2de8ca594cfc0820e52b3450199076d9d7cc2e870353cd9`
(identical to the working-tree file). Per carrier:

```
python3 -I -B reader/sqfs-list.py --layout avm \
  --files out/<ID>/oracle.tsv --nonregular out/<ID>/nonregular.tsv out/<ID>/carrier
```

| carrier | exit | oracle.tsv | nonregular.tsv |
|---|---|---|---|
| V1 | 0 | MATCH 697 lines | MATCH 381 lines |
| V2 | 0 | MATCH 8 lines | MATCH 95 lines |
| L1 | 0 | MATCH 7 lines | MATCH 13 lines |
| L2 | 0 | MATCH 6 lines | MATCH 10 lines |

`diff -q` silent on all eight comparisons (artifact `reader-diff.txt`). No row, hash, size, kind or symlink target differs.

Vendor byte chain re-verified from scratch: `fetch-vendor.py --root … --rev 7fce308… --cache … --image-cache …` exited 0 with both carriers `ok:true`,
`image_sha256` = `f518ce6b…ede6d` / `3948449d…9450`, member sha256 = `334e56df…f3d4` / `cacc6461…4b19`, carve = pin `ac4098bd…8e95` / `5ccc7614…089b`,
sizes 5 442 392 / 26 013 550. Both are carved exactly to `bytes_used`.

## 2. Independent extraction agrees with the tables on every object

`sasquatch-v4be -f -no-exit-code -n -d x/<ID>/root out/<ID>/carrier` (no `-be`), exit 0 on all four, then a stdlib walk of the extracted tree
(`cmp.py`, artifact `sasq-compare.json`):

| carrier | files in table / extracted | sha256 mismatches | size mismatches | missing/extra files | symlinks table/extracted | bad targets | dirs table/extracted | devices |
|---|---|---|---|---|---|---|---|---|
| V1 | 697 / 697 | 0 | 0 | 0 / 0 | 263 / 263 | 0 | 117 / 117 | `dev/led` char 247:0 |
| V2 | 8 / 8 | 0 | 0 | 0 / 0 | 85 / 85 | 0 | 9 / 9 | `dev/led` char 247:0 |
| L1 | 7 / 7 | 0 | 0 | 0 / 0 | 2 / 2 | 0 | 11 / 11 | none |
| L2 | 6 / 6 | 0 | 0 | 0 / 0 | 2 / 2 | 0 | 8 / 8 | none |

Totals: 718 regular files, 352 symlinks, 145 non-root directories, 2 character devices, 0 fifo/socket/hardlink. The 118/10/12/9 "created directories"
lines in the sasquatch logs include the extraction root; the reader deliberately omits the root directory, and my walk confirms the counts reconcile exactly.
V2's `filesystem_core.squashfs` (25 378 816 bytes) is present as an ordinary file and was not opened — matches the "not claimed" list.
Sparse handling is exercised (V1 `sparse_blocks: 1`) and still hashes identically.

Table hygiene (`oracle-integrity.json`): no duplicate path in any oracle or non-regular table, no path that is both a file and a non-regular entry in any
carrier, every oracle row 3-column with a valid 64-hex sha256, sums of file sizes 21 681 493 / 27 008 292 / 238 530 / 244 251 bytes.

## 3. The AVM layout identity is real — verified independently in stdlib Python

`avm-id2.py` (artifact `avm-id2.json`): parse the 96-byte superblock big-endian, then walk the 2-byte metadata block-length headers from
`inode_table_start` to `directory_table_start`, reading the header little-endian and big-endian. (The header's bit 15 is the "stored uncompressed" flag;
`sizes = raw & 0x7FFF`. My first pass omitted that mask and *falsely* failed L1/L2 — recorded here because it is a real trap for anyone re-checking by hand.)

| carrier | inode_table_start → directory_table_start (delta) | LE walk | BE walk | `mkfs_time == bytes_used` |
|---|---|---|---|---|
| V1 | 5 421 468 → 5 430 042 (8 574) | 5 blocks (1380, 1872, 2204, 1776, …) lands exactly | first header 25 605 — implausible, no walk | 5 442 392 == 5 442 392 |
| V2 | 26 011 444 → 26 012 150 (706) | 1 block 704, lands exactly | 16 386 — implausible | 26 013 550 == 26 013 550 |
| L1 | 229 534 → 230 468 (934) | 1 block raw 0x83A4 (uncompressed 932) → 2+932 = 934, lands exactly | 0xA483 = 9 347 — out of range | 230 884 == 230 884 |
| L2 | 240 269 → 241 068 (799) | 1 block raw 0x831D (797) → 799, lands exactly | 7 555 — *plausible length*, yet the walk ends at 247 826 ≠ 241 068 | 241 390 == 241 390 |

Second, independent metadata sequence on the two multi-table carriers (V1/V2): the directory-table walk `directory_table_start → fragment_table_start`
also lands exactly under LE (V1: 4 blocks, 5 430 042 → 5 440 850; V2: 2 blocks, 26 012 150 → 26 013 226) and fails under BE (V1 implausible at 5 440 066;
V2 first header 8 196 — rejected only by the 8 192 bound). Reading the structural fields little-endian is nonsense by contrast
(`inodes` 923 009 024 / 1 744 830 464 / 352 321 536 / 285 212 672, `compression` 1024 / 1024 / 1024 / 256, i.e. the "SquashFS version [1024.0]" line sasquatch prints).

Calibration note that matters for the reader's design: on L2 a BE header read yields a *length that passes plausibility* (7 555 ≤ 8 192). Only the
end-position identity `2 + len + inode_table_start == directory_table_start` rejects it. The identity, not plausibility, is the load-bearing test — consistent
with the reader's documented `auto` ordering and with the claim's statement that the marker is the trigger and the header endianness is the format.

Discriminators built from the L2 tree with the frozen writer (`gen-squashfs.py`, artifact `extractor-negative-controls.txt`):

- `stdbe.sqsh` (`--endian be`, 241 390 bytes, sha256 `98575b56…5025`, mkfs_time 1 700 000 000 ≠ bytes_used, no marker):
  `sqfs-list --layout avm` **exit 2** (`metadata body out of bounds: offset 240271 length 7555`); `--layout be` exit 0 and its file table equals the L2 oracle;
  `sasquatch-v4be` without `-be` **exit 1, 0 files** ("File system corruption detected").
- `marker-be.sqsh` (`--endian avm`, 241 390 bytes, sha256 `f75fc6bf…d2cf`, mkfs_time == bytes_used, i.e. the round-39 marker on a standard-BE body):
  identical outcome — `--layout avm` exit 2, `--layout be` reproduces the table, `sasquatch-v4be` without `-be` exit 1, 0 files.
- On the four real carriers the mirror image holds: `sasquatch` (LE build) exit 1 / 0 files on all four, `sasquatch-v4be -be` exit 1 / 0 files on all four,
  `sasquatch-v4be` (no `-be`) exit 0 and complete.

So the AVM layout is not a marker-only artefact and not a naming convention: BE structural fields + LE metadata headers is a distinct, measurable layout, and
unblob 26.6.4's `squashfs_v4_be`-without-`-be` path is the only one of the three extractor invocations that succeeds.

## 4. Lateral finding — the 3/4 score rests on one defective clause

I did not re-run the counter (parent owns the gate); I read the frozen score `.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json` and independently
reconciled the four receipts against the frozen tables (`rec.py` → `receipts.json`, `gap-reconciliation.json`):

- every oracle file is published with the same sha256 in all four receipts (`oracle_missing_n` = 0 for V1/V2/L1/L2; 697/8/7/6 published);
- every receipt names exactly one `squashfs_v4_be` chunk with no `extraction_failed`, subject digest == carrier pin, output directory under `/kaidoku-r40/`;
- gaps are exactly one `unpublished-entry` per symlink plus one structural `depth-limited`, and nothing else — 264 (V1), 86 (V2), 3 (L1), 3 (L2); every gap
  path resolves to exactly one non-regular entry, every symlink has exactly one gap, no gap lands on a directory or device. The prose predicate's gap wording
  is satisfied on all four.

The only false clause anywhere in the four carrier blocks is L2's `nonregular_unpublished_ok`. Its evidence:

```
L2 oracle.tsv      usr/bin/busy   e28f81fc…4870   40000      (a real regular file)
L2 nonregular.tsv  bin/busy       symlink        /usr/bin/busy
L2 after.json      published:     firmware.bin_extract/usr/bin/busy
score JSON         "nonregular_published": ["firmware.bin_extract/usr/bin/busy"],
                   "nonregular_unpublished_ok": false
```

`c1-counter.py:606` defines `same_rel(candidate, rel) = candidate == rel or candidate.endswith('/' + rel)`, `nonregular_published()` (line 643) applies it
to every published *regular file* against every non-regular *entry path*, and line 1092 turns any hit into `nonregular_unpublished_ok = False`. The clause's
own docstring (line 54) states the intent as "no published regular file path **equals** a non-regular entry path". Equality — resolved against the same
extraction root — holds: `usr/bin/busy ≠ bin/busy`. The endswith test conflates a file at `usr/bin/busy` with the distinct node `bin/busy` whose target happens
to be `/usr/bin/busy`; the `/bin/* -> /usr/bin/*` shape that produces it is the normal BusyBox layout, so the clause misfires on exactly the vendor images it is
meant to certify. Across all four receipts there are **zero** exact path collisions and exactly **one** suffix-only collision (L2, this one).

Consequence for the round: the frozen counter's exit 1 is reproducible and, under the freeze-integrity rule (the tool is a frozen path), procedurally correct —
but it is not evidence about coverage. On the same bytes, all four carriers satisfy the prose predicate P40-C1 and the documented intent of the failing clause;
V1's 697 files, 263 symlinks and 1 device alone demonstrate the handler/carrier/gap behaviour C1 was written to certify. Any downstream reading of "NOT MET" as
"AVM-BE coverage was not demonstrated" would be wrong.

Advisory repair (not applied — tools/ is outside my write scope and the counter is frozen): resolve the receipt path against the extract root and compare for
equality, e.g. strip the single leading `<root>/` segment before comparing, and keep `same_rel` only where a hash also gates the match (as `oracle_hits` does).

## 5. Frozen-path integrity (read-only git)

`git diff --name-only 7fce308… 42c10a58… -- <frozen C1 paths>` (…`c1-counter.py c1-extra.py c1-run.sh fetch-vendor.py sqfs-list.py gen-squashfs.py
mk-l-carriers.py .ufo/waves/round-40/c1/{carriers.json,gap-rule.json} corpus/evidence/round-40/c1/ plans/round-40-claims.md`) lists only the eight receipt
files `{V1,V2,L1,L2}/{after,run}.json`; the same command against tip `4d62ee5a…` lists the same eight and nothing else. Blob ids of all eight oracle/nonregular
tables, `carriers.json`, and both `carrier.sqsh` files are identical at freeze and tip (`frozen-path-check.txt`). So the tables I reproduced are the frozen ones.

## 6. Limits of this finding

- I verified the oracle side end to end but did **not** recompute the REA 6.5.0 `evidence_id`s or the `plus-extractor` rerun projection; both are reported true in
  the frozen score and are the parent gate's to re-exercise. The disclosed limit ("the rerun cannot prove which process wrote the committed receipt") stands
  untouched — nothing here bears on it.
- I did not adjudicate PROVINCE/README/SOURCES text, the demotion at 4d62ee5a, or R40-C2. Whether the L1's procedural stop should be re-opened is the L1's call;
  my finding is only that the miss has a counter-side cause and that the world-side coverage is intact.
- The 0x8000 uncompressed-metadata flag is required to reproduce the L1/L2 identity by hand; a checker that forgets it will wrongly conclude the AVM headers are
  not little-endian on the two lane-built carriers.

## Artifacts

`.ufo/waves/round-40/w2/artifacts/R40W2C1Oracle/`: `reader-diff.txt`, `sasq-compare.json`, `avm-id2.json`, `avm-id2.py`, `cmp.py`, `receipts.json`,
`gap-reconciliation.json`, `oracle-integrity.json`, `extractor-negative-controls.txt`, `frozen-path-check.txt`, `commands.txt`, `reader-sqfs-list-at-freeze.py`.
No vendor firmware bytes and no extracted vendor files are copied into the lane (AVM licence); carriers are cited by sha256 only.

Report: .ufo/waves/round-40/w2/R40W2C1Oracle.md
