# C1Frontier — round 49 wave 1

**Verdict: the eight sasquatch/SquashFS items below stay Frontier after a v1/v2 promotion. Do not freeze the frontier note as written.** The draft note supersedes only the round-42 v1/v2 clause, so the round-44 sentence "SquashFS v1/v2 remain Frontier" would still be on the page. The counter's `frontier_note` binding does not notice. One upstream "broadcom" input is standard gzip v3, not `squashfs_v3_broadcom`.

Axes this seat walked: coverage (what leaves Frontier), depth (the next fixture, not a new family name), calibration (the note the counter will accept vs the note the sources require).

No extraction was run. No tool was installed. Scratch removed after the listings below were copied.

## What stays Frontier

Sources, read at base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9` (working tree, not a data run):

- `PROVINCE.md` round-44 frontier note (line 430) and round-42 note (line 416). Round 36–41 notes are older and already superseded for standard LE v4, standard BE v4, AVM-BE, and LZMA v3.
- `corpus/README.md` `## Frontier` line 275 (round 44) and line 269 (round 42).
- Plan disclosed limits, `draft/plans/round-49-claims.md` lines 111–112.
- Draft landing note, `.ufo/waves/round-49/w1/artifacts/R49C1Doc/block-b-province-frontier-note.md`.

After `squashfs_v1` and `squashfs_v2` move to Core, these eight remain. Round 43's separate sentence (published sasquatch packages; vendor-mangled images, `PROVINCE.md` lines 418–422) is not one of the eight and this promotion does not touch it.

| # | Still Frontier | Cheapest next probe | Where it was opened | Bytes |
|---|---|---|---|---|
| 1 | `squashfs_v2_nonstandard` | `corpus/evidence/round-42/c2/fixtures/v2ns-le--squashfs_v2.0_le.bin` | upstream `squashfs_v2_nonstandard/little_endian/__input__/squashfs_v2.0_le.bin`; host copy matches the LFS oid | 4096; magic `zlqs`; sha256 `f25cf3ea531de5c19eb1949eb351e1bb6ee1b91d8f211598e6c4fb695de9e24a` |
| 2 | `squashfs_v3_broadcom` | same dir, `v3bc-le--squashfs_v3_le.bin` | upstream `squashfs_v3_broadcom/little_endian/__input__/squashfs_v3_le.bin` | 4096; magic `shsq`; sha256 `6baad4387dd51c8010de694420a35b6709706a268f7ba9e96e6417fb969f37d3` |
| 3 | `squashfs_v3_nonstandard` | same dir, `v3ns-le--squashfs_v3_le.bin` | upstream `squashfs_v3_nonstandard/little_endian/__input__/squashfs_v3_le.bin` | 4096; magic `zlqs`; sha256 `3bce6ae378319fd2ac08c73ede9b3890a6d0f78c16392f09117cc3ffd70d1acb` |
| 4 | gzip v3 | same dir, `v3-le--squashfs_v3_le.bin` | upstream `squashfs_v3/little_endian/__input__/squashfs_v3_le.bin` | 4096; magic `hsqs`; zlib `78 da` at offset 134; sha256 `0161351caec8e9da6e3e5ac7b046fd11d832efb18eb09e33011e6d19d50cd1f7` |
| 5 | v4 Broadcom (`squashfs_v4_broadcom`) | upstream `squashfs_v4_broadcom/__input__/squashfs_v4_be.nopad.bin` | git tree + LFS pointer; not committed in the lane | LFS size 307; oid `46f7c57770f62692fdc22ad8ed65739242f43aafa5e62a4be075ed899e21e75f`. Magic not opened |
| 6 | LE AVM (`hsqs` + AVM marker) | FRITZ!Box 6590 Cable 07.57 member `./var/remote/var/tmp/x86/filesystem.image` | not under the unblob squashfs tree. Recorded in `R40C1VendorScout` `candidates.tsv` | 27 750 408; magic `hsqs`; marker YES; member sha256 `57552a6dd81b6a43032b761bfbd10090442dbbcce88609bdb731af1242932786`. Image sha256 `0c539499044a807c2dfa3ffdf5eafe6016096912fa6e13374f48afa46cd0abae`. Bytes not on disk |
| 7 | AVM kernels | same image, member `./var/remote/var/tmp/kernel.image` | not in the unblob squashfs tree. Named in `.ufo/waves/round-40/w1/R40C1ReconWrap.md` lines 33 and 130 | 1 932 808; magic `12 91 ed fe` (0xfeed9112). Bytes not on disk |
| 8 | nested sub-images below depth 1 | FRITZ!Box 7430 07.31 nested `filesystem_core.squashfs` inside `./var/tmp/filesystem.image` | not in the unblob squashfs tree. `R40C1VendorScout.md` finding 3 | `bytes_used` 25 194 540; scout says `sqsh`, marker YES, 7524 inodes. Bytes not on disk |

