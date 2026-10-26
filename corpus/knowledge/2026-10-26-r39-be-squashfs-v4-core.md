# Standard big-endian SquashFS v4 through REA `extract-firmware`: Core on six frozen carriers, symlink outcomes stated before data

source: S122 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/file_utils.py — `is_safe_path` lines 34-39 — as read 2026-10-26
verified-at: 2026-10-26
recheck: 180d — `grep -c 'basedir.joinpath(path).resolve().relative_to(basedir.resolve())' ~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/file_utils.py` -> 1 (ran 2026-10-26)

**What is held.** REA `extract-firmware` (rea-agents 6.5.0, unblob 26.6.4 as `REA_UNBLOB_COMMAND`,
`sasquatch-v4be` 4.5.1 in `~/.local/bin` on the child `PATH`) extracts standard big-endian SquashFS v4
through unblob's `squashfs_v4_be` handler: on six frozen carriers every regular file of an independent
oracle is published with the same relative-path suffix and sha256, no chunk fails, and the only gaps
are one `unpublished-entry` per symlink that stays inside the extraction root.

| carrier | what it is | oracle files published | in-tree / escaping symlinks | gaps |
|---|---|---|---|---|
| K1 | round-37 synthetic BE gzip | 5/5 | 0 / 1 | none |
| K2 | round-37 synthetic BE gzip, space in a name | 3/3 | 1 / 0 | 1 `unpublished-entry` |
| K3 | unblob 26.6.4 `squashfs_v4_be` fixture, 4 KiB padded | 4/4 | 0 / 0 | none |
| K4 | the same fixture without padding | 4/4 | 0 / 0 | none |
| K5 | round-39 synthetic BE gzip: 4 directory levels, 0-byte and 5-block files, UTF-8 and space names | 10/10 | 2 / 1 | 2 `unpublished-entry` |
| K6 | round-39 synthetic BE **xz** (compression id 4, compressed xz data blocks) | 8/8 | 1 / 2 | 1 `unpublished-entry` |

Receipts: `corpus/evidence/round-39/c1/K{1..6}/after.json` (run by `tools/round-39/c1-run.sh after`,
output directories under `/fast/scratch/hyaku/kaidoku-r39/`). Carriers, oracles and symlink tables:
`.ufo/waves/round-39/c1/carriers.json`. Each oracle agrees with the independent reader
`tools/round-39/sqfs-list.py` and with direct `sasquatch-v4be -be` extraction.

**Symlink rule.** unblob keeps a symlink when its target, joined to the link's directory inside the
per-chunk extraction directory and resolved, is still under that directory (S122 `is_safe_path`); it
does not clamp `..` at the root, so a root-level `../hello.txt` escapes (K1). A kept link is published
as metadata only and REA records one `unpublished-entry` gap for it; a removed link is reported as
`MaliciousSymlinkRemoved` and leaves no gap. Absolute targets are re-rooted and kept. The mechanism on
the producer side, with source lines, is in `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md`
(Symlinks paragraph). "No extraction gap" is therefore the wrong success test for any image holding an
in-tree link; the right test is "gaps equal the in-tree link set" (round 38's stop,
`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`).

**Preconditions and failure signatures.** Without `sasquatch-v4be` on the child `PATH` the same carriers
publish nothing and carry `missing-extractor-dependency` naming `sasquatch-v4be` (round-38 before-arms).
An image whose `mkfs_time` equals `bytes_used` loses `-be` and fails; see the triage entry above.

**Limits.** Six carriers, four written by this lane's own generator (no third-party BE v4 writer is
available; `mksquashfs` writes LE only) and two from unblob's test suite. A receipt-only counter cannot
tell a re-minted fabricated receipt from a run; provenance comes from independent re-runs. Not held:
AVM-BE bodies, vendor-mangled SquashFS, directory or chained symlinks, special files, anything about the
extracted programs.
