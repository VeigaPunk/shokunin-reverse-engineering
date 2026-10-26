# R36W2ReviewerEntryC1 — wave-2 falsification: `2026-10-26-r36-sasquatch-squashfs-recursion.md`

Seat: R36W2ReviewerEntryC1 (leaf, kaidoku-shokunin round 36 wave 2). 2026-10-26.
Target: every number and path in `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` at tip `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930` (file committed clean in `ffc81341`, `git status --porcelain` empty), checked against committed files under `corpus/evidence/round-36/c1`, plus live re-derivation where committed bytes allow.

**Verdict: no numeric or path defect found. Every count, offset, digest, evidence id, gap shape, continuation id, composition number and external source number in the entry re-derives. Two minor wording/calibration notes (F1, F2 below); neither changes a measured value.**

## Method

All values below were read from the committed receipts with a parser (not copied from the entry), then independently re-derived where possible:

- Fixture bytes: `sha256sum` of committed `fixtures/k1-le-xz.sqsh` / `k2-le-gzip.sqsh`; superblock read (block_size@12, compressor@20, version@28).
- Oracle TSVs K1/K2 rebuilt from committed `fixtures/k1-src/`, `k2-src/` (relpath TAB sha256 TAB size, regular files, sorted) and diffed.
- Frozen counter run twice, read-only, receipts in scratch:
  `python3 -I -B tools/round-36/c1-counter.py --root <lane> --rev 3310d8fa27…7982 --freeze 790561d4…f7d0 --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out <scratch>` → exit 1, `carriers_matched: 4`, `before_evidence_id_ok`/`after_evidence_id_ok` true for all four K (also `after_oracle_hits` 3/4/2130/2130, `before_oracle_hits` 0×4, `carriers_unchanged` true, `oracle_frozen` true). Same at `--rev 01a44dbf…` (tip) → exit 0, `met_target: true`, bindings `coverage_map_row/entry_present/province_core_row/province_core_section/sourced` all true, `entry_source_ids = ["S107","S108","S109"]`.
- Vendor bytes: downloaded `nvim-linux-x86_64.appimage`, `nvim-linux-arm64.appimage`, `sasquatch_1.0_amd64.deb` from the release URLs into scratch; hashed; ELF offset recomputed (`e_shoff + e_shnum*e_shentsize`); `/usr/bin/unsquashfs -no-progress -o <off>` re-extracted both payloads and the 2130-row TSVs rebuilt and diffed against the committed `K3/oracle.tsv`, `K4/oracle.tsv`.
- Live recheck of the entry's 180d line: `HYAKU_SCRATCH=<seat scratch> bash tools/round-36/c1-run.sh after corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh <scratch>/recheck-after` → harness exit 0, `jq '.normalized_result|{files,gaps}'` → `{"files":3,"gaps":0}`.
- S107/S108/S109 release metadata via GitHub API; `squashfs.py` fetched at tag 26.6.4 and hashed.

No tool was installed or upgraded; no pacman transaction; `~/.local/bin/sasquatch*` untouched (read-only hash only). Scratch was `/fast/scratch/hyaku/kaidoku-r36/R36W2ReviewerEntryC1`, removed at the end; all cited values are reproduced inline here.

## Claim-by-claim results

### Header / sources

