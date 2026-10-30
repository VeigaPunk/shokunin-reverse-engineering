# RevExtractor — extract-firmware disposition path (rea-agents 6.5.0, read-only)

Scope: read-only source analysis of `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`
(called `PKG` below), plus read-only inspection of lane receipts and the installed unblob 26.6.4 source
(`~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob`, called `UNBLOB` below). Nothing was
executed in `PKG`; no probe, no sasquatch/unsquashfs run, no REA run.

Citation conventions:
- `dist/firmware/X.js:N` = module source (`PKG/dist/firmware/X.js`).
- `cli.js:N` = the bundled copy `PKG/dist/cli-runtime/cli.js`. This is the file the CLI actually
  executes: `scripts/rea.mjs:44` lists it in `runtimeFiles` and `scripts/rea.mjs:68` imports it. The
  r50 receipts were produced through this path (`argv_shell` in `corpus/evidence/round-50/c1/c6430/run.json`:
  `npx -y rea-agents@6.5.0 extract-firmware ...`). Line numbers differ from the module files; I verified each
  bundle line cited below with grep.
- `UNBLOB:path:N` = installed unblob source.

Vocabulary used in the answers: "producer" = unblob 26.6.4 (+ sasquatch 4.5.1 for squashfs); "poll" = the
in-run inventory loop in `FirmwareCommand.js`.

---

## Pipeline in one screen (what the verb does)

1. `FirmwareProvider.js:227-245` (cli.js:15109-15131) spawns `unblob` through `runFirmwareCommand` with
   `--process-num 1 --depth <max_depth> --randomness-depth 0 --report <r> --log <l> --extract-dir <outputRoot> <input>`.
   **No** `--extracted-file-deletion` flag is passed. `outputRoot = join(root.path, "extracted")`
   (`FirmwareProvider.js:226`, cli.js:15109). The run is given an `outputBudget` (`FirmwareProvider.js:241-245`).
2. While the producer runs, `runFirmwareCommand` polls: every 100 ms it calls
   `inventoryFirmwareOutput(outputBudget.root, ...)` (`FirmwareCommand.js:106-114`; cli.js:14481).
3. After the producer is stopped (`FirmwareCommand.js:122`), `FirmwareProvider.js:252-257` normalizes the
   report (`normalizeUnblobReport`), then `FirmwareProvider.js:260` runs the final inventory (cli.js:15142),
   then `publishFirmwareExtraction` (`FirmwareProvider.js:261-278`).
4. `publishFirmwareExtraction` (`FirmwarePublication.js:54-…`) builds `files`, `unpublished_entries`, and
   `extraction_gaps` (`FirmwarePublication.js:208-…`, `extractionGaps`).

---

## (1) Where `unpublished_entries` is computed, and from what comparison

**Computed from a disk walk, filtered by kind. It is not a comparison against any staged list or report.**

- The input is `context.entries`, produced by `inventoryFirmwareOutput(outputRoot, …)` at
  `FirmwareProvider.js:260`. That function is a full recursive walk of `extracted/`: `opendir` per directory
  (`FirmwareFiles.js:141`), `lstat` per named entry (`FirmwareFiles.js:156-166`), directories pushed to the
  work list and never emitted (`FirmwareFiles.js:167-170`), and every non-directory emitted with
  `kind = symlink | file | special` (`FirmwareFiles.js:175-185`; cli.js:14020-14036).
- `publishFirmwareExtraction` builds `unpublished` by `for (const entry of context.entries) if (entry.kind !== "file") unpublished.push({relative_path, kind, link_target})` (`FirmwarePublication.js:68-77`; cli.js:14099-14106).
  It is returned as `unpublished_entries: unpublished` (`FirmwarePublication.js:105`; cli.js:14139) and makes
  `coverage` "partial" (`FirmwarePublication.js:103`).
