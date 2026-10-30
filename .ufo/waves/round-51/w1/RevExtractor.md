# RevExtractor — round 51 wave 1 (reverse-engineering the `extract-firmware` disposition path)
Seat: RevExtractor (leaf, read-only source analysis). Milestone: r51 w1 build, device-accounting law grounding.
Verdict: **the law's "no record by construction" clause holds only under unprivileged extraction, and the reason is upstream of REA (sasquatch `mknod` under `-no-exit-code`), not a REA scope or disk-walk gap.** Two premises (sasquatch EPERM behaviour, non-fatal failure) are string-level inferences, not runtime-verified.
Full annotated call path with file:line evidence: `.ufo/waves/round-51/w1/RevExtractor/path.md`.

## Answers (file:line)

1. **Where is `unpublished_entries` computed, and from what comparison?**
   `src dist/firmware/FirmwarePublication.js:66-75` (bundle `dist/cli-runtime/cli.js:14102-14111`): every disk-walk entry with `kind !== "file"` is pushed. The "staged inventory" is the disk walk (`src dist/firmware/FirmwareFiles.js:122-190`, called at `FirmwareProvider.js:260` / `bundle:15142`) after unblob exits. There is no comparison against a handler-declared set, the report, or the oracle. The only cross-check is one-directional: reported regular files must exist on disk (`FirmwarePublication.js:58-64`).

2. **Why does a char-device oracle entry produce neither a gap nor a removal?**
   - The disk walk **does** stat non-regular files: `lstat` on every name (`FirmwareFiles.js:158-163`; `bundle:14020-14023`), kind `"special"` for char/block/fifo/socket (`FirmwareFiles.js:179-183`; `bundle:14035`). A node on disk would yield an `unpublished-entry` gap (`bundle:14279-14286`). The hypothesis "disk walk doesn't stat non-regular files" is false.
   - The list is not scoped to handler-staged entries, because REA has no handler-side staging. The squashfs handler hands the image to `sasquatch -le -no-exit-code -f -d <outdir> <image>` (unblob `handlers/filesystem/squashfs.py:53-64`; `-no-exit-code` at line 58). A char device needs `mknod`, which an unprivileged extractor cannot perform. The failure goes to sasquatch stderr; with exit 0, unblob's `Command.extract` reads stderr only on non-zero exit and otherwise discards it (`unblob extractors/command.py:50-59`). So no report, no node on disk, no StatReport, no diagnostic, no gap.
   - Removal: REA has no removal concept. The only removal it can observe is unblob's `MaliciousSymlinkRemoved` (`unblob extractor.py:58-65`, `:79-87`), which is symlink-only (the `is_symlink()` branch at `:102-104`). It reaches the envelope only as a `diagnostics` row (`src FirmwareReports.js:254-255`; `bundle:14757`). The lane's `removed.kinds=["symlink"]` matches this exactly. `removed.silent["char-device"]` has no REA source (lane-side bookkeeping).

3. **Does any code path emit a diagnostic when a non-regular entry is skipped?**
   No. Enumerated: REA publication emits only the `unpublished-entry` gap, which is a record that exists only when the entry is on disk (`FirmwarePublication.js:68-75`, `:110`). REA ignores a non-file StatReport silently (`bundle:14742-14751`). unblob `processing.py:286-290` logs "Ignoring special file" at debug level only. unblob's removal diagnostic is symlink-only. sasquatch's stderr for a failed device creation is discarded on exit 0 (`squashfs.py:58`; `command.py:55`, `:59`).

## Grounding for the law's "no record by construction" clause

