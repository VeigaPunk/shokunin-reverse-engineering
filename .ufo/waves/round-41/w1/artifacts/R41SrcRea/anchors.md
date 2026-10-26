# R41SrcRea — anchors table for the round-41 SquashFS outcome-triage table v3

Read-only source location. Every line number below was read this round from the installed copies, and
each quoted byte string was verified byte-identical to the published artifact named in the source cell
(sha256 pairs in §6). Nothing here is an extraction outcome except the five `env-*.json` envelopes.

Row ids: highest **existing** row at the base revision is **S126**; S127 (5490) and S128 (5491) are taken
by the sibling `R41SrcAvm` item, so a new row starts at **S129**.

---

## 1. Where the `depth-limited` gap kind is minted, and its fields

| # | document | file:line | quote (≤25 words) | S-row |
|---|---|---|---|---|
| 1.1 | rea-agents 6.5.0 | `dist/firmware/FirmwareReports.js:155` | `const depths = [];` | S119 |
| 1.2 | rea-agents 6.5.0 | `dist/firmware/FirmwareReports.js:229-230` | `if (record.task.depth >= context.maxDepth)` … `depths.push(path);` | S119 |
| 1.3 | rea-agents 6.5.0 | `dist/firmware/FirmwareReports.js:384` | `depth_limited_paths: depths.sort(),` | S119 |
| 1.4 | rea-agents 6.5.0 | `dist/firmware/FirmwarePublication.js:294-299` | `...normalized.depth_limited_paths.map((input_path) => ({ kind: "depth-limited", input_path, ...emptyGap,` | S119 |
| 1.5 | rea-agents 6.5.0 | `dist/firmware/FirmwarePublication.js:39-46` | `const emptyGap = { relative_path: null, handler: null, provider_id: null, range: null, root_file_range: null, dependencies: [], }` | S119 |
| 1.6 | rea-agents 6.5.0 | `dist/domain/firmware/firmwareAnalysis.js:83-104` | "One unextracted region or failing task/stage, with a supported continuation" — strict object, all six kinds, 9 fields | S119 |
| 1.7 | rea-agents 6.5.0 | `dist/domain/firmware/firmwareAnalysis.js:150` | `depth_limited_paths: z.array(z.string()),` | S119 |
| 1.8 | rea-agents 6.5.0 | `dist/firmware/FirmwarePublication.js:23,24-28` | `const MAX_EXTRACTION_DEPTH = 10;` then `maxDepth < MAX_EXTRACTION_DEPTH ? GAP_CONTINUATIONS["depth-limited"]` | S119 |
| 1.9 | rea-agents 6.5.0 | `dist/firmware/FirmwarePublication.js:17` | "Rerun extract_firmware with a higher max_depth (up to 10) and a fresh output_directory to descend into this path." | S119 |
| 1.10 | rea-agents 6.5.0 | `dist/firmware/FirmwarePublication.js:245-272` | `ceilingReached` gates a `reRootablePaths` index of nonempty published children within the input limit | S119 |
| 1.11 | rea-agents 6.5.0 | `dist/cli-runtime/cutterToolContracts-TZH9EHr5.js:1757-1764` | `max_depth: z.number().int().min(1).max(10).default(3).describe("Extraction depth; reaching it yields partial analysis")` | S123 |
| 1.12 | rea-agents 6.5.0 | `dist/cli-runtime/cli.js:15282,15293` | `maxDepth: extractInput.max_depth` … `max_depth: options.maxDepth,` | S123 |

Minting in one sentence: unblob's task at `depth >= max_depth` returns after its `StatReport`
(processing.py:274-279), REA records that task's *logical* path in `depth_limited_paths`
(FirmwareReports.js:229-230 → :384), and `extractionGaps` turns each path into a row whose every
region and identity field except `input_path` is null (FirmwarePublication.js:294-299 over `emptyGap`).

Measured (E1, `--max-depth 1`, own fixture):

```
"depth_limited_paths": ["$output/firmware.bin_extract"]
gap: {"kind":"depth-limited","input_path":"$output/firmware.bin_extract","relative_path":null,
      "handler":null,"provider_id":null,"range":null,"root_file_range":null,"dependencies":[],
      "continuation_id":"3b54e297…"}
files: [{"relative_path":"firmware.bin_extract/inner.sqfs","size":4096,"sha256":"a0652c07…"}]
coverage: "partial"   diagnostics: []
```

