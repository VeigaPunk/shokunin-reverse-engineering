# RevExtractor — annotated call path: `extract-firmware` → `unpublished_entries` / gaps / removal diagnostics

Scope: read-only source analysis. Nothing executed from rea-agents; no REA run; no sasquatch/unblob probe.
Producer pin: rea-agents 6.5.0 (`node_modules/rea-agents/package.json`), `FIRMWARE_RELEASES.unblob` = 26.6.4 (`dist/firmware/FirmwareRelease.js:8-12`). Installed `unblob` on this host is v26.6.4 (`uv tool list`), so the unblob source read below is the pinned producer's source.
Citations: `src` = `dist/<file>` source module; `bundle` = `dist/cli-runtime/cli.js` (the CLI runs this bundle; the MCP bundle `dist/mcp/main-kBXHZ8S5.js` carries the same logic at 51235-51236 and 51236 `unpublished_entries: unpublished`).
Root of rea paths: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/`.
unblob root: `/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/`.

## 1. Verb → provider

| step | location | what happens |
|---|---|---|
| verb name | `dist/cliCommandNames.js:68` | `extractFirmware: "extract-firmware"` |
| CLI registration | `bundle:15273-15292` | `cli.command(CLI_COMMANDS.extractFirmware, …)` → `execute(…, "extract_firmware", { path, output_directory, range?, max_depth, max_output_bytes, max_output_files })` |
| provider entry | `src firmware/FirmwareProvider.js:140-` / `bundle:15040-15190` | `engineName = "unblob"` for `extract_firmware` (`FirmwareProvider.js:141`); private root `PrivateRuntimeRoot.create` (`:151`); `snapshotFirmware` (`:153`, `src FirmwareFiles.js:33`) |
| producer command | `src FirmwareProvider.js:226-240`; `bundle:15110-15124` | `unblob --process-num 1 --depth <max_depth> --randomness-depth 0 --report <report.json> --log <unblob.log> --extract-dir <root>/extracted <inputPath>` |
| exit handling | `bundle:15141` | `processRun.exit_code === 1 && normalized.diagnostics.length === 0` → `AnalysisOutputError("Unblob failed without a reported extraction diagnostic")` |

## 2. unblob → squashfs handler → sasquatch (the device-node decision point)

| step | location | what happens |
|---|---|---|
| handler class | unblob `handlers/filesystem/squashfs.py:25-30` | `SquashFSExtractor.EXECUTABLE = "sasquatch"`, `V4BE_EXECUTABLE = "sasquatch-v4be"` |
| LE endianness arg | `squashfs.py:53-54` (`case Endian.LITTLE, _: commands_args.append("-le")`) | little-endian v4 AVM/LE → `-le` |
| **flags** | `squashfs.py:56-64` | `"-no-exit-code", "-f", "-d", "{outdir}", "{inpath}"` — line 58 is `-no-exit-code` |
| LE v4 handler | `squashfs.py:454` (`class SquashFSv4LEHandler`, NAME `squashfs_v4_le`) | the handler whose extractor is the default LE path (`-le`) |
| process run | unblob `extractors/command.py:50-58` | `subprocess.run(cmd, stdout=…, stderr=subprocess.PIPE, …)`; stderr is captured |
| failure record | `command.py:59-70` | ONLY `if res.returncode != 0` → `ExtractCommandFailedReport(command, stdout, stderr, exit_code)` → `ExtractError`. On exit 0 the captured stderr is **discarded** (no branch reads it). |
| FileNotFound | `command.py:69-74` | `ExtractorDependencyNotFoundReport` (only if the binary is absent) |

`-no-exit-code` + the exit-0-discards-stderr branch means a sasquatch error that does not change the exit code produces no unblob report at all. Binary evidence (read-only `strings` on `~/.local/bin/sasquatch`, no execution): the strings `create_inode: failed to create %s device %s, because %s` (non-fatal form) and `FATAL ERROR: create_inode: failed to create %s device %s, because %s` (fatal form), plus `FATAL ERROR: Both -strict-errors and -no-exit-code should not be set.  All errors are fatal`. [INFERENCE] With `-no-exit-code` (and without `-strict-errors`) a `mknod` failure is the non-fatal `create_inode … failed to create … device` message on stderr, exit 0. **Not runtime-verified** (no probe was in this seat's named scope).

## 3. unblob post-extraction and child tasks

| step | location | what happens |
|---|---|---|
| post-extract fix | unblob `processing.py:654` (chunk path) and `:678` → `extractor.py:95-113` `fix_extracted_directory` | `fix_permission(path)` on every entry; `if path.is_symlink(): fix_symlink(...)`; `if path.is_dir(): recurse`. **No branch** for char/block/fifo/socket. |
| symlink refusal | `extractor.py:50-92` `fix_symlink` | loop or traversal → `MaliciousSymlinkRemoved(link, target)` added to the task result, then `path.unlink()` (`:58-65`, `:79-87`). Symlink-only. Surfaces in the REA report as a task report. |
| child task for extracted dir | `processing.py:682-690` `self.result.add_subtask(Task(path=extract_dir, depth+1))` | the extracted tree is re-processed as a directory task |
| child walk | `processing.py:462-470` `_iterate_directory` (`path.iterdir()` → subtask per entry) | every entry, including device nodes, becomes a Task |
| per-task stat | `processing.py:270` `stat_report = StatReport.from_path(task.path); result.add_report(stat_report)` | a `StatReport` (is_file/is_link/is_dir) is recorded **before** the skip |
| special-file skip | `processing.py:286-290` `if not stat_report.is_file: log.debug("Ignoring special file (link, chrdev, blkdev, fifo, socket, door)."); return` | **debug-level log only**. No report, no diagnostic. |

Consequence: if a device node exists on disk after sasquatch, unblob's report *does* contain a `StatReport` (is_file false) for it. Absent on disk → no StatReport, no entry, no record anywhere.

## 4. REA normalizes the unblob report

| step | location | what happens |
|---|---|---|
| report read | `src FirmwareReports.js` (`normalizeUnblobReport`, `:143-`); `bundle:14673-` | JSON report → normalized `files`, `sizes`, `chunks`, `diagnostics`, `failed_extraction_stages`, … |
| StatReport | `src FirmwareReports.js:231`; `bundle:14742-14751` | `metadata = record.reports.find(StatReport)`; `files.set(path, …)` **only when** `parsedStat.is_file && !parsedStat.is_link` (`bundle:14751`). A `StatReport` for a device is accepted without error and is simply not a file. The only StatReport `is_file` check is for `$input` (`bundle:14747`). |
| known report set | `src FirmwareReports.js:65-74` | `StatReport, HashReport, FileMagicReport, RandomnessReport, ChunkReport, UnknownChunkReport, CarveDirectoryReport, MultiFileReport` |
| unknown reports → diagnostics | `src FirmwareReports.js:254-255`; `bundle:14757` | `if (!known.has(item.__typename__)) diagnostics.push({input_path, report: item})`. **This is the only path by which `MaliciousSymlinkRemoved` reaches the REA envelope** (as a `diagnostics` row). |
| extractor execution error | `src FirmwareReports.js:257-` | `ExtractorExecutionErrorReport` → `failed_extraction_stages` (extractor-failure gap family) |

REA has no `removed` concept. The string `removed` appears in the REA dist only as `MaliciousSymlinkRemoved` (diagnostic) and unrelated code. The lane's `removed.diagnostic = MaliciousSymlinkRemoved`, `removed.kinds = ["symlink"]` (`tools/round-50/gap-rule.json`) matches this exactly: the only removal REA can observe is a symlink refused by unblob.

## 5. The disk walk — the "staged inventory"

| step | location | what happens |
|---|---|---|
| call | `src FirmwareProvider.js:260`; `bundle:15142` | `entries = await inventoryFirmwareOutput(outputRoot, max_output_bytes, max_output_files, operation, signal)` — run AFTER unblob exits, over the sasquatch/unblob output directory |
| definition | `src firmware/FirmwareFiles.js:122-190`; `bundle:13992-14041` | iterative `opendir` from root; names sorted |
| **stat** | `src FirmwareFiles.js:158-163`; `bundle:14020-14023` | `lstat(path)` for **every** name, including device nodes, fifos, sockets (not only regular files) |
| directories | `src FirmwareFiles.js:164-170`; `bundle:14025-14027` | `isDirectory()` → pushed for recursion (not emitted as an entry) |
| budgets | `src FirmwareFiles.js:153-172` | `Staging entry budget exceeded`; `Staging byte budget exceeded` (regular-file bytes only) |
| kind | `src FirmwareFiles.js:179-183`; `bundle:14035` | `kind: isSymbolicLink() ? "symlink" : isFile() ? "file" : "special"`; `linkTarget: readlink` for symlinks |

Answer to the "does the disk walk not stat non-regular files?" question: **it does**. `lstat` runs on every entry and anything that is not a dir, symlink or regular file is emitted with `kind: "special"`.

## 6. Publication — where `unpublished_entries` is computed

`publishFirmwareExtraction` — `src firmware/FirmwarePublication.js:54-149`; bundle `cli-runtime/cli.js:14093-14172`.

1. `FirmwarePublication.js:58-64` / `bundle:14097-14100`: **one-directional cross-check**: every reported regular file `$output/<path>` must be among the disk `kind === "file"` entries; else throw `Reported regular file is absent from materialized output`. There is **no reverse check** (no check that a reported non-file, or a disk non-regular entry, is accounted for by the report).
2. `FirmwarePublication.js:66-75` / `bundle:14102-14111`: **`unpublished_entries` is computed here**: `for (const entry of context.entries) if (entry.kind !== "file") unpublished.push({ relative_path, kind, link_target }); continue;`. The comparison is therefore **not** "staged inventory vs disk walk" — the staged inventory *is* the disk walk, and the only selection is `kind !== "file"`. No comparison against the oracle, the handler's declared outputs, or the report's unpublished set.
3. `FirmwarePublication.js:77-98` / `bundle:14113-14131`: regular files: `hashFirmwareFile`; cross-check reported sha256 and size (`:80-85`, throws `Extracted bytes disagree with provider report`); `tree.write`; `files.push`. A regular file on disk with no report entry is published without error (no check).
4. `FirmwarePublication.js:99-112` / `bundle:14133-14146`: `coverage: unpublished.length > 0 ? "partial" : context.normalized.coverage`; `unpublished_entries: unpublished`; `...extractionGaps(unpublished, files, normalized, maxDepth)`.
5. `extractionGaps`, `src FirmwarePublication.js:208-322` / `bundle:14210-14296`:
   - `unpublished.map(entry => ({ kind: "unpublished-entry", input_path: "$output/" + entry.relative_path, …, relative_path, continuation_id: continuation(GAP_CONTINUATIONS["unpublished-entry"]) }))` — `bundle:14279-14286`.
   - `GAP_CONTINUATIONS["unpublished-entry"]` = "The entry is retained as metadata; only regular files are published, without executable permission bits." (`src FirmwarePublication.js:18`).
   - gaps sorted by `gapSortKey` (`bundle:14288`).
6. Not emitted anywhere: a diagnostic for a non-regular entry. The unpublished row *is* the record, and it exists only when the entry is on disk.

## 7. Answers to the three questions

**(1) Where is `unpublished_entries` computed, and from what comparison?**
`src FirmwarePublication.js:66-75` (`bundle:14102-14111`): the set of disk-walk entries with `kind !== "file"`. The disk walk (`src FirmwareFiles.js:122-190`) is the only inventory; there is no staged-set comparison. The unpublished row and its `unpublished-entry` gap (`bundle:14279-14286`) are the only disposition a non-regular entry can receive.

**(2) Why does a char-device oracle entry produce neither a gap nor a removal?**
Both the scope and the disk-walk answers are "it depends on the disk", and the disk is empty of device nodes by the sasquatch step (§2), not by the REA scope:
- The disk walk is **not** scoped to handler-staged entries and **does** stat non-regular files (`FirmwareFiles.js:158-163`, `:179-183`). A device node that exists under `outputRoot` *would* yield `kind: "special"` → unpublished row → `unpublished-entry` gap (`bundle:14104-14111`, `:14279-14286`). The mental model "the disk walk simply doesn't stat non-regular files" is false.
- "The squashfs handler stages no device nodes" is also not the mechanism REA sees. REA has no handler-side staging. unblob's squashfs handler hands the whole image to `sasquatch -le -no-exit-code -f -d <outdir> <image>` (`unblob squashfs.py:53-64`). Creating a char device is a `mknod` that an unprivileged process cannot perform; the failure is a sasquatch stderr line under exit 0 ([INFERENCE]: binary strings only, not runtime-probed), which unblob discards (`command.py:55`, `:59`), so no report is produced.
- A device that was never created is never in the disk walk, never a StatReport, and never a diagnostic. So the device-node "no record" is **by construction only under unprivileged extraction**. Under root/CAP_MKNOD sasquatch would create the node, and REA would emit an `unpublished-entry` gap for it (§3, §5, §6). See attack A1 below.
- The removal side: a char device has no removal path at all. The only removal REA can observe is `MaliciousSymlinkRemoved` (unblob `extractor.py:58-65`, `:79-87`, symlink-only, `:102-104` branch), which reaches REA as a `diagnostics` row (`src FirmwareReports.js:254-255`).

**(3) Does any code path emit a diagnostic when a non-regular entry is skipped?**
No. Enumerated:
- REA publication (`FirmwarePublication.js:68-75`): skips non-files silently, but emits the `unpublished-entry` gap (that is a record, not a diagnostic). Only exists when the entry is on disk.
- REA StatReport handling (`FirmwareReports.js:231`, `bundle:14747-14751`): a non-file StatReport is ignored, no diagnostic.
- unblob `processing.py:286-290`: `log.debug("Ignoring special file …")` — debug-level, not in the report.
- unblob `extractor.py:50-113`: `MaliciousSymlinkRemoved` for symlinks only; no device analogue.
- sasquatch: stderr line for a failed device creation; discarded on exit 0 (`command.py:55`, `:59`) under `-no-exit-code` (`squashfs.py:58`).
So a silently skipped device node has **no diagnostic on any path**, and `unpublished_entries` is the only record a non-regular entry can have.

## 8. Grounding for the law's "no record by construction" clause

Premises the law can cite (all from this file):
- P1: REA records non-regular entries only from the post-run disk walk (`FirmwarePublication.js:66-75`; `FirmwareFiles.js:158-183`). An absent device node → no record.
- P2: unblob's report lists non-file tasks only for entries it walks as tasks (`processing.py:270`, `:286-290`), and the walk sees device nodes only if they exist.
- P3: the only diagnostic a removal can produce is `MaliciousSymlinkRemoved` (`extractor.py:58-65`, `:79-87`) and it is symlink-only.
- P4: `sasquatch … -no-exit-code` exit 0 discards stderr (`squashfs.py:58`; `command.py:55`, `:59`).

Premise NOT established here (needs a probe or labrat, not run):
- N1: that sasquatch, run as an unprivileged user, fails `mknod` for every char device in the carriers' squashfs and leaves no node on disk. Binary strings point that way ([INFERENCE]).
- N2: that the failure is non-fatal (the squashfs continues extracting other entries). [INFERENCE] from the non-fatal message string and the `-no-exit-code` flag.

## 9. Attacks this evidence yields (for the L1 freeze / falsify wave)

- **A1 (privilege dependence).** If `c1-run.sh` ever runs the extraction with CAP_MKNOD or as root, nodes appear on disk and REA emits `unpublished-entry` gaps for them. The law's "no record" clause and `required.char-device=false` then predict *no gap*, which fails. The rule must either name the privilege predicate (receipt records uid / capability set) or accept both arms with a stated reason. A pre-freeze probe with a synthetic squashfs carrying a `dev` node, run as `id -u` non-zero and as root, would decide it. NOT run.
- **A2 (partial-coverage flag).** Whenever `unpublished.length > 0`, `coverage` becomes `"partial"` (`bundle:14137`). A device-node-only run is therefore partial. The law should not mint a Core-coverage claim from a `partial` receipt unless the rule accepts `partial`. Check the counter's `coverage` expectation.
- **A3 (regular files without reports).** Regular files on disk with no report entry are published with no check (`FirmwarePublication.js:77-98`). The oracle counter must be the sole arbiter of "every frozen regular file published"; REA will not catch a missing report for a regular file.
- **A4 (`removed` vocabulary).** `removed.kinds=["symlink"]` is correct for REA; a rule that lists `char-device` under `removed` has no REA source. `removed.silent["char-device"]` is lane-side bookkeeping, not REA output.
- **A5 (stderr discard).** A future unblob that reads sasquatch stderr on exit 0 would change P4 and would make the device-node disposition a diagnostic. The law should pin unblob 26.6.4 (`FirmwareRelease.js:11-14`) and the sasquatch build (host binary, `~/.local/bin/sasquatch`, dated Oct 26; REA does not pin sasquatch — `grep -rl sasquatch` over `dist/` returns 0).

## 10. Oracle corroboration (lane tables, read-only)

`tools/round-50/oracle/<id>.nonregular.tsv` non-regular census (`awk` count of column 2):
- c6430: char-device 1 (`dev/led 247:0`), dir 255, symlink 568
- c6490: char-device 1 (`dev/led 247:0`), dir 300, symlink 613
- g7581: char-device 13 (`dev/led 247:0`, `dev/pts/0-7 136:0-7`, `dev/tiatm 230:0`, `dev/ttyp0-2 3:0-2`), dir 349, symlink 639
- g7582: identical to g7581

These agree with the R51-C1 plan text. The round-50 `gap-rule.json` has `required["char-device"]: true` (the premise the law removes) and `removed.silent["char-device"] = ["247:0"]` (the detail-level allowance the law replaces).

## 11. Hash receipts (16-hex prefixes, `sha256sum`, 2026-10-30T04:58:50Z)

- `dist/cli-runtime/cli.js` 168cd322a29c9bae
- `dist/firmware/FirmwarePublication.js` bb4f3246bee70a5b
- `dist/firmware/FirmwareFiles.js` f6934b7bd71208d8
- `dist/firmware/FirmwareReports.js` 6885966b78451b3d
- `dist/firmware/FirmwareProvider.js` 3c1e929b01be5fc2
- unblob `processing.py` 599afe91a52fcaa3
- unblob `extractor.py` 1bb498119429ed80
- unblob `extractors/command.py` 8ae7d2a3980b80b2
- unblob `handlers/filesystem/squashfs.py` 2d7b901b54e2ad28

Commands run: `grep -n`/`sed -n` reads on the files above; `strings -n 6 ~/.local/bin/sasquatch | grep …`; `awk`/`uniq -c` on the oracle TSVs; `uv tool list`; `sha256sum … | cut -c1-16`. No rea-agents execution, no unblob run, no sasquatch run, no git mutation, no REA run.
