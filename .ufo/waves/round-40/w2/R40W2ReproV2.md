# R40W2ReproV2 — independent reproduction of R40-C1 carrier **V2**

**Verdict: CONFIRMED.** I attacked the V2 slice of P40-C1 (FRITZ!Box 6820v1 LTE 07.30 member):
carrier rebuilt from the pinned vendor chain **without** `fetch-vendor.py`, layout decoded from bytes,
oracle re-derived with the frozen reader, a fresh REA 6.5.0 `--max-depth 1` run, and the committed
receipt scored with the frozen counter's own clause functions. Every V2 clause evaluates true, the
`plus-extractor` projection of my fresh run is equal to the committed receipt, and the committed
evidence id recomputes to the stored id. Nothing in the V2 slice could be falsified.

Reviewed revisions: base `fa6a8a3f`, freeze `7fce3086`, C1 receipts `73c7bf9c`, measured
`42c10a58`, landing `4d62ee5a`. Lane worktree at dispatch `0b15c8b2`. Worktree bytes of
`tools/round-40/c1-counter.py`, `sqfs-list.py`, `.ufo/waves/round-40/c1/{carriers.json,gap-rule.json}`
were compared to their freeze bytes and are identical (counter freeze sha256 `8d288e4c…f17e81`,
reader freeze sha256 `1079fa9b…353cd9`).

## What I attacked

1. The vendor chain: can V2's carrier be re-derived from `carriers.json` alone (URL → image → tar
   member → carve), with no use of the lane's fetcher, and does each link land on the pinned hash?
2. The **format**: is V2 genuinely the AVM layout the claim defines (BE structural fields,
   **little-endian** 2-byte metadata block-length headers, marker `mkfs_time == bytes_used`), or only
   a marker-carrying BE body?
3. The oracle: does the **frozen** reader reproduce the committed `oracle.tsv`/`nonregular.tsv`, and
   does a direct `sasquatch-v4be` (no `-be`) extraction agree with it?
4. The receipt: does a fresh REA 6.5.0 run on my independently rebuilt bytes give the same
   `plus-extractor` projection, the same 8 published files, the same 86 gaps, the same subject pin?
5. The published set: do all 8 published regular files match the oracle on path suffix, sha256 **and
   size**, and is the nested `filesystem_core` image among them and unopened at depth 1?