The row names the *extract directory*, not a file, and a published regular file already sits under that
same path: "depth-limited" never means "nothing below was published".

## 2. Where `missing-extractor-dependency` is minted (R40-CL5 L3: REA mints the kind)

| # | document | file:line | quote (≤25 words) | S-row |
|---|---|---|---|---|
| 2.1 | rea-agents 6.5.0 | `dist/firmware/FirmwarePublication.js:165` | chunk-nested: `kind: "missing-extractor-dependency", input_path, ...emptyGap,` … `dependencies: [...dependencies],` | S119 |
| 2.2 | rea-agents 6.5.0 | `dist/firmware/FirmwarePublication.js:183-195` | stage-sourced: `.filter(({ kind }) => kind === "missing-extractor-dependency")` → same row shape (handler kept) | S119 |
| 2.3 | rea-agents 6.5.0 | `dist/firmware/FirmwarePublication.js:196-205` | task-wide: `input_path, ...emptyGap, dependencies: [...dependencies],` (no handler, no range) | S119 |
| 2.4 | rea-agents 6.5.0 | `dist/firmware/FirmwarePublication.js:20,177-179,192-194,202-204` | unnamed case: "The producer reported a missing extractor dependency without naming it; its identity is unavailable in this evidence." | S119 |
| 2.5 | rea-agents 6.5.0 | `dist/firmware/FirmwareReports.js:171-188` | `const dependencyNames = (reports) => {` … `return reported ? { names, unnamed } : null;` | S119 |
| 2.6 | rea-agents 6.5.0 | `dist/firmware/FirmwareReports.js:210-223` | `noteChunkMissingDependencies` accumulates chunk-keyed names/unnamed | S119 |
| 2.7 | rea-agents 6.5.0 | `dist/firmware/FirmwareReports.js:320-335` | `kind: dependencies === null ? "extractor-failure" : "missing-extractor-dependency",` | S119 |
| 2.8 | rea-agents 6.5.0 | `dist/firmware/FirmwarePublication.js:239-241` | "Chunks whose failure a dependency row already covers stay out of the generic extractor-failure emission." | S119 |
| 2.9 | rea-agents 6.5.0 | `dist/firmware/FirmwarePublication.js:288-293` | chunk `extractor-failure` filter: `chunk.extraction_failed === true && chunk.handler !== null &&` … `!dependencyChunkKeys.has(...)` | S119 |
| 2.10 | unblob 26.6.4 | `report.py:118-119` | `class ExtractorDependencyNotFoundReport(ErrorReport):` "Describes an error when the dependency of an extractor doesn't exist." | S120 |
| 2.11 | unblob 26.6.4 | `extractors/command.py:69-77` | `except FileNotFoundError:` → `ExtractorDependencyNotFoundReport(dependencies=self.get_dependencies())` → `raise ExtractError(...)` | S120 |
| 2.12 | unblob 26.6.4 | `extractors/command.py:101-102` | `def get_dependencies(self) -> list[str]: return [self._executable]` | S120 |
| 2.13 | unblob 26.6.4 | `handlers/filesystem/squashfs.py:37-54` | `executable = self.EXECUTABLE` … `case Endian.BIG, 4: executable = self.V4BE_EXECUTABLE` | S112 |
| 2.14 | unblob 26.6.4 | `handlers/filesystem/squashfs.py:68-69` | `return [self.EXECUTABLE, self.V4BE_EXECUTABLE]` (handler list — **not** what the gap carries) | S112 |

Minting in one sentence: unblob raises a *report class*, `ExtractorDependencyNotFoundReport`, whose
`dependencies` are the single executable the chosen `Command` ran (command.py:101-102); REA parses that
class (FirmwareReports.js:171-188), decides the kind string (FirmwareReports.js:332-334 and
FirmwarePublication.js:165/186/198) and suppresses the parallel generic `extractor-failure` row for the
same chunk (FirmwarePublication.js:239-241, 288-293).

Measured negative: `grep -rn "missing-extractor-dependency\|extractor-failure\|depth-limited"` over the
installed unblob package returns **0** matches in 26.6.4 — the three kind strings exist only in REA.

