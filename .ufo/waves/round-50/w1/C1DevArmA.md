# C1DevArmA — R50-C1 pre-freeze dev arm, carriers a7530 + a7590

Verdict: **both carriers extract and publish every oracle file, but only after raising REA's staging entry budget.**
The round-41 `after` arm argv taken verbatim (`--max-depth 1`, default `--max-output-files 10000`) **fails on both
carriers**: exit 1, `ok:false`, `unreadable_output`, `Staging entry budget exceeded (10000)`, ~2.3 s. Adding
`--max-output-files 20000` gives exit 0, handler `squashfs_v4_le`, 13367/13359 published regular files, zero
missing, zero extra inside the chunk root, zero sha256/size diffs. This is a harness/predicate defect to fix in the
draft before the freeze, not an REA extraction failure.

## Findings that change the drafts

1. **F1 — the round-41 argv cannot be ported unchanged.** 7530 needs ≥15147 staging entries (15145 failed, 15147 passed,
   measured), 7590 about 15148 (not probed at the boundary; passed at 20000). Entries are files + dirs + symlinks +
   the `firmware.bin_extract` dir. Byte budget is fine at the default (published 172.1 MB / 189.9 MB < 268.4 MB).
   REA allows `--max-output-files` up to 100000. The frozen argv, `parameters.max_output_files` in the receipt and the
   counter's expected `parameters` must pin it (I used 20000 for the clean runs; a 100000 + `--max-output-bytes 536870912`
   variant also passed, 40 s / 29 s). Without this the plan's "after-receipt ... no failed chunk" is unobtainable, and the
   round-41 `c1-run.sh` comment ("depth 1 fixes the 10000 budget") holds only for the smaller round-41 BE members.
2. **F2 — an 8-byte trailer becomes a second chunk.** The member is the padded squashfs (`0-34004992`, 4096-aligned from
   `bytes_used`) plus 8 trailing bytes (`23de53c4e5960d62` on 7530, `23de53c4c688c892` on 7590). unblob reports chunk 2
   `handler None`, gap `unknown-chunk-handler` x1, and publishes `firmware.bin_extract/34004992-34005000.unknown`
   (7590: `35835904-35835912.unknown`) outside the chunk root. The round-41 gap rule has `structural.unknown-chunk-handler: 0`
   (`.ufo/waves/round-41/c1/gap-rule.json`) so the port needs `1` for these carriers; the P50 text "names `squashfs_v4_le` for
   the carrier's chunk with no failed chunk" holds (no `extraction_failed`), but "chunk" is the squashfs chunk, not
   every chunk. The round-41 counter already treats a file outside the root as another namespace (self-test line ~2750), so
   "no extra regular file" is satisfied by root scoping.
3. **F3 — symlink targets are not stable and must not be compared.** unblob rewrites targets: 281/282 of the unpublished
   symlinks have a `link_target` different from the oracle detail (235/236 absolute -> relative, e.g. `/bin/supportdata.dpm` ->
   `supportdata.dpm`; also chain-collapsing, `ld-uClibc.so.1` -> `ld-uClibc-1.0.44.so`). Path + kind match is exact (857 = 852
   unpublished + 5 removed on 7530; 860 = 855 + 5 on 7590). Round-41 `unpublished` projection holds `link_target`; any port that
   compares it to the oracle table would be red on genuine data.
4. **F4 — run-unique ids in the semantic projection.** Two genuine runs of the same bytes differ in `chunks[].provider_id`
   (`3687040:2` vs `3872179:2`), `derivations[].provider_blob_id`, `files[].path`, `output_directory`, `diagnostics[].report.link`
   (absolute scratch path) and `evidence_id`. After removing those the runs are equal (checked 7530 big vs f20k: files, chunks,
   derivations, coverage, published_bytes identical; gaps identical but for `provider_id`). The rerun projection must exclude them
   (round-41 `PROJECTION_KEYS` includes `chunks` and `extraction_gaps`: verify the port strips `provider_id`/`provider_blob_id`).
5. **F5 — oracle readers agree.** `sqfs-list.py --layout auto` reports `layout: le`, `avm_marker: true`, compression `xz`, and
   its 13366/13358-row regular table equals `unsquashfs -no-xattrs` 4.7.5 extraction (rows, sha256, size: 0 diff) and equals
   `unsquashfs -lls` regular count (13366/13358). Non-regular: 926 dir + 857 symlink (7530), 932 + 860 (7590), root excluded;
   no devices/fifos/sockets. So the oracle-arm check "regular-file count == unsquashfs -lls" holds; note `auto` selects LE
   for these members (the round-41 oracle arm rejected `hsqs`; the port must accept it).
