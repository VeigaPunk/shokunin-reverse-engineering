# C1RunPort — R50-C1 run harness port (wave 1, pre-freeze)

**Verdict: DONE, draft ready for L1 review.** `tools/round-50/c1-run.sh` (draft at
`.ufo/waves/round-50/w1/C1RunPort/tools/round-50/c1-run.sh`, sha256
`5ab17c60fdf8a122dea1012d64b7ec477570c540a0fdf7692d174b2a46f05035`, 850 lines, `bash -n` clean) runs both arms
end to end on the real c6430 carrier (scratch outdir only; nothing written to the lane tree or evidence root).
Oracle arm: exit 0, three producers agree on all 3955 regular files; five mutation overlays each exit 3.
After arm: exit 0, REA 6.5.0 names `squashfs_v4_le`, all 3955 oracle files published with identical sha256+size.

## Findings the L1 must fold (ordered by consequence)

| # | Finding | Evidence |
|---|---|---|
| F1 | **Plan table error: c6430's rootfs is NOT `./var/tmp/filesystem.image`.** The cable image carries `./var/remote/var/tmp/x86/filesystem.image` (23,863,304 B, `hsqs` v4.0 xz, `mkfs_time == bytes_used == 23861507`, member sha256 `25194a87e54f98d868c614cef4ef8509c3e8f34bd6498bc03cdc3e7dcdd4934c`) and a second member `./var/remote/var/tmp/filesystem.image` (5,984,264 B) that is **big-endian AVM `sqsh`** (xz, `mkfs_time == bytes_used == 5981012`) — i.e. the Atom/x86 LE rootfs plus the ARM BE rootfs in one image. The harness refuses the BE one (exit 2) by construction. Pin the chain with the `x86` member path or the carrier is the wrong (BE) one. | tar listing of the 35,911,680 B image (image sha256 `52e3687d7363301453aa4fe0c712126874c90d3c138dee0792213dab11f5d815`, HTTP 200, 2026-10-28T23:32:52Z); superblock reads in this seat's scratch |
| F2 | **a7530 needs non-default REA budgets** (relayed by L1/C1ControlsBuild, not run by me): `--max-output-files 100000 --max-output-bytes 536870912` (schema maxima). The harness carries both as the frozen default for **every** carrier (`C1_MAX_OUTPUT_FILES`/`_BYTES` override, recorded in `argv`); the receipt then records them in `parameters.max_output_files/_bytes`, which the counter's rerun already replays (`REPLAY_PARAMS`). | `after.json` `.parameters` on c6430: `{"max_depth":1,"max_output_bytes":536870912,"max_output_files":100000,...}` |
| F3 | **Reader layout:** `--layout auto` and `--layout le` both parse the LE xz member and produce byte-identical tables (3955 files, 824 non-regular: 255 dir / 568 symlink / 1 char-device); `avm` is the BE layout and must not be used. The harness runs `auto` (primary) and `le` and exits 3 if they differ. | reader inspect: `endian little, compression xz, avm_marker true`, `block_length_signal` `plausibility` (auto) / `layout-le` (le) |
| F4 | **Three-way oracle agreement is real, not a tautology:** reader (`sqfs-list.py auto`), `/usr/bin/unsquashfs` 4.7.5 (`-no-xattrs -no-progress -f -no-exit-code`, tree walked + hashed, devices from `-lln`) and `sasquatch -le -f -no-exit-code` 4.5.1 produce `oracle.tsv` = `oracle-unsquashfs.tsv` = `oracle-check.tsv` (sha256 `f657ef51…b5165`, 3955 rows). Dir/symlink rows of `nonregular.tsv` are also compared against both extraction trees, device/fifo/socket rows against the `-lln` listing. Mutations: wrong sha, dropped row, wrong size, wrong symlink target, wrong device major:minor → each exit 3 with `mismatch_count` 2/2/2/2/1. | `receipts/c6430-scratch-dev/` |
| F5 | **Gap/removal families the c6430 receipt actually shows** (input for C1GapRule/C1CounterPort): (a) one 8-byte tail chunk `firmware.bin_extract/23863296-23863304.unknown` (a regular *file* outside the squashfs chunk root, plus gap `unknown-chunk-handler`: the member is padded to 4096 so bytes_used < file size); (b) gap `depth-limited` for the squashfs chunk root; (c) 567 `unpublished-entry` gaps, all `symlink`; (d) the 568th symlink, `usr/www/avm/cgi-bin/system_status -> /usr/www/cgi-bin/system_status` (absolute target), is **neither published nor unpublished-entry**: unblob diagnostic `MaliciousSymlinkRemoved`; (e) the char-device `dev/led` and the 255 dirs appear in no gap. Coverage is `partial`; 2 chunks, 3956 files (3955 + the tail). The round-41 three-family rule must cover (a) and (d) or c6430 fails `gaps_ok`. | `after.json` of the final run; python check: oracle 3955 vs published 3955 equal, 0 missing, 0 extra; 568 symlinks − 567 unpublished = the removed one |
| F6 | **CTL-C1-3 is realisable but the sasquatch precondition is real:** with `sasquatch` absent from the child PATH (`C1_CHILD_PATH` without `~/.local/bin`) the arm refuses (exit 2). Under `C1_ALLOW_NO_SASQUATCH=1` (recorded `sasquatch.precondition_waived: true`) REA exits 0 and the receipt carries `extraction_failed: true`, gap `missing-extractor-dependency` (handler `squashfs_v4_le`), diagnostic `ExtractorDependencyNotFoundReport` dependencies `["sasquatch"]`, 2 files only (carved chunks). unblob 26.6.4 `SquashFSExtractor.EXECUTABLE = "sasquatch"`, argv `-le` for an LE image; `sasquatch-v4be` is only used for BE images with the AVM marker. **The harness `exit 0` here — it records negatives and lets the counter judge**; it prints a stderr note when a chunk failed. | `receipts/c6430-scratch-dev/no-sasquatch-waived.run.json` |
| F7 | Receipt `parameters.path` records the carrier path (my scratch path); the counter's rerun uses its own `carrier.bin` path, so the counter's projection already has to ignore it (round-41 behaviour, not measured here). `parameters.output_directory` = `/fast/scratch/hyaku/kaidoku-r50/c1-run.XXXXXX/extract` passes the counter's prefix test; the harness checks it (`harness_observations.receipt_output_directory_prefix_ok`) and refuses a scratch base that cannot produce it. | final run `run.json` |
| F8 | The round-49 unblob log tee is **deliberately not ported**: it changes `REA_UNBLOB_COMMAND` and hence the receipt's `engine.executable_path/sha256`, which the counter's rerun projection may compare; the plan's P50-C1 has no `extract_env` clause. The extractor identity is instead evidenced by `unblob` 26.6.4 source + F6. | design note |
| F9 | Environment: `/usr/bin/time` is absent on this host (timing uses `date +%s%N`); the unblob command resolves through the uv venv symlink (`REA_UNBLOB_COMMAND=/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`, sha256 recorded in `run.json`). | |