| Claim in entry | Result | Evidence |
|---|---|---|
| S107 asset `sasquatch_1.0_amd64.deb` 187244 B, sha256 `efbc92bd…ade95`, published 2026-01-27T11:57:51Z | OK | downloaded: 187244 B, digest matches; API `published_at` matches |
| S108 `squashfs.py` at tag 26.6.4 sha256 `2d7b901b…99287`; `EXECUTABLE="sasquatch"`, `V4BE_EXECUTABLE="sasquatch-v4be"`, `get_dependencies()` returns both | OK | fetched file hashes to `2d7b901b…`; lines 25–26 and 68–69 match; LE/BE args and AVM heuristic (`bytes_used == mkfs_time`, `-le`/`-be`, `-no-exit-code`) at lines 48–58 |
| S109 K3/K4 digests `b644d034…f29fb` / `8efcec73…e1c2`, published 2026-10-09T15:43:25Z | OK | downloaded vendor files hash to exactly those digests (sizes 11454968 / 11356680); API `published_at` matches |
| unblob 26.6.4, engine `executable_sha256 0ce7b624…1d09` | OK | all 8 receipts: `provider.version="26.6.4"`, `normalized_result.engine.executable_sha256="0ce7b624…"` |
| receipts committed at `3310d8fa…`; freeze `790561d4…`; base `cab59f22…`; counter `carriers_matched 4` at that revision; `before/after_evidence_id_ok` true ×4 | OK | `git show --stat`: 3310d8fa adds exactly the 8 after receipts; 790561d4 adds carriers/oracle/before/counters/harness/plans/selftest; counter runs above |
| recheck 180d: harness after-run on K1 → `{"files":3,"gaps":0}` | OK | reproduced live today (exit 0, same jq output) |
| base `corpus/README.md` Firmware row and `PROVINCE.md` bullet quotes | OK | `git show cab59f22…`: README.md:44 contains the exact "AppImage SquashFS carved but recursion blocked by missing sasquatch"; PROVINCE.md:135 heading `### Round-4 frontier (post-unlock)`, 149–150 the exact "(AUR-only); 7z fallback covers the carved-image path today." sentence |

### Carrier table (`carriers.json` + `K*/oracle*`)

| carrier | kind | sha256 | offset | rows | distinct | Result |
|---|---|---|---|---|---|---|
| K1 | bare v4 LE xz 128 KiB | `93802938…a589` | 0 | 3 | 3 | OK — fixture hashes equal; superblock block_size 131072, compressor id 4 (xz), major 4; `hsqs` at 0; oracle-run `regular_files:3, squashfs_offset:0`; oracle.tsv = rebuilt k1-src rows exactly |
| K2 | bare v4 LE gzip 4 KiB, symlink | `ce5bf60e…084f` | 0 | 4 | 4 | OK — same method: 4096, id 1 (gzip), v4; oracle.tsv = rebuilt k2-src rows exactly |
| K3 | AppImage x86-64, v0.12.6 | `b644d034…f29fb` | 944632 | 2130 | 2116 | OK — offset re-derived from ELF header = 944632, `hsqs` there; rows rebuilt from vendor bytes: 2130, 2116 distinct, **IDENTICAL to committed TSV** |
| K4 | AppImage aarch64, v0.12.6 | `8efcec73…e1c2` | 936456 | 2130 | 2116 | OK — same: offset 936456; rebuilt TSV identical; 14 duplicate-digest rows both |
| "14 rows share their bytes" (K3/K4) | OK | 2130−2116 = 14 recomputed both carriers |
| `oracle-run.json` records `unsquashfs version 4.7.5 (2026/03/01)` | OK | all four oracle-run.json; host `/usr/bin/unsquashfs -v` matches |

### Before (no sasquatch), all four carriers

| Claim | Result | Evidence |
|---|---|---|
| exactly one gap, `kind=missing-extractor-dependency`, `handler=squashfs_v4_le`, `dependencies=["sasquatch"]`, `input_path="$input"` | OK | all four before.json |
| `root_file_range` K1 `{0,73728}`; K2 `{0,208896}`; K3 `{944632,10510336}`; K4 `{936456,10420224}` | OK | receipt `offset/length` values; K1/K2 equal the committed fixture sizes exactly |
| `continuation_id` `4ca863d0…7a07a` identical ×4; instruction verbatim | OK | byte-equal strings in all four |
| one `ExtractorDependencyNotFoundReport`, severity ERROR, deps `["sasquatch"]`, stage `squashfs_v4_le` | OK | diagnostics array length 1 in each |
| `coverage` partial ×4 | OK | receipts |
| K1/K2: `files: []`, `published_bytes: 0`, one chunk = input, `extraction_failed: true` | OK | receipts |
| K3/K4: 2 files, `published_bytes` 11454968 / 11356680 = whole carrier | OK | receipts + downloaded carrier sizes match exactly |
| K3/K4 published paths: `firmware.bin_extract/0-944632.elf64_extract/carved.elf` (944632 B) / `0-936456…` (936456 B) + `<start>-<end>.squashfs_v4_le` | OK | receipts; additionally the before carved.elf digest equals sha256(carrier[0:offset]) and the chunk digest equals sha256(carrier[offset:]) recomputed from vendor bytes (`dee51346…`/`6398c783…` K3; `ea6fcc15…`/`14bff9fe…` K4) |
| oracle hits 0/2130 before | OK | recomputed match of published digests+suffixes against oracle.tsv: 0 |
| payload chunk `extraction_failed: true`, the two elf64 records not; three chunk records | OK | chunks arrays: 3 records, flags as claimed |