Measured (E3/E4, sasquatch unreachable — `$HOME/.local/bin` stripped from the child `PATH`):

```
E3 LE image : handler "squashfs_v4_le", dependencies ["sasquatch"],        chunk extraction_failed true
E4 AVM image: handler "squashfs_v4_be", dependencies ["sasquatch-v4be"],   chunk extraction_failed true
diagnostics[0] = {input_path, stage, missing_dependencies:["sasquatch-v4be"],
                  report:{__typename__:"ExtractorDependencyNotFoundReport", severity:"ERROR",
                          dependencies:["sasquatch-v4be"]}}
```

So the gap names **only the executable that branch chose** (v4be on the AVM marker path), never the
handler's two-name list — a v3 cell that expects `[sasquatch, sasquatch-v4be]` from a v4be-only absence
would be false.

## 3. unblob's empty-target symlink branch that removes the link with no report (L6)

| # | document | file:line | quote (≤25 words) | S-row |
|---|---|---|---|---|
| 3.1 | unblob 26.6.4 | `extractor.py:67-71` | `raw_target = os.readlink(path)` … `if not raw_target:` … `logger.error("Symlink with empty target, removing.")` … `path.unlink()` … `return path` | S118 |
| 3.2 | unblob 26.6.4 | `extractor.py:58-65` | loop branch: `is_recursive_link(path)` → `MaliciousSymlinkRemoved` → `task_result.add_report(error_report)` | S118 |
| 3.3 | unblob 26.6.4 | `extractor.py:81-87` | unsafe branch: `if not safe:` → `MaliciousSymlinkRemoved` → `task_result.add_report(error_report)` → `path.unlink()` | S118 |
| 3.4 | unblob 26.6.4 | `extractor.py:95-113` | `fix_extracted_directory` → `if path.is_symlink(): fix_symlink(path, outdir, task_result)` | S118 |
| 3.5 | sasquatch 4.5.1 | `squashfs-tools/unsquashfs.c:1199-1205` | `res = symlink(i->symlink, pathname);` … `EXIT_UNSQUASH_STRICT("create_inode: failed to create symlink %s, because %s\n",` | S121 |

The branch is silent: unlike 3.2 and 3.3 it never constructs a report, so an envelope cannot show it and
REA's inventory (which runs after unblob's sanitising) never sees the link either.

**Reachability probe (new this round, cheap, negative).** An extractor cannot create the input to this
branch on Linux, because `symlink(2)` refuses an empty target:

```
$ ln -s '' empty            -> ln: failed to create symbolic link 'empty': No such file or directory (exit 1)
$ python3 -c "import os; os.symlink('','x')" -> FileNotFoundError [Errno 2] No such file or directory
```

and sasquatch writes links with that same call (3.5). A row scored on "empty-target symlink removed" is
therefore not reproducible from any SquashFS image by sasquatch 4.5.1; L6 is a prose fact (the branch
exists, is silent, and is unreachable through this extractor), not a scorable class. [INFERENCE] for
filesystems other than the host's that might accept an empty target.

## 4. Where `extractor-failure` gaps carry published files (partial)

