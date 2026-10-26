# R36ExecReproK4 — independent reproduction of R36-C1 carrier K4

Seat: leaf executor, round 36 wave 1. Advisory only. No frozen predicate, counter, carrier, harness or
oracle was changed; nothing outside this report file was written; no VCS mutation; no `agent://all`
message; no subagent, no background job. Scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36ExecReproK4`
removed at the end (every number below is transcribed into this file).

**Verdict: K4 reproduces exactly.** My two independent REA `extract-firmware` runs (sasquatch on PATH,
and every PATH directory holding an executable `sasquatch` removed) reproduce the committed
`K4/after.json` and `K4/before.json` **file-set and gap evidence with 0 differing entries**; my
independent `/usr/bin/unsquashfs` run reproduces `K4/oracle.tsv` **byte-for-byte** (sha256 equal). One
extra discriminator probe (§8) shows the after/before difference is attributable to the `sasquatch`
binary alone, not to its `sasquatch-v4be` sibling. Four advisory nuances (§7) — none is a defect in
the committed evidence.

I ran the REA CLI directly (as this seat's assignment specifies), **not** through
`tools/round-36/c1-run.sh`, so the reproduction is independent of the frozen harness as well as of
the committed receipts.

---

## 1. Environment (observed; nothing installed, upgraded or removed)

| component | value | how observed |
|---|---|---|
| rea-agents | `6.5.0` | `npx -y rea-agents@6.5.0 --version` → `6.5.0`, exit 0; resolved from npx cache `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (`package.json` name/version `rea-agents 6.5.0`) |
| unblob | `26.6.4` | `~/.local/bin/unblob --version`; both receipts record `engine = {name: "unblob", version: "26.6.4", executable_path: "/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob", executable_sha256: "0ce7b624f540c2191ff14489…"}` identically in mine and committed |
| `REA_UNBLOB_COMMAND` | `$HOME/.local/bin/unblob` (exported, as the harness does) | my invocation |
| sasquatch | `unsquashfs version 4.5.1 (2022/03/17)` | `~/.local/bin/sasquatch -version` |
| sasquatch sha256 | `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`, 382824 B | `sha256sum` — equals `sasquatch_sha256` in committed `K4/after-run.json` |
| sasquatch-v4be (sibling, not used) | 436232 B, present in `~/.local/bin` | `ls -l`; exercised only in the §8 discriminator |
| unsquashfs (oracle) | `unsquashfs version 4.7.5 (2026/03/01)` | `/usr/bin/unsquashfs -version`; equals `oracle-run.json` |
| node/npx | `fnm_multishells/6713_1792986395296/bin/node` | `command -v node` |

**PATH facts.** Full PATH = 20 entries, of which exactly **one** holds an executable `sasquatch`:
`/home/vgpnk/.local/bin`. The frozen filter
(`":".join(d for d in PATH if not os.access(d + "/sasquatch", X_OK))`) therefore drops exactly that one
directory → scrubbed PATH = 19 entries; a scan of all 19 for `$d/sasquatch` reports
`sasquatch_hits_in_scrubbed_path=0`, and `env -i PATH="$scrubbed" /usr/bin/which sasquatch` →
`no sasquatch in (…)`, exit 1. `unblob` stays reachable in both modes because it is passed by absolute
path via `REA_UNBLOB_COMMAND`, and both receipts name the same engine executable.

## 2. Carrier acquisition (frozen URL, digest checked)

```
curl -sSL -o "$S/nvim-linux-arm64.appimage" \
  https://github.com/neovim/neovim/releases/download/v0.12.6/nvim-linux-arm64.appimage    # exit 0
sha256sum → 8efcec73cea1cebcd3a19da0bc782c0c6d95da7ae6006902a9d93b5ac9efe1c2   11356680 bytes
```
Equal to `carriers.json` K4 `sha256`, to `subject.digest.sha256` in both committed receipts, and to
the `carrier_sha256` in `K4/{after,before,oracle}-run.json`. The lane holds no K4 fixture copy, so the
download *is* the carrier. Downloaded into my own scratch (different path from the committed runs'
`/fast/scratch/hyaku/kaidoku-r36/L1/carriers/…`), which is one axis of independence.

