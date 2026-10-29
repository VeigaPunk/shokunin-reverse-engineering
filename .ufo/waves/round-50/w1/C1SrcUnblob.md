# C1SrcUnblob — round 50 wave 1 (pre-freeze build): unblob LE v4 source re-open

**Verdict: the LE handler is AVM-blind, and the plan's "no `-be` binary needed" holds. S112 cannot be re-used; a new registry row is needed, and it must not take the id `S150`. Two counter-facing defects are folded into drafts below, one of them a real gap for CTL-C1-3.** Seat: C1SrcUnblob. Base `7c678ae6d97aedb969fd253b52b3d2882ef1e186`. Lane tree not written; drafts and receipts are under `.ufo/waves/round-50/w1/C1SrcUnblob/`.

## 1. Source re-open (opened 2026-10-28 UTC)

| check | command | exit | result |
|---|---|---|---|
| fetch handler (26.6.4) | `curl -sS -o … -w '%{http_code} %{size_download}' https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py` | 0 | HTTP 200, 19,842 B, 590 lines, fetched 2026-10-28T23:31:51Z |
| handler sha256 | `sha256sum` | 0 | `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` (= S108 row) |
| installed copy | `cmp` against `~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py` | 0 | identical |
| tag commit | `curl https://api.github.com/repos/onekey-sec/unblob/git/refs/tags/26.6.4` | 0 | `object.sha` `1fcc7a0a584a70a96c31f5a276c20944d199a089` (response sha256 `4801191b…`, mutable, not cited as evidence) |
| `file_utils.py` (for S122 cross-check) | same method | 0 | HTTP 200, 27,989 B, sha256 `87d4dc9a…` = S122 |
| `is_avm` / `AVM` occurrences | `grep -n -i 'avm\|is_avm'` | 0 | only lines 47-49, all inside the BE branch |

### Quoted lines (exact text, line numbers of the 26.6.4 file)

| # | line | quote (≤25 words) | what it establishes |
|---|---|---|---|
| Q1 | 24 | `class SquashFSExtractor(Extractor):` | one extractor class serves every SquashFS version |
| Q2 | 25 | `EXECUTABLE = "sasquatch"` | default binary is `sasquatch` |
| Q3 | 39-41 | `match endian, self.version:` / `case Endian.BIG, 4:` / `executable = self.V4BE_EXECUTABLE` | only BE with version 4 selects `sasquatch-v4be` |
| Q4 | 47-50 | `# see …AVM-BE-format.txt` / `is_avm = header.bytes_used == header.mkfs_time` / `if not is_avm:` / `commands_args.append("-be")` | the AVM marker test lives only in the BE v4 branch |
| Q5 | 53-54 | `case Endian.LITTLE, _:` / `commands_args.append("-le")` | every little-endian member gets `-le`, any version |
| Q6 | 56-65 | `"-no-exit-code", "-f", "-d", "{outdir}", "{inpath}"` then `extractor = Command(executable, *commands_args)` | the LE argv is `sasquatch -le -no-exit-code -f -d OUT IN` |
| Q7 | 75 | `EXTRACTOR = SquashFSExtractor(3, 0x73_71_73_68)` (in `_SquashFSBase`) | base extractor is version 3; the LE class does not override it |
| Q8 | 454-455 | `class SquashFSv4LEHandler(_SquashFSBase):` / `NAME = "squashfs_v4_le"` | handler name the REA chunk reports |
| Q9 | 463 | `68 73 71 73 [24] 04 00` | LE v4 pattern: `hsqs`, 24 bytes, major 4 (only v4 LE line in the file) |
| Q10 | 473, 483 | `uint32 mkfs_time …;` / `uint64  bytes_used;` | the LE class parses these fields but never tests them |
| Q11 | 527 | `EXTRACTOR = SquashFSExtractor(4, 0x73_71_73_68)` (in `SquashFSv4BEHandler`) | the BE v4 handler is where the version-4 extractor applies |

**Confirmed: the LE handler does not inspect the AVM marker.** The `mkfs_time`/`bytes_used` comparison is only in the BE branch (Q4). The LE class defines no `EXTRACTOR` (grep `EXTRACTOR` shows lines 75, 204, 323, 368, 414, 527, 553 only), so it uses the v3 base and reaches the LITTLE branch. `get_dependencies()` (lines 68-69) returns both `sasquatch` and `sasquatch-v4be` for the class, but a little-endian run only ever executes `sasquatch`.

Broadcom v4 (lines 548-590) uses magics `qshs`/`shsq`, not `hsqs`; the `hsqs` v4 LE pattern is unique to `SquashFSv4LEHandler`.

## 2. Registry (S112 and S108 against the plan's binding)

