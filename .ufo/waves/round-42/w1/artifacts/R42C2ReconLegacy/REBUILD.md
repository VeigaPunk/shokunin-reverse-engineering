# R42C2ReconLegacy — reproduction

Every envelope in `manifest.json` was produced by one REA 6.5.0 `extract-firmware`
run. Nothing here was installed, moved or removed: the toolchain is the pinned one.
`tools/run1.sh` is the fixture-matrix driver; its `S=` line is the seat scratch root and
must be repointed (it also honours `TMPDIR`). The arm drivers are the two functions
transcribed below.

## Pins measured on this host

| tool | pin |
| --- | --- |
| REA | `rea-agents@6.5.0` (npx; package root `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`) |
| unblob | 26.6.4, commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`, binary `~/.local/bin/unblob` sha256 `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09` |
| sasquatch | 4.5.1 (`sasquatch -version` prints `unsquashfs version 4.5.1 (2022/03/17)`) |
| sasquatch-v4be | 4.5.1 (same version line) |
| unsquashfs (reader only) | 4.7.5 (2026/03/01) |
| 7-Zip (reader only) | 26.04 |
| python3 | 3.14.8 |

## Envelope command (after arm)

```
S=<scratch>; mkdir -p "$S/runs/<run>"; cd "$S/runs/<run>"
TMPDIR=$S REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
  [--max-depth 1] <input> "$S/runs/<run>/out" > envelope.json 2> rea.err
```

`--max-depth 1` is passed exactly for the runs whose manifest `max_depth` is 1; every
other run used REA's default (3). `out/` must not pre-exist (REA refuses an existing
output directory). unblob writes `unblob.log` into the cwd, hence the per-run cwd.

## PATH arms (dependency rows)

Both arms keep `REA_UNBLOB_COMMAND` absolute and drop `$HOME/.local/bin` from the child PATH:

```
STRIPPED=$(python3 -c 'import os;print(":".join(p for p in os.environ["PATH"].split(":") if p.rstrip("/")!=os.path.expanduser("~/.local/bin")))')
# A1: neither sasquatch nor sasquatch-v4be reachable
env -u LD_LIBRARY_PATH PATH="$STRIPPED" REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 ...
# A2: only plain sasquatch reachable (scratch symlink; sasquatch-v4be absent)
mkdir -p "$S/bin" && ln -sfn "$HOME/.local/bin/sasquatch" "$S/bin/sasquatch"
env -u LD_LIBRARY_PATH PATH="$S/bin:$STRIPPED" REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 ...
```

## Inputs

### unblob 26.6.4 fixture (MIT) — 43 v1–v3 files + 3 v4 files

`https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/<family>/<endianness>/__input__/<file>`
(the `squashfs_v3_adaptive` family has no `<endianness>` directory). Per-file URL and
sha256: `fixtures.tsv`. The fixtures are not copied into the lane; `fixtures.tsv` is the pin.

### OpenWrt Kamikaze 7.09 images (DESIGNATED DEVELOPMENT — never a C1 carrier)

| file | url | sha256 | bytes |
| --- | --- | --- | --- |
| `openwrt-atheros-2.6-root.squashfs` | `https://archive.openwrt.org/kamikaze/7.09/atheros-2.6/openwrt-atheros-2.6-root.squashfs` | `70d7c4c7ce6794a627bdfb38a1efae45363888a194caef260f389be5241aff58` | 1179648 |
| `openwrt-wrt54gs-2.6-squashfs.bin` (TRX) | `https://archive.openwrt.org/kamikaze/7.09/brcm47xx-2.6/openwrt-wrt54gs-2.6-squashfs.bin` | `54931105da018d9589d64d37142f3c3bd4f48059132e89f827ea573205e8dba1` | 1904672 |

Both are squashfs 3.0 with the OpenWrt LZMA patch (`sasquatch` logs
`Detected lzma-adaptive compression`). Three other 7.09 files were downloaded only to
probe for a gzip v3 image and were not used in a run: `openwrt-wrt300n_v1-2.6-squashfs.bin`
sha256 `22b19ffb...`, `openwrt-wrtsl54gs-2.6-squashfs.bin` sha256 `618f94e0...`,
`openwrt-x86-2.6-squashfs.image` sha256 `a0a4fcf3...` (no squashfs superblock).
No third-party firmware image and nothing extracted from one is copied into the lane.

