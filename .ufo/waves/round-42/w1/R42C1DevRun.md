# R42C1DevRun — REA 6.5.0 on OpenWrt Kamikaze 7.09 SquashFS v3 (development)

**Verdict: DONE** — hypothesis confirmed in substance; one premise falsified
(`unsquashfs` oracle cannot read these images; they are LZMA-compressed v3), one
sub-claim untestable (no device nodes in either rootfs). Two additional
findings relevant to the C1 freeze are reported below. All runs exited 0 with
`ok: true`.

## Setup (read-only, no installs)

- `unsquashfs` 4.7.5 (`/usr/bin/unsquashfs`), `7z` 26.04 (`/usr/bin/7z`),
  `sasquatch` / `sasquatch-v4be` 4.5.1 (`~/.local/bin`), `unblob` 26.6.4
  (`~/.local/bin/unblob`), REA `rea-agents@6.5.0` via `npx -y`.
- No tools installed or upgraded (operator RULES.md read; nothing needed).
- Scratch `S=/fast/scratch/hyaku/kaidoku-r42/R42C1DevRun`; `TMPDIR` per run.

## Development inputs (both frozen-in-pin below; carved in scratch)

| image | URL | md5 (matches published) | sha256 | bytes |
|---|---|---|---|---|
| x86 squashfs.image | https://archive.openwrt.org/kamikaze/7.09/x86-2.6/openwrt-x86-2.6-squashfs.image | `fd7bb3294050d8bd5ea01f532e144f54` | `a0a4fcf30e0a42fa09d1f6e9577d624ef78e402590f23549389a59e250441c12` | 5 529 092 |
| brcm47xx squashfs.trx | https://archive.openwrt.org/kamikaze/7.09/brcm47xx-2.6/openwrt-brcm47xx-2.6-squashfs.trx | `e7d46481381f8d8879206da84f468211` | `42b0259f62505bd5573ca762fae6ec5799e602e87f9e9d6ce7676aacef5bb446` | 1 904 640 |

Carving (both LE SquashFS 3:0 by `unsquashfs -s`):

- x86: superblock at image offset 4 677 120 (MBR partition 1); carved to EOF →
  `x86-rootfs.squashfs` (851 972 B, sha256 `338962dd…f2c8`). Trailing 65 540 B
  junk after filesystem end (7z: Physical Size 786 432 / Tail Size 65 540).
- trx: superblock at offset 753 664; carved exactly to filesystem size
  (1 061 809 B) → `brcm47xx-rootfs.squashfs` (sha256 `13a4f1b8…c6912`).

The trx full-length carve (TRX header length) is wrong: the filesystem extends
past it; use the `unsquashfs -s` "Filesystem size" (1 061 809).

### Reader picture (important for the oracle requirement)

`unsquashfs` 4.7.5 **cannot read either image**: v3 is assumed gzip, these are
LZMA (OpenWrt-era squashfs-lzma). Exact stderr:

```
gzip uncompress failed with error code -3
read_block: failed to read block @0xbfd46
read_fragment_table: failed to read fragment table block
FATAL ERROR: File system corruption detected
```

`7z` reads both (`Method = LZMA Spec`, `Physical Size` 786 432 / 1 061 809).
`sasquatch` 4.5.1 reads both (fallback chain … `Trying to decompress with
lzma...`). So this development family is not oracle-able by the designated
`unsquashfs` producer; the C1 freeze's two-producer oracle requirement must use
readers that support LZMA v3 (7z works; a lane stdlib reader would need LZMA).

## Oracle ground truth (used for REA comparison)

- `sasquatch -lls` + `sasquatch -no-exit-code -d <root>` extraction →
  tables `oracle-regular.tsv` (relpath, sha256, size) and
  `oracle-nonregular.tsv` (relpath, kind, detail); script
  `artifacts/R42C1DevRun/oracle-build.py`.
- Cross-check with `7z l -slt` (independent, non-sasquatch): entry sets,
  kinds, and regular-file sizes agree 100% on both images (0 mismatch).
- x86: 331 entries = 137 regular + 42 dir + 152 symlink; no devices/fifo/socket.
- trx: 362 entries = 156 regular + 43 dir + 163 symlink; no devices/fifo/socket.