- P1 (REA): non-regular records come only from the post-run disk walk (`FirmwarePublication.js:66-75`; `FirmwareFiles.js:158-183`). Absent node → no record.
- P2 (unblob): device tasks are reported only if the walk reaches them (`processing.py:270`, `:286-290`).
- P3 (unblob): the only removal diagnostic is `MaliciousSymlinkRemoved`, symlink-only (`extractor.py:58-65`, `:79-87`).
- P4 (unblob): `-no-exit-code` plus exit-0 stderr discard (`squashfs.py:58`; `command.py:55`, `:59`).
- Not established (no probe run; out of this seat's named scope): N1, that unprivileged sasquatch fails every `mknod` for the carriers' device nodes and leaves none on disk ([INFERENCE] from binary strings: `create_inode: failed to create %s device %s, because %s`, plus the `-no-exit-code` / `FATAL ERROR` variant strings); N2, that the failure is non-fatal ([INFERENCE] from the non-fatal message form).

## Divergences from the plan text

- The plan's "REA 6.5.0" is confirmed (`package.json` at the rea-agents package root, version 6.5.0). unblob pin 26.6.4 (`FirmwareRelease.js:11-14`) matches the installed `unblob` v26.6.4, so the unblob source read is the pinned producer's.
- The plan says the producer "materialises regular files and directories". Directories are not emitted as entries at all (`FirmwareFiles.js:164-170`), so this is accurate but incomplete. Directories only drive recursion.
- The plan says "re-creates symlinks". unblob's `fix_symlink` re-creates them in-tree (`extractor.py:89-91`) or removes them (`:58-65`, `:79-87`). Both are accurate.
- REA does not pin or name sasquatch (`grep -rl sasquatch dist/` → 0 hits). The sasquatch binary is a host PATH artifact (`~/.local/bin/sasquatch`). Its provenance is not recorded by REA, so a receipt that names only the unblob version does not pin the device-node behaviour.
- Oracle census (read-only `awk` on `tools/round-50/oracle/*.nonregular.tsv`) matches the plan: Cable c6430/c6490 carry 1 char-device (`dev/led 247:0`); FRITZ!Box g7581/g7582 carry 13 (`dev/led` + twelve others). The round-50 rule's `required["char-device"]: true` and `removed.silent["char-device"]: ["247:0"]` are the two premises the law removes.

## Attacks for the L1 freeze / falsify wave (ranked)

- **A1 (privilege dependence, highest).** If a carrier run ever has CAP_MKNOD or runs as root, device nodes appear on disk. REA then emits `unpublished-entry` gaps for them (`bundle:14104-14111`, `:14279-14286`) and the law's "no gap" prediction fails. The rule must name the privilege predicate (receipt records uid/capabilities) or accept both arms with a stated reason. Decider: a synthetic squashfs with a `dev` pseudo-entry, extracted as non-root and as root (NOT run).
- **A2 (partial coverage).** Any unpublished entry makes `coverage: "partial"` (`bundle:14137`). A device-only run is partial, so a Core-coverage claim cannot rest on it unless the counter accepts `partial`.
- **A3 (unreported regular files).** Regular files on disk with no report entry are published with no check (`FirmwarePublication.js:77-98`). REA will not detect a missing report; only the oracle counter does.
- **A4 (vocabulary).** A rule that lists `char-device` under `removed` has no REA source. Only `symlink` may appear under `removed.kinds`.
- **A5 (stderr).** A future unblob that surfaces sasquatch stderr on exit 0 would turn the device-node disposition into a diagnostic. Pin unblob 26.6.4 and record the sasquatch binary's identity (sha256 + version) in the receipt.
- **A6 (MCP twin).** The MCP bundle `dist/mcp/main-kBXHZ8S5.js:51235-51236` carries the same publication logic. Any harness that routes through MCP inherits the same answers.

## Recommended probes (not run; for the L1 or a labrat, not this seat)

- P-A: synthetic `mksquashfs` image with one char device (pseudo-file), run `sasquatch -le -no-exit-code -f -d <out> <img>` as non-root and as root; record exit code, stderr sha256, and presence of the node. This decides N1 and N2 and A1.
- P-B: the same image through `unblob --report ... --extract-dir ...` as non-root; confirm the report carries no device StatReport when the node is absent and does when present.

## Tooling and changes

- No tool installed, upgraded or removed. No pacman use. No git mutation. No REA invocation. No unblob or sasquatch execution (`uv tool list`, `which`, `strings`, `sha256sum` only).
- Scratch `/fast/scratch/hyaku/kaidoku-r51/w1-RevExtractor` was created empty and removed before yield.
- Writes: only `.ufo/waves/round-51/w1/RevExtractor/path.md` and this report.

## Confidence

- High: §1-§6 call path and line citations (read directly; bundle and source agree at the cited points); the oracle census; the REA/unblob flags and report handling.
- Medium: "sasquatch creates no device node unprivileged" (string evidence, no runtime).
- Not verified: sasquatch's exact stderr text and whether it is fatal under `-no-exit-code` (N1, N2).