### Derived inputs — every byte is a pure function of a pinned input

`v3tool.py` (in `tools/`) parses the packed SquashFS v3 superblock (119 bytes: offsets are
`mkfs_time` 39, `bytes_used` 63, `inode_table_start` 87, `directory_table_start` 95,
`fragment_table_start` 103, `lookup_table_start` 111 — verified byte-for-byte against
`unsquashfs -s`) and walks metadata block chains by their 2-byte
`(uncompressed<<15)|length` headers without decompressing.

| derived input | parent | recipe | sha256 |
| --- | --- | --- | --- |
| `C1_v4_then_v3le.bin` | `squashfs_v4.bin + wrt54gs-v3.squashfs` | cat squashfs_v4_le/__input__/squashfs_v4.bin wrt54gs-v3.squashfs | `876529d114cc2df4c06c7e5a2f7d0509ac45f34dd4200cc307f9677888561fbc` |
| `C2_v4_then_v3be.bin` | `squashfs_v4.bin + atheros-v3-trim.squashfs` | cat squashfs_v4_le/__input__/squashfs_v4.bin atheros-v3-trim.squashfs | `a9d3f6bf7362a8be9e610eb6b492adb0c7fa7c8e31b9fb0512fcd50eb97b55ac` |
| `F1_v3_fixture_fragment.bin` | `squashfs_v3.le.nopad.bin` | zero bytes 119..144 (the only data-area block = the single fragment block) | `4d1bceef52b30aaaa50de94d1f0ba19be4858b0d4ea90df11086c57dfdb465bf` |
| `V1_inode_last.bin` | `wrt54gs-v3.squashfs` | v3tool.py --zero inode-last (last inode metadata block 1057701+845+2) | `8a7fd5e80942d9b1fa565f907ae1e4e01dbbeeac85eeb443a337d8b1216eb7dc` |
| `V2_inode_table.bin` | `wrt54gs-v3.squashfs` | v3tool.py --zero inode-table (1055746..1058548) | `38a5d68ad5d02dca8fe56c8d5f60a1d7589ef31462318d8aaa69f7290053232a` |
| `V3_dir_last.bin` | `wrt54gs-v3.squashfs` | v3tool.py --zero dir-last (directory metadata block 1061690+105+2) | `68ed8c664843a95c6caa5a78fc5c30ad2b07f64074fbe143ec88791f360edde7` |
| `V4_data_tail.bin` | `wrt54gs-v3.squashfs` | zero bytes 1055234..1055746 (last 512 B of the data area, just below inode_table_start) | `31e918e67101f31d80656fe2ec63af872d1098fc05bd8b6026115c5e01434047` |
| `V5_data_tail2.bin` | `wrt54gs-v3.squashfs` | zero bytes 989698..990210 (512 B, 65536+512 below inode_table_start) | `a424c6a0ed3f340db639461e5cf3133a38d7706226c57fe53f06b89fbc4bd37b` |
| `V6_frag_index.bin` | `wrt54gs-v3.squashfs` | zero the fragment table index at 1061797 (8 bytes) | `c7b31a34de6e8c49516d28423b1c465233b3081671b3b40cf9acb9f685f15c7d` |
| `Z1_v1_inode_table.bin` | `squashfs_v1.0_le.bin` | zero bytes 71..128 (v1 inode_table_start u32@20 .. directory_table_start u32@24) | `dfcac6c75f6bccf68ce45027bad797bcc65828dbd573225b61dfd387c9a597da` |
| `Z2_v2_inode_table.bin` | `squashfs_v2.0_le.bin` | zero bytes 88..136 (v2 inode_table_start u32@20 .. directory_table_start u32@24) | `6b9fabeec73dda69bd9e463264f9ed8c43575ae43172b3687d4a06a4048eccf6` |
| `Z3_v3ddwrt_inode_table.bin` | `squashfs_v3.be.nopad.bin (ddwrt)` | zero bytes 144..203 (v3 inode table chain; BE image) | `839c17a83b706589f1b634d0e19fbc6950c3028072e3952c1c74a290ad2150c8` |
| `tar_v3_le.tar` | `a1` | tar -cf tar_v3_le.tar -C fx/squashfs_v3 squashfs_v3_le.bin | `bdf54f2d3377a10528f37d8c37c513785bb5ffc16454b9857917fb4caaf8bce9` |
| `v3le_tail.bin` | `a1` | cat squashfs_v3.le.4kpad.bin + 256 x 0xAA (uniform fill: claimed by unblob padding handler) | `3c494904547280e1eb1fe45910d43b472a408b1e84fc274e64da7c06fa20cd4a` |
| `v3le_tail_pattern.bin` | `a1` | cat squashfs_v3.le.4kpad.bin + 256 B of "ABCD" repeated (unknown-chunk-handler) | `6cb33fd1f27baffe00a4228794ba23487206d08c50d5eb3c2f66e93e091df547` |
| `v3le_tail_random.bin` | `a1` | cat squashfs_v3.le.4kpad.bin + 256 B deterministic non-uniform bytes (unknown-chunk-handler) | `7a34920a9d01039c3940e0607440a354e30371caf253a87335aeda5b90d7b52f` |
| `v3le_tail_text.bin` | `a1` | cat squashfs_v3.le.4kpad.bin + 244 B ASCII text (unknown-chunk-handler) | `a65f7edd47e15c1d30fa063fc96358f4e641bd18fae000861170cfc6aef00e58` |