- **S112 cannot be re-used.** It is opened 2026-10-26, its `teaches` is BE-only (`Name the external sasquatch-v4be dependency as structural for standard BE v4`), and its anchor is `SquashFSExtractor` lines 24-70 quoting the BE branch. The plan's binding requires rows opened 2026-10-28..29. The registry is append-only (round-49 closure), so an in-place re-check that changes `opened`/`teaches` is not allowed. Verdict: S112 stays as it is.
- **S108** is the same URL and the same bytes, but it is opened 2026-10-26 and its anchor (24-26, 48-50, 58-62, 68-69) omits the LE class and LE branch. It also does not satisfy the 2026-10-28 binding.
- **A new row is needed** (draft D1, in `drafts.md`): same URL, opened 2026-10-28, anchor covering lines 25, 40-41, 48, 53-54, 75, 455, 463.
- **Id collision (action for L1).** `corpus/SOURCES.md` ends at `S149`, but `S150` is cited in six lessons and spot-checks (`round-35.md` l.20/34, `round-36.md` l.48, `round-38.md` l.119, `round-39.md`, `round-40.md` l.87, `round-43.md` l.25) as a **refused staged Zenn row that was never registered**. Reusing `S150` would make those refusals point at this row. Recommended id: **`S151`**.

## 3. Behavioural probe (synthetic; not a carrier, not a vendor byte)

Script: `.ufo/waves/round-50/w1/C1SrcUnblob/probe-le-handler.sh` (run once, `S=/fast/scratch/hyaku/kaidoku-r50/C1SrcUnblob/run1`, exit 0). It builds a host LE v4 xz image with `mksquashfs 4.7.5 -comp xz -all-time 0 -mkfs-time 1700000000` (superblock: `hsqs`, major 4, minor 0, comp 4, `mkfs_time 1700000000`, `bytes_used 300433`), and a twin with `mkfs_time := bytes_used` (the AVM marker), with the same content otherwise.

| run | command | exit | handler (report) | extract argv (log) | error reports |
|---|---|---|---|---|---|
| sasquatch std | `sasquatch -le -no-exit-code -f -d OUT std.sqsh` | 0 | — | — | content tree `d99b1489…` |
| sasquatch synth | `sasquatch -le … synth.sqsh` | 0 | — | — | content tree `d99b1489…` (equal) |
| unblob std, full PATH | `unblob -e … -f --report … std.sqsh` | 0 | `squashfs_v4_le` | `sasquatch -le -no-exit-code -f -d …_extract …` | none |
| unblob synth, full PATH | same, synthetic | 0 | `squashfs_v4_le` | identical argv | none |
| unblob synth, PATH without `sasquatch-v4be` | `env PATH=<sasquatch-only>:/usr/bin:/bin unblob …` | 0 | `squashfs_v4_le` | identical argv | none |
| unblob std, PATH without `sasquatch` | same, std image | **1** | `squashfs_v4_le` | `sasquatch -le …` | `ExtractorDependencyNotFoundReport`, `dependencies: ["sasquatch"]` in the chunk's `extraction_reports` |

Content-tree sha256 of the unblob extraction (names stripped) is equal for std and synth (`d99b1489…`). Raw directory names differ (`<image>_extract`), which the counter's path mapping must handle.

Synthetic image sha256s (not receipts of vendor bytes): std `a3aa1a8c…`, synth `86ec8a04…`.

## 4. Findings for the L1