## 3. Squashfs offset, derived independently

ELF64 LE header of the carrier: `e_shoff=934536`, `e_shentsize=64`, `e_shnum=30` →
`934536 + 64*30 = 936456`; bytes at 936456 are `hsqs`. `e_machine=183` (`EM_AARCH64`) — the runtime is
an aarch64 static-pie, consistent with the K3-seat's note that no aarch64 binfmt/qemu exists here, so
the payload can only be reached statically. Superblock read at 936456, decoded by hand:

```
magic=0x73717368 (hsqs)  inodes=2247  blocksize=131072  fragments=148
compression_id=6 (zstd)  block_log=17  version=4.0  bytes_used=10417706
```
Matches committed `oracle-run.json` (`squashfs_offset: 936456`, `regular_files: 2130`). Note the
payload is **zstd**, not xz/gzip: sasquatch 4.5.1 handles this v4.0 zstd image (see §5).

## 4. Oracle reproduction (`/usr/bin/unsquashfs` at offset 936456)

```
/usr/bin/unsquashfs -no-progress -o 936456 -d "$S/oracle-root" "$S/nvim-linux-arm64.appimage"
# exit 0; log: "Parallel unsquashfs: Using 32 processors", "2132 inodes (2273 blocks) to write",
#            "created 2130 files", "created 115 directories", "created 2 symlinks",
#            "created 0 devices/fifos/sockets/hardlinks"
```
Rows written by the frozen `regular files, relpath TAB sha256 TAB size, sorted` rule: **2130**.
`sha256sum` of my tsv = committed tsv = `d69c9a07dd7baca67227a814abf95832d7f25d9e7ea6809381940807cc39f067`
(239310 B); `cmp -s` → **byte-identical**.
Entry census of my own tree: 2130 regular + 2 symlink + 115 dirs (incl. root) = **2247 = superblock
`inodes`**. The 2 symlinks are exactly `.DirIcon → nvim.png` and
`nvim.png → usr/share/icons/hicolor/128x128/apps/nvim.png` (from `unsquashfs -ll`), i.e. the oracle is
genuinely "regular files only" and its exclusions are the two non-regular entries.

## 5. REA runs (my carrier path, my fresh out dirs, REA CLI directly)

```
after : PATH as given (20 dirs, sasquatch → ~/.local/bin/sasquatch)
        npx -y rea-agents@6.5.0 extract-firmware --format json "$S/nvim-linux-arm64.appimage" "$S/out-after"
before: PATH = frozen scrubbed form (19 dirs, zero dirs holding sasquatch)
        npx -y rea-agents@6.5.0 extract-firmware --format json "$S/nvim-linux-arm64.appimage" "$S/out-before"
```
Both runs: **REA CLI exit 0**; inner unblob `execution.exit_code` = **0** (after) / **1** (before);
`TMPDIR=$S`; stderr contained only `npm warn` lines, no other diagnostics.

Operational precondition observed (recorded, not a defect): REA refuses a pre-existing output root —
my very first attempt passed a directory I had already `mkdir -p`-ed and got
`{"code":"execution_failure", category:"execution_failure", message:"Analysis could not complete…",
details:{provider_id:"unblob", operation:"extract_firmware",
diagnostics:{reason:"Extraction output root already exists"}}}`, **exit 1**, no receipt. Re-run against
a non-existent path → exit 0, full receipt. So "fresh out dir" must be non-existent, not merely empty;
any replayer that pre-creates it will see exit 1 with that reason string.