| # | document | file:line | quote (≤25 words) | S-row |
|---|---|---|---|---|
| 4.1 | rea-agents 6.5.0 | `dist/firmware/FirmwareReports.js:284` | `const extractionFailed = detail !== null && detail.extraction_reports.length > 0;` | S119 |
| 4.2 | rea-agents 6.5.0 | `dist/firmware/FirmwareReports.js:295-308` | `chunks.push({` … `extraction_failed: extractionFailed,` | S119 |
| 4.3 | rea-agents 6.5.0 | `dist/firmware/FirmwarePublication.js:225-238` | `const chunkGaps = (kind, matches) => normalized.chunks.filter(matches).map((chunk) => ({ kind, input_path, ...emptyGap, handler, provider_id, range, root_file_range,` | S119 |
| 4.4 | rea-agents 6.5.0 | `dist/firmware/FirmwarePublication.js:275-285` | stage row: `kind: "extractor-failure", input_path, ...emptyGap, handler, provider_id, dependencies: [],` | S119 |
| 4.5 | rea-agents 6.5.0 | `dist/firmware/FirmwareFiles.js:121-188` | "Inventory private output without following links, enforcing aggregate staging budgets." — whole tree, no per-chunk filter | S119 |
| 4.6 | rea-agents 6.5.0 | `dist/firmware/FirmwarePublication.js:58-64` | `const materialized = new Set(context.entries.filter((entry) => entry.kind === "file")` … throws if a reported file is absent | S119 |
| 4.7 | rea-agents 6.5.0 | `dist/firmware/FirmwarePublication.js:68-98` | every non-`file` entry becomes `unpublished`; every file is hashed, cross-checked and written | S119 |
| 4.8 | rea-agents 6.5.0 | `dist/firmware/FirmwareReports.js:419-423` | `coverage: depths.length > 0` (or a diagnostic, or a null-handler or encrypted chunk) … `? "partial" : "complete"` | S119 |
| 4.9 | unblob 26.6.4 | `processing.py:666-670` | `except ExtractError as e: extraction_reports.extend(e.reports)` | **S129 (new)** |
| 4.10 | unblob 26.6.4 | `processing.py:677-679` | "we want to get consistent partial output even in case of unforeseen problems" → `fix_extracted_directory` → `delete_empty_extract_dir` | **S129 (new)** |
| 4.11 | unblob 26.6.4 | `processing.py:681-688` | `if extract_dir.exists(): self.result.add_subtask(Task(..., depth=self.task.depth + 1))` | **S129 (new)** |
| 4.12 | unblob 26.6.4 | `processing.py:746-748` | `if extract_dir.exists() and not any(extract_dir.iterdir()): extract_dir.rmdir()` | **S129 (new)** |
| 4.13 | unblob 26.6.4 | `processing.py:55,274-279` | `DEFAULT_DEPTH = 10` … `if task.depth >= self._config.max_depth:` → `return` after `StatReport` | **S129 (new)** |
| 4.14 | unblob 26.6.4 | `extractors/command.py:59-68` | `if res.returncode != 0:` → `ExtractCommandFailedReport(command, stdout, stderr, exit_code)` → `raise ExtractError(error_report)` | S120 |
| 4.15 | unblob 26.6.4 | `handlers/filesystem/squashfs.py:56-64` | argv tail `"-no-exit-code", "-f", "-d", "{outdir}", "{inpath}"` | S112 |
| 4.16 | sasquatch 4.5.1 | `squashfs-tools/unsquashfs.c:4019-4021` | `else if(strcmp(argv[i], "-no-exit-code") == 0` … (or its `-no-exit` alias) → `set_exit_code = FALSE;` | S121 |
| 4.17 | sasquatch 4.5.1 | `squashfs-tools/unsquashfs.c:4575-4618` | `if(res == FALSE && set_exit_code) exit_code = 2;` ×3 … `return exit_code;` | S121 |

Answer in one sentence: the gap row itself carries **no** file reference (`...emptyGap` nulls
`relative_path`; `dependencies: []`), while the published files are whatever the staging tree already
holds (4.5-4.7) because unblob keeps partial output and only deletes an empty extract dir (4.9-4.12) —
so "partial" is a property of the *result*, never of the gap row.

Measured (E5, fatal body failure) vs (E1):

```
E5: coverage "partial"  files []  gap {kind:"extractor-failure", handler:"squashfs_v4_le",
    provider_id:"3685440:1", range:{offset:0,length:8192}, dependencies:[]}
    diagnostics[0].report = {__typename__:"ExtractCommandFailedReport", severity:"WARNING",
      exit_code:1, command:"sasquatch -le -no-exit-code -f -d …/firmware.bin_extract …/firmware.bin",
      stderr: base64 of "read_fragment_table: failed to read fragment table index\nFATAL ERROR: File system corruption detected\n"}
E1: coverage "partial"  files [inner.sqfs]  gap {kind:"depth-limited", …}
E3: coverage "partial"  files []  chunk extraction_failed=true, single dependency row, no extractor-failure row
```

