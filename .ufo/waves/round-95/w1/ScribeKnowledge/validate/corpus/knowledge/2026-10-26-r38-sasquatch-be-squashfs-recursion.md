# Standard big-endian SquashFS v4 through REA: needs `sasquatch-v4be`; in-tree symlinks stay gaps (measured, not promoted)

source: S112 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — `SquashFSExtractor` (lines 24-70) — as read 2026-10-26
source: S113 — https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs/squashfs_v4_be/__input__ — fixture LFS oids — as read 2026-10-26
source: S114 — https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt — AVM-BE marker `mkfs_time == bytes_used` — as read 2026-10-26
verified-at: 2026-10-26
recheck: 180d — `curl -s https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py | grep -c 'V4BE_EXECUTABLE = "sasquatch-v4be"'` -> 1 (ran 2026-10-26)

**What was measured.** REA `extract-firmware` (rea-agents 6.5.0, unblob 26.6.4) on four
big-endian SquashFS v4 carriers: K1/K2 are synthetic gzip images built by
`tools/round-37/gen-squashfs.py`, and K3/K4 are the unblob 26.6.4 `squashfs_v4_be`
integration fixtures (S113). Every run names the `squashfs_v4_be` handler.

| arm | K1 | K2 | K3 | K4 |
|---|---|---|---|---|
| before: `sasquatch-v4be` unreachable (`$HOME/.local/bin` off PATH) | 0/5 files, gap `missing-extractor-dependency` [`sasquatch-v4be`] | 0/3, same gap | 0/4, same gap | 0/4, same gap |
| after: `sasquatch-v4be` 4.5.1 reachable | 5/5 oracle files, 0 gaps | 3/3 oracle files, 1 gap `unpublished-entry` (`var/lib/run-link`) | 4/4, 0 gaps | 4/4, 0 gaps |

Receipts: `corpus/evidence/round-38/c1/K{1..4}/{before,after}.json` (round-38 attempt 1;
committed round 38). Independent check: `sasquatch-v4be -be` run directly reproduces 16/16
oracle regular files. 7-Zip 26.04 refuses all four images ("Cannot open the file as archive");
that refusal is recorded as a rejected row (S115), not as a source.

**Why the dependency is structural.** unblob 26.6.4 has no in-process SquashFS reader. For
big-endian v4 its `SquashFSExtractor` picks the executable `sasquatch-v4be` and builds
`sasquatch-v4be [-be] -no-exit-code -f -d {outdir} {inpath}`. It drops `-be` when
`header.bytes_used == header.mkfs_time`, which is the AVM-BE marker (S114).
`get_dependencies()` returns both `sasquatch` and `sasquatch-v4be` (S112, lines 24-70). The
before-arm gap is therefore a property of the PATH the unblob child process sees, not of the
image. Round 38's first freeze said the gap "does not reproduce" because its probes filtered
PATH entries by directory name and never removed `~/.local/bin`.

**Symlinks.** Two symlink outcomes came out of one REA run shape:

- K1's `link-to-hello -> ../hello.txt` points outside the extraction root. unblob removes it
  and logs `MaliciousSymlinkRemoved`, so no gap is recorded.
- K2's `var/lib/run-link -> ../../a/run.sh` stays inside the tree. REA keeps it as metadata
  and records one `unpublished-entry` gap on every run in which `sasquatch-v4be` extracts the
  image (the before-arm extracts nothing, so it records only the dependency gap).

So "no extraction gap" is unreachable on any extracted carrier that holds a symlink whose target
resolves inside the extraction tree (K2). A symlink that escapes the tree is removed instead (K1),
which is why K1 is gap-free although it holds a symlink. This matches the round-36 LE entry
(`unpublished-entry` for symlinks).

**Status.** This is not a Core promotion. Round 38's coverage claim R38-C1 required "no
extraction gap" on all four carriers under its first-freeze counter, and K2 fails it, so the
claim is an honest stop (3/4 carriers). Standard BE v4 stays on the PROVINCE Frontier until a
claim that states the symlink behaviour up front verifies. AVM-BE and vendor-mangled images were
not measured. Nothing here is claimed about the extracted programs.
