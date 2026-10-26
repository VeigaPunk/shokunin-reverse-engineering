# Standard big-endian SquashFS v4 through REA: six frozen carriers, symlink rule stated before data

source: {{SID}} — unblob 26.6.4 `extractor.py:50-94` — `fix_symlink` removes a symlink whose target is outside the extraction root and reports `MaliciousSymlinkRemoved`; safe symlinks are rewritten and kept — as read 2026-10-26
source: {{SID2}} — rea-agents 6.5.0 `dist/firmware/FirmwarePublication.js:302-307` — a retained non-regular entry is recorded as an `unpublished-entry` extraction gap — as read 2026-10-26
source: S112 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — `SquashFSExtractor` selects `sasquatch-v4be` for big-endian v4 — as read 2026-10-26
source: S113 — https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs/squashfs_v4_be/__input__ — fixture LFS oids for K3/K4 — as read 2026-10-26
source: S114 — https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt — AVM-BE marker `mkfs_time == bytes_used` — as read 2026-10-26

verified-at: 2026-10-26
recheck: 180d — `python3 -I -B tools/round-39/c1-counter.py --root . --rev HEAD --freeze HEAD` green

**What was measured.** REA `extract-firmware` (rea-agents 6.5.0, unblob 26.6.4,
`sasquatch-v4be` 4.5.1 reachable on the child PATH) on the six frozen standard
big-endian SquashFS v4 carriers K1–K6. Every run names the `squashfs_v4_be`
handler and fails no chunk; every regular file of the frozen oracle is
published with the same relative-path suffix and sha256.

**Symlink rule, stated before data.** A symlink whose target resolves inside
the extraction root is kept as metadata and recorded as exactly one
`unpublished-entry` gap (S…REA publication). A symlink whose target escapes the
root is removed by unblob (`MaliciousSymlinkRemoved`) and recorded as no gap
(S…unblob sanitiser). This rule, not the image, explains the gap set on every
carrier; no other gap kind appears.

**Status.** Promoted to Core under R39-C1; AVM-BE bodies, vendor-mangled images
and anything about the extracted programs are not claimed.
