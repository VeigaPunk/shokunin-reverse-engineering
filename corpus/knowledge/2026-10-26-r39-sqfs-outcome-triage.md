# SquashFS `extract-firmware` outcome triage: eight labels separate on handler, gap kind, dependency name, the `-be` token and the symlink-removal report

source: S112 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — `SquashFSExtractor` lines 24-70 (AVM branch 44-50, `get_dependencies` 68-69) — as read 2026-10-26
source: S118 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/extractor.py — `fix_symlink` lines 50-92 — as read 2026-10-26
source: S119 — https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz — `dist/domain/firmware/firmwareAnalysis.js:84-101`, `dist/firmware/FirmwarePublication.js:68-75,241,286-308`, `dist/firmware/FirmwareReports.js:254-255,284` — as read 2026-10-26
source: S120 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/report.py — `report.py:91-98,118-122,133-138`, `extractors/command.py:59-77,101-102` — as read 2026-10-26
source: S121 — https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/squashfs-tools/unsquashfs.c — `-be` handling and `debian/rules` lines 15-18 (`-DFIX_BE` build) — as read 2026-10-26
verified-at: 2026-10-26
recheck: 180d — `grep -c 'is_avm = header.bytes_used == header.mkfs_time' ~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py` -> 1 (ran 2026-10-26)

**Features.** The round-39 triage interpreter (`tools/round-39/sqfs-triage.py`) reads six fields of an
REA 6.5.0 `extract-firmware` envelope: `H`, the chunk handlers that start with `squashfs`; `G`, the set of
`extraction_gaps[].kind`; `D`, the union of the gaps' `dependencies`; `BE`, whether a recorded sasquatch
command (`diagnostics[].report.command`) carries a standalone `-be` token (`n/a` when no command is
recorded, which is every successful run); `SR`, whether a `MaliciousSymlinkRemoved` report is present;
and `P`, the published file count. REA copies unblob's reports verbatim into `diagnostics[].report`
(S119 `FirmwareReports.js:254-255`); `command` is a field of unblob's `ExtractCommandFailedReport`,
created only when the extractor exits non-zero (S120 `report.py:91-98`, `command.py:59-68`).

**Dependency misses name the endianness.** Both v4 handlers report `missing-extractor-dependency`
when the extractor binary is not on the unblob child's `PATH`, but the gap names only the executable
the chosen `Command` needed: `Command.get_dependencies()` returns `[self._executable]` (S120
`command.py:101-102`), so big-endian names `sasquatch-v4be` and little-endian names `sasquatch`,
although the extractor's own `get_dependencies` lists both (S112 lines 68-69). A dependency row
suppresses the generic failure row for the same chunk (S119 `FirmwarePublication.js:241`), so a miss
yields one gap, never two. Measured: round-38 `corpus/evidence/round-38/c1/K1/before.json` (BE) and
the wave-1 development runs `.ufo/waves/round-39/w1/R39C2ReconDep.md` (BE and LE).

**AVM marker versus image damage.** For big-endian v4 unblob appends `-be` only when
`header.bytes_used != header.mkfs_time` (S112 lines 44-50). The `-DFIX_BE` build of `sasquatch-v4be`
reads only big-endian v4 when told so (S121), so on a standard-BE body whose `mkfs_time` happens to
equal `bytes_used` the extractor runs without `-be`, prints "suggests a SquashFS image of a different
endianess" and exits 1. Damage to an intact-header image (a zeroed id-table block, an `s_minor` other
than 0) also ends as `extractor-failure` with zero files, but the recorded argv carries `-be`. The two
outcomes share `G`, `D` and `P`; only `BE` separates them. REA's `extract-firmware` has no unblob-flag
passthrough, so the only fix for the marker case is a `PATH` wrapper named `sasquatch-v4be` that
appends `-be`. Measured: `.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/rea-k1-avm.json` and
`.ufo/waves/round-39/w1/R39C2ReconMarker.md` (marker, gzip and xz), `.ufo/waves/round-39/w1/R39C2ReconCorrupt.md`
(id-table zeroing on four trees), `.ufo/waves/round-39/w1/R39C2HeldoutGen.md` section 4 (`s_minor` 5).

**Symlinks.** unblob rewrites a symlink whose target stays inside the per-chunk extraction root and
removes one that escapes it, reporting `MaliciousSymlinkRemoved` (S118 `extractor.py:79-91`); absolute
targets are re-rooted under the extraction directory and kept, not removed (S118 lines 73-77). REA then
publishes only regular files and records each kept symlink as one `unpublished-entry` gap with
`unpublished_entries[].kind` `symlink` (S119 `FirmwarePublication.js:68-75,301-308`); a removed link
leaves no gap. So `SR` = yes with no gap means an escaping link was dropped, and `G` = `unpublished-entry`
alone means kept in-tree links. An image holding both kinds shows both signals; the table's first
match then labels it `escaping-symlink-removed` (`.ufo/waves/round-39/w1/R39C2LabMixed.md`).

**No SquashFS chunk.** A truncated image, a `bytes_used` beyond the file or an `s_major` other than 4
makes unblob's finder drop the chunk silently: REA reports no squashfs chunk, no gap and no file, with
`coverage` `complete` (`.ufo/waves/round-39/w1/R39C2ReconTruncate.md`). An empty envelope of this shape is
not an empty filesystem.

**Status and limits.** This entry backs the round-39 triage table in `SKILL.md` `## Queue-drain craft`
(rule block "SquashFS extract-firmware outcome triage (round 39)"); the interpreter reads the table,
never this entry. Development evidence only: the claim R39-C2 is scored on a held-out set generated
after the freeze. Not covered: AVM-BE bodies (LE block lengths, XZ), vendor-mangled images,
`unknown-chunk-handler`, `encrypted-chunk` and `depth-limited` gaps (they fall to `unclassified`),
little-endian body damage (no row), and anything about extracted programs.