6. The scored landing: does the frozen counter, fed only my rebuilt V2 bytes, score V2 `matched=true`
   with every clause true (calibrating against the L1's 3/4 receipt)?

## Method (exact commands, exit codes)

Scratch `S=/fast/scratch/hyaku/kaidoku-r40/R40W2ReproV2`; `TMPDIR=$S`; all runs `cd "$S"`.

```
curl -fsSL -o FRITZ.Box_6820v1_LTE-07.30.image \
  https://download.avm.de/fritzbox/fritzbox-6820-lte/other/fritz.os/FRITZ.Box_6820v1_LTE-07.30.image   # rc=0
tar -xOf FRITZ.Box_6820v1_LTE-07.30.image ./var/tmp/filesystem.image > member.bin                      # rc=0
head -c 26013550 member.bin > carrier-V2.bin
```

```
python3 -I -B <lane>/tools/round-40/sqfs-list.py --layout avm \
  --files reader/oracle.tsv --nonregular reader/nonregular.tsv --inspect carrier-V2.bin   # rc=0
git -C <lane> show 7fce3086:tools/round-40/sqfs-list.py > sqfs-list-frozen.py
python3 -I -B sqfs-list-frozen.py --layout avm --files reader2-oracle.tsv \
  --nonregular reader2-nonregular.tsv carrier-V2.bin                                      # rc=0
```

```
PATH="$HOME/.local/bin:$PATH" HYAKU_SCRATCH=/fast/scratch/hyaku \
  bash <lane>/tools/round-40/c1-run.sh oracle carrier-V2.bin repro-oracle "$S/scratch-oracle"  # rc=0
PATH="$HOME/.local/bin:$PATH" HYAKU_SCRATCH=/fast/scratch/hyaku \
  bash <lane>/tools/round-40/c1-run.sh after  carrier-V2.bin repro-after  "$S/scratch-after"   # rc=0
```

```
mkdir -p cache && cp carrier-V2.bin cache/5ccc7614263e4b4b392025e1561e071a744b6464a4c88548633e87f71f3d089b.bin
python3 -I -B <lane>/tools/round-40/c1-counter.py --root <lane> --rev 42c10a58… \
  --freeze 7fce3086… --pkg65 ~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --carrier-cache "$PWD/cache" --json-out v2-counter.json     # rc=1 (expected: V1 absent from my cache only)
```

Clause-level checks (projection, `oracle_hits`, `gap_check`, `nonregular_published`,
`provenance_ok`, `frozen_drift`) were run by importing the **freeze bytes** of `c1-counter.py`
(sha256 `8d288e4c…f17e81`) as a module and calling its own functions on the committed and my fresh
`after.json`, plus `evidence_ids()` (which drives the frozen `xpin` tool against rea-agents 6.5.0).

Toolchain actually used: Python 3.14.8, rea-agents 6.5.0 via `npx -y`,
unblob 26.6.4 (`/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`, sha256 `0ce7b624…a1d09`),
sasquatch-v4be 4.5.1 (sha256 `fac88740…b7214c6`). **No installs or upgrades were performed.**

## Results

| Link / clause | Observed | Verdict |
|---|---|---|
| Vendor image | 28 334 080 B, sha256 `3948449d…9450` = pinned `image_sha256` | ok |
| Tar member `./var/tmp/filesystem.image` | 26 013 704 B, sha256 `cacc6461…4b19` = pinned `member_sha256` | ok |
| Carve `[0, 26013550)` | 26 013 550 B, sha256 `5ccc7614…089b` = carrier pin; `bytes_used` = 26 013 550 | ok |
| Product corroboration | `var/version`: `FIRMWAREVERSION=142.07.30,,107859`; `var/content`: `Fritz_Box_HW214 (FRITZ!Box 6820 LTE)`, `Version=07.30` | matches `carriers.json` product |
| Format | magic `sqsh`, v4.0, compression 4 (xz), `mkfs_time` 26 013 550 == `bytes_used` 26 013 550 (marker true); inode-table header bytes `c002` → LE length 704, BE length 16 386 (> 8192, implausible); **identity** 26 011 444 + 2 + 704 = 26 012 150 = `directory_table_start` | genuine AVM layout |
| Frozen reader | regenerate both tables → byte-identical to committed (`oracle.tsv` `e9a63f07…bf408` 8 rows / 700 B; `nonregular.tsv` `ffc4fb61…44f46` 95 rows / 2 563 B) | ok |
| `sasquatch-v4be` (no `-be`, `-f -no-exit-code -n`) | rc 0, `check_files` 8, `check_symlinks` 85, `files_equal` true, `mismatch_count` 0, `oracle-check.tsv` sha == `oracle.tsv` sha | ok |
| Fresh REA 6.5.0 (`--max-depth 1`) | rc 0, envelope `ok=true`, 2 273 ms, chunks `["squashfs_v4_be"]`, no `extraction_failed`, coverage `partial`, 8 files, `published_bytes` 27 008 292, 86 gaps (85 `unpublished-entry` + 1 `depth-limited`), `depth_limited_paths` = `["$output/firmware.bin_extract"]`, 1 derivation | ok |
| Projection `plus-extractor` (frozen `projection_diff`) | **equal**, `diff_keys=[]` | ok |
| Oracle hit with size | 8/8 rows match published suffix **and** sha256 **and** size | ok |
| Gap rule (`gap_check`, frozen rule) | `True: 86 gaps (1 structural) on 95 non-regular entries`; the 85 `unpublished-entry` paths are exactly the 85 symlinks (set-equal); dirs (9) and the char device `dev/led` `247:0` carry no gap | ok |
| `nonregular_published` | `[]` (no published regular file collides with a non-regular entry) | ok |
| Subject / operation / provider | `5ccc7614…089b` = pin; `extract_firmware`; `unblob` | ok |
| Run provenance | committed `parameters.output_directory` = `/fast/scratch/hyaku/kaidoku-r40/run-V2/extract`, `provenance_ok` true; `parameters.max_depth` = 1 | ok |
| Evidence id | frozen `xpin` recompute `ev_0c412f3a…f0c2175` == stored `ev_0c412f3a…f0c2175` | ok |
| Receipt freshness | `after.json` first added `73c7bf9c…`; freeze is an ancestor of it and it is an ancestor of `42c10a58` | ok |
| Frozen drift | `frozen_drift(FREEZE..42c10a58) = []`, `frozen_drift(FREEZE..4d62ee5a) = []` | ok |
| Frozen counter on my rebuilt bytes | `carriers.V2.matched = true`, all 17 clauses true, `published_files` 8, `oracle_hits` 8, `gaps_note` "86 gaps (1 structural) on 95 non-regular entries" | ok |

Aggregate of that same counter run with only V2 in the cache: `carriers_matched=2` of `target=4`
(`V2` true, `L1` true, `V1` `carrier_present=false` because I deliberately rebuilt only V2, `L2`
`matched=false` on `nonregular_unpublished_ok`), `exit_code=1`. That pattern reproduces the L1's
3/4-at-`42c10a58` receipt minus V1.

## The nested core image (assigned sub-check)

`after.json` publishes exactly 8 regular files; one is
`firmware.bin_extract/filesystem_core.squashfs`, size 25 378 816, sha256 `b88a1895…c4834d8`, which is
**exactly** the oracle row (`filesystem_core.squashfs  b88a1895…  25378816`). It is not opened at
depth 1: `derivations` has one edge (outer input → `firmware.bin_extract`, handler `squashfs_v4_be`)
and `depth_limited_paths` names the extraction root only.

I re-extracted the carrier with `sasquatch-v4be -f -no-exit-code -n` in scratch to read the nested
file's own bytes: it is itself a big-endian `sqsh` v4.0 xz image with the marker true
(`mkfs_time == bytes_used == 25 374 950`), LE metadata header `dc06` → 1 756 (BE reading 23 558
implausible), `bytes_used` 3 866 bytes below the published size — i.e. the nested image is a complete
genuine AVM-layout body, not truncated. P40-C1 explicitly does not claim it; this only confirms the
"nested, not opened" description.

## Falsification attempts that failed

- **Marker-only standard-BE body?** No: the metadata header endianness identity lands on LE exactly
  (704 → `directory_table_start`), and the BE reading is out of range.
- **Oracle not reproducible by the frozen reader?** No: byte-identical `oracle.tsv` and
  `nonregular.tsv` from the freeze-bytes reader, and the independent `sasquatch-v4be` listing hash-equals
  the reader's.
- **Committed receipt not a real run of these bytes?** A fresh run on bytes I rebuilt myself matches on
  every `plus-extractor` field, including 8 file hashes/sizes, chunk handler/range, gap list, unpublished
  list, and `published_bytes`.
- **Receipt fabricated from the oracle?** Not distinguishable by design (disclosed limit), but the
  projection clause plus the exact `published_bytes`, gap ordering and 85-entry unpublished list are
  oracle-closed only by construction; my rerun reproduces them independently.
- **Gap rule bent for V2?** No: exactly 85 gaps for 85 symlinks, none for 9 dirs or the char device,
  one structural `depth-limited`, no `unknown-chunk-handler`.
- **V2 scored by a different revision's counter?** No: counter bytes at the freeze and in the worktree
  are identical; `frozen_drift` is empty through the landing.
- **Wrong carrier identity?** No: image, member and carve each hit their pinned sha256; `var/version`
  and `var/content` independently say FRITZ!Box 6820 LTE (HW214) 07.30 / build 107859.

## Limits and inference

- The carve drops 154 trailing member bytes (144 NULs + `00 00 23 de 53 c4 34 b8 ec 21`) beyond
  `bytes_used`. That is the frozen `external.length` rule and the extraction is complete against the
  oracle, so nothing observable depends on them; what those bytes are is **not** determined here.
- The rerun shows V2 extracts through the pinned toolchain at scoring time; it cannot prove which
  process wrote the committed receipt (the claim's own disclosed limit). **[INFERENCE]** the committed
  receipt and my run are the same extraction result; identity of writer is unproven and unclaimed.
- REA still records no extractor argv on success; the absence of `-be` is evidenced by the
  `squashfs_v4_be` handler branch plus my direct `sasquatch-v4be` argv, not by the receipt.
- My counter slice is not a full-claim score: V1 was not rebuilt, so `carriers_matched` from my run is
  not comparable to the target 4.
- Vendor image, member, carrier and extracted vendor files stayed in scratch and were deleted; only
  derived receipts/listings (paths, hashes, sizes) are in the artifacts dir.

## Observations outside this seat's slice (not C1-V2 defects)

- **L2's single failing clause is mechanically the suffix collision the L1 described.** In my counter
  run L2 failed only `nonregular_unpublished_ok` with `nonregular_published =
  ["firmware.bin_extract/usr/bin/busy"]`; L2's `nonregular.tsv` names `bin/busy symlink /usr/bin/busy`
  and its `oracle.tsv` names the regular file `usr/bin/busy` (`e28f81fc…`, 40 000 B).
  `same_rel('firmware.bin_extract/usr/bin/busy','bin/busy')` is true because of the bare
  `endswith('/' + rel)` test. This corroborates the L1's reading; it is an L2 question, not mine.
- Committed `V2/after.json` `parameters.path` records the L1 scratch cache path
  (`…/_l1/cache/5ccc7614….bin`), i.e. the receipt's provenance points at scratch, not at a committed
  file. That is consistent with the licence constraint (vendor bytes are never committed) and does not
  enter the projection, but it means the receipt alone cannot be re-derived without the pinned chain.

## Artifacts (`.<lane>/.ufo/waves/round-40/w2/artifacts/R40W2ReproV2/`)

`repro-evidence.json` (all measured values), `repro-after-run.json`, `repro-after-after.json`,
`repro-oracle-run.json`, `repro-oracle.tsv`, `repro-nonregular.tsv`, `repro-oracle-check.tsv`,
`frozen-reader-inspect.json`, `c1-counter-v2-slice.json`.