- The **only** comparison against the producer report is one-directional and covers regular files only:
  every reported regular file must appear in the materialized set (`FirmwarePublication.js:58-64`; cli.js:14099),
  and reported sha256/size must agree with disk (`FirmwarePublication.js:77-85`; cli.js:14116). Disk entries
  absent from the report are **not** checked in either direction, and disk symlinks/specials are never checked
  against the report at all.
- Gap rows for unpublished entries: `FirmwarePublication.js:301-307` (`unpublished.map(...)` →
  `kind: "unpublished-entry"`, `input_path: "$output/<rel>"`, continuation `GAP_CONTINUATIONS["unpublished-entry"]`
  at `FirmwarePublication.js:18`); bundle at cli.js:14279-14283.
- Schema: `unpublished_entries.kind` is `enum["symlink","special"]` (`dist/domain/firmware/firmwareAnalysis.js:137-141`).
  `extractionGap.kind` includes `unpublished-entry` (`firmwareAnalysis.js:83-91`).

So: "staged inventory" = the disk walk of `extracted/`. There is no separate staged-by-handler list anywhere
in the REA firmware path.

---

## (2) Why a char-device oracle entry produces NEITHER a gap NOR a removal

**Short answer:** the disk walk would have caught a device node if one were on disk. None is on disk. The
producer never creates it, and the producer's failure is discarded without a report. So the omission is
silent at every layer REA owns. There is no per-entry "removal" mechanism in REA's firmware path at all.

### 2a. REA's walk would classify a device, so the walk is not the reason
- The walk does `lstat` every named entry (`FirmwareFiles.js:156-166`) and classifies anything that is not a
  symlink and not a file as `special` (`FirmwareFiles.js:179-183`; cli.js:14035). Specials are not skipped
  (`FirmwareFiles.js:171-186`). The schema allows `special` (`firmwareAnalysis.js:139`).
- Therefore, **had** `dev/led` been on disk, REA would have produced `unpublished_entries[{kind:"special"}]`
  and gap `unpublished-entry` for `$output/…/dev/led`. The walk is not scoped to handler-staged entries, and it
  does stat device nodes. The scoping question resolves to: nothing staged.

### 2b. The squashfs producer does not create the node
- unblob's squashfs handler runs sasquatch: `Command(executable, "-le"|"-be", "-no-exit-code", "-f", "-d", "{outdir}", "{inpath}")`
  (`UNBLOB:handlers/filesystem/squashfs.py:56-66`). No device-handling flag is passed. `-no-exit-code`
  makes the exit status 0 regardless of per-entry failures.
- unblob's `Command.extract` captures stderr through `subprocess.PIPE` (`UNBLOB:extractors/command.py:52-58`),
  and builds an `ExtractCommandFailedReport` only when the return code is nonzero (`command.py:59-68`). On
  success nothing retains stderr. So the sasquatch message never reaches the report.
- The sasquatch binary used by REA is the same as the oracle's. Its SHA-256 `ad02d27a…` matches
  `corpus/evidence/round-50/c1/c6430/run.json` (`.sasquatch.sha256`) and
  `.ufo/waves/round-50/l1/oracle/c6430/oracle-run.json` (`sasquatch.sha256`). The binary contains the format
  string `could not create %s device %s, because you're not superuser!` (grep of `~/.local/bin/sasquatch`).
- Receipt evidence: `.ufo/waves/round-50/l1/oracle/c6430/oracle-run.json` has
  `sasquatch.log_head = "create_inode: could not create character device …/sq/root/dev/led, because you're not superuser! …"`,
  `sasquatch.exit = 0`, `crosscheck.special_in_listing = 1`, and `crosscheck.sasquatch_nonregular_in_tree = 823`
  against 824 nonregular oracle entries (255 dirs + 568 symlinks + 1 device; the device is the one missing).
- REA side of the same carrier: `corpus/evidence/round-50/c1/c6430/after.json` `normalized_result.unpublished_entries`
  contains 567 `symlink` rows and **no** `special` row (checked by value, not string match).