### After (sasquatch on PATH)

| carrier | rows | published | matched | extras | published_bytes | coverage | gaps | Result |
|---|---|---|---|---|---|---|---|---|
| K1 | 3 | 3 | 3 | 0 | 70086 | complete | none | OK |
| K2 | 4 | 4 | 4 | 0 | 273971 | partial | 1 unpublished-entry (symlink) | OK |
| K3 | 2130 | 2147 | 2130 | 17 | 51122564 | partial | 2 unpublished-entry (symlinks) | OK |
| K4 | 2130 | 2147 | 2130 | 17 | 51792724 | partial | 2 unpublished-entry (symlinks) | OK |

Byte checks: K1 70086 = 59+27+70000 (k1-src actual sizes `README.txt` 59, `etc/config.ini` 27, `payload.bin` 70000); K2 273971 = 200000+73890+75+6 (k2-src actual). `max_depth` 3 in all eight receipts (top-level `parameters`); `depth_limited_paths` empty ×8.

### Extras composition (17 = 9 carved.elf + 8 .padding)

- Runtime carve `firmware.bin_extract/0-944632.elf64_extract/carved.elf` 944632 B (K3) / `0-936456…` 936456 B (K4), same digest as the before-run carve — OK.
- 8 nested carved.elf: `usr/bin/nvim` plus exactly the seven `usr/lib/nvim/parser/{c,lua,markdown,markdown_inline,query,vim,vimdoc}.so` — OK (paths enumerated in both after.json).
- 8 `.padding`, each size 1, all sha256 `6e340b9c…a01d` = recomputed sha256 of a single NUL byte — OK; the doc's example path `usr/bin/nvim_extract/11170568-11170569.padding` exists verbatim in K3.
- None of the 17 extras' digests occurs in the oracle digest set (recomputed) — "no extra is a member of the squashfs image" holds; 2147 = 2130 + 17; over-count statement correct.

### Symlinks / coverage

- K2 `var/notice-link -> ../usr/share/doc/NOTICE`; K3/K4 `.DirIcon` and `nvim.png` -> `usr/share/icons/hicolor/128x128/apps/nvim.png` — all present in `unpublished_entries` as `{kind: "symlink", link_target: …}` — OK.
- Gap `kind=unpublished-entry`, `handler: null`, `dependencies: []`, shared `continuation_id 602c674b…8cfca`, instruction verbatim — OK ×3 carriers (K2 ×1, K3/K4 ×2).
- coverage: K1 complete, K2/K3/K4 partial after — OK. Published file records carry no mode field ("modes not published") — OK; the "lose executable permission bits" claim itself is grounded in the continuation text, not observable in receipts (noted, not contradicted).

### Install provenance

- `K*/after-run.json` ×4: `sasquatch: /home/vgpnk/.local/bin/sasquatch`, sha256 `ad02d27a…4754`, `unsquashfs version 4.5.1 (2022/03/17)` — OK; `K*/before-run.json` ×4: `sasquatch: ""` — OK.
- Host binaries read-only: sasquatch 382824 B `ad02d27a…`, sasquatch-v4be 436232 B `fac88740…` — OK.
- Deb members: downloaded `sasquatch_1.0_amd64.deb`, `ar x` + `tar -xJf`: members byte-identical (`cmp` clean) to `~/.local/bin` copies with exactly those sizes/digests — OK. `fac88740…` absent from all receipts, as the entry states — OK (grep over all 8 receipts + runs).

### Oracle method / limits