Host readers present, not run on these fixtures: `/usr/bin/unsquashfs` 4.7.5, `/usr/bin/7z` 26.04, `/home/vgpnk/.local/bin/sasquatch` 4.5.1, `/home/vgpnk/.local/bin/sasquatch-v4be` 4.5.1, `/home/vgpnk/.local/bin/unblob` 26.6.4. `command -v` exit 0 for each at 2026-10-28T21:17:27Z. `unsquashfs -version` and `sasquatch -v` print the version and exit 1; that is the binary's own status, observed 2026-10-28T21:16:08Z.

### Why that probe, and the trap

1. v2 nonstandard. The 4096-byte LE file is the magic-only variant of the v2.0 body this round is promoting (`zlqs` vs `hsqs`). Upstream v2.1 is also 4096 (LFS oid `6bae8791233a1db66163537175f253f29d1d108ea2bd172a7ac2f2484867fc9d`, fetched 2026-10-28T21:16:06Z) and adds a version change, so it is the worse probe. Round 44 already recorded `unsquashfs` exit 1 and `7z` exit 2 on both committed v2ns files. This seat did not re-run them. `sasquatch` is the same extractor unblob calls, so it is not an independent oracle.

2. v3 Broadcom. The confirmed-magic file is the LE 4096-byte `shsq` image above. A 320-byte LE nopad exists upstream (LFS oid `e763240ca30dae3e630a5313a5d3a22923a9bb019d62a6e8c2888ee487d01e58`, same fetch, magic not opened). **Do not use** `squashfs_v3_broadcom/big_endian/__input__/squashfs_v3_be.bin`. Its git blob `77c08f6161df0976b132374e754a38c0e9b42b9a` is the same blob as `squashfs_v3/big_endian/__input__/squashfs_v3_be.bin`. The LFS oid is `4e9493d9c6f868005dea8f11992129c3399e0bcb8f3a966c750cb925989ca97c`, which is the host file `v3-be--squashfs_v3_be.bin`, magic `sqsh`, zlib at offset 134. That is standard gzip v3, already item 4, not a Broadcom body. The BE nopad is a different object (oid `5baee74f14d4b5b80a2a09ce1d5cb90c1fced592fd971edb854a9df130b42282`, 320 B); its magic was not opened. `tools/round-42/fixtures.json` `duplicate_bytes` already says `v3bc-be` `same_bytes_as` `v3-be`. The lane has no `v3bc-be--*` file.

3. v3 nonstandard. Host file magic `zlqs` (BE twin `sqlz`, sha256 `01b2792bd5b5fb3455282cb84351f2e0c7e67de9b861de5a3503cdc7710c3661`). Smaller upstream nopad is 320 B (LE oid `8c7ed2e81dd0f50539cfecb187a73788bbb3e2bc79f6bb9a3073d78cb7fbf50a`); magic not opened. Round 44 recorded both external readers refusing the committed files. Not re-run.

4. gzip v3. The host `v3-le` / `v3-be` files are the ones `tools/round-42/fixtures.json` labels `compression: gzip`. The zlib marker is at offset 134 in both. They are not the round-42 Core carriers (those were published LZMA rootfs images under `squashfs_v3` / `squashfs_v3_ddwrt`). The adaptive fixtures are the other compression: `v3adapt-le--squashfs_v3_le.lzma.bin` has no `78 da` / `78 9c` / `1f 8b` marker. Upstream nopads are 320 B (`squashfs_v3.le.nopad.bin` oid `314d4bbe07b83f491e9987d7db39d8560945b2ae273ed23ead7e9d92250deb3c`); marker not opened. The committed 4096-byte file is the probe because its magic and marker were opened and it is already pinned.