- Oracle inventory of char devices: `tools/round-50/oracle/c6430.nonregular.tsv:63` `dev/led char-device 247:0`;
  g7581/g7582 have 13 (`dev/led`, `dev/pts/0..7`, `dev/tiatm`, `dev/ttyp0..2`); c6490 has 1.

### 2c. Removal: what REA and unblob actually have
- REA has **no per-entry removal diagnostic** for firmware. The only removal in REA is
  `SafeOutputTree.rollback` (`dist/artifacts/SafeOutputTree.js:217-261`), which deletes the whole unsealed
  output tree, not individual entries. There is no `removed` field in `firmwareAnalysis.js`.
- unblob's `"Ignoring special file (link, chrdev, blkdev, fifo, socket, door)."` (`UNBLOB:processing.py:286-290`)
  is a **debug** log for a `StatReport` whose `is_file` is false. It applies to tasks, not to sasquatch's
  output, and emits no report.
- unblob's `ExtractedFileDeletedReport` (`UNBLOB:processing.py:691-720`) runs only when
  `extracted_file_deletion != NONE` (`UNBLOB:processing.py:110, 729-731`). REA does not pass the flag
  (`FirmwareProvider.js:227-239`), so this path is not reachable in the default REA run. If enabled, REA would
  put it in `diagnostics`, because it is not in REA's `known` set (`FirmwareReports.js:65-74`, `253-255`).

**Conclusion for (2):** silent omission. Producer drops the node (sasquatch, exit 0, stderr discarded), REA's
walk never sees it, no gap, no diagnostic, no removal row. Coverage is "partial" in these receipts only
because of other gaps (depth, symlink rows). A char device alone would not make the envelope partial.

---

## (3) Where the depth-limited gap comes from; does the envelope carry input_path / continuation_id?

**Origin.**
- Producer: `UNBLOB:processing.py:274-279` — when `task.depth >= max_depth`, unblob logs and returns after the
  `StatReport` (already added at `processing.py:270-271`). The task therefore appears in the report with only a
  `StatReport`.
- REA: `FirmwareReports.js:225-230` — for every producer record, `path = logical(record.task.path)`;
  `if (record.task.depth >= context.maxDepth) depths.push(path)` (cli.js:14741). A `StatReport` is required
  (`FirmwareReports.js:231-233`), which the producer always supplies (see above).
- Top-level list: `depth_limited_paths: depths.sort()` (`FirmwareReports.js:384`).
- Gap row: `FirmwarePublication.js:294-300` — `{kind:"depth-limited", input_path, relative_path:null, handler:null, provider_id:null, range:null, root_file_range:null, dependencies:[], continuation_id: depthContinuationId(input_path)}` (cli.js:14272-14278).
- `depthContinuationId` (`FirmwarePublication.js:264-270`) interns the instruction text into `extraction_continuations`
  (`FirmwarePublication.js:317`, `continuation(instruction)` at `FirmwarePublication.js` `continuation` helper in `extractionGaps`).

**Envelope fields.** Yes, both are carried.
- Schema: `extractionGap.input_path: string` and `continuation_id: string` are required (`firmwareAnalysis.js:92-103`);
  `extraction_continuations: [{id, instruction}]` (`firmwareAnalysis.js:154`).
- Live example, `corpus/evidence/round-50/c1/c6430/after.json` `normalized_result.extraction_gaps[depth-limited]`:
  `{"kind":"depth-limited","input_path":"$output/firmware.bin_extract","relative_path":null,…,"continuation_id":"3b54e297…"}`
  and the instruction "Rerun extract_firmware with a higher max_depth (up to 10) and a fresh output_directory…".
  Same shape in c6490, g7581, g7582 (`depth_limited_paths: ["$output/firmware.bin_extract"]`; max-depth 1 in
  these runs).