| id | finding | evidence | severity | action |
|---|---|---|---|---|
| F1 | LE handler never reads the AVM marker; disclosed limit (1) of R50-C1 is a source fact plus a probe | §1 Q4/Q5/Q7, §3 identical argv and tree | confirms plan | keep limit (1) as stated; cite S151 |
| F2 | `no -be binary needed` holds for LE: unblob exits 0 with sasquatch-v4be absent | §3 `synth-nobe` exit 0 | confirms plan | none |
| F3 | **CTL-C1-3 gap.** A run with `sasquatch` absent still reports `handler_name: squashfs_v4_le`; the error sits in the chunk's `extraction_reports`, and unblob exits 1. A handler-name clause alone passes it. | §3 `std-nosasq`, report path `[0].reports[3].extraction_reports[0]` | **real defect in the drafted counter**; caught pre-freeze | C1 handler clause must require `extraction_reports == []` on the chunk **and** unblob exit 0; CTL-C1-3 scored with that |
| F4 | `dependencies` in the missing-extractor report lists only the executable chosen (`["sasquatch"]`), not `get_dependencies()` (both binaries). Anyone expecting both in the red receipt will mis-match. | §3 | minor | expected value for CTL-C1-3 is `["sasquatch"]` |
| F5 | unblob's log carries 10 debug-level Python tracebacks per run (from `cpio_binary` and `compress` `calculate_chunk` probes). They are not errors (`[error` appears only for F3). | `grep -c Traceback` = 10 per log; `grep '\[error'` one line in the missing-sasquatch run | minor | counter reads the JSON report, never greps the log for `Traceback` |
| F6 | extraction root name is `<input-file-name>_extract` (e.g. `le-v4-xz.sqsh_extract`), not a fixed root. | §3 `ub-*/ex/` listings | counter-relevant | the plan's "exact path relative to the chunk extract root" must be computed from that directory, not from `ex/` |
| F7 | S150 id collision in the registry (see §2). | `grep -rn S150 corpus/` | registry | use `S151` |
| F8 | S108 and S112 are duplicate rows for one URL with overlapping anchors; both stay as they are (append-only). | registry rows 114, 118 | calibration note | none this round; record in the round-50 Gate |

## 5. Gate text and drafts

Full drafts are in `.ufo/waves/round-50/w1/C1SrcUnblob/drafts.md`:
- **D1** registry row (11 cells, no `|` inside cells, id `S151`, `opened 2026-10-28`, `recheck 180d`, `used-by corpus/knowledge/<R50-C1 entry stem>.md` placeholder).
- **D2** lesson `## Gate` table (S151 admit, S108 and S112 re-checked and kept unchanged), with the round-49 table shape.
- **D3** CTL-C1-3 note (F3).

## 6. Receipts and custody

Under `.ufo/waves/round-50/w1/C1SrcUnblob/`:
- `probe-le-handler.sh` (the probe; sha256 recorded by the L1 on commit) and its stdout `receipts/probe-receipt.txt` (sha256 `78aee89269c9b099ac39331cb6fbb48cfb65bae92110b9a7b9ca6bb5bcc27a75`).
- `unblob-26.6.4-squashfs.py` (MIT source, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`), copied for the L1's re-check.
- `receipts/ub-std-full/`, `ub-synth-full/`, `ub-synth-nobe/`, `ub-std-nosasq/`: `report.json` and `unblob.log` (sha256 in the table below).
- `drafts.md`.

| file | sha256 |
|---|---|
| receipts/ub-std-full/report.json | 811890049ccee9fd96e1b63b6087c23733a944a1a91809f04dbf9f6d0d2a9cfa |
| receipts/ub-std-nosasq/report.json | f1926f387e5262f489087bb0f9490eb6a282f9fbbe7dc93d12ade0b863627c62 |
| receipts/ub-synth-full/report.json | 7e54ffa341a2a7b14855afc696b4291975f94ee45c3ec4ab80a37cea8994aefe |
| receipts/ub-synth-nobe/report.json | a94c9ebdd9ce1ae6a1443dd6967b538682ac2dbb9b69bf454e31aa9fdd5027e3 |
| receipts/ub-std-full/unblob.log | 7365691371a331f0538f734f77300e976f31ac95e8aef4ce278ba407a058f04b |
| receipts/ub-std-nosasq/unblob.log | 0f09e592a528ed43ddc8a430da5ef4dd588225802be8653ef827f33751041cf0 |
| receipts/ub-synth-full/unblob.log | b4eb219d46031d7b8b2801a8e09679c5c8d28786a7ae86dadbcc900c07c886d6 |
| receipts/ub-synth-nobe/unblob.log | 8f48c373a942ebd8522e41c5b6c40f038877a6e43b5e93a21ba4787344b038d2 |

Installed binaries (read only; no install, no PATH change, no pacman):
- `~/.local/bin/sasquatch` sha256 `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`, `-v` reports `unsquashfs version 4.5.1`; equals S107's package member `usr/bin/sasquatch`.
- `~/.local/bin/sasquatch-v4be` sha256 `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`; equals S107's `usr/bin/sasquatch-v4be`.
- `~/.local/bin/unblob` reports `26.6.4`.
- `/usr/bin/mksquashfs` and `/usr/bin/unsquashfs` 4.7.5 (used only to build the probe image).

Tools installed or upgraded by this seat: **none**. Disk guard (`scripts/hyaku/disk-guard.sh status`, exit 0): `/fast/scratch/hyaku` 31% used, 554.8G free. Scratch `/fast/scratch/hyaku/kaidoku-r50/C1SrcUnblob` removed after receipts were copied. No vendor firmware was downloaded and no `--data-run` was executed; the lane tree was not written.

## 7. Not run

- Counter port, control fixtures, REA `extract-firmware` on real AVM carriers: out of this seat's scope (other seats).
- The Freetz `AVM-BE-format.txt` and the `AVM_LE` define patch: out of scope here (C1SrcAvmIndex).
- No check that REA 6.5.0 passes the chunk through unchanged: not run by this seat.
