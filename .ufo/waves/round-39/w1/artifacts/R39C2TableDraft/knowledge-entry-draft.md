# SquashFS `extract-firmware` outcome triage: seven classes separate on gap kind, dependency name and the `-be` token (measured on sixteen envelopes)

source: S112 — unblob SquashFS handler at tag 26.6.4 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — `SquashFSExtractor` lines 24-70 — as read 2026-10-26
source: S118 — unblob 26.6.4 symlink rewrite/removal — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/extractor.py — `is_recursive_link`/`fix_symlink` lines 42-90, `is_safe_path` lines 34-39, `report.py:133-139` (`MaliciousSymlinkRemoved`) — as read 2026-10-26
source: S119 — rea-agents 6.5.0 extraction-gap schema and unpublished-entry publication — package root `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` — `dist/domain/firmware/firmwareAnalysis.js:78-96` (gap `kind` enum), `dist/firmware/FirmwarePublication.js:12-24` (gap continuations), `:208-320` (gap construction and the `unpublished-entry` mapping) — as read 2026-10-26
verified-at: 2026-10-26
recheck: 180d — `grep -c 'is_avm = header.bytes_used == header.mkfs_time' "$(python3 -c 'import unblob,os;print(os.path.dirname(unblob.__file__))')/handlers/filesystem/squashfs.py"` -> 1 and `grep -c 'kind: "unpublished-entry"' <rea-agents>/dist/firmware/FirmwarePublication.js` -> 1 (both ran 2026-10-26)

**What was measured.** Sixteen REA 6.5.0 `extract-firmware` envelopes on SquashFS v4 inputs, read
through the feature set the round-39 triage interpreter uses — `H` = `normalized_result.chunks[].handler`
values starting with `squashfs`, `G` = `extraction_gaps[].kind`, `D` = union of
`extraction_gaps[].dependencies`, `BE` = `-be` token presence in any `diagnostics[].report.command`
that names sasquatch, `SR` = a `MaliciousSymlinkRemoved` diagnostic, `P` = `len(normalized_result.files)`.
Eight envelopes are the committed round-38 receipts (`corpus/evidence/round-38/c1/K{1..4}/{before,after}.json`,
bare `data` objects), two are the round-38 AVM-marker probe
(`.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/rea-k1-{avm,orig}.json`, full CLI envelopes), and two
were produced for this entry from development carriers in scratch (`dev-clean.sqsh` /
`dev-corrupt.sqsh`, both built from a fresh four-file tree with
`tools/round-37/gen-squashfs.py … --endian be --comp gzip`; the corrupt one has bytes 942-1342
overwritten with `0xff` while the superblock stays intact). LE rows come from
`corpus/evidence/round-36/c1/K{1..4}/before.json`, which the round-36 claim already froze.

| envelope | H | G | D | BE | SR | P | class |
|---|---|---|---|---|---|---|---|
| round-38 `K1/after` | `squashfs_v4_be` | none | none | n/a | yes | 5 | escaping-symlink-removed |
| round-38 `K2/after` | `squashfs_v4_be` | `unpublished-entry` | none | n/a | no | 3 | in-tree-symlink-metadata |
| round-38 `K3/after`, `K4/after` | `squashfs_v4_be` | none | none | n/a | no | 4 | clean |
| round-38 `K{1..4}/before` | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` | n/a | no | 0 | dep-missing-be |
| round-36 `K1/K2/before` | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | n/a | no | 0 | dep-missing-le |
| round-36 `K3/K4/before` | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | n/a | no | 2 | dep-missing-le |
| AVM probe `rea-k1-avm` | `squashfs_v4_be` | `extractor-failure` | none | no | no | 0 | avm-marker-be-dropped |
| AVM probe `rea-k1-orig` | `squashfs_v4_be` | none | none | n/a | yes | 5 | escaping-symlink-removed |
| dev `dev-clean` | `squashfs_v4_be` | none | none | n/a | no | 4 | clean |
| dev `dev-corrupt` | `squashfs_v4_be` | `extractor-failure` | none | yes | no | 0 | body-extractor-failure |

**Why `-be` and not the file count decides a failed extraction.** unblob 26.6.4 has no in-process
SquashFS reader. For big-endian v4 it runs `sasquatch-v4be`, and it appends `-be` only when
`header.bytes_used != header.mkfs_time` (S112, lines 41-54); the AVM-BE format stores the same value
in both fields (S114). So one damaged standard-BE image and one intact AVM-BE image both end as
`extractor-failure` with zero published files, and the only envelope field that separates them is the
argv the producer recorded: `no` (AVM marker dropped the flag, the image is fine, the error text reads
"different endianess") versus `yes` (right endianness, "File system corruption detected"). REA
publishes that argv in `diagnostics[].report.command` with `__typename__` = `ExtractCommandFailedReport`.
`extract-firmware` takes only offset/length/max-depth/max-output limits — it has no unblob-flag
passthrough — so the only way to force `-be` back is a `PATH` wrapper named `sasquatch-v4be`.

**Why the dependency name and not the handler decides a dependency miss.** Both BE and LE v4 report
`missing-extractor-dependency`, and `get_dependencies()` names both executables (S112, lines 68-69),
but the recorded gap lists only the executable the chosen extractor needed: `sasquatch-v4be` for BE,
`sasquatch` for LE. The `published files` cell is therefore not a dependency signal at all: the LE
before-arms on the AppImage carriers published 2 files each (the ELF prefix and the opaque
`…squashfs_v4_le` range), and a BE carrier wrapped the same way would do the same.

**Symlinks, both ways, from one run shape.** A symlink whose target resolves inside the extraction
root is kept: `fix_symlink` rewrites it relative and REA records one `unpublished-entry` gap
(`kind: symlink`) on every run that extracted (S118, S119). A symlink whose target escapes the root is
removed and reported as `MaliciousSymlinkRemoved`, and REA records no gap for it (S118 lines 79-90).
"No extraction gap" is therefore unreachable on any extracted image holding an in-tree symlink, and
gap-free is not the same as symlink-free.

**Status.** This entry backs the round-39 `## Queue-drain craft` triage table
(`skill-craft-block.md` in the round-39 wave-1 artifacts, landed into `SKILL.md`); the interpreter
reads that table, never this entry. The seven classes are those the round-39 C2 claim names, with
`body-extractor-failure` grounded on a development carrier rather than on a shipped one. Not claimed:
AVM-BE *bodies* (only the marker's argv effect), vendor-mangled images, `unknown-chunk-handler` /
`depth-limited` / `encrypted-chunk` envelopes (no row; they fall to `unclassified`), and any statement
about extracted programs. Source rows S118 and S119 are new; the highest number used in `corpus/SOURCES.md`
before this round is S117 (`corpus/SOURCES.md:123`), so the integrator must land those two rows with
this entry or renumber consistently.