| | committed `after.json` | my after | committed `before.json` | my before |
|---|---|---|---|---|
| `normalized_result.files` | 2147 | **2147** | 2 | **2** |
| `(relative_path, sha256)` set | — | **identical (0 only-mine / 0 only-committed)** | — | **identical (0 / 0)** |
| `published_bytes` | 51792724 | 51792724 | 11356680 | 11356680 |
| `coverage` | partial | partial | partial | partial |
| `chunks` | 27 | 27 | 3 | 3 |
| `derivations` | 2265 | 2265 | 2 | 2 |
| `unpublished_entries` | 2 | 2 | 0 | 0 |
| `diagnostics` | 0 | 0 | 1 | 1 |
| `extraction_continuations` | 1 | 1 | 1 | 1 |
| `depth_limited_paths` | 0 | 0 | 0 | 0 |
| unblob self-report (stdout) | — | 2140 files / 124 dirs / 2 links, chunk mix `ELF64 29.01 MB 74.48%` + `SQUASHFS_V4_LE 9.94 MB 25.52%` + `PADDING 8.00 B 0.00%`, no ERROR row | — | 2 files / 1 dir / 0 links, chunk mix `SQUASHFS_V4_LE 9.94 MB 84.76%` + `ELF64 1.79 MB 15.24%`, one `Severity.ERROR ExtractorDependencyNotFoundReport` row |
| unblob exit | 0 | **0** | 1 | **1** |
| REA CLI exit | — | **0** | — | **0** |
| `evidence_id` | `ev_ff0fdb798eea077df0b11dcdd3795794c9069c667424b85c5f67f566c97379fa` | `ev_b5d765a1eed15dc57f1a7a78849840e7cb846369e58a4407dc998ff2b066fee8` | `ev_fffca90bc4b70989308fcc378c3cdefdd5baaf8ee878d8e624dc31709f5b1a01` | `ev_b17098ba91510a8e82d0a94c79d848c311de7f3e1df74eb572790633854e33c3` |

My receipts (kept as hashes only; `$S` removed): after.json `4384716` B
`964a91d651a385c46055aae077b4e56058f163b4727530b1bf89abc38153cba5`; before.json `12022` B
`dce64aee0dfc135254e9c117580b236944e8a9a63b7c7cbf4bd4847d4bfb99f2`.

### 5a. Gap comparison (kind / dependencies / handler / input_path / relative_path)

- **after, mine == committed, exactly:**
  `[("unpublished-entry", [], null, "$output/…/.DirIcon", "…/.DirIcon"), ("unpublished-entry", [], null, "$output/…/nvim.png", "…/nvim.png")]`
  → **no `missing-extractor-dependency` gap and no `sasquatch` string anywhere in the after gaps.** The
  two unpublished entries are exactly the two symlinks of §4; `derivations`, `continuations`,
  `unpublished_entries` and `depth_limited_paths` are field-equal (not just length-equal).
- **before, mine == committed, exactly:**
  `[("missing-extractor-dependency", ["sasquatch"], "squashfs_v4_le", "$input", null)]` with
  `range = root_file_range = {offset: 936456, length: 10420224}`, `chunks[squashfs_v4_le].extraction_failed = true`,
  and `diagnostics[0] = {input_path:"$input", stage:"squashfs_v4_le", missing_dependencies:["sasquatch"],
  report:{severity:"ERROR", dependencies:["sasquatch"], __typename__:"ExtractorDependencyNotFoundReport"}}`.
  (Only the run-scoped `provider_id` scalar differs: mine `555559:2` vs committed `245123:2`, §7.3.)

### 5b. Oracle coverage, computed per run by suffix path + sha256 against the committed `oracle.tsv`

Prefix used (verified present in both receipts): `firmware.bin_extract/936456-11356680.squashfs_v4_le_extract/`.

| run | oracle rows matched | missing | wrong sha256 |
|---|---|---|---|
| after, mine | **2130 / 2130** | 0 | 0 |
| after, committed | 2130 / 2130 | 0 | 0 |
| before, mine | **0 / 2130** | 2130 | 0 |
| before, committed | 0 / 2130 | 2130 | 0 |