5. v4 Broadcom. Nothing in `corpus/evidence/round-42/c2/fixtures/` is v4 Broadcom. The git tree has four inputs. Smallest is the BE nopad, 307 B. LE nopad is 308 B, oid `8ef3815d87a50c32ed5c540003ecaa4e383604708efc2916ad2ba8644b9e8487`. The padded pair is 4096 B each (LE oid `b7963fba31962c614e439f4f7a43a1eddec43afe1bdb1ffb059e72f8a15bd10b`). Pointer blobs differ from `squashfs_v4_be/__input__/squashfs_v4.nopad.bin` (git blob `9f2fc996a7cc3fc44504fd5038430b588c7cdcac`) and from `squashfs_v4_le/__input__/squashfs_v4.nopad.bin` (git blob `163dc82db8859a1eb252142004a00fe843b6bf32`), so these are not the standard v4 nopads. Content magic was not opened (LFS pointer only).

6. LE AVM. The recursive squashfs test tree (380 entries) has no path containing `avm`, `kernel`, `filesystem_core`, `fritz`, or `hsqs`. `tools/round-41/gen-squashfs.py` lines 4–15: `le` emits `hsqs` in the standard layout; `avm` and `avm-genuine` emit `sqsh`. There is no writer mode for `hsqs` plus the AVM marker. Among `candidates.tsv` rows with magic `hsqs` and `marker=YES`, the smallest member is the 6590 x86 filesystem (27 750 408 B). The other `hsqs` members (6490 x86, 7581, 7582, 7590) are larger. `carve.sh` in that artifact dir is the existing carve (`tar -xOf` of that member). The round-40 scratch path was checked and is absent. Standard `squashfs_v4_le` fixtures are the wrong probe: they are Core since round 36 and are not the AVM layout.

7. AVM kernels. Same listing absence. The 6590 main kernel member is smaller than `./var/remote/var/tmp/x86/kernel.image` (3 552 264 B, gzip at offset 14958, same recon report). Round 40 already ran REA on the main kernel and recorded `coverage: complete`, 0 files, 0 chunks, 0 gaps (report line 130). This seat did not re-run it. That result was a development image, not a frozen carrier, so the item is still Frontier.

8. Nested below depth 1. No `filesystem_core` name in the unblob squashfs tree. Round 41 V4's nested file was pre-carved to its own `bytes_used` (32 720 860) and scored as a depth-1 carrier, so that carve is Core, not this item. Round 41 V3 (5490, member `bytes_used` 30 233 394, 8 regular files published) left its nested file unopened; the entry says so and does not give that file's size. The smallest nested body with a recorded size is the 7430 `filesystem_core.squashfs` (`bytes_used` 25 194 540). Image URL `https://download.avm.de/fritzbox/fritzbox-7430/other/fritz.os/FRITZ.Box_7430-07.31.image`, image sha256 `3dd6940c3aea429944d41508cc6c5a4e3573dae8ad9bf92e293e5bf945a6ecf4`. Bytes not on disk.

## Draft defects (do not freeze as-is)

1. **The frontier note does not supersede the sentence that still says v1/v2 are Frontier.** `block-b-province-frontier-note.md` says it supersedes the round-42 clause and nothing else. `PROVINCE.md:430` and `corpus/README.md:275` still say SquashFS v1/v2 remain Frontier. No draft edits `corpus/README.md` `## Frontier`. After the drafted landing, both sentences would be true on the page.

2. **`frontier_note` does not score that.** `draft/tools/round-49/c1-counter.py` lines 2161–2163 set the binding if any line contains `Round-49 frontier note`, the stem `2026-10-28-r49-squashfs-v1v2-core`, and `SQFS12_TEXT_RE` (lines 327–328). The docstring (lines 30–31 and 185–186) says the note supersedes the SquashFS v1/v2 Frontier text. The code does not look for "superseded", does not require the eight residual names, and does not reject a surviving round-44 sentence. Checked 2026-10-28T21:15:37Z with that same predicate, exit 0:

   | line | hit |
   |---|---|
   | draft block-b (lists the eight) | true |
   | `_province()` green fixture, lines 2754–2755, which names no residual | true |
   | forgery `Round-49 frontier note 2026-10-28-r49-squashfs-v1v2-core squashfs v1` | true |
   | round-44 "SquashFS v1/v2 remain Frontier" without the mark and the stem | false |

   A landing that copies the green fixture, or the forgery, scores `frontier_note` true and drops the residual list. The round-44 sentence can stay beside it.

