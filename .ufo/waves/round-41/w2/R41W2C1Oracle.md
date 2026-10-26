CONFIRMED — attacked R41-C1's four-carrier independent oracle, AVM-vs-auto agreement, and LE metadata-header evidence; found no counterexample on the specified carriers.

## Axis and scope

Attacked **coverage** (whether all four pinned carriers' frozen tables reproduce from carrier bytes), **depth** (whether distinct producers and opposite-endian decodes independently confirm paths and hashes), and **calibration** (what was and was not established). This is scoped to V3/V4/L3/L4 and the C1 oracle artifacts; it does not revisit REA after-receipts, the landing's documentation, or C2.

## Procedure and exact evidence

Frozen claim reviewed first: `plans/round-41-claims.md`, including `## Changes from the draft` (C1 oracle definition lines 78–80, exact pins and carriers lines 60–73). I used the frozen `tools/round-41/sqfs-list.py` and harness `tools/round-41/c1-run.sh` from the lane at the checked-out working tree tip `e1c83313f33a3d97edbd8fef402db2d06172fcdc`. Read-only path log inspection showed all four committed oracle/nonregular tables first added at freeze `d764389e`; this run did not alter frozen paths. Relevant code hashes are not asserted beyond the frozen revision references.

Scratch setup: `S=/fast/scratch/hyaku/kaidoku-r41/R41W2C1Oracle`, `TMPDIR="$S"`, `HYAKU_SCRATCH=/fast/scratch/hyaku`; scratch was cleaned before yield. Tools: Python 3.14.8; REA package CLI reports 6.5.0 (used only to identify the environment, not run on carriers); unblob `26.6.4`; `sasquatch-v4be` reports unsquashfs 4.5.1, SHA-256 `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`; unblob SHA-256 `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`.

Commands/evidence:

- Vendor rebuild: `python3 -I -B <lane>/tools/round-41/fetch-vendor.py --root <lane> --rev d764389e9cbe61b9d1b07538ff3bff02d50bb34f --cache "$S/cache" --json-out "$S/fetch.json"` → exit 0; V3 and V4 each `ok:true`, `http 200`, all image/member/nested/carrier hashes match the manifest. No vendor/extracted payload is copied to artifacts.
- Lane-carrier rebuild: `python3 -I -B <lane>/tools/round-41/mk-l-carriers.py --lane <lane> --builds 2 --json "$S/lcar/result.json" "$S/lcar"` → exit 0; two builds each agree, and rebuilt L3/L4 hashes equal the frozen pins exactly.
- Independent check: a local driver ran `python3 -I -B tools/round-41/sqfs-list.py` with both `--layout avm` and `--layout auto`, each writing separate file/nonregular tables and inspect JSON, then ran `/home/vgpnk/.local/bin/sasquatch-v4be -f -no-exit-code -n [-o OFFSET] -d ROOT CARRIER` with **no `-be`** and hashed every extracted regular file. All commands exited 0. This direct run is kept separately from the frozen harness run.
- Frozen harness oracle arm: `bash <lane>/tools/round-41/c1-run.sh oracle <carrier> <artifact-dir> "$S/runscratch-$id"` for each carrier → all four exit 0. It reran `--layout avm` and its direct sasquatch cross-check; each recorded `files_equal:true`, mismatch_count 0, direct extractor exit 0.
- The direct comparator checked complete `(path, sha256, size)` rows, not just cardinalities; nonregular complete `(path, kind, detail)` rows; and exact paths for both AVM-vs-auto tables. Every comparison matched, with zero missing, extra, changed, path or hash rows.
- A separate independent Python inode-table metadata-header walk read each BE SquashFS superblock's `inode_table_start` and `directory_table_start`, then stepped the 2-byte block-length header chain under LE and BE decoding. The LE walk terminates exactly at `directory_table_start` for all four. BE fails immediately with an impossible metadata length >8192. The committed reader's AVM inspect additionally reported `header_endian=little`, `avm_marker=true`, and no warnings for all four. AVM and auto produced identical complete file and nonregular tables in all cases.

## Results by carrier

| Carrier | Regular paths | Nonregular paths (dir / symlink / char device) | Rebuilt AVM vs committed | AVM vs auto | direct sasquatch vs reader | LE inode chain | BE inode chain |
|---|---:|---|---|---|---|---|---|
| V3 | 8 | 9 / 85 / 1 (95 total) | exact, 8/8 | exact, 8/8 and 95/95 | exact, 8/8 | 1 block, len 724, lands exactly | first len 21506 > 8192 |
| V4 | 6349 | 401 / 615 / 1 (1017 total) | exact, 6349/6349 | exact, 6349/6349 and 1017/1017 | exact, 6349/6349 | 31 blocks, lands exactly | first len 26631 > 8192 |
| L3 | 13 | 20 / 3 / 0 (23 total) | exact, 13/13 | exact, 13/13 and 23/23 | exact, 13/13 | 1 block, len 1411, lands exactly | len 16877 > 8192 |
| L4 | 14 | 17 / 3 / 0 (20 total) | exact, 14/14 | exact, 14/14 and 20/20 | exact, 14/14 | 1 block, len 1337, lands exactly | first len 14725 > 8192 |

All four have `sqsh` at offset 0, `mkfs_time == bytes_used == file length`, and carrier SHA matches its pin. In V3/V4, the sole special node is one character device; the direct extractor omitted it as expected. Its regular-file table still matched completely. The extractors report all symlinks present (V3 85, V4 615, L3/L4 3 each); this is observation about this direct invocation, not a general symlink disposition guarantee.

## Artifacts

Full evidence is in `.ufo/waves/round-41/w2/artifacts/R41W2C1Oracle/`:

- `oracle-run/<ID>/oracle-run.json`: frozen harness run record (including complete cross-check mismatch list and inspect); `oracle.tsv`, `nonregular.tsv`, `oracle-check.tsv` are copied from harness output.
- Per-ID `committed-*`, `regenerated-*`, `oracle-auto.tsv`, `nonregular-auto.tsv`, `direct-sasquatch-files.tsv`, `inspect-avm.json`, `inspect-auto.json`, `direct-run.json`, `carrier-pin.json`: byte-level tables and run context sufficient to inspect every row and SHA.
- `comparison.json`: comparison results and inspect metadata; `meta-walk.txt` (if present) reports independent LE/BE inode-chain walks; scripts `driver.py`, `compare.py`, `meta_walk.py` describe the replay procedure.

The committed and regenerated tables are small enough to include. Firmware and extracted firmware bytes are not included. Rebuild vendor carriers with the fetch command above (the original licensed URLs/hashes are in `carriers.json`); reproduce the L3/L4 carriers with the lane-builder command above.

## Verdict / limits

No oracle falsifier found for the frozen V3/V4/L3/L4 pins. I independently regenerated and fully compared every file path, SHA-256 and size and every nonregular path/kind/detail, saw exact AVM-vs-auto agreement, and directly reproduced exact regular-file sets with sasquatch-v4be without `-be`. The LE metadata-header conclusion is supported for the full inode table chain on each carrier, not inferred from a single plausible decoded length. This confirms the tested oracle portion only; it does not establish which prior process created freeze-time tables, validate REA run provenance, nor expand C1 beyond the named carriers.

One attempted invocation initially passed unsupported `--root` to `mk-l-carriers.py` and exited 2; after reading its CLI I reran with its positional outdir and documented flags, successfully. A prior scratch metadata-walker print bug was corrected before collecting the reported full result. Neither failed scratch attempt changed lane inputs.