**Caveats for r52 `depth_gap_recorded`.**
- `range`, `root_file_range`, `relative_path`, `handler`, `provider_id` are all null for depth rows. If the clause
  requires a byte range or a relative path it cannot be satisfied by the envelope. `input_path` is the only
  locator, and it names a directory (the squashfs output root), not a file.
- Files beneath a depth-limited directory are still published as regular files at `analysis_depth` = the depth
  reported by the producer (`FirmwarePublication.js` `files.push`, `analysis_depth: reported?.depth`). The envelope
  does not mark them as beyond-budget.
- The continuation text differs when `max_depth` = 10 (`FirmwarePublication.js:23-28`, `reRootablePaths` at
  `FirmwarePublication.js:247-263`). Not exercised in r50.

---

## (4) Where the readlink ENOENT class comes from; is the race plausible?

**Observed string.** `.ufo/waves/round-40/w2/R40W2C2RegenB.md` §6 (lines ~150–160):
`ENOENT: no such file or directory, readlink '/tmp/rea-firmware-pAY6tQ/extracted/firmware.bin_extract/m1l5kvd/ke9e0'`
on H10 (1 of 17 H10 invocations; 1 of 58 in the seat; 0 of 28 in the follow-up). Two facts from the note: the
path is under `extracted/` (the outputRoot, `FirmwareProvider.js:226`), and `ke9e0` is a **relative** in-tree
link (`m1l5kvd/ke9e0 → ../5z5b5p5d4`).

**Wrapping.** A non-`AnalysisError` thrown in `#execute` becomes `ProviderAdapterError` with
`diagnostics.reason = cause.message` (`FirmwareProvider.js:302-320`). That is the envelope shape in the note
(`details.provider_id:"unblob"`, `operation:"extract_firmware"`, `diagnostics.reason:"ENOENT…"`). Consistent.

**Unguarded readlink sites.**
- **A. `FirmwareFiles.js:184` (cli.js:14036)** inside `inventoryFirmwareOutput`. The `lstat` right before it is
  ENOENT-guarded (`FirmwareFiles.js:158-166`), so an entry that vanishes **before** `lstat` is skipped. The
  `readlink` is not guarded. An entry that vanishes **between** `lstat` and `readlink` throws.
  - Callers: (i) the **poll** `FirmwareCommand.js:112-113` (cli.js:14481), which runs every 100 ms **while the producer
    is still running**; (ii) the final inventory `FirmwareProvider.js:260` (cli.js:15142), which runs only after
    `supervisor.stop()` (`FirmwareCommand.js:122`). The final call cannot race a stopped producer. **The
    concurrent caller is the poll.**
  - Propagation from the poll: the throw is caught at `FirmwareCommand.js:119-121` (cli.js:14486), the producer is
    stopped (`:122`), then `throw failure` (`FirmwareCommand.js:139-140`, cli.js:14505). The whole extraction fails
    with no retry. That matches the R40W2C2RegenB note (§6): the first attempt failed and the retry succeeded.
- **B. `FilesystemSnapshot.js:169`** (cli.js:23371), process-capture "symlink projection". `visit` does
  `lstatIfPresent` (`:164`), then `readlink` (`:169`), then `lstat` again (`:170`), with no ENOENT handling. This is
  the closest match to "symlink projection walking a deleted entry", and it has the same window shape. The file
  branch of the same function handles ENOENT as an omission (`hashFile`, `FilesystemSnapshot.js:52-70`), so the
  symlink branch is inconsistent with it. Errors are normalized at `dist/process/capture/ProcessHarness.js:561-574`
  (`captureProcessScenario` → `normalizeCaptureFailure`), so it fails as a classified execution failure, not a
  crash. **No receipt in the lane contains this site's error.** The lane's ENOENT receipts are firmware's (path
  under `rea-firmware-*/extracted/`).