Non-oracle published paths in my after run — **17**, fully enumerated: 1 outer carve
`firmware.bin_extract/0-936456.elf64_extract/carved.elf` (936456 B), 8 ×
`…/<file>_extract/0-<n>.elf64_extract/carved.elf` (whole-file chunks, depth 2) and 8 × `…/<file>_extract/<n>-<n+1>.padding`
(1 B each, `6e340b9c…` = sha256 of one zero byte; depth `null`). 2130 + 17 = 2147 exactly; duplicate
`relative_path` count 0; published-depth histogram `{1: 2131, 2: 8, null: 8}`. The 8 carved files are
`usr/bin/nvim`, and the 7 `usr/lib/nvim/parser/*.so`. This is the same "unblob keeps whole-file chunks
and publishes recursion output beside them" behaviour the claim lists as a disclosed pre-freeze probe.

My before run publishes 2 paths, both anchored to carrier byte ranges
(`sha256` recomputed by me from the carrier): `firmware.bin_extract/0-936456.elf64_extract/carved.elf`
= `ea6fcc154b1a7f107cf30e245fedac76dc5a60dcfb3122ca9a8dc27957cdd590` = sha256 of bytes `[0,936456)`;
`firmware.bin_extract/936456-11356680.squashfs_v4_le` (whole-file chunk, `mime null`)
= `14bff9fee8106d1d694897cdeda2304f8c77b8df8ff145c01b93ac27f046a5bf` = sha256 of bytes
`[936456,11356680)`. My after run has **no** whole-file squashfs chunk (it was extracted instead) — the
concrete behaviour change the claim asserts.

### 5c. Full-document diff, to show nothing else moved

Recursive leaf diff of my receipt vs the committed one, then the same diff after normalising
run-scoped paths (`/fast/scratch/…` → `<PATH>`) and allocator ids (`\d+:\d+`):

- **after**: 2147 differing leaves under `normalized_result.files`, **all of them the `path` field**;
  2265 under `derivations`, **all `provider_blob_id`**; 27 under `chunks`, **all `provider_id`**;
  `extraction_gaps`, `extraction_continuations`, `unpublished_entries`, `depth_limited_paths` = 0
  differing leaves; plus `evidence_id`, `subject.local_path`, `parameters.path`,
  `parameters.output_directory`, `normalized_result.output_directory`.
  After normalisation: **`raw_result` equal (1390149 B canonical JSON both sides)** and
  **envelope-minus-`raw_result`-minus-`evidence_id` equal**. `analysis_profile`, `authority`,
  `limitations`, `coverage`, `published_bytes` equal as well.
- **before**: 2 files (`path` only), 2 derivations (`provider_blob_id`), 3 chunks (`provider_id`),
  1 gap (`provider_id`), 16 `raw_result.report` leaves and 4 `raw_result.execution.args` leaves (the
  `--report/--log/--extract-dir` temp paths). After the same normalisation:
  **`raw_result` equal (6761 B both sides)** and **envelope-minus-`raw_result`-minus-`evidence_id`
  equal**.
- **`evidence_id` differs and is not counted, as instructed**: the semantic projection includes
  `parameters` + `normalized_result`, hence the volatile `output_directory` and carrier `local_path`.
  I did **not** recompute ids (that binding is the counter's; this seat's assignment excludes it) — I
  only established that the ids differ and that *everything else* is equal modulo run-scoped metadata.

## 6. Exit codes, all runs (verbatim)