6. `MaliciousSymlinkRemoved`: 5 per carrier, identical in both (see table). Their oracle targets are `libbroadbandcfg.so.1`
   (a link into an absolute `/usr/share/ctlmgr/...` chain) and absolute `/usr/www/cgi-bin/system_status`.

## Chain pins (measured here)

| item | 7530 | 7590 |
|---|---|---|
| image bytes / sha256 | 41,850,880 / `b17fe5cd0bd3faa713dd92513cb3a65c23e61f5f23366c343b78674955d35e9c` (equals the plan's) | 42,393,600 / `267ef427337d2141736ad6ed5d9389722a6a1234dd590bb7d4ebf11a00616c0d` |
| member `./var/tmp/filesystem.image` bytes / sha256 | 34,005,000 / `df6c22ddd009870404375aff606853c9d5171580437b6aae193114d2040c6e56` | 35,835,912 / `05ba6ac992f77076cd72d97ed98ab7612f3cc6969f6bbf736515537a9373c3dc` |
| superblock | `hsqs`, v4.0, xz(4), inodes 15150, `mkfs_time == bytes_used == 34003969` | inodes 15151, `mkfs_time == bytes_used == 35834769` |
| oracle.tsv sha256 (13366 / 13358 rows; saved gz) | `20c62eaa872637d71dace9c6f2baf944751d3e02829f38dbcca9d4da72998758` | `dde2dd3f6a50be762790e68d3a26964e64a2056ad132d70a4609e191e4d5d5d6` |
| nonregular.tsv sha256 | `fd3fb9ad7111a9e7334e2fb1c93df97dabb8070aac1eb02a4100e763305726e6` | `154d6c0995688f230b774f7bb2bfaf1c839fb6f090b1c3748c2ebfce08bf883f` |

Chain commands: `curl -sSfL -o <img> https://download.avm.de/fritzbox/fritzbox-<m>/deutschland/fritz.os/FRITZ.Box_<m>-08.25.image` (exit 0 both,
2026-10-28T~23:31Z); `tar -xOf <img> ./var/tmp/filesystem.image > car-<m>/filesystem.image` (exit 0); `tar -tvf` showed the member as above.
Superblock read with `struct '<IIIIHHHHHHQQ'` at offset 4, matches `unsquashfs -s` (Filesystem size 34003969 / 35834769, xz, 65536 block).

## Run table (REA 6.5.0 via `npx -y rea-agents@6.5.0`, unblob 26.6.4, `REA_UNBLOB_COMMAND=~/.local/bin/unblob`, `sasquatch` 4.5.1 on PATH, cwd and TMPDIR = private scratch dir, output under `.../kaidoku-r50/`)

Argv: `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1 [extra] <carrier> <outdir>`; script `receipts/run1.sh`.
Wall times are with the host loaded by other seats (run-to-run 29-63 s).

| run | extra args | exit | wall ms | envelope sha256 (raw, ungzipped) | result |
|---|---|---|---|---|---|
| 7530 def | none (= round-41 argv) | **1** | 2325 | `ab4436da4dfc1f4a7b025bdf2f4b24354ab71c259cbb676a0a56b294e0ac0d02` | `unreadable_output` / `Staging entry budget exceeded (10000)` |
| 7590 def | none | **1** | 2275 | `12c8604547a344ee9dbe5a88eafa9818087d6d175359a6390a2254001a504e4d` | same |
| 7530 f15k | `--max-output-files 15145` | 1 | 3038 | `c4783a6ff375d76f71cca7288090af758d2bbf3a3e3b540f3be8eb40e2029dcc` | same, budget 15145 |
| 7530 f15147 | `--max-output-files 15147` | 0 | (not timed in table; ~30 s) | not saved | ok |
| 7530 f20k | `--max-output-files 20000` | **0** | 63113 | `a933417628d4ae179a902f835a4a953fe4a9a8577d937752f88a4bc7785092ab` | ok, evidence `ev_cfebb046e227f8fd0ae5c8416cf4a122477f04a1ae0cd9f762a8ca985be03a43` |
| 7590 f20k | `--max-output-files 20000` | **0** | 50008 | `79da88fb276972e1079e7f0c57388c12adc3058bbcdb4678ea6d80a5869f2351` | ok, evidence `ev_b491456336edde9fedf10d202305953f7bd6e5b26af415bb5a01137b633e97f6` |
| 7530 big | `--max-output-files 100000 --max-output-bytes 536870912` | 0 | 40237 | `676cf747d4e13fbf07e6d8c88bdb96666b7f217e42f2c780df1c31c56d59940c` | ok, `ev_b9508405f637ce957e05b23b2cdc36d03bc9d5fa083991bf6f2d6c14fc0964e0` |
| 7590 big | same | 0 | 28710 | `2b99a443bf905c13dad7e05ccd94a79bfd230d3cabce1ec777960136ddc7d1c2` | ok, `ev_3d84d806e527fc96383976f5782b2bbd56c58933c22b7b8ff9d3b2b8f0bb46b5` |

Start times UTC: def 23:34:27/23:34:29, f20k 23:35:14/23:36:17, big 23:33:13/23:33:58 (2026-10-28). Envelopes are 7.2 MB raw, saved gzipped in
`w1/C1DevArmA/receipts/` (`<m>-<tag>.envelope.json.gz`).

## Per-carrier result (identical for f20k and big runs; coverage `partial`)

| field | a7530 | a7590 |
|---|---|---|
| `derivations[]` | 1 edge, handler `squashfs_v4_le`, child `$output/firmware.bin_extract/0-34004992.squashfs_v4_le_extract`, parent range 0+34004992 | 1 edge, `squashfs_v4_le`, `0-35835904.squashfs_v4_le_extract`, 0+35835904 |
| `chunks[]` | squashfs_v4_le 0+34004992 (`extraction_failed false`, encrypted false); handler None 34004992+8 (`extraction_failed false`) | squashfs_v4_le 0+35835904; None 35835904+8 |
| `files[]` total / inside squashfs root / outside | 13367 / 13366 / 1 (`34004992-34005000.unknown`) | 13359 / 13358 / 1 (`35835904-35835912.unknown`) |
| `unsquashfs -lls` regular count / oracle rows | 13366 / 13366 | 13358 / 13358 |
| oracle files missing from publication / extra inside root / sha256-or-size diffs | **0 / 0 / 0** | **0 / 0 / 0** |
| `extraction_gaps[]` | `unpublished-entry` 852, `unknown-chunk-handler` 1, `depth-limited` 1 (854) | `unpublished-entry` 855, `unknown-chunk-handler` 1, `depth-limited` 1 (857) |
| `unpublished_entries` | 852, all `symlink` | 855, all `symlink` |
| `MaliciousSymlinkRemoved` diagnostics | 5 (only diagnostic type): `lib/libbroadbandcfg.so`, `lib/libbroadbandcfg.so.1`, `usr/www/1und1/cgi-bin/system_status`, `usr/www/avm/cgi-bin/system_status`, `usr/www/avme/cgi-bin/system_status` | the same 5 paths |
| oracle symlinks vs REA | 857 = 852 unpublished + 5 removed; path-exact | 860 = 855 + 5; path-exact |
| oracle dirs / non-regular other | 926 dirs; 0 devices/fifo/sockets | 932 dirs; 0 |
| `published_bytes` | 172,089,104 | 189,853,649 |
| subject digest | `df6c22dd...c6e56` = carrier pin | `05ba6ac9...3c3dc` = carrier pin |
| `parameters.output_directory` | contains `/kaidoku-r50/` (scratch run; real runs will be `/fast/scratch/hyaku/kaidoku-r50/...`) | same |

Does each carrier publish every oracle file? **Yes** — a7530: all 13366 at the exact path under the squashfs chunk root with equal sha256/size;
a7590: all 13358. No path differs. The only non-oracle regular file is the out-of-root `.unknown` trailer.

## Not run / limits
- Counter-time rerun determinism over a whole fresh process was checked for 7530 only (big vs f20k; the two differ in parameters, hence evidence id).
- 7590 entry-budget boundary not probed (estimated 15148, 7530 measured 15147).
- No port of the counter or harness was written in this seat; `c1-run.sh` `after` arm needs the `--max-output-files` flag, `/kaidoku-r50/` segment, and (oracle arm) `hsqs` acceptance.
- Tooling installed: none. Scratch `/fast/scratch/hyaku/kaidoku-r50/C1DevArmA` removed at yield; vendor bytes never copied into the lane tree.