## REA runs (`extract-firmware --format json --full-output --max-depth 1`)

Command per run (cwd = run dir; `TMPDIR` = run dir):
`REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0
extract-firmware --format json --full-output --max-depth 1 <input> <fresh outdir>`
The "without" arm removes `/home/vgpnk/.local/bin` from the child PATH
(sasquatch hidden; npx/node/7z still reachable). Six runs: 3 inputs × 2 arms.
Envelopes archived at `artifacts/R42C1DevRun/envelopes/`, analyzer at
`artifacts/R42C1DevRun/analyze-envelope.py`, summaries at
`artifacts/R42C1DevRun/summaries/`.

| run | input | exit | duration (meta) | handler(s) | chunks | published | oracle regular | missing | extra | hashdiff |
|---|---|---|---|---|---|---|---|---|---|---|
| x86-fs-with | carved x86 fs | 0 | 1344 ms | `squashfs_v3` + (null) | 2 | 138 | 137 | 0 | `firmware.bin_extract/786432-851972.unknown` | 0 |
| x86-fs-without | carved x86 fs | 0 | 1048 ms | `squashfs_v3` (failed) + (null) | 2 | 2 | 137 | all | — | — |
| trx-fs-with | carved trx fs | 0 | 1321 ms | `squashfs_v3` | 1 | 156 | 156 | 0 | 0 | 0 |
| trx-fs-without | carved trx fs | 0 | 1126 ms | `squashfs_v3` (failed) | 1 | 0 | 156 | all | — | — |
| trx-img-with | whole published TRX | 0 | 1199 ms | `trx_v1` | 1 | 3 (part0/1/2) | 156 | all | — | — |
| trx-img-without | whole published TRX | 0 | 1209 ms | `trx_v1` | 1 | 3 | 156 | all | — | — |

### Gap-kind histogram (with `dependencies`)