| run | command | exit |
|---|---|---|
| carrier download | `curl -sSL` | 0 |
| after (first attempt, pre-created out dir) | `npx -y rea-agents@6.5.0 extract-firmware …` | **1** (`execution_failure`, "Extraction output root already exists") |
| after (fresh out dir) | same | **0** |
| before (scrubbed PATH) | same | **0** |
| v4be-only discriminator (§8) | same | **0** |
| oracle | `/usr/bin/unsquashfs -no-progress -o 936456 …` | **0** |
| oracle tsv compare | `cmp -s` | 0 (identical) |
| version probes | `npx -y rea-agents@6.5.0 --version`, `unblob --version`, `unsquashfs -version` | 0 |

## 7. Advisory nuances (reported, not repaired; all present identically in the committed receipts)

1. **`reported_sha256 == null` for 8 of the 2147 after entries and 1 of the 2 before entries.**
   The 8 are the `…padding` chunks (`analysis_depth: null`); the 1 is the whole-file
   `firmware.bin_extract/936456-11356680.squashfs_v4_le` chunk. `sha256` (computed by REA) is present
   in every case; only the *reported* value is null. Identical field-for-field in the committed
   receipt, so not a reproduction difference — but any consumer that reads `reported_sha256` instead
   of `sha256` will see nulls. All 2130 oracle-matched entries carry
   `reported_sha256 == sha256 == oracle sha256`.
2. **`unpublished_entries[].link_target` is the resolved target, not the immediate one.** unblob gives
   `.DirIcon → usr/share/icons/hicolor/128x128/apps/nvim.png` (the target of the *second* symlink),
   whereas `unsquashfs -ll` shows `.DirIcon → nvim.png`. Same for `nvim.png`. Committed receipt and
   mine agree exactly; worth knowing only if a later counter compares `link_target` to the raw inode
   string.
3. **`provider_id` / `provider_blob_id` / `blob_id` are run-scoped allocator ids, not content.** Three
   separate runs on this host produced three different prefixes (`554774:…` mine-after,
   `555559:…` mine-before, `348737:`/`245123:` committed) with identical suffix numbering. They are
   the only scalar differences in `chunks`/`derivations`/`extraction_gaps`; they must not be used as
   content equality evidence, and I excluded them explicitly rather than treating them as diffs.
4. **The before-path filter drops a directory, not a binary.** `/home/vgpnk/.local/bin` holds both
   `sasquatch` and `sasquatch-v4be`, so "every PATH dir containing `sasquatch` removed" removes both
   binaries at once. Harmless here (§8 shows v4be alone does not close the gap), but the filter does
   not isolate a single executable — it isolates a directory.

## 8. Extra falsifier I ran: `sasquatch` alone is what closes the gap