`wrt54gs-v3.squashfs` is `openwrt-wrt54gs-2.6-squashfs.bin[753696:753696+1061809]`
(753696 = first `hsqs`; 1061809 = its `bytes_used`). `atheros-v3-trim.squashfs` is the
first 999424 bytes of the atheros image = unblob's chunk end
`round_up(bytes_used=995971, 4096)`; the untrimmed 1179648-byte file leaves 180224
unclaimed bytes, which is why it produces an `unknown-chunk-handler` gap.

Zero-file damage uses the level-specific table offsets: v1/v2 `inode_table_start` `u32@20`
to `directory_table_start` `u32@24`; v3 `u64@87` to `u64@95`.

## Envelopes not copied (over the 256 KiB copy cap)

| run | input | input sha256 | bytes |
| --- | --- | --- | --- |
| `a1_trx_d3` | `openwrt-wrt54gs-2.6-squashfs.bin` | `54931105da018d9589d64d37142f3c3bd4f48059132e89f827ea573205e8dba1` | 733413 |
| `atheros_ddefault` | `openwrt-atheros-2.6-root.squashfs` | `70d7c4c7ce6794a627bdfb38a1efae45363888a194caef260f389be5241aff58` | 581445 |
| `base_be` | `atheros-v3-trim.squashfs` | `ea653cfb1e8b9bc48698ca453a79d8cf4c9d82bffe5a27bed98160935d232b0d` | 503127 |
| `base_le` | `wrt54gs-v3.squashfs` | `13a4f1b8f30044185730b92ad46ff39feebf959d554b6b33c742373b737c6912` | 521151 |
| `concat_C1` | `C1_v4_then_v3le.bin` | `876529d114cc2df4c06c7e5a2f7d0509ac45f34dd4200cc307f9677888561fbc` | 614560 |
| `concat_C2` | `C2_v4_then_v3be.bin` | `a9d3f6bf7362a8be9e610eb6b492adb0c7fa7c8e31b9fb0512fcd50eb97b55ac` | 594038 |
| `dmg_V4_data_tail` | `V4_data_tail.bin` | `31e918e67101f31d80656fe2ec63af872d1098fc05bd8b6026115c5e01434047` | 524940 |
| `dmg_V4b_data_tail` | `V4_data_tail.bin` | `31e918e67101f31d80656fe2ec63af872d1098fc05bd8b6026115c5e01434047` | 525097 |
| `dmg_V5_data_tail2` | `V5_data_tail2.bin` | `a424c6a0ed3f340db639461e5cf3133a38d7706226c57fe53f06b89fbc4bd37b` | 520641 |

Those envelopes are reproducible byte-for-byte in projection with the commands above and the
input pin; their `sha256` is in `manifest.json`.

## What an envelope's paths mean

`parameters.path`, `parameters.output_directory`, `normalized_result.files[].path` and
`normalized_result.output_directory` name the (now removed) scratch tree; every
`rea-firmware-*` directory was created by REA under `$S`. The scratch is deleted, so a
byte-identical replay needs the same command but a different scratch path — which
changes `evidence_id` (it hashes `parameters`). Two reruns of the same input in different
directories therefore have the same file/gap projection and different `evidence_id`
(measured: `dmg_V4_data_tail` vs `dmg_V4b_data_tail`).
