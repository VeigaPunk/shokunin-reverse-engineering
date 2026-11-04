# Nested SquashFS container chains through REA `extract-firmware`: publication is not analysis (round 84, R84-C3)

status: R84-C3 measured and governed — the nested-container edge class is Core for the bounded
class named below iff `tools/round-84/nested-sqfs.py --rev <REV> --work <SCRATCH> --json-out
<OUT>` reports A1-A9 true, the file-count control firing, `met true` and exit 0 at the measured
revision (SCORECARD `## 2026-11-04 — round 84`). The before state is the unmeasured Frontier
bullet: at BASE `043b89a25241710a68b45526c3287fb3c8d907c3` the counter does not exist
(`git show BASE:tools/round-84/nested-sqfs.py` fails) and `PROVINCE.md` + `corpus/README.md`
each list "nested sub-images below depth 1" as open.

source: S301 — mksquashfs(1) manual page, `-repro-time TIME`, https://man.archlinux.org/man/mksquashfs.1.en — "build a reproducible filesystem image. This is equivalent to specifying -mkfs-time TIME and -inode-time TIME, which achieves reproducibility by setting all timestamps to TIME." (24 words, derived-text lines 168-174; snapshot sha256 `3ea8c1a1b429a5da35c7ffa0719ee2dade48ab8566c099c02b2c25bbe2052765`) — grounds the reproducible fixture chain; it says nothing about extraction behaviour.
source: S302 — rea-agents 6.5.0 `dist/firmware/FirmwarePublication.js:17` (installed package file, sha256 `bb4f3246bee70a5b32b048e5ef956e649626b6449b1d457454440739a8d51029`) — "Rerun extract_firmware with a higher max_depth (up to 10) and a fresh output_directory to descend into this path." (18 words) — the provider's own remedy text for a `depth-limited` gap.
verified-at: 2026-11-04 (receipt `.ufo/waves/round-84/pre/c3-pilot.json`; the landing run is `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-84/l1/scores/c3-at-landing.json` at the measured revision)
recheck: `python3 -I -B tools/round-84/nested-sqfs.py --rev <REV> --work <SCRATCH> --json-out <OUT>` -> exit 0, `met true`, all nine arms true; the fixture pins are `a`/`b`/`c` and must be unchanged. Source recheck: refetch the mksquashfs page and `grep -n 'repro-time' <snapshot>`; re-read `FirmwarePublication.js:17` in the pinned 6.5.0 package.

## The measured surface

[observation] The fixture is a lane-built three-level chain of standard little-endian SquashFS v4
images (mksquashfs 4.7.5, gzip, block 4096, `-repro-time 1760000000`): `c.sqfs` holds three leaf
files, `b.sqfs` holds `c.sqfs` plus two files, `a.sqfs` holds `b.sqfs` plus one file. Rebuilding
twice yields identical digests (`-repro-time`), and each nested carrier's bytes equal its
`unsquashfs` oracle member (`b_is_oracle_member true`, `c_is_oracle_member true`). Fixture pins:
`a e82c59956789a47b7524dda30d9ac4f6139a4cf279b0e5403039df88549d06c2`,
`b 7d2dd0e73d1bbeffe02aef346ea45b5c3604255a598b9cb7b1daaa6ef6fc3d1a`,
`c f68b42fa16a9b1ed0fd57165f0a949e89271c09a59db680b3e39a155fbea4aa8`.

[observation] `rea-agents@6.5.0 extract-firmware a.sqfs <absent-out> --max-depth 3 --format json`
publishes exactly the eight oracle members (three containers, five regular files) at their exact
nested relative paths under `firmware.bin_extract/`, with every published sha256 equal to the
oracle's, and reports `coverage: partial`, one `extraction_gaps` entry of kind `depth-limited`
whose `input_path` is the deepest extract root
`firmware.bin_extract/inner-b.sqfs_extract/inner-c.sqfs_extract`, and one
`depth_limited_paths` entry naming the same root. The leaf level's files carry
`analysis_depth: null`; mid-level files carry `2`; the outer-level members carry `1`.

[observation] The same command with `--max-depth 4` publishes the same eight members with the same
bytes, reports `coverage: complete`, no `extraction_gaps` and no `depth_limited_paths`, and the
leaf-level files carry `analysis_depth: 3`. The unblob engine block is identical across both runs
(`unblob` 26.6.4, executable sha256 `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`),
and both runs exit 0.

[inference] Publication and analysis are not the same set. At `--max-depth N` the provider
descends the chain to level N (the deepest level's members are published) but analyzes only
levels 1..N-1, recording one `depth-limited` gap at the deepest extract root. Reading the
published file list as the completeness signal therefore cannot see the difference: the cheap
rule "published count equals the oracle count, therefore complete" labels the depth-3 run
complete although the provider itself reports `partial` (the counter's control arm fires on
exactly this). The provider's own remedy text (S302) names the fix: a higher `max_depth` and a
fresh output directory.

[inference] The rule for this bounded class is: a three-level standard LE v4 gzip chain needs
`--max-depth 4` for `coverage: complete`; at `--max-depth 3` the eight members are all present
but the deepest level is unanalyzed and the envelope says `partial`. Reading `coverage` and the
gap list, not the file count, is what distinguishes the two.

## Scope, and what this does not establish

[unknown] Not covered: vendor or otherwise externally supplied images (the carriers here are
lane-built), compressors other than gzip, block sizes other than 4096, the AVM/BE layouts the
lane holds elsewhere, any chain other than the measured three-level fixture (two-level and four-level chains
unmeasured), chains whose intermediate levels contain more than one container, providers other than unblob 26.6.4, and any image whose member count, byte count or
path set exceeds the provider's `--max-output-files`/`--max-output-bytes` budgets.

[unknown] `analysis_depth: null` is read from the envelope field of the same name; it is not an
independent statement about what the provider did with those bytes beyond its own record. No
claim is made that a `depth-limited` run would miss members for every provider version; the
remedy text is from 6.5.0 only.

[observation] The chain recipe, oracle, envelopes and the file-count control are re-derivable
from the receipt: `fixture_pins`, `chain.oracle_counts`, `depths.3.observed`,
`depths.4.observed`, `arms`, `control`. The receipts are `.ufo/waves/round-84/pre/c3-pilot.json`
(pre-freeze pilot, disclosed) and the landing receipt named in the status line.