`-no-exit-code` is visible inside the diagnostic's own `command` string — and it is why a **non-fatal**
partial sasquatch run returns 0 (4.16-4.17) and produces no `extractor-failure` row at all: only fatal
paths (`exit(1)` / `EXIT_UNSQUASH*`, e.g. 3.5's strict macro) survive the suppression. I confirmed one
fatal path end-to-end (E5, exit 1 with and without the flag) and did **not** construct a fatal failure
that leaves files behind (P>0 + `extractor-failure`); see the report's limits.

---

## 5. S-row disposition (for the L1)

| target | document | disposition |
|---|---|---|
| 1 (mint + fields), 2 (kind mint), 4.1-4.8 (REA side) | rea-agents 6.5.0 tarball | **Existing S119** — extend its anchor with the line ranges in §1/§2/§4 and widen `teaches` to cover the depth row and the gap-does-not-carry-files rule. No new row: the tarball digest is already pinned by S119 (and S123). |
| 1.11-1.12 (`max_depth` input cell, CLI flag) | same tarball | **Existing S123** — extend anchor (`cutterToolContracts-TZH9EHr5.js:1757-1764`, `cli.js:15282-15295`); its scope already owns "the operation catalog and CLI command map", add "and the `extract_firmware` input cell". |
| 2.10-2.12 (report class, raise site, one-name dependencies) | unblob `report.py`, `extractors/command.py` | **Existing S120** — extend anchor with `command.py:59-77,101-102` and `report.py:118-119`; `teaches` already says the report names the one executable. |
| 2.13-2.14 (which executable each endianness branch runs) | unblob `handlers/filesystem/squashfs.py` | **Already inside S112** — its anchor cites `SquashFSExtractor` `lines 24-70`, which contains `:37-54` and `:68-69`. No anchor change. The *fact* the v3 cell needs (the gap carries the one chosen executable, not this two-name handler list) lands on S119/S120 above. |
| 3.1-3.4 (empty-target silence) | unblob `extractor.py` | **Existing S118** — extend anchor with `:58-71,95-113`; widen scope to "and the empty-target removal it performs without a report". |
| 3.5, 4.16-4.17 (symlink(2) writer, exit-status control) | sasquatch `unsquashfs.c` | **Existing S121 covers the document** (same file, digest `ece42b66…` re-verified today). Two options for the L1: extend S121's anchor + scope, or mint **S130** on the same document if one-fact-per-row is preferred. Draft S130 text is in `row-drafts.md`. |
| 4.9-4.13 (partial-output retention, depth gate, empty-dir deletion) | unblob `processing.py` | **No row covers this document** (`grep processing.py corpus/SOURCES.md` → 0 hits). Draft **S129** in `row-drafts.md`. |

## 6. Identity checks run today (2026-10-26)

| document | check |
|---|---|
| rea-agents 6.5.0 tarball | re-downloaded, sha256 `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699` = S119/S123 pin; the five files cited here are byte-identical inside the tarball and in the installed copy (`FirmwarePublication.js` `bb4f3246…`, `FirmwareReports.js` `6885966b…`, `FirmwareFiles.js` `f6934b7b…`, `firmwareAnalysis.js` `2cbc1cc4…`, `package.json` `a5003023…`) |
| unblob 26.6.4 `extractor.py` | HTTP 200, 4129 B, sha256 `1bb49811…` = S118 pin = installed copy |
| unblob 26.6.4 `report.py` | 10553 B, sha256 `2329783f…` = S120 pin = installed copy |
| unblob 26.6.4 `file_utils.py` | 27989 B, sha256 `87d4dc9a…` = S122 pin = installed copy |
| unblob 26.6.4 `processing.py` | HTTP 200, 32013 B, sha256 `599afe91a52fcaa308ad3c36ea58172c1d8de4d9c11cab92ad94130bd7671826` = installed copy |
| sasquatch `unsquashfs.c` @ `sasquatch-v4.5.1-6` | HTTP 200, 120167 B, sha256 `ece42b66f37ba67707c2c51b47b643c027232153705f59d238da79958a54cb40` = S121 pin |
| sasquatch `unsquashfs.h` @ same tag | HTTP 200, 8443 B, sha256 `b2061930b21b7c8b34d2d4c15f41f7b80b5371976ac597d3d30534e19024251d` (contains no `EXIT_UNSQUASH` definition — that macro's body was not traced) |
| REA 6.5.0 / unblob 26.6.4 / sasquatch 4.5.1 versions used by the five probes | envelope `provider.version` `26.6.4`, `engine.executable_sha256` `0ce7b624…`, `engine.version` `26.6.4`; diagnostics' `command` shows the `sasquatch` argv |