- **Guarded for contrast:** `ReferenceSourceReaderEntries.js:203-236` (`readStableSymlinkTarget` maps ENOENT/ENOTDIR
  to `changedSymlink`); `dist/cli-runtime/artifacts__ArtifactProvider-zXI0QjSL.js:451-464` (`lstat` and `readlink` inside
  one `try`, `missing(cause)` → undefined); `dist/artifacts/apple/DylibResolutionReader.js:54-65`.

**Producer-side writer (the racing party).** The window is created by unblob, not by sasquatch:
- `UNBLOB:extractor.py:95-113` `fix_extracted_directory` walks the extraction directory and calls
  `fix_symlink` for every symlink (`extractor.py:102-104`).
- `fix_symlink` (`extractor.py:50-92`), for an inside-safe link, does `path.unlink()` (`:90`) and then
  `path.symlink_to(relative_target)` (`:91`). **Every** in-tree symlink that passes the safety check is therefore
  unlinked and recreated during the producer run. The H10 link is exactly this kind (relative, in-tree).
- Callers: `UNBLOB:processing.py:447`, `:654`, `:678`. All run inside the producer process, while REA's poll is active.

**Window, named.**
- Producer: between `path.unlink()` (`extractor.py:90`) and `path.symlink_to()` (`extractor.py:91`), the name is
  absent. This is a same-process pair of syscalls with Python code in between (microseconds).
- REA: poll `lstat` (`FirmwareFiles.js:158`) sees the old symlink; `readlink` (`FirmwareFiles.js:184`) executes after
  the producer's unlink and before its re-create. REA's side is wider than the producer's, because the `readlink` is
  dispatched to the libuv threadpool after the `lstat` resolves, and it can queue behind other fs work.
- **Verdict: plausible, low per-event probability, and consistent with the observed rate** (1/17 on the one
  carrier with many in-tree links; 0/28 on the follow-up). The number of rewritten links per carrier (568 in
  c6430) gives many chances per run. The race is between the producer's unlink/re-create and REA's poll, not a
  deleted-entry projection.
- Not established: whether sasquatch's `-f` (force overwrite) also unlinks existing entries. That would be a second
  writer in the same window. It needs sasquatch source, which is not in the tree (inference).

**Fix surface (for the L1, not a change I made):** the poll does not need to fail on a vanished entry, and a
`readlink` ENOENT after a successful `lstat` should be treated like the guarded `lstat` ENOENT (skip). Alternatively,
the in-run poll could skip symlink targets altogether, because the final inventory covers them.

---

## Additional findings (in scope of the claims)

### F1. The "removal diagnostics" are unblob's `MaliciousSymlinkRemoved`; they never become gaps
- Producer: `UNBLOB:extractor.py:58-65` (symlink loop: `path.unlink()` at `:64`), `:77-87` (traversal: `path.unlink()` at
  `:87`). Report class: `UNBLOB:report.py:133-138`.
- REA normalization: the typename is not in the `known` set (`FirmwareReports.js:65-74`), so it goes to
  `diagnostics` with `input_path` = the **attributing task** (`FirmwareReports.js:253-255`). No
  gap row is produced for it. `coverage` becomes partial through `diagnostics.length > 0` (`FirmwareReports.js:419-423`).
- Live data, all four carriers (`corpus/evidence/round-50/c1/*/after.json`, `normalized_result.diagnostics`):
  - c6430 and c6490: 1 `MaliciousSymlinkRemoved`, `link …/firmware.bin_extract/usr/www/avm/cgi-bin/system_status`,
    `target "usr/www/cgi-bin/system_status"`, `input_path "$input"`.
  - g7581 and g7582: 3, for `dev/log` (target `/var/tmp/log`), `usr/www/avm/cgi-bin/system_status`, and
    `usr/www/avme/cgi-bin/system_status`.
- These are exactly the symlinks missing from REA's `unpublished_entries` versus the oracle:
  - c6430 oracle 568 vs REA 567; missing `usr/www/avm/cgi-bin/system_status`.
  - g7581 oracle 639 vs REA 636; missing `dev/log`, `usr/www/avm/cgi-bin/system_status`, `usr/www/avme/cgi-bin/system_status`.
  - c6490 and g7582 follow the same pattern (see the diff I ran on the four receipts).