## What changed against round 41 / round 49 (the port delta)

* CLI `c1-run.sh after|oracle --id ID --carrier FILE [--outdir DIR] [--scratch BASE] [--pin SHA] [--data-run] [--force] [--keep-scratch] [--dry-run]`
  (r41 was positional `MODE CARRIER OUTDIR [SCRATCH]`; default outdir `<lane>/corpus/evidence/round-50/c1/<id>`, lane = script's grandparent, else `--outdir` required).
* **Data-run guard** (r49): `after` always refuses without `--data-run`/`KAIDOKU_C1_DATA_RUN=1`; `oracle` refuses when OUTDIR contains `/corpus/evidence/round-50/` without it. `--dry-run` prints the plan, writes nothing. Occupied `after.json`/`oracle.tsv` slot → exit 2 unless `--force`.
* **Scratch hardening**: base must carry `/kaidoku-r50/` (`C1_ALLOW_FOREIGN_SCRATCH=1` waives, recorded); `after` also requires the `/fast/scratch/hyaku/kaidoku-r50/` prefix (the counter's test). A private `c1-run.XXXXXX` is made *inside* the base and only that dir is removed (r41 `rm -rf`'d a caller-supplied SCRATCH).
* Fixed child PATH = r49 `FIXED_PATH`; `C1_CHILD_PATH` override recorded. Pins enforced (exit 2 unless `C1_ALLOW_PIN_DRIFT=1`): unblob 26.6.4, sasquatch 4.5.1, unsquashfs 4.7.5, rea-agents 6.5.0.
* Superblock precondition (both arms): `hsqs` offset 0, v4.0, comp 4, `mkfs_time == bytes_used`, `bytes_used <= size`; reader `--inspect` must agree; `C1_ALLOW_NONAVM=1` waives (CTL-C1-4 standard-LE control), recorded. Checked **before** anything is created in OUTDIR.
* Oracle: reader auto+le, plus unsquashfs and sasquatch `-le` (r41 had reader + sasquatch-v4be); new table `oracle-unsquashfs.tsv`; fields `unsquashfs`/`sasquatch` in `oracle-run.json`; TSV-unsafe paths (tab/newline) are exit 3.
* After: `--max-output-*` (F2); `summary` now bounded (gaps_detail/unpublished head ≤20 + counts by kind, `chunks_detail`, `parameters`) because r41's unbounded summary passed through `jq --argjson` and died with *"Argument list too long"* on the 2 MB receipt (observed, rc 126 on the first c6430 run); `harness_observations` (subject digest = carrier, output-dir prefix, `squashfs_v4_le` named, no failed chunk); exit 3 when the subject digest ≠ carrier or no receipt.
* jq field renames: `sasquatch_v4be` → `sasquatch`; schema `kaidoku-r50-c1-run-v1`.

## Test log (all in scratch `/fast/scratch/hyaku/kaidoku-r50/C1RunPort`, removed at exit)

| check | command (abbrev.) | exit | result |
|---|---|---|---|
| syntax | `bash -n c1-run.sh` | 0 | clean |
| dry run | `c1-run.sh oracle … --dry-run` | 0 | plan printed, nothing written |
| after without `--data-run` | `c1-run.sh after … ` | 2 | refused |
| oracle into `…/corpus/evidence/round-50/…` without `--data-run` | | 2 | refused |
| foreign scratch `/fast/scratch/hyaku/foreign` | | 2 | refused; no outdir created |
| bad `--pin` | | 2 | refused |
| BE member (`sqsh`) as carrier | `--carrier c6430-small.member` | 2 | refused; no outdir created |
| **oracle, c6430 (final)** | start 2026-10-28T23:41:07Z, `--pin 25194a87…` | **0** | 3955 / 824 rows (255 dir, 568 symlink, 1 char-device), 3 tables identical, wall 10.3 s under load (5.2–5.7 s idle runs; reader ≈2.1 s, unsquashfs ≈0.7 s, sasquatch ≈0.6 s) |
| **after, c6430 (final, scratch outdir)** | 2026-10-28T23:41:17Z, `--data-run` | **0** | `squashfs_v4_le`, partial, 3956 files, 2 chunks, subject digest = carrier, wall 64.6 s under load (11.7 s idle) |
| mutations ×5 (wrong sha/dropped/size/symlink/device) | wrapper reader `receipts/…/mutation-wrapper.py` | 3 ×5 | each flagged |
| after, no sasquatch on PATH | `C1_CHILD_PATH=/usr/bin:/bin:<fnm>` | 2 | precondition |
| after, no sasquatch, waived | `C1_ALLOW_NO_SASQUATCH=1` | 0 | F6 |

sha256 of key outputs (final run): `oracle.tsv`/`oracle-unsquashfs.tsv`/`oracle-check.tsv` `f657ef513614824a9bfcf9f297bbe14482ac27a97dc6bb898481f2f1e49b5165`;
`nonregular.tsv` `cb691b4420cb2232eee6018af2776b59376a1116482066fc2d9834f85ed77594`; `oracle-run.json` `933359c10ae220931385193d28b545d54d4ff23c4624c0757f8f1502591f3361`;
`run.json` `6dd22383fa61454400abd090b9861c76d564a74d6bb5396dbb2e13e59caff28c`; after receipt `after.json` `79232d7087038de13a0cd633155039c49e57a86e7c7e59e02dd995320456edd0` (not copied: 2.2 MB, scratch-path-dependent; the final scratch is deleted). Oracle stdout was empty (sha `e3b0c442…`).
Carrier chain recorded: image `FRITZ.Box_6430_Cable-07.30.image` sha256 `52e3687d…d815`; member `./var/remote/var/tmp/x86/filesystem.image` sha256 `25194a87…4934c`. No vendor bytes are in the lane tree; only listings/hashes/receipts under `w1/C1RunPort/receipts/`.

## Open items for the L1 (not mine to decide)

1. Choose the c6430 member path (F1) and re-check the other three carriers' member paths (`a7530`, `a7590`, `c6490`) — only c6430 was inspected here.
2. Decide whether `after` should exit 3 when a chunk has `extraction_failed` (currently exit 0 + note; the counter judges).
3. The counter port must use the same `FIXED_PATH` (r41 counter's rerun inherits the ambient PATH) and replay the max-output parameters (it already does).
4. `oracle-unsquashfs.tsv` is an extra evidence file beyond the four named tables; drop it from the commit if the freeze wants exactly four (the comparison verdict is in `oracle-run.json` anyway).
5. `HYAKU_SCRATCH` ≠ `/fast/scratch/hyaku` makes `after` refuse (the counter's prefix test), by design.

Tools installed/updated: none. Scratch removed after receipt copy.