- `tools/round-36/c1-run.sh` implements exactly the described method: `hsqs`→0, else ELF64-LE `e_shoff + e_shnum*e_shentsize`; assert `hsqs`; `/usr/bin/unsquashfs -no-progress -o <off> -d <dir> <carrier>`; relpath TAB sha256 TAB size, regular files only (skips symlinks and non-regular), sorted; `oracle-run.json` fields `regular_files/squashfs_offset/unsquashfs` — OK (read the committed harness).
- K1/K2 independent expected record: oracle.tsv byte-identical to rows rebuilt from committed `k1-src/`/`k2-src/` — OK.
- K3 second oracle citation: `.ufo/waves/round-36/w1/R36ExecAppImageExtract.md` exists and states 2130/2130, 0 digest, 0 size mismatches (line 12) — OK; `R36ExecReproK{1,2,3,4}.md` all present.
- K4 limitation still true on this host: `qemu-aarch64` absent — OK.

### Receipts table (evidence ids)

All eight stored `evidence_id` values match the entry's table exactly: K1 `ev_df7bef52…`/`ev_b5bd2e7f…`, K2 `ev_7506d2a8…`/`ev_c939cd88…`, K3 `ev_91e4ab30…`/`ev_b83bd305…`, K4 `ev_fffca90b…`/`ev_ff0fdb79…` — OK; the frozen counter re-derives all eight to true at `3310d8fa…`.

## Findings

**F1 (wording, path shape — no count affected).** "members are published under `<carrier>_extract/` for a bare image": in all four committed receipts the bare-image members sit under `firmware.bin_extract/` (e.g. K1 `firmware.bin_extract/README.txt`, K2 `firmware.bin_extract/usr/lib/kaidoku/blocks.bin`), i.e. the prefix is the whole-file chunk name unblob assigns (`firmware.bin`), not a name derived from the carrier file name (`k1-le-xz.sqsh` would suggest `k1-le-xz_extract/`). The sentence is correct only if "<carrier>" is read as that chunk. Matching uses the suffix rule and is unaffected; suggest a future edit may spell out `firmware.bin_extract/`.

**F2 (calibration, "depth 3").** "(…parser .so) — depth 3, the configured maximum": `parameters.max_depth` is 3 in all eight receipts, so "configured maximum = 3" is right, but the deepest published files record `analysis_depth: 2` in the receipts (the 8 nested carved.elf; `.padding` records are null; the squashfs members are 1). No published file carries depth 3. Reading "depth 3" as "three chained extractions" is defensible but the receipts' own depth field stops at 2; a reader comparing the entry to `analysis_depth` will see 2.

**Recording, not a defect:** the entry's "the frozen counter reports `carriers_matched 4` at that revision" is exactly true at `3310d8fa…`, where `met_target` is still false because the entry/PROVINCE/README bindings do not exist until `ffc81341`. The entry does not claim otherwise; for completeness the counter at the tip `01a44dbf…` reports `met_target: true` with all bindings true and `entry_source_ids ["S107","S108","S109"]`.

## Numbers I could not re-derive

None material. Every number in the entry was re-derived from committed c1 bytes, live harness runs, vendor downloads, the GitHub API, or the frozen counter. The only entry numbers grounded solely in quoted source text (S107/S108/S109) were additionally confirmed against the live tag bytes/API today; none was left to trust alone. The "patched squashfs-tools 4.5.1" provenance of sasquatch and the S107 quote text rest on the cited scout receipts, not on c1 evidence, and are used by the entry only as provenance, not as measurement.

## Residual risk / verification gaps

- My K3/K4 oracle rebuild used the same `/usr/bin/unsquashfs` 4.7.5 as wave 1, so it confirms reproducibility, not independence; the entry states this limit itself, and the K3 AppImage-runtime cross-check remains the only code-separate confirmation (K4 single-implementation, as disclosed).
- The live after-run I reproduced is K1 only (cheap fixture); K2–K4 after-runs were not re-executed live this wave (their receipts are internally consistent, id-verified by the frozen counter, and the K3/K4 oracle halves were re-derived from vendor bytes).
- Downloads today confirm the vendor bytes still match the frozen digests; no authenticity claim beyond digest equality is made or tested.

## Tooling record

No installs or upgrades (operator authorization not exercised): used preinstalled `python3`, `curl`, `jq`, `git` (read-only subcommands only), `/usr/bin/unsquashfs`, host `~/.local/bin/sasquatch*` read-only, frozen counters/harness as committed. Scratch removed; nothing written outside this report file and the seat scratch.
