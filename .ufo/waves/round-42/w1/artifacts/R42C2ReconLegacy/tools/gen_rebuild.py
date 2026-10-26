import json
ART='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy'
m=json.load(open(ART+'/manifest.json'))
E=m['entries']
head = """# R42C2ReconLegacy — reproduction

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
TMPDIR=$S REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \\
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \\
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
"""
rows=[]
for e in E:
    i=e['input']
    if i['kind']=='derived' and i['name'] not in [r[0] for r in rows]:
        rows.append((i['name'],i.get('parent'),i.get('recipe'),i.get('sha256')))
for name,parent,recipe,sha in sorted(rows):
    head += '| `%s` | `%s` | %s | `%s` |\n' % (name,parent,recipe,sha)
head += """
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
"""
for e in E:
    if not e['envelope']['copied']:
        head += '| `%s` | `%s` | `%s` | %d |\n' % (e['run'], e['input']['name'], e['input']['sha256'], e['envelope']['bytes'])
head += """
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
"""
open(ART+'/REBUILD.md','w').write(head)
print('wrote', len(head), 'rows', len(rows))