3. **Coverage-map draft is labeled round 44.** `block-c-readme-coverage-map-row.md` begins `| SquashFS v1/v2 through REA (round 44) |` and then cites the r49 stem. `coverage_map_row` (counter lines 2186–2189) is true if the stem appears in any `|` row under `## Coverage map`. The round number is not checked. The existing README row for that label cites `2026-10-28-r44-squashfs-v1v2-core` and says measured, not promoted (README line 104).

## Commands

UTC times are the clock printed around the command. Stdout sha256 is of the saved response body when one was kept. A check with no saved stdout says so. Extractions: not run.

| UTC | exit | command | stdout sha256 |
|---|---|---|---|
| 2026-10-28T21:10:39Z | 0 | `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` | not recorded (human status; `/fast/scratch/hyaku` 39% used, 497.5G free) |
| 2026-10-28T21:11:51Z | 0 | `curl -fsSL -o contents.json` GitHub contents `tests/integration/filesystem/squashfs?ref=26.6.4` | `be3180fc1c5221b7e91b3e442d10109348f3a50f6b7cbdfe7d915b6353542e00` |
| 2026-10-28T21:11:51Z | 0 | `curl -fsSL` tag `refs/tags/26.6.4` | `4801191bdda9b8acd9b179b24671edb19e797ed29deff645f03ec2a6040f1873` |
| 2026-10-28T21:11:51Z | 22 | `curl -fsSL` tag `refs/tags/v26.6.4` (HTTP 404) | no body kept |
| 2026-10-28T21:13:16Z | 0 | GitHub git trees, recursive, eight handler dirs (script; each HTTP 200, `truncated=false`) | per-tree sha256 in the script stdout at that time; bodies under scratch, not all copied |
| 2026-10-28T21:13:33Z | 0 | `curl -fsSL -o fs-parent.json` contents `tests/integration/filesystem?ref=26.6.4` | `58719fb967a94ea73e8a3cb55e91dae1f0f1624c0353877a1669924959e42b9d` |
| 2026-10-28T21:15:35Z | 0 | `curl -fsSL -o squashfs-tree.json` git tree `d9915e5b24f9158463ec938aa6afedce54abee06?recursive=1` | `a9428eb732aef70ea83ccc355dc37fbd9497720d252bb726a12ab6b8f6873442` |
| 2026-10-28T21:15:35Z | 0 | parse of that tree: `truncated false`, 380 entries, 57 `*.bin` inputs, 0 name hits for avm/kernel/filesystem_core/fritz/hsqs | not recorded separately |
| 2026-10-28T21:15:33Z | 0 | `sha256sum` of the eight host fixtures named above, plus magic of every file in `corpus/evidence/round-42/c2/fixtures/` | fixture sha256s are the stdout; the combined stdout sha256 was not recorded |
| 2026-10-28T21:15:33Z | 0 | LFS pointer fetch (raw git blobs) for v4 broadcom ×4, v3 LE, v3bc LE, v2ns LE 2.0, and the shared v3/v3bc BE blob | pointer-file sha256s below; HTTP 200 |
| 2026-10-28T21:16:06Z | 0 | LFS pointer fetch for the six nopads and v2ns LE 2.1 | stdout sha256 not recorded; oid and size lines were read from that run. Re-fetch at 2026-10-28T21:17:27Z returned HTTP 403, so those seven pointer files are not in `listings/` |
| 2026-10-28T21:15:37Z | 0 | four-line `frontier_note` predicate check | not recorded |
| 2026-10-28T21:16:43Z | 0 | zlib/gzip/lzma marker scan of six host fixtures | not recorded; hits are in the table above |
| 2026-10-28T21:16:08Z | 0 | `unblob --version` → `26.6.4` | not recorded |
| 2026-10-28T21:16:08Z | 1 | `unsquashfs -version` → `unsquashfs version 4.7.5 (2026/03/01)` | not recorded |
| 2026-10-28T21:16:08Z | 0 | `7z \| head -2` → `7-Zip 26.04 (x64)` | pipeline, not a clean stdout hash |
| 2026-10-28T21:16:08Z | 1 | `sasquatch -v` and `sasquatch-v4be -v` → `unsquashfs version 4.5.1 (2022/03/17)` | not recorded |
| 2026-10-28T21:17:27Z | 0 | `sha256sum` of the copied listing files | see `listings/` table |
| 2026-10-28T21:15:33Z | 0 (test `[ -e ]` printed ABSENT) | round-40 scratch paths for the 6590 LE member and kernel | not a hash; both ABSENT |