- So gap accounting for symlinks does not reconcile against the oracle unless MSR diagnostics are counted. The
  diagnostics row carries the wrong `input_path` (`$input`, not the removed link's `$output/…`) and the **private
  staging path** in `link` (`/fast/scratch/hyaku/kaidoku-r50/c1-run.*/rea-firmware-*/extracted/…`), which is not a
  logical path and cannot be joined to a gap.
- Trigger (inference, not probed): `fix_symlink` decides safety with `Path.resolve()` (`extractor.py:77`, `:79`),
  which follows other in-tree links. If a link's resolution crosses a not-yet-rewritten absolute link, `resolve()`
  reaches a host path and the check fails. Processing order is `iterdir()` order (`extractor.py:99`), so the removal
  set may depend on directory-entry order. The removed links all have absolute targets in the oracle
  (`c6430.nonregular.tsv:729`, `:817`; `usr/www/avm/cgi-bin/*` → `/usr/www/cgi-bin/*`). A permutation probe would
  test this; I did not run one.

### F2. Silent-loss inventory, summarized for the L1 law
| carrier | oracle symlinks | REA symlink rows | MSR removals (diag) | oracle char devices | REA special rows | REA gaps (depth/unpub) |
|---|---|---|---|---|---|---|
| c6430 | 568 | 567 | 1 | 1 | 0 | 1 / 567 |
| c6490 | 613 | 612 | 1 | 1 | 0 | 1 / 612 |
| g7581 | 639 | 636 | 3 | 13 | 0 | 1 / 636 |
| g7582 | 639 | 636 | 3 | 13 | 0 | 1 / 636 |

(Counts from the committed `after.json` and `tools/round-50/oracle/*.nonregular.tsv`. Oracle symlink counts come
from the `symlink` rows of each nonregular TSV.)

Under the current REA rules, no row in this table is a gap except the symlinks REA sees on disk and the one depth
row. The 1/3 MSR symlinks and the 1/13 char devices per carrier are unaccounted for by any envelope row other than
the diagnostics list (MSR only).

### F3. Minor: MSR link paths leak private staging roots
`diagnostics[].report.link` carries absolute paths under the run's private root (see F1). Not a claim issue by
itself, but the r52 bindings should not compare those strings across runs.

---

## Confidence
- (1) Computed from the disk walk, filtered by kind: **high** (code, `FirmwarePublication.js:68-77`, `FirmwareProvider.js:260`).
- (2a) The walk would gap a device if one were on disk: **high** (code). (2b) The device is not created: **high** on the
  receipts plus the unblob code; the sasquatch source itself is not local (the message text and exit-0 are observed).
  (2c) No per-entry removal in REA: **high**.
- (3) Depth gap and both envelope fields present: **high** (code plus `after.json`). The r52 `depth_gap_recorded`
  requirement is unknown to me; the envelope cannot carry a byte range for it.
- (4) Source of the ENOENT string: **high** that it is firmware's `FirmwareFiles.js:184` via the poll
  (`FirmwareCommand.js:112-113`), because the final inventory cannot race a stopped producer. The window mechanism
  (unblob's `unlink`/`symlink_to` in `extractor.py:90-91`): **medium** (code-path reasoning; not reproduced).
  The `FilesystemSnapshot.js:169` site is a same-shape unguarded readlink with no receipt: **high** on the code, no
  observed occurrence.
- F1 trigger (`resolve()` order dependence): **low-to-medium** (inference; needs a probe).

## What was not done
- No execution of anything in `PKG`, no probe, no sasquatch/unsquashfs run, no REA run.
- No check of sasquatch's own source for `-f` unlink semantics (not in the tree).
- The depth-limited and ENOENT behaviour for `max_depth = 10` was not exercised.