To rule out an attribution error (the after file set could have come from `sasquatch-v4be`, from a
7z/direct-carve fallback, or from the filtered directory's absence for an unrelated reason) I ran a
third extraction with a hand-built PATH: `$S/bin-v4be-only` (holding **only** a symlink to
`sasquatch-v4be`) prepended to the scrubbed PATH. Asserted with `env -i PATH=… which`:
`sasquatch` → **absent**, `sasquatch-v4be` → `$S/bin-v4be-only/sasquatch-v4be`; `node`/`npx` and
`REA_UNBLOB_COMMAND` unchanged.

Result (exit 0): `files = 2`, `published_bytes = 11356680`, gap
`[("missing-extractor-dependency", ["sasquatch"], "squashfs_v4_le")]`, same single diagnostic,
`(relative_path, sha256)` set **equal to my before run** (2/2). So:
- `sasquatch` is **necessary** — no fallback path exists in the squashfs handler;
- `sasquatch` is **sufficient** (my full-PATH after run had only that one extra directory);
- `sasquatch-v4be` **cannot** substitute for it on this LE image, and the gap names `sasquatch`, which
  is exactly the frozen expectation for K4.

## 9. Exact commands (scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36ExecReproK4`)

```
curl -sSL -o "$S/nvim-linux-arm64.appimage" https://github.com/neovim/neovim/releases/download/v0.12.6/nvim-linux-arm64.appimage
export TMPDIR="$S" REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob
npx -y rea-agents@6.5.0 extract-firmware --format json "$S/nvim-linux-arm64.appimage" "$S/out-after"     # exit 0
PATH=<scrubbed 19-dir PATH> npx -y rea-agents@6.5.0 extract-firmware --format json \
     "$S/nvim-linux-arm64.appimage" "$S/out-before"                                                     # exit 0
PATH="$S/bin-v4be-only:<scrubbed PATH>" npx -y rea-agents@6.5.0 extract-firmware --format json \
     "$S/nvim-linux-arm64.appimage" "$S/out-v4be"                                                       # exit 0
/usr/bin/unsquashfs -no-progress -o 936456 -d "$S/oracle-root" "$S/nvim-linux-arm64.appimage"            # exit 0
# comparisons: python3 -I over normalized_result.files / extraction_gaps / oracle.tsv (no writes)
```
PATH scrubbing expression (the frozen one, re-derived rather than imported):
`python3 -I -c 'import os,sys; print(":".join(d for d in sys.argv[1].split(":") if d and not os.access(os.path.join(d,"sasquatch"), os.X_OK)))' "$PATH"`

## 10. Limits / what I did not do

- Not run: `c1-counter.py`, `c1-counter.py --selftest`, any control (`CTL-C1-0/1/2`), K1/K2/K3, any
  PROVINCE/README/knowledge binding check, evidence-id recomputation. `carriers_matched` and
  `met_target` are **not** asserted here.
- Not re-tested: 7z fallback, BE/AVM carriers, the aarch64 AppImage **runtime** (no
  `qemu-aarch64*` and no binfmt handler on this host — confirmed to me by the K3 seat and consistent
  with my own inability to execute the payload; only the static offset-936456 squashfs was read),
  loader behaviour, or anything about the extracted programs.
- No tool installed/upgraded/removed (nothing to record for the 2026-10-19 tooling directive);
  `npx` used the already-present 6.5.0 cache; `sasquatch` 4.5.1 used read-only.
- Receipt JSONs lived only in my scratch; every count, set claim, hash and exit code above is
  transcribed into this file, and the scratch tree (carrier, extraction trees, receipts) was removed.

## 11. Retained evidence (the falsifiable anchors)

- carrier sha256 `8efcec73cea1cebcd3a19da0bc782c0c6d95da7ae6006902a9d93b5ac9efe1c2`, 11356680 B.
- offset/superblock: `e_shoff=934536 e_shentsize=64 e_shnum=30 → 936456`, magic `hsqs`,
  `inodes=2247 blocksize=131072 comp=6 (zstd) frags=148 v4.0 bytes_used=10417706`.
- oracle: 2130 rows, `cmp -s` clean vs committed; tsv sha256
  `d69c9a07dd7baca67227a814abf95832d7f25d9e7ea6809381940807cc39f067`; entry census
  2130 regular / 2 symlink / 115 dirs = 2247 inodes.
- after: 2147 files, 51792724 published bytes, 0 differential-file entries vs committed
  (0/0), 2130/2130 oracle matches, gaps = 2 × `unpublished-entry` with empty dependencies,
  17 enumerated non-oracle paths, unblob exit 0, REA exit 0, receipt sha256 `964a91d6…53cba5`.
- before: 2 files, 11356680 published bytes, 0 differential entries (0/0), 0/2130 oracle matches,
  gap = `missing-extractor-dependency`/`["sasquatch"]`/`squashfs_v4_le`/`$input` with
  `range = {936456, 10420224}`, 1 diagnostic, unblob exit 1, REA exit 0, receipt sha256
  `dce64aee…4bfb99f2`.
- v4be-only probe: 2-file set identical to `before`, same gap, exit 0 → `sasquatch` alone is
  necessary and sufficient; `sasquatch-v4be` cannot substitute.
- path filter: 20 → 19 PATH entries, exactly `/home/vgpnk/.local/bin` dropped, 0 remaining dirs
  holding `sasquatch`.