Tag object: `refs/tags/26.6.4` → commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`. There is no tag `v26.6.4`.

Top-level handler directories in `contents.json` (11): `squashfs_v1`, `squashfs_v2`, `squashfs_v2_nonstandard`, `squashfs_v3`, `squashfs_v3_adaptive`, `squashfs_v3_broadcom`, `squashfs_v3_ddwrt`, `squashfs_v3_nonstandard`, `squashfs_v4_be`, `squashfs_v4_broadcom`, `squashfs_v4_le`. No AVM, kernel, or filesystem_core directory.

Saved listing bodies (sha256 of the file in this seat's `listings/`):

| file | sha256 |
|---|---|
| `listings/contents.json` | `be3180fc1c5221b7e91b3e442d10109348f3a50f6b7cbdfe7d915b6353542e00` |
| `listings/tag.json` | `4801191bdda9b8acd9b179b24671edb19e797ed29deff645f03ec2a6040f1873` |
| `listings/fs-parent.json` | `58719fb967a94ea73e8a3cb55e91dae1f0f1624c0353877a1669924959e42b9d` |
| `listings/squashfs-tree.json` | `a9428eb732aef70ea83ccc355dc37fbd9497720d252bb726a12ab6b8f6873442` |
| `listings/lfs-pointers/v2ns_le_2_0.txt` | `25fd9b79877bc05c4248d4c05ca051fd379e91e5c9cc1e26394a5c8259923894` |
| `listings/lfs-pointers/v3_le.txt` | `079d7c61dd030a5e8837fdf23a3527710e5a9be64669196ee74940865d82f1a2` |
| `listings/lfs-pointers/v3_be_and_v3bc_be_same.txt` | `1822017b705bd9e78bb444f9a8263e653242e86f11e830a174275cb53f455150` |
| `listings/lfs-pointers/v3bc_le.txt` | `3004abefe139e1f58aa67ed1202342957ce719b44d440f101795ff24c7e66468` |
| `listings/lfs-pointers/v4bc_be.txt` | `bc01f529bfa65cb358669e203acc0acdd24b0bfa86bfbacb89500eb75a0145e2` |
| `listings/lfs-pointers/v4bc_be_nopad.txt` | `e00ee833a7a2ca84f89844b6b3ba05a8193a4a117a32c1cd92f3918e5126060c` |
| `listings/lfs-pointers/v4bc_le.txt` | `497f6bea6d2a5b2a19b41cc0c5d87b5ef16afa0e7f588ba9f94d2f490a4dd87a` |
| `listings/lfs-pointers/v4bc_le_nopad.txt` | `02c8384adc5a052b40bb18d7465d971313b74abab5d7f8523d8e509f7e08694c` |

`candidates.tsv` sha256 `38949d2ffe25001b88b1d4d2a419eea2349e30f01271267a15492541a243ceec`. `carve.sh` sha256 `e357746b93a9986e1cd73e740c7eaad48035adbfa12fdc4eca744a6358c790bd`.

Per-directory tree fetches at 2026-10-28T21:13:16Z (HTTP 200, not copied; stdout of that script):

| dir | response sha256 | entries |
|---|---|---|
| `squashfs_v2_nonstandard` | `b882036c4311d623a98c9d1f4251369b5856f143b68953845ee591acc6120072` | 30 |
| `squashfs_v3` | `ec5f31a48199627954ec9aedbe9311abf48604275d862b81ee2816a8e2d310a1` | 50 |
| `squashfs_v3_adaptive` | `eb614581fbc7b5ca144c56a5ef848fad6ff01fc68852760ff2bb7b499bda166c` | 10 |
| `squashfs_v3_broadcom` | `4ee3f8a797175651b18e37a109c8b299cb356a6b128bcec0321bb721b179b120` | 50 |
| `squashfs_v3_nonstandard` | `e94cc1bfca86af91505c5b98a64ff41fab935aa022a48822f4f7156f75521cba` | 50 |
| `squashfs_v4_broadcom` | `872de2bb0f3502a7da4649739e30b1d75c58fff2cd0c769152446e3d11a98c1c` | 24 |
| `squashfs_v4_le` | `21d1beb12c76ee2fde6a0db47670b06a27a49da76195178ac56360980b783e74` | 37 |
| `squashfs_v4_be` | `6c57509f8876085a643b5067408c323c7d5858fd1bc7b2a5876a524027d237cc` | 26 |