- trx-fs-with: `unpublished-entry` 163 (deps `[]`), `depth-limited` 1 (deps
  `[]`, continuation `3b54e297…`; instruction: "Rerun extract_firmware with a
  higher max_depth (up to 10) …").
- x86-fs-with: `unpublished-entry` 152, `depth-limited` 1, `unknown-chunk-handler`
  1 (deps `[]`, provider `2197969:2`, range 786432+65540 — the trailing junk).
- x86-fs-without / trx-fs-without: `missing-extractor-dependency` 1 with
  **`dependencies: ["sasquatch"]`** (handler `squashfs_v3`, range = whole fs);
  x86 additionally `unknown-chunk-handler` 1. Diagnostics:
  `ExtractorDependencyNotFoundReport` (severity ERROR, dependencies
  `["sasquatch"]`), entry_path null.
- trx-img-with / trx-img-without: `depth-limited` 1 only; `trx_v1` extractor
  does not need sasquatch (identical both arms).

### Diagnostics kinds

Only `ExtractorDependencyNotFoundReport` (the two without-arms). **Zero**
`MaliciousSymlinkRemoved` on any run — see symlink dispositions below.

### Symlink / special dispositions

- All 152 (x86) / 163 (trx) oracle symlinks → exactly one `unpublished-entry`
  gap each, kind `symlink`, `link_target` preserved verbatim. Counts match the
  oracle exactly; no symlink published as a file, none removed.
- This includes escaping/absolute targets: `etc/mtab -> /proc/mounts`,
  `etc/rc.d/S10boot -> /etc/init.d/boot`, etc. None produced a
  `MaliciousSymlinkRemoved` diagnostic on this REA version with these images.
  (Round-41 V4 showed 4 such removals; behavior is image/run dependent.)
- Directories are invisible: 0 dir entries in `files`, 0 in
  `unpublished_entries`.
- Devices: neither rootfs contains any device node, so "keeps devices
  invisible" was not exercisable here (nothing to hide). Note for C1 carriers:
  a v3 carrier with devices is needed to exercise that clause.

### Depth-limited fields

`depth_limited_paths` = exactly the chunk extract root, one entry:
- x86-fs-with: `$output/firmware.bin_extract/0-786432.squashfs_v3_extract`
- trx-fs-with / trx-img-with / trx-img-without: `$output/firmware.bin_extract`

For the whole-TRX input, the container chunk consumes the depth budget: the
inner SquashFS is never reached (only `part0/1/2` published), and no
`missing-extractor-dependency` appears even without sasquatch because the
squashfs chunk is never discovered at max-depth 1. **Implication for C1
carrier methodology:** feeding a wrapped image (TRX/nested) to `--max-depth 1`
does not publish the rootfs; carriers must be freeze as carved rootfs bytes (or
run at a depth that reaches the fs).

### Exact published path prefix (extract root)

- trx-fs-with: `$output/firmware.bin_extract/` — i.e. under the REA output
  directory, a `firmware.bin_extract` directory (REA stages the input as
  `firmware.bin`); files publish at `…/firmware.bin_extract/<relpath>`.
- x86-fs-with: `$output/firmware.bin_extract/0-786432.squashfs_v3_extract/`
  (per-chunk subdirectory when more than one chunk is detected).

### Subject / digest

`subject.digest.sha256` equals the input sha256 on every run (e.g.
`13a4f1b8…` for the trx fs). Note: `evidence_id` is null at the envelope top
level in these `--full-output` envelopes (round-41 `after.json` carried it;
verify where it lives in the frozen-format receipt before relying on it).

## Hypothesis check

1. "publishes every regular file the `unsquashfs` oracle lists" — **premise
   falsified** (unsquashfs cannot read LZMA v3); with the sasquatch+7z ground
   truth substituted, confirmed for the exact carve (156/156) and for x86
   (137/137) with one extra file from trailing junk (below).
2. "one `unpublished-entry` gap per in-tree symlink/special" — **confirmed**
   (152/152, 163/163; no other specials present).
3. "one `depth-limited` gap" — **confirmed** (exactly one per fs run, plus one
   for the container runs).
4. "keeps devices invisible" — **not exercisable** (no devices); directories
   invisible confirmed.
5. "removes escaping symlinks with `MaliciousSymlinkRemoved`" — **not
   observed**: with sasquatch on PATH, zero such diagnostics; absolute-target
   symlinks are retained as `unpublished-entry`.
6. Additional facts: exit 0 ok:true on all six runs; chunk handler name
   `squashfs_v3` (family `squashfs_v3*`); missing-extractor-dependency gap
   carries `dependencies: ["sasquatch"]` (matches C2 draft step 3 input).

## C1-freeze-relevant observations (dev evidence only)

- Feeding a padded capture (fs + trailing junk) yields an extra published file
  `firmware.bin_extract/<off>-<end>.unknown` and an `unknown-chunk-handler`
  gap. The exact-length carve avoids both. Carriers should be pinned as exact
  chunks, or the counter/claim must tolerate the `.unknown` artifact.
- Carving must use the filesystem size from `unsquashfs -s`, not a container
  header length (TRX length field is shorter than the fs end).
- The `squashfs_v3` handler + sasquatch handle these LZMA v3 images
  (sasquatch falls back to lzma); `unsquashfs` does not, so oracle pairs for
  such carriers need an LZMA-capable non-sasquatch reader (7z works).
- The draft's `squashfs_v3*` handler naming is satisfied by the observed
  `squashfs_v3` ("the one frozen per carrier" — handler base name carries no
  endianness suffix for LE).

## Evidence files

- `artifacts/R42C1DevRun/envelopes/{x86-fs-with,x86-fs-without,trx-fs-with,
  trx-fs-without,trx-img-with,trx-img-without}.json` — full envelopes (< 5 MB).
- `artifacts/R42C1DevRun/oracle/{x86,trx}/*.tsv` — oracle tables + 7z lists.
- `artifacts/R42C1DevRun/summaries/*` — analyzer reports per run.
- `artifacts/R42C1DevRun/inputs.json` — pins, readers, run facts.
- Scripts: `artifacts/R42C1DevRun/oracle-build.py`, `analyze-envelope.py`.

No tools installed; no VCS mutation; all lane writes confined to the two paths
above plus this report.
